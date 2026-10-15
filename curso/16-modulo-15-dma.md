# Módulo 15. DMA

El DMA copia del ADC a la memoria sin que el núcleo mueva cada muestra. El núcleo se entera cuando el bloque está listo, o cuando él decide mirarlo. Es la diferencia entre apuntar cada lectura y dejar un registrador llenando la hoja.

**No comprobado en hardware.**

## Objetivos

- Leer PA0 muestra a muestra, como referencia.
- Llenar un búfer por DMA a un ritmo elegido.
- Seguir parpadeando LD2 mientras el búfer se llena.

## Prerrequisitos

El potenciómetro del [módulo 11](12-modulo-11-adc.md) en PA0. USART2 para volcar. PA5 para el LED.

## Un solo ADC

**Analogía.** La encuesta del módulo 11 es ir al instrumento, esperar y anotar. El DMA es un ayudante que anota las siguientes N lecturas en una tabla mientras tú haces otra cosa. Si le pides un modo que la errata no soporta bien, el ayudante puede perder una línea.

**Técnico.** Se usa un solo ADC, ADC1, canal PA0, no el modo dual intercalado. ES0261 avisa de un overrun de DMA en modo dual intercalado con un solo canal, y de que la bandera de overrun puede no activarse si no se lee el dato. Esta práctica no entra en ese modo. Aun así, al terminar un bloque se mira el error del handle (`hadc1.ErrorCode`) y, si no es cero, se imprime. No se da el bloque por bueno en silencio.

El ritmo se fija con el muestreo y con un disparo periódico, o con conversiones continuas. Para poder seguir el volcado por el UART, el bloque es de 32 muestras y se pide despacio: un disparo desde TIM6 cada 10 ms, por ejemplo, deja el bloque en unos 320 ms. Es una elección de diseño para ver el texto, no la velocidad máxima del ADC. El datasheet habla de hasta 5 Msps en la familia; este ejercicio no pretende alcanzarlos.

## Ejemplo 1. Muestra a muestra

1. **Problema.** Tener la referencia lenta antes de cambiar de método.
2. **Objetivo.** Imprimir una muestra de PA0 cada 200 ms, por encuesta, como en el módulo 11.
3. **Material.** Potenciómetro de 10 kΩ entre 3,3 V y GND, cursor a PA0.
4. **Funcionamiento.** `HAL_ADC_Start`, espera, `HAL_ADC_GetValue`, `HAL_ADC_Stop`.
5. **Dibujo.** [Potenciómetro](img/cable-potenciometro-pa0.svg).
6. **Cableado.** El del módulo 11, ejemplo 1. CN8 pin 1, CN6 pin 4 y CN6 pin 6.
7. **Cálculos.** V = N * 3300 / 4096 milivoltios, con la misma convención del módulo 11.
8. **CubeMX.** ADC1 IN1, sin DMA todavía, resolución 12 bits. USART2 115200.
9. **Código.** Reutiliza `imprimir_pa0` del módulo 11, llamada cada 200 ms con `HAL_GetTick` o, en este ejemplo de referencia, con `HAL_Delay(200)`.
10. **Dónde.** `main.c`.
11. **Compilar y probar.** Gira el potenciómetro y mira el monitor.
12. **Esperado, no medido.** El número sigue al cursor. Esta es la línea de base del ejemplo 2.
13. **Fallos.** Los del módulo 11: pin, 5 V, canal equivocado.
14. **Variación.** Anota diez valores con el cursor quieto. La dispersión es el ruido de tu montaje.
15. **Criterio.** Tienes una lectura por encuesta antes de activar el DMA.

## Ejemplo 2. El mismo pin, por DMA

1. **Problema.** Copiar 32 muestras sin un `GetValue` por muestra.
2. **Objetivo.** Llenar `muestras[32]` y volcar el primer y el último valor.
3. **Material.** El mismo potenciómetro.
4. **Funcionamiento.** El ADC avisa al DMA al terminar cada conversión. El DMA escribe la siguiente posición del array. Al completar 32, una callback pone un aviso y el bucle imprime.
5. **Dibujo.** El mismo cable.
6. **Cableado.** El mismo.
7. **Cálculos.** 32 muestras cada 10 ms ocupan 320 ms. Durante ese tiempo el cursor puede moverse: el primer y el último valor no tienen por qué coincidir. Si el cursor está quieto, se parecen, dentro del ruido que anotaste.
8. **CubeMX.** ADC1 en conversión continua o disparado por TIM6 cada 10 ms. DMA en modo normal o circular, periférico a memoria, half word, incremento solo en memoria. NVIC del DMA habilitado. Si TIM6 no está en tu árbol, la conversión continua también sirve para este ejemplo: el bloque se llena a la velocidad del muestreo, que puede ser alta. En ese caso no imprimas muestra a muestra; imprime solo al acabar el bloque. Documenta cuál de los dos ritmos dejaste.
9. **Código.**

```c
/* USER CODE BEGIN PV */
static uint16_t muestras[32];
static volatile uint8_t bloque_listo;
/* USER CODE END PV */
```

