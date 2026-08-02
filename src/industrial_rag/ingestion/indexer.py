"""Indexación de fragmentos en Qdrant con payload de metadatos."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Iterable

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from industrial_rag.config import Settings, get_settings
from industrial_rag.models import ManualChunk
from industrial_rag.retrieval.embeddings import Embeddings


class ManualIndexer:
    def __init__(
        self,
        client: QdrantClient | None = None,
        embeddings: Embeddings | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.client = client or _build_client(self.settings)
        self.embeddings = embeddings or Embeddings(self.settings.embedding_model)
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        name = self.settings.qdrant_collection
        exists = self.client.collection_exists(name)
        if not exists:
            self.client.create_collection(
                collection_name=name,
                vectors_config=qmodels.VectorParams(
                    size=self.settings.embedding_dim,
                    distance=qmodels.Distance.COSINE,
                ),
            )
        if self.settings.use_memory_qdrant:
            return
        for field in (
            "metadata.machine_id",
            "metadata.equipment_id",
            "metadata.manufacturer",
            "metadata.model",
            "metadata.line",
            "metadata.section",
            "metadata.fault_codes",
        ):
            try:
                self.client.create_payload_index(
                    collection_name=name,
                    field_name=field,
                    field_schema=qmodels.PayloadSchemaType.KEYWORD,
                )
            except Exception:
                pass

    def index_chunks(self, chunks: Iterable[ManualChunk], *, batch_size: int = 32) -> int:
        """Indexa por lotes para no saturar RAM en VPS de 4GB."""
        batch: list[ManualChunk] = []
        total = 0
        for chunk in chunks:
            batch.append(chunk)
            if len(batch) >= batch_size:
                total += self._upsert_batch(batch)
                batch = []
        if batch:
            total += self._upsert_batch(batch)
        return total

    def _upsert_batch(self, batch: list[ManualChunk]) -> int:
        vectors = self.embeddings.embed_documents([c.text for c in batch])
        points = [
            qmodels.PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=chunk.to_payload(),
            )
            for chunk, vector in zip(batch, vectors, strict=True)
        ]
        self.client.upsert(
            collection_name=self.settings.qdrant_collection,
            points=points,
        )
        return len(points)

    def index_jsonl(self, path: Path) -> int:
        """Carga chunks pre-etiquetados (útil para piloto sin PDFs reales)."""
        chunks: list[ManualChunk] = []
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                payload = json.loads(line)
                chunks.append(ManualChunk.model_validate(payload))
        return self.index_chunks(chunks)


def _build_client(settings: Settings) -> QdrantClient:
    if settings.use_memory_qdrant:
        return QdrantClient(location=":memory:")
    return QdrantClient(url=settings.qdrant_url)
