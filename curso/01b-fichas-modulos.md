# Fichas de los módulos

Esta página dice, módulo por módulo, qué problema se resuelve, qué se sabe al terminar, cuáles son las tres prácticas y qué pin se usa. No sustituye la lección. La lección escrita, con el procedimiento reproducible, está en el módulo 1 y en el módulo 2. Del 3 al 28 la ficha es el contrato: el código y el dibujo de cableado llegan con la entrega de ese módulo.

Nada de lo planificado se ha compilado ni se ha probado en una placa. Donde un número eléctrico importa, la ficha remite al datasheet o a UM1724.

El mapa de pines común está en el [índice](01-indice-y-matriz.md). Estas fichas no lo cambian.

## Nivel básico

### Módulo 1. Arquitectura de la tarjeta

**Estado.** Escrito en [Módulo 1](02-modulo-01-arquitectura.md).

**Para qué sirve.** Poder señalar el chip, el ST-LINK, el LED, el pulsador y los conectores sin mezclarlos, y alimentar la placa por USB sin poner 5 V en el pin de 3,3 V.

**Al terminar.** Lees la etiqueta `MB1136-F303RE-Cxx`, reconoces LD1, LD2 y LD3, y sabes que D0 y D1 no llevan PA2 y PA3 de fábrica.

**Prácticas.** Identificar las piezas. Copiar la revisión. Medir +5 V en CN6 pin 5 y +3,3 V en CN6 pin 4.

**Pines.** Solo se observan. PA5 es el LED verde, PC13 el pulsador azul, PA13 y PA14 el depurador.

### Módulo 2. Alimentación y límites eléctricos

**Estado.** Escrito en [Módulo 2](03-modulo-02-alimentacion.md).

**Para qué sirve.** Decidir si un cable se puede conectar, antes de que haya un programa. La placa trabaja con 5 V en un raíl y con 3,3 V en el chip. No es lo mismo.

**Al terminar.** Distingues un máximo absoluto de una corriente de trabajo, clasificas un pin como TC, TTa o FT, y calculas la resistencia de un LED con la hoja de ese LED.

**Prácticas.** Clasificar cinco conexiones propuestas y rechazar las que salen del rango. Calcular un resistor de LED con un Vf declarado. Repartir el presupuesto de 300 mA del USB y el de 80 mA de la suma de pines.

**Pines.** No se añade ninguno. Se usan las medidas de CN6 pin 4 y pin 5 hechas en el módulo 1.

**Límite.** Un pin TTa, como PA0, no admite 5 V. Un pin FT admite hasta 5,5 V en la entrada y sigue saliendo a 3,3 V. PC13 no alimenta un LED.

### Módulo 3. Instalación y primer proyecto

**Estado.** Planificado. El procedimiento de instalación ya está en [Fuentes y entorno](00-fuentes-y-entorno.md). Este módulo lo recorre con la placa delante y deja el primer programa mínimo.

**Para qué sirve.** Pasar de «la placa enciende» a «yo he generado, compilado y grabado un proyecto».

**Al terminar.** Tienes un proyecto CMake abierto en VS Code, generado desde CubeMX para la placa NUCLEO-F303RE, y sabes parar la ejecución en `main`.

**Prácticas.**

1. Proyecto vacío que solo compila y llega a `main`. Sirve para separar un fallo de herramientas de un fallo de tu código.
2. El LED verde cambia de estado cada medio segundo con `HAL_Delay`. Es el primer lazo visible.
3. Un punto de ruptura dentro de ese retardo, y la variable que cuenta los pasos se lee en la vista *Variables* con el programa parado.

**Pines.** PA5 como GPIO de salida, que es lo que CubeMX propone al elegir la placa. No se cablea nada fuera.

**Qué no se afirma.** Hasta que se redacte el módulo, este repositorio no incluye ese proyecto ni dice que haya compilado.

### Módulo 4. Fundamentos de C aplicados a STM32

**Estado.** Planificado. No supone que ya sepas C.

**Para qué sirve.** Leer el `main.c` que genera CubeMX sin tratarlo como un conjuro. Un `uint8_t`, un `while` y una función son las herramientas de los módulos siguientes.

