"""Plantilla de prompting estricto para diagnóstico industrial."""

from __future__ import annotations

from industrial_rag.models import RetrievedChunk

SYSTEM_PROMPT = (
    "Actúa como un especialista en mantenimiento industrial. "
    "Con base ÚNICAMENTE en el extracto del manual proporcionado, "
    "genera la guía de troubleshooting. "
    "No inventes datos fuera del manual. "
    "Si la información no está explícita en el extracto, responde exactamente: "
    "'Información no disponible en el manual oficial'."
)

RESPONSE_FORMAT = """Formato de Respuesta Requerido:
* Descripción de la Falla: (Explicación breve).
* Causas Probables: (Lista priorizada de la más a la menos común).
* Pruebas de Campo: (Puntos de prueba específicos con multímetro/instrumentación y valores esperados).
* Acción Correctora Paso a Paso.
* Referencia del Manual: (Indicar la página exacta de la fuente).

Si la información no está explícita en el extracto, responde: 'Información no disponible en el manual oficial'."""


def build_user_prompt(
    equipment_id: str,
    fault_query: str,
    chunks: list[RetrievedChunk],
) -> str:
    context_blocks = []
    for index, chunk in enumerate(chunks, start=1):
        meta = chunk.metadata
        context_blocks.append(
            f"[Extracto {index} | página {meta.page_number} | "
            f"{meta.manufacturer} {meta.model} | sección={meta.section or 'n/a'}]\n"
            f"{chunk.text}"
        )
    context = "\n\n---\n\n".join(context_blocks) if context_blocks else "(sin extractos)"

    return (
        f"Equipo: {equipment_id}\n"
        f"Consulta de falla: {fault_query}\n\n"
        f"Actúa como un especialista en mantenimiento industrial. "
        f"Con base ÚNICAMENTE en el siguiente extracto del manual correspondiente "
        f"al equipo {equipment_id}, genera la guía de troubleshooting.\n\n"
        f"{RESPONSE_FORMAT}\n\n"
        f"EXTRACTO DEL MANUAL OFICIAL:\n{context}"
    )


UNAVAILABLE_MESSAGE = "Información no disponible en el manual oficial."
