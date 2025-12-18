# app/models/ranker.py
from typing import List, Dict
from app.core.types import GenomeEntity
from app.models.backends import PHIBackend


class PhageHostRanker:
    """
    Backend-agnostic ranking orchestrator.

    This class does not know how scores are computed.
    It only:
      - passes GenomeEntity objects to the backend
      - sorts results
      - formats API responses
    """

    def __init__(self, backend: PHIBackend):
        self.backend = backend

    def rank(
        self,
        query: GenomeEntity,
        dataset: List[GenomeEntity],
        top_k: int,
        id_key: str,
        name_key: str,
    ) -> List[Dict]:
        """
        Rank dataset entities against a single query entity.

        Args:
            query: Single GenomeEntity (phage or host)
            dataset: List of GenomeEntity candidates
            top_k: Number of top results to return
            id_key: Identifier field name in metadata
            name_key: Name field for display

        Returns:
            List of ranked result dictionaries.
        """

        scores = self.backend.score(query, dataset)

        ranked = sorted(
            zip(dataset, scores),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]

        results = []
        for entity, score in ranked:
            results.append(
                {
                    id_key: getattr(entity, id_key, None),
                    name_key: entity.scientific_name,
                    "score": float(score),
                }
            )
        return results