**Al terminar.** Sabes el tamaño de los enteros que usa el HAL, qué es una variable global frente a una local, y por qué un bucle `while (1)` es el programa que se queda corriendo.

**Prácticas.** Las tres son sobre el proyecto del módulo 3, sin hardware nuevo.

1. Declarar un contador, incrementarlo y verlo en el depurador. Se explica el tipo antes de usarlo.
2. Sacar el parpadeo a una función con un argumento en milisegundos.
3. Un `if` que mira una variable y cambia el periodo. Todavía no se lee el pulsador: el valor se cambia desde el depurador para ver la decisión.

**Pines.** Otra vez solo PA5.

### Módulo 5. GPIO

**Estado.** Planificado. Es el primer módulo con piezas fuera de la placa.

**Para qué sirve.** Encender una lámpara de señal y leer un mando. En un cuadro industrial eso es un piloto y un pulsador de marcha, aquí a 3,3 V.

**Al terminar.** Configuras un pin como salida push-pull, como entrada con pull-up o pull-down, y explicas el antirrebote. El datasheet da el pull interno entre 25 kΩ y 55 kΩ, típico 40 kΩ (tabla 66). Para un pulsador externo este curso usa además 4,7 kΩ externos, del mismo orden que R30 de la placa, porque el valor interno varía y no es un contacto de mando.

**Prácticas.**

1. LED verde de la placa, PA5, y un LED externo en PC7 (D9, CN5 pin 2) con la resistencia calculada en el módulo 2. PC7 se elige para no compartir PA5 con el LED de la tarjeta.
2. El pulsador azul B1, en PC13, enciende el LED mientras se mantiene. Se lee a nivel bajo. PC13 no se usa como salida.
3. Un pulsador externo a 3,3 V, con 4,7 kΩ a VDD, 100 nF a GND y lectura con antirrebote por tiempo. El pin de esa entrada será PA8 (D7, CN9 pin 8), que está libre en el mapa.

**Límite.** La corriente del LED externo sale del cálculo, no de «220 Ω porque sí». La suma de todos los pines no pasa de 80 mA, y cada pin se queda en la zona de 8 mA que el datasheet asocia a un nivel de salida firme.

### Módulo 6. Depuración y diagnóstico

**Estado.** Planificado.

**Para qué sirve.** Cuando el LED no hace lo que crees, distinguir un pin mal elegido, un programa que no llegó a grabarse y una variable que no vale lo que imaginas.

**Al terminar.** Pones un punto de ruptura, miras una variable con el programa parado, abres la vista de periféricos del GPIO y usas el analizador de fallos si el núcleo se cae.

**Prácticas.**

1. Parar dentro del bucle del módulo 5 y comprobar que el registro de salida de PA5 coincide con el LED.
2. Cambiar una variable desde el depurador y ver que el periodo del parpadeo cambia. Se explica que esto no es lo mismo que una *live watch* con el programa corriendo: la documentación de la extensión 3.x documenta la vista con la ejecución parada.
3. Provocar un acceso inválido a propósito, en un proyecto de ensayo, y leer la falta. El ejercicio dice qué línea lo causa y cómo se quita. No se deja ese fallo en los proyectos siguientes.

**Pines.** Los del módulo 5.

### Módulo 7. UART y terminal serie

**Estado.** Planificado.

**Para qué sirve.** Ver números en el PC sin un depurador, que es como un panel de operador mínimo. También hablar con otra placa de 3,3 V.

**Al terminar.** Envías y recibes texto por el puerto COM virtual, y por un segundo UART hacia un ESP32, con tierra común y niveles de 3,3 V en los dos lados.

**Prácticas.**

