# Fuentes oficiales y entorno de trabajo

Esta página fija las fuentes con las que se escribió la primera entrega y el procedimiento de instalación vigente para programar la NUCLEO-F303RE desde Visual Studio Code. El procedimiento se contrastó con la documentación publicada por STMicroelectronics. **No se instaló el entorno en este equipo ni se grabó una placa**: los pasos describen lo que dice el manual, no un resultado medido aquí.

## Cómo leer las marcas de este curso

Cada afirmación técnica lleva una de estas marcas.

- **Verificado.** Sale de un manual, un datasheet, una errata o un esquema, con sección o tabla.
- **Convención de este curso.** Es una decisión pedagógica para no pisar el mismo pin en módulos distintos. No es una obligación del fabricante.
- **Esperado.** Es lo que el diseño debe hacer. No es una medida tomada con polímetro sobre una placa concreta.
- **No comprobado en hardware.** Este texto no afirma que el programa se compiló, se simuló o se ejecutó en una tarjeta.

## Las cinco piezas que no hay que mezclar

Antes de instalar nada conviene separar cinco nombres que en la caja parecen uno solo.

| Pieza | Qué es | Qué no es |
| --- | --- | --- |
| STM32F303RET6 | El microcontrolador, en cápsula LQFP64, referencia U5 en el esquema | La tarjeta entera |
| NUCLEO-F303RE | La tarjeta de evaluación, PCB MB1136 | El chip, ni el programa |
| ST-LINK/V2-1 | El depurador integrado, con su propio microcontrolador STM32F103CBT6 | La aplicación que vas a escribir |
| Conectores Arduino Uno Rev. 3 | CN5, CN6, CN8 y CN9 | Todos los pines del chip |
| Conectores ST Morpho | CN7 y CN10, 38 pines cada uno | Pines nuevos: son las mismas pistas, con más señales |

**Verificado.** UM1724 Rev 17, tabla 1: el código de pedido NUCLEO-F303RE usa la placa MB1136 y el microcontrolador STM32F303RET6. La sección 7.11 nombra el ST-LINK como STM32F103CBT6. La sección 1 describe los conectores Arduino Uno V3 y los conectores ST morpho.

## Documentación que se consultó

Las fechas son las que aparecen en la portada o en la página del documento consultado en octubre de 2026. ST puede publicar una revisión posterior. Si un número de esta entrega no coincide con el PDF que tienes abierto, manda el PDF.

