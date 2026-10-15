# Módulo 25. Bajo consumo

Medir cuánto entra al microcontrolador, y bajar ese gasto cuando no hay trabajo. Sigue siendo un prototipo de mesa. No es un diseño de pila ni un número para un catálogo.

**No comprobado en hardware.** Este texto no trae una corriente de ejemplo. La que anotes es la tuya.

## Objetivos

- Medir la corriente de Run con el polímetro en JP6, como dice UM1724 §7.8.
- Entrar en Sleep, y anotar la corriente.
- Despertar con B1, y saber qué impide bajar más.

## Prerrequisitos

Polímetro que mida miliamperios. JP6 accesible. El módulo 23 puede estar en el mismo programa solo si recuerdas que un IWDG activo despierta o reinicia: para este ensayo, deja el IWDG desactivado. No quieres un reinicio a mitad de la medida.

## JP6

**Analogía.** JP6 es el único hilo por el que la corriente del microcontrolador pasa cuando quieres contarla. Abrirlo es cortar ese hilo. Sin el amperímetro en su lugar, el chip se queda sin alimentación. El ST-LINK puede seguir encendido: no es la corriente que estás midiendo.

**Técnico. Verificado en UM1724 §7.8.** JP6 une la red de 3,3 V con VDD del MCU. Con el puente puesto, el chip se alimenta. Para medir, se quita el puente y se pone el amperímetro en serie, en la escala de miliamperios, y solo entonces se interpreta la lectura. Si el puente está quitado y no hay amperímetro, el MCU está apagado. LD3 puede seguir indicando 5 V. No confundas las dos cosas.

El modo de esta lección es Sleep: el núcleo se para y los periféricos que tengan reloj pueden seguir. Stop apaga más relojes y exige mirar cómo se despierta y cómo se rearma el reloj de sistema. El capítulo de potencia de RM0316 es la referencia antes de cambiar Sleep por Stop. Si tu lectura de ese capítulo te lleva a Stop, anota el modo y no mezcles los dos procedimientos. El código de abajo es Sleep.

En placas C-02 o posteriores, el MCO de 8 MHz del ST-LINK entra por PF0 (SB16 y SB50 cerrados, SB55 abierto, UM1724 tabla 10). Ese reloj sigue presente. No esperes la corriente de un chip con todos los relojes externos apagados. El depurador, si está conectado, también impide el mínimo. Para anotar la corriente, sal del modo depuración y deja el programa corriendo, o la lectura será la del chip con el SWD activo. Dilo en el cuaderno.

ES0261, sección de sistema, se consulta antes de afirmar que un modo de bajo consumo despierta como dice el manual. Si tu revisión describe un límite, anótalo y no publiques la corriente como si el modo hubiera sido el ideal.

## Ejemplo 1. Corriente en Run

1. **Problema.** No saber cuánto entra antes de hablar de «bajo consumo».
2. **Objetivo.** Medir la corriente con el programa en el bucle, LD2 conmutando, sin depurador conectado en el momento de la lectura.
3. **Material.** Polímetro en miliamperios. Cables cortos en JP6.
4. **Funcionamiento.** El programa no entra en Sleep. Solo vive, para tener la referencia.
5. **Dibujo.** No hay un SVG: JP6 está en la placa. Mira la serigrafía y la figura de UM1724 §7.8 antes de quitar el puente.
6. **Cableado.**

| Paso | Acción |
| --- | --- |
| 1 | Programa grabado y depurador cerrado |
| 2 | Polímetro en mA, puntas listas |
| 3 | Quitar JP6 y, en el acto, poner el amperímetro en su lugar |
| 4 | Leer y anotar |
| 5 | Volver a poner el puente al terminar |

No dejes JP6 abierto al guardar la placa.

7. **Cálculos.** No hay un valor previsto en este texto. Anota el rango del polímetro que usaste.
8. **CubeMX.** Reloj de 72 MHz como el resto del curso. PA5 salida. Sin IWDG.
9. **Código.** El parpadeo con `HAL_Delay(500)` basta como carga conocida.
10. **Dónde.** `main.c`.
11. **Compilar y probar.** Graba, desconecta la sesión de depuración, mide.
12. **Esperado, no medido.** Una corriente estable en la escala de miliamperios, que tú anotas. No la copies de otro modelo de Nucleo.
13. **Fallos.** Lectura cero y el chip muerto: JP6 está abierto sin el amperímetro, o el polímetro está en la escala equivocada y su fusible se abrió. LD3 apagado: eso es el 5 V, no JP6. Corriente que cambia con el LED: normal, es PA5. Anota con el LED apagado y con el LED encendido si quieres separarlas.
14. **Variación.** Para el bucle en un `while(1)` vacío, sin conmutar, y anota la diferencia. Sigue siendo Run.
15. **Criterio.** Tienes un número tuyo, con el puente repuesto al acabar.

## Ejemplo 2. Sleep