1. El programa arranca y escribe una línea por USART2 (PA2/PA3 hacia el ST-LINK). La velocidad se fija en CubeMX y se repite en el monitor. Se explica el formato 8N1 antes de usarlo.
2. El PC envía un carácter y la placa lo devuelve, y otro carácter cambia el estado del LED. Sigue siendo el puerto virtual. No se sueldan SB62 ni SB63.
3. USART1 en PA9 (D8, transmisión) y PA10 (D2, recepción) hacia un ESP32 a 3,3 V. El ESP32 no se alimenta desde un pin del STM32. Si el módulo UART del otro lado fuera de 5 V, haría falta un desplazador: la entrada FT admite 5 V, pero la salida del STM32 sigue siendo 3,3 V y muchos receptores de 5 V no la dan por válida.

**Pines.** PA2/PA3 reservados al ST-LINK. PA9/PA10 para el enlace externo.

## Nivel intermedio

### Módulo 8. Temporizadores y programas que no se bloquean

**Estado.** Planificado.

**Para qué sirve.** Un semáforo no puede quedarse dormido dentro de `HAL_Delay` si además tiene que leer un pulsador. El tiempo pasa en un temporizador y el programa solo mira si ya toca cambiar.

**Al terminar.** Distingues un retardo que bloquea el procesador de una cuenta con un temporizador. TIM2 es el temporizador de 32 bits; TIM3 tiene canales en D9 y D5.

**Prácticas.**

1. El mismo parpadeo del LED, ahora con un temporizador y sin `HAL_Delay` en el lazo principal.
2. Semáforo de tres luces en pines libres: rojo en PA8 (D7), ámbar en PB5 (D4), verde en PC7 (D9). Cada LED con su resistencia. Los tiempos se explican como los de un cruce pequeño, no como una norma de tráfico.
3. Medir el tiempo entre dos pulsaciones de B1 con un temporizador de entrada, y mostrar el resultado por el puerto serie.

**Pines.** PA8, PB5, PC7 como salidas. PC13 como entrada. USART2 para el texto.

### Módulo 9. Interrupciones y prioridades

**Estado.** Planificado. La palabra «interrupción» se define aquí, con la analogía del teléfono que suena mientras estás midiendo, antes de hablar de prioridades del NVIC.

**Para qué sirve.** Atender un flanco en el momento en que ocurre, sin preguntar todo el tiempo si el pulsador está pulsado.

**Al terminar.** Habilitas una interrupción externa, le das una prioridad y explicas por qué la rutina tiene que ser corta.

**Prácticas.**

1. B1 por interrupción cambia el LED. El antirrebote se hace al salir, no dentro de un retardo largo en la interrupción.
2. La misma tecla y, a la vez, la recepción del UART. Se da más prioridad a una de las dos y se observa cuál espera.
3. Dos flancos seguidos más rápidos que el antirrebote, y el programa no cuenta de más. Es el criterio de que el antirrebote está bien puesto.

**Pines.** PC13 y PA8. USART2.

**Errata.** Antes de escribir el código se revisa ES0261 por si la sección de sistema afecta al modo de despertar. Se citará la sección concreta en la lección, no aquí de memoria.

### Módulo 10. PWM y cargas con etapa externa

**Estado.** Planificado.

**Para qué sirve.** Variar la luz de un LED y mandar un relé o un motor pequeño sin pedir la corriente al pin. Un servo de aeromodelismo se manda con un pulso; no es un servo industrial.

**Al terminar.** Configuras un canal PWM, calculas la corriente de base de un transistor para un relé de baja tensión y separas la alimentación del motor de la del microcontrolador.

**Prácticas.**

1. Brillo del LED externo en PC7 con TIM3 canal 2. La frecuencia se elige por encima del parpadeo visible y se justifica en la lección.
2. Un transistor NPN, con resistencia de base calculada y diodo en antiparalelo con la bobina, activa un relé o un zumbador de 5 V. La bobina no toca el GPIO. El 5 V de la bobina sale de CN6 pin 5 solo si la corriente cabe en el presupuesto del USB; si no, fuente aparte y GND común.
3. Un servo educativo tipo SG90: señal en PB10 (D6, TIM2 canal 3), alimentación de 5 V del servo desde una fuente externa, nunca desde un pin ni desde el regulador de 3,3 V. El pulso de mando se describe con los tiempos de la hoja de ese servo.

