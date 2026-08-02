"""División de texto en fragmentos con metadatos obligatorios."""

from __future__ import annotations

import re
from typing import Callable, Iterable

from industrial_rag.ingestion.fault_codes import extract_fault_codes
from industrial_rag.models import ChunkMetadata, ManualChunk

# Filas tipo: E-05 | Sobrecorriente | Verificar motor
_FAULT_ROW = re.compile(
    r"(?P<code>[A-Z]?-?\d{1,4}|E-?\d{2,4}|F\d{2,4}|ALM?\s*\d{0,4})"
    r"\s*[|:]\s*(?P<body>.+)",
    re.IGNORECASE,
)


def split_plain_text(
    text: str,
    *,
    metadata_base: ChunkMetadata,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[ManualChunk]:
    """Parte texto continuo en chunks con overlap, preservando metadatos."""
    cleaned = re.sub(r"\n{3,}", "\n\n", text.strip())
    if not cleaned:
        return []

    paragraphs = [p.strip() for p in cleaned.split("\n\n") if p.strip()]
    chunks: list[ManualChunk] = []
    buffer = ""

    for paragraph in paragraphs:
        candidate = f"{buffer}\n\n{paragraph}".strip() if buffer else paragraph
        if len(candidate) <= chunk_size:
            buffer = candidate
            continue
        if buffer:
            chunks.append(_make_chunk(buffer, metadata_base))
        if len(paragraph) <= chunk_size:
            buffer = paragraph
        else:
            for piece in _window(paragraph, chunk_size, chunk_overlap):
                chunks.append(_make_chunk(piece, metadata_base))
            buffer = ""

    if buffer:
        chunks.append(_make_chunk(buffer, metadata_base))
    return chunks


def chunk_fault_table_markdown(
    markdown_table: str,
    *,
    metadata_base: ChunkMetadata,
) -> list[ManualChunk]:
    """
    Procesa tablas de códigos de falla conservando la relación
    Código | Causa | Solución en Markdown (regla de oro del diseño).
    Cada fila se indexa con su fault_code en metadatos.
    """
    rows = [line.strip() for line in markdown_table.splitlines() if line.strip()]
    header_cells = _detect_header(rows)
    chunks: list[ManualChunk] = []

    for row in rows:
        if row.startswith("| ---") or set(row.replace("|", "").strip()) <= {"-", " "}:
            continue
        lowered = row.lower()
        if lowered.startswith("| código") or lowered.startswith("| code"):
            continue
        if any(h and h.lower() in lowered for h in (header_cells[:1] if header_cells else [])):
            # Saltar fila de encabezado ya detectada
            if "causa" in lowered or "cause" in lowered or "descrip" in lowered:
                continue

        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) >= 3:
            code, cause, solution = cells[0], cells[1], cells[2]
            header = header_cells or ["Código", "Causa", "Solución"]
            # Repetir encabezado en cada chunk (evita pérdida de contexto)
            text = (
                f"| {' | '.join(header[:3])} |\n"
                f"| --- | --- | --- |\n"
                f"| {code} | {cause} | {solution} |"
            )
            codes = extract_fault_codes(code) or [_normalize_code(code)]
            meta = metadata_base.model_copy(
                update={"section": "fault_codes", "fault_codes": [c for c in codes if c]}
            )
            chunks.append(ManualChunk(text=text, metadata=meta))
            continue

        match = _FAULT_ROW.match(row)
        if match:
            code = match.group("code").strip()
            text = f"Falla {code}: {match.group('body').strip()}"
            codes = extract_fault_codes(code) or [_normalize_code(code)]
            meta = metadata_base.model_copy(
                update={"section": "fault_codes", "fault_codes": [c for c in codes if c]}
            )
            chunks.append(ManualChunk(text=text, metadata=meta))

    return chunks


def merge_page_chunks(
    pages: Iterable[tuple[int, str]],
    metadata_factory: Callable[[int], ChunkMetadata],
) -> list[ManualChunk]:
    """Convierte páginas (número, texto) en chunks con page_number correcto."""
    result: list[ManualChunk] = []
    for page_number, page_text in pages:
        base = metadata_factory(page_number)
        if _looks_like_fault_table(page_text):
            result.extend(chunk_fault_table_markdown(page_text, metadata_base=base))
        else:
            result.extend(split_plain_text(page_text, metadata_base=base))
    return result


def _looks_like_fault_table(text: str) -> bool:
    lowered = text.lower()
    has_header = ("código" in lowered or "code" in lowered) and (
        "causa" in lowered or "cause" in lowered or "soluci" in lowered
    )
    pipe_rows = sum(1 for line in text.splitlines() if line.count("|") >= 2)
    return has_header or pipe_rows >= 3


def _detect_header(rows: list[str]) -> list[str]:
    for row in rows[:3]:
        if row.count("|") < 2:
            continue
        cells = [c.strip() for c in row.strip("|").split("|")]
        joined = " ".join(cells).lower()
        if "código" in joined or "code" in joined or "alarm" in joined:
            return cells
    return []


def _window(text: str, size: int, overlap: int) -> list[str]:
    step = max(size - overlap, 1)
    return [text[i : i + size] for i in range(0, len(text), step)]


def _normalize_code(raw: str) -> str:
    return " ".join(raw.upper().split())


def _make_chunk(text: str, metadata: ChunkMetadata) -> ManualChunk:
    codes = extract_fault_codes(text)
    meta = metadata.model_copy(update={"fault_codes": codes}) if codes else metadata.model_copy()
    if codes and meta.section is None:
        meta.section = "fault_codes"
    return ManualChunk(text=text.strip(), metadata=meta)
