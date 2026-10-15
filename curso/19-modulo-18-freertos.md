# Módulo 18. FreeRTOS

Hasta aquí un solo bucle llama a todos los pasos. Una tarea es un bucle con vida propia. El sistema operativo les reparte el procesador. Una cola pasa un aviso de una tarea a otra. Un semáforo evita que dos tareas hablen a la vez por el mismo UART.

**No comprobado en hardware.** La versión del middleware es la que CubeMX descargue para tu proyecto. No se fija aquí un número de versión.

## Objetivos

- Crear dos tareas: una parpadea y otra mira el pulsador.
- Pasar el aviso del pulsador por una cola.
- Impedir que dos textos se mezclen en USART2.

## Prerrequisitos

Módulos 7 y 17. Ganas con haber visto el bucle único, para notar qué cambia.

## Qué es una tarea

**Analogía.** El bucle único es un solo operario que recorre todas las máquinas. Dos tareas son dos operarios. La cola es la bandeja donde uno deja un parte y el otro lo recoge. El semáforo del UART es el turno de palabra: si los dos hablan, el papel sale con las frases cruzadas.

**Técnico.** CubeMX puede generar CMSIS-RTOS v2. Los nombres de esa versión son `osThreadNew`, `osMessageQueueNew`, `osSemaphoreNew`, `osSemaphoreAcquire` y `osSemaphoreRelease`. La versión 1 usaba `osThreadCreate` y otros nombres. Usa los que aparezcan en el `cmsis_os.h` que tu proyecto haya generado. Si no coinciden con este listado, manda el de tu cabecera: no mezcles las dos APIs.

Anota en un comentario el nombre del paquete que CubeMX muestre, por ejemplo el componente FreeRTOS del STM32CubeF3 que haya resuelto, y su versión. «El que se descargó en esta generación» es la frase correcta si no copias el número de la pantalla.

La extensión 3.x documenta vistas de depuración para FreeRTOS. Con el programa parado puedes mirar las tareas. Sigue sin ser una watch en marcha.

El proyecto con RTOS ya no debe usar `HAL_Delay` creyendo que es la única forma de esperar: `osDelay` cede el procesador. `HAL_Delay` dentro de una tarea puede bloquear el tick si la prioridad y el SysTick no están como CubeMX los dejó. Prefiere `osDelay`.

## Ejemplo 1. Dos tareas

1. **Problema.** El parpadeo y la lectura del pulsador no tienen por qué ser el mismo bucle.
2. **Objetivo.** Una tarea conmuta LD2 cada 300 ms. Otra lee B1 y enciende o apaga el LED de PC7, si sigue montado, o solo cuenta.
3. **Material.** La placa. PC7 opcional, con su resistencia.
4. **Funcionamiento.** CubeMX crea `osThreadNew` por cada tarea que definas en el árbol. Cada función es un `for (;;)` con un `osDelay`. Ninguna vuelve.
5. **Dibujo.** No hay cable obligatorio. Si usas PC7, el del LED externo.
6. **Cableado.** PA5 interno. PC13 interno.
7. **Cálculos.** 300 ms de la tarea del LED. La otra puede despertar cada 20 ms para muestrear B1, que es el antirrebote por muestreo.
8. **CubeMX.** Middleware FreeRTOS, interfaz CMSIS-RTOS v2 si está ofrecida. Dos tareas, `led` y `boton`, ambas de prioridad normal. Reloj del sistema como lo deje el generador. No borres la tarea por defecto hasta ver que la tuya arranca: puedes dejar la tarea por defecto vacía con un `osDelay`.
9. **Código.** Dentro de la función que CubeMX haya generado para la tarea, en su USER CODE:

```c
for (;;)
{
  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
  osDelay(300);
}
```

Y en la otra:

```c
for (;;)
{
  if (HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET)
  {
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_7, GPIO_PIN_SET);
  }
  else
  {
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_7, GPIO_PIN_RESET);
  }
  osDelay(20);
}
```

Si tu cabecera es v1, el retardo se llamará como indique esa cabecera. No copies `osDelay` si no compila.

