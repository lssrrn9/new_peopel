"""Buscador híbrido: vectores densos + boost por códigos de falla exactos."""

from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from industrial_rag.config import Settings, get_settings
from industrial_rag.ingestion.fault_codes import query_fault_codes
from industrial_rag.models import ChunkMetadata, RetrievedChunk
from industrial_rag.retrieval.embeddings import Embeddings


class MetadataFilteredSearcher:
    """
    1) Filtro duro por machine_id / equipment_id
    2) Búsqueda densa semántica
    3) Reordenación con boost si el chunk contiene el código exacto (AL 38 ≠ AL 39)
    """

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
        vector = self.embeddings.embed_query(query)
        qdrant_filter = self._to_qdrant_filter(metadata_filter)
        fetch_limit = max((limit or self.settings.search_limit) * 3, 9)

        response = self.client.query_points(
            collection_name=self.settings.qdrant_collection,
            query=vector,
            query_filter=qdrant_filter,
            limit=fetch_limit,
            with_payload=True,
        )

        codes = query_fault_codes(query)
        results: list[RetrievedChunk] = []
        for hit in response.points:
            payload = hit.payload or {}
            text = payload.get("text", "")
            meta_raw = payload.get("metadata", {})
            if not text or not meta_raw:
                continue
            meta = ChunkMetadata.model_validate(meta_raw)
            score = float(hit.score or 0.0) + self._exact_code_boost(codes, meta, text)
            results.append(RetrievedChunk(text=text, metadata=meta, score=score))

        results.sort(key=lambda item: item.score, reverse=True)
        return results[: limit or self.settings.search_limit]

    @staticmethod
    def _exact_code_boost(codes: list[str], meta: ChunkMetadata, text: str) -> float:
        if not codes:
            return 0.0
        boost = 0.0
        meta_codes = {c.upper() for c in meta.fault_codes}
        text_upper = text.upper()
        for code in codes:
            if code in meta_codes:
                boost += 0.35
            elif code in text_upper:
                boost += 0.2
            else:
                # Penalizar levemente códigos vecinos del mismo prefijo (AL 39 vs AL 38)
                prefix = code.rstrip("0123456789").strip()
                if prefix and any(
                    other.startswith(prefix) and other != code for other in meta_codes
                ):
                    boost -= 0.05
        return boost

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
