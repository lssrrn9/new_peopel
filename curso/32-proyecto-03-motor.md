# Proyecto P3. Monitor de motor

Cuenta de pulsos o encoder a RPM, una entrada analógica de 0 a 3,3 V que representa una corriente mediante un sensor de laboratorio, y alarmas por el puerto serie. El motor, si se usa el del módulo 10, es el servo educativo o un motor pequeño con driver externo. No se supervisa un motor de red.

**No comprobado en hardware.**

## Qué reúne

Módulos 7, 11 y 16. El servo del módulo 10 es opcional y no es el motor vigilado: es una carga de juguete aparte. No lo alimentes desde un pin.

## Material

- Encoder de 3,3 V en PB6 y PB7, o el contador de pulsos del módulo 16 si no hay encoder.
- Una tensión de 0 a 3,3 V en PA1 que represente la corriente. Puede ser el potenciómetro, y entonces el informe dice «corriente simulada». Si tienes un sensor de corriente de laboratorio cuya salida quepa en 0 a 3,3 V, usa su hoja y no la escala del potenciómetro.
- USART2 para las alarmas.
- Opcional: servo en PB10, con 5 V externos, solo como actuador de demostración. No es el eje que el encoder mide, salvo que mecánicamente lo acoples y lo escribas.

## Pines

| Función | Pin |
| --- | --- |
| Encoder A | PB6, D10, TIM4_CH1 |
| Encoder B | PB7, CN7 pin 21, TIM4_CH2 |
| Corriente simulada o sensor | PA1, A1, TTa |
| Alarma luminosa | PA5, LD2, o PC7 si quieres un LED propio |
| Texto | USART2 |
| Servo opcional | PB10, señal nada más |

PB6 no es el NSS del SPI. PA1 no es el 0–10 V del módulo 27 a la vez.

## Ejemplo 1. RPM y una alarma de velocidad

1. **Problema.** Ver la velocidad y un aviso si se pasa de un tope.
2. **Objetivo.** Imprimir RPM cada segundo y encender LD2 si se superan 100 RPM de diseño.
3. **Material.** El encoder o el pulsador de cuentas, con N escrito.
4. **Funcionamiento.** La fórmula del módulo 16. Umbral 100 RPM, de juguete. LD2 se enciende por encima y se apaga por debajo de 90, para no parpadear en el borde.
5. **Dibujo.** [Encoder](img/cable-encoder-pb6-pb7.svg).
6. **Cableado.** El del módulo 16. 3,3 V. Pull-up solo si la salida es abierta.
7. **Cálculos.** `RPM = delta * 60 / marcas_por_vuelta` en una ventana de 1 s. 100 RPM y 90 RPM son el umbral y la histéresis. N sale de la hoja.
8. **CubeMX.** TIM4 encoder. PA5 salida. USART2.
9. **Código.** El bucle de ventana del módulo 16, más:

```c
if (rpm > 100U) { HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET); }
if (rpm < 90U) { HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET); }
```

10. **Dónde.** `main.c`.
11. **Compilar y probar.** Gira despacio y más deprisa. Mira el texto y LD2.
12. **Esperado, no medido.** LD2 sigue el umbral. La RPM es coherente con N y con lo que haces a ojo. No hay tacómetro patrón en el texto.
13. **Fallos.** RPM enormes: N = 1 con un encoder de muchas marcas, o rebotes. LD2 no se apaga: falta la histéresis y el ruido cruza 100. Encoder de 24 V: no se conecta.
14. **Variación.** Imprime también el sentido, si usas la cuadratura.
15. **Criterio.** El informe dice N, la ventana y el umbral.

## Ejemplo 2. La entrada que representa la corriente

