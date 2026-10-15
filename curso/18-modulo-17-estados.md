# Módulo 17. Máquinas de estados

Una cadena de `HAL_Delay` no dice en qué situación está el programa. Una máquina de estados le pone nombre a cada situación y escribe qué la hace cambiar. El `main` solo pide «da un paso».

**No comprobado en hardware.**

## Objetivos

- Reescribir el semáforo como estados con nombre.
- Añadir una alarma con reposo, prealarma y alarma.
- Partir el programa en archivos que CubeMX no borre.

## Prerrequisitos

El semáforo del [módulo 8](09-modulo-08-temporizadores.md): PA8 rojo, PB5 ámbar, PC7 verde, cada uno con su resistencia. B1 en PC13. El tiempo con `HAL_GetTick`, no con un retardo que tape el resto.

## La idea

**Analogía.** Un parte de averías no dice «espera 4 segundos y luego haz lo otro». Dice: en reposo, en prealarma o en alarma, y qué evento cambia de hoja. El semáforo es el mismo tipo de parte: rojo, rojo y ámbar, verde, ámbar.

**Técnico.** Cada estado es un valor de un `enum`. Cada paso mira el tiempo que lleva en ese estado y, si toca, pasa al siguiente. El trabajo de encender pines está en una función. `main` llama a `semaforo_paso` y a `alarma_paso`. No hay otro hilo: sigue siendo el bucle único. FreeRTOS llega en el módulo 18.

## Ejemplo 1. Semáforo con estados

1. **Problema.** La tabla de fases del módulo 8 no tiene nombre, y cuesta añadir rojo+ámbar.
2. **Objetivo.** Cuatro estados: rojo, rojo-ámbar, verde, ámbar.
3. **Material.** Los tres LED del módulo 8. No el transistor en PB5 a la vez.
4. **Funcionamiento.** Tiempos de juguete: rojo 4000 ms, rojo-ámbar 1000 ms, verde 4000 ms, ámbar 1000 ms. Al vencer, el estado cambia. Cada paso escribe las tres luces.
5. **Dibujo.** [Semáforo](img/cable-semaforo.svg).
6. **Cableado.** El del módulo 8.

| Estado | PA8 | PB5 | PC7 |
| --- | --- | --- | --- |
| Rojo | 1 | 0 | 0 |
| Rojo-ámbar | 1 | 1 | 0 |
| Verde | 0 | 0 | 1 |
| Ámbar | 0 | 1 | 0 |

7. **Cálculos.** Los tiempos de arriba. En rojo-ámbar hay dos LED: calcula las dos corrientes y súmalas. Con 4,8 mA cada una, son unos 10 mA, dentro de la suma de 80 mA y con cada pin en su zona de diseño.
8. **CubeMX.** PA8, PB5 y PC7 salidas, como en el módulo 8.
9. **Código.**

```c
/* USER CODE BEGIN 0 */
typedef enum
{
  ST_ROJO = 0,
  ST_ROJO_AMBAR,
  ST_VERDE,
  ST_AMBAR
} estado_semaforo_t;

static estado_semaforo_t estado_sem;
static uint32_t marca_sem;

static void aplicar_luces(uint8_t r, uint8_t a, uint8_t v)
{
  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_8, r ? GPIO_PIN_SET : GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_5, a ? GPIO_PIN_SET : GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_7, v ? GPIO_PIN_SET : GPIO_PIN_RESET);
}

static void semaforo_paso(void)
{
  static const uint32_t duracion[] = {4000U, 1000U, 4000U, 1000U};
  if ((HAL_GetTick() - marca_sem) < duracion[estado_sem])
  {
    return;
  }
  marca_sem = HAL_GetTick();
  estado_sem = (estado_semaforo_t)((estado_sem + 1) % 4);
  if (estado_sem == ST_ROJO) { aplicar_luces(1, 0, 0); }
  if (estado_sem == ST_ROJO_AMBAR) { aplicar_luces(1, 1, 0); }
  if (estado_sem == ST_VERDE) { aplicar_luces(0, 0, 1); }
  if (estado_sem == ST_AMBAR) { aplicar_luces(0, 1, 0); }
}
/* USER CODE END 0 */
```