**Pines.** PC7, un GPIO libre para la base del transistor (PB5 si el semáforo del módulo 8 no está montado a la vez; la lección lo dirá), PB10 para el servo.

### Módulo 11. ADC

**Estado.** Planificado.

**Para qué sirve.** Leer una posición, un nivel o una temperatura que llegan como tensión, dentro de 0 a 3,3 V.

**Al terminar.** Explicas la resolución de 12 bits, eliges un tiempo de muestreo y pasas el número del conversor a voltios con la referencia real. En este encapsulado VREF+ está unido por dentro a VDDA (nota 4 de la tabla de pines). En la placa, VDDA llega de VDD por SB57.

**Prácticas.**

1. Potenciómetro de 10 kΩ entre 3,3 V y GND, cursor a PA0 (A0, CN8 pin 1). PA0 es TTa: solo 0 a 3,3 V.
2. Una tensión continua de laboratorio, limitada con un divisor calculado para no pasar de 3,3 V, leída en PA1 (A1).
3. Un sensor de temperatura analógico cuya hoja quepa en 0 a 3,3 V, en PB0 (A3). El modelo se fija al escribir la lección, con su hoja al lado. No se adelanta un factor de conversión inventado.

**Pines.** PA0, PA1, PB0. PA4 se reserva al DAC del módulo 12.

**Errata.** ES0261 tiene varias limitaciones del ADC. La lección dirá cuáles afectan a estas tres prácticas antes de dar el código por bueno.

### Módulo 12. DAC

**Estado.** Planificado. El chip tiene dos canales. Los dos salen a un conector, pero uno está ocupado.

**Para qué sirve.** Generar una tensión de referencia o una rampa lenta sin un potenciómetro.

**Al terminar.** Sacas una tensión por PA4 y la compruebas con el polímetro. Sabes que PA5 también es DAC1_OUT2 y que no se usa porque es el LED verde.

**Prácticas.**

1. Tensión fija en PA4 (A2, CN8 pin 3), medida con el polímetro entre PA4 y GND.
2. Una rampa que recorre el fondo de escala en un tiempo conocido, y el puerto serie dice el código que se escribió.
3. Esa tensión como referencia de un comparador del propio chip, si el pin del comparador sigue libre en el mapa. Si no queda libre sin deshacer otro módulo, la tercera práctica se queda en la rampa y se dice por qué.

**Condición.** Con el DAC en uso, VDDA tiene que estar entre 2,4 V y 3,6 V (datasheet, tabla 19). En la placa lo está, porque sale de los 3,3 V.

### Módulo 13. I2C

**Estado.** Planificado.

**Para qué sirve.** Leer un sensor o escribir en una pantalla con dos hilos compartidos por varias piezas.

**Al terminar.** Explicas dirección, ACK y pull-up. Usas PB8 (SCL) y PB9 (SDA), que son D15 y D14, no A4 y A5.

**Prácticas.**

1. Barrer las direcciones de 7 bits y mostrar cuáles responden. Sirve para comprobar el cableado antes de culpar al programa.
2. Leer un sensor I2C de 3,3 V. El modelo, con su dirección y su hoja, se fija en la lección.
3. Escribir texto en una pantalla OLED I2C de 3,3 V. Si el módulo no trae resistencias de pull-up, se ponen 4,7 kΩ a 3,3 V en SCL y en SDA.

**Pines.** PB8 y PB9. No se usan a la vez como CAN.

**Alimentación.** La pantalla y el sensor van a 3,3 V de la placa, no a 5 V. Un módulo diseñado solo para 5 V no se conecta directo.

### Módulo 14. SPI

**Estado.** Planificado.

**Para qué sirve.** Hablar con un dispositivo que tiene reloj, dato de ida y dato de vuelta, más rápido que I2C y con un hilo de selección por dispositivo.

**Al terminar.** Nombras SCK, MISO, MOSI y NSS, y eliges el flanco que pide la hoja del dispositivo.

**Prácticas.**

