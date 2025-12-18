# app/core/source.py
from pathlib import Path
from typing import Optional, List
from Bio import SeqIO
from io import StringIO
from Bio.SeqRecord import SeqRecord


class GenomeSource:
    """
    User-facing genome input abstraction.

    Supports:
    - FASTA file path
    - FASTA string

    Produces:
    - List[SeqRecord]
    """

    def __init__(
        self,
        fasta: Optional[str] = None,
        path: Optional[Path] = None,
    ):
        if fasta is None and path is None:
            raise ValueError("Either fasta or path must be provided.")
        self.fasta = fasta
        self.path = path

    def read(self) -> List[SeqRecord]:
        if self.path is not None:
            records = list(SeqIO.parse(self.path, "fasta"))
        else:
            records = list(SeqIO.parse(StringIO(self.fasta), "fasta"))

        if len(records) == 0:
            raise ValueError("No FASTA sequences found.")
        return records
