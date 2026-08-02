#!/usr/bin/env python3
"""Indexa manuales Markdown/PDF del registro de equipos (0 tokens LLM)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from industrial_rag.config import Settings
from industrial_rag.ingestion.service import ManualIngestionService


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", action="store_true")
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()

    settings = Settings()
    settings.use_memory_qdrant = args.memory
    settings.equipment_registry_path = args.data_root / "equipment_registry.json"
    settings.ingest_batch_size = args.batch_size

    service = ManualIngestionService(settings=settings)
    counts = service.ingest_registry(
        registry_path=settings.equipment_registry_path,
        data_root=args.data_root,
        batch_size=args.batch_size,
    )
    print(
        json.dumps(
            {
                "indexed_by_equipment": counts,
                "total": sum(counts.values()),
                "tokens_llm": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
