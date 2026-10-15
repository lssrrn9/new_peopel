# Módulo 23. Watchdog y fallos

Un watchdog es un temporizador que reinicia el chip si el programa no lo atiende a tiempo. Sirve para salir de un bucle que se quedó colgado. Al volver, hay que saber que el arranque no fue un encendido normal.

**No comprobado en hardware.** Los tiempos dependen del LSI. El datasheet da fLSI de 30 kHz, 40 kHz típico y 50 kHz. No se ha medido el de tu placa.

## Objetivos

- Mantener el watchdog alimentado y no reiniciar.
- Dejar de alimentarlo y ver un reinicio, con un patrón de LD2 distinto.
- Imprimir la causa del reset en el arranque siguiente.

## Prerrequisitos

PA5 y USART2. El IWDG usa el oscilador interno de baja frecuencia, no un pin. Este módulo usa el watchdog independiente, no el de ventana. El de ventana (WWDG) existe en el chip; se cita para no confundir los nombres, y no se configura aquí.

## El perro guardián

**Analogía.** Es un temporizador de «sigue ahí» que un vigilante carga. Si el operario no lo recarga, el vigilante pulsa el reset. No arregla el fallo: solo impide quedarse colgado para siempre. Al volver, el parte tiene que decir «me reinició el vigilante», no «me acaban de enchufar».

**Técnico.** El IWDG cuenta con el LSI. Tiempo aproximado, con prescaler 32 y recarga 4095: `(32 * 4096) / fLSI`. Con 40 kHz, unos 3,3 s. Con 30 kHz, unos 4,4 s. Con 50 kHz, unos 2,6 s. El programa tiene que recargar bastante antes del mínimo, por ejemplo cada 500 ms. Esos números son cuentas con la tabla del datasheet, no una medida. Confirma en RM0316 la fórmula del IWDG por si el recuento del reload incluye el +1, que es lo que la fórmula de arriba ya supone al usar 4096 para un reload de 4095.

Las banderas de reset están en `RCC->CSR`. Los nombres CMSIS de esta familia incluyen `RCC_CSR_IWDGRSTF`, `RCC_CSR_PORRSTF` y `RCC_CSR_PINRSTF`. Se borran escribiendo `RCC_CSR_RMVF`. Léelas al arrancar, antes de borrarlas. Cítalas desde el capítulo RCC de RM0316 si tu cabecera usa el mismo registro.

## Ejemplo 1. Recargar a tiempo

1. **Problema.** Activar el watchdog sin que la placa se reinicie sola.
2. **Objetivo.** LD2 conmuta cada 500 ms y el IWDG se recarga en ese mismo ritmo.
3. **Material.** La placa.
4. **Funcionamiento.** El prescaler y la recarga dejan un margen de más de 2 s incluso con el LSI rápido. Recargar cada 500 ms entra en ese margen.
5. **Dibujo.** No hay.
6. **Cableado.** No hay.
7. **Cálculos.** Los del apartado técnico. 500 ms es holgado frente a 2,6 s.
8. **CubeMX.** IWDG activado. Prescaler 32, reload 4095, o los valores que CubeMX nombre así. PA5 salida. No actives el WWDG a la vez en este ejemplo.
9. **Código.**

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
  HAL_IWDG_Refresh(&hiwdg);
  HAL_Delay(500);
  /* USER CODE END WHILE */
