# Módulo 6. Depuración y diagnóstico

El LED del módulo 5 puede no coincidir con lo que crees. Este módulo separa tres causas: el pin no es el que miras, el programa que corre no es el que acabas de compilar, y una variable no vale lo que imaginas. Al final se provoca un fallo a propósito, en un ensayo, y se quita.

**No comprobado en hardware.** Los nombres de vistas son los de STM32CubeIDE for Visual Studio Code 3.x. No se ejecutó este ensayo al redactarlo.

## Objetivos

- Parar en el bucle y ver el registro de salida de PA5.
- Cambiar una variable con el programa parado y ver el efecto al reanudar.
- Leer un fallo provocado y dejar el proyecto otra vez sano.

## Prerrequisitos

El proyecto del [módulo 5](06-modulo-05-gpio.md), preset Debug. La *live watch* con el programa corriendo no forma parte de este módulo: la pregunta frecuente de la extensión 3.x decía que no estaba en la versión inicial. Lo que se usa es la vista con la ejecución parada.

## Qué está pasando cuando paras

**Analogía.** Parar el depurador es como pulsar la seta y que el operario se quede con la mano donde estaba, para que puedas leer el parte. No es lo mismo que mirar la máquina en marcha con una cámara. Si el parte está en otro idioma (preset Release, sin símbolos), no lees la línea de C.

**Técnico.** El ST-LINK habla con PA13 (SWDIO) y PA14 (SWCLK). Esos pines no se usan como GPIO. El `.elf` de Debug lleva la relación entre la línea de C y la instrucción. La vista de periféricos lee registros del chip con el núcleo parado. El registro de datos de salida del GPIO se llama ODR en el manual de referencia RM0316, capítulo de GPIO. El bit 5 de `GPIOA` es PA5. Un 1 en ese bit es nivel alto.

## Ejemplo 1. El registro de PA5 y el LED

1. **Problema.** LD2 no hace lo que el `if` parece decir, y no sabes si el pin llegó a ponerse a 1.
2. **Objetivo.** Parar y comprobar que el bit de PA5 coincide con LD2.
3. **Material.** El proyecto del módulo 5, ejemplo 2 o 3. LD2 visible.
4. **Funcionamiento.** `HAL_GPIO_WritePin` acaba escribiendo el registro de set/reset, y el nivel queda reflejado en ODR. Con el núcleo parado, el pin mantiene el último nivel.
5. **Dibujo.** No hay cableado nuevo.
6. **Cableado.** El del módulo 5, si sigue montado. No hace falta tocarlo.
7. **Cálculos.** No hay.
8. **CubeMX.** Sin cambios. Sigue en Debug, no en Release.
9. **Código.** Sirve el bucle del ejemplo 2 del módulo 5. Añade una variable para tener un sitio claro donde parar:

```c
/* USER CODE BEGIN PV */
static uint8_t nivel_pa5;
/* USER CODE END PV */
```

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  if (HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET)
  {
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);
  }
  else
  {
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);
  }
  nivel_pa5 = (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_5) == GPIO_PIN_SET) ? 1U : 0U;
  /* USER CODE END WHILE */
```

10. **Dónde.** `main.c`, zonas USER CODE.
11. **Compilar y probar.** Punto de ruptura en la línea de `nivel_pa5`. Pulsa B1, reanuda hasta parar, mira el LED y la vista de periféricos del GPIOA, registro ODR, bit 5. Suelta B1 y repite.
12. **Esperado, no medido.** Con B1 pulsado, LD2 encendido, `nivel_pa5` a 1 y el bit 5 de ODR a 1. Con B1 suelto, los tres a 0. Si el LED y el bit no coinciden, el fallo es de cable o de puente SB21, no del `if`.
13. **Fallos.** No hay vista de periféricos: el programa no está parado, o la extensión no ha cargado los periféricos de este chip. ODR no cambia y el LED tampoco: no se grabó el `.elf` nuevo. Comprueba la fecha del build.
14. **Variación.** Pon el punto de ruptura antes del `WritePin` y mira que ODR todavía tiene el valor de la vuelta anterior. Das un paso y cambia.
15. **Criterio.** Puedes decir si el desacuerdo está en el programa o en el pin físico.

## Ejemplo 2. Editar el periodo con el programa parado

1. **Problema.** Quieres probar dos ritmos sin recompilar cada vez.
2. **Objetivo.** Cambiar `periodo_ms` en *Variables* y ver LD2 al reanudar.
3. **Material.** El mismo proyecto.
4. **Funcionamiento.** Con la ejecución parada escribes la RAM. Al reanudar, el programa usa ese valor. No es una watch en marcha.
5. **Dibujo.** No hay.
6. **Cableado.** Ninguno nuevo.
7. **Cálculos.** 100 ms y 1000 ms son los dos ensayos. No son medidas de un cronómetro de laboratorio.
8. **CubeMX.** Sin cambios.
9. **Código.**

```c
/* USER CODE BEGIN PV */
static volatile uint32_t periodo_ms = 300;
/* USER CODE END PV */
```

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
  HAL_Delay(periodo_ms);
  /* USER CODE END WHILE */
```

