"""Deterministic hashing embeddings for offline examples and tests."""

import hashlib
import math
import re


class HashingEmbedder:
    """Map text tokens into normalized fixed-size vectors without dependencies."""

    def __init__(self, dimensions: int = 128) -> None:
        if dimensions < 8:
            raise ValueError("dimensions must be at least 8")
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        """Produce a stable signed hashing vector for the supplied text."""
        vector = [0.0] * self.dimensions
        for token in re.findall(r"[a-z0-9]+", text.lower()):
            digest = hashlib.blake2b(token.encode(), digest_size=8).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] & 1 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector))
        return [value / norm for value in vector] if norm else vector