| Documento | Revisión consultada | Para qué se usa | Enlace |
| --- | --- | --- | --- |
| Página de producto NUCLEO-F303RE | Consulta de octubre de 2026 | Código de pedido, paquete de esquemas y archivos de fabricación | [st.com/en/evaluation-tools/nucleo-f303re](https://www.st.com/en/evaluation-tools/nucleo-f303re.html) |
| UM1724, *STM32 Nucleo-64 boards (MB1136)* | Rev 17, septiembre de 2025 | Alimentación, jumpers, puentes, conectores, revisiones de placa | [PDF UM1724](https://www.st.com/resource/en/user_manual/um1724-stm32-nucleo64-boards-mb1136-stmicroelectronics.pdf) |
| Esquema MB1136-DEFAULT-C05 | 17 de agosto de 2022 | Valores de R30, R31, C15, reguladores y referencia de CN1 | [PDF del esquema C05](https://www.st.com/resource/en/schematic_pack/mb1136-default-c05_schematic.pdf) |
| Datasheet STM32F303xD / STM32F303xE | DocID026415 Rev 5, octubre de 2016 | Memoria, periféricos del F303RE, límites eléctricos, tipo de cada pin | [PDF del datasheet](https://www.st.com/resource/en/datasheet/stm32f303re.pdf) |
| RM0316, manual de referencia | El citado por el datasheet | Registros y periféricos. Se abrirá en el módulo que los use | Enlace desde la página del producto, documento RM0316 |
| ES0261, errata del silicio Rev Y | Rev 5, diciembre de 2018 | Limitaciones del STM32F303RET6 revisión Y | [PDF ES0261](https://www.st.com/resource/en/errata_sheet/es0261-stm32f303xd-stm32f303xe-device-errata-stmicroelectronics.pdf) |
| UM3512, instalación de STM32CubeIDE for VS Code | Rev 2, marzo de 2026 | Requisitos e instalación de la extensión | [PDF UM3512](https://www.st.com/resource/en/user_manual/um3512-stm32cube-for-visual-studio-code-installation-guide-stmicroelectronics.pdf) |
| Documentación en línea de STM32CubeIDE for Visual Studio Code | Canal *latest*, consultado en octubre de 2026 | Instalación, primer proyecto, CMake, depuración, preguntas frecuentes | [dev.st.com, STM32CubeIDE for VS Code](https://dev.st.com/stm32cube-docs/stm32cubeide-vscode/latest/en/index.html) |
| UM1718, STM32CubeMX | La guía de usuario vigente en st.com; la interfaz descrita en la documentación en línea corresponde a la rama 6.18 | Crear el proyecto y generar código con cadena CMake | [Página de STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html) |

El datasheet, en su introducción, remite al manual de referencia RM0316 y al manual de programación PM0214 para el núcleo Cortex-M4. Esos dos documentos se citan cuando un módulo entra en registros o en el juego de instrucciones. No hace falta leerlos para el módulo 1.

### Qué se comprobó en el silicio y en la placa

**Verificado en el datasheet, tabla 2, columna STM32F303Rx con 512 KB**, que es el STM32F303RET6:

- Núcleo Arm Cortex-M4 con FPU, 72 MHz.
- 512 KB de Flash.
- 64 KB de SRAM en el bus de datos y 16 KB de CCM. El título del datasheet resume el conjunto como 80 KB de SRAM.
- 4 ADC de 12 bits y 22 canales en este encapsulado. El texto de descripción habla de 5 Msps.
- 2 canales de DAC de 12 bits.
- 7 comparadores y 4 amplificadores operacionales, según la descripción de la familia.
- Temporizadores: 2 avanzados de 16 bits (TIM1 y TIM8), 5 de propósito general de 16 bits, 1 de propósito general de 32 bits y 2 básicos de 16 bits.
- 3 I2C, 3 USART, 2 UART, 1 CAN 2.0B y 1 USB full-speed.
- Hasta 4 SPI en la familia. Cuáles salen al conector se fija en el mapa de pines del índice, con la tabla de funciones alternativas.
- 12 canales DMA.
- 26 entradas/salidas normales (TC y TTa) y 25 tolerantes a 5 V (FT y FTf). En total, 51 en LQFP64.
- Tensión de trabajo de VDD: 2,0 V a 3,6 V. En esta tarjeta el regulador la deja en 3,3 V.

**Verificado en UM1724 sobre la tarjeta**, y desarrollado en el módulo 1:

- ST-LINK/V2-1 integrado, con puerto COM virtual, almacenamiento masivo y depuración SWD.
- LED de usuario LD2 en PA5 (D13) para esta referencia. El manual avisa de que otras Nucleo-64 usan PB13.
- Pulsador de usuario B1 en PC13. Pulsador de reset B2 en NRST.
- USART2 en PA2 y PA3 hacia el ST-LINK, con SB13 y SB14 cerrados y SB62 y SB63 abiertos.
- Desde la revisión de placa C-02, el reloj de 8 MHz llega desde el ST-LINK al pin PF0, y hay un cristal de 32,768 kHz.

La errata ES0261 aplica al silicio revisión Y. UM1724, tabla 34, identifica la NUCLEO-F303RE con STM32F303RET6 revisión Y y con esa errata. Cada módulo práctico mirará la sección de la errata del periférico que vaya a usar. No se copia aquí la lista completa para no tratar una limitación de silicio como si fuera un fallo de la práctica.

## Entorno principal

El curso usa esta cadena, en este orden:

1. Visual Studio Code.
2. La extensión oficial **STM32CubeIDE for Visual Studio Code**, paquete de extensiones de ST, generación 3.x. En el Marketplace el identificador del paquete es `stmicroelectronics.stm32-vscode-extension`.
3. STM32CubeMX, aplicación de escritorio, para elegir la placa, configurar pines y generar el proyecto.
4. CMake, descargado por el gestor de *bundles* de la extensión. No se instala aparte el antiguo STM32CubeCLT.
5. La cadena GNU Arm Embedded que trae ese gestor.
6. El ST-LINK/V2-1 ya soldado en la tarjeta, para grabar y depurar.

**Verificado.** La nota de versión de la extensión 3.x dice que la arquitectura nueva sustituye el paquete único STM32CubeCLT por un gestor de bundles y por CMSIS-PACK de la familia. También dice que la depuración usa un adaptador propio de ST, compatible con ST-LINK y con J-Link. La guía del primer proyecto indica generar en CubeMX con la cadena **CMake** y abrir esa carpeta en VS Code.

No uses como camino principal el IDE basado en Eclipse (STM32CubeIDE de escritorio). El manual de la placa todavía lo nombra entre las cadenas admitidas por el fabricante. Aquí queda como alternativa, no como el procedimiento del curso.

La extensión 2.x pedía STM32CubeCLT y, con frecuencia, la extensión Cortex-Debug de terceros. Esas instrucciones no sirven para la 3.x. Si ya tenías la 2.x, desinstálala antes de instalar la 3.x. Así lo recomienda la página de migración.

### Sistema operativo

**Verificado** en la página *System requirements* de la documentación en línea:

| Sistema | Versiones indicadas |
| --- | --- |
| Windows 10 y Windows 11 | 64 bits. Es la plataforma principal de este curso |
| Ubuntu 22.04, 24.04 y 26.04 | 64 bits |
| Fedora 43 y 44 | 64 bits |
| macOS 15 y macOS 26 | Intel y Apple silicon |

El mismo documento pide un procesador de 1,6 GHz o más, 4 GB de RAM, 10 GB libres y una pantalla de al menos 1024×768.

La extensión necesita salida a Internet la primera vez, hacia estos servidores de ST:

- `https://developer.st.com/bundles`, para las herramientas de línea de comandos.
- `https://developer.st.com/st-pack-server/`, para la descripción de los productos.

Si la red de tu empresa intercepta HTTPS, la documentación remite a un artículo de la comunidad sobre proxy y certificados. Sin esos dos servidores el primer proyecto no se puede crear: la propia lista de problemas conocidos dice que un proyecto vacío creado sin red queda defectuoso.

## Instalación en Windows

Haz los pasos en este orden. Un paso saltado suele aparecer después como «la placa no sale».

### 1. Visual Studio Code

1. Descarga el instalador de [code.visualstudio.com](https://code.visualstudio.com/).
2. Instálalo para tu usuario.
3. Ábrelo una vez para que cree el perfil.

UM3512 recomienda un perfil de VS Code dedicado a STM32, porque otras extensiones de C y de C++ pueden chocar con las de ST. En la práctica: *File*, *Preferences*, *Profiles*, crea uno llamado `STM32` y trabaja dentro de ese perfil.

### 2. Extensión de ST

1. En la barra lateral, abre *Extensions*.
2. Busca `STM32`.
3. Instala **STM32CubeIDE for Visual Studio Code**, publicada por STMicroelectronics.
4. Espera a que termine el paquete. La 3.x no es una sola extensión: arrastra varias.

Si migras desde la 2.x, desinstala antes la anterior. La pregunta frecuente de ST lo repite: no instales la nueva encima sin quitar la vieja.

La primera apertura descarga bundles. Hace falta red y puede tardar varios minutos. En la barra de actividad aparece el icono de STM32. Ahí está el gestor de bundles. Déjalo terminar hasta que las filas de compilación y depuración queden al día.

### 3. Controlador de ST-LINK

**Verificado.** La página de instalación dice que, en la versión actual, el usuario instala a mano el controlador de la sonda porque hace falta privilegio de administrador.

1. Abre el icono de STM32CubeIDE for VS Code.
2. En *STM32Cube Resources*, elige **ST-Link USB Drivers**.
3. Acepta el instalador de Windows.

La lista de problemas conocidos describe el síntoma si te saltas este paso en un Windows 11 nuevo: la vista *STM32Cube Devices and Boards* no muestra ninguna placa, y la utilidad de actualización del ST-LINK tampoco la ve.

Linux y macOS no usan ese instalador de Windows. En Ubuntu, si la sesión de depuración se queja de `libncurses5`, la página de problemas conocidos trae el paquete concreto para 22.04, 24.04 y Fedora. En Ubuntu no instales VS Code desde Snap si vas a usar esta extensión: el mismo documento dice que CMake no descubre el proyecto en esa instalación. Usa el paquete `.deb` o `apt`.

### 4. STM32CubeMX

1. Desde la página de STM32CubeMX en st.com, descarga el instalador de Windows.
2. Instálalo. En el primer arranque inicia sesión con una cuenta de ST, o usa el modo que ofrezca el instalador de tu versión, y deja que actualice la base de microcontroladores.
3. Cuando el curso pida un paquete de firmware, CubeMX descarga **STM32CubeF3**. Acepta esa descarga. No copies a mano un árbol de firmware de un tutorial antiguo.

La generación hacia VS Code se hace eligiendo la cadena **CMake** en la pantalla de *Project Manager*. Esa opción es la que describe la guía *Import STM32CubeMX project* de la extensión 3.x.

### 5. Cable y primera detección

**Verificado en el esquema C05.** El conector CN1 está especificado como Neltron `5075BMR-05-SM`, un zócalo Mini-USB tipo B de cinco contactos. Hace falta un cable **Mini-USB con líneas de datos**. Un cable que solo lleva los dos hilos de carga enciende luces y no aparece en el PC.

UM1724, tabla 35, dice que la revisión de placa C-05 cambió el conector CN1. El esquema C05 consultado sigue siendo Mini-B. Si tu etiqueta no dice C05, mira la forma del conector antes de comprar el cable. La sección 3.1 del manual advierte de que el cable depende de la referencia de la placa.

1. Deja los dos puentes de CN2 puestos. Así el ST-LINK apunta al STM32 de la propia tarjeta.
2. Deja JP5 entre los pines 1 y 2. Esa es la posición de fábrica para alimentar desde el USB.
3. Deja JP6 puesto. Si está quitado y no hay un amperímetro, el microcontrolador no recibe alimentación.
4. Enchufa el Mini-USB al CN1 y el otro extremo al PC.
5. En VS Code, abre la vista de dispositivos y placas de la extensión.

**Esperado, según UM1724 §7.6.** LD1, el LED tricolor del ST-LINK, pasa por rojo intermitente, se queda rojo al enumerar y pasa a verde cuando la comunicación con el STM32 de destino queda lista. LD3, el LED rojo de potencia, se enciende cuando la parte del microcontrolador tiene 5 V. Si LD3 no enciende, el PC no concedió los 300 mA que la placa pide con JP1 abierto, o JP5 no está en U5V. El módulo 1 practica esta observación.

## Crear el proyecto de una práctica

Este es el camino que repetirás desde el módulo 3. El módulo 1 todavía no genera código.

### En STM32CubeMX

1. *File*, *New Project*.
2. Pestaña *Board Selector*. Busca `NUCLEO-F303RE`.
3. *Start Project*. Si CubeMX ofrece inicializar los periféricos con la configuración de la placa, acepta. Así PA5 queda como el LED de usuario y PC13 como el pulsador, que es lo que la placa trae cableado.
4. En *Project Manager*:
   - Nombre del proyecto, por ejemplo `m03-parpadeo`.
   - Ruta sin espacios raros, dentro de la carpeta de prácticas.
   - *Toolchain / IDE*: **CMake**.
5. *Generate Code*.

CubeMX crea, entre otros, el archivo `.ioc`, `CMakeLists.txt`, `CMakePresets.json` y las carpetas `Core/Inc` y `Core/Src`. El archivo `main.c` tiene zonas delimitadas por comentarios `USER CODE BEGIN` y `USER CODE END`. Lo que escribas fuera de esas zonas se pierde la próxima vez que pulses *Generate Code*.

### En Visual Studio Code

Según la guía *Open in VS Code* de la extensión:

1. *File*, *Open Folder*, y elige la carpeta del proyecto. No abras solo `main.c`.
2. Cuando VS Code pregunte el *configure preset*, elige **Debug**.
3. En el panel de la extensión, pulsa **Discover STM32Cube project**.
4. En el cuadro de configuración elige la placa NUCLEO-F303RE, la cadena GNU Arm y el proyecto principal. *Save and close*.
5. CMake configura y crea `build/Debug`.

El preset Debug es el que usarás mientras aprendes, porque conserva información para el depurador. El preset Release existe para optimizar. No lo uses para seguir un fallo línea a línea.

### Compilar

En la vista de CMake, pulsa el botón de construcción del objetivo activo. También vale el atajo de construcción de VS Code cuando la extensión ha registrado la tarea.

**Esperado.** La salida termina sin la palabra `error` y aparece un archivo `.elf` dentro de la carpeta de construcción. La página de depuración dice que, si VS Code no sabe qué depurar, casi siempre falta ese `.elf` porque la compilación no llegó a buen puerto.

Errores de compilación frecuentes, tomados de la página *Build* de la extensión:

- Un archivo de cabecera que no se encuentra: la configuración de CMake no se ejecutó, o se generó el código y no se volvió a descubrir el proyecto.
- Un símbolo sin definir: falta un fuente en la lista de CMake, normalmente porque se creó el archivo y no se regeneró.
- Memoria que no cabe: el mapa del enlazador se pasó de Flash o de RAM. En estas prácticas iniciales no debería ocurrir.
- `Cannot activate the STM32Cube Debug Core` por una dependencia que no encuentra: cierra VS Code y ábrelo otra vez. Es un problema conocido de la extensión.

### Grabar y depurar

1. Abre *Run and Debug* con Ctrl+Shift+D.
2. Pulsa el botón de depuración. Si pregunta la sonda, elige el ST-LINK de la tarjeta.
3. Si el firmware del ST-LINK pide actualización, la vista de dispositivos tiene una acción para hacerlo. La página de depuración lo señala como el fallo más habitual del primer arranque.
4. La extensión crea una configuración de tipo `stlinkgdbtarget`. Si quieres conservarla, crea un `launch.json` desde el enlace *create a launch.json file*. El archivo tiene que estar en `.vscode` en la raíz del proyecto. La configuración generada al vuelo no se guarda al cerrar la sesión.

Con la ejecución parada en un punto de ruptura puedes leer la vista *Variables*, los registros del núcleo y la vista de periféricos. Poner un punto de ruptura es pulsar a la izquierda del número de línea.

La pregunta frecuente de ST distingue esto de la *live watch* de CubeIDE: ver y modificar variables mientras el programa sigue corriendo no estaba en la versión inicial de la extensión 3.x. Parar en un punto de ruptura y mirar la variable sí está documentado.

El servidor GDB no tiene control de acceso. La propia página de depuración advierte de no exponerlo a una red que no sea de confianza.

### Puerto serie virtual

La pregunta frecuente confirma que la extensión trae un **SERIAL MONITOR**. Con la configuración de fábrica, ese puerto es el USART2 del STM32F303RET6 (PA2 transmisión, PA3 recepción) a través del ST-LINK.

En Windows aparece un puerto COM nuevo cuando la placa enumera. En el monitor eliges ese puerto, la velocidad que hayas configurado en CubeMX y 8 bits de datos, sin paridad y un bit de parada, salvo que el módulo diga otra cosa.

No hace falta un adaptador USB-serie externo para hablar con el PC mientras SB13 y SB14 sigan cerrados. Esos puentes son el camino de fábrica.

## Errores frecuentes de puesta en marcha

| Lo que ves | Causa documentada | Qué hacer |
| --- | --- | --- |
| No aparece ninguna placa | Falta el controlador de ST-LINK en Windows, o el cable no tiene datos | Instalar el controlador desde la extensión. Probar otro cable Mini-USB |
| LD3 apagado y el MCU no responde | El PC no dio 300 mA, JP5 no está en 1-2, o JP6 está abierto | Revisar los tres jumpers. UM1724 §7.5.1 y §7.8 |
| La placa se alimenta con un cargador de pared y LD3 sigue apagado | No hay enumeración USB, así que no se cierra el camino de 5 V | Poner JP1 en ON, como indica la nota de §7.5.1, o usar un puerto de un PC |
| El depurador no encuentra el `.elf` | La compilación no terminó | Leer el registro de CMake y corregir antes de depurar |
| El ST-LINK pide actualizar el firmware | La versión de la sonda es anterior a la que espera la herramienta | Actualizar desde la vista de dispositivos |
| Proyecto vacío creado sin red | Problema conocido: el proyecto queda mal generado | Crearlo con acceso a los servidores de ST |
| VS Code instalado con Snap en Ubuntu | Problema conocido: CMake no descubre el proyecto | Instalar VS Code con `.deb` o `apt` |
| Choca una extensión de C/C++ de Microsoft | La página de migración lo lista como conflicto posible | Usar el perfil dedicado y no mezclar el paquete de C/C++ de Microsoft con el de ST |

## Lo que este curso no va a hacer

- No va a tratar la NUCLEO-F303RE como si tuviera Wi-Fi, Ethernet o una borna de 24 V. No los tiene.
- No va a conectar 230 V, 24 V, 0–10 V ni 4–20 mA a un pin. Esas señales entran por una etapa externa, en el módulo 27.
- No va a presentar un prototipo de prácticas como un equipo listo para un cuadro industrial.

## Siguiente página

El índice, el mapa de pines que usarán todos los módulos y la matriz de materiales están en [Índice y matriz](01-indice-y-matriz.md).
