# Módulo 2. Alimentación, niveles de tensión y límites eléctricos

Este módulo responde a una sola pregunta: ¿este cable se puede conectar a este pin? Todavía no hay programa. El módulo 1 dejó medidas de 5 V y de 3,3 V. Aquí se explica por qué las dos existen y qué pasa si se cruzan.

**No comprobado en hardware.** Los números salen de UM1724 Rev 17 y del datasheet DocID026415 Rev 5. No son medidas de una placa concreta. La práctica 3 te pide anotar las tuyas.

## Objetivos

Al terminar puedes:

1. Separar el raíl de 5 V de la placa del raíl de 3,3 V del microcontrolador.
2. Decir si un pin es TC, TTa o FT, y qué tensión de entrada le corresponde.
3. Distinguir un máximo absoluto de la corriente a la que el nivel de salida sigue siendo un «cero» o un «uno» firme.
4. Calcular la resistencia de un LED a partir de la hoja de ese LED.
5. Rechazar una conexión de 5 V, de 10 V o de una bobina directa a un GPIO.

## Prerrequisitos

El [módulo 1](02-modulo-01-arquitectura.md), con la revisión de tu placa anotada y las dos medidas de CN6. Hace falta el polímetro. No hace falta el compilador.

## Material

| Pieza | Para qué |
| --- | --- |
| La NUCLEO-F303RE ya identificada | Práctica 3 |
| Polímetro | Voltios de continua |
| Papel | Clasificar conexiones y hacer el cálculo |
| Hoja de un LED indicador que vayas a usar en el módulo 5 | El cálculo numérico. Si aún no la tienes, la práctica 2 deja el resultado en función de Vf e If |

No se monta el LED en esta práctica. Se calcula. Montarlo es el módulo 5, cuando el programa pueda encenderlo.

## 1. Dos tensiones en la misma tarjeta

**Analogía.** En un cuadro puedes tener un circuito de mando a 24 V y una lámpara de señal a 24 V, y al lado una fuente de instrumentos a otra tensión. Unirlas «porque las dos son tensión» quema el instrumento. Aquí el USB trae 5 V y el chip vive a 3,3 V. El regulador es la frontera.

**Técnico. Verificado.**

- Con JP5 en los pines 1-2, el USB alimenta la red de +5 V después de que el PC acepta la placa. UM1724 §7.5.1: con JP1 abierto la placa pide 300 mA. Por encima de eso hay que usar VIN o E5V.
- U4, el LD39050PU33R del esquema C05, obtiene 3,3 V de esos 5 V. UM1724 §7.5.4 limita a 500 mA lo que se puede sacar por el pin de 3,3 V.
- El microcontrolador admite en VDD de 2,0 V a 3,6 V (datasheet, tabla 19). La placa lo deja en 3,3 V. No está pensada para alimentarlo a 5 V.
- CN6 pin 5 es +5 V. CN6 pin 4 es +3,3 V. El módulo 1 midió esos dos.

El pin de 3,3 V puede usarse como salida hacia un sensor que pida poca corriente, dentro de los 500 mA del regulador y del presupuesto real del USB. No es una fuente de motores.

## 2. Máximo absoluto y condición de trabajo

**Analogía.** La corriente de disparo de un automático no es la corriente a la que quieres trabajar todo el día. Si te acercas al disparo, el cable se calienta y el automático puede saltar. El máximo absoluto del chip es ese disparo: pasarlo puede dañar el componente aunque dure poco. La corriente de trabajo es más baja, la que mantiene un nivel lógico reconocible.

**Técnico. Verificado** en el datasheet, tabla 17, máximos absolutos:

| Símbolo | Qué limita | Máximo |
| --- | --- | --- |
| IIO(PIN) | Corriente que un pin absorbe o entrega | 25 mA |
| ΣIIO(PIN) | Suma de todos los pines y pines de control | 80 mA |
| ΣIVDD | Suma de toda la corriente que entra por las alimentaciones | 160 mA |
| IINJ(PIN) en un pin FT | Corriente inyectada | −5 mA a 0 |
| IINJ(PIN) en un pin TC o TTa | Corriente inyectada | ±5 mA |
| ΣIINJ(PIN) | Suma de las corrientes inyectadas | ±25 mA |

