# Módulo 20. PID

Un PID acerca una medida a una consigna. Primero se prueba sobre una fórmula, para ver cada término sin quemar nada. Después, sobre un LED y una fotorresistencia: una planta de juguete, no un horno ni un motor.

**No comprobado en hardware.** Las ganancias de ejemplo no son una sintonía medida.

## Objetivos

- Escribir un PID discreto con periodo fijo y salida limitada.
- Ver el efecto de cada término en un modelo que vive en el programa.
- Repetirlo con el brillo de PC7 y la luz leída en PA1, y decir qué no se puede concluir.

## Prerrequisitos

Módulos 10, 11 y 19. LED con resistencia en PC7. Fotorresistencia (LDR) para el ejemplo 2, con un divisor.

## El regulador

**Analogía.** La consigna es la temperatura que pides. La medida es el termómetro. P empuja más cuanto mayor es el error, como abrir más el grifo si el vaso está más vacío. I acumula el error que no se acaba de ir, como recordar que llevas un rato por debajo. D mira si el error está creciendo, y frena. Sin un límite, I sigue acumulando mientras la salida ya está al máximo: es el windup, y la salida no vuelve cuando ya debería.

**Técnico.** Periodo fijo `dt` en segundos. En el ejemplo, 50 ms.

```
error = consigna - medida
integral = integral + error * dt
derivada = (error - error_anterior) / dt
salida = Kp*error + Ki*integral + Kd*derivada
```

Después se recorta `salida` entre 0 y 1000, que son las cuentas del PWM del módulo 10. Si la salida recortada no es la que el PID pidió, no se sigue integrando. Eso es un anti-windup simple. Las ganancias del modelo de juguete son un punto de partida para ver el signo, no una sintonía: `Kp = 2`, `Ki = 0,5`, `Kd = 0` en el primer ensayo. Se cambian de una en una.

Unidades: si la medida y la consigna están en las mismas cuentas de ADC, la salida hay que escalarla al PWM. En el modelo, medida y salida son «unidades de juguete» de 0 a 1000. Se dice en el `printf`.

## Ejemplo 1. Planta de mentira

1. **Problema.** Entender P, I y D sin cablear.
2. **Objetivo.** Una planta `medida = medida + (salida − medida) / 16` cada 50 ms, y un PID que la lleve a 600.
3. **Material.** Solo el programa y USART2.
4. **Funcionamiento.** La planta es un filtro lento hacia la salida del PID. No es un proceso real. Sirve para ver si el número se acerca a la consigna y si se pasa.
5. **Dibujo.** No hay.
6. **Cableado.** USB y el monitor.
7. **Cálculos.** Con Kp = 2, Ki = 0, Kd = 0, error inicial 600, salida pedida 1200, recortada a 1000. La planta camina hacia 1000 y se queda por encima o cerca de 600 según el recorte y P. Con P solo y sin recorte, una planta de ganancia 1 se estabiliza cuando `Kp * error = medida` y `medida = salida`, es decir el error no se anula. Por eso hace falta I para error nulo en este modelo. Esa frase es el objetivo del ensayo.
8. **CubeMX.** USART2. No hace falta ADC todavía.
9. **Código.**

```c
/* USER CODE BEGIN 0 */
static int32_t planta;
static int32_t integral;
static int32_t error_ant;
static const int32_t KP = 2;
static const int32_t KI = 1; /* por segundo, aplicado como Ki * error * dt */
static const int32_t KD = 0;

static int32_t pid_paso(int32_t consigna, int32_t medida)
{
  int32_t error = consigna - medida;
  int32_t derivada = (error - error_ant) * 20; /* /0,05 s = *20 */
  int32_t propuesta_i = integral + error / 20; /* dt = 0,05; 1/20 para enteros */
  int32_t salida = KP * error + KI * propuesta_i + KD * derivada;
  if (salida > 1000) { salida = 1000; }
  else if (salida < 0) { salida = 0; }
  else { integral = propuesta_i; }
  error_ant = error;
  return salida;
}
/* USER CODE END 0 */
```

