# Índice, mapa de pines y matriz de materiales

Esta página es el contrato del curso. Los módulos que todavía no están escritos respetarán este mapa. Si una práctica futura necesita mover un pin, se actualizará aquí antes de publicar el módulo.

Nada de esta página se ha ejecutado en una tarjeta. Las columnas de pin salen de UM1724 Rev 17 y del datasheet DocID026415 Rev 5. La columna «por qué este pin» es una **convención de este curso**.

## Cómo está organizado

| Nivel | Módulos | Qué se espera al terminarlo |
| --- | --- | --- |
| Básico | 1 a 7 | Encender, leer un pulsador y hablar por el puerto serie sin dañar la placa |
| Intermedio | 8 a 16 | Tiempo, interrupciones, PWM, analógico, buses e encoder |
| Avanzado | 17 a 28 | Programa partido en estados, FreeRTOS, control, buses de campo y un prototipo documentado |
| Integradores | P1 a P4 | Cuatro montajes que reutilizan los módulos, sin pins nuevos en conflicto |

Cada módulo, cuando se publique, traerá objetivos, prerrequisitos, teoría en dos niveles, prácticas, resumen, glosario, preguntas con respuesta explicada, ejercicios y una lista de comprobación.

Los módulos prácticos traen al menos tres ejemplos de dificultad creciente. Los conceptuales traen ejercicios guiados sobre la placa. El formato de cada ejemplo con hardware es el de quince puntos pedido para el curso: problema, objetivo, materiales, explicación, dibujo, tabla de cableado, cálculos, CubeMX, código completo, sitio del código, prueba en VS Code, resultado esperado, diagnóstico, variaciones y criterios de aceptación.

Cada módulo tiene ahora una ficha con el problema que resuelve, lo que se sabe al terminar, las tres prácticas, los pines y el límite que no se cruza. Las fichas están en [Fichas de los módulos](01b-fichas-modulos.md). El texto completo, con procedimientos, está escrito para el módulo 1 y para el módulo 2. Del 3 al 28 la ficha fija el contenido; el desarrollo línea a línea llega en la entrega de ese módulo.

## Índice

### Nivel básico

| Módulo | Título | Estado de esta entrega |
| --- | --- | --- |
| 1 | Arquitectura de la tarjeta y función de cada parte | Escrito |
| 2 | Alimentación, niveles de tensión y límites eléctricos | Escrito |
| 3 | Instalación y primer proyecto | Planificado |
| 4 | Fundamentos de C aplicados a STM32 | Planificado |
| 5 | GPIO: salidas, entradas, pull-up, pull-down y antirrebote | Planificado |
| 6 | Depuración y diagnóstico | Planificado |
| 7 | UART y terminal serie | Planificado |

### Nivel intermedio

| Módulo | Título | Estado |
| --- | --- | --- |
| 8 | Temporizadores, medida de tiempo y programas que no se quedan bloqueados | Planificado |
| 9 | Interrupciones y prioridades | Planificado |
| 10 | PWM y mando de cargas con una etapa externa | Planificado |
| 11 | ADC: lectura, resolución, muestreo y calibración | Planificado |
| 12 | DAC. Está en el chip y sale a un conector | Planificado |
| 13 | I2C, sensores y una pantalla compatible | Planificado |
| 14 | SPI y un dispositivo externo | Planificado |
| 15 | DMA y adquisición que no ocupa al núcleo a cada muestra | Planificado |
| 16 | Encoder, cuenta de pulsos y velocidad | Planificado |

### Nivel avanzado

| Módulo | Título | Estado |
| --- | --- | --- |
| 17 | Máquinas de estados y programa partido en módulos | Planificado |
| 18 | FreeRTOS: tareas, colas, semáforos y sincronización | Planificado |
| 19 | Filtrado digital | Planificado |
| 20 | PID sobre una planta de baja tensión o un modelo en el propio programa | Planificado |
| 21 | Modbus RTU con un transceptor RS-485 externo | Planificado |
| 22 | CAN con transceptor externo y una segunda estación | Planificado |
| 23 | Watchdog, fallos y recuperación | Planificado |
| 24 | Memoria no volátil y parámetros que sobreviven al apagado | Planificado |
| 25 | Bajo consumo | Planificado |
| 26 | HAL, LL y registros: cuándo vale cada uno | Planificado |
| 27 | Interfaces para señales industriales | Planificado |
| 28 | Pruebas, documentación y preparación de un prototipo | Planificado |

