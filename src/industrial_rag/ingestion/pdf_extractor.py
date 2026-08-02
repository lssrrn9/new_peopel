"""Extracción local de PDFs (0 tokens LLM) con soporte de tablas de falla."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator


def extract_pages(pdf_path: Path) -> list[tuple[int, str]]:
    """
    Extrae texto por página (1-indexed) sin enviar nada a un LLM.

    Preferencia: PyMuPDF (mejor con tablas). Fallback: pypdf.
    """
    return list(iter_pages(pdf_path))


def iter_pages(pdf_path: Path) -> Iterator[tuple[int, str]]:
    """Generador página a página para no saturar RAM en manuales 1000+ págs."""
    try:
        yield from _iter_pymupdf(pdf_path)
    except ImportError:
        yield from _iter_pypdf(pdf_path)


def extract_pages_from_bytes(pdf_bytes: bytes, filename: str = "upload.pdf") -> list[tuple[int, str]]:
    """Extrae páginas desde bytes (endpoint de ingestión HTTP)."""
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "PyMuPDF (pymupdf) es requerido para ingestión por upload. "
            "Instale con: pip install pymupdf"
        ) from exc

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages: list[tuple[int, str]] = []
    try:
        for index in range(len(doc)):
            page = doc[index]
            text = _page_text_pymupdf(page)
            if text.strip():
                pages.append((index + 1, text.strip()))
    finally:
        doc.close()
    _ = filename
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


def _iter_pymupdf(pdf_path: Path) -> Iterator[tuple[int, str]]:
    import fitz  # type: ignore

    doc = fitz.open(pdf_path)
    try:
        for index in range(len(doc)):
            text = _page_text_pymupdf(doc[index])
            if text.strip():
                yield index + 1, text.strip()
    finally:
        doc.close()


def _page_text_pymupdf(page) -> str:
    """
    Preferir dict de bloques/tablas para no aplastar filas de códigos de falla.
    Si hay tablas detectables, serializarlas a Markdown con encabezado.
    """
    table_md = _tables_as_markdown(page)
    if table_md:
        # Mantener también el texto no-tabla de la página
        plain = page.get_text("text") or ""
        # Evitar duplicar si casi todo es tabla
        if len(plain.strip()) > len(table_md) + 80:
            return f"{plain.strip()}\n\n{table_md}".strip()
        return table_md

    # "blocks" conserva mejor el orden visual que el volcado lineal puro
    blocks = page.get_text("blocks") or []
    parts: list[str] = []
    for block in blocks:
        if len(block) >= 5 and isinstance(block[4], str):
            part = block[4].strip()
            if part:
                parts.append(part)
    if parts:
        return "\n\n".join(parts)
    return page.get_text("text") or ""


def _tables_as_markdown(page) -> str:
    """Convierte tablas de la página a Markdown (Código | Causa | Solución…)."""
    finder = getattr(page, "find_tables", None)
    if finder is None:
        return ""
    try:
        found = finder()
    except Exception:
        return ""

    tables = getattr(found, "tables", None) or []
    if not tables:
        return ""

    sections: list[str] = []
    for table in tables:
        try:
            rows = table.extract()
        except Exception:
            continue
        if not rows:
            continue
        header = [str(c or "").strip() or "col" for c in rows[0]]
        md_lines = [
            "| " + " | ".join(header) + " |",
            "| " + " | ".join("---" for _ in header) + " |",
        ]
        for row in rows[1:]:
            cells = [str(c or "").strip().replace("\n", " ") for c in row]
            # Alinear longitud
            if len(cells) < len(header):
                cells.extend([""] * (len(header) - len(cells)))
            md_lines.append("| " + " | ".join(cells[: len(header)]) + " |")
        sections.append("\n".join(md_lines))
    return "\n\n".join(sections)


def _iter_pypdf(pdf_path: Path) -> Iterator[tuple[int, str]]:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            yield index, text.strip()


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