Cada 50 ms: `salida = pid_paso(600, planta);` y `planta = planta + (salida - planta) / 16;`. Imprime consigna, planta y salida. El entero trunca. Es parte del ejemplo.

Revisa el signo de la integral: `error / 20` es `error * dt` con dt = 0,05 solo si aceptas la división entera. Para no perder el error pequeño, acumula en milésimas: `integral_m += error * 50` (50 ms) y usa `integral_m / 1000` como integral en segundos. El listado de arriba es el esquema; si la integral no se mueve con errores pequeños, pasa a milésimas. Documenta cuál dejaste.

10. **Dónde.** `main.c`.
11. **Compilar y probar.** Graba y mira si `planta` se acerca a 600.
12. **Esperado, no medido.** Con P solo, puede quedarse con error. Con I, el error baja y la salida deja de estar pegada al máximo si la consigna es alcanzable. Si oscila, baja Kp o Ki. No hay una curva guardada en el repositorio.
13. **Fallos.** Se va a 0 y se queda: el signo del error está al revés. No se mueve: `dt` entero se comió la integral y Kp es 0. Oscila sin parar: ganancias altas para esta planta de juguete. Bájalas de una en una.
14. **Variación.** Escalón de consigna de 600 a 200. La salida tiene que bajar, no solo subir.
15. **Criterio.** Has visto, en el texto, un caso con error permanente sin I y un caso que se acerca con I.

## Ejemplo 2. LED y fotorresistencia

1. **Problema.** Salir del modelo sin fingir un proceso industrial.
2. **Objetivo.** La consigna es un número de ADC. El PWM de PC7 ilumina. PA1 lee el divisor de la LDR.
3. **Material.** LED y resistencia en PC7, como en el módulo 10. LDR en serie con 10 kΩ. Punto medio a PA1. La LDR puede ir a 3,3 V y la resistencia a GND, o al revés: el signo del proceso cambia, y el PID tiene que saberlo. Elige la que sube el ADC cuando sube el brillo, para que el proceso tenga ganancia positiva. Si sale al revés, invierte el error y escríbelo.
4. **Funcionamiento.** Cada 50 ms se lee PA1, se calcula el PID y se escribe el compare de TIM3 canal 2. El LED y la LDR tienen que verse: un tubo opaco o cinta, para que la luz de la sala no mande más que el LED. Sigue siendo un juguete.
5. **Dibujo.** LED como [cable-led-pc7.svg](img/cable-led-pc7.svg). LDR: CN6 pin 4 a la LDR, la LDR a PA1 (CN8 pin 2), 10 kΩ de PA1 a GND. 100 nF de PA1 a GND.
6. **Cableado.** Esos puntos. Nada de red eléctrica. La LDR no se calienta a propósito con otra fuente.
7. **Cálculos.** A oscuras, según el montaje, PA1 está cerca de 0 si la LDR está arriba y vale mucho. Con el LED encima, la LDR baja y PA1 sube. Confírmalo con una lectura cruda antes de cerrar el lazo. Si no sube al encender el LED a mano (`compare` 900), no cierres el PID.
8. **CubeMX.** TIM3 PWM en PC7, como en el módulo 10. ADC1 en PA1. Quita el DAC de PA4 si estorba en el mismo proyecto.
9. **Código.** El `pid_paso` del ejemplo 1. `salida` va a `__HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_2, (uint32_t)salida)`. La medida es el ADC, así que la consigna tiene que estar en cuentas de ADC, no en 600 de juguete, salvo que escales. Empieza con una consigna que hayas visto al poner el PWM a mitad, por ejemplo el N que imprimiste.
10. **Dónde.** `main.c`.
11. **Compilar y probar.** Primero lazo abierto: tres brillos, anota N. Luego cierra el lazo con Kp pequeño, Ki 0, Kd 0. Tapa la LDR con el dedo.
12. **Esperado, no medido.** Al tapar, el LED debe pedir más luz si la ganancia del montaje es la que crees. Al destapar, debe bajar. Si hace lo contrario, para y cambia el signo. No es un ensayo de estabilidad de un proceso.
13. **Fallos.** El LED se queda al máximo: windup, o la LDR no ve el LED y el error no baja. Acerca el LED a la LDR. La lectura no cambia: PA1 no es el punto medio. Se calienta el LED: falta la resistencia.
14. **Variación.** Luz de la sala encendida y apagada. Verás que la consigna deja de significar lo mismo. Escríbelo: la planta no está aislada.
15. **Criterio.** Has comprobado el signo en lazo abierto antes de cerrar el lazo.