### Proyectos integradores

| Proyecto | Título | Se apoya en |
| --- | --- | --- |
| P1 | Estación de temperatura: lectura, pantalla y alarma | 11, 13, 5, 17 |
| P2 | Tanque: nivel simulado, estados de bomba y fallos | 11, 17, 20, 23 |
| P3 | Monitor de motor: RPM, una señal analógica y alarmas | 16, 11, 7 |
| P4 | Nodo de adquisición: medidas, parámetros y Modbus RTU | 15, 21, 24 |

## Periféricos que sí están, y dónde se usan

**Verificado** en el datasheet de la familia STM32F303xD/E, tabla 2, columna del encapsulado de 64 pines con 512 KB de Flash.

| Periférico | ¿Está en el STM32F303RET6? | ¿Sale en esta tarjeta sin soldar puentes? | Módulo |
| --- | --- | --- | --- |
| GPIO | Sí, 51 líneas | La mayoría, por Arduino o por Morpho. PA2, PA3, PA13 y PA14 tienen dueño | 5 |
| Temporizadores TIM1, TIM8, TIM2, TIM3, TIM4, TIM15, TIM16, TIM17 y dos básicos | Sí | Varios canales llegan a CN5 y CN9 | 8, 10, 16 |
| Interrupciones del núcleo | Sí | No es un conector | 9 |
| ADC, cuatro unidades, 22 canales en LQFP64 | Sí | A0 a A5, y más canales por Morpho | 11, 15 |
| DAC, dos canales | Sí. PA4 es DAC1_OUT1 y PA5 es DAC1_OUT2 | PA4 está en A2. PA5 está ocupado por LD2 | 12 |
| Comparadores y operacionales | Sí, 7 y 4 | Varios pines analógicos los comparten. Se usarán solo si el módulo lo necesita y el pin sigue libre | 11, 27 |
| I2C1 en PB8 y PB9 | Sí | D15 y D14, siempre | 13 |
| SPI2 en PB13, PB14, PB15 y PB12 | Sí, función alternativa AF5 del datasheet, tabla 14 | Morpho CN10, pines 30, 28, 26 y 16 | 14 |
| DMA, 12 canales | Sí | No es un conector | 15 |
| USART2 hacia el PC | Sí | Por el USB del ST-LINK, no por D0/D1 | 7 |
| USART1 en PA9 y PA10 | Sí | D8 y D2 | 7, enlace con ESP32 |
| CAN en PA11 y PA12 | Sí, funciones alternativas del datasheet | Morpho CN10 pines 14 (PA11) y 12 (PA12). Hace falta transceptor | 22 |
| USB full-speed del propio STM32 | Sí, en PA11 y PA12 | No hay conector USB de dispositivo en la zona del MCU. Choca con el CAN de este curso, así que no hay módulo de USB de dispositivo | — |
| FSMC | No en el STM32F303Rx | No aplica | — |
| Wi-Fi, Ethernet, RS-485, CAN físico | No están en la tarjeta | Hace falta un módulo externo | 21, 22, 27 |

PB8 y PB9 también pueden ser CAN_RX y CAN_TX. Este curso no los usa para CAN, porque ya son el I2C de los módulos de pantalla. El CAN va por PA11 y PA12.

## Mapa de pines que el curso se compromete a respetar

La posición de fábrica de los puentes es la de UM1724, tabla 10: el estado por defecto es el que el manual marca, y las prácticas no piden soldar nada en los módulos básicos.

