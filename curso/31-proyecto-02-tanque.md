# Proyecto P2. Tanque simulado

El nivel es una tensión de 0 a 3,3 V, no un depósito con agua junto a la placa. La bomba es un LED o un relé de baja tensión que representa el contactor. Hay marcha, paro y fallo. El watchdog del módulo 23, si ya está dado, reinicia un cuelgue. No se bombea líquido.

**No comprobado en hardware.**

## Qué reúne

Módulos 11, 17, 20 y 23. El PID es opcional: el ejemplo 1 es una marcha/paro con histéresis, que es el control que este tanque de juguete necesita. El ejemplo 3 muestra el PID del módulo 20 sobre el mismo modelo, no sobre agua.

## Material

- Potenciómetro de 10 kΩ en PA0, como nivel de 0 a 100 %. O el divisor del módulo 11 si la tensión ya viene limitada.
- LED «bomba» en PC7 con su resistencia, o el transistor y un relé de baja tensión en PB5. No un contactor de red.
- B1 como paro de emergencia de la práctica: pulsado, la bomba se queda en fallo hasta un rearme que tú definas.
- USART2 para el estado.

## Pines

| Función | Pin |
| --- | --- |
| Nivel 0 a 3,3 V | PA0, A0 |
| Bomba de juguete | PC7 LED, o PB5 por transistor |
| Paro | PC13, B1 |
| Informe | USART2 |

PA0 no lleva a la vez el lazo de 4–20 mA del módulo 27.

## Ejemplo 1. Marcha y paro por nivel

1. **Problema.** Representar un tanque que pide llenado sin montar un tanque.
2. **Objetivo.** Por debajo del 40 % la bomba se enciende. Por encima del 80 % se apaga. Entre medias, se queda como estaba.
3. **Material.** El potenciómetro y el LED de PC7.
4. **Funcionamiento.** `porcentaje = N * 100 / 4095`, entero. Estados `PARO`, `MARCHA`, `FALLO`. De PARO se pasa a MARCHA si el nivel es menor que 40 y no hay paro de emergencia. De MARCHA se pasa a PARO si el nivel es mayor que 80. B1 pasa a FALLO desde cualquiera y apaga la bomba. Rearme: soltar B1 y recibir `r` por el UART, para que no rearranque solo al soltar. Esa elección se escribe para que no sea un rearme involuntario.
5. **Dibujo.** [Potenciómetro](img/cable-potenciometro-pa0.svg) y [LED](img/cable-led-pc7.svg). Si usas relé, [transistor](img/cable-rele-transistor.svg) y no el LED de PC7 a la vez si decides que la bomba es solo el relé. Puedes dejar el LED como lámpara de marcha y el relé como «contactor» solo si los pines son distintos: LED en PC7 y bobina por PB5.
6. **Cableado.** 3,3 V en el potenciómetro. Bobina, si la hay, como en el módulo 10, sin red eléctrica.
7. **Cálculos.** 40 % de 4095 ≈ 1638. 80 % ≈ 3276. Histéresis de 40 puntos porcentuales, de diseño, para no oscilar en el umbral.
8. **CubeMX.** ADC1 en PA0. PC7 salida. PC13 entrada. USART2.
9. **Código.** Un `enum` y `tanque_paso()`, llamado desde el bucle con el tiempo de `HAL_GetTick`. Imprime el estado cuando cambie, no cien veces por segundo.
10. **Dónde.** `tanque.c` si ya partes archivos. Si no, USER CODE de `main.c`, y el módulo 17 explica cómo sacarlo luego.
11. **Compilar y probar.** Gira el potenciómetro despacio de abajo arriba y al revés.
12. **Esperado, no medido.** El LED enciende por debajo de 40, sigue encendido hasta pasar de 80 y se apaga. No parpadea en el 40.
13. **Fallos.** Oscila: no hay histéresis, los dos umbrales son iguales. No enciende: el porcentaje está al revés porque el potenciómetro está girado, y lo aceptas invirtiendo la escala en un solo sitio. B1 no lleva a fallo: lees el nivel alto como pulsado.
14. **Variación.** Añade un tiempo máximo de marcha de 20 s. Si no se alcanza el 80, pasa a FALLO. Es un estado, no un `HAL_Delay` de 20 s.
15. **Criterio.** Puedes rellenar, con el potenciómetro, las filas de marcha, paro e histéresis sin agua y sin 230 V.

## Ejemplo 2. Fallo y watchdog

