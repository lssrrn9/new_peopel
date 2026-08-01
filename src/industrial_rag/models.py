"""Modelos de dominio: metadatos obligatorios y reportes de diagnóstico."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class ChunkMetadata(BaseModel):
    """Metadatos obligatorios de cada fragmento indexado."""

    equipment_id: str = Field(..., min_length=1, description="ID único del equipo en planta")
    manufacturer: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)
    line: str = Field(..., min_length=1, description="Línea de producción")
    manual_version: str = Field(..., min_length=1)
    page_number: int = Field(..., ge=1)
    section: str | None = Field(
        default=None,
        description="Sección del manual (ej. fault_codes, wiring, maintenance)",
    )
    source_file: str | None = None

    @field_validator("equipment_id", "manufacturer", "model", "line", "manual_version")
    @classmethod
    def strip_nonempty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Campo de metadatos obligatorio vacío")
        return cleaned


class ManualChunk(BaseModel):
    """Fragmento listo para indexar en la base vectorial."""

    text: str = Field(..., min_length=1)
    metadata: ChunkMetadata

    def to_payload(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "metadata": self.metadata.model_dump(),
        }


class EquipmentRecord(BaseModel):
    """Relación Equipo → Archivo PDF / fabricante / línea."""

    equipment_id: str
    name: str
    manufacturer: str
    model: str
    line: str
    manual_file: str
    manual_version: str
    qr_code: str | None = None


class FaultTrigger(BaseModel):
    """Payload de entrada: alarma automática o selección manual del técnico."""

    equipment_id: str
    query: str = Field(..., min_length=1, description="Código o descripción de falla")
    source: str = Field(
        default="manual",
        description="mqtt | webhook | appsheet | scada | manual",
    )
    alarm_code: str | None = None
    technician_id: str | None = None


class RetrievedChunk(BaseModel):
    text: str
    metadata: ChunkMetadata
    score: float


class DiagnosticReport(BaseModel):
    equipment_id: str
    fault_query: str
    description: str
    probable_causes: list[str]
    field_tests: list[str]
    corrective_actions: list[str]
    manual_references: list[str]
    raw_response: str
    pages: list[int]
    unavailable: bool = False
