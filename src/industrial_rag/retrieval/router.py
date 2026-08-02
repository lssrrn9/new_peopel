"""Enrutamiento por metadatos: nunca buscar en toda la biblioteca."""

from __future__ import annotations

import json
from pathlib import Path

from industrial_rag.models import EquipmentRecord, FaultTrigger


class MetadataRouter:
    """
    Aplica filtro duro por equipment_id (+ machine_id / fabricante / modelo).

    Regla: la consulta vectorial NUNCA busca sin este filtro previo.
    Así el mismo índice sirve a varias máquinas sin contaminación cruzada.
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
                "Relacione machine_id + equipment_id → archivo PDF antes de consultar."
            )
        return self.registry[equipment_id]

    def list_by_machine(self, machine_id: str) -> list[EquipmentRecord]:
        return [eq for eq in self.registry.values() if eq.machine_id == machine_id]

    def build_filter(self, trigger: FaultTrigger) -> dict:
        """
        Construye el filtro de Qdrant restringido al equipo (y máquina) afectados.
        """
        equipment = self.registry.get(trigger.equipment_id)

        must = [
            {
                "key": "metadata.equipment_id",
                "match": {"value": trigger.equipment_id},
            }
        ]

        machine_id = trigger.machine_id
        if machine_id is None and equipment is not None:
            machine_id = equipment.machine_id
        if machine_id:
            must.append(
                {
                    "key": "metadata.machine_id",
                    "match": {"value": machine_id},
                }
            )

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