10. **Dónde.** `PV` y el bucle.
11. **Compilar y probar.** Punto de ruptura en `HAL_Delay`. En la parada, escribe 1000 en `periodo_ms`. Reanuda unos segundos y vuelve a parar. Escribe 100.
12. **Esperado, no medido.** El ritmo sigue el valor que dejaste. `volatile` evita que el compilador deje el 300 fijo en la llamada.
13. **Fallos.** El valor vuelve a 300 solo: la edición no se aplicó al proceso parado, o estás mirando una copia. La variable no aparece: Release, o el compilador la eliminó. Vuelve a Debug.
14. **Variación.** Pon 0. `HAL_Delay(0)` vuelve enseguida y el LED parece fijo, encendido a medias. No es un PWM: es un bucle demasiado rápido. El PWM es el módulo 10.
15. **Criterio.** Distingues «editar parado» de «ver el valor en marcha».

## Ejemplo 3. Un acceso inválido, y cómo se quita

1. **Problema.** Cuando el núcleo se cae, la pantalla del depurador no es un fallo del cable. Hay que saber leerla y hay que dejar el proyecto sano.
2. **Objetivo.** Provocar un acceso a una dirección prohibida, ver el fallo y borrar esa línea.
3. **Material.** Este ejemplo es un ensayo. No se deja en los módulos siguientes.
4. **Funcionamiento.** El Cortex-M4 separa la memoria. Escribir en la dirección 0 no es escribir en RAM de datos. El núcleo entra en una falta. El analizador de fallos de la extensión muestra esa excepción con el programa detenido.
5. **Dibujo.** No hay.
6. **Cableado.** Ninguno.
7. **Cálculos.** No hay.
8. **CubeMX.** Sin cambios. Sigue pudiendo depurar por SWD: el fallo no desconecta PA13 y PA14.
9. **Código.** Añádelo solo para este ensayo, al principio del bucle:

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  volatile uint32_t *prohibido = (uint32_t *)0x00000000U;
  *prohibido = 0x12345678U;
  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
  HAL_Delay(periodo_ms);
  /* USER CODE END WHILE */
```

La dirección 0 en este mapa no es una RAM de programa que puedas usar. Por eso la falta es el resultado previsto del ensayo.

10. **Dónde.** El bucle de `main.c`. En cuanto lo hayas visto, borra las dos líneas del puntero y la escritura.
11. **Compilar y probar.** Build y depurar. La ejecución no debe seguir parpadeando. Abre el analizador de fallos. Anota el tipo de falta que te muestre. Para, quita las dos líneas, vuelve a compilar y graba.
12. **Esperado, no medido.** El depurador se detiene en la falta en vez de conmutar LD2. Después de borrar el ensayo y grabar de nuevo, LD2 vuelve a conmutar. El texto exacto de la ventana depende de la versión de la extensión: anótalo como lo que tú viste.
13. **Fallos.** El LED sigue parpadeando: no grabaste este `.elf`, o el optimizador eliminó la escritura. `volatile` en el puntero está para que no la elimine. El depurador no conecta: eso es el cable o el controlador, no esta falta. Si ya no depura después del ensayo, pulsa reset (B2) y vuelve a *Run and Debug*.
14. **Variación.** No hagas una segunda falta «más interesante». Este ensayo basta, y se quita.
15. **Criterio.** El proyecto que pasas al módulo 7 no contiene la escritura a `0x00000000`.

## Resumen

Parado, el bit de ODR de PA5 se compara con LD2. Una variable `volatile` se edita en esa parada. Un acceso inválido se provoca una vez, se lee y se borra.

## Glosario

| Término | Definición |
| --- | --- |
| Punto de ruptura | Parada pedida en una línea |
| ODR | Registro de datos de salida del GPIO, RM0316 |
| Falta | Excepción del núcleo por un acceso que el mapa no permite |
| Release | Preset que estorba para seguir una línea de C |
| SWD | Depuración por PA13 y PA14, a través del ST-LINK |

## Preguntas

**1.** ¿LD1 apagado demuestra que el programa se cayó?

Respuesta. No. LD1 lo gobierna el ST-LINK. La falta se ve en el depurador.

**2.** ¿Por qué el ensayo escribe en la dirección 0?

Respuesta. Para provocar una falta conocida y aprender a quitarla. No es una técnica de trabajo.

**3.** ¿Editar `periodo_ms` mientras el programa corre es lo que acabas de practicar?

Respuesta. No. Has editado con la ejecución parada.

## Lista de comprobación

- [ ] He visto el bit 5 de ODR coincidir con LD2.
- [ ] He cambiado `periodo_ms` parado y el ritmo ha seguido ese valor.
- [ ] He quitado el acceso inválido y el proyecto vuelve a parpadear.

## Siguiente

[Módulo 7](08-modulo-07-uart.md): ver números en el PC sin dejar el programa parado.
