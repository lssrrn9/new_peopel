# Módulo 4. Fundamentos de C aplicados a STM32

El módulo 3 dejó un `main.c` que parpadea. Este módulo explica el C que ya estás leyendo. No hace falta haber programado antes. Hace falta el proyecto del módulo 3, abierto en VS Code, en el preset Debug.

**No comprobado en hardware.** Este código no se compiló ni se grabó al redactarlo. Los tamaños de `uint8_t`, `uint16_t` y `uint32_t` son los que exige el lenguaje en esos tipos, no una medida de esta placa.

## Objetivos

- Leer un tipo entero y saber cuántos bits ocupa.
- Distinguir una variable que vive todo el programa de una que muere al salir de la función.
- Sacar el parpadeo a una función con un argumento en milisegundos.
- Usar un `if` cuyo dato cambias tú desde el depurador, con el programa parado.

## Prerrequisitos

El [módulo 3](04-modulo-03-primer-proyecto.md), con PA5 ya como salida y LD2 visible. No hay cableado nuevo.

## El lenguaje, con la analogía delante

**Analogía.** Una orden de trabajo tiene casillas. Unas caben un dígito, otras un número largo. Si anotas un valor en una casilla que se tira al acabar la tarea, a la siguiente tarea ya no está. El turno de noche que no termina es el `while (1)`. Una función es un procedimiento con nombre: le pasas un dato y hace siempre lo mismo.

**Técnico.**

| Tipo | Bits | Para qué lo usa este curso |
| --- | --- | --- |
| `uint8_t` | 8 | Un byte de una trama, un carácter |
| `uint16_t` | 16 | Un código de ADC o de DAC de 12 bits |
| `uint32_t` | 32 | Milisegundos, un contador que no quieres que desborde pronto |
| `int` | En la cadena GNU Arm de este entorno, 32 bits | Evítalo en pines y en tiempos. El HAL no lo usa para eso |

Esos tres `uintN_t` salen de `stdint.h`, que el proyecto de CubeMX ya incluye a través de sus cabeceras. No son un invento del HAL.

Una variable declarada dentro de una función es local: al salir, ese espacio se reutiliza. Una declarada fuera, o dentro con `static`, conserva el valor. `volatile` le dice al compilador que no dé por hecho que nadie más cambia esa variable. La usarás cuando el depurador o una interrupción escriban en ella.

`HAL_Delay` sigue bloqueando el procesador. Aquí todavía se usa. El módulo 8 lo quita del lazo.

## Ejemplo 1. Tres contadores y su tamaño

1. **Problema.** Tratar todos los números como si fueran iguales y no entender por qué uno desborda y otro no.
2. **Objetivo.** Declarar un `uint8_t`, un `uint16_t` y un `uint32_t`, incrementarlos y leerlos con el programa parado.
3. **Material.** El proyecto del módulo 3. Ninguna pieza externa.
4. **Funcionamiento.** Cada vuelta del bucle suma uno. El de 8 bits vuelve a 0 al pasar de 255. El de 16 bits, al pasar de 65535. El de 32 bits, en la práctica de este módulo, no llega.
5. **Dibujo.** No hay cableado.
6. **Cableado.** Solo el USB en CN1. LD2 sigue en PA5.

| Qué | Señal |
| --- | --- |
| LED verde | PA5, ya configurado |

7. **Cálculos.** 2^8 = 256 valores, de 0 a 255. 2^16 = 65536 valores, de 0 a 65535.
8. **CubeMX.** El mismo proyecto. No hace falta un pin nuevo.
9. **Código.**

```c
/* USER CODE BEGIN PV */
static uint8_t cuenta8;
static uint16_t cuenta16;
static uint32_t cuenta32;
/* USER CODE END PV */
```

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  cuenta8++;
  cuenta16++;
  cuenta32++;
  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
  HAL_Delay(200);
  /* USER CODE END WHILE */
```

10. **Dónde.** Las tres variables en `USER CODE BEGIN PV`. El incremento en el bucle de `Core/Src/main.c`.
11. **Compilar y probar.** Preset Debug, build, depurar con ST-LINK. Punto de ruptura en `HAL_GPIO_TogglePin`. En cada parada mira *Variables*.
12. **Esperado, no medido.** `cuenta8` recorre 0, 1, 2… y, al pasar de 255, vuelve a 0. `cuenta32` coincide con el número de paradas. Si el compilador elimina alguna porque no ve que se use, declárala `volatile`.
13. **Fallos.** La vista vacía: estás en Release o no estás parado en esa función. El LED no cambia: el programa sigue parado en el punto de ruptura. Reanuda.
14. **Variación.** Suma 10 en vez de 1 y cuenta cuántas vueltas necesita `cuenta8` para volver a 0. Son 26 vueltas si partes de 0, porque 250 + 10 desborda a 4.
15. **Criterio.** Lees los tres valores y puedes explicar el vuelco del de 8 bits.

## Ejemplo 2. El parpadeo sale a una función

1. **Problema.** El bucle mezcla el tiempo, el pin y la cuenta. Cuando el programa crezca, eso no se puede leer.
2. **Objetivo.** Una función `parpadeo` que recibe los milisegundos.
3. **Material.** El mismo proyecto.
4. **Funcionamiento.** Llamar a una función es saltar a ese procedimiento y volver. El argumento `ms` es una copia local. Cambiar `ms` dentro no cambia la variable del llamador.
5. **Dibujo.** No hay cableado.
6. **Cableado.** Ninguno.
7. **Cálculos.** 200 ms y 800 ms son los dos periodos que vas a comparar en el ejemplo 3. No son una norma.
8. **CubeMX.** Sin cambios.
9. **Código.** La función va en la zona de funciones de usuario, antes de `main` o donde CubeMX haya dejado `USER CODE BEGIN 0`.

```c
/* USER CODE BEGIN 0 */
static void parpadeo(uint32_t ms)
{
  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
  HAL_Delay(ms);
}
/* USER CODE END 0 */
```

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  parpadeo(200);
  /* USER CODE END WHILE */
```