1. **Problema.** El núcleo no tiene nada que hacer entre dos despertares.
2. **Objetivo.** Entrar en Sleep y anotar la corriente en las mismas condiciones que el ejemplo 1.
3. **Material.** El mismo amperímetro.
4. **Funcionamiento.** `HAL_PWR_EnterSLEEPMode` con el regulador principal encendido y `WFI`. El núcleo espera una interrupción. Sin una interrupción, se queda ahí: por eso el ejemplo 3 añade B1. Para este ejemplo puedes despertar con el SysTick si sigue activo: entonces Sleep dura poco entre ticks y la corriente media no es la de un Sleep profundo. Para ver el efecto, desactiva la interrupción del SysTick antes de dormir y acepta que `HAL_GetTick` se congela. Al despertar, la vuelves a activar. Documenta esa elección.
5. **Dibujo.** No hay.
6. **Cableado.** El de JP6, igual que el ejemplo 1.
7. **Cálculos.** No hay un objetivo numérico. La comparación es «menor que mi medida de Run», no «igual a la del datasheet», porque la placa tiene ST-LINK, LED y el MCO.
8. **CubeMX.** Sin periféricos de más. No inicies el USB de dispositivo ni el CAN.
9. **Código.**

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  HAL_SuspendTick();
  HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);
  HAL_ResumeTick();
  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
  HAL_Delay(200);
  /* USER CODE END WHILE */
```

Sin el ejemplo 3, el `WFI` puede no volver si no queda ninguna interrupción. No dejes el programa así sin una fuente de despertar. Pasa al ejemplo 3 antes de dar la medida por hecha, o añade un temporizador que ya sepas que interrumpe.

10. **Dónde.** El bucle.
11. **Compilar y probar.** Mide otra vez en JP6, sin depurador.
12. **Esperado, no medido.** Una corriente que tú anotas al lado de la de Run. Si no baja, el núcleo no está durmiendo: el SysTick lo despierta al momento o no llegaste a `EnterSLEEPMode`.
13. **Fallos.** Corriente igual a Run: no duerme. Placa que no vuelve: no hay interrupción. JP6 abierto al desconectar el polímetro: el chip se apaga y creerás que el modo es «corriente cero». No cuentes esa lectura.
14. **Variación.** Si tras leer RM0316 prefieres Stop, sustituye la llamada por `HAL_PWR_EnterSTOPMode` y, al volver, reconfigura el reloj de sistema como indique el ejemplo que CubeMX o el manual den para salir de Stop. No des por hecho que sigue a 72 MHz. Anota el modo real.
15. **Criterio.** Dos números en el cuaderno, Run y Sleep, medidos por ti.

## Ejemplo 3. Despertar con B1

1. **Problema.** Salir del sueño con el pulsador, no con un reset.
2. **Objetivo.** Dormir hasta que B1 baje, conmutar LD2 y volver a dormir.
3. **Material.** B1. El amperímetro, si sigues midiendo.
4. **Funcionamiento.** EXTI en PC13, flanco de bajada, como en el módulo 9. Esa interrupción es la que cumple el `WFI`. La callback puede estar vacía: basta con que exista la interrupción. Al volver, se conmuta LD2.
5. **Dibujo.** No hay cable nuevo.
6. **Cableado.** PC13 interno, SB17 cerrado.
7. **Cálculos.** No hay.
8. **CubeMX.** PC13 como EXTI, NVIC habilitado. Sin IWDG.
9. **Código.** La callback vacía de usuario, sin `HAL_Delay`. El bucle del ejemplo 2, que ahora sí tiene quién lo despierte. Quita el `HAL_Delay(200)` si quieres pasar casi todo el tiempo dormido; deja una conmutación al despertar para ver que volviste.
10. **Dónde.** `main.c` y la callback de EXTI, una sola definición.
11. **Compilar y probar.** Sin depurador. LD2 cambia al pulsar B1. Mide la corriente entre pulsaciones.
12. **Esperado, no medido.** Quieto, duerme. Al pulsar, un cambio de LED y otra vez a dormir. La corriente es la tuya.
13. **Fallos.** No despierta: NVIC o el flanco. Despierta solo: el pin flota. El pull de la placa debería impedirlo si SB17 está cerrado. Corriente que no baja: el depurador sigue conectado, o el MCO y el ST-LINK dominan la lectura porque estás midiendo en otro sitio que no es JP6. Confirma que las puntas están en JP6 y no en el USB.
14. **Variación.** Anota qué quitaste (depurador, IWDG, periféricos) y qué no puedes quitar en esta placa (MCO en PF0 mientras los puentes de reloj sigan como de fábrica). No abras esos puentes en este módulo.
15. **Criterio.** El despertar es B1, y el cuaderno dice qué se dejó encendido a propósito.

## Resumen

JP6 en serie con el amperímetro, puente repuesto al terminar. Sleep con despertar por B1. Sin una corriente de ejemplo publicada. El MCO de la placa C-02 en adelante sigue ahí.

## Glosario

| Término | Definición |
| --- | --- |
| Run | El núcleo ejecuta instrucciones |
| Sleep | El núcleo parado, a la espera de una interrupción |
| JP6 | El puente de VDD del MCU. Abierto y sin amperímetro, el MCU se apaga |
| WFI | Instrucción de esperar a una interrupción |

## Preguntas

**1.** ¿Una lectura de 0 mA con JP6 vacío demuestra un buen modo de bajo consumo?

Respuesta. No. Demuestra que el chip no está alimentado.

**2.** ¿Por qué no publico una corriente típica?

Respuesta. Porque depende de tu placa, del depurador y del MCO, y esta redacción no la midió.

**3.** ¿Stop y Sleep son la misma llamada?

Respuesta. No. Si cambias a Stop, el reloj de sistema al volver forma parte del procedimiento.

## Lista de comprobación

- [ ] He anotado la corriente de Run y la de Sleep, medidas en JP6.
- [ ] He vuelto a colocar el puente.
- [ ] B1 despierta el programa.
- [ ] He escrito qué relojes dejé activos, entre ellos el MCO si la placa es C-02 o posterior.

## Siguiente

[Módulo 26](27-modulo-26-hal-ll-registros.md): la misma salida de PA5 en tres niveles de acceso.
