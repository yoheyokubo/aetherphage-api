# app/utils/encoding.py
import numpy as np
from itertools import product


def _kmer_dict(k: int = 3):
    """
    Build a dictionary mapping k-mers to indices.
    """
    alphabet = ["A", "C", "G", "T"]
    kmers = ["".join(p) for p in product(alphabet, repeat=k)]
    return {kmer: i for i, kmer in enumerate(kmers)}


_KMER_INDEX = _kmer_dict(3)


def encode_sequence(seq: str, k: int = 3) -> np.ndarray:
    """
    Encode a DNA sequence into a simple k-mer frequency vector.

    Note:
        This is a placeholder implementation. In production, replace this
        with the same encoding used in MCL4PHI / CL4PHI (e.g., binomial k-mer).
    """
    seq = seq.upper()
    vec = np.zeros(len(_KMER_INDEX), dtype=np.float32)

    if len(seq) < k:
        return vec

    for i in range(len(seq) - k + 1):
        kmer = seq[i : i + k]
        if kmer in _KMER_INDEX:
            idx = _KMER_INDEX[kmer]
            vec[idx] += 1.0

    total = vec.sum()
    if total > 0:
        vec /= total
    return vec
