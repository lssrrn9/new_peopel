# Módulo 3. Instalación y primer proyecto

Aquí el programa pasa de la pantalla al chip. La instalación detallada está en [Fuentes y entorno](00-fuentes-y-entorno.md). Este módulo la recorre con la NUCLEO-F303RE conectada y deja tres proyectos de dificultad creciente.

**No comprobado en hardware.** Al redactar esto no se instaló el entorno, no se compiló y no se grabó una placa. Los pasos son los de la documentación de STM32CubeIDE for Visual Studio Code 3.x y de UM1724.

## Objetivos

- Generar un proyecto CMake para la placa NUCLEO-F303RE.
- Compilarlo y grabarlo con el ST-LINK de la propia tarjeta.
- Parar la ejecución en `main` y ver una variable.

## Prerrequisitos

Módulos 1 y 2. Cable Mini-USB con datos. CN2 puesto, JP5 en pines 1-2, JP6 puesto, JP1 abierto.

## Qué es cada herramienta

**Analogía.** CubeMX es el plano del cuadro: dice qué borne hace qué. El compilador traduce el plano a órdenes que el operario entiende. El ST-LINK es quien entrega esas órdenes al operario y quien puede decir «para aquí y dime qué estás mirando». VS Code es la mesa donde tienes el plano, el compilador y el botón de parar.

**Técnico.**

- STM32CubeMX escribe el archivo `.ioc`, `CMakeLists.txt`, `CMakePresets.json` y `Core/Src/main.c`.
- La cadena es **CMake**, no el IDE de Eclipse.
- El preset **Debug** conserva símbolos. El preset Release optimiza y estorba para seguir una línea.
- Lo que escribas fuera de `USER CODE BEGIN` / `USER CODE END` desaparece al volver a generar el código.
- El resultado de la compilación es un `.elf`. Sin ese archivo el depurador no tiene qué grabar.

Reloj que debes ver en la pestaña *Clock Configuration* al elegir esta placa: entrada de 8 MHz por el MCO del ST-LINK (PF0, en placas C-02 o posteriores), PLL hasta 72 MHz, APB1 a 36 MHz y APB2 a 72 MHz. Si tu pantalla muestra otra cosa, no sigas: o la placa no está seleccionada o el reloj HSE no es el de la Nucleo. Confírmalo; no lo des por medido.

## Ejemplo 1. El proyecto que solo llega a main

1. **Problema.** Separar un fallo de instalación de un fallo de tu código.
2. **Objetivo.** Compilar, grabar y parar en `main` sin encender todavía un LED a propósito.
3. **Material.** La placa, el cable y el PC. Nada en los conectores.
4. **Funcionamiento.** CubeMX genera la inicialización de la placa. `main` llama a `HAL_Init`, configura el reloj y entra en un bucle vacío. El chip está vivo y no hace otra cosa.
5. **Dibujo.** No hay cableado externo. La orientación de la placa es la del [módulo 1](02-modulo-01-arquitectura.md).
6. **Cableado.** Solo el USB en CN1.

| Origen | Destino |
| --- | --- |
| PC | CN1, Mini-USB con datos |

7. **Cálculos.** No hay.
8. **CubeMX.** *File > New Project > Board Selector > NUCLEO-F303RE > Start Project*. Acepta la inicialización de periféricos de la placa. En *Project Manager*, toolchain **CMake**. Genera el código.
9. **Código.** No añadas nada todavía. El `while (1)` generado se queda vacío.
10. **Dónde.** `Core/Src/main.c`, bucle `while (1)`, sin tocar fuera de las zonas USER CODE.
11. **Compilar y probar.** Abre la carpeta en VS Code. Preset Debug. *Discover STM32Cube project* si la extensión lo pide. Build. *Run and Debug*, sonda ST-LINK. Cuando pare, la línea actual debe ser el principio de `main` o la primera línea del bucle, según `runEntry`.
12. **Esperado, no medido.** La compilación termina sin `error`. Aparece un `.elf`. LD3 encendido. LD1 indica comunicación con el destino, según UM1724 §7.6. LD2 puede quedarse apagado: ya no corre la demostración de fábrica.
13. **Fallos.** Placa invisible: controlador ST-LINK o cable sin datos. Sin `.elf`: la compilación no acabó. LD3 apagado: JP5, JP6 o los 300 mA, como en el módulo 1.
14. **Variación.** Cierra el proyecto y ábrelo de nuevo. Tiene que recordar el preset Debug.
15. **Criterio.** Paras en `main` y puedes continuar la ejecución con el botón de reanudar.

## Ejemplo 2. El LED verde cambia cada medio segundo

1. **Problema.** Ver que el programa que grabaste es el que se ejecuta, no el de fábrica.
2. **Objetivo.** Conmutar PA5 cada 500 ms.
3. **Material.** Solo la placa. LD2 es el LED.
4. **Funcionamiento.** PA5 es D13 y el ánodo del LED verde a través de R31 = 510 Ω y de SB21. Nivel alto enciende, nivel bajo apaga (UM1724 §7.6). `HAL_Delay` deja el procesador esperando. En el módulo 8 se sustituye por un temporizador.
5. **Dibujo.** No hay cableado externo. El LED es LD2, junto a la zona del microcontrolador, no LD1.
6. **Cableado.** Ninguno. Señal PA5, CN5 pin 6 si quisieras medirla, y GND en CN6 pin 6.

| Qué miras | Conector | Pin | Señal |
| --- | --- | --- | --- |
| LED de la placa | — | — | PA5, SB21 cerrado |
| Misma pista, si mides | CN5 | 6 | D13 |

