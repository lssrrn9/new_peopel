"""CLI: indexar piloto y ejecutar diagnóstico en consola."""

from __future__ import annotations

import argparse
import json
import os

from industrial_rag.config import Settings
from industrial_rag.models import FaultTrigger
from industrial_rag.pipeline import TroubleshootingPipeline


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="RAG industrial con router de metadatos",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    index_p = sub.add_parser("index-pilot", help="Indexa chunks de data/sample_chunks")
    index_p.add_argument("--memory", action="store_true", help="Usar Qdrant en memoria")

    run_p = sub.add_parser("troubleshoot", help="Diagnóstico filtrado por equipo")
    run_p.add_argument("--equipment-id", required=True)
    run_p.add_argument("--query", required=True)
    run_p.add_argument("--memory", action="store_true")
    run_p.add_argument(
        "--reindex",
        action="store_true",
        help="Reindexa datos piloto antes de consultar",
    )

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

    pipeline = TroubleshootingPipeline(settings=settings)

    if args.command == "index-pilot":
        count = pipeline.load_pilot_data()
        print(json.dumps({"indexed_chunks": count}, ensure_ascii=False, indent=2))
        return

    if args.command == "troubleshoot":
        if args.reindex or settings.use_memory_qdrant:
            pipeline.load_pilot_data()
        report = pipeline.troubleshoot(
            FaultTrigger(equipment_id=args.equipment_id, query=args.query)
        )
        print(report.model_dump_json(indent=2, ensure_ascii=False))
        return


if __name__ == "__main__":
    main()
