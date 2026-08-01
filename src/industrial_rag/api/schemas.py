"""Esquemas HTTP para AppSheet / n8n / SCADA."""

from __future__ import annotations

from pydantic import BaseModel, Field

from industrial_rag.models import DiagnosticReport


class TroubleshootRequest(BaseModel):
    equipment_id: str = Field(..., examples=["VFD-LINE1-02"])
    query: str = Field(..., examples=["Falla E-05"])
    source: str = Field(default="manual", examples=["appsheet", "mqtt", "webhook"])
    alarm_code: str | None = None
    technician_id: str | None = None


class TroubleshootResponse(BaseModel):
    ok: bool = True
    report: DiagnosticReport
    latency_hint: str = "Respuesta filtrada por equipment_id (sin contaminación cruzada)"


class HealthResponse(BaseModel):
    status: str
    collection: str
    registry_equipment_count: int


class IndexResponse(BaseModel):
    indexed_chunks: int
