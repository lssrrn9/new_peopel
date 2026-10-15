# Proyecto P1. Estación de temperatura

Una estación de mesa: un sensor de 3,3 V, el valor en una pantalla I2C y una alarma por umbral. No es un registro de temperatura de un proceso industrial. La exactitud es la de la hoja del sensor que montes.

**No comprobado en hardware.**

## Qué reúne

Módulos 5, 11, 13 y 17. El umbral se puede guardar con el módulo 24 cuando quieras que sobreviva al USB. El módulo 28 deja la tabla de pruebas.

## Material

- TMP36 en PB0, si usas la fórmula del módulo 11, o el MCP9808 en el I2C si prefieres el sensor digital. Elige uno y no mezcles las dos fórmulas.
- OLED SSD1306 a 3,3 V en PB8/PB9, si el barrido del módulo 13 la encontró.
- LED de alarma con su resistencia en PC7, o el transistor del módulo 10 si la alarma es un zumbador. No los dos en el mismo pin. PC7 aquí es el LED. El zumbador, si lo hay, va por el transistor en PB5 y no coincide con el ámbar del semáforo.
- USART2 para el diagnóstico, aunque haya pantalla.

## Pines

| Función | Pin | Notas |
| --- | --- | --- |
| Temperatura analógica | PB0, A3 | Solo si el sensor es el TMP36 u otro de 0 a 3,3 V |
| Temperatura I2C | PB8, PB9 | MCP9808, dirección según la hoja |
| Pantalla | PB8, PB9 | Otra dirección en el mismo bus |
| Alarma luminosa | PC7 | Resistencia calculada |
| Informe | PA2, PA3 | Puerto virtual |

PA0 queda libre. No pongas el potenciómetro a la vez que un 4–20 mA.

## Ejemplo 1. Medir y mostrar el número

1. **Problema.** Ver la temperatura sin el PC.
2. **Objetivo.** Leer el sensor elegido y sacar el número por USART2 y, si la pantalla está, una franja o un texto mínimo.
3. **Material.** El sensor y, si ya funciona, la OLED del módulo 13.
4. **Funcionamiento.** Un paso cada 500 ms. La fórmula es la del módulo del sensor, no una media de las dos. La pantalla, si no tienes fuente de texto, puede mostrar la franja del módulo 13 como «vivo» y el número queda en el UART. Escribir dígitos en el SSD1306 es una ampliación: un mapa de 8×8 por dígito basta, y no se incluye aquí una fuente entera.
5. **Dibujo.** [TMP36](img/cable-tmp36-pb0.svg) o [I2C](img/cable-i2c-pb8-pb9.svg), el que corresponda. No los dos sensores a la vez salvo que documentes cuál manda.
6. **Cableado.** El del módulo que elegiste. 3,3 V. GND común en el lado de la placa.
7. **Cálculos.** Los de la hoja. Umbral todavía no.
8. **CubeMX.** ADC3 en PB0 o I2C1 en PB8/PB9, USART2, PC7 salida.
9. **Código.** Reúne `leer` del módulo 11 o `leer_mcp9808` del módulo 13. Imprime `T` cada medio segundo con `HAL_GetTick`. No bloquees 500 ms si más adelante la alarma tiene que ser ágil: espera con el tick.
10. **Dónde.** `main.c` o `temperatura.c` incluido en CMake, como en el módulo 17.
11. **Compilar y probar.** Compara con un termómetro de la sala.
12. **Esperado, no medido.** Un valor cercano a la sala. Anótalo en `PRUEBAS.md` como medida tuya.
13. **Fallos.** Los de los módulos 11 y 13. Pantalla negra con UART correcto: la alarma de datos puede esperar; no subas la alimentación de la OLED a 5 V para «arreglarla».
14. **Variación.** Media de 8 muestras del módulo 19 si la lectura salta. El retraso de esa media se anota.
15. **Criterio.** Sabes qué hoja justifica el número que imprimes.

## Ejemplo 2. Umbral con estados

