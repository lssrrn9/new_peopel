"""Módulo 7 — Parámetros, panel del drive y SigmaWin+."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, FIG, FUENTE, FUENTE_SW, GRAY,
                     GRAY_LINE, GREEN, INK, LIGHT, LIGHT_BLUE, NAVY,
                     NAVY_SOFT, RED, WHITE, Card, Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 07",
        "Parámetros, panel y SigmaWin+",
        [
            "El panel frontal: leer el estado y navegar sin PC",
            "La lógica `Pn` / `Fn` / `Un` y cómo se editan los parámetros",
            "SigmaWin+ Ver.7: conexión, menú y flujo de trabajo con pantallas reales",
            "JOG, monitor, traza, autoajuste, análisis mecánico y alarmas",
            "El engranaje electrónico explicado con números",
            "Los parámetros que realmente vas a tocar y la copia de seguridad",
        ],
        duration="5 h",
        notes=(
            "A partir de aquí el curso se vuelve práctico con el equipo. Si dispone "
            "de un drive, mantenga este módulo con el equipo encendido y el PC "
            "conectado.\n\n"
            "Regla que hay que establecer desde el principio: antes de tocar nada, "
            "guardar una copia de la configuración actual. Siempre."
        ),
    )

    _diagrama_panel(d)

    d.cards_slide(
        "La lógica de la Σ-X: `Pn`, `Fn` y `Un`",
        [
            Card(
                "`Pn___` — Parámetros",
                "**Configuran** el comportamiento del drive y se guardan en memoria "
                "no volátil.\n"
                "· Numéricos: `Pn100` = 40,0 Hz.\n"
                "· De selección por dígitos: `Pn000.1` selecciona el modo de "
                "control.\n"
                "· Algunos exigen apagar y encender para hacerse efectivos.",
                "blue",
            ),
            Card(
                "`Fn___` — Funciones de utilidad",
                "**Ejecutan** una operación: no son valores, son acciones.\n"
                "· `Fn002` JOG · `Fn004` JOG programado.\n"
                "· `Fn005` inicialización de parámetros.\n"
                "· `Fn008` setup del encoder absoluto.\n"
                "· `Fn201` autoajuste avanzado.\n"
                "· `Fn000` historial de alarmas.",
                "amber",
            ),
            Card(
                "`Un___` — Monitores",
                "**Muestran** valores en tiempo real; son de sólo lectura.\n"
                "· `Un000` velocidad del motor.\n"
                "· `Un002` par (% del nominal).\n"
                "· `Un008` error de posición.\n"
                "· `Un005` / `Un006` estado de entradas y salidas.\n"
                "Son la base del diagnóstico rápido.",
                "green",
            ),
        ],
        subtitle="Tres familias, tres propósitos distintos",
        intro="Si entiendes esta clasificación, el manual deja de ser intimidante: "
              "sabes en qué capítulo buscar.",
        notes=(
            "Truco didáctico: pida a los alumnos que asocien cada familia con un "
            "verbo. Pn = configurar. Fn = hacer. Un = mirar.\n\n"
            "Los monitores Un son la herramienta de diagnóstico más rápida que "
            "existe: sin PC, sin cables, directamente en el display. Un005 y Un006 "
            "(estado de entradas y salidas) resuelven en 30 segundos la pregunta "
            "'¿le está llegando la señal de servo ON o no?'."
        ),
    )

    d.steps_slide(
        "Editar un parámetro: procedimiento y precauciones",
        [
            ("Anota el valor actual antes de cambiar nada",
             "Sin excepciones. Si el cambio empeora el comportamiento, tienes que "
             "poder volver atrás en segundos."),
            ("Comprueba si el parámetro se puede cambiar con el servo activo",
             "Muchos parámetros de configuración exigen servo OFF; el drive lo "
             "rechaza o avisa si no se cumple la condición."),
            ("Introduce el nuevo valor y confírmalo",
             "En el panel se navega con las teclas de flecha y se confirma con la "
             "tecla de datos; en SigmaWin+, escribiendo en la celda."),
            ("Verifica si requiere reinicio",
             "El drive lo indica con un aviso (familia `A.941`). Hasta que no se "
             "reinicie, el valor nuevo está escrito pero no aplicado."),
            ("Prueba el efecto de forma controlada",
             "Un cambio cada vez, y comprobando. Cambiar cinco parámetros a la vez "
             "hace imposible saber cuál ha sido el responsable."),
            ("Guarda la configuración completa",
             "Exporta el fichero de parámetros a disco con fecha y descripción del "
             "cambio. Es tu histórico de configuración."),
        ],
        subtitle="La disciplina en el cambio de parámetros ahorra días de trabajo",
        callout=(
            "red",
            "Cuidado con `Fn005` (inicialización de parámetros)",
            "Devuelve el drive a valores de fábrica. Es útil cuando heredas un equipo "
            "con configuración desconocida, pero borra la sintonización y la "
            "asignación de E/S. Nunca lo ejecutes sin tener copia previa.",
        ),
        notes=(
            "El paso 5 es el más importante desde el punto de vista metodológico. En "
            "sintonización, cambiar varias cosas a la vez es la forma más rápida de "
            "perderse.\n\n"
            "Sobre los avisos de reinicio: es una fuente de confusión clásica. El "
            "técnico cambia el parámetro, prueba, no ve diferencia, y concluye que el "
            "parámetro 'no hace nada'. En realidad hacía falta un ciclo de "
            "alimentación.\n\n"
            "Recomiende una convención de nombres para los ficheros de parámetros: "
            "MAQUINA_EJE_FECHA_motivo.  Por ejemplo: LINEA3_EJEX_20240115_ajuste_"
            "ganancias."
        ),
    )

    d.two_col_slide(
        "SigmaWin+: la herramienta imprescindible",
        (
            "Qué te permite hacer",
            [
                "**Editar todos los parámetros** con descripción, rango y unidades a "
                "la vista, en lugar de números crípticos en un display de cinco "
                "dígitos.",
                "**Autoajuste guiado**: los asistentes de sintonización se manejan "
                "mucho mejor desde el PC que desde el panel.",
                "**Traza (osciloscopio software)**: captura consigna, posición real, "
                "error, velocidad, par y corriente sincronizados. Es la herramienta "
                "de diagnóstico definitiva.",
                "**Análisis mecánico**: excitación y respuesta en frecuencia para "
                "localizar resonancias.",
                "**Monitorización en vivo** de todas las variables y del estado de "
                "E/S.",
                "**Copia de seguridad y comparación** entre configuraciones.",
                "**Historial de alarmas** con contexto.",
            ],
        ),
        (
            "Cómo trabajar con él",
            [
                "Conexión habitual por **USB al conector `CN7`**; también por bus en "
                "las variantes de red.",
                "Instala el driver USB antes de conectar; el PC debe reconocer el "
                "drive como dispositivo.",
                "#Flujo de trabajo recomendado",
                "- Abrir proyecto → leer parámetros del drive → **guardar copia "
                "original**.",
                "- Trabajar, ajustar y probar.",
                "- Guardar la nueva versión con fecha y comentario.",
                "- Comparar antes/después con la función de comparación.",
                "#Modo offline",
                "Permite preparar toda la configuración de una máquina **antes** de "
                "ir a planta, y volcarla en minutos durante la puesta en marcha.",
            ],
        ),
        subtitle="Se puede trabajar sin PC, pero es mucho más lento y más arriesgado",
        tones=("blue", "cyan"),
        callout=(
            "green",
            "Consejo profesional",
            "Lleva siempre en el maletín: portátil con SigmaWin+ instalado y "
            "probado, cable USB de repuesto, y una carpeta con las copias de "
            "parámetros de todos los ejes de la planta. Los tres elementos juntos "
            "convierten una avería de un día en una de una hora.",
        ),
        notes=(
            "Insista en la función de traza: es lo que separa el ajuste 'por oído' "
            "del ajuste con criterio. Ver el error de seguimiento en función del "
            "tiempo, superpuesto al perfil de velocidad, permite decidir con datos "
            "qué ganancia tocar.\n\n"
            "El modo offline es un argumento de venta interno muy potente: permite "
            "que un ingeniero prepare toda la configuración desde la oficina y que la "
            "puesta en marcha en cliente se reduzca a volcar y verificar.\n\n"
            "Comente que el SGDXS (Σ-X) se trabaja con **SigmaWin+ Ver.7**. La "
            "versión 5 es otra generación de interfaz: no la mezcle en el aula. "
            "Descargue siempre la última versión compatible desde la web de YASKAWA.\n\n"
            "Las láminas siguientes son capturas oficiales de SigmaWin+ Ver.7 "
            "tomadas del manual SIEP C710812 03I. El aspecto puede variar ligeramente "
            "según la revisión del software, pero los bloques del menú y el flujo "
            "son los mismos."
        ),
    )

    d.figure_slide(
        "Conexión del operador digital al SERVOPACK",
        FIG + "conexion_operador.png",
        subtitle="Comunicación local: `CN3` (RS-422) y `CN7` (USB / SigmaWin+)",
        puntos=[
            "El **operador digital** se conecta al conector `CN3`.",
            "El PC con **SigmaWin+** se conecta al conector USB `CN7`.",
            "Usa **siempre el cable especificado por YASKAWA**: con otro cable la "
            "inmunidad al ruido no está garantizada.",
            "- Modelos de operador habituales: `JUSP-OP05A-1-E` y equivalentes "
            "indicados en el catálogo.",
        ],
        fuente=FUENTE + " · apartados 4.7 y 4.8",
        notes=(
            "La figura del operador digital es textual en el manual: el mensaje "
            "importante es usar el cable original y el conector correcto.\n\n"
            "CN7 es USB; CN3 es el operador. No se intercambian."
        ),
    )

    d.figure_slide(
        "El mapa de SigmaWin+: estado del eje y menú de funciones",
        FIG + "sw_mapa.png",
        subtitle="Una vez en línea, todo se abre desde este menú de nueve bloques",
        puntos=[
            "Arriba: el **estado del eje** (POWER, HBB, P-OT, N-OT, FSTP).",
            "El botón del drive abre el **[Menu]**. Ahí están todas las funciones.",
            "#Los bloques que más vas a usar",
            "- **Basic Functions**: Edit Parameters, Set Up Wizard.",
            "- **Operation**: Jog y Program JOG.",
            "- **Monitor**: Trace, Monitor y Life Monitor.",
            "- **Tuning**: autoajuste y nivel de respuesta.",
            "- **Diagnostic**: Mechanical Analysis y EasyFFT.",
            "- **Troubleshooting**: Display Alarm y Alarm Trace.",
        ],
        fuente=FUENTE_SW + " · apartado 9.2",
        notes=(
            "Esta es la lámina de orientación. El alumno debe poder señalar, sin "
            "pensar, en qué bloque está cada tarea.\n\n"
            "Truco de aula: pida nueve voluntarios y asigne un bloque a cada uno. "
            "Luego lance situaciones ('el eje no gira', 'quiero ver el error de "
            "seguimiento', 'hay una alarma A.720') y que el grupo diga el bloque.\n\n"
            "HBB encendido = el CN8 está abriendo el HWBB: el eje no dará par aunque "
            "todo lo demás esté bien. Es el primer LED que hay que mirar."
        ),
    )

    d.steps_slide(
        "Flujo de trabajo la primera vez que abres SigmaWin+",
        [
            ("Instalar SigmaWin+ Ver.7 y el driver USB",
             "Descárgalo de YASKAWA. Extrae el ZIP completo antes de instalar. "
             "SigmaWin+ 5 y 7 pueden convivir; para la Σ-X usa siempre la 7."),
            ("Conectar el PC al `CN7` con el cable USB original",
             "Enciende primero el SERVOPACK (al menos la alimentación de control) "
             "y después conecta el USB. El PC debe reconocer el dispositivo."),
            ("Arrancar SigmaWin+ y poner el eje en línea",
             "En la ventana Home, añade el servo, elige la comunicación USB y "
             "conéctate. El drive aparece en el workspace con sus LEDs de estado."),
            ("Abrir el menú del eje y **guardar una copia**",
             "`Edit Parameters` → `Export` o `Save to Project`. Esta es la copia "
             "'como llegó'. Sin ella no se toca nada."),
            ("Trabajar en el bloque que corresponda",
             "Setup Wizard o Edit Parameters para configurar. Jog para probar. "
             "Tuning para autoajustar. Trace para medir. Display Alarm si hay fallo."),
            ("Escribir, verificar y volver a guardar",
             "Tras cambiar parámetros: `Write to Servo` → `Edited Parameters`. "
             "Si el drive pide reinicio, ciclo de alimentación. Luego exporta "
             "'como quedó' con fecha y motivo."),
        ],
        subtitle="Seis pasos. El que se salta el 4 es el que un día no puede volver atrás",
        callout=(
            "amber",
            "Verde en la celda = escrito en el PC, no todavía en el drive",
            "Al editar un parámetro, la celda se pone verde. Hasta que no pulses "
            "`Write to Servo` → `Edited Parameters` el SERVOPACK sigue con el valor "
            "anterior. Confundir 'lo he cambiado en pantalla' con 'ya está en el "
            "eje' es el error de principiante más caro.",
        ),
        notes=(
            "Haga este flujo en el banco, en voz alta, la primera vez. Luego pida "
            "a cada alumno que lo repita solo.\n\n"
            "Sobre el driver USB: si el PC no ve el drive, no es un problema de "
            "SigmaWin+, es de Windows. Compruebe el Administrador de dispositivos "
            "antes de reinstalar el software.\n\n"
            "Modo offline: se puede preparar un proyecto sin drive (útil en "
            "oficina). Al llegar a planta se conecta y se vuelca. No sustituye la "
            "copia 'como llegó' del equipo real."
        ),
    )

    d.figure_slide(
        "Editar parámetros: nombre, rango, unidades y escritura",
        FIG + "sw_parametros.png",
        subtitle="`Edit Parameters`: dejas de memorizar códigos de cinco dígitos",
        puntos=[
            "Doble clic en la celda → cambia el valor → **Enter**.",
            "La celda **verde** es un cambio pendiente de escribir al drive.",
            "`Write to Servo` → **Edited Parameters** lo vuelve blanco: ya está "
            "en el SERVOPACK.",
            "Los `Pn` de bits (como `Pn000.0`) se eligen en un desplegable: "
            "sentido de giro, modo de parada…",
            "Los `Pn` numéricos (`Pn100`, `Pn101`, `Pn102`) muestran **rango y "
            "valor por defecto** en un recuadro.",
            "- `Read from Servo` recarga lo que hay realmente en el equipo.",
        ],
        fuente=FUENTE_SW + " · apartado 5.1.3",
        notes=(
            "Demuestre en vivo el ciclo verde → Write → blanco. Es el gesto que "
            "hay que automatizar.\n\n"
            "Compare con el panel: en el display no ves el nombre, ni el rango, "
            "ni las unidades. Por eso se edita mal y se confirma peor.\n\n"
            "Edited Parameters vs All Parameters: lo normal es escribir sólo lo "
            "cambiado. All Parameters se usa al clonar un eje o al restaurar un "
            "fichero completo."
        ),
    )

    d.figure_slide(
        "JOG desde SigmaWin+: el primer movimiento del motor",
        FIG + "sw_jog.png",
        subtitle="`Operation` → `Jog` · el eje se mueve sólo mientras mantienes el ratón",
        puntos=[
            "Ruta: **[Operation] → [Jog]**.",
            "La velocidad es `Pn304`. Empieza baja: 50–100 min⁻¹, no 500.",
            "1) **Servo ON**. El indicador pasa a verde.",
            "2) Mantén **Forward (+)** o **Reverse (−)**. Al soltar, para.",
            "Antes de pulsar OK, el software avisa: **P-OT y N-OT quedan "
            "deshabilitados** durante el JOG. El eje no respetará finales de "
            "carrera.",
            "- Tras el JOG, ciclo de alimentación si el manual lo pide.",
        ],
        fuente=FUENTE_SW + " · apartado 7.3.3",
        callout=(
            "red",
            "El JOG no es un movimiento 'suave de prueba'",
            "Con los OT desactivados y sin el ciclo del PLC, eres tú el único "
            "límite. Zona despejada, E-stop a mano y nadie cerca del mecanismo.",
        ),
        notes=(
            "El JOG es la prueba de que potencia, encoder y motor están bien. Si "
            "el motor no gira aquí, no tiene sentido pasar al PLC.\n\n"
            "Insista en el 'dead-man': sólo se mueve mientras se mantiene el "
            "botón. Eso evita que un clic accidental deje el eje lanzado.\n\n"
            "Pn304 a 500 min⁻¹ como en la captura del manual es demasiado para "
            "un primer arranque didáctico. Bájelo."
        ),
    )

    d.figure_slide(
        "Monitor en vivo: lo que el panel muestra, pero entero",
        FIG + "sw_monitor.png",
        subtitle="`Monitor` → `Monitor` · pestañas Operation, Status e I/O",
        puntos=[
            "Equivalente software de los monitores `Un`, con nombres y unidades.",
            "**Operation**: velocidad, consigna, error de posición, carga, "
            "regeneración y alarma actual.",
            "**Status**: `/S-RDY`, `/COIN`, `/BK`, freno dinámico, avisos.",
            "**I/O**: el estado real de cada entrada y salida de `CN1`.",
            "En la captura aparece `A.810` (batería del encoder): el monitor "
            "no miente aunque el eje 'parezca parado'.",
            "- Si `/S-ON` no llega, se ve aquí antes de tocar ganancias.",
        ],
        fuente=FUENTE_SW + " · apartado 9.2.2",
        notes=(
            "Rutina de tres pestañas: Operation (¿qué hace el eje?), Status "
            "(¿está listo?) e I/O (¿le llegan las señales?).\n\n"
            "A.810 es un ejemplo didáctico excelente: mucha gente busca un fallo "
            "de sintonización y es la pila del encoder absoluto.\n\n"
            "Compare con Un005/Un006 del panel: misma información, menos cómoda."
        ),
    )

    d.figure_slide(
        "La traza: el osciloscopio que lleva el SERVOPACK dentro",
        FIG + "sw_traza.png",
        subtitle="`Monitor` → `Trace` · consigna, real, error, par y E/S en la misma base de tiempos",
        puntos=[
            "`Setting` abre **Trace Setting**: qué señales, con qué muestreo "
            "y con qué disparo.",
            "Señales típicas: **Feedback Speed**, **Torque Reference**, "
            "error de posición, `/S-ON`.",
            "El **trigger** (flanco, umbral, pre-trigger) evita capturar a ciegas.",
            "Muestreo de ejemplo: 125 µs × 1024 = 128 ms de ventana.",
            "Guarda la captura (y el CSV) **antes y después** de cada ajuste.",
            "- Sin traza, la sintonización es opinión. Con traza, es medida.",
        ],
        fuente=FUENTE_SW + " · apartado 9.3.2",
        notes=(
            "Esta es la herramienta que separa al técnico que 'o ye el eje' del "
            "que decide con datos. Dedíquele tiempo de práctica.\n\n"
            "Ejercicio: capture un posicionamiento, identifique sobrepaso, tiempo "
            "de establecimiento y par de punta. Luego suba Pn102 un 20 % y "
            "repita. La comparación enseña más que diez láminas.\n\n"
            "Real Time Trace es la versión continua; Trace es la de disparo, más "
            "útil para un ciclo concreto."
        ),
    )

    d.figure_slide(
        "Autoajuste guiado: el drive propone las ganancias",
        FIG + "sw_autoajuste.png",
        subtitle="`Tuning` → `Tuning` · Autotuning without a Host Reference (`Fn201`)",
        puntos=[
            "El asistente pide **Servo ON**, modo (posicionado), mecánica "
            "(husillo, correa…) y recorrido.",
            "`Start tuning` → confirmación de seguridad → el eje se mueve solo.",
            "Al terminar ves **settling time**, overshoot y la tabla "
            "`Value (before)` / `Value (after)` en rojo.",
            "En el ejemplo, `Pn100` pasa de 400 a 2400 (0,1 Hz): el autoajuste "
            "ha subido la ganancia de velocidad.",
            "También enciende notch, control de vibración y filtros si los "
            "detecta.",
            "- Carga **real** acoplada y recorrido libre. Nunca en vacío.",
        ],
        fuente=FUENTE_SW + " · apartado 8.7",
        callout=(
            "red",
            "El autoajuste mueve el eje con vibración deliberada",
            "Nunca en un vertical sin freno verificado, ni con gente cerca, ni "
            "con recorrido insuficiente. El E-stop tiene que estar a mano.",
        ),
        notes=(
            "Muestre la tabla before/after: es la prueba de que el software no "
            "es 'magia', escribe Pn100, Pn101, Pn102, Pn103, filtros…\n\n"
            "Después del autoajuste, verifique con el ciclo real y con la traza. "
            "Aceptar a ciegas el resultado es tan malo como no usarlo.\n\n"
            "El detalle de Pn103 (inercia) es el puente con el Módulo 04: "
            "compare el valor medido con el calculado."
        ),
    )

    d.figure_slide(
        "Análisis mecánico: ver la resonancia en un diagrama de Bode",
        FIG + "sw_analisis.png",
        subtitle="`Diagnostic` → `Mechanical Analysis` · de la frecuencia al filtro notch",
        puntos=[
            "`START` excita el eje y traza **ganancia (dB)** y **fase** frente "
            "a la frecuencia.",
            "El software marca **resonancia** y **antirresonancia** (en el "
            "ejemplo: 1320 Hz y 984 Hz).",
            "Esa frecuencia se copia al filtro notch (`Pn409` / pestaña "
            "`Notch Filter Setting`).",
            "`EasyFFT` (`Fn206`) es la versión rápida: detecta el pico y "
            "propone el notch.",
            "- Úsalo con ganancia baja, al principio del ajuste. A ganancia "
            "alta puede vibrar de más.",
        ],
        fuente=FUENTE_SW + " · apartado 8.17",
        notes=(
            "Conecte esta lámina con el Módulo 09: notch, EasyFFT y análisis "
            "en frecuencia dejan de ser abstractos cuando se ve la gráfica.\n\n"
            "Interpretación mínima: un pico de ganancia = la mecánica 'canta' "
            "a esa frecuencia. El notch la atenúa para poder subir ganancias "
            "sin que el eje silbe o oscile."
        ),
    )

    d.figure_slide(
        "Alarmas e historial: el primer sitio al que ir cuando el eje para",
        FIG + "sw_alarmas.png",
        subtitle="`Troubleshooting` → `Display Alarm` · código, nombre y cuándo ocurrió",
        puntos=[
            "Pestaña **Alarm diagnosis**: alarma activa y guía de causas.",
            "Pestaña **Alarm History**: lista persistente (no se borra al "
            "resetear ni al apagar).",
            "Columnas: número, nombre (`A.C90`, `A.041`…) y tiempo acumulado "
            "de funcionamiento.",
            "`Clear` borra el historial. Úsalo sólo cuando hayas documentado.",
            "Desde aquí se puede abrir la **traza de alarma** si el drive la "
            "ha guardado.",
            "- Elimina la causa **antes** de resetear. Si no, volverá.",
        ],
        fuente=FUENTE_SW + " · apartado 13.2",
        notes=(
            "El historial es oro en mantenimiento: '¿esto es nuevo o ya pasaba "
            "hace dos semanas?'. Enséñeles a no pulsar Clear por higiene.\n\n"
            "Puente con el Módulo 11: el método de diagnóstico empieza siempre "
            "aquí, no en cambiar ganancias."
        ),
    )

    d.cards_slide(
        "Qué pantalla abrir según lo que necesites",
        [
            Card(
                "Configurar el eje",
                "**Set Up Wizard** para la primera puesta en servicio.\n"
                "**Edit Parameters** para un cambio puntual o para clonar un eje "
                "(`Export` / `Import`).",
                "blue",
            ),
            Card(
                "Mover y comprobar",
                "**Jog**: ¿gira el motor?\n"
                "**Program JOG**: un ciclo repetido sin PLC.\n"
                "**Wiring Check** / **I/O Monitor**: ¿llegan `/S-ON`, P-OT, N-OT?",
                "cyan",
            ),
            Card(
                "Medir y sintonizar",
                "**Monitor**: números en vivo.\n"
                "**Trace**: la forma de onda.\n"
                "**Tuning**: autoajuste.\n"
                "**Mechanical Analysis / EasyFFT**: resonancias.",
                "green",
            ),
            Card(
                "Cuando algo va mal",
                "**Display Alarm** e historial.\n"
                "**Alarm Trace**: qué hacía el eje en el instante del fallo.\n"
                "LEDs del workspace: HBB, P-OT, N-OT, POWER.",
                "amber",
            ),
        ],
        subtitle="No memorices 400 funciones: memoriza estas cuatro preguntas",
        columns=2,
        notes=(
            "Cierre del bloque de software con una chuleta. Imprímala y péguela "
            "en el maletín junto al cable USB.\n\n"
            "Recuerde: el panel frontal sigue siendo válido para JOG, Un y Fn "
            "cuando no hay PC. SigmaWin+ no sustituye el criterio; lo acelera."
        ),
    )

    d.figure_slide(
        "Monitor analógico `CN5`",
        FIG + "monitor_analogico.png",
        subtitle="Salida para osciloscopio: velocidad, par y error en tiempo real",
        puntos=[
            "Conecta un instrumento de medida al conector `CN5`.",
            "Permite ver en un osciloscopio las señales internas del lazo.",
            "Es especialmente útil en **sintonización avanzada** (Módulo 09).",
            "- El instrumento no lo suministra YASKAWA.",
        ],
        fuente=FUENTE + " · apartado 4.10",
        notes=(
            "CN5 es una herramienta poco conocida y muy valiosa. En ejes difíciles, "
            "ver la señal real en un osciloscopio sigue siendo insustituible."
        ),
    )

    _diagrama_engranaje(d)

    d.table_slide(
        "Engranaje electrónico: tres ejemplos resueltos",
        ["Aplicación", "Unidad de referencia deseada", "Cálculo", "Resultado"],
        [
            ["Husillo de 20 mm de paso, acoplamiento directo",
             "1 unidad = 0,001 mm (1 µm)",
             "Vueltas por 1 mm = 1/20. Unidades por vuelta = 20 mm × 1.000 = 20.000",
             "`B/A` = 16.777.216 / 20.000"],
            ["Mesa rotativa con reductor 10:1",
             "1 unidad = 0,001° (360.000 unidades por vuelta de mesa)",
             "Una vuelta de mesa = 10 vueltas de motor = 167.772.160 cuentas",
             "`B/A` = 167.772.160 / 360.000"],
            ["Cinta con polea de 100 mm de diámetro, reductor 5:1",
             "1 unidad = 0,01 mm",
             "Perímetro = 314,16 mm por vuelta de polea = 5 vueltas de motor",
             "`B/A` = (16.777.216 × 5) / 31.416"],
        ],
        [3.0, 2.6, 4.2, 2.5],
        subtitle="`Pn20E` (numerador B) y `Pn210` (denominador A)",
        size=9.5,
        foot="Simplifica siempre la fracción antes de escribirla y comprueba que "
             "numerador y denominador caben en el rango admitido por los parámetros. "
             "Si no es exacta, quedará un error de redondeo acumulativo.",
        notes=(
            "El caso de la mesa rotativa merece atención: si la fracción no es exacta, "
            "el error se acumula vuelta tras vuelta y al cabo de miles de "
            "posicionados la mesa se ha 'ido'. En ejes rotativos infinitos hay que "
            "elegir la unidad de referencia de modo que la fracción sea exacta, o "
            "usar la función de límite multivuelta coherente con la relación de "
            "transmisión.\n\n"
            "Comprobación práctica infalible tras configurar el engranaje: ordena un "
            "movimiento de 100 mm (o de 100 unidades conocidas) y **mídelo con un "
            "metro o un comparador**. Si no coincide, el engranaje está mal. Esta "
            "comprobación de 2 minutos evita fallos que aparecerían meses después."
        ),
    )

    d.table_slide(
        "Los parámetros que más vas a tocar (1/2)",
        ["Parámetro", "Qué hace", "Comentario práctico"],
        [
            ["`Pn000.0`", "Sentido de giro (rotación inversa)",
             "Se cambia aquí, **no** intercambiando fases del motor"],
            ["`Pn000.1`", "Selección del modo de control",
             "Par, velocidad, posición o combinados"],
            ["`Pn001.0`", "Método de parada ante alarma o servo OFF",
             "Freno dinámico, rampa o marcha libre"],
            ["`Pn20E` / `Pn210`", "Engranaje electrónico (numerador/denominador)",
             "Define la unidad de referencia de todo el eje"],
            ["`Pn212`", "Pulsos de salida del encoder",
             "Sólo si el controlador necesita realimentación"],
            ["`Pn50A` / `Pn50B`", "Asignación de entradas digitales",
             "Permite forzar señales sin cablearlas: úsalo con cabeza"],
            ["`Pn50E` / `Pn50F` / `Pn510`", "Asignación de salidas digitales",
             "Aquí se asigna `/BK`, `/COIN`, `/S-RDY`…"],
            ["`Pn522`", "Ventana de posicionado (`/COIN`)",
             "Determina cuándo el PLC recibe 'posición alcanzada'"],
            ["`Pn520`", "Nivel de alarma por exceso de error de posición",
             "Protege la mecánica; si salta, revisa dimensionamiento o ganancias"],
            ["`Pn506` / `Pn507` / `Pn508`", "Temporización del freno de retención",
             "Críticos en ejes verticales"],
        ],
        [2.5, 4.4, 5.1],
        subtitle="Configuración básica del eje",
        size=9.5,
        notes=(
            "Pn000.0 merece un comentario: cambiar el sentido de giro por parámetro "
            "es lo correcto. Intercambiar dos fases del motor 'para que gire al "
            "revés' es un error grave: el encoder sigue indicando el sentido "
            "original, la realimentación queda invertida y el eje se embala o dispara "
            "alarma.\n\n"
            "Pn520 es el guardián de la mecánica: si el eje no puede seguir la "
            "consigna (choque, atasco, dimensionamiento insuficiente), esta alarma "
            "detiene el movimiento antes de romper algo. No lo suba sin entender por "
            "qué está saltando."
        ),
    )

    d.table_slide(
        "Los parámetros que más vas a tocar (2/2)",
        ["Parámetro", "Qué hace", "Comentario práctico"],
        [
            ["`Pn100`", "Ganancia del lazo de velocidad [Hz]",
             "El parámetro central de la sintonización"],
            ["`Pn101`", "Constante de tiempo integral de velocidad [ms]",
             "Se baja para más rigidez; demasiado bajo, oscila"],
            ["`Pn102`", "Ganancia del lazo de posición [1/s]",
             "Determina el error de seguimiento"],
            ["`Pn103`", "Relación de inercias [%]",
             "**Ajústalo primero**: el resto de ganancias se escalan con él"],
            ["`Pn401`", "Constante de tiempo del filtro de par [ms]",
             "Suaviza el ruido; demasiado alto, resta rapidez"],
            ["`Pn408`", "Habilitación de filtros notch y de fricción",
             "Bits de activación de las funciones de filtrado"],
            ["`Pn409` / `Pn40A`", "Frecuencia y factor Q del 1.er filtro notch",
             "Contra resonancia mecánica de alta frecuencia"],
            ["`Pn140`", "Control por modelo de referencia (MFC)",
             "Mejora el seguimiento sin sacrificar estabilidad"],
            ["`Pn14A`", "Frecuencia de supresión de vibración",
             "Contra oscilación de baja frecuencia de la estructura"],
            ["`Pn170`", "Función de ajuste sin sintonizar (tuning-less)",
             "Activa de fábrica; desactívala al pasar a ajuste manual"],
            ["`Pn304`", "Velocidad de JOG [rpm]",
             "Ponla baja (50-100 rpm) para las primeras pruebas"],
            ["`Pn600`", "Capacidad de la resistencia de regeneración",
             "Declara la resistencia externa si la instalas"],
        ],
        [2.5, 4.4, 5.1],
        subtitle="Sintonización, filtros y pruebas",
        size=9.5,
        foot="Estos parámetros se explican en detalle en el Módulo 09. Aquí sólo "
             "interesa saber que existen y dónde están.",
        notes=(
            "No entre en detalle aquí: es un mapa, no el territorio. Basta con que el "
            "alumno sepa que existe un conjunto reducido de parámetros que resuelve "
            "el 95 % de los casos.\n\n"
            "Mensaje importante: el manual tiene cientos de parámetros, pero en la "
            "práctica un especialista toca habitualmente unos veinte. Eso "
            "tranquiliza mucho a quien empieza."
        ),
    )

    d.table_slide(
        "Monitores `Un` para diagnóstico rápido",
        ["Monitor", "Qué muestra", "Cómo se usa en la práctica"],
        [
            ["`Un000`", "Velocidad real del motor [rpm]",
             "Comprobar que el eje se mueve a la velocidad esperada"],
            ["`Un001`", "Consigna de velocidad [rpm]",
             "Comparar con `Un000`: si difieren mucho, el eje no sigue"],
            ["`Un002`", "Par actual [% del nominal]",
             "**El monitor más útil**: valida el dimensionamiento en la máquina real"],
            ["`Un005`", "Estado de las entradas digitales",
             "¿Llega el servo ON? ¿Están los finales de carrera cerrados?"],
            ["`Un006`", "Estado de las salidas digitales",
             "¿Se está dando la orden de freno? ¿Está activa la alarma?"],
            ["`Un007`", "Velocidad de la consigna de pulsos",
             "Verifica que el controlador está enviando pulsos"],
            ["`Un008`", "Error de posición [unidades de referencia]",
             "Mide la calidad del seguimiento; base del ajuste de `Pn522`"],
            ["`Un00D`", "Contador de realimentación de posición",
             "Comprobar repetibilidad tras un ciclo completo"],
            ["`Un00B`", "Relación de carga / tasa de sobrecarga acumulada",
             "Anticipa alarmas `A.720` antes de que ocurran"],
        ],
        [1.7, 4.3, 6.0],
        subtitle="Diagnóstico sin PC, directamente en el display",
        size=10.0,
        foot="La numeración concreta de algunos monitores varía entre series: "
             "consulta la lista del manual de tu equipo.",
        notes=(
            "Enseñe la rutina de diagnóstico en tres monitores: Un005 (¿llegan las "
            "señales?), Un002 (¿cuánto par está pidiendo?) y Un008 (¿está siguiendo "
            "la consigna?). Con esos tres se descarta el 70 % de las causas en "
            "cinco minutos.\n\n"
            "Un002 tiene un valor especial para el ingeniero: permite comparar el par "
            "real con el calculado en el Módulo 04. Si el eje pide un 90 % de par "
            "donde el cálculo decía 47 %, hay un problema mecánico que hay que "
            "resolver antes de que rompa algo."
        ),
    )

    d.steps_slide(
        "Copia de seguridad y gestión de configuraciones",
        [
            ("Copia inicial en la puesta en marcha",
             "Antes de tocar nada y después de terminar el ajuste. Dos ficheros: "
             "'como llegó' y 'como quedó'."),
            ("Copia tras cada intervención",
             "Con fecha, autor y motivo del cambio en el nombre del fichero o en un "
             "comentario del proyecto."),
            ("Archivo centralizado y accesible",
             "En el servidor de mantenimiento, no en el portátil de una persona. "
             "Debe estar disponible a las 3 de la mañana."),
            ("Documento de eje en papel dentro del armario",
             "Modelo de drive y motor, parámetros críticos, valor de origen y fecha "
             "de la última sintonización."),
            ("Procedimiento de sustitución probado",
             "Cargar parámetros en el drive nuevo, ejecutar `Fn008` si el encoder es "
             "absoluto, rehacer origen y verificar el ciclo."),
        ],
        subtitle="La copia que no existe es la que siempre hace falta",
        callout=(
            "amber",
            "Detalle que se olvida siempre",
            "El fichero de parámetros **no** contiene el origen de la máquina ni la "
            "posición absoluta del encoder. Tras sustituir un drive o un motor, hay "
            "que rehacer el origen aunque los parámetros sean idénticos.",
        ),
        notes=(
            "Este es el módulo donde conviene hablar de gestión: el mejor técnico del "
            "mundo no puede arreglar en una hora una máquina cuya configuración se "
            "perdió.\n\n"
            "Proponga un formato de etiqueta para pegar dentro del armario, junto al "
            "drive, con: modelo de drive, modelo de motor, versión de firmware, fecha "
            "de puesta en marcha, fecha del último cambio de batería y ruta del "
            "fichero de parámetros en el servidor."
        ),
    )


# --------------------------------------------------------------------------
# Diagramas
# --------------------------------------------------------------------------

def _diagrama_panel(d: Deck) -> None:
    slide = d.canvas_slide(
        "El panel frontal: leer el estado sin PC",
        "Cinco dígitos que te dicen casi todo",
        notes=(
            "Enseñe a interpretar el display en el equipo real. Al energizar, el "
            "drive muestra su estado; ante un fallo, el código de alarma con el "
            "formato A.xxx.\n\n"
            "La navegación por el panel sigue siempre el mismo patrón: se elige la "
            "familia de función (parámetros, monitores, funciones de utilidad), se "
            "navega hasta el número deseado, se entra en el valor, se modifica y se "
            "confirma.\n\n"
            "El panel es suficiente para diagnóstico y para cambios puntuales, pero "
            "para sintonizar o para cargar una configuración completa hay que usar "
            "SigmaWin+. Nadie sintoniza un eje con cinco dígitos y cuatro teclas.\n\n"
            "Detalle útil: el punto decimal parpadeante en algunos dígitos indica "
            "estados concretos (por ejemplo, que el valor mostrado está pendiente de "
            "confirmación). Consulte la leyenda del manual."
        ),
    )

    # Panel
    px, py = Inches(0.8), Inches(1.90)
    pw, ph = Inches(4.6), Inches(3.1)
    d._rect(slide, px, py, pw, ph, fill=NAVY, line=NAVY)
    d._rect(slide, px + Inches(0.45), py + Inches(0.45), Inches(3.7),
            Inches(1.05), fill=INK, line=CYAN, line_w=Pt(1.5))
    d._text(slide, px + Inches(0.45), py + Inches(0.62), Inches(3.7),
            Inches(0.7), "A.7 2 0", size=Pt(34), color=CYAN, bold=True,
            align=PP_ALIGN.CENTER, font="Consolas")

    teclas = ["MODE/SET", "▲", "▼", "◀ / DATA"]
    tw = Inches(0.95)
    tx = px + Inches(0.30)
    for t in teclas:
        d.box(slide, tx, py + Inches(1.85), tw, Inches(0.62), t, GRAY,
              size=9.5, radius=0.15)
        tx += tw + Inches(0.12)
    d.label(slide, px, py + ph + Inches(0.14), pw,
            "Display de 5 dígitos y 4 teclas de navegación", size=10,
            color=GRAY)

    # Lecturas típicas
    d._rect(slide, Inches(5.85), Inches(1.90), Inches(6.85), Inches(3.1),
            fill=LIGHT, line=GRAY_LINE)
    d._text(slide, Inches(6.10), Inches(2.05), Inches(6.3), Inches(0.3),
            "Qué estás viendo en el display", size=Pt(13), color=NAVY,
            bold=True)
    filas = [
        ("Estado de funcionamiento", "El drive indica si está listo, con el servo "
         "activo o en baseblock", BLUE),
        ("`A.___`", "Código de **alarma**: el eje está parado y hay que actuar", RED),
        ("`A.9__`", "Código de **aviso** (warning): el eje sigue funcionando, pero "
         "algo va mal", AMBER),
        ("Valor numérico", "Monitor `Un` o parámetro `Pn` que estás consultando o "
         "editando", GREEN),
    ]
    y = Inches(2.50)
    for titulo, desc, color in filas:
        d._rect(slide, Inches(6.10), y, Inches(6.3), Inches(0.55), fill=WHITE,
                line=GRAY_LINE)
        d._rect(slide, Inches(6.10), y, Inches(0.06), Inches(0.55), fill=color)
        d._text(slide, Inches(6.32), y + Inches(0.05), Inches(1.9),
                Inches(0.25), titulo, size=Pt(10), color=color, bold=True)
        d._text(slide, Inches(6.32), y + Inches(0.28), Inches(5.9),
                Inches(0.25), desc, size=Pt(9.5), color=GRAY)
        y += Inches(0.62)

    d.callout(slide, Inches(0.8), Inches(5.35), Inches(11.9), Inches(1.05),
              "blue", "Los tres gestos que hay que dominar en el panel",
              "1) Consultar un monitor `Un` para ver qué está pasando.   "
              "2) Leer el historial de alarmas con `Fn000` para saber qué pasó "
              "antes.   3) Ejecutar un JOG con `Fn002` para comprobar que el motor "
              "responde. Todo lo demás es más cómodo desde SigmaWin+.")


def _diagrama_engranaje(d: Deck) -> None:
    slide = d.canvas_slide(
        "El engranaje electrónico",
        "Convierte 'unidades del programador' en cuentas de encoder",
        notes=(
            "Este concepto genera muchas dudas, así que conviene explicarlo con una "
            "pregunta: ¿en qué unidades quieres programar la máquina? ¿En milímetros? "
            "¿En micras? ¿En grados? El engranaje electrónico es lo que traduce esa "
            "unidad de referencia a cuentas del encoder.\n\n"
            "Fórmula general: B/A = (resolución del encoder × relación de "
            "transmisión) / (unidades de referencia por vuelta del eje de carga).\n\n"
            "Ejemplo del diagrama: encoder de 24 bits (16.777.216 cuentas/vuelta), "
            "husillo de 20 mm de paso, y queremos programar en micras. Una vuelta de "
            "motor son 20 mm = 20.000 micras. Luego B/A = 16.777.216 / 20.000.\n\n"
            "Dos advertencias:\n"
            "1) Si la fracción no es exacta, hay error de redondeo que se acumula. "
            "Elija unidades que den fracciones exactas siempre que pueda.\n"
            "2) Cambiar el engranaje cambia el significado de TODOS los parámetros "
            "expresados en unidades de referencia (Pn522, Pn520, velocidades de "
            "consigna). Hay que revisarlos después."
        ),
    )

    y = Inches(2.30)
    h = Inches(1.05)
    cajas = [
        ("CONTROLADOR\npiensa en micras", BLUE, Inches(2.75)),
        ("ENGRANAJE\nELECTRÓNICO\n`Pn20E` / `Pn210`", AMBER, Inches(2.75)),
        ("DRIVE\npiensa en cuentas\nde encoder", NAVY, Inches(2.75)),
        ("MOTOR + HUSILLO\nse mueve en mm", CYAN, Inches(2.75)),
    ]
    x = Inches(0.62)
    for texto, color, w in cajas:
        d.box(slide, x, y, w, h, texto, color, size=11, radius=0.10)
        if x + w < Inches(12.0):
            d.arrow(slide, x + w + Inches(0.04), y + h / 2 - Inches(0.10),
                    Inches(0.20), Inches(0.20), color=GRAY)
        x += w + Inches(0.28)

    # Fórmula
    d._rect(slide, Inches(0.62), Inches(3.85), Inches(12.1), Inches(1.15),
            fill=LIGHT_BLUE, line=BLUE, line_w=Pt(0.75))
    d._text(slide, Inches(0.62), Inches(4.00), Inches(12.1), Inches(0.35),
            "B / A  =  (resolución del encoder × relación de transmisión)  /  "
            "(unidades de referencia por vuelta del eje de carga)",
            size=Pt(14), color=NAVY, bold=True, align=PP_ALIGN.CENTER)
    d._text(slide, Inches(0.62), Inches(4.45), Inches(12.1), Inches(0.4),
            "B = `Pn20E` (numerador)          A = `Pn210` (denominador)",
            size=Pt(12), color=GRAY, align=PP_ALIGN.CENTER)

    # Ejemplo
    d._rect(slide, Inches(0.62), Inches(5.20), Inches(12.1), Inches(1.72),
            fill=LIGHT, line=GRAY_LINE)
    d._text(slide, Inches(0.95), Inches(5.35), Inches(11.4), Inches(0.3),
            "Ejemplo del curso: husillo de 20 mm de paso, acoplamiento directo, "
            "programar en micras", size=Pt(12.5), color=NAVY, bold=True)
    d._text(slide, Inches(0.95), Inches(5.72), Inches(11.4), Inches(1.05),
            "Una vuelta de motor = 20 mm = **20.000 unidades de referencia** de "
            "1 µm.\n"
            "B / A = 16.777.216 / 20.000  →  se simplifica antes de escribirlo en "
            "los parámetros.\n"
            "**Comprobación obligatoria**: ordena un desplazamiento de 100 mm y "
            "mídelo con un comparador. Si no coincide, el engranaje está mal "
            "calculado.",
            size=Pt(11.5), color=INK, spacing=1.15)
