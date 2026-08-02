"""Esquemas HTTP para AppSheet / n8n / SCADA / ingestión."""

from __future__ import annotations

from pydantic import BaseModel, Field

from industrial_rag.models import DiagnosticReport


class TroubleshootRequest(BaseModel):
    equipment_id: str = Field(..., examples=["VFD-TUBE-01"])
    query: str = Field(..., examples=["Falla E-05"])
    machine_id: str | None = Field(default=None, examples=["TUBE-FORMER-01"])
    source: str = Field(default="manual", examples=["appsheet", "mqtt", "webhook"])
    alarm_code: str | None = None
    technician_id: str | None = None


class TroubleshootResponse(BaseModel):
    ok: bool = True
    report: DiagnosticReport
    latency_hint: str = (
        "Respuesta filtrada por machine_id + equipment_id (sin contaminación cruzada)"
    )


class HealthResponse(BaseModel):
    status: str
    collection: str
    registry_equipment_count: int
    ingestion_uses_llm: bool = False


class IndexResponse(BaseModel):
    indexed_chunks: int
    tokens_llm: int = 0


class IngestResponse(BaseModel):
    status: str = "ok"
    equipment_id: str
    machine_id: str
    indexed_chunks: int
    tokens_llm: int = 0
    manual: str
