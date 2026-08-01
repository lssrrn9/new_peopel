"""Enrutamiento por metadatos: nunca buscar en toda la biblioteca."""

from __future__ import annotations

import json
from pathlib import Path

from industrial_rag.models import EquipmentRecord, FaultTrigger


class MetadataRouter:
    """
    Aplica filtro duro por equipment_id (y opcionalmente línea/fabricante).

    Regla: la consulta vectorial NUNCA busca sin este filtro previo.
    """

    def __init__(self, registry_path: Path | None = None) -> None:
        self.registry: dict[str, EquipmentRecord] = {}
        if registry_path and registry_path.exists():
            self.load_registry(registry_path)

    def load_registry(self, path: Path) -> None:
        data = json.loads(path.read_text(encoding="utf-8"))
        self.registry = {
            item["equipment_id"]: EquipmentRecord.model_validate(item)
            for item in data
        }

    def resolve_equipment(self, equipment_id: str) -> EquipmentRecord:
        if equipment_id not in self.registry:
            raise KeyError(
                f"Equipo '{equipment_id}' no está en el registro. "
                "Relacione ID → archivo PDF antes de consultar."
            )
        return self.registry[equipment_id]

    def build_filter(self, trigger: FaultTrigger) -> dict:
        """
        Construye el filtro de Qdrant restringido al equipo afectado.

        Payload recibido: { equipment_id, query }
        Filtro: metadata.equipment_id == equipment_id
        """
        equipment = None
        if trigger.equipment_id in self.registry:
            equipment = self.registry[trigger.equipment_id]

        must = [
            {
                "key": "metadata.equipment_id",
                "match": {"value": trigger.equipment_id},
            }
        ]
        # Refuerzo opcional si el registro está disponible
        if equipment is not None:
            must.append(
                {
                    "key": "metadata.manufacturer",
                    "match": {"value": equipment.manufacturer},
                }
            )
            must.append(
                {
                    "key": "metadata.model",
                    "match": {"value": equipment.model},
                }
            )

        return {"must": must}

    def search_query(self, trigger: FaultTrigger) -> str:
        """Normaliza la consulta (código de alarma + texto libre)."""
        parts = [trigger.query.strip()]
        if trigger.alarm_code and trigger.alarm_code not in trigger.query:
            parts.insert(0, trigger.alarm_code.strip())
        return " ".join(parts)
