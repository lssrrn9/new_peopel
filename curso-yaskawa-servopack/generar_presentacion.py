#!/usr/bin/env python3
"""Genera la presentación del curso «Servo drives YASKAWA SERVOPACK».

Uso:
    python3 generar_presentacion.py [--salida RUTA] [--sin-guia]

Produce:
    salida/CURSO_YASKAWA_SERVOPACK_3kW.pptx   presentación completa
    salida/GUIA_DEL_INSTRUCTOR.md             guion con las notas de cada lámina
"""

from __future__ import annotations

import argparse
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from builder import Deck  # noqa: E402

FOOTER = ("Curso YASKAWA SERVOPACK · SGD7S-200A + servomotor 3 kW · "
          "material de formación")

MODULOS = [
    "contenido.m00_apertura",
    "contenido.m01_fundamentos",
    "contenido.m02_servopack",
    "contenido.m03_motor",
    "contenido.m04_dimensionamiento",
    "contenido.m05_instalacion",
    "contenido.m06_control",
    "contenido.m07_parametros",
    "contenido.m08_puesta_en_marcha",
    "contenido.m09_sintonizacion",
    "contenido.m10_seguridad",
    "contenido.m11_diagnostico",
    "contenido.m12_proyecto",
    "contenido.m13_anexos",
]


def construir() -> Deck:
    deck = Deck(FOOTER)
    for nombre in MODULOS:
        modulo = importlib.import_module(nombre)
        modulo.build(deck)
    return deck


def escribir_guia(deck: Deck, ruta: str) -> None:
    lineas = [
        "# Guía del instructor — Curso YASKAWA SERVOPACK (3 kW)",
        "",
        "Documento generado automáticamente a partir de las notas del orador de "
        "`CURSO_YASKAWA_SERVOPACK_3kW.pptx`.",
        "Sirve como guion de clase y como manual de estudio en texto plano.",
        "",
        f"**Total de diapositivas:** {len(deck.outline)}",
        "",
        "---",
        "",
    ]
    for i, (tipo, titulo, notas) in enumerate(deck.outline, start=1):
        if tipo == "Módulo":
            lineas += [f"## {titulo}", ""]
        else:
            lineas += [f"### {i}. {titulo}", ""]
        if notas:
            lineas += [notas.strip(), ""]
    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lineas))


def main() -> int:
    base = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--salida",
        default=os.path.join(base, "salida",
                             "CURSO_YASKAWA_SERVOPACK_3kW.pptx"),
        help="ruta del archivo .pptx de salida",
    )
    parser.add_argument("--sin-guia", action="store_true",
                        help="no generar la guía del instructor en Markdown")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.salida), exist_ok=True)
    deck = construir()
    deck.save(args.salida)
    print(f"Presentación generada: {args.salida}")
    print(f"Diapositivas: {len(deck.prs.slides._sldIdLst)}")

    if not args.sin_guia:
        guia = os.path.join(os.path.dirname(args.salida),
                            "GUIA_DEL_INSTRUCTOR.md")
        escribir_guia(deck, guia)
        print(f"Guía del instructor: {guia}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
