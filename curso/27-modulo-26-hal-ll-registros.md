# Módulo 26. HAL, LL y registros

El curso ha usado el HAL. A veces hace falta ver el bit, o una función que no esconda el registro. Este módulo enciende el mismo LED de tres maneras y dice qué se rompe al regenerar el proyecto.

**No comprobado en hardware.**

## Objetivos

- Conmutar PA5 con HAL, como hasta ahora.
- Conmutarlo con las funciones LL en un proyecto generado con esa opción.
- Conmutarlo escribiendo BSRR, con el nombre sacado del capítulo GPIO de RM0316.

## Prerrequisitos

PA5 como LD2. El manual de referencia RM0316 abierto por el GPIO. No hace falta cable nuevo.

## Tres distancias al registro

**Analogía.** El HAL es un parte de trabajo ya impreso: «conmuta el piloto». LL es el mismo parte, pero tú rellenas cada casilla del formulario. El registro es ir al armario y mover el interruptor con el número de borne delante. Los tres pueden encender LD2. No cuestan lo mismo cuando CubeMX vuelve a generar el código, ni cuando cambias de chip.

**Técnico.** `HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5)` es la forma del curso. LL, si el proyecto se generó con driver LL para el GPIO, ofrece `LL_GPIO_TogglePin(GPIOA, LL_GPIO_PIN_5)`. El registro de puesta a uno y a cero se llama BSRR en RM0316. Escribir el bit en la mitad baja pone el pin a 1. Escribirlo en la mitad alta lo pone a 0. ODR también refleja el nivel, pero BSRR evita leer-modificar-escribir el puerto entero. No copies un fragmento de otro manual si el nombre no aparece en el capítulo GPIO de RM0316 de esta familia.

Regenerar desde CubeMX reescribe lo que está fuera de USER CODE. Una llamada HAL dentro de USER CODE sobrevive. Una inicialización LL que CubeMX hubiera escrito fuera, no. Un proyecto pasado de HAL a LL no es un cambio de una línea: es otra generación. Por eso el ejemplo 2 es un proyecto distinto, o el mismo regenerado a conciencia, no un parche.

## Ejemplo 1. HAL

1. **Problema.** Tener la referencia conocida.
2. **Objetivo.** Conmutar LD2 cada 300 ms con HAL.
3. **Material.** La placa.
4. **Funcionamiento.** El HAL mira el ODR y escribe BSRR por ti. No necesitas nombrar el registro.
5. **Dibujo.** No hay.
6. **Cableado.** PA5 interno, SB21 cerrado.
7. **Cálculos.** No hay.
8. **CubeMX.** Proyecto de la placa, PA5 `GPIO_Output`, driver HAL.
9. **Código.**

```c
HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
HAL_Delay(300);
```

10. **Dónde.** El bucle, USER CODE.
11. **Compilar y probar.** LD2 conmuta. Regenera el proyecto desde CubeMX sin cambiar pines y vuelve a compilar. El USER CODE tiene que seguir ahí.
12. **Esperado, no medido.** El parpadeo continúa después de regenerar.
13. **Fallos.** El código desaparece: lo escribiste fuera de las marcas. SB21 abierto: el pin conmuta y el LED de la placa no. Puedes medirlo en CN5 pin 6.
14. **Variación.** `HAL_GPIO_WritePin` a 1 y a 0 en vez de toggle. El efecto es el mismo si los tiempos son iguales.
15. **Criterio.** Sabes qué líneas son tuyas y cuáles son del generador.

## Ejemplo 2. LL

1. **Problema.** Ver la misma acción con las funciones que no empaquetan tanto.
2. **Objetivo.** Conmutar PA5 con `LL_GPIO_TogglePin` en un proyecto donde CubeMX haya incluido el driver LL del GPIO.
3. **Material.** La placa. Puede ser una copia del proyecto, para no romper el de HAL.
4. **Funcionamiento.** LL exige que el reloj del puerto esté dado y el pin configurado. CubeMX lo hace en `MX_GPIO_Init` si pediste LL. No llames a LL sobre un pin que nadie configuró.
5. **Dibujo.** No hay.
6. **Cableado.** El mismo PA5.
7. **Cálculos.** No hay.
8. **CubeMX.** En el proyecto, elige el driver LL para GPIO, o el modo mixto que tu versión ofrezca, y genera. Si la opción no aparece con ese nombre, usa la que la pantalla llame «LL» en el GPIO y anota el texto. No inventes una ruta de menú si la tuya dice otra cosa.
9. **Código.**

```c
LL_GPIO_TogglePin(GPIOA, LL_GPIO_PIN_5);
LL_mDelay(300);
```

`LL_mDelay` es un retardo ocupado, del mismo estilo que `HAL_Delay`. Si no está en tu cabecera, usa un bucle contado y dilo, o conserva `HAL_Delay` solo para el tiempo. La línea que importa es la del pin.