1. Un registro de desplazamiento 74HC595 alimentado a 3,3 V enciende una fila de LED con sus resistencias. Es el dispositivo más fácil de ver.
2. Leer el identificador o un registro de un sensor SPI de 3,3 V. El modelo se fija con su hoja.
3. Dos dispositivos en el mismo bus, cada uno con su NSS, y el programa demuestra que no se pisan.

**Pines.** SPI2, para no usar PA5: PB13 SCK (CN10 pin 30), PB14 MISO (CN10 pin 28), PB15 MOSI (CN10 pin 26), PB12 NSS (CN10 pin 16). Es la función alternativa AF5 de la tabla 14 del datasheet. Un segundo NSS puede ir por PB6 (D10) si hace falta.

**Errata.** ES0261 describe casos del CRC del SPI y del bit BSY. La lección los mira antes de activar CRC o el modo esclavo. Estas prácticas son maestro, sin CRC.

### Módulo 15. DMA

**Estado.** Planificado.

**Para qué sirve.** Llenar una tabla de medidas sin que el núcleo copie cada muestra a mano. Es la diferencia entre mirar un instrumento a cada instante y dejar que un registrador llene la hoja.

**Al terminar.** Lanzas una conversión continua del ADC hacia memoria y vuelcas el bloque por el puerto serie.

**Prácticas.**

1. La misma lectura del potenciómetro en PA0, muestra a muestra, como referencia lenta.
2. La misma señal, con DMA, a un ritmo elegido y justificado.
3. Un búfer que se llena mientras el lazo principal sigue parpadeando el LED. El criterio es que el LED no se detiene cuando llegan las muestras.

**Pines.** PA0 y PA5. USART2 para volcar.

**Errata.** ES0261 avisa de un overrun de DMA en modo dual intercalado con un solo canal, y de que la bandera de overrun puede no activarse si no se lee el dato. La práctica 2 usa un solo ADC y lee el bloque de forma que ese caso quede explicado.

### Módulo 16. Encoder, pulsos y velocidad

**Estado.** Planificado.

**Para qué sirve.** Contar piezas en una cinta o vueltas de un eje pequeño, y pasar de pulsos a RPM con la cantidad de pulsos por vuelta.

**Al terminar.** Configuras un temporizador en modo encoder o en captura, y el cálculo de RPM está escrito con unidades.

**Prácticas.**

1. Contar pulsos de un pulsador o de un generador de 3,3 V, y mostrar la cuenta.
2. RPM de una rueda de prueba de la que se conoce el número de marcas. La fórmula se desarrolla en la lección.
3. Un encoder incremental de 3,3 V, con sus dos canales en cuadratura. Si la salida es en colector abierto, pull-up a 3,3 V. No se conecta un encoder industrial de 24 V.

**Pines.** Se elegirán en TIM2 o TIM3 entre los que el mapa deja libres al llegar aquí: la lección publicará la tabla y no reutilizará PB8/PB9 ni PA2/PA3. Hasta entonces no se inventa el número de pin en un dibujo.

## Nivel avanzado

### Módulo 17. Máquinas de estados

**Estado.** Planificado.

**Para qué sirve.** Que un semáforo o una alarma no sean una cadena de retardos imposible de ampliar. Cada situación tiene un nombre y unas transiciones.

**Al terminar.** Partes el programa en archivos, uno por bloque, y el `main` solo llama al paso de la máquina.

**Prácticas.**

1. El semáforo del módulo 8 reescrito como estados: rojo, rojo-ámbar, verde, ámbar.
2. Una alarma con reposo, prealarma y alarma, usando el pulsador y un umbral que todavía puede ser una constante.
3. El mismo programa repartido en `semaforo.c`, `alarma.c` y `main.c`, dentro de las zonas que CubeMX no borra.

**Pines.** Los ya usados. No se añaden.

### Módulo 18. FreeRTOS

**Estado.** Planificado. El núcleo del curso no usa un sistema operativo hasta aquí. Se define qué es una tarea antes de crear la primera.

**Para qué sirve.** Tener a la vez la lectura, el puerto serie y el parpadeo sin convertir el lazo principal en un embudo.

**Al terminar.** Creas dos tareas, una cola y un semáforo. Sabes qué pasa si dos tareas escriben el UART sin turnarse.

