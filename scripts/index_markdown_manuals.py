#!/usr/bin/env python3
"""Indexa manuales Markdown del registro de equipos (piloto)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from industrial_rag.config import Settings
from industrial_rag.ingestion.chunker import merge_page_chunks
from industrial_rag.ingestion.indexer import ManualIndexer
from industrial_rag.ingestion.pdf_extractor import load_markdown_manual
from industrial_rag.models import ChunkMetadata, EquipmentRecord


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", action="store_true")
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    args = parser.parse_args()

    settings = Settings()
    settings.use_memory_qdrant = args.memory
    settings.equipment_registry_path = args.data_root / "equipment_registry.json"

    registry = json.loads(settings.equipment_registry_path.read_text(encoding="utf-8"))
    indexer = ManualIndexer(settings=settings)
    total = 0

    seen_files: set[str] = set()
    for item in registry:
        eq = EquipmentRecord.model_validate(item)
        # Un archivo puede servir a varios equipos: indexar una vez por equipment_id
        md_path = args.data_root / eq.manual_file
        if not md_path.exists():
            print(f"SKIP missing manual: {md_path}")
            continue

        pages = load_markdown_manual(md_path)

        def factory(page_number: int, eq: EquipmentRecord = eq, md_path: Path = md_path) -> ChunkMetadata:
            return ChunkMetadata(
                equipment_id=eq.equipment_id,
                manufacturer=eq.manufacturer,
                model=eq.model,
                line=eq.line,
                manual_version=eq.manual_version,
                page_number=page_number,
                source_file=md_path.name,
            )

        chunks = merge_page_chunks(pages, factory)
        # Si varios equipos comparten el mismo PDF, duplicar chunks por equipment_id
        count = indexer.index_chunks(chunks)
        total += count
        seen_files.add(str(md_path))
        print(f"Indexed {count} chunks for {eq.equipment_id} from {md_path.name}")

    print(json.dumps({"indexed_chunks": total, "files": sorted(seen_files)}))


if __name__ == "__main__":
    main()