10. **Dónde.** El bucle del proyecto LL. Incluye el encabezado que CubeMX haya añadido, normalmente a través de `main.h`.
11. **Compilar y probar.** LD2 tiene que conmutar igual que en el ejemplo 1.
12. **Esperado, no medido.** El mismo ritmo, a ojo. No es una comparación de microsegundos.
13. **Fallos.** `LL_GPIO_TogglePin` no existe: el proyecto sigue en HAL y no has generado LL. El pin no cambia: `MX_GPIO_Init` no se llama, o el reloj de GPIOA está apagado. Regenerar un proyecto HAL encima de este borra la configuración LL. No mezcles los dos proyectos en la misma carpeta sin querer.
14. **Variación.** Pon el pin a 1 con `LL_GPIO_SetOutputPin` y a 0 con `LL_GPIO_ResetOutputPin`.
15. **Criterio.** Puedes decir qué tuviste que regenerar para que LL existiera.

## Ejemplo 3. BSRR

1. **Problema.** Saber qué bit se mueve cuando el HAL y el LL ya no hacen falta, o cuando quieres verlos por dentro.
2. **Objetivo.** Poner PA5 a 1 y a 0 escribiendo `GPIOA->BSRR`, y señalar el bit en RM0316.
3. **Material.** RM0316, capítulo GPIO, registro BSRR. La placa.
4. **Funcionamiento.** El bit 5 corresponde a PA5. La mitad baja del registro pone a 1. La mitad alta pone a 0. `GPIO_PIN_5` en la cabecera CMSIS vale `(1 << 5)`, así que sirve como máscara si compruebas que es así en tu `stm32f303xe.h`. Compruébalo. No lo des por bueno solo porque aquí se diga.
5. **Dibujo.** No hay.
6. **Cableado.** PA5.
7. **Cálculos.** Bit 5. Desplazamiento 16 para la mitad alta: `GPIO_PIN_5 << 16` pone PA5 a 0 sin tocar los demás bits en esa escritura.
8. **CubeMX.** El pin tiene que seguir configurado como salida. El registro no configura el modo. Puedes dejar el proyecto HAL del ejemplo 1 y escribir el registro dentro del USER CODE. No hace falta quitar el HAL del resto.
9. **Código.**

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  GPIOA->BSRR = GPIO_PIN_5;                 /* PA5 a 1. RM0316, BSRR bits bajos */
  HAL_Delay(300);
  GPIOA->BSRR = (uint32_t)GPIO_PIN_5 << 16; /* PA5 a 0. BSRR bits altos */
  HAL_Delay(300);
  /* USER CODE END WHILE */
```

10. **Dónde.** El bucle. Un comentario con el nombre del registro y el capítulo, para que no parezca un número mágico.
11. **Compilar y probar.** LD2 conmuta. Con el depurador parado, mira el periférico GPIOA, ODR bit 5, como en el módulo 6. Tiene que seguir a las escrituras.
12. **Esperado, no medido.** El LED y el bit coinciden. Regenerar CubeMX no borra estas líneas si siguen en USER CODE, pero sí puede rehacer `MX_GPIO_Init`. Si alguien cambia PA5 de modo en el `.ioc`, tu BSRR escribirá un pin que ya no es salida.
13. **Fallos.** No se apaga: estás escribiendo ODR con una lectura antigua y pisas otros bits, o el desplazamiento está mal y pones a 1 otro pin. Mira ODR entero, no solo el LED. Otro pin se mueve: la máscara no es el bit 5. Vuelve a la cabecera.
14. **Variación.** Lee `(GPIOA->IDR >> 5) & 1` y comprueba que la entrada lee el nivel que acabas de escribir, en un pin de salida. Es una comprobación, no un pulsador.
15. **Criterio.** Puedes señalar BSRR en el manual y el bit 5 en el depurador.

## Resumen

HAL para el día a día del curso. LL cuando generas el proyecto así y quieres ver los pasos. BSRR cuando el bit importa, dentro del USER CODE, con el pin ya configurado. Regenerar no perdona lo que esté fuera de las marcas, ni un cambio de modo del pin en el `.ioc`.

## Glosario

| Término | Definición |
| --- | --- |
| HAL | La capa que ha usado el curso. Una llamada, varios registros por debajo |
| LL | Funciones más cercanas al registro, generadas si el proyecto las incluye |
| BSRR | Registro de puesta a 1 y a 0 de los pines, en RM0316 |
| USER CODE | La zona que CubeMX conserva al regenerar |

## Preguntas

**1.** ¿El registro configura solo el modo del pin?

Respuesta. No. BSRR escribe el nivel. El modo lo deja la inicialización, sea HAL o LL.

**2.** ¿Por qué no leer ODR, cambiar un bit y escribir ODR?

Respuesta. Porque entre la lectura y la escritura otra operación puede cambiar el puerto. BSRR escribe solo el bit que nombras.

**3.** ¿Conviene pasar todo el curso a registros?

Respuesta. No. El coste es el que acabas de ver: regenerar, el modo del pin y el manual abierto. Se baja de nivel cuando hace falta ver el bit.

## Lista de comprobación

- [ ] LD2 ha conmutado con HAL.
- [ ] He generado un proyecto con LL, o he anotado cómo lo llama mi versión de CubeMX.
- [ ] He señalado BSRR en RM0316 y el bit 5 en el depurador.
- [ ] El código propio está en USER CODE.

## Siguiente

[Módulo 27](28-modulo-27-interfaces.md): entrar 24 V, 0–10 V o 4–20 mA sin llevar esa señal al pin.