1. **Problema.** Añadir una segunda magnitud sin llamarla corriente de un motor de red.
2. **Objetivo.** Leer PA1 y imprimir «corriente simulada» en una escala que tú declares.
3. **Material.** Potenciómetro de 10 kΩ entre 3,3 V y GND, cursor a PA1. Declara: 0 V representa 0 A y 3,3 V representa 5 A de un motor de juguete que no está ahí. Es una escala de pantalla, no un shunt.
4. **Funcionamiento.** `cents = mv * 500 / 3300` son centésimas de amperio si 3,3 V son 5,00 A. Imprímelo con esa unidad en el texto: `sim 1.25 A`. Alarma si pasa de 4,00 A de esa escala, otro mensaje, sin apagar un motor que no existe.
5. **Dibujo.** El del divisor no hace falta si es un potenciómetro: mismo esquema que PA0, pero en CN8 pin 2.
6. **Cableado.** CN6 pin 4, CN6 pin 6, CN8 pin 2. Nada de shunt en un cable de red.
7. **Cálculos.** 4,00 A de escala son 4/5 * 3,3 V = 2,64 V, N ≈ 2,64/3,3*4096 ≈ 3277. Por debajo de 3,50 A (histéresis) se retira el aviso.
8. **CubeMX.** ADC en PA1. Puede ser el mismo ADC1 si no choca con otro canal, leyendo en la ventana de un segundo o cada 20 ms.
9. **Código.** Una función `leer_pa1` como la del módulo 11. No uses la fórmula del TMP36.
10. **Dónde.** El mismo bucle que ya imprime RPM, para que las dos líneas salgan juntas cada segundo.
11. **Compilar y probar.** Gira el potenciómetro. El texto cambia. LD2 de velocidad no tiene por qué seguir a este potenciómetro.
12. **Esperado, no medido.** 0 V cerca de 0 A de escala y 3,3 V cerca de 5 A de escala. Mide el pin si quieres comprobar el ADC. La corriente de un motor no se ha medido.
13. **Fallos.** Llamar al valor «corriente del motor» en el informe. Corrígelo. Pin por encima de 3,3 V: el potenciómetro está a 5 V. Páralo.
14. **Variación.** Si el sensor es real y de 3,3 V, sustituye la escala por la de su hoja y cambia el rótulo del texto.
15. **Criterio.** El rótulo dice «simulada» mientras el sensor no esté.

## Ejemplo 3. Las dos alarmas, y el servo aparte

1. **Problema.** No mezclar el actuador con la medida.
2. **Objetivo.** Si hay alarma de velocidad o de escala de corriente, el texto lo dice. El servo, si está montado, se queda en su posición media y no se usa como «el motor vigilado» salvo que el encoder esté en su eje y lo escribas.
3. **Material.** Opcional, el servo del módulo 10.
4. **Funcionamiento.** Una función `alarma_texto` imprime `vel`, `sim` o `ok`. El servo recibe el pulso de 1,5 ms y no cambia en este proyecto. Así se ve que la señal de PB10 no es la medida.
5. **Dibujo.** [Servo](img/cable-servo-educativo.svg), solo si lo montas. 5 V externos.
6. **Cableado.** El del módulo 10 para el servo. GND común. Señal en PB10.
7. **Cálculos.** Pulso medio del módulo 10: 750 cuentas con el prescaler que ya calculaste. No lo recalcules distinto sin decirlo.
8. **CubeMX.** TIM2 canal 3 en PB10, además de TIM4. Comprueba que los dos timers caben en el proyecto. TIM3 no hace falta si el LED de alarma es PA5 por GPIO.
9. **Código.** `HAL_TIM_PWM_Start` y un compare fijo. Las alarmas no escriben ese compare.
10. **Dónde.** `main.c`.
11. **Compilar y probar.** Provoca cada alarma por separado y las dos juntas. El servo no debe moverse.
12. **Esperado, no medido.** El texto distingue las causas. El servo quieto demuestra que no está en el lazo.
13. **Fallos.** El servo se alimenta del 3,3 V y la placa se cae. Pásalo a la fuente externa. El encoder cuenta el ruido del servo: sepáralos físicamente y, si el encoder no está acoplado, dilo.
14. **Variación.** Quita el servo del todo. El monitor de RPM y de escala sigue siendo el proyecto.
15. **Criterio.** El informe no habla de un motor de red ni de un variador.

## Pruebas mínimas

| Id | Estímulo | Esperado por diseño |
| --- | --- | --- |
| T1 | Eje parado | RPM 0, LD2 apagado |
| T2 | Giro por encima de 100 RPM, con tu N | LD2 encendido y texto de velocidad |
| T3 | Bajar de 90 RPM | LD2 apagado |
| T4 | PA1 a 0 V | Escala cerca de 0, rótulo «simulada» si es potenciómetro |
| T5 | PA1 cerca de 3,3 V | Escala cerca de 5 A de la convención, aviso por encima de 4 |
| T6 | Las dos a la vez | El texto cita las dos causas |
| T7 | Servo, si está | Quieto en el pulso medio, 5 V externos |
| T8 | Inspección | No hay motor de red |

## Qué no demuestra

No hay par, no hay corriente real de un devanado y no hay protección de una máquina. El encoder de 24 V y el variador quedan fuera.