Inyectar corriente es aplicar una tensión fuera del rango del pin y dejar que entre o salga corriente por la protección interna. No es un modo de uso. Es un accidente que el fabricante acota.

El mismo datasheet, en el apartado de corriente de salida, dice con claridad que los GPIO pueden absorber o entregar hasta ±8 mA, y hasta ±20 mA si se acepta un nivel de salida más degradado. La tabla 67 concreta ese segundo caso: a 20 mA, VOL puede subir hasta 1,3 V y VOH puede bajar hasta VDD − 1,3 V. Un «cero» de 1,3 V ya no es un cero cómodo para otro circuito digital.

Por eso este curso dimensiona los LED y las bases de transistor alrededor de **8 mA o menos** por pin, y trata 20 mA como zona degradada y 25 mA como límite que no se usa. La suma de 80 mA sigue aplicando: diez pines a 8 mA ya la igualan.

PC13, PC14 y PC15 son un caso aparte. La nota 2 de la tabla de pines dice que pasan por un interruptor que solo absorbe 3 mA, que no deben usarse como fuente de corriente para un LED y que, en salida, no deben pasar de 2 MHz con 30 pF. El pulsador azul puede estar en PC13. Un LED, no.

## 3. Qué tensión admite cada tipo de pin

**Analogía.** Hay bornas de mando que aceptan 24 V y bornas de señal que solo aceptan la tensión del instrumento. El número de la borna no lo dice: lo dice el plano. Aquí el plano es la columna «I/O structure» de la tabla 13 del datasheet.

**Técnico. Verificado** en la tabla 19:

| Tipo | Tensión de entrada permitida en trabajo | En esta placa, ejemplos |
| --- | --- | --- |
| TC | De −0,3 V a VDD + 0,3 V | PC13 |
| TTa | De −0,3 V a VDDA + 0,3 V | PA0, PA1, PA2, PA3, PA4, PA5, PB0, PC0, PC1 |
| FT y FTf | De −0,3 V a 5,5 V | PA9, PA10, PA11, PA12 |

Con VDD y VDDA en 3,3 V, un pin TTa se queda cerca de 3,6 V como techo. Un divisor mal hecho que deje pasar 5 V no «casi entra»: se sale.

Un pin FT tolera 5 V en la **entrada**. La nota 4 de la tabla 66 añade que, para sostener una tensión por encima de VDD + 0,3 V, hay que desactivar el pull-up y el pull-down internos. Y la salida de ese pin, cuando el programa lo pone a uno, sigue siendo próxima a 3,3 V, no a 5 V. Un circuito que exija un uno de 5 V no se conforma con un pin FT.

BOOT0 admite de 0 a 5,5 V. En la placa está a nivel bajo salvo que se puentee como indica UM1724.

## 4. El presupuesto del USB y el de VIN

**Verificado** en UM1724, tablas 6 y 7.

| Fuente | Dónde | Qué no pasar |
| --- | --- | --- |
| USB, JP1 abierto | CN1 | 300 mA para la placa y lo que cuelgues de ella |
| USB, JP1 cerrado | CN1 | 100 mA |
| VIN | CN6 pin 8 o CN7 pin 24 | 7 V a 12 V. A 7 V, 800 mA de entrada. Entre 7 V y 9 V, 450 mA. Entre 9 V y 12 V, 250 mA |
| E5V | CN7 pin 6 | 4,75 V a 5,25 V, 500 mA |
| +3,3 V como salida | CN6 pin 4 | 500 mA del regulador U4, y además lo que el USB pueda dar si esa es la fuente |