```c
/* USER CODE BEGIN 0 */
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *hadc)
{
  if (hadc == &hadc1)
  {
    bloque_listo = 1U;
  }
}
/* USER CODE END 0 */
```

```c
/* USER CODE BEGIN 2 */
HAL_ADC_Start_DMA(&hadc1, (uint32_t *)muestras, 32);
/* USER CODE END 2 */
```

En el bucle, si `bloque_listo` está a 1, imprimes `muestras[0]` y `muestras[31]`, miras `hadc1.ErrorCode`, pones el aviso a 0 y, si el DMA estaba en modo normal, vuelves a llamar a `HAL_ADC_Start_DMA`. En modo circular no hace falta rearrancarlo; sí hace falta copiar el bloque antes de que se sobrescriba, o imprimir sabiendo que el búfer sigue vivo.

10. **Dónde.** La callback, una sola vez, en el archivo donde CubeMX la haya dejado o en `USER CODE BEGIN 0` si no existe. El array en `PV`.
11. **Compilar y probar.** Con el cursor quieto y luego girándolo durante el bloque.
12. **Esperado, no medido.** Quieto: los dos extremos del array se parecen. En movimiento: se separan. `ErrorCode` distinto de cero se imprime, no se ignora.
13. **Fallos.** Callback que no llega: NVIC del DMA apagado, o la conversión no está en curso. Valores siempre 0: el array no es el destino del DMA, o el ancho es word y estás mirando mal los 16 bits. Overrun: bajaste a leer demasiado tarde en modo circular, o activaste un modo dual. Vuelve a un solo ADC.
14. **Variación.** Imprime las 32 muestras en hexadecimal, una línea, para ver la forma del giro.
15. **Criterio.** No hay un `HAL_ADC_GetValue` dentro del bucle de las 32 muestras.

## Ejemplo 3. El LED no se detiene

1. **Problema.** Demostrar que el núcleo sigue haciendo otra cosa.
2. **Objetivo.** LD2 conmuta cada 200 ms de `HAL_GetTick` mientras llegan bloques.
3. **Material.** PA5 y el potenciómetro.
4. **Funcionamiento.** El bucle no espera al ADC. Mira el aviso del DMA y mira el reloj del LED. Son independientes.
5. **Dibujo.** No hay cable nuevo.
6. **Cableado.** PA5 es LD2, ya en la placa.
7. **Cálculos.** 200 ms del LED frente a 320 ms del bloque, si usaste el disparo de 10 ms. Los dos ritmos no tienen por qué coincidir.
8. **CubeMX.** El del ejemplo 2, más PA5 como salida si no lo estaba.
9. **Código.** En el mismo `while`, añade la conmutación del módulo 8:

```c
static uint32_t marca;
if ((HAL_GetTick() - marca) >= 200U)
{
  marca = HAL_GetTick();
  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
}
```

No pongas `HAL_Delay` esperando al bloque.

10. **Dónde.** El bucle, junto al tratamiento de `bloque_listo`.
11. **Compilar y probar.** Observa LD2 y el monitor a la vez. Gira el potenciómetro.
12. **Esperado, no medido.** El LED no se queda fijo mientras salen líneas de muestras. Si se queda fijo, el bucle está bloqueado en un `Receive` o en un `Delay`.
13. **Fallos.** El LED se para durante el `printf` de 32 líneas largas: el UART bloqueante frena el bucle, no el DMA. Acorta el texto al primer y último valor. El LED no arranca: PA5 no es salida en este proyecto.
14. **Variación.** Cuenta cuántos bloques llegan en diez parpadeos. Es una comprobación grosera del ritmo, no una calibración.
15. **Criterio.** Puedes señalar qué parte hace el DMA y qué parte hace el `while`.

## Resumen

La encuesta sigue siendo válida. El DMA llena la tabla. Un solo ADC, y el código de error se mira. LD2 demuestra que el bucle no espera muestra a muestra.

## Glosario

| Término | Definición |
| --- | --- |
| DMA | Copia entre periférico y memoria sin un bucle de CPU por dato |
| Bloque | Las N muestras pedidas |
| Overrun | Una muestra nueva pisa a una que no se leyó |
| Modo circular | Al llenar la tabla, el DMA vuelve al principio |

## Preguntas

**1.** ¿El DMA sustituye al ADC?

Respuesta. No. El ADC convierte. El DMA transporta el resultado.

**2.** ¿Por qué no se usa el modo dual intercalado?

Respuesta. Porque ES0261 describe un fallo de overrun de DMA en ese caso, y esta práctica no lo necesita.

**3.** ¿Un `printf` largo demuestra que el DMA se paró?

Respuesta. No. Demuestra que el bucle tardó en volver a mirar el LED. El bloque puede haberse llenado igual.

## Lista de comprobación

- [ ] He visto la lectura por encuesta y la del bloque.
- [ ] He mirado `ErrorCode` al menos una vez.
- [ ] LD2 sigue conmutando mientras llegan muestras.
- [ ] El proyecto usa un solo ADC, no el modo dual.

## Siguiente

[Módulo 16](17-modulo-16-encoder.md): contar pulsos y pasarlos a RPM.
