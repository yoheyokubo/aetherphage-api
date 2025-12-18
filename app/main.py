# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from tempfile import NamedTemporaryFile
from pathlib import Path
from typing import List

from app.core.types import GenomeEntity
from app.utils.sequence import GenomeSource
from app.utils.dataset import load_host_candidates, load_phage_candidates
from app.models.ranker import PhageHostRanker
from app.models.backends import RandomBackend

app = FastAPI(
    title="AetherPhage API",
    description="Sequence-aware API for phage–host interaction ranking.",
    version="0.3.0",
)

# ---------------------------------------------------------------------
# Load dataset metadata (sequence paths / names / lineage are resolved here)
# ---------------------------------------------------------------------

host_entities: List[GenomeEntity] = load_host_candidates()
phage_entities: List[GenomeEntity] = load_phage_candidates()

# ---------------------------------------------------------------------
# Initialize ranker (backend can be swapped later)
# ---------------------------------------------------------------------

ranker = PhageHostRanker(
    backend=RandomBackend()  # placeholder (CL4PHI / others can be injected)
)


@app.get("/health")
def health_check():
    """Lightweight health check endpoint."""
    return {
        "status": "ok",
        "num_hosts": len(host_entities),
        "num_phages": len(phage_entities),
        "backend": ranker.backend.name,
    }


# ---------------------------------------------------------------------
# Upload-based endpoints (default)
# ---------------------------------------------------------------------

@app.post("/predict/phage")
async def predict_hosts(
    file: UploadFile = File(...),
    top_k: int = 10,
):
    """
    Upload a single phage FASTA file and rank host candidates.
    """
    if top_k <= 0:
        raise HTTPException(status_code=400, detail="top_k must be positive.")

    with NamedTemporaryFile(delete=False, suffix=".fasta") as tmp:
        content = await file.read()
        tmp.write(content)
        fasta_path = Path(tmp.name)

    query_entity = GenomeEntity(
        seqs=GenomeSource(path=fasta_path).read()
    )

    results = ranker.rank(
        query=query_entity,
        dataset=host_entities,
        top_k=top_k,
        id_key="host_id",
        name_key="scientific_name",
    )

    return {
        "query_type": "phage_to_host",
        "filename": file.filename,
        "top_k": top_k,
        "results": results,
    }


@app.post("/predict/host")
async def predict_phages(
    file: UploadFile = File(...),
    top_k: int = 10,
):
    """
    Upload a single host FASTA file and rank phage candidates.
    """
    if top_k <= 0:
        raise HTTPException(status_code=400, detail="top_k must be positive.")

    with NamedTemporaryFile(delete=False, suffix=".fasta") as tmp:
        content = await file.read()
        tmp.write(content)
        fasta_path = Path(tmp.name)

    query_entity = GenomeEntity(
        seqs=GenomeSource(path=fasta_path).read()
    )

    results = ranker.rank(
        query=query_entity,
        dataset=phage_entities,
        top_k=top_k,
        id_key="phage_id",
        name_key="scientific_name",
    )

    return {
        "query_type": "host_to_phage",
        "filename": file.filename,
        "top_k": top_k,
        "results": results,
    }