**Prácticas.**

1. Una tarea parpadea y otra espera el pulsador.
2. El pulsador deja un aviso en una cola y otra tarea cambia el LED.
3. El puerto serie se protege para que los textos de dos tareas no se mezclen.

**Herramienta.** El paquete STM32CubeF3 que CubeMX descargue para esta placa, con el middleware FreeRTOS que esa versión ofrezca. La lección anotará el nombre y la versión exactos del componente generado. La extensión 3.x documenta vistas de depuración para FreeRTOS.

### Módulo 19. Filtrado digital

**Estado.** Planificado.

**Para qué sirve.** Que un umbral no dispare una alarma por un pico de ruido de una sola muestra.

**Al terminar.** Implementas una media móvil y un filtro de primer orden, y comparas la señal cruda con la filtrada en el puerto serie.

**Prácticas.**

1. Media de N muestras del potenciómetro. N se elige y se justifica.
2. Un filtro recursivo sencillo, con el coeficiente explicado como «cuánta memoria guarda de la muestra anterior».
3. Las dos salidas a la vez, cruda y filtrada, para ver el retraso. El retraso se cuenta en muestras, no se esconde.

**Pines.** PA0 y USART2.

### Módulo 20. PID

**Estado.** Planificado.

**Para qué sirve.** Acercar una medida a una consigna. Primero en un modelo que vive en el programa, para ver el efecto de cada término sin quemar un motor. Después en una planta de juguete de baja tensión.

**Al terminar.** Escribes un PID discreto con periodo fijo, limitas la salida y explicas qué no puedes concluir de un LED y una fotorresistencia.

**Prácticas.**

1. El proceso es una fórmula en el programa. La consigna y la salida se imprimen.
2. Un LED y una fotorresistencia, a 3,3 V, como planta lenta. No es un horno ni un motor.
3. El mismo regulador con la salida limitada, y un cambio de consigna que no satura para siempre.

**Pines.** PWM en PC7 para el LED. La fotorresistencia, con su divisor calculado, en PA1. Esos componentes se eligen con su hoja al escribir la lección.

### Módulo 21. Modbus RTU

**Estado.** Planificado.

**Para qué sirve.** Publicar una medida a un maestro, que es el papel de muchos instrumentos de campo. La placa no trae RS-485.

**Al terminar.** Montas un transceptor de 3,3 V, una terminación de 120 Ω y un esclavo que responde a una lectura de registros.

**Prácticas.**

1. Una trama de prueba escrita a mano, comprobada byte a byte, todavía por el UART antes del transceptor.
2. Esclavo con un registro de retención que el maestro lee. El maestro es un adaptador USB-RS485 o una segunda placa con el mismo transceptor.
3. Dos registros: una medida y una consigna que el maestro puede escribir, con un límite de rango rechazado si se sale.

**Material.** Transceptor RS-485 con alimentación y niveles de 3,3 V, por ejemplo un MAX3485 o equivalente. No un MAX485 a 5 V pegado al pin. Par trenzado y resistencia de 120 Ω en los dos extremos del bus de prueba.

**Pines.** USART1 en PA9 y PA10, más un GPIO libre para el sentido de transmisión del transceptor. La lección fijará ese GPIO entre los que sigan libres y lo dibujará. USART2 se queda para el mensaje de diagnóstico hacia el PC.

### Módulo 22. CAN

**Estado.** Planificado. El STM32F303RET6 tiene un controlador CAN. La placa no tiene transceptor ni conector CAN.

**Para qué sirve.** Intercambiar un identificador y unos datos con otra estación, como en un vehículo o una máquina, sin que cada nodo espere su turno por un maestro único.

**Al terminar.** Envías y recibes un identificador entre dos nodos, con transceptores de E/S a 3,3 V.

**Prácticas.**

1. Un nodo transmite un identificador fijo y el otro lo recibe. Los dos transceptores comparten CANH, CANL y la referencia que indique su hoja.
2. Un filtro que acepta un identificador y descarta otro.
3. Una segunda estación distinta, un adaptador CAN-USB o una segunda Nucleo, repite el intercambio.