1. **Problema.** Un programa colgado dejaría la bomba de juguete en el estado que tuviera, para siempre.
2. **Objetivo.** El IWDG se recarga solo en el paso del tanque. Un cuelgue provocado reinicia, y el arranque deja la bomba apagada hasta el rearme.
3. **Material.** El del ejemplo 1.
4. **Funcionamiento.** Al arrancar, el estado es FALLO si la bandera del IWDG está puesta, y PARO si no. La bomba se escribe apagada en `USER CODE BEGIN 2` antes de entrar al bucle. Recargar el IWDG dentro de `tanque_paso` vigila que ese paso siga llamándose. No lo recargues en un temporizador aparte.
5. **Dibujo.** No hay cable nuevo.
6. **Cableado.** El mismo.
7. **Cálculos.** El timeout del módulo 23, aproximado por el LSI. El paso se llama mucho antes, cada vuelta del bucle.
8. **CubeMX.** IWDG como en el módulo 23. Recuerda que un punto de ruptura largo reinicia.
9. **Código.** `HAL_IWDG_Refresh` al final de `tanque_paso`. Una letra `c` entra en `while (1) {}` para el ensayo de cuelgue. Quítela del uso normal o déjala documentada como ensayo.
10. **Dónde.** El paso y la zona 2.
11. **Compilar y probar.** Marcha normal: no se reinicia. Envía `c`: hay reinicio y la bomba queda apagada, estado FALLO, hasta `r`.
12. **Esperado, no medido.** La bomba no se queda encendida a través del reinicio. Compruébalo mirando el LED durante el hueco.
13. **Fallos.** La bomba vuelve a marcha sola: el arranque no mira la bandera y el nivel sigue bajo. El `if` inicial tiene que mandar más que el nivel, hasta el rearme.
14. **Variación.** Imprime la causa, como en el módulo 23, además del estado.
15. **Criterio.** Después de `c`, hace falta `r`. El LED no queda encendido por un reset.

## Ejemplo 3. PID sobre el modelo, no sobre el agua

1. **Problema.** Querer «control continuo» sin fingir que el potenciómetro es un depósito.
2. **Objetivo.** Aplicar el PID del módulo 20 a la planta de mentira, usando el potenciómetro solo como consigna de nivel, de 0 a 1000 unidades de juguete. La salida del PID se muestra en el ciclo de trabajo del LED, como esfuerzo de bomba, y el «nivel» que el PID ve es la planta interna, no PA0.
3. **Material.** El LED en PC7 como PWM. El potenciómetro como consigna.
4. **Funcionamiento.** Se explica en el informe: PA0 no es el nivel del proceso en este ejemplo. Es la orden del operario. El proceso es la fórmula del módulo 20. Así no se cierra un lazo mentiroso «potenciómetro que se lee a sí mismo».
5. **Dibujo.** Los mismos cables. El significado cambia y se escribe al lado.
6. **Cableado.** PWM del módulo 10 en PC7. El LED deja de ser marcha/paro digital. No uses el mismo pin como GPIO y como PWM sin cambiar el proyecto.
7. **Cálculos.** Consigna = N del ADC escalado a 0–1000. Planta y PID como en el módulo 20, con límite y anti-windup. Periodo 50 ms.
8. **CubeMX.** TIM3 canal 2 en PC7. ADC en PA0.
9. **Código.** `pid_paso` y la planta interna. Imprime consigna, planta y salida. El estado FALLO de B1 fuerza la salida a 0 y no integra.
10. **Dónde.** `main.c` o `tanque.c`.
11. **Compilar y probar.** Mueve el potenciómetro. La planta del texto debe acercarse a la consigna y el brillo debe seguir a la salida, no al potenciómetro de forma instantánea.
12. **Esperado, no medido.** Un acercamiento en el monitor. El brillo no es un nivel de líquido.
13. **Fallos.** El lazo «controla» el propio ADC del potenciómetro: has usado PA0 como medida y como consigna. Sepáralos. Oscilación: baja Kp, como en el módulo 20.
14. **Variación.** Vuelve al ejemplo 1, que es el que representa el tanque. Deja el PID como ensayo de regulador, no como el control del proyecto.
15. **Criterio.** El informe dice que no hay depósito, que no hay agua y que el PID de este ejemplo no actúa sobre una planta física.

## Pruebas mínimas

| Id | Estímulo | Esperado por diseño |
| --- | --- | --- |
| T1 | Nivel simulado 20 % | Marcha, LED o bobina activos |
| T2 | Subir del 40 al 70 | Sigue en marcha |
| T3 | Pasar de 80 | Paro |
| T4 | Bajar del 80 al 50 | Sigue en paro |
| T5 | B1 durante la marcha | Fallo y bomba off |
| T6 | Soltar B1 | Sigue en fallo hasta `r` |
| T7 | Letra `c` | Reinicio por IWDG y bomba off |
| T8 | Mirar la mesa | No hay líquido ni red eléctrica |

## Qué no demuestra

No hay tanque, no hay caudal y no hay contactor de máquina. El relé de baja tensión representa al contactor en el parte, no lo sustituye.
