"""Servicio de ingestión local de manuales PDF/Markdown — 0 tokens LLM."""

from __future__ import annotations

import json
from pathlib import Path

from industrial_rag.config import Settings, get_settings
from industrial_rag.ingestion.chunker import merge_page_chunks
from industrial_rag.ingestion.indexer import ManualIndexer
from industrial_rag.ingestion.pdf_extractor import (
    extract_pages,
    extract_pages_from_bytes,
    load_markdown_manual,
)
from industrial_rag.models import ChunkMetadata, EquipmentRecord


class ManualIngestionService:
    """
    Ingesta offline: PDF/Markdown → chunks con metadatos → embeddings locales → Qdrant.

    No llama a ningún LLM comercial. Reutilizable para cualquier máquina
    registrando equipos con machine_id distinto.
    """

    def __init__(
        self,
        indexer: ManualIndexer | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.indexer = indexer or ManualIndexer(settings=self.settings)

    def ingest_equipment_file(
        self,
        equipment: EquipmentRecord,
        file_path: Path,
        *,
        batch_size: int = 32,
    ) -> int:
        pages = self._load_pages(file_path)

        def factory(page_number: int) -> ChunkMetadata:
            return ChunkMetadata(
                machine_id=equipment.machine_id,
                equipment_id=equipment.equipment_id,
                manufacturer=equipment.manufacturer,
                model=equipment.model,
                line=equipment.line,
                manual_version=equipment.manual_version,
                page_number=page_number,
                source_file=file_path.name,
            )

        chunks = merge_page_chunks(pages, factory)
        return self.indexer.index_chunks(chunks, batch_size=batch_size)

    def ingest_pdf_bytes(
        self,
        equipment: EquipmentRecord,
        pdf_bytes: bytes,
        filename: str,
        *,
        batch_size: int = 32,
    ) -> int:
        pages = extract_pages_from_bytes(pdf_bytes, filename=filename)

        def factory(page_number: int) -> ChunkMetadata:
            return ChunkMetadata(
                machine_id=equipment.machine_id,
                equipment_id=equipment.equipment_id,
                manufacturer=equipment.manufacturer,
                model=equipment.model,
                line=equipment.line,
                manual_version=equipment.manual_version,
                page_number=page_number,
                source_file=filename,
            )

        chunks = merge_page_chunks(pages, factory)
        return self.indexer.index_chunks(chunks, batch_size=batch_size)

    def ingest_registry(
        self,
        registry_path: Path | None = None,
        *,
        data_root: Path | None = None,
        batch_size: int = 32,
    ) -> dict[str, int]:
        path = registry_path or self.settings.equipment_registry_path
        root = data_root or path.parent
        records = [
            EquipmentRecord.model_validate(item)
            for item in json.loads(path.read_text(encoding="utf-8"))
        ]
        counts: dict[str, int] = {}
        for equipment in records:
            manual_path = root / equipment.manual_file
            if not manual_path.exists():
                counts[equipment.equipment_id] = 0
                continue
            counts[equipment.equipment_id] = self.ingest_equipment_file(
                equipment,
                manual_path,
                batch_size=batch_size,
            )
        return counts

    @staticmethod
    def _load_pages(file_path: Path) -> list[tuple[int, str]]:
        suffix = file_path.suffix.lower()
        if suffix in {".md", ".markdown"}:
            return load_markdown_manual(file_path)
        if suffix == ".pdf":
            return extract_pages(file_path)
        raise ValueError(f"Formato no soportado: {suffix}. Use PDF o Markdown.")