```

`HAL_Delay` aquí es aceptable porque el único trabajo es demostrar que se recarga. En un programa con más tareas, la recarga tiene que estar en un sitio que deje de ejecutarse si el programa se cuelga de verdad. No la pongas en una interrupción que siga viva cuando el bucle ya esté muerto: entonces el watchdog no se entera.

10. **Dónde.** El bucle. El arranque del IWDG lo genera CubeMX.
11. **Compilar y probar.** Graba y espera al menos medio minuto.
12. **Esperado, no medido.** LD2 sigue conmutando. La placa no se reinicia. Si se reinicia, el reload no es el que crees o `Refresh` no se está llamando.
13. **Fallos.** Reinicios periódicos: el tiempo real es más corto que 500 ms. Abre la configuración y la fórmula. No se puede depurar con un punto de ruptura largo: parado, dejas de recargar y el IWDG reinicia. Para mirar variables, desactiva el IWDG en un ensayo o recarga en un sitio que siga corriendo. Dilo, no lo dejes desactivado sin querer.
14. **Variación.** Recarga cada 100 ms. Sigue sin reiniciar.
15. **Criterio.** Medio minuto sin reinicio, con el refresh en el bucle.

## Ejemplo 2. Dejar de recargar

1. **Problema.** Comprobar que el reinicio ocurre, y verlo en el LED.
2. **Objetivo.** Tras unos segundos sanos, entrar en un bucle que no recarga. LD2, al volver, parpadea deprisa durante un segundo para marcar que la causa fue el IWDG.
3. **Material.** La placa y, en el ejemplo 3, el monitor.
4. **Funcionamiento.** Un contador llega a 10 vueltas de 500 ms y entonces entra en `while (1) { }` sin refresh. El IWDG expira. Al arrancar, si la bandera está puesta, se hacen diez conmutaciones rápidas de LD2 antes del ritmo normal.
5. **Dibujo.** No hay.
6. **Cableado.** No hay.
7. **Cálculos.** Unos 5 s de trabajo sano más el tiempo del LSI hasta el reset. Verás un hueco del orden de los segundos calculados arriba. Mide el tuyo con un reloj de pared y anótalo como tuyo. No está en este texto.
8. **CubeMX.** El del ejemplo 1.
9. **Código.**

```c
/* USER CODE BEGIN 2 */
if ((RCC->CSR & RCC_CSR_IWDGRSTF) != 0U)
{
  for (uint32_t i = 0; i < 10U; i++)
  {
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    HAL_Delay(80);
    HAL_IWDG_Refresh(&hiwdg);
  }
}
/* USER CODE END 2 */
```

Hay que recargar también durante el aviso, o el watchdog vencerá otra vez a mitad de los parpadeos. En el bucle principal, deja de llamar a `Refresh` cuando `vueltas` pase de 10. No pongas ese `while (1)` vacío hasta haber visto el ejemplo 1.

10. **Dónde.** Zona 2 y el bucle.
11. **Compilar y probar.** Graba. LD2 lento, luego se para, luego ráfaga rápida, y se repite.
12. **Esperado, no medido.** Ese patrón. El hueco entre la parada y la ráfaga es tu medida del timeout.
13. **Fallos.** Ráfaga también al pulsar B2 (reset): la bandera de pin puede estar puesta y estás mirando la bandera equivocada. El ejemplo 3 separa las causas. No hay ráfaga nunca: no estás leyendo `IWDGRSTF`, o la borras antes. Bucle infinito que el depurador no suelta: es el ensayo. El reset tiene que sacarte.
14. **Variación.** Quita el cuelgue y confirma que la ráfaga desaparece en el siguiente encendido por corriente, no solo en el siguiente reset. Un power-on limpia la causa de IWDG.
15. **Criterio.** Distingues el ritmo sano del ritmo de «vuelvo de un cuelgue».

## Ejemplo 3. Imprimir la causa

1. **Problema.** El LED no dice si fue el watchdog, el pulsador de reset o quitar el USB.
2. **Objetivo.** Una línea por USART2 al arrancar, y luego borrar las banderas.
3. **Material.** El monitor serie.
4. **Funcionamiento.** Se lee `RCC->CSR` una vez. Se imprime qué bits están. Se escribe `RMVF` para no repetir la misma causa en el siguiente arranque sano.
5. **Dibujo.** No hay.
6. **Cableado.** USART2 por el ST-LINK.
7. **Cálculos.** No hay.
8. **CubeMX.** USART2 115200 8N1.
9. **Código.**

```c
/* USER CODE BEGIN 2 */
uint32_t causa = RCC->CSR;
char linea[80];
int n = snprintf(linea, sizeof(linea),
                 "csr 0x%08lX iwdg %u pin %u por %u\r\n",
                 (unsigned long)causa,
                 (causa & RCC_CSR_IWDGRSTF) ? 1 : 0,
                 (causa & RCC_CSR_PINRSTF) ? 1 : 0,
                 (causa & RCC_CSR_PORRSTF) ? 1 : 0);
if (n > 0)
{
  HAL_UART_Transmit(&huart2, (uint8_t *)linea, (uint16_t)n, 50);
}
__HAL_RCC_CLEAR_RESET_FLAGS();
/* USER CODE END 2 */
```

`__HAL_RCC_CLEAR_RESET_FLAGS` es la macro del HAL que pone `RMVF`. Si tu versión no la tiene, escribe el bit que nombre RM0316.

10. **Dónde.** Zona 2, antes de borrar y antes del bucle que se cuelga.
11. **Compilar y probar.** Tres arranques: quita y pon el USB; pulsa B2; deja que venza el IWDG. Anota las tres líneas.
12. **Esperado, no medido.** El cuelgue marca `iwdg 1`. El pulsador negro marca el reset de pin. Quitar el USB marca power-on. Puede haber más de un bit a la vez; anótalo en vez de forzar una sola causa.
13. **Fallos.** Siempre los mismos bits: no estás borrando las banderas. Línea vacía: USART2 no está listo antes de transmitir. La zona 2 ya tiene el UART inicializado si CubeMX generó el orden habitual. Texto cortado: el watchdog reinicia durante el `printf` porque el ejemplo 2 ya no recarga. Recarga una vez justo antes de imprimir si hace falta.
14. **Variación.** Guarda el último código en una variable y compáralo con la línea. En el módulo 24 esa causa se podrá guardar en Flash; aquí vive solo hasta el próximo apagado si no la imprimes.
15. **Criterio.** Las tres causas que provocaste se distinguen en el cuaderno.

## Resumen

El IWDG se recarga en el bucle que demuestra que el programa sigue vivo. Si ese bucle muere, hay reinicio. La bandera se imprime y se borra. El tiempo es aproximado porque el LSI lo es.

## Glosario

| Término | Definición |
| --- | --- |
| IWDG | Watchdog independiente, con reloj LSI |
| LSI | Oscilador interno lento, 30/40/50 kHz en el datasheet |
| Bandera de reset | Bit que recuerda la causa del último arranque |
| WWDG | Watchdog de ventana. No se usa en este módulo |

## Preguntas

**1.** ¿Por qué no recargar el IWDG dentro de un temporizador que sigue corriendo aunque el bucle esté muerto?

Respuesta. Porque entonces el cuelgue del bucle no se vería. La recarga tiene que vivir en el camino que quieres vigilar.

**2.** ¿El timeout es exactamente 3,3 s?

Respuesta. No. Esa cifra es con 40 kHz. El datasheet admite de 30 kHz a 50 kHz.

**3.** ¿Un punto de ruptura largo es compatible con el IWDG activo?

Respuesta. No, si durante la parada nadie recarga. El chip se reinicia. Es una limitación del ensayo, no un fallo del depurador.

## Lista de comprobación

- [ ] Con la recarga en el bucle, la placa no se reinicia sola.
- [ ] Sin la recarga, vuelve y LD2 lo marca.
- [ ] He anotado las banderas de tres causas distintas.
- [ ] He medido el hueco del timeout en mi mesa y no lo he copiado de los 3,3 s.

## Siguiente

[Módulo 24](25-modulo-24-flash.md): guardar un número que sobreviva a quitar el USB.