## Ejemplo 3. Límite que no se queda pegado

1. **Problema.** Un cambio de consigna grande satura la salida y la integral no perdona.
2. **Objetivo.** El mismo regulador, con el anti-windup del ejemplo 1, y un escalón que no deje la salida en el máximo para siempre.
3. **Material.** El modelo del ejemplo 1, que es más limpio para ver esto. Puedes repetirlo en la LDR si el ejemplo 2 ya funciona.
4. **Funcionamiento.** Consigna 200 durante un segundo, luego 900. La salida puede pegarse a 1000 un momento. Tiene que volver cuando la medida llegue. Si la integral siguiera creciendo durante la saturación, tardaría de más.
5. **Dibujo.** No hay.
6. **Cableado.** No hay, si es el modelo.
7. **Cálculos.** Tope 0 a 1000. El código solo integra cuando `salida` no se ha recortado. Compara mentalmente con la versión que integra siempre: esa tarda más en soltar. Puedes simular las dos en el mismo programa, una cada vez.
8. **CubeMX.** El del ejemplo 1.
9. **Código.** El `pid_paso` ya recorta y solo guarda `integral` cuando no recorta. Añade un cambio de consigna a los 2 s de `HAL_GetTick`: de 200 a 900.
10. **Dónde.** El bucle.
11. **Compilar y probar.** Mira `salida` y `planta` en el monitor.
12. **Esperado, no medido.** `salida` toca 1000 y luego baja cuando `planta` se acerca a 900. Si no baja, la integral se está guardando también en saturación.
13. **Fallos.** No llega a 900 porque la planta y el tope no dan para más. Entonces la consigna no es alcanzable: bájala. El ensayo no vale si pides por encima de lo que la planta puede.
14. **Variación.** Quita el anti-windup a propósito, observa la cola de saturación y vuelve a ponerlo.
15. **Criterio.** Puedes explicar el windup con la columna de `salida` que acabas de ver, y no llamas a esto un lazo de temperatura industrial.

## Resumen

Periodo fijo, salida limitada, integral que no crece en el tope. Primero un modelo. Después un LED y una LDR, con el signo comprobado en abierto. De esa mesa no sale un ajuste para una máquina.

## Glosario

| Término | Definición |
| --- | --- |
| Consigna | El valor que quieres |
| Error | Consigna menos medida, con el signo del proceso ya acordado |
| Windup | La integral que sigue creciendo cuando la salida ya no puede más |
| Lazo abierto | El mando se pone a mano, sin regulador |

## Preguntas

**1.** ¿Un PID de esta práctica sirve para un horno?

Respuesta. No. Ni la planta, ni la medida, ni la sintonía son las de un horno.

**2.** ¿Por qué el periodo tiene que ser fijo?

Respuesta. Porque Ki y Kd están definidos por segundo. Si el bucle a veces tarda 50 ms y a veces 500, las ganancias ya no son esas.

**3.** ¿Kd es obligatorio?

Respuesta. No. El primer ensayo va con Kd = 0 para ver P e I.

## Lista de comprobación

- [ ] He visto error permanente con P solo en el modelo, o he anotado por qué mi planta no lo muestra.
- [ ] He comprobado el signo de la LDR en lazo abierto.
- [ ] La salida está limitada y la integral no crece mientras está en el tope.
- [ ] No he descrito este montaje como un lazo industrial.

## Siguiente

[Módulo 21](22-modulo-21-modbus.md): publicar un registro a un maestro, por RS-485.