10. **Dónde.** Los archivos que CubeMX cree para las tareas, normalmente separados de `main.c`, en el USER CODE de cada una. `main` solo inicializa el núcleo y arranca el planificador, como haya generado CubeMX.
11. **Compilar y probar.** Graba. LD2 parpadea. B1 enciende el LED de PC7 mientras se mantiene, si lo montaste.
12. **Esperado, no medido.** Los dos comportamientos a la vez. Parar el depurador muestra dos tareas en la vista de RTOS, si tu versión de la extensión la tiene.
13. **Fallos.** Solo arranca una: la otra no está creada en el árbol, o su función vuelve. Nada arranca: `osKernelStart` no se ha llamado, o hay un error de heap. CubeMX suele reservar el heap en su configuración; si una creación devuelve NULL, anótalo y sube el heap en la configuración del middleware, no a ciegas en un mapa de memoria.
14. **Variación.** Cambia el periodo de LD2 a 100 ms. La tarea del botón no se recompila en espíritu: no debería cambiar su lectura.
15. **Criterio.** Puedes señalar qué `for (;;)` es de quién.

## Ejemplo 2. Una cola

1. **Problema.** La tarea del botón no debería tocar el LED si otra tarea es la dueña de ese LED.
2. **Objetivo.** El botón deja un 0 o un 1 en una cola. La tarea del LED lo aplica a PA5, además de su parpadeo o en su lugar.
3. **Material.** B1 y LD2.
4. **Funcionamiento.** `osMessageQueueNew(4, sizeof(uint32_t), NULL)` crea una bandeja de cuatro avisos. `osMessageQueuePut` deja el valor. `osMessageQueueGet` lo recoge con un tiempo de espera corto para no tapar el parpadeo, o la tarea del LED solo atiende la cola y otra tercera parpadea. Para no multiplicar tareas, la del LED mira la cola con espera 0 y luego hace `osDelay(300)` y conmuta. Verás el parpadeo y, además, puedes usar el valor para otra salida.
5. **Dibujo.** No hay.
6. **Cableado.** El de la placa.
7. **Cálculos.** Cuatro huecos en la cola. Si nadie lee, los siguientes `Put` fallan. Hay que mirar el código de retorno.
8. **CubeMX.** La cola puede crearse en el árbol o en código, en `USER CODE BEGIN 2`, antes de arrancar el núcleo. Si la creas en código, hazlo donde las tareas ya puedan ver el identificador: un `osMessageQueueId_t` global en un `.c` de usuario.
9. **Código.**

```c
static osMessageQueueId_t cola_boton;

/* tras osKernelInitialize, o donde tu main de usuario pueda, antes de las tareas */
cola_boton = osMessageQueueNew(4, sizeof(uint32_t), NULL);
```

En la tarea del botón, cuando el nivel estable cambie, `osMessageQueuePut(cola_boton, &valor, 0, 0)`. En la tarea del LED:

```c
uint32_t valor = 0U;
if (osMessageQueueGet(cola_boton, &valor, NULL, 0U) == osOK)
{
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_7, valor ? GPIO_PIN_SET : GPIO_PIN_RESET);
}
```

Los nombres `osOK` y el tipo del identificador tienen que existir en tu `cmsis_os.h`.

10. **Dónde.** Un `.c` de usuario más las tareas generadas. Si CubeMX ya crea la cola en el árbol, no la crees otra vez.
11. **Compilar y probar.** Pulsa B1. PC7 debe seguir el aviso, y LD2 debe seguir parpadeando.
12. **Esperado, no medido.** El LED de PC7 cambia por la cola, no porque la tarea del botón escriba el pin.
13. **Fallos.** `Put` falla siempre: la cola es NULL porque se creó después de arrancar, o el heap no alcanzó. PC7 no cambia y LD2 sí: la tarea del LED no mira la cola. No vuelvas a escribir PC7 desde las dos tareas.
14. **Variación.** Manda el número de pulsaciones en vez de 0 y 1, e imprímelo en el ejemplo 3.
15. **Criterio.** Un solo sitio escribe PC7.

