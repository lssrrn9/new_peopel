"""Capa de embeddings con FastEmbed y fallback determinista para tests."""

from __future__ import annotations

import hashlib
import math
import struct
from typing import Sequence


class Embeddings:
    """
    Usa FastEmbed cuando está disponible.
    Si falla la descarga del modelo, usa un hash embedding determinista
    (solo para pruebas unitarias / CI sin red).
    """

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5", dim: int = 384) -> None:
        self.model_name = model_name
        self.dim = dim
        self._model = None
        try:
            from fastembed import TextEmbedding

            self._model = TextEmbedding(model_name=model_name)
        except Exception:
            self._model = None

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        if self._model is not None:
            return [list(vec) for vec in self._model.embed(list(texts))]
        return [self._hash_embed(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def _hash_embed(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values: list[float] = []
        while len(values) < self.dim:
            digest = hashlib.sha256(digest + text.encode("utf-8")).digest()
            for i in range(0, len(digest) - 3, 4):
                raw = struct.unpack(">I", digest[i : i + 4])[0]
                values.append((raw / 0xFFFFFFFF) * 2 - 1)
                if len(values) >= self.dim:
                    break
        norm = math.sqrt(sum(v * v for v in values)) or 1.0
        return [v / norm for v in values]