La secuencia con fuente externa, UM1724 §7.5.2, es obligatoria: JP5 en pines 2-3, JP1 quitado, conectar VIN o E5V, encender la fuente, ver LD3, y solo después el USB. La fuente tiene que ser SELV según la norma que cita el manual. Un cargador de teléfono sin datos no enumera: LD3 se queda apagado salvo que JP1 esté cerrado, y ese modo es el de 100 mA.

## 5. Cálculo de un LED, con los datos de su hoja

Un LED no se alimenta «a 3,3 V» como una resistencia. Hay que vencer su caída Vf y limitar la corriente con una resistencia.

La corriente que buscamos, If, la eliges por debajo de 8 mA y por debajo de la corriente continua que la hoja del LED permita. La tensión del pin a nivel alto es, en la zona de 8 mA y con VDD entre 2,7 V y 3,6 V, al menos VDD − 0,4 V (tabla 67, condición de VOH). Para no quedarte corto de corriente por ser optimista, el cálculo de la resistencia usa 3,3 V como tensión de fuente y acepta que la corriente real será un poco menor. Es un cálculo de diseño, no una medida.

Fórmula:

```text
R = (VDD − Vf) / If
```

**Ejemplo con supuestos declarados, no medidos.** Supón que la hoja de tu LED rojo dice Vf = 2,0 V cuando If = 5 mA, y que 5 mA está dentro de lo que esa hoja permite de forma continua.

```text
R = (3,3 V − 2,0 V) / 0,005 A = 1,3 V / 0,005 A = 260 Ω
```

El valor comercial inmediato por encima es 270 Ω. Con 270 Ω:

```text
If = 1,3 V / 270 Ω = 4,8 mA
```

Potencia en la resistencia:

```text
P = 4,8 mA × 1,3 V = 6,3 mW
```

Una resistencia de 1/4 W, que son 250 mW, va sobrada. Si tu hoja dice otro Vf u otra corriente, se repite la cuenta. No se reutiliza 510 Ω, que es R31 del LED de la placa en el esquema C05, salvo que el cálculo caiga ahí.

El LED externo del módulo 5 irá en PC7, no en PC13.

## Práctica 1. Aprobar o rechazar una conexión

**Problema.** La mayoría de las placas dañadas en un curso se dañan antes del primer programa, por un cable de 5 V en un pin analógico.

**Objetivo.** Clasificar conexiones sin enchufarlas.

**Material.** Esta tabla y el mapa de pines del índice. Nada conectado.

Marca cada fila como aceptable o rechazada, y escribe el motivo con el tipo de pin.

| Propuesta | Tu decisión, antes de mirar abajo |
| --- | --- |
| Cursor de un potenciómetro de 10 kΩ entre 3,3 V y GND, al pin PA0 | |
| Un pulsador que lleva 5 V de un Arduino clásico al pin PA0 | |
| Un receptor de 5 V cuya salida entra en PA9, con el pull interno desactivado | |
| La bobina de un relé de 5 V entre PA8 y GND | |
| El pin de 3,3 V de la placa a la alimentación de un sensor que pide 15 mA | |

**Respuestas.**

1. Aceptable. PA0 es TTa y el cursor se queda entre 0 y 3,3 V. Es la práctica del módulo 11.
2. Rechazada. PA0 no admite 5 V. Hace falta un divisor o un nivel de 3,3 V.
3. Aceptable como entrada, porque PA9 es FTf y 5 V está por debajo de 5,5 V, siempre que el pull interno esté desactivado. La respuesta del STM32 hacia ese circuito seguirá siendo de 3,3 V: si el otro lado no la entiende, falta un desplazador en ese sentido.
4. Rechazada. La bobina pide una corriente y un pico al soltar que no corresponden a un GPIO. Hace falta transistor y diodo. Es el módulo 10.
5. Aceptable en corriente, porque 15 mA cabe en los 500 mA de U4 y en los 300 mA del USB, siempre que el resto del montaje no se coma el presupuesto. El sensor tiene que ser de 3,3 V.

