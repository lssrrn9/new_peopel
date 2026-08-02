"""Detección de códigos de falla alfanuméricos en texto de manuales."""

from __future__ import annotations

import re

# Patrones típicos industriales: AL 38, E-05, ERR-04, F123, Alarm 39, Fault 12
_FAULT_PATTERNS = [
    re.compile(
        r"\b(?:AL|ALM|ALARM|ERR|ERROR|FAULT|FLT|W|WARN|WARNING)\s*[-:]?\s*\d{1,4}\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bE\s*[-:]?\s*\d{2,4}\b", re.IGNORECASE),
    re.compile(r"\bF\d{2,4}\b", re.IGNORECASE),
    re.compile(r"\bA\d{2,4}\b", re.IGNORECASE),
]


def extract_fault_codes(text: str) -> list[str]:
    """Extrae códigos de falla normalizados sin consumir tokens de LLM."""
    found: list[str] = []
    seen: set[str] = set()
    for pattern in _FAULT_PATTERNS:
        for match in pattern.finditer(text):
            code = _normalize(match.group(0))
            if code not in seen:
                seen.add(code)
                found.append(code)
    return found


def query_fault_codes(query: str) -> list[str]:
    """Códigos presentes en la pregunta del técnico."""
    return extract_fault_codes(query)


def _normalize(raw: str) -> str:
    cleaned = re.sub(r"\s+", " ", raw.strip().upper())
    cleaned = re.sub(r"\s*([-:])\s*", r"\1", cleaned)
    # Unificar prefijos largos a formas cortas comunes
    cleaned = cleaned.replace("ALARM ", "AL ").replace("ALARM:", "AL ")
    cleaned = cleaned.replace("WARNING ", "W ").replace("ERROR ", "ERR ")
    cleaned = cleaned.replace("FAULT ", "FAULT ").replace("FLT ", "FAULT ")
    return cleaned
