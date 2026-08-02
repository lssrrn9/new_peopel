#!/usr/bin/env python3
"""
Ingesta un PDF de 1000+ páginas en Qdrant sin gastar tokens de LLM.

Uso:
  python scripts/ingest_pdf_manual.py \\
    --pdf manuals/Danfoss_FC302.pdf \\
    --equipment-id VFD-TUBE-01 \\
    --memory
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from industrial_rag.config import Settings
from industrial_rag.ingestion.service import ManualIngestionService
from industrial_rag.retrieval.router import MetadataRouter


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingesta PDF local → Qdrant (0 tokens LLM)")
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--equipment-id", required=True)
    parser.add_argument("--memory", action="store_true")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("data/equipment_registry.json"),
    )
    args = parser.parse_args()

    if args.memory:
        os.environ["USE_MEMORY_QDRANT"] = "true"

    settings = Settings(
        use_memory_qdrant=args.memory,
        equipment_registry_path=args.registry,
        ingest_batch_size=args.batch_size,
    )
    router = MetadataRouter(args.registry)
    equipment = router.resolve_equipment(args.equipment_id)
    service = ManualIngestionService(settings=settings)
    count = service.ingest_equipment_file(
        equipment,
        args.pdf,
        batch_size=args.batch_size,
    )
    print(
        json.dumps(
            {
                "machine_id": equipment.machine_id,
                "equipment_id": equipment.equipment_id,
                "manual": str(args.pdf),
                "indexed_chunks": count,
                "tokens_llm": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