| Señal | Conector y pin | Uso en el curso | No usar a la vez para |
| --- | --- | --- | --- |
| PA5 | CN5 pin 6, D13. También CN10 pin 11 | LED verde LD2. PWM de brillo del propio LED | SPI1_SCK, DAC1_OUT2 |
| PC13 | CN7 pin 23. Pulsador B1, SB17 cerrado | Entrada de usuario, activa a nivel bajo | Una salida. El datasheet prohíbe usarlo como fuente de corriente |
| PA2 | No está en D1 mientras SB62 esté abierto | USART2_TX hacia el ST-LINK | Un sensor en D1 |
| PA3 | No está en D0 mientras SB63 esté abierto | USART2_RX desde el ST-LINK | Un sensor en D0 |
| PA9 | CN5 pin 1, D8. También CN10 pin 21 | USART1_TX hacia un ESP32 u otro 3,3 V | — |
| PA10 | CN9 pin 3, D2. También CN10 pin 33 | USART1_RX | — |
| PA0 | CN8 pin 1, A0. Tipo TTa | Potenciómetro y señales de 0 a 3,3 V | 5 V |
| PA1 | CN8 pin 2, A1. Tipo TTa | Segunda entrada analógica, nivel simulado | 5 V |
| PA4 | CN8 pin 3, A2. Tipo TTa | DAC1_OUT1 cuando haya módulo de DAC. Hasta entonces, entrada analógica | DAC y ADC a la vez |
| PB0 | CN8 pin 4, A3. Tipo TTa | Entrada analógica de reserva | 5 V |
| PC1 | CN8 pin 5, A4, con SB56 cerrado | Entrada analógica | I2C. PB9 no está aquí de fábrica |
| PC0 | CN8 pin 6, A5, con SB51 cerrado | Entrada analógica | I2C. PB8 no está aquí de fábrica |
| PB8 | CN5 pin 10, D15. También CN10 pin 3 | I2C1_SCL | CAN en este mismo pin |
| PB9 | CN5 pin 9, D14. También CN10 pin 5 | I2C1_SDA | CAN en este mismo pin |
| PB6 | CN5 pin 3, D10 | Chip select de SPI2 si hace falta un NSS por software, o GPIO | No es el SCK |
| PC7 | CN5 pin 2, D9 | TIM3_CH2, PWM de un LED externo | — |
| PB4 | CN9 pin 6, D5 | TIM3_CH1, PWM de reserva. También es SWO si se depura por traza | Traza SWO y PWM a la vez |
| PB10 | CN9 pin 7, D6 | TIM2_CH3, servo educativo | — |
| PB3 | CN9 pin 4, D3 | Libre como GPIO. Es el SWO del conector CN4 | No cortar SB15 sin motivo |
| PA8 | CN9 pin 8, D7 | GPIO de propósito general | — |
| PB5 | CN9 pin 5, D4 | GPIO de propósito general | — |
| PB13 | CN10 pin 30 | SPI2_SCK | — |
| PB14 | CN10 pin 28 | SPI2_MISO | — |
| PB15 | CN10 pin 26 | SPI2_MOSI | — |
| PB12 | CN10 pin 16 | SPI2_NSS | — |
| PA11 | CN10 pin 14 | CAN_RX, con transceptor | USB_DM |
| PA12 | CN10 pin 12 | CAN_TX, con transceptor | USB_DP |
| PA13 | CN7 pin 13 | SWDIO. No usarlo como GPIO | Cualquier otra función con el ST-LINK puesto |
| PA14 | CN7 pin 15 | SWCLK. No usarlo como GPIO | Cualquier otra función con el ST-LINK puesto |
| PF0 | CN7 pin 29 | Reloj de 8 MHz desde el ST-LINK en C-02 o posterior | GPIO |
| PC14, PC15 | CN7 pines 25 y 27 | Cristal de 32,768 kHz en C-02 o posterior | GPIO |

PA0, PA1, PA2, PA3, PA4, PA5, PA6, PA7, PB0, PC0, PC1, PC2, PC3 y PC4 son TTa en la tabla 13 del datasheet: su tensión de entrada llega como máximo a VDDA + 0,3 V. No son tolerantes a 5 V. PA9 y PA10 son FTf: el datasheet, tabla 19, permite en un pin FT o FTf hasta 5,5 V como máximo absoluto. Eso no convierte la salida en 5 V. La salida sigue siendo 3,3 V.

PC13, PC14 y PC15 se alimentan a través de un interruptor que solo absorbe 3 mA. La nota 2 de la tabla de pines del datasheet dice que no deben usarse como fuente de corriente, por ejemplo para encender un LED, y que en salida no deben superar 2 MHz con 30 pF. En el encapsulado de 64 pines, la nota 4 de esa misma tabla dice que VREF+ no sale a un pin: queda unido por dentro a VDDA. En la placa, AREF es esa red AVDD.

## Matriz de prácticas y materiales

