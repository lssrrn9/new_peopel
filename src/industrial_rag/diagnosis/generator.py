"""Generación de diagnóstico con LLM o modo extractivo (sin API)."""

from __future__ import annotations

import re
from typing import Protocol

import httpx

from industrial_rag.config import Settings, get_settings
from industrial_rag.diagnosis.prompts import (
    SYSTEM_PROMPT,
    UNAVAILABLE_MESSAGE,
    build_user_prompt,
)
from industrial_rag.models import DiagnosticReport, RetrievedChunk


class LLMClient(Protocol):
    def complete(self, system: str, user: str) -> str: ...


class AnthropicClient:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def complete(self, system: str, user: str) -> str:
        response = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": self.model,
                "max_tokens": 1200,
                "system": system,
                "messages": [{"role": "user", "content": user}],
            },
            timeout=60.0,
        )
        response.raise_for_status()
        data = response.json()
        parts = data.get("content", [])
        return "".join(p.get("text", "") for p in parts if p.get("type") == "text")


class GeminiClient:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def complete(self, system: str, user: str) -> str:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )
        response = httpx.post(
            url,
            json={
                "system_instruction": {"parts": [{"text": system}]},
                "contents": [{"parts": [{"text": user}]}],
            },
            timeout=60.0,
        )
        response.raise_for_status()
        data = response.json()
        candidates = data.get("candidates", [])
        if not candidates:
            return UNAVAILABLE_MESSAGE
        parts = candidates[0].get("content", {}).get("parts", [])
        return "".join(p.get("text", "") for p in parts)


class ExtractiveFallbackClient:
    """
    Sin API key: sintetiza el reporte solo con el texto recuperado.
    Garantiza trazabilidad y no inventa fuera del extracto.
    """

    def complete(self, system: str, user: str) -> str:
        # El prompt ya incluye el extracto; reutilizamos la sección final.
        if "EXTRACTO DEL MANUAL OFICIAL:" not in user:
            return UNAVAILABLE_MESSAGE
        extract = user.split("EXTRACTO DEL MANUAL OFICIAL:", 1)[1].strip()
        if not extract or extract == "(sin extractos)":
            return UNAVAILABLE_MESSAGE

        pages = sorted({int(p) for p in re.findall(r"página (\d+)", extract)})
        page_ref = ", ".join(f"pág. {p}" for p in pages) or "página no indicada"

        cause = ""
        solution = ""
        for line in extract.splitlines():
            stripped = line.strip()
            if not stripped.startswith("|") or "---" in stripped or "Código" in stripped:
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) >= 3:
                cause = cells[1]
                solution = cells[2]
                break

        description = cause or extract.split("\n", 1)[0][:300]
        field_tests = [
            line.lstrip("- ").strip()
            for line in extract.splitlines()
            if line.strip().startswith("- ")
        ][:4] or ["Seguir los puntos de prueba descritos en el extracto del manual."]

        causes = [cause] if cause else ["Revisar causas indicadas en el extracto del manual."]
        actions = [solution] if solution else ["Aplicar la solución del manual oficial."]

        causes_block = "\n".join(f"  {i}. {item}" for i, item in enumerate(causes, 1))
        tests_block = "\n".join(f"  {i}. {item}" for i, item in enumerate(field_tests, 1))
        actions_block = "\n".join(f"  {i}. {item}" for i, item in enumerate(actions, 1))

        return (
            f"* Descripción de la Falla: {description}\n"
            f"* Causas Probables:\n{causes_block}\n"
            f"* Pruebas de Campo:\n{tests_block}\n"
            f"* Acción Correctora Paso a Paso:\n{actions_block}\n"
            f"* Referencia del Manual: {page_ref}"
        )


class DiagnosticGenerator:
    def __init__(
        self,
        llm: LLMClient | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.llm = llm or self._default_llm()

    def _default_llm(self) -> LLMClient:
        if self.settings.anthropic_api_key:
            return AnthropicClient(
                self.settings.anthropic_api_key,
                self.settings.anthropic_model,
            )
        if self.settings.gemini_api_key:
            return GeminiClient(
                self.settings.gemini_api_key,
                self.settings.gemini_model,
            )
        return ExtractiveFallbackClient()

    def generate(
        self,
        equipment_id: str,
        fault_query: str,
        chunks: list[RetrievedChunk],
    ) -> DiagnosticReport:
        if not chunks:
            return DiagnosticReport(
                equipment_id=equipment_id,
                fault_query=fault_query,
                description=UNAVAILABLE_MESSAGE,
                probable_causes=[],
                field_tests=[],
                corrective_actions=[],
                manual_references=[],
                raw_response=UNAVAILABLE_MESSAGE,
                pages=[],
                unavailable=True,
            )

        user_prompt = build_user_prompt(equipment_id, fault_query, chunks)
        raw = self.llm.complete(SYSTEM_PROMPT, user_prompt).strip()
        pages = sorted({c.metadata.page_number for c in chunks})
        unavailable = UNAVAILABLE_MESSAGE.lower() in raw.lower() and len(raw) < 120

        return DiagnosticReport(
            equipment_id=equipment_id,
            fault_query=fault_query,
            description=_section(raw, "Descripción de la Falla"),
            probable_causes=_bullets(raw, "Causas Probables"),
            field_tests=_bullets(raw, "Pruebas de Campo"),
            corrective_actions=_bullets(raw, "Acción Correctora"),
            manual_references=_bullets(raw, "Referencia del Manual")
            or [f"páginas {pages}"],
            raw_response=raw,
            pages=pages,
            unavailable=unavailable,
        )


def _section(text: str, title: str) -> str:
    pattern = re.compile(
        rf"\*?\s*{re.escape(title)}\s*:?\s*(.+?)(?=\n\*|\n\n|$)",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else text.split("\n", 1)[0].strip()


def _bullets(text: str, title: str) -> list[str]:
    pattern = re.compile(
        rf"\*?\s*{re.escape(title)}[^\n]*\n(.*?)(?=\n\*\s|\n\* [A-Z]|$)",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return []
    block = match.group(1)
    # Cortar si aparece otra sección con título conocido
    for stopper in (
        "Causas Probables",
        "Pruebas de Campo",
        "Acción Correctora",
        "Referencia del Manual",
    ):
        if stopper.lower() == title.lower():
            continue
        cut = re.search(rf"\n\s*\*?\s*{re.escape(stopper)}", block, re.IGNORECASE)
        if cut:
            block = block[: cut.start()]
    items = re.findall(r"(?:^\s*\d+\.|^\s*-|^\s*\*)\s+(.+)", block, re.MULTILINE)
    return [item.strip().rstrip(".") for item in items if item.strip()]
