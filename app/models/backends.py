# app/models/backends.py
from abc import ABC, abstractmethod
from typing import List
import numpy as np

from app.core.types import GenomeEntity
from app.utils.encoding import encode_sequence


class PHIBackend(ABC):
    """
    Abstract base class for phage–host interaction backends.

    A backend is responsible for computing a compatibility score
    between one query GenomeEntity and multiple candidate GenomeEntity objects.
    """

    name: str = "abstract"

    @abstractmethod
    def score(
        self,
        query: GenomeEntity,
        dataset: List[GenomeEntity],
    ) -> List[float]:
        """
        Compute scores for query vs dataset.

        Args:
            query: Single GenomeEntity (phage or host)
            dataset: List of GenomeEntity candidates

        Returns:
            List of scores (higher = more compatible)
        """
        raise NotImplementedError


# ---------------------------------------------------------------------
# Random backend (baseline / backward compatibility)
# ---------------------------------------------------------------------

class RandomBackend(PHIBackend):
    """
    Random scoring backend.

    This backend is useful for:
    - smoke testing the API
    - backward compatibility
    - demonstrating the ranking pipeline without heavy dependencies
    """

    name = "random"

    def score(
        self,
        query: GenomeEntity,
        dataset: List[GenomeEntity],
    ) -> List[float]:
        return np.random.rand(len(dataset)).tolist()


# ---------------------------------------------------------------------
# Simple k-mer backend (encode_sequence-based)
# ---------------------------------------------------------------------

class KmerBackend(PHIBackend):
    """
    Simple k-mer frequency backend.

    This backend:
    - uses encode_sequence() on raw DNA strings
    - averages scores across multiple contigs/chromosomes
    - serves as a lightweight, deterministic baseline

    Note:
        This is NOT CL4PHI.
        It exists to keep backward compatibility with early prototypes.
    """

    name = "kmer"

    def score(
        self,
        query: GenomeEntity,
        dataset: List[GenomeEntity],
    ) -> List[float]:

        # Encode query: average across multiple sequences if necessary
        query_vecs = [
            encode_sequence(str(rec.seq))
            for rec in query.seqs
        ]
        query_vec = np.mean(query_vecs, axis=0)

        scores: List[float] = []

        for entity in dataset:
            entity_vecs = [
                encode_sequence(str(rec.seq))
                for rec in entity.seqs
            ]
            entity_vec = np.mean(entity_vecs, axis=0)

            # Cosine similarity
            denom = (
                np.linalg.norm(query_vec)
                * np.linalg.norm(entity_vec)
                + 1e-8
            )
            score = float(np.dot(query_vec, entity_vec) / denom)
            scores.append(score)

        return scores
