#!/usr/bin/env python3
"""Esquemas de cableado de las prácticas. No son fotos ni planos mecánicos.

Cada dibujo nombra el conector, el pin y la señal según UM1724 Rev 17.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "curso" / "img"
FONT = "Liberation Sans, Segoe UI, sans-serif"


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def diagrama(nombre, titulo, nota, pines, bloques, avisos):
    """pines: lista de (conector, pin, senal, destino).
    bloques: lista de (titulo, lineas).
    """
    w, h = 1100, 220 + 28 * max(len(pines), 6) + 36 * len(avisos)
    h = max(h, 520)
    y_box = 88
    box_h = 36 + 22 * len(pines)
    parts = []
    a = parts.append
    a(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<title>{esc(titulo)}</title>
<rect width="100%" height="100%" fill="#f6f3ee"/>
<style>text {{ font-family: {FONT}; fill: #1c1917; }}</style>
<text x="24" y="32" font-size="20" font-weight="700">{esc(titulo)}</text>
<text x="24" y="54" font-size="12" fill="#57534e">{esc(nota)}</text>
''')
    a(f'<rect x="24" y="{y_box}" width="460" height="{box_h}" rx="8" fill="#dbeafe" stroke="#1e3a5f" stroke-width="1.6"/>')
    a(f'<text x="40" y="{y_box + 24}" font-size="14" font-weight="700" fill="#1e3a5f">NUCLEO-F303RE · USB arriba</text>')
    y = y_box + 48
    for con, pin, senal, dest in pines:
        a(f'<text x="40" y="{y}" font-size="13">{esc(con)} pin {esc(pin)} · {esc(senal)} → {esc(dest)}</text>')
        y += 22
    x = 560
    yb = y_box
    for title, lines in bloques:
        bh = 36 + 20 * len(lines)
        a(f'<rect x="{x}" y="{yb}" width="500" height="{bh}" rx="8" fill="#fff" stroke="#c2410c" stroke-width="1.5"/>')
        a(f'<text x="{x + 16}" y="{yb + 24}" font-size="14" font-weight="700" fill="#c2410c">{esc(title)}</text>')
        yy = yb + 46
        for line in lines:
            a(f'<text x="{x + 16}" y="{yy}" font-size="13">{esc(line)}</text>')
            yy += 20
        yb += bh + 16
    ya = max(y_box + box_h, yb) + 28
    for aviso in avisos:
        a(f'<text x="24" y="{ya}" font-size="13">{esc(aviso)}</text>')
        ya += 22
    a("</svg>\n")
    path = OUT / nombre
    path.write_text("".join(parts), encoding="utf-8")
    print(path.name)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    diagrama(
        "cable-led-pc7.svg",
        "LED externo en PC7 (D9)",
        "UM1724 Tabla 14: CN5 pin 2 = D9 = PC7. Corriente limitada por R, calculada en el módulo 2.",
        [("CN5", "2", "PC7 / D9", "resistencia del LED"),
         ("CN6", "6", "GND", "cátodo del LED")],
        [("LED indicador",
          ["Ánodo hacia la resistencia.",
           "Cátodo (pata corta, lado plano) a GND.",
           "R = (3,3 V − Vf) / If, If ≤ 8 mA.",
           "No usar PC13 para este LED."])],
        ["Tierra común: GND de CN6. Alimentación del LED: el propio pin, no 5 V.",
         "PC7 es FT (datasheet, tabla 13). La salida sigue siendo de 3,3 V."],
    )
    diagrama(
        "cable-pulsador-pa8.svg",
        "Pulsador externo en PA8 (D7)",
        "UM1724 Tabla 14: CN9 pin 8 = D7 = PA8.",
        [("CN9", "8", "PA8 / D7", "pulsador y condensador"),
         ("CN6", "4", "+3,3 V", "resistencia 4,7 kΩ"),
         ("CN6", "7", "GND", "otro extremo del pulsador")],
        [("Red del pulsador",
          ["4,7 kΩ de +3,3 V a PA8.",
           "100 nF de PA8 a GND.",
           "Pulsador entre PA8 y GND.",
           "En reposo el pin está a 3,3 V. Pulsado, a 0 V."])],
        ["No alimentes el pulsador con 5 V: PA8 se queda en la red de 3,3 V.",
         "El pulsador azul de la placa sigue siendo PC13 y no se cablea aquí."],
    )
    diagrama(
        "cable-semaforo.svg",
        "Semáforo de tres LED",
        "Pines libres del mapa del curso. Cada LED con su resistencia a GND.",
        [("CN9", "8", "PA8 / D7", "LED rojo, ánodo vía R"),
         ("CN9", "5", "PB5 / D4", "LED ámbar, ánodo vía R"),
         ("CN5", "2", "PC7 / D9", "LED verde, ánodo vía R"),
         ("CN6", "6", "GND", "cátodos de los tres LED")],
        [("Tres indicadores",
          ["Un resistor por LED, calculado con su Vf.",
           "No unas los tres ánodos a una sola R.",
           "Corriente de trabajo ≤ 8 mA por pin.",
           "Suma muy por debajo de 80 mA."])],
        ["Esto imita los tiempos de un cruce, no cumple una norma de tráfico.",
         "LD2 (PA5) no forma parte del semáforo."],
    )
    diagrama(
        "cable-esp32-uart.svg",
        "USART1 hacia un ESP32 a 3,3 V",
        "UM1724: D8 = PA9 = USART1_TX, D2 = PA10 = USART1_RX. Los dos son FT/FTf.",
        [("CN5", "1", "PA9 / D8 TX", "RX del ESP32"),
         ("CN9", "3", "PA10 / D2 RX", "TX del ESP32"),
         ("CN6", "7", "GND", "GND del ESP32")],
        [("ESP32",
          ["Aliméntalo por su propio USB.",
           "UART a 3,3 V, no el pin de 5 V.",
           "TX del uno va al RX del otro.",
           "GND común obligatorio."])],
        ["La salida del STM32 es 3,3 V aunque el pin tolere 5 V en la entrada.",
         "USART2 (PA2/PA3) se queda para el puerto virtual del ST-LINK."],
    )
    diagrama(
        "cable-rele-transistor.svg",
        "Relé o zumbador con transistor y diodo",
        "La bobina no toca el GPIO. El diodo va en antiparalelo con la bobina.",
        [("CN9", "5", "PB5 / D4", "resistencia de base"),
         ("CN6", "6", "GND", "emisor del NPN y masa de la bobina"),
         ("CN6", "5", "+5 V", "bobina, solo si la corriente cabe en el USB")],
        [("Etapa",
          ["NPN: emisor a GND, colector a la bobina.",
           "Resistencia de base calculada en el módulo.",
           "Diodo 1N4007, cátodo al + de la bobina.",
           "Si la bobina pide más de lo que el USB puede, fuente de 5 V aparte y GND común."])],
        ["No conectes la bobina entre un GPIO y GND.",
         "Un relé de red no se cablea en esta práctica: solo la bobina de baja tensión."],
    )
    diagrama(
        "cable-servo-educativo.svg",
        "Servo educativo, no industrial",
        "Señal en PB10 (D6, TIM2_CH3). El motor del servo no sale de un pin ni de 3,3 V.",
        [("CN9", "7", "PB10 / D6", "cable de señal, normalmente naranja o blanco"),
         ("CN6", "6", "GND", "GND del servo y de su fuente de 5 V"),
         ("Fuente 5 V externa", "—", "+5 V", "cable rojo del servo")],
        [("Servo de hobby",
          ["Tipo SG90 o equivalente de prácticas.",
           "Pulso según la hoja de ese servo, en torno a 1–2 ms cada 20 ms.",
           "No es un servo industrial con encoder y driver de potencia.",
           "La fuente de 5 V del servo es externa y comparte GND."])],
        ["No alimentes el servo desde CN6 pin 4 (3,3 V).",
         "Confirma en la hoja que la señal de 3,3 V es aceptada. Si no, hace falta un desplazador."],
    )
    diagrama(
        "cable-potenciometro-pa0.svg",
        "Potenciómetro en PA0 (A0)",
        "UM1724 Tabla 14: CN8 pin 1 = A0 = PA0, ADC1_IN1, pin TTa.",
        [("CN8", "1", "PA0 / A0", "cursor del potenciómetro"),
         ("CN6", "4", "+3,3 V", "un extremo del potenciómetro"),
         ("CN6", "6", "GND", "el otro extremo")],
        [("Potenciómetro 10 kΩ lineal",
          ["Solo entre 0 y 3,3 V.",
           "No lo alimentes a 5 V.",
           "PA0 no es tolerante a 5 V."])],
        ["Giro a un extremo: cerca de 0 V. Al otro: cerca de 3,3 V.",
         "El código convierte el número de 12 bits con Vref = VDDA ≈ 3,3 V."],
    )
    diagrama(
        "cable-divisor-pa1.svg",
        "Divisor para una tensión externa en PA1",
        "La fuente externa se limita antes de A1. PA1 es TTa.",
        [("CN8", "2", "PA1 / A1", "punto medio del divisor"),
         ("CN6", "6", "GND", "masa de la fuente y R inferior")],
        [("Divisor",
          ["R superior desde la tensión a medir hasta PA1.",
           "R inferior de PA1 a GND.",
           "Valores calculados para que  el máximo previsto sea < 3,3 V.",
           "Fuente SELV. GND común con la placa."])],
        ["Si la tensión de origen puede pasar del valor previsto, añade un límite a 3,3 V.",
         "No conectes la fuente al pin sin el divisor."],
    )
    diagrama(
        "cable-tmp36-pb0.svg",
        "TMP36 en PB0 (A3), si usas ese sensor",
        "La fórmula es la de la hoja Analog Devices del TMP36. Confírmala en tu revisión.",
        [("CN8", "4", "PB0 / A3", "salida Vout del TMP36"),
         ("CN6", "4", "+3,3 V", "Vs del TMP36"),
         ("CN6", "6", "GND", "GND del TMP36")],
        [("TMP36",
          ["Vs entre 2,7 V y 5,5 V según su hoja: aquí 3,3 V.",
           "Vout ≈ 750 mV a 25 °C, 10 mV/°C.",
           "T (°C) = (Vout_mV − 750) / 10.",
           "100 nF entre Vs y GND, junto al sensor."])],
        ["Si usas otro sensor, no apliques esta fórmula.",
         "PB0 es TTa: la salida del sensor tiene que caber en 0 a 3,3 V."],
    )
    diagrama(
        "cable-i2c-pb8-pb9.svg",
        "I2C1 en D15 y D14",
        "UM1724: D15 = PB8 = SCL, D14 = PB9 = SDA. No son A4 ni A5 de fábrica.",
        [("CN5", "10", "PB8 / D15 SCL", "SCL del módulo"),
         ("CN5", "9", "PB9 / D14 SDA", "SDA del módulo"),
         ("CN6", "4", "+3,3 V", "VCC del módulo"),
         ("CN6", "6", "GND", "GND del módulo")],
        [("Módulo I2C a 3,3 V",
          ["Pull-up 4,7 kΩ a 3,3 V en SCL y SDA si el módulo no los trae.",
           "No alimentes un módulo de solo 5 V.",
           "La dirección de 7 bits se lee en la serigrafía o en la hoja."])],
        ["PB8 y PB9 no se usan a la vez como CAN.",
         "A4 y A5 siguen siendo PC1 y PC0."],
    )
    diagrama(
        "cable-spi2-595.svg",
        "74HC595 a 3,3 V por SPI2",
        "SPI2 en el Morpho CN10, para no usar PA5. Datasheet, AF5.",
        [("CN10", "30", "PB13 SCK", "SRCLK (reloj) del 595"),
         ("CN10", "26", "PB15 MOSI", "SER (dato) del 595"),
         ("CN10", "16", "PB12 NSS", "RCLK (latch)"),
         ("CN6", "4", "+3,3 V", "VCC del 595"),
         ("CN6", "6", "GND", "GND y OE a GND, MR a 3,3 V")],
        [("74HC595 y LED",
          ["Alimentado a 3,3 V, no a 5 V.",
           "Cada salida Q lleva su resistencia y su LED a GND.",
           "MISO (PB14, CN10 pin 28) no hace falta para este integrado."])],
        ["PA5 sigue siendo el LED verde de la placa.",
         "Confirma los nombres SER, SRCLK y RCLK en la hoja del 595 que compres."],
    )
    diagrama(
        "cable-encoder-pb6-pb7.svg",
        "Encoder incremental en TIM4",
        "PB6 = TIM4_CH1 (D10). PB7 = TIM4_CH2 está en CN7 pin 21, no en el Arduino.",
        [("CN5", "3", "PB6 / D10", "canal A"),
         ("CN7", "21", "PB7", "canal B"),
         ("CN6", "4", "+3,3 V", "pull-up si la salida es en colector abierto"),
         ("CN6", "6", "GND", "GND del encoder")],
        [("Encoder de 3,3 V",
          ["No conectes un encoder de 24 V.",
           "Si es colector abierto: 4,7 kΩ a 3,3 V en cada canal.",
           "Cuenta los pulsos por vuelta en la hoja para pasar a RPM."])],
        ["TIM3 queda libre para el PWM de PC7.",
         "GND común con la placa."],
    )
    diagrama(
        "cable-rs485.svg",
        "Modbus RTU con transceptor de 3,3 V",
        "USART1 en PA9/PA10. El sentido del transceptor sale por PC6 (CN10 pin 4).",
        [("CN5", "1", "PA9 TX", "DI del transceptor"),
         ("CN9", "3", "PA10 RX", "RO del transceptor"),
         ("CN10", "4", "PC6", "DE y /RE unidos"),
         ("CN6", "4", "+3,3 V", "VCC del transceptor de 3,3 V"),
         ("CN6", "6", "GND", "GND del transceptor")],
        [("Bus RS-485",
          ["Transceptor tipo MAX3485 o equivalente de 3,3 V.",
           "A y B al par trenzado.",
           "120 Ω entre A y B en cada extremo del bus de prueba.",
           "No uses un MAX485 alimentado a 5 V pegado al pin."])],
        ["La segunda estación es otro USB-RS485 o otra placa con el mismo transceptor.",
         "USART2 sigue disponible para mensajes de diagnóstico al PC."],
    )
    diagrama(
        "cable-can.svg",
        "CAN con transceptor de E/S a 3,3 V",
        "PA11 = CN10 pin 14, PA12 = CN10 pin 12. No uses PB8/PB9: son el I2C.",
        [("CN10", "14", "PA11 CAN_RX", "RXD del transceptor"),
         ("CN10", "12", "PA12 CAN_TX", "TXD del transceptor"),
         ("CN6", "4", "+3,3 V", "VIO o VCC lógico, según la hoja"),
         ("CN6", "6", "GND", "GND lógico")],
        [("Transceptor y bus",
          ["Familia TJA1051T/3 o equivalente con E/S de 3,3 V.",
           "CANH y CANL al otro nodo.",
           "Terminación según la hoja del transceptor y la longitud del cable.",
           "El lado del bus puede pedir 5 V: esa alimentación no sale de un GPIO."])],
        ["PA11 y PA12 también son el USB del chip. Este curso no los usa como USB.",
         "Hacen falta dos nodos. Uno solo no demuestra el bus."],
    )
    diagrama(
        "cable-opto-24v.svg",
        "Entrada de 24 V mediante optoacoplador",
        "Los 24 V se quedan en el lado del LED del opto. Al GPIO solo llega el lado de 3,3 V.",
        [("CN9", "8", "PA8 / D7", "colector del opto y pull-up"),
         ("CN6", "4", "+3,3 V", "pull-up 4,7 kΩ"),
         ("CN6", "6", "GND", "emisor del opto")],
        [("Lado de campo, SELV 24 V",
          ["Fuente de 24 V de continua, no la red de 230 V.",
           "Resistor en serie con el LED del opto, calculado con su Vf.",
           "El GND de 24 V no se une al GND de la placa.",
           "El opto es el aislamiento de esta práctica."])],
        ["Un prototipo de mesa no es un módulo de entradas de un cuadro.",
         "Calcula el resistor con la hoja del opto que montes."],
    )
    diagrama(
        "cable-0-10v.svg",
        "Entrada 0–10 V reducida a menos de 3,3 V",
        "PA1 es TTa. 10 V no se conectan al pin.",
        [("CN8", "2", "PA1 / A1", "salida del divisor y del límite"),
         ("CN6", "6", "GND", "referencia del divisor")],
        [("Acondicionamiento",
          ["R1 = 30 kΩ desde la señal de 0–10 V.",
           "R2 = 10 kΩ de PA1 a GND. A 10 V, PA1 ve 2,5 V.",
           "A 12 V, PA1 vería 3,0 V. Por encima, un límite a 3,3 V.",
           "Condensador de 100 nF de PA1 a GND.",
           "Si las tierras de campo y de la placa no pueden unirse, esta etapa no basta: hace falta aislamiento."])],
        ["Ejemplo numérico de diseño, no una medida.",
         "La fuente de 0–10 V es SELV."],
    )
    diagrama(
        "cable-4-20ma.svg",
        "Lazo 4–20 mA a tensión, lado de baja tensión",
        "Resistencia de 150 Ω: 4 mA → 0,60 V, 20 mA → 3,00 V.",
        [("CN8", "1", "PA0 / A0", "tensión sobre la resistencia de 150 Ω"),
         ("CN6", "6", "GND", "lado de la resistencia que va a GND de la placa")],
        [("Lazo",
          ["La fuente del lazo es externa.",
           "150 Ω, potencia muy por debajo de 0,25 W a 20 mA.",
           "Un diodo o una abrazadera impide que un lazo abierto o un error supere 3,3 V.",
           "Este esquema supone que el retorno del lazo puede compartir GND con la placa.",
           "Si no puede, el módulo aislador sustituye a la resistencia directa."])],
        ["No conectes la fuente de 24 V del lazo a un GPIO.",
         "Confirma en el instrumento si el lazo es de dos hilos y quién lo alimenta."],
    )


if __name__ == "__main__":
    main()
