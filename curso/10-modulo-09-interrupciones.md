# Módulo 9. Interrupciones y prioridades

Preguntar en cada vuelta del bucle si el pulsador cambió funciona, y es lo que hiciste en el módulo 8. Una interrupción es el aviso que llega en el momento del flanco, aunque el programa vaya por otra línea. La rutina que atiende ese aviso tiene que ser corta.

**No comprobado en hardware.**

## Objetivos

- Atender B1 por una interrupción externa, con antirrebote fuera de un retardo largo.
- Ver que una prioridad decide quién espera cuando coinciden el pulsador y el UART.
- Comprobar que dos flancos más rápidos que el filtro no cuentan dos veces.

## Prerrequisitos

Módulos 7 y 8. El pulsador de la placa, B1, y el monitor serie.

## La idea, antes del NVIC

**Analogía.** El bucle del módulo 8 es mirar el teléfono cada cierto tiempo por si alguien llamó. La interrupción es el timbre: dejas un momento lo que tenías en la mano, apuntas quién llamó y vuelves. Si te quedas hablando media hora en el pasillo, el trabajo de la mesa no avanza. Por eso dentro de la interrupción no se pone un `HAL_Delay` largo.

**Técnico.** Una línea GPIO puede pedir una interrupción al flanco. En este chip, PC13 entra por la línea EXTI13 y comparte el canal de interrupción EXTI15_10. El NVIC es quien ordena las peticiones del núcleo. Un número de prioridad más bajo se atiende antes. Los nombres exactos de la prioridad los ves en la pestaña NVIC de CubeMX; no los copies de otro STM32.

ES0261 Rev 5, de diciembre de 2018, aplica al silicio Y de esta familia. Antes de usar este módulo para despertar de un modo de bajo consumo, abre la sección de sistema de esa errata. El ejemplo de aquí no entra en Sleep ni en Stop: eso es el módulo 25. Si tu revisión de ES0261 describe un límite al despertar por EXTI, anótalo en el margen y no des por bueno un consumo de sueño que esta lección no mide.

## Ejemplo 1. B1 por interrupción

1. **Problema.** El flanco no debe esperar a que el bucle acabe un trabajo largo.
2. **Objetivo.** Cada pulsación aceptada de B1 conmuta LD2, y la interrupción solo anota el evento.
3. **Material.** La placa. PC13 no se cablea fuera.
4. **Funcionamiento.** CubeMX activa EXTI en el flanco de bajada de PC13. La función `HAL_GPIO_EXTI_Callback` pone un aviso si han pasado al menos 20 ms desde el último aviso aceptado. El bucle, fuera de la interrupción, mira el aviso y conmuta PA5. El filtro no es un `HAL_Delay` dentro de la callback.
5. **Dibujo.** No hay cableado externo.
6. **Cableado.** B1 interno, SB17 cerrado. PA5 es LD2.

| Señal | Papel |
| --- | --- |
| PC13 | EXTI, flanco a nivel bajo |
| PA5 | LED, se toca en el bucle, no en la callback |

7. **Cálculos.** 20 ms es la misma convención de antirrebote del módulo 5.
8. **CubeMX.** PC13 como `GPIO_EXTI13`, flanco de bajada, pull-up. NVIC: habilita EXTI line[15:10]. PA5 salida. Genera.
9. **Código.**

```c
/* USER CODE BEGIN PV */
static volatile uint8_t aviso_b1;
static volatile uint32_t ultimo_b1;
/* USER CODE END PV */
```

```c
/* USER CODE BEGIN 0 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
  if (GPIO_Pin == GPIO_PIN_13)
  {
    uint32_t ahora = HAL_GetTick();
    if ((ahora - ultimo_b1) >= 20U)
    {
      ultimo_b1 = ahora;
      aviso_b1 = 1U;
    }
  }
}
/* USER CODE END 0 */
```

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  if (aviso_b1)
  {
    aviso_b1 = 0U;
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
  }
  /* USER CODE END WHILE */
