"""API FastAPI: ingestión local de PDFs + consulta filtrada multi-máquina."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from industrial_rag.api.schemas import (
    HealthResponse,
    IndexResponse,
    IngestResponse,
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
    if settings.sample_chunks_path.exists():
        pipeline.load_pilot_data()
    yield


app = FastAPI(
    title="Industrial RAG Multi-Máquina",
    description=(
        "Ingesta local de manuales PDF (0 tokens LLM) y diagnóstico filtrado "
        "por machine_id + equipment_id. Reutilizable para formadoras de tubos "
        "u otras líneas con equipos de distintos fabricantes."
    ),
    version="0.2.0",
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
        ingestion_uses_llm=False,
    )


@app.post("/troubleshoot", response_model=TroubleshootResponse)
def troubleshoot(request: TroubleshootRequest) -> TroubleshootResponse:
    pipeline = get_pipeline()
    trigger = FaultTrigger(
        equipment_id=request.equipment_id,
        query=request.query,
        machine_id=request.machine_id,
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
    request.source = request.source or "webhook"
    return troubleshoot(request)


@app.post("/admin/reindex-pilot", response_model=IndexResponse)
def reindex_pilot() -> IndexResponse:
    pipeline = get_pipeline()
    count = pipeline.load_pilot_data()
    return IndexResponse(indexed_chunks=count, tokens_llm=0)


@app.post("/admin/ingest-registry", response_model=IndexResponse)
def ingest_registry() -> IndexResponse:
    """Indexa todos los PDF/MD del registro. 0 tokens LLM."""
    pipeline = get_pipeline()
    counts = pipeline.ingest_registry()
    return IndexResponse(indexed_chunks=sum(counts.values()), tokens_llm=0)


@app.post("/ingestar", response_model=IngestResponse)
async def ingestar_pdf(
    file: UploadFile = File(...),
    equipment_id: str = Form(...),
) -> IngestResponse:
    """
    Ingesta un manual PDF sin consumir tokens de LLM comercial.
    Los metadatos (machine_id, fabricante, modelo) salen del registro de equipos.
    """
    pipeline = get_pipeline()
    try:
        equipment = pipeline.router.resolve_equipment(equipment_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    contents = await file.read()
    filename = file.filename or "manual.pdf"
    try:
        count = pipeline.ingestion.ingest_pdf_bytes(
            equipment,
            contents,
            filename,
            batch_size=pipeline.settings.ingest_batch_size,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return IngestResponse(
        equipment_id=equipment.equipment_id,
        machine_id=equipment.machine_id,
        indexed_chunks=count,
        tokens_llm=0,
        manual=filename,
    )
