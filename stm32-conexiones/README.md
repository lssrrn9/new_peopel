# Conexiones STM32 Blue Pill

Figuras de cableado de la placa **Blue Pill STM32F103C8T6**. Cada figura es un PNG, no un dibujo hecho con caracteres.

Abre `index.html` en el navegador para verlas juntas.

| Figura | Qué muestra |
| --- | --- |
| `figuras/01-mapa-pines.png` | Headers de 20 pines y header SWD |
| `figuras/02-alimentacion.png` | USB o pin 5 V, tierra y salida de 3,3 V |
| `figuras/03-stlink-swd.png` | ST-Link V2: SWDIO, SWCLK y GND |
| `figuras/04-uart-bootloader.png` | USB-TTL cruzado a PA9 y PA10 |
| `figuras/05-sensor-i2c.png` | I2C1 en PB6 (SCL) y PB7 (SDA) |
| `figuras/06-periferico-spi.png` | SPI1 en PA4, PA5, PA6 y PA7 |

El orden de los headers sigue el mapa de [stm32-base.org](https://stm32-base.org/boards/STM32F103C8T6-Blue-Pill.html). Las funciones USART, I2C, SPI y SWD son las de reset del STM32F103, sin remap. Confirma la serigrafía de tu placa antes de contar: hay clones con el conector al revés.

Para regenerar los PNG:

```bash
python3 generar_figuras.py
```

Hace falta Pillow (`pip install pillow`).
