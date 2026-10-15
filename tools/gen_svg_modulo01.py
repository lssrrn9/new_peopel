#!/usr/bin/env python3
"""Diagramas SVG deterministas del Módulo 1.

Las posiciones de los componentes en la vista superior son esquemáticas
(no son un plano mecánico). Los nombres de señal, números de pin y
puentes salen de UM1724 Rev 17 (Figura 15, Tablas 14 y 26, Tabla 10)
y del esquema MB1136-DEFAULT-C05 (17-AGO-2022).
"""

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "curso" / "img"

FONT = "Liberation Sans, Segoe UI, sans-serif"


def svg_open(w, h, title):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<title>{title}</title>
<rect width="100%" height="100%" fill="#f6f3ee"/>
<style>
  text {{ font-family: {FONT}; fill: #1c1917; }}
  .h {{ font-size: 22px; font-weight: 700; }}
  .sub {{ font-size: 12px; fill: #57534e; }}
  .sm {{ font-size: 11px; }}
  .xs {{ font-size: 10px; }}
  .tiny {{ font-size: 9px; }}
  .w {{ fill: #fff; }}
  .pin {{ font-size: 9px; font-family: {FONT}; }}
</style>
'''


def svg_close():
    return "</svg>\n"


def text(x, y, s, cls="sm", anchor="start", fill=None):
    extra = f' fill="{fill}"' if fill else ""
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{extra}>{s}</text>\n'


def rect(x, y, w, h, fill, stroke="#1c1917", sw=1.2, rx=4):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
    )


def line(x1, y1, x2, y2, stroke="#44403c", sw=1.5, marker=None):
    m = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
        f'stroke-width="{sw}"{m}/>\n'
    )


def path(d, stroke="#44403c", sw=1.5, marker=None):
    m = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}"{m}/>\n'
    )


def defs_arrows():
    return """<defs>
  <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 1.2 L 9 5 L 0 8.8 z" fill="#44403c"/>
  </marker>
  <marker id="arrw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 1.2 L 9 5 L 0 8.8 z" fill="#1d4ed8"/>
  </marker>
</defs>
"""


ARDUINO = [
    # connector, pin, name, stm32, note
    ("CN6", "1", "NC", "—", "sin conexión"),
    ("CN6", "2", "IOREF", "—", "referencia 3,3 V"),
    ("CN6", "3", "RESET", "NRST", "reset del MCU"),
    ("CN6", "4", "+3.3V", "—", "entrada o salida 3,3 V"),
    ("CN6", "5", "+5V", "—", "salida 5 V"),
    ("CN6", "6", "GND", "—", "tierra"),
    ("CN6", "7", "GND", "—", "tierra"),
    ("CN6", "8", "VIN", "—", "entrada 7–12 V"),
    ("CN8", "1", "A0", "PA0", "ADC1_IN1, TTa"),
    ("CN8", "2", "A1", "PA1", "ADC1_IN2, TTa"),
    ("CN8", "3", "A2", "PA4", "ADC2_IN1 y DAC1_OUT1"),
    ("CN8", "4", "A3", "PB0", "ADC3_IN12, TTa"),
    ("CN8", "5", "A4", "PC1", "por defecto; PB9 si se cambian puentes"),
    ("CN8", "6", "A5", "PC0", "por defecto; PB8 si se cambian puentes"),
    ("CN5", "10", "D15", "PB8", "I2C1_SCL"),
    ("CN5", "9", "D14", "PB9", "I2C1_SDA"),
    ("CN5", "8", "AREF", "—", "AVDD"),
    ("CN5", "7", "GND", "—", "tierra"),
    ("CN5", "6", "D13", "PA5", "LD2, SPI1_SCK, DAC1_OUT2"),
    ("CN5", "5", "D12", "PA6", "SPI1_MISO"),
    ("CN5", "4", "D11", "PA7", "TIM17_CH1 o SPI1_MOSI"),
    ("CN5", "3", "D10", "PB6", "TIM4_CH1 o SPI1_NSS"),
    ("CN5", "2", "D9", "PC7", "TIM3_CH2"),
    ("CN5", "1", "D8", "PA9", "USART1_TX, FT"),
    ("CN9", "8", "D7", "PA8", "GPIO"),
    ("CN9", "7", "D6", "PB10", "TIM2_CH3"),
    ("CN9", "6", "D5", "PB4", "TIM3_CH1"),
    ("CN9", "5", "D4", "PB5", "GPIO"),
    ("CN9", "4", "D3", "PB3", "TIM2_CH2; también SWO"),
    ("CN9", "3", "D2", "PA10", "USART1_RX, FT"),
    ("CN9", "2", "D1", "PA2", "NO conectado de fábrica (SB62 OFF)"),
    ("CN9", "1", "D0", "PA3", "NO conectado de fábrica (SB63 OFF)"),
]

# CN7 odd/even and CN10 odd/even from Table 26
CN7 = [
    (1, "PC10", 2, "PC11"),
    (3, "PC12", 4, "PD2"),
    (5, "VDD", 6, "E5V"),
    (7, "BOOT0", 8, "GND"),
    (9, "—", 10, "—"),
    (11, "—", 12, "IOREF"),
    (13, "PA13", 14, "RESET"),
    (15, "PA14", 16, "+3.3V"),
    (17, "PA15", 18, "+5V"),
    (19, "GND", 21, "PB7"),
]
# wait I mixed. Table is pairs of odd pin name and even pin name.
# Redo properly as list of (odd_pin, odd_name, even_pin, even_name)

CN7 = [
    (1, "PC10", 2, "PC11"),
    (3, "PC12", 4, "PD2"),
    (5, "VDD", 6, "E5V"),
    (7, "BOOT0", 8, "GND"),
    (9, "—", 10, "—"),
    (11, "—", 12, "IOREF"),
    (13, "PA13 SWD", 14, "NRST"),
    (15, "PA14 SWD", 16, "+3.3V"),
    (17, "PA15", 18, "+5V"),
    (19, "GND", 20, "GND"),
    (21, "PB7", 22, "GND"),
    (23, "PC13 B1", 24, "VIN"),
    (25, "PC14 LSE", 26, "—"),
    (27, "PC15 LSE", 28, "PA0"),
    (29, "PF0 MCO", 30, "PA1"),
    (31, "PF1", 32, "PA4"),
    (33, "VBAT", 34, "PB0"),
    (35, "PC2", 36, "PC1 / PB9"),
    (37, "PC3", 38, "PC0 / PB8"),
]

CN10 = [
    (1, "PC9", 2, "PC8"),
    (3, "PB8", 4, "PC6"),
    (5, "PB9", 6, "PC5"),
    (7, "AVDD", 8, "U5V"),
    (9, "GND", 10, "—"),
    (11, "PA5 LD2", 12, "PA12"),
    (13, "PA6", 14, "PA11"),
    (15, "PA7", 16, "PB12"),
    (17, "PB6", 18, "PB11"),
    (19, "PC7", 20, "GND"),
    (21, "PA9", 22, "PB2"),
    (23, "PA8", 24, "PB1"),
    (25, "PB10", 26, "PB15"),
    (27, "PB4", 28, "PB14"),
    (29, "PB5", 30, "PB13"),
    (31, "PB3", 32, "AGND"),
    (33, "PA10", 34, "PC4"),
    (35, "PA2 abierto", 36, "—"),
    (37, "PA3 abierto", 38, "—"),
]


def entidades():
    w, h = 1100, 620
    s = svg_open(w, h, "Tres entidades: MCU, tarjeta y ST-LINK")
    s += defs_arrows()
    s += text(40, 36, "Tres piezas distintas que viajan juntas", "h")
    s += text(40, 58, "NUCLEO-F303RE no es el microcontrolador. El ST-LINK no es el programa. Los conectores no son el chip.", "sub")

    boxes = [
        (40, 90, 300, 250, "#1e3a5f", "1. Microcontrolador", "STM32F303RET6",
         ["Pastilla LQFP64 soldada en U5", "Cortex-M4F, 72 MHz", "512 KB Flash, 64+16 KB SRAM",
          "Aquí vive el programa", "Pines: PA5, PC13, PA2…"]),
        (400, 90, 300, 250, "#0f766e", "2. Tarjeta", "NUCLEO-F303RE",
         ["PCB de referencia MB1136", "Reguladores, LED, pulsadores",
          "Conectores Arduino y Morpho", "Jumpers JP1, JP5, JP6",
          "Puentes de soldadura SB"]),
        (760, 90, 300, 250, "#9a3412", "3. Depurador", "ST-LINK/V2-1",
         ["Otro MCU: STM32F103CBT6", "Va en el extremo del USB",
          "Graba, depura y puerto serie", "No ejecuta tu aplicación",
          "Se aísla quitando CN2"]),
    ]
    for x, y, bw, bh, color, kicker, title, lines in boxes:
        s += rect(x, y, bw, bh, "#fff", color, 2.5, 8)
        s += rect(x, y, bw, 8, color, color, 0, 0)
        s += text(x + 16, y + 36, kicker, "xs", fill=color)
        s += text(x + 16, y + 62, title, "h")
        yy = y + 96
        for line_s in lines:
            s += text(x + 16, yy, "• " + line_s, "sm")
            yy += 22

    s += rect(40, 370, 1020, 210, "#fff", "#a8a29e", 1, 8)
    s += text(60, 400, "Y además, dos familias de conectores sobre la misma tarjeta", "h")
    s += rect(60, 420, 470, 130, "#fff7ed", "#c2410c", 1.5, 6)
    s += text(76, 446, "Arduino Uno Rev. 3", "sm")
    s += text(76, 470, "CN6 potencia, CN8 analógico, CN5 y CN9 digitales.", "sm")
    s += text(76, 492, "Sirve para shields y para el banco de pruebas.", "sm")
    s += text(76, 514, "No da acceso a todos los pines del LQFP64.", "sm")
    s += rect(560, 420, 470, 130, "#eff6ff", "#1d4ed8", 1.5, 6)
    s += text(576, 446, "ST Morpho", "sm")
    s += text(576, 470, "CN7 (izquierda, 38 pines) y CN10 (derecha, 38 pines).", "sm")
    s += text(576, 492, "Misma pista de cobre que el conector Arduino cuando", "sm")
    s += text(576, 514, "la señal está cableada. No son pines extra del MCU.", "sm")
    return s + svg_close()


def vista():
    w, h = 980, 1280
    s = svg_open(w, h, "Vista superior esquemática NUCLEO-F303RE")
    s += text(24, 32, "NUCLEO-F303RE — vista superior esquemática", "h")
    s += text(24, 54, "Orientación: conector USB arriba. No es un plano a escala. Pines según UM1724 Rev 17, Figura 15.", "sub")

    # board
    s += rect(250, 80, 420, 1120, "#d6e2ee", "#1e3a5f", 2.5, 12)
    # ST-LINK zone
    s += rect(270, 100, 380, 250, "#ccfbf1", "#0f766e", 1.5, 8)
    s += text(460, 124, "Zona ST-LINK/V2-1", "sm", "middle", "#0f766e")
    s += rect(390, 140, 140, 36, "#fff", "#0f766e", 1.5, 4)
    s += text(460, 163, "CN1  USB Mini-B", "sm", "middle")
    s += text(460, 198, "U2  STM32F103CBT6", "xs", "middle")
    s += text(460, 216, "LD1  COM (tricolor)", "xs", "middle")
    s += rect(300, 240, 90, 36, "#fef9c3", "#a16207", 1.2, 3)
    s += text(345, 262, "CN2 ON", "xs", "middle")
    s += rect(410, 240, 100, 36, "#fef9c3", "#a16207", 1.2, 3)
    s += text(460, 262, "JP5  1-2", "xs", "middle")
    s += rect(530, 240, 90, 36, "#fef9c3", "#a16207", 1.2, 3)
    s += text(575, 262, "JP1 OFF", "xs", "middle")
    s += text(460, 300, "CN4 SWD (para otra tarjeta, con CN2 quitado)", "tiny", "middle")
    s += text(460, 328, "Corte posible entre ST-LINK y el MCU", "tiny", "middle", "#57534e")

    # MCU zone
    s += rect(340, 560, 240, 160, "#1e3a5f", "#1e3a5f", 1, 8)
    s += text(460, 610, "U5", "sm", "middle", "#fff")
    s += text(460, 636, "STM32F303RET6", "sm", "middle", "#fff")
    s += text(460, 658, "LQFP64", "xs", "middle", "#dbeafe")
    s += text(460, 690, "El programa corre aquí", "xs", "middle", "#dbeafe")

    # user IO
    s += rect(300, 780, 120, 70, "#dcfce7", "#166534", 1.4, 6)
    s += text(360, 808, "LD2 verde", "sm", "middle")
    s += text(360, 828, "PA5  SB21 ON", "xs", "middle")
    s += rect(440, 780, 130, 70, "#dbeafe", "#1d4ed8", 1.4, 6)
    s += text(505, 808, "B1 USER", "sm", "middle")
    s += text(505, 828, "PC13  SB17 ON", "xs", "middle")
    s += rect(300, 870, 120, 56, "#fee2e2", "#991b1b", 1.4, 6)
    s += text(360, 894, "LD3 PWR", "sm", "middle")
    s += text(360, 912, "hay +5 V", "xs", "middle")
    s += rect(440, 870, 130, 56, "#f5f5f4", "#44403c", 1.4, 6)
    s += text(505, 894, "B2 RESET", "sm", "middle")
    s += text(505, 912, "NRST a masa", "xs", "middle")
    s += rect(360, 950, 200, 48, "#fef9c3", "#a16207", 1.2, 4)
    s += text(460, 978, "JP6 IDD  cerrado = VDD", "xs", "middle")
    s += text(460, 1040, "X2  32,768 kHz en C-02 o posterior", "xs", "middle")
    s += text(460, 1080, "Serigrafía: NUCLEO-F303RE", "xs", "middle", "#1e3a5f")
    s += text(460, 1110, "Abajo: lado opuesto al USB", "tiny", "middle", "#57534e")

    # left morpho / arduino labels
    s += rect(70, 380, 150, 640, "#eff6ff", "#1d4ed8", 1.2, 6)
    s += text(145, 404, "Izquierda", "sm", "middle", "#1d4ed8")
    s += text(145, 424, "CN7 Morpho", "xs", "middle")
    s += text(145, 442, "38 pines", "xs", "middle")
    s += text(145, 470, "Dentro, más", "xs", "middle")
    s += text(145, 488, "cerca del MCU:", "xs", "middle")
    s += text(145, 516, "CN6 potencia", "xs", "middle", "#c2410c")
    s += text(145, 534, "CN8 A0–A5", "xs", "middle", "#c2410c")
    s += text(145, 570, "El mapa pin a pin", "tiny", "middle")
    s += text(145, 586, "está en los", "tiny", "middle")
    s += text(145, 602, "diagramas de", "tiny", "middle")
    s += text(145, 618, "conectores.", "tiny", "middle")

    s += rect(700, 380, 150, 640, "#fff7ed", "#c2410c", 1.2, 6)
    s += text(775, 404, "Derecha", "sm", "middle", "#c2410c")
    s += text(775, 424, "CN10 Morpho", "xs", "middle")
    s += text(775, 442, "38 pines", "xs", "middle")
    s += text(775, 470, "Dentro:", "xs", "middle")
    s += text(775, 496, "CN5  D8–D15", "xs", "middle", "#1d4ed8")
    s += text(775, 514, "CN9  D0–D7", "xs", "middle", "#1d4ed8")
    s += text(775, 550, "D0 y D1 no", "xs", "middle", "#991b1b")
    s += text(775, 568, "llegan al MCU", "xs", "middle", "#991b1b")
    s += text(775, 586, "con SB62/SB63", "xs", "middle", "#991b1b")
    s += text(775, 604, "abiertos.", "xs", "middle", "#991b1b")

    s += text(24, 1240, "Leyenda de color: verde azulado = ST-LINK, azul oscuro = MCU, ámbar = jumpers, naranja = Arduino, azul = Morpho.", "tiny")
    return s + svg_close()


def bloques():
    w, h = 1180, 760
    s = svg_open(w, h, "Diagrama de bloques NUCLEO-F303RE")
    s += defs_arrows()
    s += text(28, 34, "NUCLEO-F303RE — bloques y quién habla con quién", "h")
    s += text(28, 56, "UM1724 Rev 17, secciones 7.4 a 7.10, y esquema MB1136 C05.", "sub")

    s += rect(28, 90, 200, 160, "#ede9fe", "#6d28d9", 1.6, 8)
    s += text(128, 130, "PC", "h", "middle")
    s += text(128, 158, "VS Code", "sm", "middle")
    s += text(128, 178, "CubeMX", "sm", "middle")
    s += text(128, 198, "terminal serie", "sm", "middle")
    s += text(128, 228, "USB con datos", "xs", "middle")

    s += rect(300, 80, 280, 200, "#ccfbf1", "#0f766e", 1.8, 8)
    s += text(440, 110, "ST-LINK/V2-1", "h", "middle", "#0f766e")
    s += text(440, 136, "U2 STM32F103CBT6", "sm", "middle")
    s += text(440, 160, "1. Depuración SWD", "xs", "middle")
    s += text(440, 178, "2. Disco y programación", "xs", "middle")
    s += text(440, 196, "3. Puerto COM virtual", "xs", "middle")
    s += text(440, 214, "4. MCO 8 MHz hacia PF0", "xs", "middle")
    s += text(440, 240, "CN1 pide hasta 300 mA", "xs", "middle")
    s += text(440, 258, "si JP1 está abierto", "xs", "middle")

    s += rect(760, 70, 390, 250, "#dbeafe", "#1e3a5f", 1.8, 8)
    s += text(955, 100, "STM32F303RET6", "h", "middle", "#1e3a5f")
    s += text(955, 124, "U5 · Cortex-M4F a 72 MHz", "sm", "middle")
    s += text(778, 156, "512 KB Flash · 64 KB SRAM + 16 KB CCM", "xs")
    s += text(778, 176, "4 ADC · 2 DAC · 7 comp. · 4 op-amp", "xs")
    s += text(778, 196, "TIM1 y TIM8 · TIM2 de 32 bits", "xs")
    s += text(778, 216, "3 USART · 2 UART · 3 I2C · CAN · USB", "xs")
    s += text(778, 236, "51 E/S: 26 TC/TTa y 25 FT/FTf", "xs")
    s += text(778, 256, "VDD = 3,3 V del regulador U4", "xs")
    s += text(778, 290, "El programa corre solo aquí.", "xs")

    s += line(228, 160, 300, 160, "#44403c", 1.8, "arr")
    s += text(264, 150, "USB", "tiny", "middle")

    links = [
        (120, "1  SWD   PA13 / PA14"),
        (165, "2  NRST"),
        (210, "3  USART2   PA2 / PA3"),
        (255, "4  MCO 8 MHz a PF0"),
    ]
    for y, label in links:
        s += line(580, y, 760, y, "#1d4ed8", 1.4, "arrw")
        s += text(670, y - 8, label, "tiny", "middle")

    s += rect(28, 360, 552, 160, "#ffedd5", "#c2410c", 1.5, 8)
    s += text(48, 388, "Alimentación (hoja Top and Power)", "sm")
    s += text(48, 414, "USB 5 V → U5V. JP5 en 1-2 selecciona U5V (defecto).", "xs")
    s += text(48, 434, "VIN 7–12 V entra por U3 LD1117S50TR y sale 5 V.", "xs")
    s += text(48, 454, "E5V es 5 V directo, por CN7 pin 6, con JP5 en 2-3.", "xs")
    s += text(48, 474, "+5 V → U4 LD39050PU33R → +3,3 V (VDD). JP6 en serie.", "xs")
    s += text(48, 494, "LD3 rojo se enciende cuando hay +5 V en la parte del MCU.", "xs")

    s += rect(600, 360, 550, 160, "#ecfccb", "#3f6212", 1.5, 8)
    s += text(620, 388, "Lo que sale hacia el protoboard", "sm")
    s += text(620, 414, "Arduino Uno Rev. 3: CN5, CN6, CN8, CN9.", "xs")
    s += text(620, 434, "Morpho: CN7 y CN10, 38 pines cada uno.", "xs")
    s += text(620, 454, "PA13 y PA14 están en CN7, pero son el SWD.", "xs")
    s += text(620, 474, "No los uses como E/S con el ST-LINK conectado.", "xs")
    s += text(620, 494, "PA2 y PA3 no llegan a D1/D0: SB62 y SB63 abiertos.", "xs")

    s += rect(28, 545, 1122, 185, "#fff", "#a8a29e", 1, 8)
    s += text(48, 574, "Señales que comparten pista y por eso se reservan en este curso", "sm")
    rows = [
        "PA5 — LD2, D13, SPI1_SCK y DAC1_OUT2. El curso lo deja para el LED de la tarjeta.",
        "PC13 — pulsador B1, activo a nivel bajo, con R30 = 4,7 kΩ y C15 = 100 nF.",
        "PA2 / PA3 — USART2 hacia el puerto COM virtual. No están en el conector Arduino.",
        "PF0 — entrada de reloj de 8 MHz desde el ST-LINK en placas C-02 o posteriores.",
        "PB8 / PB9 — I2C1 en D15/D14. También pueden ser CAN; este curso los deja para I2C.",
    ]
    y = 600
    for r in rows:
        s += text(48, y, r, "xs")
        y += 22
    return s + svg_close()


def alimentacion():
    w, h = 1180, 820
    s = svg_open(w, h, "Caminos de alimentación NUCLEO-F303RE")
    s += defs_arrows()
    s += text(24, 32, "Caminos de alimentación y jumpers", "h")
    s += text(24, 54, "UM1724 Rev 17, §7.5, Tablas 6 a 9. Esquema MB1136 C05, hoja Top and Power.", "sub")

    cols = [
        (24, "#ede9fe", "#6d28d9", "Fuentes", [
            "CN1 USB",
            "5 V, VBUS",
            "100 mA antes",
            "de enumerar",
            "",
            "VIN",
            "CN6 pin 8",
            "CN7 pin 24",
            "7 V a 12 V",
            "",
            "E5V",
            "CN7 pin 6",
            "4,75–5,25 V",
            "500 mA máx.",
        ]),
    ]
    # manual layout
    s += rect(20, 80, 200, 150, "#ede9fe", "#6d28d9", 1.4, 6)
    s += text(120, 108, "CN1 USB", "sm", "middle")
    s += text(120, 132, "5 V (VBUS)", "xs", "middle")
    s += text(120, 152, "100 mA al conectar", "xs", "middle")
    s += text(120, 172, "300 mA si JP1 OFF", "xs", "middle")
    s += text(120, 200, "Solo el ST-LINK", "tiny", "middle")

    s += rect(20, 250, 200, 130, "#fef9c3", "#a16207", 1.4, 6)
    s += text(120, 278, "VIN", "sm", "middle")
    s += text(120, 302, "7 V a 12 V", "xs", "middle")
    s += text(120, 322, "CN6-8 o CN7-24", "xs", "middle")
    s += text(120, 348, "800 mA a 7 V", "tiny", "middle")
    s += text(120, 364, "250 mA entre 9 y 12 V", "tiny", "middle")

    s += rect(20, 400, 200, 110, "#ffedd5", "#c2410c", 1.4, 6)
    s += text(120, 428, "E5V", "sm", "middle")
    s += text(120, 452, "4,75 V a 5,25 V", "xs", "middle")
    s += text(120, 472, "CN7 pin 6", "xs", "middle")
    s += text(120, 492, "500 mA máximo", "xs", "middle")

    s += rect(20, 530, 200, 110, "#fee2e2", "#991b1b", 1.4, 6)
    s += text(120, 558, "+3,3 V externo", "sm", "middle")
    s += text(120, 582, "CN6 pin 4", "xs", "middle")
    s += text(120, 602, "3,0 V a 3,6 V", "xs", "middle")
    s += text(120, 622, "ST-LINK no arranca", "tiny", "middle")

    s += rect(280, 80, 250, 150, "#ccfbf1", "#0f766e", 1.4, 6)
    s += text(405, 108, "Parte ST-LINK", "sm", "middle")
    s += text(405, 132, "Siempre que hay USB", "xs", "middle")
    s += text(405, 156, "T2, P-MOS, deja pasar", "xs", "middle")
    s += text(405, 176, "U5V hacia el MCU tras", "xs", "middle")
    s += text(405, 196, "la enumeración", "xs", "middle")

    s += rect(280, 260, 250, 140, "#fff", "#a16207", 1.4, 6)
    s += text(405, 288, "U3 LD1117S50TR", "sm", "middle")
    s += text(405, 314, "De VIN hace 5 V", "xs", "middle")
    s += text(405, 338, "Ese 5 V entra a JP5", "xs", "middle")
    s += text(405, 358, "por el lado E5V", "xs", "middle")
    s += text(405, 378, "(pin 3)", "xs", "middle")

    s += rect(600, 150, 220, 180, "#fef9c3", "#a16207", 2, 8)
    s += text(710, 180, "JP5", "h", "middle")
    s += text(710, 210, "pin 1-2 = U5V", "sm", "middle")
    s += text(710, 232, "defecto, USB", "xs", "middle")
    s += text(710, 262, "pin 2-3 = E5V", "sm", "middle")
    s += text(710, 284, "VIN o 5 V externo", "xs", "middle")
    s += text(710, 310, "Míralo antes de alimentar", "tiny", "middle", "#991b1b")

    s += rect(600, 360, 220, 100, "#fff7ed", "#c2410c", 1.4, 6)
    s += text(710, 390, "JP1", "sm", "middle")
    s += text(710, 414, "OFF: pide 300 mA", "xs", "middle")
    s += text(710, 434, "ON: se limita a 100 mA", "xs", "middle")

    s += rect(880, 90, 270, 120, "#fef3c7", "#a16207", 1.4, 6)
    s += text(1015, 118, "+5 V", "h", "middle")
    s += text(1015, 146, "CN6 pin 5 · CN7 pin 18", "xs", "middle")
    s += text(1015, 168, "LD3 rojo encendido", "xs", "middle")
    s += text(1015, 188, "Sale hacia un shield", "tiny", "middle")

    s += rect(880, 240, 270, 130, "#dbeafe", "#1d4ed8", 1.4, 6)
    s += text(1015, 268, "U4 LD39050PU33R", "sm", "middle")
    s += text(1015, 292, "LDO 3,3 V", "xs", "middle")
    s += text(1015, 312, "500 mA máximo", "xs", "middle")
    s += text(1015, 332, "SB2 ON = esta salida", "xs", "middle")
    s += text(1015, 352, "llega a +3,3 V", "xs", "middle")

    s += rect(880, 400, 270, 110, "#dcfce7", "#166534", 1.6, 6)
    s += text(1015, 428, "+3,3 V  VDD del MCU", "sm", "middle")
    s += text(1015, 452, "CN6 pin 4", "xs", "middle")
    s += text(1015, 472, "CN7 pines 12 y 16", "xs", "middle")
    s += text(1015, 492, "No inyectes 5 V aquí", "xs", "middle", "#991b1b")

    s += rect(880, 540, 270, 110, "#1e3a5f", "#1e3a5f", 1.4, 6)
    s += text(1015, 570, "JP6 en serie con VDD", "sm", "middle", "#fff")
    s += text(1015, 594, "ON: el MCU recibe 3,3 V", "xs", "middle", "#dbeafe")
    s += text(1015, 614, "OFF: solo con amperímetro", "xs", "middle", "#dbeafe")
    s += text(1015, 634, "Si no, U5 está apagado", "xs", "middle", "#fecaca")

    s += line(220, 150, 280, 150, "#0f766e", 1.6, "arr")
    s += path("M 530 145 H 545 V 185 H 600", "#0f766e", 1.6, "arr")
    s += line(220, 310, 280, 320, "#a16207", 1.6, "arr")
    s += path("M 530 330 H 548 V 230 H 600", "#a16207", 1.6, "arr")
    s += path("M 220 455 H 250 V 520 H 575 V 305 H 600", "#c2410c", 1.5, "arr")
    s += text(250, 548, "E5V no pasa por U3", "tiny", fill="#c2410c")
    s += line(820, 210, 880, 150, "#a16207", 1.6, "arr")
    s += line(1015, 210, 1015, 240, "#1d4ed8", 1.6, "arrw")
    s += line(1015, 370, 1015, 400, "#166534", 1.6, "arr")
    s += line(1015, 510, 1015, 540, "#1e3a5f", 1.6, "arr")

    s += rect(20, 670, 1130, 125, "#fff", "#a8a29e", 1, 6)
    s += text(36, 696, "Orden si usas fuente externa (UM1724 §7.5.2)", "sm")
    s += text(36, 720, "1) JP5 en pines 2-3.  2) JP1 quitado.  3) Conectar VIN o E5V.  4) Encender la fuente.", "xs")
    s += text(36, 740, "5) Comprobar que LD3 enciende.  6) Después conectar el USB. La fuente debe ser SELV (EN 62368-1).", "xs")
    s += text(36, 764, "Un cargador USB no enumera: LD3 se queda apagado y el MCU no recibe 5 V, salvo que pongas JP1 en ON.", "xs")
    s += text(36, 784, "Nunca pongas 5 V en el pin de +3,3 V, ni 12 V en VIN por encima del límite de la Tabla 7.", "xs")
    return s + svg_close()


def tabla_arduino():
    w, h = 1100, 1180
    s = svg_open(w, h, "Conectores Arduino de la NUCLEO-F303RE")
    s += text(24, 32, "Conectores Arduino Uno Rev. 3 en la NUCLEO-F303RE", "h")
    s += text(24, 54, "UM1724 Rev 17, Tabla 14 y Figura 15. La columna «de fábrica» indica el puente por defecto.", "sub")

    headers = ["Conector", "Pin", "Nombre", "Señal STM32", "Nota verificada"]
    xs = [24, 130, 190, 280, 430]
    s += rect(20, 74, 1060, 28, "#1e3a5f", "#1e3a5f", 0, 0)
    for x, htxt in zip(xs, headers):
        s += text(x, 93, htxt, "xs", fill="#fff")

    y = 102
    colors = {"CN6": "#fff7ed", "CN8": "#ecfccb", "CN5": "#eff6ff", "CN9": "#f5f5f4"}
    for i, (con, pin, name, sig, note) in enumerate(ARDUINO):
        bg = colors[con]
        if "NO conectado" in note:
            bg = "#fee2e2"
        s += rect(20, y, 1060, 26, bg, "#e7e5e4", 0.6, 0)
        vals = [con, pin, name, sig, note]
        for x, val in zip(xs, vals):
            s += text(x, y + 17, val, "xs")
        y += 26

    s += text(24, y + 28, "A4 y A5: SB56 y SB51 están cerrados de fábrica, así que llegan PC1 y PC0. PB9 y PB8 están en D14 y D15.", "xs")
    s += text(24, y + 48, "D0 y D1 aparecen en la serigrafía, pero SB62 y SB63 están abiertos: la pista no llega al MCU.", "xs")
    s += text(24, y + 68, "PA0, PA1, PA4, PB0, PC0 y PC1 son TTa: la entrada analógica no admite 5 V (datasheet, Tabla 19).", "xs")
    return s + svg_close()


def tabla_morpho():
    w, h = 1180, 980
    s = svg_open(w, h, "Conectores ST Morpho NUCLEO-F303RE")
    s += text(24, 32, "ST Morpho — CN7 izquierda y CN10 derecha", "h")
    s += text(24, 54, "UM1724 Rev 17, Tabla 26 (NUCLEO-F303RE). 19×2 cada conector. Pin 1 arriba, con el USB hacia arriba.", "sub")

    def draw_table(x0, title, rows, color):
        out = text(x0, 90, title, "sm", fill=color)
        out += rect(x0, 100, 540, 24, color, color, 0, 0)
        labels = ["Impar", "Señal", "Par", "Señal"]
        lx = [x0 + 8, x0 + 70, x0 + 270, x0 + 330]
        for x, lab in zip(lx, labels):
            out += text(x, 116, lab, "xs", fill="#fff")
        y = 124
        for i, (a, an, b, bn) in enumerate(rows):
            bg = "#fff" if i % 2 == 0 else "#f5f5f4"
            if "abierto" in an or "abierto" in bn or "SWD" in an:
                bg = "#fee2e2"
            out += rect(x0, y, 540, 22, bg, "#e7e5e4", 0.4, 0)
            out += text(x0 + 8, y + 15, str(a), "xs")
            out += text(x0 + 70, y + 15, an, "xs")
            out += text(x0 + 270, y + 15, str(b), "xs")
            out += text(x0 + 330, y + 15, bn, "xs")
            y += 22
        return out

    s += draw_table(24, "CN7 — Morpho izquierdo", CN7, "#1d4ed8")
    s += draw_table(600, "CN10 — Morpho derecho", CN10, "#c2410c")
    s += text(24, 940, "Filas en rojo: PA13/PA14 son el depurador. PA2 y PA3 figuran en la tabla pero el puente de fábrica los deja abiertos (SB62, SB63).", "xs")
    s += text(24, 960, "CN7 pin 36 es PC1 por defecto (A4). CN7 pin 38 es PC0 por defecto (A5). Cambian a PB9/PB8 solo si se modifican SB46, SB52, SB56 y SB51.", "xs")
    return s + svg_close()


def reverso():
    w, h = 1000, 720
    s = svg_open(w, h, "Cómo identificar la revisión de la placa")
    s += text(24, 34, "Cómo saber qué revisión tienes en la mano", "h")
    s += text(24, 56, "UM1724 Rev 17, §8.1 y Tabla 35. La etiqueta está en la cara de abajo.", "sub")

    s += rect(40, 90, 420, 260, "#fff", "#1e3a5f", 1.6, 8)
    s += text(60, 120, "Etiqueta, ejemplo de lectura", "sm")
    s += rect(70, 145, 360, 160, "#fef9c3", "#a16207", 1.2, 4)
    s += text(90, 180, "NUCLEO-F303RE", "h")
    s += text(90, 210, "MB1136-F303RE-C05", "sm")
    s += text(90, 236, "syywwxxxxx", "sm")
    s += text(90, 270, "MB1136 = PCB    F303RE = montaje", "xs")
    s += text(90, 288, "C = revisión del circuito    05 = ensamblado", "xs")

    s += rect(500, 90, 460, 260, "#fff", "#0f766e", 1.6, 8)
    s += text(520, 120, "Qué cambia y qué no", "sm")
    items = [
        "C-01: sin cristal de 32 kHz y sin MCO.",
        "C-02: entra X2 32,768 kHz y el MCO de 8 MHz.",
        "C-03: otro cristal ABS25 y condensadores nuevos.",
        "C-04: cambia el transistor T2 de potencia.",
        "C-05: cambia CN1, B1 y B2. Sigue siendo Mini-B",
        "en el esquema C05 (5075BMR-05-SM).",
    ]
    y = 150
    for it in items:
        s += text(520, y, it, "xs")
        y += 28

    s += rect(40, 380, 920, 300, "#fff", "#a8a29e", 1.2, 8)
    s += text(60, 412, "Puentes que debes conocer antes de cablear", "sm")
    bridges = [
        ("SB13, SB14", "ON", "PA2/PA3 unidos al ST-LINK (puerto virtual)"),
        ("SB62, SB63", "OFF", "PA2/PA3 NO llegan a D1/D0 ni al Morpho"),
        ("SB21", "ON", "LD2 verde unido a PA5 / D13"),
        ("SB17", "ON", "Pulsador B1 unido a PC13"),
        ("SB56, SB51", "ON", "A4 = PC1 y A5 = PC0"),
        ("SB46, SB52", "OFF", "PB8/PB9 no están duplicados en A5/A4"),
        ("SB16, SB50", "ON*", "MCO 8 MHz a PF0, desde la revisión C-02"),
        ("SB2", "ON", "La salida de 3,3 V del LDO llega a VDD"),
        ("SB45, SB57", "ON", "VBAT y VDDA unidos a VDD"),
    ]
    y = 440
    for name, state, desc in bridges:
        s += text(60, y, name, "xs")
        s += text(200, y, state, "xs", fill="#166534" if state.startswith("ON") else "#991b1b")
        s += text(280, y, desc, "xs")
        y += 24
    return s + svg_close()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "tres-entidades.svg": entidades(),
        "nucleo-f303re-vista-superior.svg": vista(),
        "nucleo-f303re-bloques.svg": bloques(),
        "nucleo-f303re-alimentacion.svg": alimentacion(),
        "nucleo-f303re-conectores-arduino.svg": tabla_arduino(),
        "nucleo-f303re-conectores-morpho.svg": tabla_morpho(),
        "nucleo-f303re-reverso-revision.svg": reverso(),
    }
    for name, data in files.items():
        path = OUT / name
        path.write_text(data, encoding="utf-8")
        print(path, path.stat().st_size)


if __name__ == "__main__":
    main()
