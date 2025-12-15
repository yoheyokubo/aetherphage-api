# app/main.py
from typing import List

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.models.ranker import PhageHostRanker
from app.utils.fasta import load_single_fasta_sequence
from app.utils.encoding import encode_sequence
from app.utils.dataset import load_host_candidates, load_phage_candidates

app = FastAPI(
    title="Phage-Host Interaction API",
    description=(
        "Minimal API for phage–host interaction ranking on the Cherry dataset.\n"
        "Supports both JSON-based and file-upload-based queries."
    ),
    version="0.2.0",
)

# Load model and dataset metadata at startup.
ranker = PhageHostRanker(model_path=None)  # TODO: set model path when ready
host_candidates = load_host_candidates()
phage_candidates = load_phage_candidates()


class PhageQuery(BaseModel):
    phage_fasta: str
    top_k: int = 10


class HostQuery(BaseModel):
    host_fasta: str
    top_k: int = 10


@app.get("/health")
def health_check():
    """
    Lightweight health check endpoint.
    """
    return {"status": "ok"}


# ------------------------------
# JSON-based endpoints
# ------------------------------


@app.post("/predict/phage")
def predict_hosts(query: PhageQuery):
    """
    (1) Accept a phage genome in FASTA text and rank hosts in the dataset.
    """
    try:
        seq = load_single_fasta_sequence(query.phage_fasta)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if query.top_k <= 0:
        raise HTTPException(status_code=400, detail="top_k must be positive.")

    encoded = encode_sequence(seq)
    results = ranker.rank_hosts_for_phage(encoded, host_candidates, top_k=query.top_k)

    return {
        "query_type": "phage_to_host",
        "top_k": query.top_k,
        "num_candidates": len(host_candidates),
        "results": results,
    }


@app.post("/predict/host")
def predict_phages(query: HostQuery):
    """
    (2) Accept a host genome in FASTA text and rank phages in the dataset.
    """
    try:
        seq = load_single_fasta_sequence(query.host_fasta)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if query.top_k <= 0:
        raise HTTPException(status_code=400, detail="top_k must be positive.")

    encoded = encode_sequence(seq)
    results = ranker.rank_phages_for_host(encoded, phage_candidates, top_k=query.top_k)

    return {
        "query_type": "host_to_phage",
        "top_k": query.top_k,
        "num_candidates": len(phage_candidates),
        "results": results,
    }


# ------------------------------
# File-upload endpoints
# ------------------------------


@app.post("/upload/phage")
async def upload_phage(file: UploadFile = File(...), top_k: int = 10):
    """
    Upload a single phage FASTA file and rank hosts in the dataset.

    This endpoint is convenient for GUI-based usage (e.g., Swagger UI or a web frontend).
    """
    if top_k <= 0:
        raise HTTPException(status_code=400, detail="top_k must be positive.")

    if file.content_type not in ("text/plain", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    raw_bytes = await file.read()
    try:
        text = raw_bytes.decode()
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded text.")

    try:
        seq = load_single_fasta_sequence(text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    encoded = encode_sequence(seq)
    results = ranker.rank_hosts_for_phage(encoded, host_candidates, top_k=top_k)

    return {
        "query_type": "phage_to_host",
        "filename": file.filename,
        "top_k": top_k,
        "num_candidates": len(host_candidates),
        "results": results,
    }


@app.post("/upload/host")
async def upload_host(file: UploadFile = File(...), top_k: int = 10):
    """
    Upload a single host FASTA file and rank phages in the dataset.

    This endpoint is convenient for GUI-based usage (e.g., Swagger UI or a web frontend).
    """
    if top_k <= 0:
        raise HTTPException(status_code=400, detail="top_k must be positive.")

    if file.content_type not in ("text/plain", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    raw_bytes = await file.read()
    try:
        text = raw_bytes.decode()
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded text.")

    try:
        seq = load_single_fasta_sequence(text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    encoded = encode_sequence(seq)
    results = ranker.rank_phages_for_host(encoded, phage_candidates, top_k=top_k)

    return {
        "query_type": "host_to_phage",
        "filename": file.filename,
        "top_k": top_k,
        "num_candidates": len(phage_candidates),
        "results": results,
    }