**Pines.** PA11 (CN10 pin 14) recepción y PA12 (CN10 pin 12) transmisión, funciones alternativas del datasheet. No se usan PB8 y PB9, que son el I2C. Estos pines también son el USB del chip: este curso no los usa como USB.

**Material.** Dos transceptores con lado lógico de 3,3 V, de la familia TJA1051T/3 o equivalente, y el cable que pida su hoja. La terminación del bus se copia de esa hoja, no de una cifra genérica si la hoja dice otra cosa.

### Módulo 23. Watchdog y fallos

**Estado.** Planificado.

**Para qué sirve.** Que un programa bloqueado vuelva a arrancar solo, y que al volver se sepa que hubo un fallo y no un encendido normal.

**Al terminar.** Activas el watchdog de ventana o el independiente, provocas un cuelgue controlado y lees la causa del reset.

**Prácticas.**

1. El programa alimenta el watchdog a tiempo y no se reinicia.
2. Un bucle sin alimentar el watchdog reinicia la placa, y LD2 lo indica con un patrón distinto del arranque normal.
3. El código de la causa del reset se guarda y se imprime por el puerto serie en el arranque siguiente.

**Pines.** PA5 y USART2.

### Módulo 24. Memoria no volátil

**Estado.** Planificado.

**Para qué sirve.** Que un umbral de alarma siga ahí después de quitar el USB. En este chip eso se hace en la Flash, no hay una EEPROM aparte que el datasheet describa como tal.

**Al terminar.** Escribes una página con el procedimiento del HAL o del manual de referencia RM0316, lees el valor al arrancar y no escribes en cada vuelta del bucle.

**Prácticas.**

1. Guardar un número, quitar alimentación y comprobar que vuelve.
2. Una consigna que se cambia por el puerto serie y se guarda solo cuando se pide, no en cada tecla.
3. Un corte de alimentación simulado a mitad de la escritura, y el programa arranca con el último valor íntegro o con el valor de fábrica. El criterio se escribe antes de la prueba.

**Pines.** Ninguno nuevo. USART2 para el mando.

### Módulo 25. Bajo consumo

**Estado.** Planificado.

**Para qué sirve.** Medir cuánto gasta el chip y bajar ese gasto cuando no hay nada que hacer. Sigue siendo un prototipo de mesa, no un diseño de pila certificado.

**Al terminar.** Mides la corriente por JP6, entras en un modo de bajo consumo y vuelves con el pulsador o con el reloj.

**Prácticas.**

1. Corriente en Run, con el polímetro en serie en JP6, tal como indica UM1724 §7.8. Sin amperímetro, JP6 abierto apaga el chip.
2. Un modo Sleep o Stop, el que la lección elija después de leer el capítulo de potencia de RM0316, y la corriente anotada por el estudiante.
3. Despertar con B1. Se explica qué relojes y qué pines impiden que el consumo baje, entre ellos el MCO de 8 MHz que la placa C-02 en adelante deja conectado a PF0.

**Medidas.** Las que anote cada estudiante. Este texto no trae una corriente de ejemplo.

### Módulo 26. HAL, LL y registros

**Estado.** Planificado.

**Para qué sirve.** Elegir el nivel de acceso con un motivo, no por costumbre. HAL es la capa que ha usado el curso. LL y el registro se ven cuando hace falta ver el bit.

**Al terminar.** Enciendes el mismo LED de tres maneras y dices el coste de cada una: líneas de código, lo que esconde y lo que se rompe si CubeMX regenera.

**Prácticas.**

1. PA5 con HAL, como hasta ahora.
2. El mismo pin con las funciones LL, en un proyecto generado con esa opción.
3. El mismo pin escribiendo el registro de salida, con el nombre del registro sacado de RM0316. La lección cita el registro y el bit. No se copia un fragmento suelto como si fuera el proyecto.

**Pines.** PA5.

### Módulo 27. Interfaces industriales

**Estado.** Planificado. Aquí se separa el prototipo de mesa de un equipo de cuadro.

