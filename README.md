# AetherPhage API

## Why this project exists

Bacteriophages (phages) are viruses that infect bacteria. Predicting which phage can infect which host bacterium — the **phage–host interaction (PHI) prediction problem** — is a central problem in:

- **Phage therapy**: selecting effective phages to target pathogenic bacteria, especially antibiotic-resistant strains
- **Metagenomics**: interpreting large-scale sequencing data where phages and hosts are mixed and unlabeled
- **Microbial ecology**: understanding virus–host dynamics in complex environments

Most PHI prediction methods remain confined to research code and papers. They are difficult to reuse, integrate into pipelines, or evaluate consistently.

This project was created to **bridge the gap between research models and practical use** by exposing PHI prediction through a simple, reproducible API.

---

## What this API does (current version)

The current API implements the following workflow:

1. Accepts **either a phage genome or a host genome** as input (FASTA format)
2. Compares the input genome against a **reference database (CHERRY dataset)**
3. Computes **interaction scores** using a machine-learning model
4. Returns the **top-K predicted interaction partners**, including:
   - interaction score
   - organism name
   - taxonomic lineage (if available)

This design reflects how PHI prediction is often used in practice: querying likely hosts for a phage, or likely phages for a host.

---

## How to use the API

### Endpoint

POST `/predict`

---

### Input parameters

- `query_fasta`: genome sequence in FASTA format (phage or host)
- `query_type`: `"phage"` or `"host"`
- `top_k`: number of top predictions to return

---

### Example (JSON input)

```bash
curl -X POST https://<API_ENDPOINT>/predict   -H "Content-Type: application/json"   -d '{
    "query_fasta": ">query\nATG...",
    "query_type": "phage",
    "top_k": 5
  }'
```

---

### Example response

```json
{
  "query_type": "phage",
  "top_k": 5,
  "results": [
    {
      "rank": 1,
      "organism": "Escherichia coli",
      "lineage": "Bacteria; Proteobacteria; Gammaproteobacteria",
      "score": 0.87
    }
  ],
  "model": "CL4PHI",
  "database": "CHERRY"
}
```

---

## Model

The current version integrates **CL4PHI**, a contrastive-learning-based PHI prediction model.

The API is intentionally designed so that the **external interface remains stable**, even if the underlying model or scoring method changes.

---

## Implementation (for developers)

- Python + FastAPI
- Dockerized service
- Deployed on AWS using:
  - Amazon ECR (image registry)
  - Amazon ECS Fargate (container execution)
  - Application Load Balancer (HTTPS access)
  - GitHub Actions (CI/CD)

Deployment automation is defined under `.github/workflows/`.

---

## Development status

- API endpoint: implemented
- CL4PHI integration: implemented
- CHERRY dataset support: implemented
- FASTA file upload: supported
- Additional models and confidence estimation: planned

---

## Intended audience

- Researchers who want reproducible PHI prediction
- Engineers building bioinformatics pipelines
- Evaluators reviewing applied ML + systems work

---

## License

Apache License 2.0

---

## Disclaimer

This software is for research and experimental use only.
