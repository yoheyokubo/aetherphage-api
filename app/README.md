# PHI-API (Phage-Host Interaction API)

Minimal FastAPI service for phage–host interaction ranking on the Cherry dataset.

## Features (v1)

- `POST /predict/phage`  
  - Input: single phage genome (FASTA text)  
  - Output: ranked list of host candidates from Cherry dataset

- `POST /predict/host`  
  - Input: single host genome (FASTA text)  
  - Output: ranked list of phage candidates from Cherry dataset

- `GET /health`  
  - Health check

## Project structure

```bash
phi-api/
  app/
    main.py
    models/ranker.py
    utils/{fasta,encoding,dataset}.py
  data/
    cherry_hosts.csv
    cherry_phages.csv
  weights/
  Dockerfile
  requirements.txt

