"""Buscador vectorial con filtro duro de metadatos."""

from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from industrial_rag.config import Settings, get_settings
from industrial_rag.models import ChunkMetadata, RetrievedChunk
from industrial_rag.retrieval.embeddings import Embeddings


class MetadataFilteredSearcher:
    def __init__(
        self,
        client: QdrantClient,
        embeddings: Embeddings | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.client = client
        self.settings = settings or get_settings()
        self.embeddings = embeddings or Embeddings(
            self.settings.embedding_model,
            dim=self.settings.embedding_dim,
        )

    def search(
        self,
        query: str,
        metadata_filter: dict,
        *,
        limit: int | None = None,
    ) -> list[RetrievedChunk]:
        """
        1) Aplica filtro duro por metadatos
        2) Busca solo dentro del subconjunto del equipo afectado
        """
        vector = self.embeddings.embed_query(query)
        qdrant_filter = self._to_qdrant_filter(metadata_filter)

        response = self.client.query_points(
            collection_name=self.settings.qdrant_collection,
            query=vector,
            query_filter=qdrant_filter,
            limit=limit or self.settings.search_limit,
            with_payload=True,
        )

        results: list[RetrievedChunk] = []
        for hit in response.points:
            payload = hit.payload or {}
            text = payload.get("text", "")
            meta_raw = payload.get("metadata", {})
            if not text or not meta_raw:
                continue
            results.append(
                RetrievedChunk(
                    text=text,
                    metadata=ChunkMetadata.model_validate(meta_raw),
                    score=float(hit.score or 0.0),
                )
            )
        return results

    @staticmethod
    def _to_qdrant_filter(metadata_filter: dict) -> qmodels.Filter:
        conditions = []
        for item in metadata_filter.get("must", []):
            conditions.append(
                qmodels.FieldCondition(
                    key=item["key"],
                    match=qmodels.MatchValue(value=item["match"]["value"]),
                )
            )
        return qmodels.Filter(must=conditions)
