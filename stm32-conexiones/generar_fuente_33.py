#!/usr/bin/env python3
"""Fuente de 3,3 V con AMS1117-3.3 desde 5 V.

SOT-223, patas hacia abajo y mirando el texto:
pin 1 GND, pin 2 VOUT, pin 3 VIN. La aleta es VOUT.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "figuras"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

INK = (28, 36, 48)
MUTED = (70, 84, 102)
WHITE = (255, 255, 255)
GREEN = (46, 125, 50)
GREEN_DK = (27, 94, 32)
RED = (183, 28, 28)
BLACK = (33, 33, 33)


def font(size, bold=False):
    return ImageFont.truetype(SANS_B if bold else SANS, size)


def text(draw, xy, msg, size, fill=INK, bold=False, anchor="lt"):
    draw.text(xy, msg, font=font(size, bold), fill=fill, anchor=anchor)


def rr(draw, box, radius, fill, outline=None, width=3):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def gnd(draw, x, y):
    draw.line((x, y, x, y + 14), fill=BLACK, width=4)
    draw.line((x - 20, y + 14, x + 20, y + 14), fill=BLACK, width=4)
    draw.line((x - 12, y + 24, x + 12, y + 24), fill=BLACK, width=4)
    draw.line((x - 5, y + 34, x + 5, y + 34), fill=BLACK, width=4)


def electro(draw, x, y1, y2):
    """Electrolítico entre y1 (positivo, arriba) e y2 (abajo)."""
    mid = (y1 + y2) // 2
    draw.line((x, y1, x, mid - 22), fill=BLACK, width=4)
    draw.line((x - 22, mid - 22, x + 22, mid - 22), fill=BLACK, width=5)
    draw.arc((x - 22, mid - 16, x + 22, mid + 18), 200, 340, fill=BLACK, width=5)
    draw.line((x, mid + 16, x, y2), fill=BLACK, width=4)
    text(draw, (x - 28, mid - 28), "+", 20, RED, True, "rm")


def ceramic(draw, x, y1, y2):
    mid = (y1 + y2) // 2
    draw.line((x, y1, x, mid - 16), fill=BLACK, width=4)
    draw.line((x - 18, mid - 16, x + 18, mid - 16), fill=BLACK, width=4)
    draw.line((x - 18, mid - 4, x + 18, mid - 4), fill=BLACK, width=4)
    draw.line((x, mid - 4, x, y2), fill=BLACK, width=4)


def build():
    w, h = 2100, 1500
    img = Image.new("RGB", (w, h), (244, 247, 251))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w, 110), fill=GREEN_DK)
    text(draw, (36, 18), "Fuente de 3,3 V", 38, WHITE, True)
    text(draw, (36, 68), "De 5 V a 3,3 V con un AMS1117-3.3. Sirve para el STM32 y los pulsadores.", 20, (200, 230, 201))

    # Bloque de entrada
    rr(draw, (40, 160, 300, 280), 14, WHITE, RED, 4)
    text(draw, (170, 200), "5 V", 32, RED, True, "mm")
    text(draw, (170, 242), "USB o fuente", 18, MUTED, anchor="mm")

    # Rail de 5 V hacia el pin VIN
    draw.line((300, 210, 760, 210), fill=RED, width=8)
    text(draw, (480, 182), "5 V", 20, RED, True, "mm")

    # Caps de entrada
    draw.line((430, 210, 430, 250), fill=BLACK, width=4)
    electro(draw, 430, 250, 430)
    text(draw, (460, 300), "10 µF", 20, INK, True, "lm")
    gnd(draw, 430, 430)
    draw.line((560, 210, 560, 270), fill=BLACK, width=4)
    ceramic(draw, 560, 270, 400)
    text(draw, (590, 310), "100 nF", 20, INK, True, "lm")
    draw.line((560, 400, 560, 430), fill=BLACK, width=4)
    draw.line((430, 444, 560, 444), fill=BLACK, width=3)

    # Regulador, terminales a los lados
    bx, by, bw, bh = 820, 250, 460, 280
    rr(draw, (bx, by, bx + bw, by + bh), 16, (255, 248, 225), (230, 81, 0), 4)
    text(draw, (bx + bw // 2, by + 90), "AMS1117-3.3", 32, (191, 54, 12), True, "mm")
    text(draw, (bx + bw // 2, by + 140), "regulador de 3,3 V", 18, MUTED, anchor="mm")
    text(draw, (bx + bw // 2, by + 190), "La aleta de metal", 18, INK, True, "mm")
    text(draw, (bx + bw // 2, by + 216), "también es la salida", 18, INK, True, "mm")

    # Pin VIN a la izquierda, a la altura del rail de 5 V
    draw.line((760, 210, bx, 210), fill=RED, width=8)
    rr(draw, (bx - 130, 178, bx, 242), 8, RED, None, 1)
    text(draw, (bx - 65, 210), "VIN  pin 3", 18, WHITE, True, "mm")

    # Pin GND
    draw.line((bx, 460, bx - 90, 460), fill=BLACK, width=6)
    draw.line((bx - 90, 460, bx - 90, 520), fill=BLACK, width=4)
    gnd(draw, bx - 90, 520)
    text(draw, (bx - 90, 575), "pin 1, GND", 18, BLACK, True, "mt")

    # Pin VOUT a la derecha
    draw.line((bx + bw, 320, bx + bw + 80, 320), fill=GREEN, width=8)
    rr(draw, (bx + bw, 288, bx + bw + 170, 352), 8, GREEN, None, 1)
    text(draw, (bx + bw + 85, 320), "VOUT  pin 2", 18, WHITE, True, "mm")
    draw.line((bx + bw + 170, 320, 1680, 320), fill=GREEN, width=8)
    text(draw, (1560, 290), "3,3 V", 22, GREEN, True, "mm")

    # Caps de salida
    draw.line((1500, 320, 1500, 380), fill=BLACK, width=4)
    electro(draw, 1500, 380, 560)
    text(draw, (1534, 430), "22 µF", 20, INK, True, "lm")
    gnd(draw, 1500, 560)
    draw.line((1620, 320, 1620, 400), fill=BLACK, width=4)
    ceramic(draw, 1620, 400, 520)
    text(draw, (1654, 430), "100 nF", 20, INK, True, "lm")
    draw.line((1620, 520, 1620, 574), fill=BLACK, width=4)
    draw.line((1500, 574, 1620, 574), fill=BLACK, width=3)

    # Borne
    rr(draw, (1720, 240, 2050, 420), 16, WHITE, GREEN, 4)
    text(draw, (1885, 300), "Salida", 20, MUTED, anchor="mm")
    text(draw, (1885, 342), "3,3 V", 36, GREEN, True, "mm")
    draw.line((1680, 320, 1720, 320), fill=GREEN, width=8)

    # Vista del encapsulado
    rr(draw, (40, 640, 760, 1040), 16, WHITE, (120, 144, 156), 3)
    text(draw, (70, 664), "Patas del AMS1117, SOT-223", 22, INK, True)
    text(draw, (70, 700), "Texto de frente. Patas hacia abajo.", 18, MUTED)
    px, py = 230, 760
    draw.rectangle((px, py, px + 300, py + 70), fill=(176, 190, 197), outline=BLACK, width=3)
    text(draw, (px + 150, py + 35), "aleta = 3,3 V", 18, INK, True, "mm")
    rr(draw, (px + 20, py + 70, px + 280, py + 150), 6, (255, 248, 225), BLACK, 3)
    text(draw, (px + 150, py + 110), "AMS1117-3.3", 20, (191, 54, 12), True, "mm")
    for i, (num, name, color) in enumerate((("1", "GND", BLACK), ("2", "3,3 V", GREEN), ("3", "5 V", RED))):
        cx = px + 70 + i * 80
        draw.rectangle((cx - 14, py + 150, cx + 14, py + 200), fill=color)
        text(draw, (cx, py + 218), num, 20, color, True, "mt")
        text(draw, (cx, py + 246), name, 16, color, True, "mt")

    # Notas
    rr(draw, (800, 640, 2050, 1460), 16, WHITE, GREEN_DK, 4)
    text(draw, (830, 668), "Para no quemarlo", 26, GREEN_DK, True)
    notes = [
        "La entrada tiene que ser de unos 5 V. Por debajo de 4,5 V la salida se cae.",
        "No pongas un diodo en serie con la entrada: se come el margen del regulador.",
        "El positivo del electrolítico va al cable de color. La raya del cuerpo va a GND.",
        "La aleta es salida. No la apoyes en GND ni en los 5 V.",
        "De aquí salen los 3,3 V de los pulsadores. La bobina del relé no: esa sigue a 5 V.",
        "Blue Pill ya por USB: no conectes esta fuente a su pin 3.3.",
        "Blue Pill sin USB y sin 5 V: esta salida sí entra por el pin marcado 3.3.",
        "En los dos casos, la masa de esta fuente y la masa de la placa son el mismo cable.",
    ]
    y = 730
    for i, line in enumerate(notes, start=1):
        draw.ellipse((830, y, 868, y + 38), fill=GREEN)
        text(draw, (849, y + 19), str(i), 18, WHITE, True, "mm")
        text(draw, (886, y + 19), line, 20, INK, anchor="lm")
        y += 86

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "07-fuente-3v3.png"
    img.save(path, "PNG", optimize=True)
    print(path, img.size)


if __name__ == "__main__":
    build()
