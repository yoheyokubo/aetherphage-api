# app/models/ranker.py
from typing import List, Dict, Optional
import numpy as np
import random

try:
    import torch
    from torch import nn

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


class PhageHostRanker:
    """
    Wrapper around a PHI model (e.g., MCL4PHI, CL4PHI, PBLKS).

    In this template:
        - If PyTorch is available and a model is provided, use it.
        - Otherwise, fall back to random scores for demonstration purposes.

    This design allows:
        - Local/Docker demo without heavy dependencies
        - Easy migration to a real PyTorch model on Shirokane or AWS
    """

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.model: Optional["nn.Module"] = None

        random.seed(42)
        np.random.seed(42)

        if HAS_TORCH and model_path is not None:
            # TODO: Replace this with your actual MCL4PHI / CL4PHI loading code.
            # Example:
            #   self.model = MCL4PHI(...)
            #   self.model.load_state_dict(torch.load(model_path, map_location="cpu"))
            #   self.model.eval()
            pass

    def _score_with_model(
        self,
        query_vec: np.ndarray,
        candidate_vecs: np.ndarray,
    ) -> np.ndarray:
        """
        Score query against candidates using a PyTorch model.

        Args:
            query_vec: (D,) numpy array
            candidate_vecs: (N, D) numpy array

        Returns:
            scores: (N,) numpy array
        """
        if not HAS_TORCH or self.model is None:
            raise RuntimeError("PyTorch model is not loaded.")

        with torch.no_grad():
            q = torch.from_numpy(query_vec).float().unsqueeze(0)  # (1, D)
            c = torch.from_numpy(candidate_vecs).float()          # (N, D)

            # TODO:
            #   Implement the actual scoring logic.
            #   For example, if the model outputs a compatibility score:
            #
            #   scores = self.model(q, c)  # (N,)
            #
            # Here we just compute cosine similarity as a placeholder.
            q_norm = q / (q.norm(dim=1, keepdim=True) + 1e-8)
            c_norm = c / (c.norm(dim=1, keepdim=True) + 1e-8)
            scores = (q_norm @ c_norm.T).squeeze(0)  # (N,)

        return scores.cpu().numpy()

    def _score_random(self, num_candidates: int) -> np.ndarray:
        """
        Return random scores as a fallback (for demo / smoke tests).
        """
        return np.random.rand(num_candidates)

    def rank_hosts_for_phage(
        self,
        encoded_phage: np.ndarray,
        host_candidates: List[Dict],
        top_k: int = 10,
    ) -> List[Dict]:
        """
        Rank host candidates for a given encoded phage sequence.
        """
        num_candidates = len(host_candidates)
        if num_candidates == 0:
            return []

        # Placeholder: random scores
        scores = self._score_random(num_candidates)

        ranked = sorted(
            [
                {
                    "host_id": h["host_id"],
                    "host_name": h.get("host_name", ""),
                    "score": float(s),
                }
                for h, s in zip(host_candidates, scores)
            ],
            key=lambda x: x["score"],
            reverse=True,
        )
        return ranked[:top_k]

    def rank_phages_for_host(
        self,
        encoded_host: np.ndarray,
        phage_candidates: List[Dict],
        top_k: int = 10,
    ) -> List[Dict]:
        """
        Rank phage candidates for a given encoded host sequence.
        """
        num_candidates = len(phage_candidates)
        if num_candidates == 0:
            return []

        # Placeholder: random scores
        scores = self._score_random(num_candidates)

        ranked = sorted(
            [
                {
                    "phage_id": p["phage_id"],
                    "phage_name": p.get("phage_name", ""),
                    "score": float(s),
                }
                for p, s in zip(phage_candidates, scores)
            ],
            key=lambda x: x["score"],
            reverse=True,
        )
        return ranked[:top_k]
