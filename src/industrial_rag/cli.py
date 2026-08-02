"""CLI: ingestión local de PDFs (0 tokens) y diagnóstico filtrado."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from industrial_rag.config import Settings
from industrial_rag.models import EquipmentRecord, FaultTrigger
from industrial_rag.pipeline import TroubleshootingPipeline


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description=(
            "RAG industrial multi-máquina: ingestión local de PDFs (0 tokens LLM) "
            "y consulta filtrada por machine_id/equipment_id"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    index_p = sub.add_parser("index-pilot", help="Indexa chunks de data/sample_chunks")
    index_p.add_argument("--memory", action="store_true", help="Usar Qdrant en memoria")

    ingest_reg = sub.add_parser(
        "ingest-registry",
        help="Indexa todos los manuales PDF/MD del registro (0 tokens LLM)",
    )
    ingest_reg.add_argument("--memory", action="store_true")
    ingest_reg.add_argument("--batch-size", type=int, default=None)

    ingest_pdf = sub.add_parser(
        "ingest-pdf",
        help="Indexa un PDF concreto asociándolo a un equipo del registro",
    )
    ingest_pdf.add_argument("--pdf", type=Path, required=True)
    ingest_pdf.add_argument("--equipment-id", required=True)
    ingest_pdf.add_argument("--memory", action="store_true")
    ingest_pdf.add_argument("--batch-size", type=int, default=None)

    run_p = sub.add_parser("troubleshoot", help="Diagnóstico filtrado por equipo")
    run_p.add_argument("--equipment-id", required=True)
    run_p.add_argument("--query", required=True)
    run_p.add_argument("--machine-id", default=None)
    run_p.add_argument("--memory", action="store_true")
    run_p.add_argument(
        "--reindex",
        action="store_true",
        help="Reindexa datos piloto antes de consultar",
    )

    list_p = sub.add_parser("list-equipment", help="Lista equipos del registro")
    list_p.add_argument("--machine-id", default=None)

    serve_p = sub.add_parser("serve", help="Levanta API FastAPI")
    serve_p.add_argument("--host", default=None)
    serve_p.add_argument("--port", type=int, default=None)

    args = parser.parse_args(argv)

    if args.command == "serve":
        import uvicorn

        settings = Settings()
        uvicorn.run(
            "industrial_rag.api.main:app",
            host=args.host or settings.api_host,
            port=args.port or settings.api_port,
            reload=False,
        )
        return

    if getattr(args, "memory", False):
        os.environ["USE_MEMORY_QDRANT"] = "true"

    settings = Settings()
    if getattr(args, "memory", False):
        settings.use_memory_qdrant = True
    if getattr(args, "batch_size", None):
        settings.ingest_batch_size = args.batch_size

    pipeline = TroubleshootingPipeline(settings=settings)

    if args.command == "index-pilot":
        count = pipeline.load_pilot_data()
        print(json.dumps({"indexed_chunks": count}, ensure_ascii=False, indent=2))
        return

    if args.command == "ingest-registry":
        counts = pipeline.ingestion.ingest_registry(
            batch_size=settings.ingest_batch_size,
        )
        print(
            json.dumps(
                {"indexed_by_equipment": counts, "total": sum(counts.values())},
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.command == "ingest-pdf":
        equipment = pipeline.router.resolve_equipment(args.equipment_id)
        count = pipeline.ingestion.ingest_equipment_file(
            equipment,
            args.pdf,
            batch_size=settings.ingest_batch_size,
        )
        print(
            json.dumps(
                {
                    "equipment_id": equipment.equipment_id,
                    "machine_id": equipment.machine_id,
                    "indexed_chunks": count,
                    "tokens_llm": 0,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.command == "list-equipment":
        items: list[EquipmentRecord]
        if args.machine_id:
            items = pipeline.router.list_by_machine(args.machine_id)
        else:
            items = list(pipeline.router.registry.values())
        print(
            json.dumps(
                [item.model_dump() for item in items],
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.command == "troubleshoot":
        if args.reindex or settings.use_memory_qdrant:
            pipeline.load_pilot_data()
        report = pipeline.troubleshoot(
            FaultTrigger(
                equipment_id=args.equipment_id,
                query=args.query,
                machine_id=args.machine_id,
            )
        )
        print(report.model_dump_json(indent=2, ensure_ascii=False))
        return


if __name__ == "__main__":
    main()