La columna de materiales es lo que hay que tener encima de la mesa cuando se publique el módulo. Los valores eléctricos son requisitos, no una marca. Donde el cálculo del resistor dependa del LED que compres, el módulo lo hará con la hoja de ese LED. Aquí solo se anticipa el rango.

Hasta el módulo 10 todo es baja tensión, alimentado por el USB de la placa o por una pila o fuente de laboratorio de 5 V aislada de la red. Ningún módulo pide conectar la red eléctrica a la tarjeta.

| Módulo | Prácticas previstas | Material nuevo respecto al anterior |
| --- | --- | --- |
| 1 | Tres recorridos guiados: identificar piezas, leer la etiqueta, observar LEDs y medir 5 V y 3,3 V | Placa, cable Mini-USB de datos, polímetro |
| 2 | Tres ejercicios de límites: qué pin admite 5 V, cuánta corriente puede salir de un pin, qué pasa si JP5 está al revés | El mismo polímetro. Fuente de laboratorio solo si se practica VIN, y debe ser SELV |
| 3 | Tres proyectos mínimos: vacío que compila, LED que parpadea, punto de ruptura en el retardo | PC con el entorno de la página de fuentes |
| 4 | Tres ejercicios de C: tipos y tamaños, un bucle, una función que lee una variable global | Ninguno de hardware |
| 5 | LED de la placa, LED externo, pulsador de la placa, pulsador externo con antirrebote | Protoboard, cables, LED rojo de indicador, resistencias, pulsador, 4,7 kΩ, 100 nF |
| 6 | Parar en un bucle, mirar una variable, ver el registro del GPIO, provocar un fallo y leer el analizador | Ninguno nuevo |
| 7 | Eco por el puerto virtual, tramas con un formato fijo, enlace con un ESP32 a 3,3 V por USART1 | ESP32 u otra placa de 3,3 V. Tierra común. Sin desplazador de nivel si ambos lados son 3,3 V |
| 8 | Parpadeo sin bloquear, semáforo, medida del tiempo entre dos flancos | LED externo ya pedido. Tres LED si se monta el semáforo: rojo, ámbar y verde, cada uno con su resistor |
| 9 | Pulsador por interrupción, prioridad frente a USART, antirrebote en la interrupción | El pulsador del módulo 5 |
| 10 | Brillo del LED por PWM, transistor para una carga que el pin no puede alimentar, servo educativo | LED, resistor calculado, transistor NPN de pequeña señal (2N2222 o equivalente), diodo, servo de hobby tipo SG90 alimentado a 5 V desde una fuente externa, no desde un GPIO |
| 11 | Potenciómetro, una tensión dentro de 0 a 3,3 V, temperatura con un sensor analógico de 3,3 V | Potenciómetro lineal de 10 kΩ, sensor analógico cuya salida quepa en 0 a 3,3 V (se fijará el modelo con su hoja al escribir el módulo) |
| 12 | Tensión continua en PA4, rampa, tono o referencia para un comparador | Polímetro. Opcional: osciloscopio |
| 13 | Barrido del bus, sensor I2C de 3,3 V, pantalla OLED I2C de 3,3 V | Módulo I2C alimentado a 3,3 V. Pull-up de 4,7 kΩ a 3,3 V si el módulo no los trae |
| 14 | Leer un registro SPI, un sensor SPI de 3,3 V, una cadena de LEDs con un registro de desplazamiento 74HC595 alimentado a 3,3 V | Dispositivo SPI de 3,3 V. Cables cortos |
| 15 | ADC por encuesta, ADC por DMA, un búfer que se vuelca por el puerto serie | El potenciómetro del módulo 11 |
| 16 | Contar pulsos, RPM con una rueda de prueba, encoder incremental de 3,3 V | Encoder o dos salidas en cuadratura compatibles con 3,3 V. Resistencia de pull-up si la salida es en colector abierto |
| 17 | Semáforo como máquina de estados, alarma con estados, el mismo programa partido en archivos | Ninguno nuevo |
| 18 | Dos tareas, una cola entre la tecla y el LED, un semáforo para el puerto serie | Ninguno nuevo |
| 19 | Media móvil, un filtro IIR pequeño, comparar la señal cruda y la filtrada | El potenciómetro |
| 20 | PID sobre un modelo en el programa, PID sobre un LED y un fotorresistor como planta de juguete, discusión de qué no es un lazo industrial | Fotorresistor y LED, o solo el modelo en código |
| 21 | Trama Modbus de prueba, esclavo que publica un registro, segunda estación (otro USB-RS485 o una segunda placa) | Transceptor RS-485 de alimentación y niveles de 3,3 V, por ejemplo un MAX3485 o equivalente. Par trenzado. Resistencia de terminación 120 Ω. No un MAX485 alimentado a 5 V pegado al pin |
| 22 | Dos nodos CAN a 3,3 V en el lado lógico, un identificador, un filtro | Dos transceptores CAN con E/S de 3,3 V (familia TJA1051T/3 o equivalente) y dos placas, o una placa y un adaptador CAN-USB compatible |
| 23 | Watchdog de ventana, un bucle que se cuelga, recuperación con un código de fallo | Ninguno nuevo |
| 24 | Guardar un umbral en Flash, leerlo al arrancar, proteger la escritura ante un apagón | Ninguno nuevo |
| 25 | Medir corriente en JP6, un modo Sleep, qué periférico impide bajar el consumo | Polímetro en modo corriente, en serie con JP6, como describe UM1724 §7.8 |
| 26 | La misma salida de LED con HAL, con LL y con el registro, y cuándo no compensa bajar de nivel | Ninguno nuevo |
| 27 | Entrada 24 V con optoacoplador, 0–10 V con divisor y protección, 4–20 mA con resistencia y amplificador o con un módulo ya aislado | Módulos o componentes calculados en ese módulo. Alimentación de 24 V solo en el lado aislado, nunca en un header de la Nucleo |
| 28 | Lista de pruebas del prototipo, un informe, qué falta para que deje de ser un montaje de prácticas | Carpeta del proyecto |

