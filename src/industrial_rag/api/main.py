"""API FastAPI: trigger manual (AppSheet) o automático (webhook/MQTT bridge)."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from industrial_rag.api.schemas import (
    HealthResponse,
    IndexResponse,
    TroubleshootRequest,
    TroubleshootResponse,
)
from industrial_rag.config import get_settings
from industrial_rag.models import FaultTrigger
from industrial_rag.pipeline import TroubleshootingPipeline

_pipeline: TroubleshootingPipeline | None = None


def get_pipeline() -> TroubleshootingPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = TroubleshootingPipeline()
    return _pipeline


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    pipeline = get_pipeline()
    # Auto-carga del piloto si hay datos de muestra
    if settings.sample_chunks_path.exists():
        pipeline.load_pilot_data()
    yield


app = FastAPI(
    title="Industrial RAG Troubleshooting",
    description=(
        "Pipeline RAG con enrutamiento por metadatos para diagnóstico "
        "de fallas en línea de producción."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    pipeline = get_pipeline()
    return HealthResponse(
        status="ok",
        collection=settings.qdrant_collection,
        registry_equipment_count=len(pipeline.router.registry),
    )


@app.post("/troubleshoot", response_model=TroubleshootResponse)
def troubleshoot(request: TroubleshootRequest) -> TroubleshootResponse:
    """
    Opción B (manual) / Webhook n8n:
    Payload: { equipment_id, query }
    """
    pipeline = get_pipeline()
    trigger = FaultTrigger(
        equipment_id=request.equipment_id,
        query=request.query,
        source=request.source,
        alarm_code=request.alarm_code,
        technician_id=request.technician_id,
    )
    try:
        report = pipeline.troubleshoot(trigger)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return TroubleshootResponse(report=report)


@app.post("/webhook/alarm", response_model=TroubleshootResponse)
def webhook_alarm(request: TroubleshootRequest) -> TroubleshootResponse:
    """Opción A: alarma PLC/SCADA vía webhook (MQTT bridge → n8n → aquí)."""
    request.source = request.source or "webhook"
    return troubleshoot(request)


@app.post("/admin/reindex-pilot", response_model=IndexResponse)
def reindex_pilot() -> IndexResponse:
    pipeline = get_pipeline()
    count = pipeline.load_pilot_data()
    return IndexResponse(indexed_chunks=count)