En `USER CODE BEGIN 2`, enciende el rojo y guarda `marca_sem = HAL_GetTick()`. En el bucle, solo `semaforo_paso();`.

10. **Dónde.** Todavía en `main.c`. El ejemplo 3 lo saca a otro archivo.
11. **Compilar y probar.** Observa el orden, incluido el momento con rojo y ámbar juntos.
12. **Esperado, no medido.** El ciclo tiene cuatro fases y el verde no coincide con el rojo.
13. **Fallos.** Se salta una fase: `duracion` no tiene cuatro elementos. Dos luces que no tocan: `aplicar_luces` no se llama al cambiar. PB5 ocupado por el relé: desmonta el relé.
14. **Variación.** Alarga el verde a 6000 ms cambiando solo esa casilla.
15. **Criterio.** Puedes decir el nombre del estado mirando las luces.

## Ejemplo 2. Alarma de tres estados

1. **Problema.** Un umbral que solo enciende un LED no distingue «acaba de pasar» de «lleva un rato mal».
2. **Objetivo.** Reposo, prealarma y alarma. El umbral, en este ejemplo, es una constante que simulas con B1: pulsado significa «la medida está fuera».
3. **Material.** B1 y LD2. LD2 indica la alarma. El semáforo puede seguir en sus pines.
4. **Funcionamiento.** En reposo, si B1 se pulsa, se pasa a prealarma y se anota el tiempo. Si se suelta, se vuelve a reposo. Si la prealarma dura 2000 ms con B1 aún pulsado, se pasa a alarma y LD2 se enciende. En alarma, soltar B1 vuelve a reposo y apaga LD2. 2000 ms es de diseño.
5. **Dibujo.** No hay cable nuevo.
6. **Cableado.** PC13 y PA5 de la placa.
7. **Cálculos.** 2000 ms de confirmación. No es un tiempo de proceso industrial.
8. **CubeMX.** PC13 entrada. PA5 salida.
9. **Código.**

```c
typedef enum { AL_REPOSO = 0, AL_PRE, AL_ALARMA } estado_alarma_t;

static estado_alarma_t estado_al;
static uint32_t marca_al;

static void alarma_paso(void)
{
  uint8_t fuera = (HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET) ? 1U : 0U;
  uint32_t ahora = HAL_GetTick();
  if (estado_al == AL_REPOSO && fuera)
  {
    estado_al = AL_PRE;
    marca_al = ahora;
  }
  else if (estado_al == AL_PRE && !fuera)
  {
    estado_al = AL_REPOSO;
  }
  else if (estado_al == AL_PRE && (ahora - marca_al) >= 2000U)
  {
    estado_al = AL_ALARMA;
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);
  }
  else if (estado_al == AL_ALARMA && !fuera)
  {
    estado_al = AL_REPOSO;
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);
  }
}
```

El bucle llama a `semaforo_paso` y a `alarma_paso`.

10. **Dónde.** `main.c`, hasta el ejemplo 3.
11. **Compilar y probar.** Pulsación corta: LD2 no se enciende. Pulsación de más de dos segundos: LD2 se enciende hasta que sueltas.
12. **Esperado, no medido.** Ese comportamiento. El semáforo no se detiene durante la pulsación, porque ningún paso llama a `HAL_Delay`.
13. **Fallos.** El semáforo se congela: volviste a meter un retardo. LD2 enciende al momento: la prealarma no está en el camino. B1 al revés: comprueba el nivel bajo.
14. **Variación.** Sustituye B1 por `N > umbral` cuando unas el ADC. La máquina no cambia de forma; cambia la expresión de `fuera`.
15. **Criterio.** Hay tres nombres y LD2 solo está encendido en alarma.

## Ejemplo 3. Tres archivos