El servo del módulo 10 es un **servo de aeromodelismo o de robótica educativa**. Se manda con un pulso de aproximadamente 1 ms a 2 ms repetido cada 20 ms, y la alimentación del motor es de unos 5 V por un cable distinto del pin de señal. No es un servomotor industrial con encoder, driver y red de 230 V o de 24 V. El curso no alimenta el motor del servo desde el pin del microcontrolador ni desde el 3,3 V de la placa.

El relé, cuando aparezca en el módulo 10 y en los proyectos, se activa con transistor o con un módulo que ya traiga transistor y diodo. La bobina no se conecta a un GPIO. La corriente de un pin, en valor absoluto máximo, es 25 mA, y la suma de todos los pines es 80 mA (datasheet, tabla 17). Esos números son máximos absolutos, no la corriente a la que conviene trabajar.

## Material común para comprar una sola vez

- Una NUCLEO-F303RE. Anota la línea `MB1136-F303RE-Cxx` de la etiqueta de abajo.
- Un cable USB tipo A o tipo C, del lado del PC, a Mini-USB tipo B, con hilos de datos.
- Protoboard de 830 puntos y un juego de cables macho-macho y macho-hembra.
- Polímetro que mida tensión continua y corriente continua en miliamperios.
- Resistencias de 220 Ω, 330 Ω, 510 Ω, 1 kΩ, 4,7 kΩ y 10 kΩ, 1/4 W.
- Condensadores cerámicos de 100 nF.
- LED indicadores de 3 mm o 5 mm, rojo, ámbar y verde. Guarda su hoja para calcular el resistor. No reutilices el valor 510 Ω de la placa sin calcular: ese valor es el de R31 en el esquema de la tarjeta, no una ley general.
- Pulsadores para protoboard.
- Transistor NPN de pequeña señal y diodo 1N4007, o un módulo de relé pensado para entrada de 3,3 V.
- Destornillador pequeño, para no apoyarte en los pulsadores cuando pongas un shield. El manual avisa de que la caperuza de B1 o B2 puede dejar el reset pulsado.

## Lo que no está en la primera entrega

Están escritos el entorno, este índice, las fichas de los 28 módulos y los módulos 1 y 2. Del módulo 3 en adelante la ficha ya dice qué se practica y con qué pines; el procedimiento, el código y el dibujo de cada ejemplo se publican con ese módulo.

Cuando se publique un módulo, su carpeta de proyecto vivirá en `proyectos/` y el HTML se regenerará con `tools/build_html.py`.