1. **Problema.** Un LED que sigue a cada cuenta es un parpadeo, no una alarma.
2. **Objetivo.** Reposo, prealarma y alarma, como en el módulo 17. El umbral de fábrica es 30 °C. Dos segundos por encima pasan a alarma y encienden PC7.
3. **Material.** El del ejemplo 1. Puedes subir la temperatura con el dedo. No uses un soldador ni una llama.
4. **Funcionamiento.** `fuera` es «la temperatura es mayor que el umbral». El resto de la máquina no cambia.
5. **Dibujo.** LED en PC7: [cable-led-pc7.svg](img/cable-led-pc7.svg).
6. **Cableado.** El LED con su resistencia. PC7 no es el sensor.
7. **Cálculos.** 30 °C y 2000 ms son de diseño de esta práctica. Cámbialos en un solo sitio, una constante.
8. **CubeMX.** Sin pines nuevos.
9. **Código.** `alarma_paso` del módulo 17, con `fuera` calculado desde la temperatura en décimas para no comparar flotantes a ciegas: `fuera = (decimas > 300) ? 1U : 0U` si la unidad es décimas de grado. Ajusta la escala a la función que ya tengas y documéntala.
10. **Dónde.** `alarma.c` y la lectura en otro archivo, o los dos pasos en `main` si aún no partes el proyecto.
11. **Compilar y probar.** Por debajo del umbral, PC7 apagado. Mantén el sensor por encima dos segundos: PC7 encendido. Al bajar, se apaga al volver a reposo.
12. **Esperado, no medido.** Ese comportamiento. El tiempo se puede contar con el reloj de pared. Anótalo.
13. **Fallos.** Enciende al instante: no estás en prealarma. No apaga: la transición de vuelta no mira `fuera`. Umbral en otra unidad: 30 cuentas de ADC no son 30 °C.
14. **Variación.** Histéresis de 1 °C: se entra a 30 y se sale a 29, para no oscilar. Es un estado más, o una comparación distinta según el estado actual.
15. **Criterio.** PC7 solo está encendido en el estado de alarma.

## Ejemplo 3. Umbral que se guarda

1. **Problema.** Al quitar el USB, el umbral vuelve al 30 de fábrica aunque lo hubieras cambiado.
2. **Objetivo.** `+`, `-` y `g` del módulo 24, aplicados al umbral en décimas o en grados enteros.
3. **Material.** El monitor serie.
4. **Funcionamiento.** La RAM tiene el umbral de trabajo. `g` lo escribe en la última página. Al arrancar, si la marca es válida y el valor está entre 0 y 80 °C, se usa. Si no, 30 °C. El límite 0 a 80 es de esta práctica, para rechazar una Flash corrupta.
5. **Dibujo.** No hay cable nuevo.
6. **Cableado.** No hay.
7. **Cálculos.** Fábrica 30. Rango 0 a 80. Dirección `PARAM_ADDR` del módulo 24.
8. **CubeMX.** Sin cambios. No actives una protección de la Flash.
9. **Código.** `flash_leer` y `flash_guardar`, y el parser de un carácter. El paso de la alarma usa la variable, no la constante.
10. **Dónde.** `main.c`, USER CODE.
11. **Compilar y probar.** Cambia el umbral, no pulses `g`, quita el USB: vuelve a 30 o al último guardado. Pulsa `g`, quita el USB: vuelve el nuevo, si estaba en rango.
12. **Esperado, no medido.** Lo que anotes en la tabla del módulo 28.
13. **Fallos.** Los del módulo 24, más un umbral de 30 cuentas interpretado como grados. Imprime la unidad en el texto.
14. **Variación.** La pantalla muestra el umbral además de la medida, si ya tienes dígitos. Si no, el UART basta.
15. **Criterio.** La alarma y la memoria no se pisan el pin, y el informe dice la exactitud que no tienes.

## Pruebas mínimas

| Id | Estímulo | Esperado por diseño |
| --- | --- | --- |
| T1 | Sensor a temperatura de la sala | Texto cercano al termómetro de la sala. La diferencia se anota, no se tapa |
| T2 | Dedo sobre el sensor | El número sube |
| T3 | Por debajo del umbral | PC7 apagado |
| T4 | Por encima, menos de 2 s | PC7 apagado |
| T5 | Por encima, más de 2 s | PC7 encendido |
| T6 | `g` y quitar USB | El umbral se conserva |
| T7 | Valor fuera de 0 a 80 en la Flash | Se usa 30 |
| T8 | Pantalla, si está montada | Sigue a 3,3 V y no bloquea el UART |

## Qué no demuestra

No hay calibración, no hay registro continuo, no hay caja y no hay una exactitud mejor que la de la hoja. El módulo 28 pide escribirlo así.