Puedes dejar los contadores del ejemplo 1 o quitarlos. Si los quitas, quítalos también de `PV` y del bucle.

10. **Dónde.** `parpadeo` en `USER CODE BEGIN 0`. La llamada en el `while`.
11. **Compilar y probar.** Build y depurar. Un punto de ruptura en la primera línea de `parpadeo` y otro en la llamada. Entras y sales con *Step Into* y *Step Out*.
12. **Esperado, no medido.** Al entrar, `ms` vale 200. Al salir, el programa vuelve a la línea siguiente del `while`. LD2 cambia al ritmo de ese retardo.
13. **Fallos.** Error de compilación «implicit declaration»: la función está debajo del `while` y no hay prototipo. Déjala en `USER CODE BEGIN 0`, que está antes de `main`. El LED fijo: sigues parado dentro de la función.
14. **Variación.** Llama a `parpadeo(200)` y luego a `parpadeo(800)` en la misma vuelta. El ritmo deja de ser uniforme. Eso es el argumento, no un pin distinto.
15. **Criterio.** El tiempo está en un solo sitio, el argumento, y el bucle solo llama.

## Ejemplo 3. Un if que decides desde el depurador

1. **Problema.** Ver una decisión del programa sin cablear todavía el pulsador.
2. **Objetivo.** Si `modo` es 0, el periodo es 200 ms. Si no, es 800 ms. Cambias `modo` con la ejecución parada.
3. **Material.** El mismo proyecto.
4. **Funcionamiento.** `if` mira una condición y elige un camino. `modo` es global y `volatile` porque la vas a escribir desde el depurador, no desde el programa.
5. **Dibujo.** No hay cableado. El pulsador real es el módulo 5.
6. **Cableado.** Ninguno.
7. **Cálculos.** No hay.
8. **CubeMX.** Sin cambios.
9. **Código.**

```c
/* USER CODE BEGIN PV */
static volatile uint32_t modo;
/* USER CODE END PV */
```

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  uint32_t periodo = 200;
  if (modo != 0U)
  {
    periodo = 800;
  }
  parpadeo(periodo);
  /* USER CODE END WHILE */
```

10. **Dónde.** `modo` en `PV`. El `if` en el bucle. `periodo` es local: nace y muere en cada vuelta.
11. **Compilar y probar.** Punto de ruptura en el `if`. En la primera parada `modo` es 0. Reanuda y observa el ritmo. Para otra vez, en *Variables* escribe 1 en `modo`, reanuda.
12. **Esperado, no medido.** Con `modo` a 0 el cambio de LD2 es más rápido que con `modo` a 1. Esto no es una *live watch* con el programa corriendo: escribes el valor mientras está parado, como en el módulo 3.
13. **Fallos.** Escribes `modo` y no cambia el ritmo: el compilador había guardado el valor en un registro. Por eso va `volatile`. Escribes el valor con el programa corriendo y no se queda: la vista de la extensión 3.x, en su versión inicial, documenta la edición con la ejecución parada.
14. **Variación.** Añade un tercer valor: si `modo` es 2, `periodo` es 50. Usa `else if`.
15. **Criterio.** Puedes decir qué línea se ejecuta para cada valor de `modo` antes de reanudar.

## Resumen

`uint8_t`, `uint16_t` y `uint32_t` tienen tamaño fijo. Una función recibe el tiempo. Un `if` elige el periodo. Todo sigue en PA5 y en el USER CODE.

## Glosario

| Término | Definición |
| --- | --- |
| Tipo | El tamaño y el significado de una casilla |
| Variable local | Existe mientras se ejecuta la función |
| Variable global | Existe mientras corre el programa |
| Argumento | El dato que le pasas a una función |
| `if` | Elige un camino según una condición |
| `volatile` | El compilador no puede suponer que el valor sigue igual |

## Preguntas

**1.** ¿Por qué `cuenta8` vuelve a 0?

Respuesta. Tiene 8 bits. El valor siguiente a 255 no cabe y la suma queda en 0.

**2.** ¿Cambiar `ms` dentro de `parpadeo` cambia la constante 200 de la llamada?

Respuesta. No. `ms` es una copia. La llamada sigue escribiendo 200.

**3.** ¿`HAL_Delay` deja al procesador libre para otra cosa?

Respuesta. No. Se queda en esa espera. El módulo 8 separa el tiempo del bucle.

## Ejercicios

1. Declara un `uint16_t` a 65535, súmale 1 y di qué valor esperas ver parado en la línea siguiente.
2. Escribe una función `encender` y otra `apagar` que usen `HAL_GPIO_WritePin` con `GPIO_PIN_SET` y `GPIO_PIN_RESET`. El bucle las llama con un `HAL_Delay` entre medias.
3. Explica, sin cablear nada, qué cambiarías del ejemplo 3 para que el pulsador decidiera `modo`. No lo implementes todavía.

## Lista de comprobación

- [ ] He visto desbordar un `uint8_t` en el depurador.
- [ ] El tiempo del parpadeo está en el argumento de una función.
- [ ] He cambiado `modo` con el programa parado y el ritmo ha seguido esa decisión.

## Siguiente

[Módulo 5](06-modulo-05-gpio.md): el mismo pin, más un LED y un pulsador fuera de la placa.
