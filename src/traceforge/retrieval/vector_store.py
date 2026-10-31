"""Small in-memory cosine vector index for local RAG examples."""

import math


class VectorStore:
    """Store text and vectors and rank them by cosine similarity."""

    def __init__(self) -> None:
        self._items: list[tuple[str, str, list[float]]] = []

    def add(self, ident: str, text: str, vector: list[float]) -> None:
        """Insert a vector, replacing any existing item with the same ID."""
        self._items = [item for item in self._items if item[0] != ident]
        self._items.append((ident, text, vector))

    def search(self, query: list[float], limit: int = 5) -> list[tuple[str, str, float]]:
        """Return top matches as ID, text, and cosine score."""
        scored = []
        for ident, text, vector in self._items:
            if len(query) != len(vector):
                raise ValueError("query and stored vectors must have equal dimensions")
            score = sum(left * right for left, right in zip(query, vector, strict=True))
            if not math.isfinite(score):
                continue
            scored.append((ident, text, score))
        return sorted(scored, key=lambda item: item[2], reverse=True)[: max(0, limit)]
