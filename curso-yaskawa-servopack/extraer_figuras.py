#!/usr/bin/env python3
"""Extrae del manual oficial las figuras que se integran en el curso.

El manual **no** se incluye en el repositorio (es propiedad de YASKAWA). Este
script lo descarga, renderiza las páginas indicadas y recorta la figura
correspondiente, dejando los PNG en `figuras/`.

    python3 extraer_figuras.py

Manual de referencia:
    Σ-X-Series AC Servo Drive · Σ-XS SERVOPACK with Analog Voltage/Pulse Train
    References · Product Manual · Model SGDXS-□□□□00□ · MANUAL NO. SIEP C710812 03I
    (YASKAWA Electric Corporation)

Las figuras resultantes son propiedad de YASKAWA y se emplean en el curso como
material de referencia técnica, citando siempre la fuente.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile

from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
FIGURAS = os.path.join(BASE, "figuras")
URL_MANUAL = "https://www.yaskawa.eu.com/_downloads/download_d21545"
DPI = 200

# (nombre, página del PDF, selección)
# La selección es o bien el índice del bloque de contenido dentro de la página
# (-1 = el bloque más alto), o bien una banda vertical explícita expresada como
# fracción de la altura de la página: (arriba, abajo).
Seleccion = int | tuple[float, float]

FIGURAS_MANUAL: list[tuple[str, int, Seleccion]] = [
    ("partes_servopack", 52, (0.075, 0.40)),
    ("diagrama_bloques_200a", 80, -1),
    ("conexiones_generales", 124, -1),
    ("potencia_protecciones", 134, (0.13, 0.54)),
    ("secuencia_encendido", 133, -1),
    ("regeneracion_externa", 141, -1),
    ("cableado_encoder", 145, -1),
    ("freno_retencion", 153, -1),
    ("cn1_conector", 157, (0.15, 0.31)),
    ("cn1_ejemplo_velocidad", 158, (0.23, 0.78)),
    ("cn1_ejemplo_posicion", 160, -1),
    ("cn1_circuitos_analogicos", 164, (0.045, 0.21)),
    ("cn1_circuitos_pulsos", 164, (0.28, 0.50)),
    ("cn1_circuitos_salida", 165, -1),
    ("cn8_seguridad", 167, (0.19, 0.44)),
    ("cn8_ejemplo", 167, (0.64, 0.87)),
    ("conexion_operador", 170, -1),
    ("monitor_analogico", 172, -1),
    ("emc_instalacion", 111, -1),
    ("puesta_a_tierra", 122, -1),
]


def _descargar_manual(destino: str) -> str:
    ruta = os.path.join(destino, "manual_sigmaX.pdf")
    if os.path.exists(ruta):
        return ruta
    print("Descargando el manual oficial (≈41 MB)…")
    subprocess.run(["curl", "-sSL", "--max-time", "300", "-o", ruta,
                    URL_MANUAL], check=True)
    return ruta


def _bloques(im: Image.Image, umbral: int = 245, hueco: int = 26,
             cabecera: float = 0.055, pie: float = 0.045
             ) -> list[tuple[int, int]]:
    """Devuelve las bandas verticales con contenido, saltando cabecera y pie."""
    gris = im.convert("L")
    ancho, alto = gris.size
    y0, y1 = int(alto * cabecera), int(alto * (1 - pie))
    pixeles = gris.load()
    llenas: list[bool] = []
    for y in range(y0, y1):
        fila = any(pixeles[x, y] < umbral for x in range(0, ancho, 3))
        llenas.append(fila)

    bandas: list[tuple[int, int]] = []
    inicio = None
    vacias = 0
    for i, llena in enumerate(llenas):
        if llena:
            if inicio is None:
                inicio = i
            vacias = 0
        elif inicio is not None:
            vacias += 1
            if vacias >= hueco:
                bandas.append((y0 + inicio, y0 + i - vacias))
                inicio = None
    if inicio is not None:
        bandas.append((y0 + inicio, y1))
    return [(a, b) for a, b in bandas if b - a > alto * 0.04]


def _recortar(im: Image.Image, banda: tuple[int, int],
              margen: int = 18) -> Image.Image:
    gris = im.convert("L")
    ancho = gris.size[0]
    pixeles = gris.load()
    x_min, x_max = ancho, 0
    for y in range(banda[0], banda[1], 2):
        for x in range(ancho):
            if pixeles[x, y] < 245:
                x_min = min(x_min, x)
                break
        for x in range(ancho - 1, -1, -1):
            if pixeles[x, y] < 245:
                x_max = max(x_max, x)
                break
    if x_min >= x_max:
        x_min, x_max = 0, ancho - 1
    caja = (max(x_min - margen, 0), max(banda[0] - margen, 0),
            min(x_max + margen, ancho), min(banda[1] + margen, im.size[1]))
    return im.crop(caja)


def main() -> int:
    os.makedirs(FIGURAS, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        cache = os.environ.get("MANUAL_CACHE", tmp)
        os.makedirs(cache, exist_ok=True)
        pdf = _descargar_manual(cache)

        for nombre, pagina, indice in FIGURAS_MANUAL:
            prefijo = os.path.join(tmp, f"pg{pagina}")
            subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-f",
                            str(pagina), "-l", str(pagina), pdf, prefijo],
                           check=True)
            candidatos = [f for f in os.listdir(tmp)
                          if f.startswith(f"pg{pagina}-")]
            if not candidatos:
                print(f"  ! sin render para la página {pagina}")
                continue
            im = Image.open(os.path.join(tmp, candidatos[0]))
            if isinstance(indice, tuple):
                alto = im.size[1]
                banda = (int(alto * indice[0]), int(alto * indice[1]))
            else:
                bandas = _bloques(im)
                if not bandas:
                    print(f"  ! sin bloques en la página {pagina}")
                    continue
                banda = (max(bandas, key=lambda b: b[1] - b[0]) if indice == -1
                         else bandas[min(indice, len(bandas) - 1)])
            fig = _recortar(im, banda)
            # Ancho máximo razonable para una diapositiva
            if fig.size[0] > 1800:
                escala = 1800 / fig.size[0]
                fig = fig.resize((1800, int(fig.size[1] * escala)),
                                 Image.LANCZOS)
            destino = os.path.join(FIGURAS, f"{nombre}.png")
            fig.convert("RGB").quantize(colors=64).save(destino, optimize=True)
            print(f"  {nombre:26s} p{pagina:<4d} {fig.size[0]}×{fig.size[1]}  "
                  f"{os.path.getsize(destino)//1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
