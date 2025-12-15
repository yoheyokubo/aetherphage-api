# app/utils/fasta.py
from io import StringIO
from typing import List
from Bio import SeqIO


def load_single_fasta_sequence(text: str) -> str:
    """
    Parse a FASTA-formatted string and return a single sequence.
    Raises an error if zero or multiple sequences are found.
    """
    handle = StringIO(text)
    records: List[SeqIO.SeqRecord] = list(SeqIO.parse(handle, "fasta"))

    if len(records) == 0:
        raise ValueError("No FASTA sequence found in the input text.")
    if len(records) > 1:
        raise ValueError("Multiple sequences found; expected exactly one.")

    seq = str(records[0].seq).upper()
    if not seq:
        raise ValueError("Sequence is empty.")
    return seq

