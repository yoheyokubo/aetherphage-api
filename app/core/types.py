# app/core/types.py
from dataclasses import dataclass
from typing import List, Optional
from Bio.SeqRecord import SeqRecord


@dataclass(frozen=True)
class GenomeEntity:
    """
    Core biological entity used across the entire system.
    """
    seqs: List[SeqRecord]
    scientific_name: Optional[str] = None
    lineage: Optional[List[int]] = None