"""Orquestación del flujo: Trigger → Router → RAG híbrido → Diagnóstico."""

from __future__ import annotations

from pathlib import Path

from qdrant_client import QdrantClient

from industrial_rag.config import Settings, get_settings
from industrial_rag.diagnosis.generator import DiagnosticGenerator
from industrial_rag.ingestion.indexer import ManualIndexer, _build_client
from industrial_rag.ingestion.service import ManualIngestionService
from industrial_rag.models import DiagnosticReport, FaultTrigger
from industrial_rag.retrieval.embeddings import Embeddings
from industrial_rag.retrieval.router import MetadataRouter
from industrial_rag.retrieval.search import MetadataFilteredSearcher


class TroubleshootingPipeline:
    """
    Secuencia estricta:
      Trigger → Router metadatos → Buscador híbrido → LLM (opcional) → Reporte

    La ingestión de manuales es un paso separado y siempre local (0 tokens).
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
        self.ingestion = ManualIngestionService(
            indexer=self.indexer,
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

    def ingest_registry(self) -> dict[str, int]:
        """Indexa todos los manuales del registro (PDF/MD) sin LLM."""
        return self.ingestion.ingest_registry()

    def troubleshoot(self, trigger: FaultTrigger) -> DiagnosticReport:
        if self.router.registry:
            equipment = self.router.resolve_equipment(trigger.equipment_id)
            if trigger.machine_id and trigger.machine_id != equipment.machine_id:
                raise KeyError(
                    f"El equipo '{trigger.equipment_id}' pertenece a "
                    f"'{equipment.machine_id}', no a '{trigger.machine_id}'."
                )
            if trigger.machine_id is None:
                trigger = trigger.model_copy(update={"machine_id": equipment.machine_id})

        metadata_filter = self.router.build_filter(trigger)
        query = self.router.search_query(trigger)
        chunks = self.searcher.search(query, metadata_filter)
        report = self.generator.generate(trigger.equipment_id, query, chunks)
        return report.model_copy(update={"machine_id": trigger.machine_id})