**Criterio.** Las cinco decisiones coinciden con la tabla y puedes decir el tipo de pin de PA0 y de PA9 sin mirar.

## Práctica 2. Resistencia de tu LED

**Problema.** El módulo 5 va a pedir un LED externo. La resistencia se decide ahora, con la hoja delante.

**Objetivo.** Dejar escritos Vf, If, R comercial y la potencia.

**Pasos.**

1. En la hoja del LED, anota Vf a la corriente que elijas. Si la hoja da Vf a 20 mA y tú vas a usar 5 mA, usa el Vf de 5 mA si viene, o indica que estás aproximando.
2. Elige If ≤ 8 mA y ≤ la corriente continua de la hoja.
3. Calcula R = (3,3 − Vf) / If y sube al valor comercial siguiente de la serie E12: 220, 270, 330, 390, 470, 510, 680, 1000 Ω.
4. Recalcula If con ese valor y comprueba que no te pasaste de la hoja ni de 8 mA.
5. Calcula la potencia y comprueba que es menor que la de la resistencia que vas a comprar.

**Resultado esperado.** Una línea en el cuaderno: «LED …, Vf = … V a … mA, R = … Ω, If resultante = … mA, P = … mW». No hay un número único correcto para todos los LED.

**Si todavía no tienes la hoja.** Repite el ejemplo de 2,0 V y 5 mA, márcalo como supuesto, y sustitúyelo antes del módulo 5.

## Práctica 3. Presupuesto de corriente

**Problema.** Varios LED «pequeños» y un sensor caben pin a pin y no caben en la suma, o no caben en los 300 mA del USB si se les suma otra cosa.

**Objetivo.** Sumar antes de montar.

**Datos de este ejercicio, supuestos de diseño.** Tres LED a 5 mA cada uno, sacados de tres pines. Un sensor a 15 mA desde el pin de 3,3 V. El microcontrolador en marcha gasta, además, su propia corriente de VDD: no la incluyas como si fuera cero, pero tampoco inventes una cifra. El módulo 25 la medirá en JP6. Para este ejercicio suma solo lo que cuelgas fuera.

**Cuentas.**

```text
Pines: 3 × 5 mA = 15 mA, frente a 80 mA de suma y 8 mA por pin.
Sensor: 15 mA desde el regulador de 3,3 V, no desde un GPIO.
USB: la placa ya está dentro de los 300 mA. 15 mA del sensor más los LED,
que salen de los 3,3 V y por tanto también del USB, son unas decenas de mA.
```

Con solo esto, el presupuesto del curso básico cabe. Deja de caber en cuanto un motor, un servo o una bobina se alimentan del USB. Esos van a fuente aparte.

**Medida.** Repite, si quieres, las dos tensiones del módulo 1 y anótalas otra vez. No midas corriente colocando el polímetro en amperios entre 3,3 V y GND: eso es un cortocircuito.

**Criterio.** En el cuaderno está la suma de los tres LED, la del sensor, y una frase que diga si un servo de 5 V entra o no en este presupuesto. La respuesta es que el servo no se alimenta del pin ni se da por sentado que quepa en el USB.

## Resumen

- 5 V es la red de la placa. 3,3 V es la red del chip. No se cruzan.
- 25 mA por pin y 80 mA en total son máximos absolutos. El trabajo de un LED se queda en unos 8 mA, donde el nivel de salida sigue siendo firme. A 20 mA el cero puede valer 1,3 V.
- Un pin TTa no ve 5 V. Un pin FT puede ver hasta 5,5 V en la entrada, con el pull interno desactivado, y su salida sigue siendo de 3,3 V.
- PC13 no enciende un LED.
- El USB, con JP1 abierto, son 300 mA para todo. Un motor no entra en esa cuenta.
- La resistencia del LED se calcula con la hoja del LED.

## Glosario