**Para qué sirve.** Entrar 24 V, 0–10 V o 4–20 mA sin tocar el pin con esa señal. La placa no tiene esas interfaces.

**Al terminar.** Dibujas la cadena: señal de campo, protección, aislamiento si hace falta, y solo entonces un pin de 3,3 V. Sabes cuándo el optoacoplador es necesario y cuándo un divisor bien calculado no basta porque las tierras no se pueden unir.

**Prácticas.** Las tres se hacen con baja tensión en el lado de la Nucleo. El lado de 24 V, si se monta, queda del otro lado del aislamiento y con una fuente SELV, nunca con la red de 230 V.

1. Una entrada de 24 V de continua convertida con optoacoplador a un GPIO de 3,3 V. El cálculo del LED del opto se hace con su hoja.
2. Una señal de 0–10 V reducida con divisor, limitación y filtrado, de forma que el pin analógico no pase de 3,3 V ni en el caso de 10 V ni si alguien aplica un poco más. El divisor se calcula en la lección. No se conecta el 10 V directo a PA0.
3. Un lazo de 4–20 mA convertido a tensión con una resistencia de precisión y una etapa que quepa en el ADC, o con un módulo ya hecho cuya hoja se cita. Se explica la diferencia entre un lazo alimentado por el instrumento y uno que no lo está.

**Qué no es.** Un equipo para instalar en una máquina. No hay marcado, no hay ensayo de aislamiento y no hay bornero de potencia.

### Módulo 28. Pruebas y prototipo

**Estado.** Planificado.

**Para qué sirve.** Dejar el montaje en un estado en el que otra persona pueda repetirlo y sepa qué no está demostrado.

**Al terminar.** Tienes una lista de pruebas, el resultado esperado de cada una, el resultado que tú mediste y una lista de limitaciones.

**Prácticas.**

1. Escribir la lista de pruebas del proyecto que elijas entre P1 y P4, antes de ejecutarlas.
2. Ejecutarlas y separar «esperado por el diseño» de «medido en mi mesa».
3. Redactar qué faltaría para salir del laboratorio: alimentación, conectores, aislamiento, watchdog ya probado y versión del firmware.

## Proyectos integradores

Estos cuatro montajes no añaden pines fuera del mapa. Cada uno se escribe cuando estén publicados los módulos de los que depende.

### P1. Estación de temperatura

Lectura de un sensor de 3,3 V, valor en la pantalla I2C y alarma por umbral en un LED o en el transistor del módulo 10. Depende de los módulos 5, 11, 13 y 17. El umbral se puede guardar cuando exista el módulo 24. No es un registro de temperatura de un proceso industrial: el sensor y la exactitud son los de la hoja del componente que se elija.

### P2. Control de tanque

El nivel es una tensión de 0 a 3,3 V, no un depósito real con agua junto a la placa. La bomba es un LED o un relé de baja tensión que representa el contactor. Hay estados de marcha, paro y fallo, y el watchdog del módulo 23 si ya está dado. Depende de 11, 17, 20 y 23. No se bombea líquido en esta práctica.

### P3. Monitor de motor

Cuenta de pulsos o encoder a RPM, una entrada analógica de 0 a 3,3 V que representa una corriente mediante un sensor de laboratorio, y alarmas por el puerto serie. Depende de 7, 11 y 16. El motor, si se usa el del módulo 10, es pequeño y con driver externo. No se supervisa un motor de red.

### P4. Nodo de adquisición

Varias medidas por ADC, con DMA cuando el módulo 15 esté escrito, parámetros guardados en Flash y publicación por Modbus RTU. Depende de 15, 21 y 24. La segunda estación es el maestro Modbus. El nodo no incluye Ethernet ni Wi-Fi.

## Dónde está cada lección completa

| Módulo | Archivo |
| --- | --- |
| 1 | [02-modulo-01-arquitectura.md](02-modulo-01-arquitectura.md) |
| 2 | [03-modulo-02-alimentacion.md](03-modulo-02-alimentacion.md) |
| 3 a 28 y P1 a P4 | Ficha en esta página. La lección completa se añade al publicar ese módulo |
