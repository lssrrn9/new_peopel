"""Extracción de texto de PDFs con soporte para tablas de falla en Markdown."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


def extract_pages(pdf_path: Path) -> list[tuple[int, str]]:
    """
    Extrae texto por página (1-indexed).

    Nota operativa: las tablas de códigos de falla suelen romperse con
    extractores estándar. Para páginas de fallas preferir OCR multimodal
    o tablas ya convertidas a Markdown (ver load_markdown_manual).
    """
    reader = PdfReader(str(pdf_path))
    pages: list[tuple[int, str]] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append((index, text.strip()))
    return pages


def load_markdown_manual(md_path: Path) -> list[tuple[int, str]]:
    """
    Carga un manual en Markdown con marcadores de página:

        <!-- page: 114 -->
        contenido...
    """
    content = md_path.read_text(encoding="utf-8")
    pages: list[tuple[int, str]] = []
    current_page = 1
    buffer: list[str] = []

    for line in content.splitlines():
        marker = _page_marker(line)
        if marker is not None:
            if buffer:
                pages.append((current_page, "\n".join(buffer).strip()))
                buffer = []
            current_page = marker
            continue
        buffer.append(line)

    if buffer:
        pages.append((current_page, "\n".join(buffer).strip()))
    return [(p, t) for p, t in pages if t]


def _page_marker(line: str) -> int | None:
    stripped = line.strip().lower()
    if stripped.startswith("<!-- page:") and stripped.endswith("-->"):
        raw = stripped.removeprefix("<!-- page:").removesuffix("-->").strip()
        try:
            return int(raw)
        except ValueError:
            return None
    if stripped.startswith("# página ") or stripped.startswith("# page "):
        parts = stripped.split()
        try:
            return int(parts[-1])
        except ValueError:
            return None
    return None
