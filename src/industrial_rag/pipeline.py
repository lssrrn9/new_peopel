"""Orquestación del flujo: Trigger → Router → RAG → Diagnóstico."""

from __future__ import annotations

from pathlib import Path

from qdrant_client import QdrantClient

from industrial_rag.config import Settings, get_settings
from industrial_rag.diagnosis.generator import DiagnosticGenerator
from industrial_rag.ingestion.indexer import ManualIndexer, _build_client
from industrial_rag.models import DiagnosticReport, FaultTrigger
from industrial_rag.retrieval.embeddings import Embeddings
from industrial_rag.retrieval.router import MetadataRouter
from industrial_rag.retrieval.search import MetadataFilteredSearcher


class TroubleshootingPipeline:
    """
    Secuencia estricta:
      Trigger → Router metadatos → Buscador vectorial → LLM → Reporte
    """

    def __init__(
        self,
        settings: Settings | None = None,
        client: QdrantClient | None = None,
        embeddings: Embeddings | None = None,
        generator: DiagnosticGenerator | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.client = client or _build_client(self.settings)
        self.embeddings = embeddings or Embeddings(
            self.settings.embedding_model,
            dim=self.settings.embedding_dim,
        )
        self.router = MetadataRouter(self.settings.equipment_registry_path)
        self.searcher = MetadataFilteredSearcher(
            self.client,
            embeddings=self.embeddings,
            settings=self.settings,
        )
        self.generator = generator or DiagnosticGenerator(settings=self.settings)
        self.indexer = ManualIndexer(
            client=self.client,
            embeddings=self.embeddings,
            settings=self.settings,
        )

    def load_pilot_data(self, chunks_dir: Path | None = None) -> int:
        directory = chunks_dir or self.settings.sample_chunks_path
        total = 0
        if not directory.exists():
            return 0
        for path in sorted(directory.glob("*.jsonl")):
            total += self.indexer.index_jsonl(path)
        return total

    def troubleshoot(self, trigger: FaultTrigger) -> DiagnosticReport:
        # 1) Validar equipo y construir filtro duro
        if self.router.registry:
            self.router.resolve_equipment(trigger.equipment_id)
        metadata_filter = self.router.build_filter(trigger)
        query = self.router.search_query(trigger)

        # 2) Búsqueda vectorial SOLO en el manual del equipo
        chunks = self.searcher.search(query, metadata_filter)

        # 3) Generar diagnóstico estricto
        return self.generator.generate(trigger.equipment_id, query, chunks)