## Ejemplo 3. El UART con turno

1. **Problema.** Dos `HAL_UART_Transmit` a la vez mezclan las letras.
2. **Objetivo.** Una función `imprimir` que toma un semáforo, transmite y lo suelta. Las dos tareas la usan.
3. **Material.** Monitor serie.
4. **Funcionamiento.** `osSemaphoreNew(1, 1, NULL)` es un turno de una ficha, y esa ficha está disponible. `osSemaphoreAcquire` espera la ficha. `osSemaphoreRelease` la devuelve. Sin la ficha, la otra tarea espera en el acquire, no en medio de un byte.
5. **Dibujo.** No hay.
6. **Cableado.** USART2 por el ST-LINK.
7. **Cálculos.** Un solo dueño. Tiempo de espera del acquire: 100 ms. Si no hay ficha, se descarta el mensaje y se cuenta el descarte. No se bloquea para siempre.
8. **CubeMX.** USART2 115200, como siempre.
9. **Código.**

```c
static osSemaphoreId_t turno_uart;

static void imprimir(const char *texto)
{
  if (osSemaphoreAcquire(turno_uart, 100U) != osOK)
  {
    return;
  }
  HAL_UART_Transmit(&huart2, (uint8_t *)texto, (uint16_t)strlen(texto), 50);
  osSemaphoreRelease(turno_uart);
}
```

Hace falta `string.h`. Crea el semáforo junto a la cola. La tarea del LED imprime `led\r\n` cada varios parpadeos. La del botón imprime `boton\r\n` al cambiar. No llames a `HAL_UART_Transmit` fuera de `imprimir`.

10. **Dónde.** El mismo `.c` de usuario, con prototipo en un `.h` si las tareas están en otros archivos.
11. **Compilar y probar.** Pulsa B1 mientras LD2 vive. Mira el monitor.
12. **Esperado, no medido.** Las palabras salen enteras, una por línea, sin letras intercaladas. Puede haber ráfagas. No hay una traza guardada.
13. **Fallos.** Sigue mezclado: una tarea transmite por su cuenta. Bloqueo total: `Acquire` sin tiempo y el `Release` no se alcanza porque el transmit se quedó. Por eso el acquire tiene 100 ms y el transmit tiene su propio timeout.
14. **Variación.** Quita el semáforo un momento, a propósito, y observa la mezcla. Vuelve a ponerlo. Ese ensayo se deshace.
15. **Criterio.** El único `HAL_UART_Transmit` del proyecto está dentro de `imprimir`.

## Resumen

Dos tareas, una cola y un turno del UART. Los nombres de función son los de la cabecera que CubeMX generó. La versión del middleware se anota desde esa generación, no de memoria.

## Glosario

| Término | Definición |
| --- | --- |
| Tarea | Un bucle que el planificador ejecuta junto a otros |
| Cola | Bandeja de avisos entre tareas |
| Semáforo | Ficha de turno para un recurso que no se puede compartir a medias |
| `osDelay` | Espera que deja correr a las demás tareas |

## Preguntas

**1.** ¿Puedo copiar `osThreadCreate` de un ejemplo viejo?

Respuesta. Solo si tu `cmsis_os.h` es el de la versión 1. Si CubeMX generó la versión 2, la función es `osThreadNew`.

**2.** ¿Por qué el semáforo no es el del semáforo de luces?

Respuesta. Es la misma palabra para otra cosa: una ficha de acceso, no un cruce.

**3.** ¿Dos tareas pueden escribir PA5?

Respuesta. No conviene. Un recurso, un dueño. El otro manda un aviso.

## Lista de comprobación

- [ ] He anotado la versión de FreeRTOS que generó CubeMX.
- [ ] El código usa la API de esa cabecera.
- [ ] La cola es el único camino desde el botón hasta el LED que no es suyo.
- [ ] El UART se transmite en un solo sitio, con el turno tomado.

## Siguiente

[Módulo 19](20-modulo-19-filtrado.md): que un pico de una sola muestra no dispare una alarma.