| Término | Definición |
| --- | --- |
| Raíl | Nudo de alimentación. Aquí hay raíl de 5 V y raíl de 3,3 V |
| VDD | Alimentación del núcleo y de los pines digitales. 3,3 V en esta placa |
| VDDA | Alimentación analógica. En la placa queda unida a VDD por SB57, y en el chip de 64 pines VREF+ está unido por dentro a VDDA |
| Máximo absoluto | Límite que no se debe pasar. No es la corriente de diseño |
| GPIO | Pin programable como entrada o salida |
| Push-pull | Salida que conecta el pin a VDD o a GND mediante transistores. Se usa en el módulo 5 |
| Pull-up | Resistencia que lleva el pin a nivel alto cuando nadie lo fuerza. La interna vale entre 25 kΩ y 55 kΩ |
| Vf | Caída de tensión del LED a una corriente dada, sacada de su hoja |
| SELV | Muy baja tensión de seguridad, la condición que UM1724 pide a una fuente externa |

## Preguntas

**1.** ¿Por qué el LED de la placa lleva 510 Ω y el tuyo puede llevar otro valor?

Respuesta. 510 Ω es R31 del esquema C05, elegido por ST para LD2. Tu LED tiene otro Vf y otra corriente. Se calcula.

**2.** PA9 admite 5 V. ¿Puedo alimentar un relé de 5 V desde PA9?

Respuesta. No. Que la entrada tolere 5 V no aumenta la corriente que el pin puede entregar, ni convierte la salida en 5 V. El relé va con transistor y diodo.

**3.** ¿Diez LED a 8 mA caben porque cada pin aguanta 25 mA?

Respuesta. No. Diez por 8 mA son 80 mA, que es el máximo absoluto de la suma, no un objetivo. Además 8 mA es el borde de la zona de nivel firme. Se bajaría la corriente por LED o se moverían algunas cargas a transistores.

**4.** ¿El pin de 3,3 V y un pin GPIO a nivel alto son la misma fuente?

Respuesta. No. El pin de 3,3 V sale del regulador U4, hasta 500 mA. Un GPIO sale de un transistor interno del chip, en la zona de unos 8 mA si quieres un nivel alto de verdad, y nunca por encima del máximo absoluto de 25 mA.

**5.** ¿Qué hago si la hoja del LED solo da Vf a 20 mA?

Respuesta. No pongas 20 mA. O buscas la curva y lees Vf a 5 mA, o declaras que usas el Vf de 20 mA como aproximación y compruebas la corriente real en el módulo 5 midiendo la caída en la resistencia. Esa medida será tuya; no está en este texto.

## Ejercicios

1. Recalcula el ejemplo si Vf = 1,8 V e If = 2 mA. Tiene que salirte R = 750 Ω antes de normalizar, y 820 Ω como comercial siguiente. If con 820 Ω: 1,5 V / 820 Ω = 1,8 mA.
2. Un compañero quiere leer un potenciómetro alimentado a 5 V con PA0, «porque el ADC es de 12 bits y tendrá resolución». Explica por qué la resolución no compensa la tensión.
3. JP5 está en los pines 2-3 y solo hay cable USB. ¿Qué esperas de LD3 según el módulo 1 y la sección 7.5? Que no haya 5 V en la parte del microcontrolador, porque esa posición espera VIN o E5V.

## Lista de comprobación

- [ ] Sé qué pin de CN6 es 5 V y cuál es 3,3 V.
- [ ] Puedo clasificar PA0, PC13 y PA9.
- [ ] Tengo la resistencia de mi LED calculada, o el ejemplo marcado como supuesto.
- [ ] Sé que 25 mA no es la corriente de diseño.
- [ ] No he conectado 5 V a un pin TTa ni una bobina a un GPIO.

## Módulo siguiente

El módulo 3 instala el proyecto en VS Code y graba el primer parpadeo de PA5. El procedimiento de herramientas está en [Fuentes y entorno](00-fuentes-y-entorno.md). La lección, con los tres ejemplos y el código, se publica en la siguiente entrega. La ficha ya dice qué contiene.
