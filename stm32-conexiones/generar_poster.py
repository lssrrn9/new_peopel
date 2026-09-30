#!/usr/bin/env python3
"""Póster de pulsadores y relés para Nucleo-64 y Blue Pill.

Nucleo, conector Arduino: D2=PA10, D4=PB5, D7=PA8, D8=PA9.
Blue Pill, pin del encapsulado LQFP48: 10=PA0, 11=PA1, 12=PA2, 13=PA3.
En la placa esos pines están serigrafiados A0, A1, A2 y A3.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figuras"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

INK = (28, 36, 48)
MUTED = (70, 84, 102)
WHITE = (255, 255, 255)
BLUE = (21, 101, 192)
BLUE_DK = (13, 71, 161)
GREEN = (46, 125, 50)
GREEN_DK = (27, 94, 32)
ORANGE = (230, 81, 0)
BROWN = (109, 76, 19)
RED = (183, 28, 28)
BLACK = (33, 33, 33)
GOLD = (255, 193, 7)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(SANS_B if bold else SANS, size)


def text(draw, xy, msg, size, fill=INK, bold=False, anchor="lt"):
    draw.text(xy, msg, font=font(size, bold), fill=fill, anchor=anchor)


def rr(draw, box, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wire(draw, pts, color, width=8):
    if len(pts) < 2:
        return
    draw.line(pts, fill=WHITE, width=width + 8, joint="curve")
    draw.line(pts, fill=color, width=width, joint="curve")
    for x, y in (pts[0], pts[-1]):
        r = width // 2 + 2
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color, outline=WHITE, width=2)


def gnd(draw, x, y):
    draw.line((x, y, x, y + 14), fill=BLACK, width=3)
    draw.line((x - 18, y + 14, x + 18, y + 14), fill=BLACK, width=3)
    draw.line((x - 11, y + 22, x + 11, y + 22), fill=BLACK, width=3)
    draw.line((x - 5, y + 30, x + 5, y + 30), fill=BLACK, width=3)


def resistor_v(draw, x, y1, y2):
    draw.line((x, y1, x, y1 + 14), fill=BLACK, width=3)
    draw.line((x, y2 - 14, x, y2), fill=BLACK, width=3)
    top, bot = y1 + 14, y2 - 14
    pts = []
    for i in range(8):
        yy = top + (bot - top) * i / 7
        pts.append((x + (11 if i % 2 else -11), yy))
    draw.line(pts, fill=BLACK, width=3)


def resistor_h(draw, x1, x2, y):
    draw.line((x1, y, x1 + 14, y), fill=BLACK, width=3)
    draw.line((x2 - 14, y, x2, y), fill=BLACK, width=3)
    left, right = x1 + 14, x2 - 14
    pts = []
    for i in range(8):
        xx = left + (right - left) * i / 7
        pts.append((xx, y + (9 if i % 2 else -9)))
    draw.line(pts, fill=BLACK, width=3)


def npn(draw, x, y):
    draw.ellipse((x - 26, y - 26, x + 26, y + 26), outline=BLACK, width=3, fill=WHITE)
    draw.line((x - 16, y - 14, x - 16, y + 14), fill=BLACK, width=4)
    draw.line((x - 16, y - 6, x + 8, y - 20), fill=BLACK, width=3)
    draw.line((x - 16, y + 6, x + 8, y + 20), fill=BLACK, width=3)
    draw.polygon([(x, y + 10), (x + 12, y + 18), (x + 12, y + 6)], fill=BLACK)
    text(draw, (x + 32, y - 30), "C", 18, INK, True)
    text(draw, (x - 44, y - 12), "B", 18, INK, True)
    text(draw, (x + 32, y + 12), "E", 18, INK, True)
    return (x - 42, y), (x, y - 46), (x, y + 46)


def diode(draw, x, y_top, y_bot):
    mid = (y_top + y_bot) // 2
    draw.line((x, y_top, x, mid - 14), fill=BLACK, width=3)
    draw.line((x, mid + 18, x, y_bot), fill=BLACK, width=3)
    draw.polygon([(x - 13, mid + 14), (x + 13, mid + 14), (x, mid - 12)], outline=BLACK, fill=WHITE)
    draw.line((x - 15, mid - 16, x + 15, mid - 16), fill=BLACK, width=4)


def pin_mark(draw, x, y, color):
    draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill=color, outline=WHITE, width=3)


def board_shell(draw, x, y, w, h, fill, outline, usb_fill, title, subtitle, title_fill):
    rr(draw, (x + 8, y + 10, x + w + 8, y + h + 10), 22, (180, 190, 200), None, 1)
    rr(draw, (x, y, x + w, y + h), 22, fill, outline, 4)
    draw.rounded_rectangle((x + w // 2 - 46, y + 16, x + w // 2 + 46, y + 48), radius=6, fill=usb_fill)
    text(draw, (x + w // 2, y + 32), "USB", 16, WHITE if usb_fill[0] < 80 else BLUE_DK, True, "mm")
    text(draw, (x + w // 2, y + h - 58), title, 26, title_fill, True, "mm")
    text(draw, (x + w // 2, y + h - 28), subtitle, 16, title_fill, anchor="mm")


def nucleo(draw, x, y):
    w, h = 340, 680
    board_shell(draw, x, y, w, h, WHITE, (100, 120, 140), (55, 71, 79), "NUCLEO", "conectores Arduino", BLUE_DK)
    rr(draw, (x + 105, y + 200, x + 235, y + 320), 8, (38, 50, 56), None, 1)
    text(draw, (x + 170, y + 260), "STM32", 24, WHITE, True, "mm")
    pins = {
        "D2": (x, y + 150),
        "D4": (x, y + 500),
        "D7": (x + w, y + 150),
        "D8": (x + w, y + 500),
    }
    labels = {
        "D2": ("D2   PA10", BLUE, "rm"),
        "D4": ("D4   PB5", BLUE, "rm"),
        "D7": ("D7   PA8", ORANGE, "lm"),
        "D8": ("D8   PA9", BROWN, "lm"),
    }
    for key, (px, py) in pins.items():
        pin_mark(draw, px, py, labels[key][1])
        if labels[key][2] == "rm":
            text(draw, (px - 18, py - 28), labels[key][0], 20, labels[key][1], True, "rm")
    return pins


def bluepill(draw, x, y):
    w, h = 340, 680
    board_shell(draw, x, y, w, h, (21, 101, 192), (8, 40, 90), (176, 190, 197), "Blue Pill", "serigrafía A0 A1 A2 A3", WHITE)
    text(draw, (x + w // 2, y + 32), "USB", 16, BLUE_DK, True, "mm")
    rr(draw, (x + 110, y + 210, x + 230, y + 330), 6, (16, 20, 24), None, 1)
    text(draw, (x + 170, y + 258), "F103C8", 22, WHITE, True, "mm")
    draw.ellipse((x + w - 70, y + 78, x + w - 44, y + 104), fill=RED, outline=WHITE, width=2)
    text(draw, (x + w // 2, y + 92), "PC13 LED", 16, WHITE, True, "mm")
    pins = {
        "10": (x, y + 150),
        "11": (x, y + 500),
        "12": (x + w, y + 150),
        "13": (x + w, y + 500),
    }
    left = {"10": "A0   PA0", "11": "A1   PA1"}
    right = {"12": "A2   PA2", "13": "A3   PA3"}
    for key, label in left.items():
        px, py = pins[key]
        pin_mark(draw, px, py, BLUE)
        text(draw, (px - 18, py - 28), label, 20, BLUE_DK, True, "rm")
    for key, label in right.items():
        px, py = pins[key]
        color = ORANGE if key == "12" else BROWN
        pin_mark(draw, px, py, color)
    return pins


def input_block(draw, pin, title, detail):
    x, y = pin
    nx = x - 250
    text(draw, (nx, y - 150), title, 22, BLUE_DK, True, "mm")
    text(draw, (nx, y - 122), detail, 16, MUTED, anchor="mm")
    text(draw, (nx + 36, y - 96), "+3,3 V de la placa", 18, GREEN, True, "lm")
    draw.line((nx, y - 78, nx, y - 36), fill=GREEN, width=6)
    draw.ellipse((nx - 7, y - 86, nx + 7, y - 72), fill=GREEN, outline=WHITE, width=2)
    draw.ellipse((nx - 24, y - 34, nx + 24, y + 14), outline=BLACK, width=3, fill=WHITE)
    draw.arc((nx - 14, y - 24, nx + 14, y + 4), 200, 340, fill=BLACK, width=3)
    draw.line((nx, y + 14, nx, y), fill=BLACK, width=3)
    wire(draw, [(nx, y), pin], BLUE, 8)
    resistor_v(draw, nx, y + 8, y + 78)
    text(draw, (nx + 20, y + 36), "10 kΩ a GND", 18, INK, True, "lm")
    gnd(draw, nx, y + 78)


def relay_block(draw, pin, title, pin_label, color):
    px, py = pin
    x = px + 90
    text(draw, (px + 22, py - 72), title, 22, color, True)
    text(draw, (px + 22, py - 46), pin_label, 18, color, True)
    cx = x + 250
    base, collector, emitter = npn(draw, cx, py + 8)
    resistor_h(draw, x + 8, base[0], py)
    text(draw, ((x + 8 + base[0]) // 2, py - 16), "1 kΩ", 16, INK, True, "mb")
    wire(draw, [pin, (x, py)], color, 8)
    draw.line((collector[0], collector[1], cx, py - 74), fill=BLACK, width=3)
    rr(draw, (cx - 100, py - 116, cx + 100, py - 74), 8, (255, 243, 224), color, 2)
    text(draw, (cx, py - 95), "Bobina 5 V", 18, color, True, "mm")
    draw.line((cx, py - 116, cx, py - 138), fill=RED, width=5)
    text(draw, (cx - 12, py - 152), "+5 V", 18, RED, True, "rm")
    diode(draw, cx + 150, py - 138, py - 74)
    draw.line((cx + 70, py - 95, cx + 150, py - 95), fill=BLACK, width=2)
    draw.line((cx, py - 138, cx + 150, py - 138), fill=RED, width=3)
    text(draw, (cx + 168, py - 132), "1N4007", 17, INK, True, "lm")
    text(draw, (cx + 168, py - 110), "banda hacia +5 V", 15, MUTED, anchor="lm")
    gnd(draw, emitter[0], emitter[1] + 4)
    text(draw, (emitter[0] + 28, emitter[1] + 8), "GND común", 16, INK, True, "lm")


def contact_card(draw, x, y, w, h):
    rr(draw, (x, y, x + w, y + h), 18, WHITE, (106, 27, 154), 4)
    text(draw, (x + 28, y + 24), "Contacto del relé", 28, (74, 20, 140), True)
    text(draw, (x + 28, y + 66), "La lámpara o el motor se conectan al contacto, no al pin.", 18, MUTED)
    bx, by = x + 40, y + 130
    rr(draw, (bx, by, bx + 180, by + 100), 10, BLUE, None, 1)
    text(draw, (bx + 90, by + 36), "Relé", 22, WHITE, True, "mm")
    text(draw, (bx + 90, by + 68), "NC    COM    NO", 15, (227, 242, 253), anchor="mm")
    text(draw, (bx + 90, by + 120), "Bornes", 16, MUTED, anchor="mt")

    sx, sy = x + 280, y + 150
    text(draw, (sx, y + 120), "Por dentro", 18, INK, True)
    draw.ellipse((sx + 10, sy + 36, sx + 26, sy + 52), outline=BLACK, width=3)
    text(draw, (sx - 8, sy + 44), "COM", 16, INK, True, "rm")
    draw.line((sx + 18, sy + 36, sx + 90, sy + 8), fill=BLACK, width=3)
    draw.ellipse((sx + 82, sy, sx + 98, sy + 16), outline=BLACK, width=3)
    text(draw, (sx + 106, sy - 4), "NO", 16, INK, True, "lm")
    draw.ellipse((sx + 10, sy + 78, sx + 26, sy + 94), outline=BLACK, width=3)
    text(draw, (sx + 34, sy + 78), "NC, sin usar en este ejemplo", 16, MUTED, anchor="lm")

    lx = x + 640
    text(draw, (lx, y + 120), "Carga entre COM y NO", 18, INK, True)
    text(draw, (lx, y + 168), "L", 18, RED, True, "mm")
    draw.line((lx + 16, y + 168, lx + 70, y + 168), fill=RED, width=6)
    rr(draw, (lx + 70, y + 146, lx + 250, y + 192), 8, (255, 243, 224), ORANGE, 3)
    text(draw, (lx + 160, y + 169), "Lámpara o motor", 16, ORANGE, True, "mm")
    draw.line((lx + 250, y + 168, lx + 310, y + 168), fill=BLACK, width=4)
    draw.line((lx + 310, y + 150, lx + 360, y + 124), fill=BLACK, width=3)
    text(draw, (lx + 292, y + 196), "COM", 15, INK, True)
    text(draw, (lx + 366, y + 112), "NO", 15, INK, True)
    draw.line((lx + 360, y + 168, lx + 430, y + 168), fill=BLACK, width=4)
    text(draw, (lx + 444, y + 168), "N", 18, BLACK, True, "lm")
    text(draw, (lx, y + 230), "Esa fuente puede ser de 5 V, 12 V o 24 V.", 17, MUTED)
    text(draw, (lx, y + 258), "No la lleves a un pin del STM32.", 17, RED, True)


def notes_card(draw, x, y, w, h):
    rr(draw, (x, y, x + w, y + h), 18, (255, 251, 254), (194, 24, 91), 4)
    text(draw, (x + 28, y + 24), "Notas", 28, (136, 14, 79), True)
    items = [
        "Pulsador a +3,3 V de la placa, y 10 kΩ desde el pin hasta GND.",
        "El pin de salida solo llega a la base del transistor, a través de 1 kΩ.",
        "La bobina del relé se alimenta con 5 V de otra fuente.",
        "La masa de esa fuente va unida a la masa del STM32.",
        "El 1N4007 va en paralelo con la bobina. La banda mira hacia +5 V.",
        "En la Blue Pill, PC13 es el LED. Los relés van en A2 y A3.",
        "C, B y E son del símbolo. El orden de patas cambia según el transistor.",
    ]
    yy = y + 84
    for i, line in enumerate(items, start=1):
        draw.ellipse((x + 28, yy, x + 60, yy + 32), fill=BLUE)
        text(draw, (x + 44, yy + 16), str(i), 16, WHITE, True, "mm")
        text(draw, (x + 76, yy + 16), line, 18, INK, anchor="lm")
        yy += 46


def legend_card(draw, x, y, w, h):
    rr(draw, (x, y, x + w, y + h), 18, WHITE, BLUE, 4)
    text(draw, (x + 28, y + 24), "Colores", 28, BLUE_DK, True)
    rows = [
        (BLUE, "Entrada, del pulsador al pin"),
        (ORANGE, "Salida del relé A o del relé C"),
        (BROWN, "Salida del relé B o del relé D"),
        (GREEN, "3,3 V de la placa"),
        (RED, "+5 V externo de la bobina"),
        (BLACK, "GND, masa común"),
    ]
    yy = y + 90
    for color, label in rows:
        rr(draw, (x + 28, yy, x + 92, yy + 28), 6, color, None, 1)
        text(draw, (x + 110, yy + 14), label, 18, INK, anchor="lm")
        yy += 52


def build():
    w, h = 3400, 1860
    img = Image.new("RGB", (w, h), (244, 247, 251))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w // 2, 110), fill=BLUE_DK)
    draw.rectangle((w // 2, 0, w, 110), fill=GREEN_DK)
    text(draw, (36, 22), "A y B  —  Nucleo", 36, WHITE, True)
    text(draw, (36, 70), "Entradas D2 (PA10) y D4 (PB5).   Salidas D7 (PA8) y D8 (PA9).", 20, (187, 222, 251))
    text(draw, (w // 2 + 36, 22), "C y D  —  Blue Pill F103", 36, WHITE, True)
    text(draw, (w // 2 + 36, 70), "Entradas A0 (PA0) y A1 (PA1).   Salidas A2 (PA2) y A3 (PA3).", 20, (200, 230, 201))
    draw.rectangle((0, 110, w // 2, 1320), fill=(227, 242, 253))
    draw.rectangle((w // 2, 110, w, 1320), fill=(232, 245, 233))

    n = nucleo(draw, 430, 200)
    input_block(draw, n["D2"], "Pulsador A", "entrada")
    input_block(draw, n["D4"], "Pulsador B", "entrada")
    relay_block(draw, n["D7"], "Relé A", "D7 (PA8)", ORANGE)
    relay_block(draw, n["D8"], "Relé B", "D8 (PA9)", BROWN)

    b = bluepill(draw, w // 2 + 500, 200)
    input_block(draw, b["10"], "Pulsador C", "entrada")
    input_block(draw, b["11"], "Pulsador D", "entrada")
    relay_block(draw, b["12"], "Relé C", "A2 (PA2)", ORANGE)
    relay_block(draw, b["13"], "Relé D", "A3 (PA3)", BROWN)

    contact_card(draw, 24, 1350, 1500, 480)
    notes_card(draw, 1548, 1350, 1180, 480)
    legend_card(draw, 2752, 1350, 624, 480)

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "00-pulsadores-reles.png"
    img.save(path, "PNG", optimize=True)
    print(path, img.size)


if __name__ == "__main__":
    build()
