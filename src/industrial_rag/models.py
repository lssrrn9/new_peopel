"""Modelos de dominio: metadatos obligatorios y reportes de diagnóstico."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class ChunkMetadata(BaseModel):
    """Metadatos obligatorios de cada fragmento indexado.

    La arquitectura es multi-máquina: el mismo índice puede servir a una
    formadora de tubos, una línea de empaque u otra planta, siempre que
    cada chunk lleve machine_id + equipment_id.
    """

    machine_id: str = Field(
        ...,
        min_length=1,
        description="ID de la máquina o línea completa (ej. TUBE-FORMER-01)",
    )
    equipment_id: str = Field(
        ...,
        min_length=1,
        description="ID único del equipo dentro de la máquina",
    )
    manufacturer: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)
    line: str = Field(..., min_length=1, description="Línea / área de producción")
    manual_version: str = Field(..., min_length=1)
    page_number: int = Field(..., ge=1)
    section: str | None = Field(
        default=None,
        description="Sección del manual (ej. fault_codes, wiring, maintenance)",
    )
    fault_codes: list[str] = Field(
        default_factory=list,
        description="Códigos de falla detectados en el fragmento (AL 38, E-05…)",
    )
    source_file: str | None = None

    @field_validator(
        "machine_id",
        "equipment_id",
        "manufacturer",
        "model",
        "line",
        "manual_version",
    )
    @classmethod
    def strip_nonempty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Campo de metadatos obligatorio vacío")
        return cleaned

    @field_validator("fault_codes")
    @classmethod
    def normalize_fault_codes(cls, values: list[str]) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()
        for raw in values:
            code = " ".join(raw.upper().split())
            if code and code not in seen:
                seen.add(code)
                normalized.append(code)
        return normalized


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
    """Relación Máquina → Equipo → Archivo PDF / fabricante."""

    machine_id: str = Field(
        ...,
        description="Máquina a la que pertenece el equipo (reutilizable por planta)",
    )
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
    machine_id: str | None = Field(
        default=None,
        description="Opcional: restringe aún más a una máquina concreta",
    )
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
    machine_id: str | None = None