1. **Problema.** `main.c` ya mezcla dos máquinas.
2. **Objetivo.** Dejar `semaforo.c`, `alarma.c` y las llamadas en `main.c`.
3. **Material.** El mismo.
4. **Funcionamiento.** CubeMX regenera `main.c` y conserva el USER CODE. Un `.c` nuevo no lo borra, pero CMake tiene que compilarlo. En un proyecto CMake de CubeMX, el sitio seguro es añadir el archivo donde el `CMakeLists.txt` ya recoge los fuentes de `Core/Src`, o en la zona que el propio fichero marque como mantenida por el usuario. Si tu versión no tiene esa zona, crea `Core/Src/semaforo.c` y comprueba que el globo de fuentes de `CMakeLists.txt` incluye `Core/Src/*.c`. Si no lo incluye, añade una línea en el bloque que CubeMX indique como editable, no fuera de él a ciegas: al regenerar, lo de fuera de ese bloque puede perderse.
5. **Dibujo.** No hay.
6. **Cableado.** El mismo.
7. **Cálculos.** No hay.
8. **CubeMX.** Genera una vez y mira `CMakeLists.txt` antes de dar por hecho el globo.
9. **Código.** `semaforo.h` declara `void semaforo_inicia(void);` y `void semaforo_paso(void);`. Lo mismo para la alarma. Los `.c` contienen lo que estaba en `main.c`. `main` incluye los dos `.h` dentro de `USER CODE BEGIN Includes` y llama a los `paso` en el bucle.
10. **Dónde.** `Core/Inc` y `Core/Src`, más el USER CODE de `main.c`.
11. **Compilar y probar.** Build. Si el enlazador dice que `semaforo_paso` no existe, el `.c` no entró en CMake. Corrígelo antes de seguir. Regenera el código desde CubeMX una vez y comprueba que los `.c` nuevos siguen en el disco y que el proyecto aún enlaza.
12. **Esperado, no medido.** El comportamiento es el de los ejemplos 1 y 2. Regenerar no borra esos archivos.
13. **Fallos.** «undefined reference»: el fuente no está en el target. «multiple definition»: dejaste el cuerpo también en `main.c`. El archivo desaparece al generar: lo habías puesto en una carpeta que CubeMX limpia. Muévelo a `Core/Src` y versiona el cambio.
14. **Variación.** Añade `const char *semaforo_nombre(void);` que devuelva el nombre del estado, e imprímelo por USART2 cuando cambie.
15. **Criterio.** `main` no enciende pines del semáforo. Solo llama a los pasos.

## Resumen

Cada situación tiene un nombre y una transición. El bucle llama a los pasos. Los archivos nuevos tienen que entrar en CMake sin quedar a merced de una regeneración ciega.

## Glosario

| Término | Definición |
| --- | --- |
| Estado | Una situación con nombre |
| Transición | El paso de una situación a otra cuando se cumple una condición |
| Paso | La función que se llama muchas veces y hace como mucho una transición |

## Preguntas

**1.** ¿Por qué el semáforo no se para mientras mantienes B1?

Respuesta. Porque `alarma_paso` no espera los 2000 ms dentro de un retardo. Mira el reloj y vuelve.

**2.** ¿CubeMX borra `semaforo.c`?

Respuesta. No, si está en `Core/Src` y no es un archivo que CubeMX considere generado. El riesgo está en `CMakeLists.txt` si lo editaste fuera de la zona que el generador conserva.

**3.** ¿Esto ya es FreeRTOS?

Respuesta. No. Sigue habiendo un solo bucle.

## Lista de comprobación

- [ ] Veo las cuatro fases, incluida rojo-ámbar.
- [ ] Una pulsación corta no deja LD2 encendido.
- [ ] Tras regenerar, el proyecto sigue enlazando los dos archivos nuevos.

## Siguiente

[Módulo 18](19-modulo-18-freertos.md): dos tareas de verdad, cuando un solo bucle ya no se quiere estirar más.