7. **Cálculos.** Con R31 = 510 Ω, aunque el LED no cayera tensión, la corriente sería 3,3 / 510 = 6,5 mA, por debajo de 8 mA de trabajo y de 25 mA de máximo absoluto. Es el mismo razonamiento del módulo 1.
8. **CubeMX.** Al partir de la placa, PA5 suele estar ya como `GPIO_Output` con etiqueta LD2. Compruébalo en el pinout. Si está en reset, ponlo tú como salida push-pull, sin pull, velocidad baja. Regenera el código.
9. **Código.** Dentro del bucle, en la zona USER CODE:

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
  HAL_Delay(500);
  /* USER CODE END WHILE */
```

El generador ya cerró el `while` más abajo. No dupliques la llave de cierre. Si tu `main.c` tiene la marca `USER CODE END WHILE` dentro del bucle, el fragmento anterior encaja ahí. Si la marca está fuera, deja el `HAL_GPIO_TogglePin` y el `HAL_Delay` entre `USER CODE BEGIN WHILE` y `USER CODE END WHILE`, respetando las llaves que CubeMX haya escrito.

10. **Dónde.** `Core/Src/main.c`, bucle infinito. No hace falta otro archivo.
11. **Compilar y probar.** Build, depurar con ST-LINK, reanudar la ejecución. No dejes el programa parado en un punto de ruptura si quieres ver el parpadeo.
12. **Esperado, no medido.** LD2 cambia de estado cada 500 ms de `HAL_Delay`, más el tiempo de la propia instrucción, que a 72 MHz es despreciable frente a medio segundo. No hay una medida de cronómetro en este texto.
13. **Fallos.** LED siempre apagado: SB21 abierto, o el pin no es PA5, o el programa está parado en el depurador. LED de otra placa de la familia: algunas Nucleo-64 usan PB13; esta no, según la tabla 14.
14. **Variación.** Cambia 500 por 100 y por 1000 y observa el ritmo. Sigue siendo un retardo bloqueante.
15. **Criterio.** El verde conmuta y LD1 no es el que tú estás gobernando.

## Ejemplo 3. Un punto de ruptura y una variable

1. **Problema.** Comprobar que el depurador ve el estado del programa, no solo que el LED se mueve.
2. **Objetivo.** Contar las conmutaciones y leer el contador con el programa parado.
3. **Material.** El mismo proyecto.
4. **Funcionamiento.** Una variable global vive en RAM. Al parar en la línea siguiente al incremento, la vista *Variables* muestra el valor. Eso no es la *live watch* con el programa corriendo, que la pregunta frecuente de la extensión 3.x decía que no estaba en la versión inicial.
5. **Dibujo.** No hay cableado nuevo.
6. **Cableado.** Ninguno.
7. **Cálculos.** No hay.
8. **CubeMX.** El mismo proyecto. No regeneres después de editar si no hace falta: regenerar no borra el USER CODE, pero conviene no depender de ello al principio.
9. **Código.**

```c
/* USER CODE BEGIN PV */
static uint32_t pasos;
/* USER CODE END PV */
```

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  pasos++;
  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
  HAL_Delay(500);
  /* USER CODE END WHILE */
```

10. **Dónde.** `pasos` en `USER CODE BEGIN PV`, cerca de las variables globales. El incremento en el bucle.
11. **Compilar y probar.** Pon un punto de ruptura en `HAL_GPIO_TogglePin`. Inicia la depuración. En cada parada, `pasos` debe haber subido una unidad respecto a la parada anterior. Reanuda.
12. **Esperado, no medido.** La primera parada muestra 1, la segunda 2, y así. Si el compilador en Debug elimina `pasos` porque no le ve uso, márcala `volatile`. En Debug, con la variable usada, no debería hacer falta. Si desaparece, declara `static volatile uint32_t pasos;`.
13. **Fallos.** La vista vacía: no estás parado en ese marco de pila, o estás en Release. El contador salta de 10 en 10: hay más de un punto de ruptura o el programa corrió entre medias.
14. **Variación.** Añade `if (pasos == 10) { pasos = 0; }` y comprueba el vuelco a cero.
15. **Criterio.** Lees el valor parado en la línea, lo reanudas y el valor siguiente es coherente.

## Resumen

El proyecto de la placa, en CMake, se abre en VS Code, se compila en Debug y se graba con el ST-LINK. PA5 mueve LD2. Una variable se mira con el programa parado.

## Glosario

| Término | Definición |
| --- | --- |
| Compilar | Traducir C a instrucciones del Cortex-M4 |
| `.elf` | Ejecutable con símbolos de depuración |
| Grabar | Escribir ese ejecutable en la Flash del STM32F303RET6 |
| Punto de ruptura | Orden al depurador de parar en una línea |
| `HAL_Delay` | Espera activa en milisegundos. El núcleo no atiende otra cosa mientras tanto |

## Preguntas

**1.** ¿LD1 parpadeando demuestra que tu `HAL_Delay` funciona?

Respuesta. No. LD1 lo gobierna el ST-LINK. Tu programa gobierna LD2, que es PA5.

**2.** ¿Por qué el preset Release estorba en este módulo?

Respuesta. Quita información que el depurador necesita para parar en una línea de C y mostrar `pasos`.

**3.** ¿Dónde no debes escribir?

Respuesta. Fuera de los comentarios `USER CODE`. Esa parte la regenera CubeMX.

## Lista de comprobación

- [ ] El proyecto es de la placa NUCLEO-F303RE y la cadena es CMake.
- [ ] El reloj en CubeMX queda en 72 MHz con el HSE de 8 MHz de la placa, o has anotado que en tu pantalla no era así y no has seguido.
- [ ] LD2 conmuta.
- [ ] Has leído `pasos` con el programa parado.

## Siguiente

[Módulo 4](05-modulo-04-lenguaje-c.md): leer el C que acabas de usar, sin dar por sabido el lenguaje.
