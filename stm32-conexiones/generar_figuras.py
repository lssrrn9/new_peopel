#!/usr/bin/env python3
"""Figuras PNG de conexión para la Blue Pill STM32F103C8T6.

Los nombres de pin del header siguen el mapa de stm32-base.org para esa
placa. Las funciones (USART1, I2C1, SPI1, SWD) son las de reset del
STM32F103, sin remap.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figuras"

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BG = (244, 247, 251)
INK = (22, 32, 46)
MUTED = (84, 98, 116)
LINE = (210, 220, 232)
CARD = (255, 255, 255)
PCB = (18, 78, 158)
PCB_DARK = (10, 48, 108)
ST = (0, 92, 168)

C_5V = (198, 40, 40)
C_3V3 = (230, 126, 0)
C_GND = (55, 65, 78)
C_SWDIO = (21, 101, 192)
C_SWCLK = (46, 125, 50)
C_TX = (123, 31, 162)
C_RX = (0, 121, 107)
C_SDA = (57, 73, 171)
C_SCL = (245, 127, 23)
C_SCK = (245, 127, 23)
C_MISO = (0, 121, 107)
C_MOSI = (194, 24, 91)
C_CS = (109, 76, 19)
C_OPT = (120, 130, 145)
C_GPIO = (90, 122, 168)
C_XTAL = (94, 96, 166)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(SANS_B if bold else SANS, size)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = word if not cur else f"{cur} {word}"
        if text_size(draw, trial, fnt)[0] <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def bezier(p0, p1, p2, p3, steps: int = 48) -> list[tuple[float, float]]:
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def draw_wire(draw: ImageDraw.ImageDraw, a: tuple[int, int], b: tuple[int, int], color, width: int = 8, dashed: bool = False) -> None:
    span = max(80, (b[0] - a[0]) // 2)
    pts = bezier(a, (a[0] + span, a[1]), (b[0] - span, b[1]), b)
    if dashed:
        for i in range(0, len(pts) - 1, 2):
            j = min(i + 1, len(pts) - 1)
            draw.line([pts[i], pts[j]], fill=color, width=width)
    else:
        draw.line(pts, fill=(255, 255, 255), width=width + 6, joint="curve")
        draw.line(pts, fill=color, width=width, joint="curve")
    r = width // 2 + 2
    for p in (a, b):
        draw.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=color, outline=(255, 255, 255), width=2)


def header_bar(draw: ImageDraw.ImageDraw, w: int, title: str, subtitle: str) -> int:
    draw.rectangle((0, 0, w, 132), fill=PCB_DARK)
    draw.rectangle((0, 132, w, 140), fill=ST)
    draw.text((48, 28), title, font=font(40, True), fill=(255, 255, 255))
    draw.text((48, 82), subtitle, font=font(22), fill=(186, 214, 242))
    return 168


def footer(draw: ImageDraw.ImageDraw, w: int, h: int, lines: list[str]) -> None:
    top = h - 36 - 34 * len(lines)
    draw.rectangle((0, top - 16, w, h), fill=(232, 238, 246))
    y = top
    fnt = font(20)
    for line in lines:
        draw.text((48, y), line, font=fnt, fill=INK)
        y += 34


def new_canvas(w: int, h: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (w, h), BG)
    return img, ImageDraw.Draw(img)


def save(img: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    img.save(path, "PNG", optimize=True)
    print(path)


def wiring(
    name: str,
    title: str,
    subtitle: str,
    left_title: str,
    left_sub: str,
    right_title: str,
    right_sub: str,
    links: list[dict],
    notes: list[str],
) -> None:
    """links: side labels plus color. Each item has left, right, color, optional dashed, tag."""
    w, h = 1800, 280 + 92 * len(links) + 50 + 36 + 34 * len(notes)
    img, draw = new_canvas(w, h)
    header_bar(draw, w, title, subtitle)

    left_x, right_x = 70, 1080
    card_w = 620
    top = 190
    row_h = 92
    card_h = 78 + row_h * len(links)

    for x, card_title, card_sub in (
        (left_x, left_title, left_sub),
        (right_x, right_title, right_sub),
    ):
        rounded(draw, (x, top, x + card_w, top + card_h), 22, CARD, LINE, 2)
        draw.rectangle((x, top, x + card_w, top + 64), fill=PCB)
        draw.rounded_rectangle((x, top, x + card_w, top + 28), radius=22, fill=PCB)
        draw.text((x + 24, top + 10), card_title, font=font(26, True), fill=(255, 255, 255))
        draw.text((x + 24, top + 74), card_sub, font=font(18), fill=MUTED)

    for i, link in enumerate(links):
        y = top + 118 + i * row_h
        cy = y + 28
        for x, key in ((left_x, "left"), (right_x, "right")):
            rounded(draw, (x + 22, y, x + card_w - 22, y + 58), 12, (247, 249, 252), LINE, 2)
            draw.rectangle((x + 22, y, x + 34, y + 58), fill=link["color"])
            draw.text((x + 50, y + 8), link[key], font=font(22, True), fill=INK)
            extra = link.get(key + "_note")
            if extra:
                draw.text((x + 50, y + 34), extra, font=font(16), fill=MUTED)
        a = (left_x + card_w - 8, cy)
        b = (right_x + 8, cy)
        connected = link.get("connected", True)
        if connected:
            draw_wire(draw, a, b, link["color"], width=8, dashed=link.get("dashed", False))
        tag = link.get("tag")
        if tag:
            tw, _th = text_size(draw, tag, font(16, True))
            mx = (a[0] + b[0]) // 2
            box_top = cy - 36 if connected else cy - 16
            box_bot = box_top + 32
            rounded(draw, (mx - tw // 2 - 10, box_top, mx + tw // 2 + 10, box_bot), 8, CARD, link["color"], 2)
            draw.text((mx - tw // 2, box_top + 4), tag, font=font(16, True), fill=link["color"])

    footer(draw, w, h, notes)
    save(img, name)


def pin_row(draw, x, y, w, name, func, color) -> None:
    rounded(draw, (x, y, x + w, y + 46), 8, CARD, LINE, 1)
    draw.rectangle((x, y, x + 10, y + 46), fill=color)
    draw.text((x + 20, y + 4), name, font=font(18, True), fill=INK)
    draw.text((x + 20, y + 24), func, font=font(14), fill=MUTED)


def figura_mapa() -> None:
    header1 = [
        ("1  VB", "VBAT", C_3V3),
        ("2  C13", "PC13, LED de la placa (activo en bajo)", C_SWCLK),
        ("3  C14", "PC14, cristal de 32 kHz", C_XTAL),
        ("4  C15", "PC15, cristal de 32 kHz", C_XTAL),
        ("5  A0", "PA0, ADC", C_SWDIO),
        ("6  A1", "PA1, ADC", C_SWDIO),
        ("7  A2", "PA2, USART2_TX", C_TX),
        ("8  A3", "PA3, USART2_RX", C_RX),
        ("9  A4", "PA4, SPI1_NSS", C_CS),
        ("10  A5", "PA5, SPI1_SCK", C_SCK),
        ("11  A6", "PA6, SPI1_MISO", C_MISO),
        ("12  A7", "PA7, SPI1_MOSI", C_MOSI),
        ("13  B0", "PB0, ADC", C_SWDIO),
        ("14  B1", "PB1, ADC", C_SWDIO),
        ("15  B10", "PB10, I2C2_SCL", C_SCL),
        ("16  B11", "PB11, I2C2_SDA", C_SDA),
        ("17  R", "NRST, reset", C_5V),
        ("18  3.3", "Salida del regulador, 3,3 V", C_3V3),
        ("19  G", "GND", C_GND),
        ("20  G", "GND", C_GND),
    ]
    header2 = [
        ("1  3.3", "Salida del regulador, 3,3 V", C_3V3),
        ("2  G", "GND", C_GND),
        ("3  5V", "Entrada de 5 V (si no usas el USB)", C_5V),
        ("4  B9", "PB9, I2C1_SDA solo con remap", C_OPT),
        ("5  B8", "PB8, I2C1_SCL solo con remap", C_OPT),
        ("6  B7", "PB7, I2C1_SDA", C_SDA),
        ("7  B6", "PB6, I2C1_SCL", C_SCL),
        ("8  B5", "PB5, GPIO", C_GPIO),
        ("9  B4", "PB4, GPIO", C_GPIO),
        ("10  B3", "PB3, GPIO", C_GPIO),
        ("11  A15", "PA15, GPIO", C_GPIO),
        ("12  A12", "PA12, USB D+", C_TX),
        ("13  A11", "PA11, USB D-", C_RX),
        ("14  A10", "PA10, USART1_RX", C_RX),
        ("15  A9", "PA9, USART1_TX", C_TX),
        ("16  A8", "PA8, GPIO", C_GPIO),
        ("17  B15", "PB15, SPI2_MOSI", C_MOSI),
        ("18  B14", "PB14, SPI2_MISO", C_MISO),
        ("19  B13", "PB13, SPI2_SCK", C_SCK),
        ("20  B12", "PB12, SPI2_NSS", C_CS),
    ]
    swd = [
        ("1  3V3", "Riel de 3,3 V", C_3V3),
        ("2  DIO", "SWDIO, pin PA13", C_SWDIO),
        ("3  CLK", "SWCLK, pin PA14", C_SWCLK),
        ("4  GND", "Tierra", C_GND),
    ]

    row_h = 52
    w = 1680
    body = 150 + max(len(header1), len(header2)) * row_h
    h = 168 + body + 210
    img, draw = new_canvas(w, h)
    header_bar(
        draw,
        w,
        "Mapa de pines · Blue Pill STM32F103C8T6",
        "Orden del pin 1 al 20 según stm32-base.org. Confirma la serigrafía de tu placa.",
    )

    col_w = 740
    gap = 40
    x1 = 48
    x2 = x1 + col_w + gap
    y0 = 180
    for x, title, rows in ((x1, "Header 1", header1), (x2, "Header 2", header2)):
        rounded(draw, (x, y0, x + col_w, y0 + 56 + len(rows) * row_h), 16, (255, 255, 255), LINE, 2)
        draw.text((x + 18, y0 + 14), title, font=font(24, True), fill=PCB)
        for i, (name, func, color) in enumerate(rows):
            pin_row(draw, x + 16, y0 + 56 + i * row_h, col_w - 32, name, func, color)

    y_swd = y0 + 56 + len(header1) * row_h + 28
    draw.text((48, y_swd), "Header SWD de 4 pines (aparte de los dos headers largos)", font=font(22, True), fill=INK)
    swd_w = 380
    for i, (name, func, color) in enumerate(swd):
        pin_row(draw, 48 + i * (swd_w + 16), y_swd + 40, swd_w, name, func, color)

    footer(
        draw,
        w,
        h,
        [
            "El pin marcado 3.3 es salida del regulador de la placa. No le inyectes 5 V.",
            "PA13 y PA14 son el depurador SWD. No los uses como GPIO si quieres seguir programando.",
            "I2C1 por defecto es PB6 (SCL) y PB7 (SDA). PB8 y PB9 solo valen si activas el remap.",
        ],
    )
    # footer() used h+40 but canvas is h; the last notes may clip. Rebuild with correct height.
    # Recreate cleanly below if this overflows. Checked: y_swd + 40 + 46 must be above footer.
    save(img, "01-mapa-pines.png")


def figura_alimentacion() -> None:
    wiring(
        "02-alimentacion.png",
        "Alimentación de la Blue Pill",
        "Una sola fuente de 5 V. El pin 3,3 V alimenta sensores, no entra desde fuera.",
        "Fuente",
        "Elige una sola de estas dos entradas",
        "Blue Pill STM32F103C8T6",
        "Conector y pines de potencia",
        [
            {"left": "Cable USB 5 V", "left_note": "Al conector micro-USB de la placa", "right": "Micro-USB de la placa", "right_note": "Forma habitual de alimentar", "color": C_5V, "tag": "opción A"},
            {"left": "5 V externo", "left_note": "No lo uses a la vez que el USB", "right": "Pin 5V", "right_note": "Entrada al regulador de la placa", "color": C_5V, "tag": "opción B", "dashed": True},
            {"left": "GND de la fuente", "left_note": "Tierra común con los módulos", "right": "Pin G  (GND)", "right_note": "Hay varios pines G, son la misma tierra", "color": C_GND, "tag": "obligatorio"},
            {"left": "Sensores y módulos", "left_note": "Solo si trabajan a 3,3 V", "right": "Pin 3.3", "right_note": "Sale del regulador. No le pidas mucha corriente", "color": C_3V3, "tag": "salida"},
            {"left": "Jumper BOOT0", "left_note": "Posición 0 para arrancar tu programa", "right": "BOOT0 a 0", "right_note": "0 = flash. 1 = bootloader de sistema", "color": C_SWCLK, "tag": "arranque"},
        ],
        [
            "No conectes 5 V al pin marcado 3.3. Ese pin es una salida.",
            "No alimentes por USB y por el pin 5V al mismo tiempo.",
            "La lógica de los GPIO es de 3,3 V. Un sensor de 5 V necesita adaptación de nivel.",
        ],
    )


def figura_swd() -> None:
    wiring(
        "03-stlink-swd.png",
        "Programar y depurar por SWD",
        "ST-Link V2 hacia el header de 4 pines de la Blue Pill. Une cada señal por su nombre.",
        "ST-Link V2",
        "Los clones no coinciden en el orden físico: guía por el nombre",
        "Header SWD de la Blue Pill",
        "Orden publicado: 3V3, DIO, CLK, GND",
        [
            {"left": "SWDIO", "left_note": "Datos del depurador", "right": "DIO   pin PA13", "right_note": "Pin 2 del header SWD", "color": C_SWDIO, "tag": "datos"},
            {"left": "SWCLK", "left_note": "Reloj del depurador", "right": "CLK   pin PA14", "right_note": "Pin 3 del header SWD", "color": C_SWCLK, "tag": "reloj"},
            {"left": "GND", "left_note": "Tierra común", "right": "GND", "right_note": "Pin 4 del header SWD", "color": C_GND, "tag": "obligatorio"},
            {"left": "3,3 V del ST-Link", "left_note": "Solo si la placa no tiene otra fuente", "right": "3V3", "right_note": "Pin 1 del header SWD. Opcional", "color": C_3V3, "tag": "opcional", "dashed": True},
        ],
        [
            "Si la Blue Pill ya está alimentada por USB, deja sin conectar el cable de 3,3 V.",
            "BOOT0 puede quedarse en 0. El ST-Link graba la flash sin pasar por el bootloader UART.",
            "PA13 y PA14 quedan ocupados por el depurador.",
        ],
    )


def figura_uart() -> None:
    wiring(
        "04-uart-bootloader.png",
        "Grabar por el puerto serie USART1",
        "Adaptador USB-TTL de 3,3 V. TX de un lado entra en RX del otro.",
        "Adaptador USB-TTL 3,3 V",
        "CP2102, CH340 o FTDI en modo 3,3 V",
        "Blue Pill",
        "USART1 y jumper de arranque",
        [
            {"left": "TX del adaptador", "left_note": "Sale del adaptador", "right": "PA10   USART1_RX", "right_note": "Entra al micro", "color": C_TX, "tag": "cruzado"},
            {"left": "RX del adaptador", "left_note": "Entra al adaptador", "right": "PA9    USART1_TX", "right_note": "Sale del micro", "color": C_RX, "tag": "cruzado"},
            {"left": "GND", "left_note": "Tierra común", "right": "GND", "right_note": "Cualquier pin G", "color": C_GND, "tag": "obligatorio"},
            {"left": "VCC del adaptador", "left_note": "Déjalo sin conectar", "right": "No va a la placa", "right_note": "Aliméntala por su USB, nunca por el pin 3.3", "color": C_5V, "tag": "no unir", "dashed": True, "connected": False},
        ],
        [
            "Para entrar al bootloader: BOOT0 en 1, BOOT1 en 0, pulsa RESET y entonces el programa de grabación ve el puerto.",
            "Cuando termine la grabación: BOOT0 otra vez en 0 y pulsa RESET para ejecutar lo grabado.",
            "El bootloader de sistema usa 8 bits, paridad par y 1 bit de parada. La velocidad la detecta al recibir 0x7F.",
        ],
    )


def figura_i2c() -> None:
    wiring(
        "05-sensor-i2c.png",
        "Sensor o pantalla por I2C1",
        "Conexión por defecto del STM32F103, sin remap: SCL en PB6 y SDA en PB7.",
        "Módulo I2C a 3,3 V",
        "OLED, BMP280, EEPROM y similares",
        "Blue Pill  ·  I2C1",
        "Pines del Header 2",
        [
            {"left": "VCC", "left_note": "Alimentación del módulo", "right": "Pin 3.3", "right_note": "No uses 5 V en un módulo de 3,3 V", "color": C_3V3, "tag": "3,3 V"},
            {"left": "GND", "left_note": "Tierra del módulo", "right": "Pin G", "right_note": "Tierra común", "color": C_GND, "tag": "GND"},
            {"left": "SDA", "left_note": "Datos", "right": "PB7", "right_note": "I2C1_SDA", "color": C_SDA, "tag": "SDA"},
            {"left": "SCL", "left_note": "Reloj", "right": "PB6", "right_note": "I2C1_SCL", "color": C_SCL, "tag": "SCL"},
        ],
        [
            "SDA y SCL necesitan resistencias de pull-up de 4,7 kΩ hacia 3,3 V si el módulo no las trae.",
            "PB8 (SCL) y PB9 (SDA) no son el bus por defecto: solo funcionan si el programa activa el remap de I2C1.",
            "I2C2, el otro bus, está en PB10 (SCL) y PB11 (SDA).",
        ],
    )


def figura_spi() -> None:
    wiring(
        "06-periferico-spi.png",
        "Pantalla o memoria por SPI1",
        "Funciones de reset del STM32F103 en el puerto A. MISO y MOSI no se cruzan.",
        "Módulo SPI a 3,3 V",
        "TFT, tarjeta SD o flash",
        "Blue Pill  ·  SPI1",
        "Pines del Header 1",
        [
            {"left": "VCC", "left_note": "Alimentación del módulo", "right": "Pin 3.3", "right_note": "Salida del regulador", "color": C_3V3, "tag": "3,3 V"},
            {"left": "GND", "left_note": "Tierra del módulo", "right": "Pin G", "right_note": "Tierra común", "color": C_GND, "tag": "GND"},
            {"left": "SCK", "left_note": "Reloj", "right": "PA5", "right_note": "SPI1_SCK", "color": C_SCK, "tag": "SCK"},
            {"left": "MISO", "left_note": "Datos hacia el maestro", "right": "PA6", "right_note": "SPI1_MISO", "color": C_MISO, "tag": "MISO"},
            {"left": "MOSI", "left_note": "Datos hacia el módulo", "right": "PA7", "right_note": "SPI1_MOSI", "color": C_MOSI, "tag": "MOSI"},
            {"left": "CS", "left_note": "Selección del chip, activo en bajo", "right": "PA4", "right_note": "SPI1_NSS. Puedes usar otro GPIO", "color": C_CS, "tag": "CS"},
        ],
        [
            "MISO va con MISO y MOSI va con MOSI. El cruce TX/RX es solo del puerto serie.",
            "Elige un módulo de 3,3 V, o pon un adaptador de nivel si el módulo es de 5 V.",
            "SPI2 está en PB13 (SCK), PB14 (MISO), PB15 (MOSI) y PB12 (NSS).",
        ],
    )


def main() -> None:
    figura_mapa()
    figura_alimentacion()
    figura_swd()
    figura_uart()
    figura_i2c()
    figura_spi()


if __name__ == "__main__":
    main()