```

Si CubeMX ya generó `HAL_GPIO_EXTI_Callback` en `stm32f3xx_it.c`, no crees una segunda. Escribe el cuerpo en el USER CODE de esa función, o deja una sola definición en `USER CODE BEGIN 0` y no dupliques el símbolo. Un error de «multiple definition» significa que hay dos.

10. **Dónde.** `main.c` si la callback no existe todavía. Si existe en el archivo de interrupciones, el cuerpo va allí, en su USER CODE, y las variables siguen en `main.c` con un `extern` en el otro archivo, dentro de USER CODE.
11. **Compilar y probar.** Graba, pulsa B1, observa LD2.
12. **Esperado, no medido.** Una pulsación, un cambio de LD2. Mantener el dedo no repite el cambio: el flanco de bajada ya pasó. El rebote corto no cuenta gracias a los 20 ms.
13. **Fallos.** No ocurre nada: NVIC sin habilitar, o el flanco elegido es el de subida y sueltas demasiado rápido para notarlo. Cuenta dos: baja el trabajo del bucle y confirma que `ultimo_b1` es `volatile`. El enlace no compila: callback duplicada.
14. **Variación.** Cambia el flanco a subida y comprueba que LD2 cambia al soltar. Vuelve a bajada para el resto del módulo.
15. **Criterio.** La callback no llama a `HAL_Delay` ni a `HAL_UART_Transmit`.

## Ejemplo 2. La tecla y el UART, con prioridad

1. **Problema.** Si la rutina del UART fuera lenta, el pulsador tendría que esperar, o al revés.
2. **Objetivo.** Dejar la interrupción del UART más prioritaria que la de EXTI y ver el orden en el monitor.
3. **Material.** Monitor serie a 115200 8N1. B1.
4. **Funcionamiento.** USART2 en interrupción recibe un byte y anota un carácter. EXTI anota el pulsador. El bucle imprime qué aviso llegó. La prioridad se ve en CubeMX: un valor numérico menor se atiende primero. Para el ensayo, pon USART2 más prioritario que EXTI15_10.
5. **Dibujo.** No hay cableado nuevo.
6. **Cableado.** USART2 por el ST-LINK. PC13 es B1.
7. **Cálculos.** No hay tiempos nuevos. El ensayo no mide microsegundos de latencia.
8. **CubeMX.** USART2 con interrupción global habilitada en NVIC. En NVIC, la prioridad de USART2 más alta que la de EXTI (número más bajo). Anota los dos números que te muestre tu versión de CubeMX.
9. **Código.** Además del ejemplo 1:

```c
/* USER CODE BEGIN PV */
static volatile uint8_t aviso_uart;
static volatile uint8_t letra_uart;
/* USER CODE END PV */
```

```c
/* USER CODE BEGIN 0 */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
  if (huart == &huart2)
  {
    aviso_uart = 1U;
  }
}
/* USER CODE END 0 */
```

```c
/* USER CODE BEGIN 2 */
HAL_UART_Receive_IT(&huart2, (uint8_t *)&letra_uart, 1U);
/* USER CODE END 2 */
```

En el bucle, si `aviso_uart` está a 1, transmite la línea `uart\r\n`, lo pone a 0 y vuelve a llamar a `HAL_UART_Receive_IT`. Si `aviso_b1` está a 1, transmite `boton\r\n` y conmuta LD2. `letra_uart` tiene que ser `volatile` y del tamaño de un byte; el cast del listado anterior exige que la variable sea `uint8_t`. Declárala `static volatile uint8_t letra_uart;`.

10. **Dónde.** La callback de UART, igual que la de EXTI: una sola definición, en el USER CODE que CubeMX haya dejado.
11. **Compilar y probar.** Escribe una letra en el monitor y pulsa B1, varias veces, también casi a la vez.
12. **Esperado, no medido.** Aparecen las dos palabras. Con la prioridad del UART por delante, una recepción no se queda detrás de la callback del botón, porque la del botón solo pone un aviso. Este ensayo no demuestra la prioridad si las dos callbacks son igual de cortas: la prioridad se ve cuando alargas a propósito la del botón. No la alargues con `HAL_Delay`. Si quieres verla, pon en la callback del botón un bucle vacío contado, de ensayo, y quítalo al acabar. Anota lo que observes.
13. **Fallos.** Solo llega un carácter: falta volver a armar `HAL_UART_Receive_IT` después de cada byte. Texto mezclado: estás transmitiendo desde las dos callbacks. Transmite solo en el bucle.
14. **Variación.** Invierte las prioridades en CubeMX, regenera y repite el ensayo. Anota los números.
15. **Criterio.** Puedes señalar qué interrupción tiene el número menor y qué trabajo no está dentro de la callback.

## Ejemplo 3. Dos flancos más rápidos que el filtro

1. **Problema.** Un rebote o dos clics muy seguidos no deben contar como dos órdenes.
2. **Objetivo.** Demostrar que un segundo flanco antes de 20 ms no incrementa el contador.
3. **Material.** B1. Para un flanco repetible, puedes puentear un momento PC13 a GND con un cable, dos veces seguidas. Hazlo solo a GND de la placa, nunca a 5 V. PC13 es tipo TC: no admite 5 V.
4. **Funcionamiento.** El contador solo sube cuando la callback acepta el flanco. La propia callback rechaza el que llega antes de 20 ms.
5. **Dibujo.** Si usas cable: CN7 pin 23 (PC13) a CN6 pin 6 (GND), un toque breve. Mejor usar el dedo en B1 si no quieres un cable en el Morpho.
6. **Cableado.** Preferible B1, sin cable. Si puenteas, solo a GND y solo un instante.
7. **Cálculos.** 20 ms de filtro. Dos toques separados menos de eso deben dejar el contador en 1.
8. **CubeMX.** El del ejemplo 1.
9. **Código.** En el bucle, donde se atiende `aviso_b1`, incrementa `pulsaciones` y transmite el valor:

```c
/* USER CODE BEGIN PV */
static volatile uint32_t pulsaciones;
/* USER CODE END PV */
```

```c
if (aviso_b1)
{
  aviso_b1 = 0U;
  pulsaciones++;
  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
}
```

Mira `pulsaciones` con un punto de ruptura, o imprime el número por USART2 como en el módulo 8.

10. **Dónde.** Junto al aviso del ejemplo 1.
11. **Compilar y probar.** Un pulso limpio: el contador sube 1. Dos toques muy rápidos, casi un rebote: sigue subiendo solo 1. Dos toques separados por más de medio segundo: sube 2.
12. **Esperado, no medido.** El filtro rechaza el segundo flanco cercano. No hay un generador calibrado en este texto; el criterio es el que tú observes con el depurador.
13. **Fallos.** Siempre suma 2: `ultimo_b1` no se actualiza, o no es `volatile`. No suma: el flanco de CubeMX no es el de bajada, o NVIC está deshabilitado.
14. **Variación.** Sube el filtro a 200 ms. Hace falta separar más los clics. Es el mismo programa.
15. **Criterio.** Puedes explicar por qué la cuenta no sigue el número de rebotes del contacto.

## Resumen

La interrupción anota y vuelve. El bucle hace el trabajo lento. La prioridad es un número del NVIC. El antirrebote no es un retardo dentro de la callback.

## Glosario

| Término | Definición |
| --- | --- |
| Interrupción | Aviso que desvía el programa un momento |
| EXTI | Línea que convierte un flanco de un pin en ese aviso |
| NVIC | El árbitro de prioridades del Cortex-M4 |
| Callback | La función del HAL que se ejecuta al atender el aviso |
| Prioridad | Quién pasa delante. En este núcleo, el número menor va antes |

## Preguntas

**1.** ¿Por qué no transmites el UART dentro de la callback?

Respuesta. Porque esa rutina debe terminar pronto. Transmitir espera, y bloquea a quien tenga menos prioridad.

**2.** ¿`volatile` en `aviso_b1` es decoración?

Respuesta. No. El bucle y la interrupción comparten la variable. Sin `volatile`, el compilador puede no volver a leerla.

**3.** ¿Este módulo demuestra el despertar desde Stop?

Respuesta. No. ES0261 se consulta antes de afirmar eso, y el ensayo es el módulo 25.

## Lista de comprobación

- [ ] La callback de B1 no tiene `HAL_Delay`.
- [ ] He anotado las dos prioridades del NVIC.
- [ ] Un segundo flanco dentro del filtro no incrementa la cuenta.
- [ ] He quitado cualquier bucle de ensayo que hubiera metido en la callback.

## Siguiente

[Módulo 10](11-modulo-10-pwm.md): variar el brillo y mandar una carga con un transistor.
