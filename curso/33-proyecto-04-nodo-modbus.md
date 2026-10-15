# Proyecto P4. Nodo de adquisición

Varias medidas por el ADC, con DMA si el módulo 15 está en el proyecto, parámetros en la Flash y publicación por Modbus RTU. El maestro es la segunda estación del módulo 21. El nodo no incluye Ethernet ni Wi-Fi: esta placa no los tiene.

**No comprobado en hardware.**

## Qué reúne

Módulos 15, 21 y 24. El módulo 28 es la tabla de pruebas del nodo.

## Material

- Potenciómetro en PA0, como canal 0.
- Una segunda tensión de 0 a 3,3 V en PA1, canal 1. Puede ser otro potenciómetro o el divisor ya limitado.
- Transceptor RS-485 de 3,3 V, DE en PC6, USART1 en PA9 y PA10. El ESP32 desconectado.
- USART2 como consola local.
- El maestro Modbus del módulo 21.

## Pines

| Función | Pin |
| --- | --- |
| Canal 0 | PA0 |
| Canal 1 | PA1 |
| RS-485 | PA9, PA10, PC6 |
| Consola | USART2 |
| Parámetros | Flash, sin pin |

PA9 y PA10 no llevan el ESP32 a la vez. PA0 no lleva el 4–20 mA a la vez que el potenciómetro.

## Mapa de registros

Decisión de este proyecto, no de la especificación Modbus:

| Registro | Acceso | Contenido |
| --- | --- | --- |
| 0 | Lectura | Media de 8 muestras de PA0, en cuentas de 0 a 4095 |
| 1 | Lectura | Media de 8 muestras de PA1 |
| 2 | Lectura y escritura | Umbral de PA0, de 0 a 4095. De fábrica 2000. Se guarda en Flash solo con la función de escritura, no en cada muestra |
| 3 | Lectura | 1 si la media de PA0 supera el umbral, 0 si no |

Escribir un umbral mayor que 4095 se rechaza con excepción, como el 1001 del módulo 21.

## Ejemplo 1. Dos canales y la media

1. **Problema.** Tener las dos medidas antes de hablar con el maestro.
2. **Objetivo.** Llenar dos medias de 8 muestras y imprimirlas por USART2.
3. **Material.** Los dos potenciómetros o el que tengas en PA0 y una tensión limitada en PA1.
4. **Funcionamiento.** Un solo ADC, dos canales en secuencia, o dos lecturas por encuesta una detrás de otra. El DMA del módulo 15 se usa si dejas un solo canal en el bloque; con dos canales, la encuesta es más clara y el DMA puede quedar para el canal 0 en un segundo paso. No actives el modo dual intercalado (ES0261). Periodo 20 ms.
5. **Dibujo.** [PA0](img/cable-potenciometro-pa0.svg). PA1 con el mismo tipo de potenciómetro a 3,3 V, en CN8 pin 2.
6. **Cableado.** Extremos a 3,3 V y GND. Cursores a A0 y A1. Pins TTa.
7. **Cálculos.** Media de 8, como en el módulo 19. Retraso de unas 4 muestras, que a 20 ms son unos 80 ms. Se dice en el informe.
8. **CubeMX.** ADC1 con los dos canales en scan, o dos configuraciones que cambies en código. Lo que tu versión genere con menos sorpresas: encuesta de PA0 y luego de PA1. USART2.
9. **Código.** Dos ventanas del módulo 19. Imprime `c0` y `c1` cada 200 ms.
10. **Dónde.** `main.c`.
11. **Compilar y probar.** Mueve cada potenciómetro y comprueba que la columna correcta cambia.
12. **Esperado, no medido.** Los canales no se cruzan. Si se cruzan, el orden de muestreo no es el que crees.
13. **Fallos.** Siempre el mismo valor en los dos: los dos cursores están en el mismo pin, o el ADC no cambia de canal. Revisa la configuración de rango y de canal en el HAL, que en esta familia pide `HAL_ADC_ConfigChannel` antes de cada conversión si no estás en scan.
14. **Variación.** DMA en PA0 únicamente, como en el módulo 15, y PA1 por encuesta. El LED de PA5 puede parpadear para repetir el criterio de que el bucle vive.
15. **Criterio.** Puedes señalar qué registro será cada canal.

## Ejemplo 2. Publicar por Modbus

