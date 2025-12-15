# app/utils/dataset.py
import csv
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def load_host_candidates() -> List[Dict]:
    """
    Load host metadata from 'data/cherry_hosts.csv'.

    Expected CSV columns:
        - host_id
        - host_name (optional)
    """
    path = DATA_DIR / "cherry_hosts.csv"
    hosts: List[Dict] = []

    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            hosts.append(
                {
                    "host_id": row["host_id"],
                    "host_name": row.get("host_name", ""),
                }
            )
    return hosts


def load_phage_candidates() -> List[Dict]:
    """
    Load phage metadata from 'data/cherry_phages.csv'.

    Expected CSV columns:
        - phage_id
        - phage_name (optional)
    """
    path = DATA_DIR / "cherry_phages.csv"
    phages: List[Dict] = []

    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            phages.append(
                {
                    "phage_id": row["phage_id"],
                    "phage_name": row.get("phage_name", ""),
                }
            )
    return phages
