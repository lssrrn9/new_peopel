#!/usr/bin/env python3
"""Genera `VER_EL_CURSO.md`: el curso completo como galería de imágenes.

Permite leer las 126 diapositivas directamente en GitHub, sin descargar el
.pptx ni abrir PowerPoint. Requiere haber exportado antes las imágenes:

    python3 generar_presentacion.py
    soffice --headless --convert-to pdf --outdir salida \
            salida/CURSO_YASKAWA_SERVOPACK_3kW.pptx
    pdftoppm -r 96 -png salida/CURSO_YASKAWA_SERVOPACK_3kW.pdf diapositivas/d
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generar_presentacion import construir  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(BASE, "VER_EL_CURSO.md")


def _limpio(texto: str) -> str:
    """Quita el marcado en línea del título para usarlo en Markdown."""
    return texto.replace("**", "").replace("`", "").replace("\n", " ").strip()


def main() -> int:
    deck = construir()
    modulos: list[tuple[int, str]] = []
    for i, (tipo, titulo, _) in enumerate(deck.outline, start=1):
        if tipo == "Módulo":
            modulos.append((i, _limpio(titulo)))

    out: list[str] = [
        "# Ver el curso completo",
        "",
        "Las 126 diapositivas del curso **Servo drives YASKAWA SERVOPACK "
        "(3 kW)**, en imágenes. No hace falta descargar nada ni tener "
        "PowerPoint: basta con desplazarse por esta página.",
        "",
        "| También disponible como | |",
        "|---|---|",
        "| Presentación editable | [`CURSO_YASKAWA_SERVOPACK_3kW.pptx`]"
        "(salida/CURSO_YASKAWA_SERVOPACK_3kW.pptx) |",
        "| Documento PDF | [`CURSO_YASKAWA_SERVOPACK_3kW.pdf`]"
        "(salida/CURSO_YASKAWA_SERVOPACK_3kW.pdf) |",
        "| Guion del instructor (notas de todas las láminas) | "
        "[`GUIA_DEL_INSTRUCTOR.md`](salida/GUIA_DEL_INSTRUCTOR.md) |",
        "",
        "## Índice",
        "",
    ]
    for num, titulo in modulos:
        ancla = re.sub(r"[^a-z0-9áéíóúñ\s-]", "", titulo.lower())
        ancla = ancla.strip().replace(" ", "-")
        out.append(f"- [{titulo}](#{ancla}) · lámina {num}")
    out += ["", "---", ""]

    inicio = {n for n, _ in modulos}
    for i, (tipo, titulo, _) in enumerate(deck.outline, start=1):
        imagen = f"diapositivas/d-{i:03d}.png"
        if i in inicio:
            out += ["", f"## {_limpio(titulo)}", ""]
        elif tipo == "Portada":
            out += ["", "## Portada", ""]
        out += [
            f"**{i}. {_limpio(titulo)}**",
            "",
            f'<img src="{imagen}" width="900" alt="Diapositiva {i}">',
            "",
        ]

    with open(DESTINO, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    print(f"Galería generada: {DESTINO} ({len(deck.outline)} diapositivas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