1. **Problema.** El PC de la consola no es el maestro de campo.
2. **Objetivo.** El maestro lee los registros 0 y 1, y ve las medias.
3. **Material.** El transceptor y el maestro del módulo 21. 120 Ω en los dos extremos.
4. **Funcionamiento.** El parser del módulo 21, ampliado a dos registros de lectura. La consola sigue en USART2. DE en PC6 se pone a 1 solo durante la respuesta.
5. **Dibujo.** [RS-485](img/cable-rs485.svg).
6. **Cableado.** El del módulo 21. Transceptor de 3,3 V. Sin MAX485 a 5 V en el pin.
7. **Cálculos.** Función 0x03, esclavo 1, registros 0 y 1. CRC con la misma función ya comprobada.
8. **CubeMX.** USART1 y PC6, además del ADC.
9. **Código.** Al armar la respuesta de un registro, el valor es la media de 16 bits, byte alto primero. No envíes el float. No actualices la Flash aquí.
10. **Dónde.** El parser, en `modbus.c` si lo sacaste del `main`, con las medias en variables `volatile` si un día las escribe una interrupción. En encuesta, el bucle puede escribirlas él mismo.
11. **Compilar y probar.** Lee desde el maestro mientras giras PA0. USART2 puede imprimir lo mismo para comparar.
12. **Esperado, no medido.** El maestro y la consola se parecen, con el retraso de la media y el del maestro. Anota la diferencia, no la tapes.
13. **Fallos.** Los del módulo 21: A/B, DE, velocidad, CRC. El ESP32 sigue pinchado: quítalo. El maestro lee 40001 y tu código contesta solo a la dirección 0: documenta la numeración.
14. **Variación.** Una sola petición de dos registros (`cantidad = 2`) y una respuesta con cuatro bytes de datos. El byte count es 4.
15. **Criterio.** El maestro ve los dos canales sin usar el COM virtual como bus de campo.

## Ejemplo 3. El umbral se escribe y se guarda

1. **Problema.** El umbral no puede volver a 2000 cada vez que se va la luz, ni escribirse en cada muestra.
2. **Objetivo.** La función 0x06 sobre el registro 2 guarda en RAM y en Flash si el valor es de 0 a 4095. El registro 3 refleja la comparación. Al arrancar, el umbral sale de la Flash o vale 2000.
3. **Material.** El mismo bus.
4. **Funcionamiento.** `flash_guardar` del módulo 24, llamado solo desde el tratamiento de la escritura válida, no desde el muestreo. Si la marca no es válida, umbral 2000. Registro 3: 1 cuando `media0 > umbral`.
5. **Dibujo.** No hay cable nuevo.
6. **Cableado.** El mismo.
7. **Cálculos.** Fábrica 2000. Máximo 4095. Una escritura de 4096 es excepción 0x03 y no toca la Flash.
8. **CubeMX.** Sin pines nuevos. La Flash no se protege de lectura.
9. **Código.** El parser llama a `flash_guardar` y, si devuelve −1, responde excepción 0x04 (fallo del esclavo) y no da por escrito el valor. Si la Flash se escribió, el eco de la función 0x06 es la respuesta normal.
10. **Dónde.** Parser y funciones de Flash en USER CODE o en archivos incluidos por CMake.
11. **Compilar y probar.** Escribe 1000, lee el registro 2, quita el USB, vuelve, lee otra vez. Escribe 5000 y comprueba que sigue 1000. Pon PA0 por encima y por debajo, y lee el registro 3.
12. **Esperado, no medido.** El umbral sobrevive. El ilegal no. El registro 3 cambia con el potenciómetro. Anótalo en `PRUEBAS.md`.
13. **Fallos.** La Flash se escribe en cada muestra: el módulo 24 ya explicó por qué no. Una excepción que no sale al bus: DE no envuelve esa respuesta. Dirección de página que pisa el programa: el nodo no arranca. Recupera y revisa `PARAM_ADDR`.
14. **Variación.** La consola local también puede cambiar el umbral con `g`, pero entonces hay dos dueños. Elige uno: o el maestro, o la consola. Este proyecto elige el maestro. La consola solo lee.
15. **Criterio.** Un solo camino escribe la Flash, el rango se rechaza y no hay ningún chip de red en el montaje.

## Pruebas mínimas

| Id | Estímulo | Esperado por diseño |
| --- | --- | --- |
| T1 | Mover solo PA0 | Cambia el registro 0, no el 1 |
| T2 | Mover solo PA1 | Cambia el registro 1, no el 0 |
| T3 | Leer 0x03 desde el maestro | Los valores se parecen a la consola |
| T4 | Escribir umbral 1000 y quitar USB | Al volver, el registro 2 vale 1000 |
| T5 | Escribir 5000 | Excepción, el umbral no cambia |
| T6 | PA0 por encima del umbral | Registro 3 igual a 1 |
| T7 | PA0 por debajo | Registro 3 igual a 0 |
| T8 | Mirar el montaje | No hay ESP32 en PA9/PA10 ni módulo de Ethernet |

## Qué no demuestra

No hay red Ethernet, no hay Wi-Fi y no hay un SCADA. Hay un esclavo Modbus de cuatro registros en una mesa, con la Flash escrita solo al pedirla.
