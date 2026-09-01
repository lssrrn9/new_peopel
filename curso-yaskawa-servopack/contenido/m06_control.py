"""Módulo 6 — Interfaz de control: CN1, analógico, tren de pulsos y bus."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, GRAY, GRAY_LINE, GREEN, INK, LIGHT,
                     LIGHT_BLUE, NAVY, NAVY_SOFT, RED, WHITE, Card, Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 06",
        "Interfaz de control: CN1, analógico, pulsos y bus",
        [
            "Para qué sirve cada conector del amplificador",
            "Entradas y salidas digitales de `CN1`: asignación y remapeo",
            "Consigna analógica de velocidad y de par",
            "Consigna por tren de pulsos y salida de encoder",
            "Finales de carrera y métodos de parada",
            "Buses de movimiento: MECHATROLINK-III y EtherCAT (CiA 402)",
        ],
        duration="4 h",
        notes=(
            "Este módulo conecta el drive con el mundo exterior. El objetivo es que "
            "el alumno sea capaz de leer el esquema de un armario ajeno y entender "
            "qué señal hace qué, y de diseñar el suyo propio.\n\n"
            "Recuerde a lo largo del módulo que los números de pin concretos dependen "
            "de la variante de interfaz del amplificador: hay que verificarlos en el "
            "manual del modelo instalado."
        ),
    )

    d.table_slide(
        "Los conectores del SERVOPACK y para qué sirve cada uno",
        ["Conector", "Función", "Qué se conecta", "Cuándo lo usarás"],
        [
            ["`CN1`", "Entradas y salidas de control",
             "Servo ON, finales de carrera, reset de alarma, salidas de estado, "
             "consigna analógica y tren de pulsos",
             "Siempre en variantes analógicas/pulsos; parcialmente en variantes de bus"],
            ["`CN2`", "Realimentación del encoder", "Cable de encoder del motor",
             "Siempre"],
            ["`CN3`", "Operador digital", "Consola JUSP-OP05A", "Opcional"],
            ["`CN5`", "Monitor analógico",
             "Osciloscopio para ver velocidad, par o error en tiempo real",
             "Muy útil en sintonización avanzada"],
            ["`CN6` / `CN6A-B`", "Comunicación de bus (en variantes de bus)",
             "MECHATROLINK-III o EtherCAT (entrada y salida)",
             "En arquitecturas con bus de movimiento"],
            ["`CN7`", "USB", "PC con SigmaWin+",
             "En puesta en marcha, ajuste y diagnóstico"],
            ["`CN8`", "Seguridad funcional (HWBB)",
             "Relé o módulo de seguridad; sale con puente de fábrica",
             "Siempre que la máquina requiera STO"],
        ],
        [1.4, 2.6, 4.0, 4.0],
        subtitle="Mapa mental del frontal del amplificador",
        size=9.5,
        foot="La disponibilidad y el número exacto de conectores varía según la "
             "variante de interfaz: comprueba el frontal de tu equipo.",
        notes=(
            "Insista en CN7 y CN8. CN7 porque es la puerta de entrada al equipo para "
            "cualquier trabajo serio, y CN8 porque su puente de fábrica es la causa "
            "más frecuente de 'no da par y no da alarma'.\n\n"
            "CN5 (monitor analógico) es una joya poco conocida: permite sacar "
            "velocidad y par a un osciloscopio con una escala configurable por "
            "parámetro. En sintonización de ejes difíciles, ver la señal real en un "
            "osciloscopio de verdad sigue siendo insustituible."
        ),
    )

    _diagrama_cn1(d)

    d.table_slide(
        "Entradas digitales: asignación de fábrica y remapeo",
        ["Señal", "Qué hace", "Notas de uso"],
        [
            ["`/S-ON`", "Servo ON: habilita el par en el motor",
             "Sin esta señal el eje está libre. Es la señal maestra"],
            ["`P-OT` / `N-OT`",
             "Finales de carrera de sobrerrecorrido en sentido positivo y negativo",
             "**Activas a nivel bajo**: si no se cablean, el drive las considera en "
             "alarma. Se pueden deshabilitar por parámetro (bajo tu responsabilidad)"],
            ["`/ALM-RST`", "Reinicio de alarma",
             "Sólo funciona si la causa ha desaparecido; algunas alarmas exigen "
             "ciclo de alimentación"],
            ["`/P-CL` / `/N-CL`", "Limitación externa de par en cada sentido",
             "Muy útil en apriete controlado y en topes mecánicos"],
            ["`/P-CON`", "Conmutación de función (P/PI, modo de control, sentido…)",
             "Su efecto depende de `Pn000` y del modo configurado"],
            ["`/SPD-A` `/SPD-B` `/SPD-D`", "Selección de velocidades internas",
             "Permite trabajar sin consigna analógica"],
            ["`/C-SEL`", "Conmutación de modo de control",
             "En modos combinados (velocidad↔par, por ejemplo)"],
            ["`/ZCLAMP`", "Fijación a velocidad cero",
             "Evita deriva con consigna analógica próxima a 0 V"],
            ["`/INHIBIT`", "Inhibición del tren de pulsos",
             "Congela la consigna de posición sin desactivar el servo"],
        ],
        [2.1, 4.1, 5.8],
        subtitle="Se reasignan con `Pn50A` y `Pn50B` (selección de señales de entrada)",
        size=9.5,
        foot="Los parámetros de asignación usan dígitos hexadecimales por señal: cada "
             "dígito indica a qué terminal físico se asocia, o si la señal se fuerza a "
             "activa o inactiva permanentemente.",
        notes=(
            "Explique el concepto de asignación: en la Σ-7 las señales lógicas no "
            "están atadas a un pin. Con Pn50A/Pn50B se decide qué terminal físico "
            "(SI0…SI6) activa cada señal lógica, e incluso se puede fijar una señal "
            "como 'siempre activa' sin cablearla.\n\n"
            "Eso último es muy práctico en un banco de pruebas (por ejemplo, forzar "
            "P-OT y N-OT a inactivo para no tener que cablear finales de carrera), "
            "pero es PELIGROSO dejarlo así en una máquina de producción. Debe quedar "
            "documentado y revisado.\n\n"
            "Detalle que confunde a todo el mundo la primera vez: P-OT y N-OT son "
            "señales de seguridad con lógica negativa. El contacto debe estar CERRADO "
            "en funcionamiento normal, de modo que un cable roto detenga el eje. Es "
            "la filosofía correcta, pero sorprende a quien viene de otras marcas."
        ),
    )

    d.two_col_slide(
        "Salidas digitales y señales de estado",
        (
            "Las salidas más utilizadas",
            [
                "`ALM` — **Alarma**. Contacto que se abre ante cualquier fallo grave. "
                "Se cablea en serie con la bobina del contactor de línea y se lleva "
                "al PLC.",
                "`/S-RDY` — **Servo listo**: el drive tiene potencia y está preparado "
                "para recibir servo ON.",
                "`/COIN` — **Posicionado completado**: la posición real está dentro de "
                "la ventana `Pn522`. Es la señal que espera el PLC para continuar el "
                "ciclo.",
                "`/V-CMP` — Velocidad alcanzada (en modo velocidad).",
                "`/TGON` — El motor está girando por encima del umbral `Pn502`.",
                "`/BK` — **Mando del freno** de retención.",
                "`/WARN` — Aviso previo a la alarma (sobrecarga, batería…).",
                "`/NEAR` — Proximidad al destino: permite al PLC anticipar la "
                "siguiente acción.",
            ],
        ),
        (
            "Cómo se configuran y se usan",
            [
                "Se asignan a los terminales físicos con `Pn50E`, `Pn50F` y `Pn510`.",
                "Hay **menos salidas físicas que señales disponibles**: hay que elegir "
                "las tres o cuatro que realmente aporta valor cablear.",
                "#Selección típica en máquina automática",
                "- `ALM` al circuito de seguridad y al PLC.",
                "- `/COIN` al PLC para encadenar el ciclo.",
                "- `/BK` al relé del freno (si el eje lo lleva).",
                "- `/S-RDY` al PLC para la lógica de arranque.",
                "#Cuidado con la ventana de posicionado",
                "`Pn522` demasiado grande da un `/COIN` prematuro (la máquina avanza "
                "antes de tiempo); demasiado pequeña, y `/COIN` no llega nunca y el "
                "ciclo se cuelga.",
            ],
        ),
        subtitle="Lo que el drive le cuenta al PLC",
        tones=("blue", "cyan"),
        notes=(
            "El ajuste de Pn522 merece una explicación con dibujo: es una ventana "
            "alrededor del destino. Se fija en unidades de referencia, es decir, "
            "después del engranaje electrónico.\n\n"
            "Método práctico para ajustarla: haz un posicionado, mira el error final "
            "estabilizado en Un008 y pon Pn522 en un valor unas 3-5 veces mayor que "
            "ese error residual, siempre dentro de la tolerancia mecánica de la "
            "aplicación.\n\n"
            "Un fallo clásico: /COIN se activa antes de que el eje esté realmente "
            "quieto porque la ventana es enorme. La máquina empieza la siguiente "
            "operación y aparecen defectos de calidad intermitentes."
        ),
    )

    d.two_col_slide(
        "Consigna analógica: velocidad y par",
        (
            "Cómo funciona",
            [
                "Dos entradas diferenciales de tensión: `V-REF` (velocidad) y `T-REF` "
                "(par), con rango típico **±10 V**.",
                "El signo de la tensión define el sentido de giro.",
                "**Escalado de velocidad**: `Pn300` fija a cuántas rpm equivale la "
                "tensión nominal de consigna.",
                "**Escalado de par**: `Pn400` fija a qué porcentaje de par equivale la "
                "tensión nominal.",
                "**Ajuste de offset**: siempre hay unos milivoltios de deriva. Se "
                "corrigen con la función de ajuste automático de offset o "
                "manualmente por parámetro.",
            ],
        ),
        (
            "Ventajas, inconvenientes y trucos",
            [
                "#A favor",
                "- Respuesta inmediata, sin latencia de red. Es la razón de que "
                "sobreviva en máquina-herramienta.",
                "- Compatible con cualquier CNC o controlador antiguo.",
                "#En contra",
                "- Sensible al ruido: cable apantallado obligatorio y masa de señal "
                "bien referenciada.",
                "- La deriva térmica del convertidor del controlador se traduce en "
                "movimiento lento del eje con consigna cero.",
                "#Truco imprescindible",
                "- Usa `/ZCLAMP` o una banda muerta para que el eje no derive con "
                "consigna próxima a cero.",
                "- Verifica el offset **en frío y en caliente**: cambia.",
            ],
        ),
        subtitle="El método clásico, todavía muy vivo en máquina-herramienta",
        tones=("amber", "blue"),
        callout=(
            "blue",
            "En modo analógico de velocidad, el lazo de posición lo cierra el CNC",
            "El drive sólo regula velocidad. La precisión de posicionado depende "
            "entonces del CNC y de la calidad de la señal analógica, no del "
            "SERVOPACK.",
        ),
        notes=(
            "Explique la arquitectura clásica de máquina-herramienta: el CNC lee la "
            "posición (por el encoder del drive o por una regla), cierra el lazo de "
            "posición y envía una consigna de velocidad analógica al drive. El drive "
            "es un 'regulador de velocidad de alta calidad'.\n\n"
            "El ajuste del offset es un procedimiento clásico de puesta en marcha: "
            "con consigna a cero, el eje debe quedar completamente parado. La Σ-7 "
            "tiene funciones de utilidad específicas para el ajuste automático y "
            "manual del offset de las entradas analógicas."
        ),
    )

    _diagrama_pulsos(d)

    d.bullets_slide(
        "Sobrerrecorrido, límites y métodos de parada",
        [
            "#Las tres capas de protección de recorrido",
            "**Límite software del controlador**: la primera barrera; el PLC o el CNC "
            "no genera consignas fuera del rango útil.",
            "**Finales de carrera `P-OT` / `N-OT`** cableados al drive: detienen el eje "
            "aunque el controlador falle.",
            "**Topes mecánicos y finales de seguridad** independientes: la última "
            "barrera, dimensionada para absorber el impacto.",
            "",
            "#Qué hace el drive al detectar sobrerrecorrido",
            "Detiene el movimiento en el sentido de la infracción, pero **permite "
            "salir** en sentido contrario: así puedes retirar el eje.",
            "El método de parada se configura en `Pn001`: parada por freno dinámico, "
            "parada por rampa de par o desactivación libre.",
            "- Tras la parada, el eje puede quedar **enclavado** (manteniendo "
            "posición) o **libre**, según la configuración.",
            "",
            "#Métodos de parada disponibles y cuándo usarlos",
            "**Freno dinámico** — parada rápida cortocircuitando las fases. Adecuado "
            "para emergencia; genera esfuerzo mecánico.",
            "**Parada por par máximo (rampa)** — el motor frena de forma controlada. "
            "Es la más suave para la mecánica.",
            "**Marcha libre (coast)** — el eje se detiene por rozamiento. Inaceptable "
            "en ejes verticales o de gran inercia.",
        ],
        subtitle="`Pn001` decide qué pasa cuando algo va mal",
        callout=(
            "red",
            "Regla de seguridad",
            "Deshabilitar `P-OT`/`N-OT` por parámetro para 'facilitar las pruebas' y "
            "olvidarse de reactivarlos es una de las causas más habituales de "
            "colisiones caras. Documenta cualquier deshabilitación temporal.",
        ),
        notes=(
            "Comente la diferencia entre parada de sobrerrecorrido y parada de "
            "emergencia: la primera es una función del drive, la segunda es una "
            "función de seguridad de la máquina que debe resolverse con la cadena de "
            "seguridad (Módulo 10).\n\n"
            "Detalle importante en ejes verticales: si al detectar sobrerrecorrido el "
            "eje queda libre, la carga cae. Hay que configurar la parada con "
            "enclavamiento y coordinar con el freno de retención.\n\n"
            "Consejo de puesta en marcha: pruebe físicamente los finales de carrera "
            "moviendo el eje a baja velocidad y accionándolos a mano antes de "
            "trabajar a velocidad nominal."
        ),
    )

    d.table_slide(
        "Buses de movimiento: MECHATROLINK-III y EtherCAT",
        ["Aspecto", "MECHATROLINK-III", "EtherCAT (CoE, perfil CiA 402)"],
        [
            ["Origen", "Bus propietario YASKAWA para movimiento",
             "Estándar abierto muy extendido en la industria"],
            ["Topología", "Línea, con repetidores/switch dedicado",
             "Línea o anillo sobre Ethernet industrial"],
            ["Controlador típico", "MP2000 / MP3000 de YASKAWA",
             "Cualquier maestro EtherCAT (Beckhoff, Omron, Codesys, Yaskawa…)"],
            ["Modos de operación", "Posición, velocidad, par, interpolación, "
             "búsqueda de origen",
             "Modos CiA 402: `csp` (posición cíclica), `csv` (velocidad cíclica), "
             "`cst` (par cíclico), `pp`, `hm`"],
            ["Ventajas", "Integración total con el ecosistema YASKAWA; sincronismo "
             "excelente",
             "Interoperabilidad, coste de infraestructura bajo, diagnóstico remoto"],
            ["Cableado", "Cable específico del bus",
             "Cable Ethernet industrial apantallado"],
            ["Puesta en marcha", "Direccionamiento por interruptores/parámetro y "
             "configuración en el controlador",
             "Fichero ESI, mapeo PDO y configuración del maestro"],
            ["Diagnóstico", "Alarmas de comunicación específicas del bus",
             "Contadores de error por puerto, muy útiles para localizar el cable malo"],
        ],
        [2.0, 4.5, 5.5],
        subtitle="En instalación nueva, el bus es casi siempre la mejor opción",
        size=9.5,
        foot="Con bus desaparece casi todo el cableado de CN1: servo ON, consigna y "
             "estado viajan por telegrama. Los finales de carrera y la seguridad "
             "siguen siendo cableado físico.",
        notes=(
            "Aclare un malentendido habitual: aunque se use bus, la seguridad "
            "(CN8/HWBB) y normalmente los finales de carrera siguen siendo cableado "
            "físico. El bus transporta el mando, no la seguridad, salvo que se use "
            "una capa de seguridad certificada (FSoE).\n\n"
            "Sobre los modos CiA 402: el que se usa en el 90 % de las máquinas es csp "
            "(cyclic synchronous position), en el que el maestro envía una posición "
            "objetivo cada ciclo de bus (típicamente 1-2 ms) y el drive interpola "
            "entre puntos. Toda la trayectoria la calcula el maestro.\n\n"
            "Ventaja de mantenimiento poco valorada: con bus, los parámetros y el "
            "estado del drive son accesibles desde el PLC, lo que permite diagnóstico "
            "remoto y sustitución de equipo con recarga automática de parámetros."
        ),
    )

    d.cards_slide(
        "Cómo elegir la arquitectura de control",
        [
            Card(
                "Elige ANALÓGICA / PULSOS si…",
                "· Sustituyes un drive antiguo y el controlador se queda.\n"
                "· El controlador sólo tiene salida de pulsos o ±10 V.\n"
                "· Hay uno o dos ejes y no se necesita diagnóstico remoto.\n"
                "· Se prioriza la latencia mínima sobre todo lo demás.",
                "amber",
            ),
            Card(
                "Elige BUS (EtherCAT / MECHATROLINK) si…",
                "· Instalación nueva con más de dos ejes.\n"
                "· Se necesita sincronismo entre ejes (levas, gantry, corte al "
                "vuelo).\n"
                "· Quieres diagnóstico y parametrización remotos.\n"
                "· Quieres reducir cableado y errores de montaje.",
                "blue",
            ),
            Card(
                "Elige POSICIONAMIENTO INTERNO si…",
                "· El movimiento se reduce a unas pocas posiciones fijas.\n"
                "· No hay PLC de movimiento y se quiere simplificar.\n"
                "· El ciclo se dispara con entradas digitales sencillas.\n"
                "· Se acepta menos flexibilidad a cambio de menos coste.",
                "green",
            ),
        ],
        subtitle="Tres arquitecturas, tres contextos distintos",
        intro="La decisión se toma al comprar el amplificador: forma parte del código "
              "de modelo y no se puede cambiar después.",
        notes=(
            "Cierre el módulo con una recomendación clara: en proyecto nuevo, bus. "
            "En retrofit, analógica o pulsos, salvo que también se cambie el "
            "controlador.\n\n"
            "Un aviso de coste: el bus reduce mucho el cableado y el tiempo de "
            "montaje, pero exige competencias de red industrial en el equipo de "
            "mantenimiento. Si la planta no las tiene, hay que formar antes de "
            "instalar; si no, el primer fallo de comunicación será un día de parada."
        ),
    )


# --------------------------------------------------------------------------
# Diagramas
# --------------------------------------------------------------------------

def _diagrama_cn1(d: Deck) -> None:
    slide = d.canvas_slide(
        "Cableado típico de `CN1`",
        "Entradas por optoacoplador, salidas por transistor, todo referido a 24 V",
        notes=(
            "Explique el concepto de alimentación de las entradas: el drive no "
            "alimenta sus propias entradas digitales. Hay que llevar los 24 V a un "
            "terminal común (+24VIN) y desde ahí los contactos externos cierran cada "
            "entrada. Es la causa número uno de 'las entradas no responden' en un "
            "primer montaje.\n\n"
            "Las entradas son por optoacoplador con común configurable, lo que "
            "permite trabajar en lógica positiva (source) o negativa (sink) según "
            "cómo se alimente el común. Hay que decidirlo al diseñar el armario y "
            "mantener el criterio en toda la máquina.\n\n"
            "Las salidas son transistores de colector abierto con capacidad limitada "
            "(decenas de miliamperios): no atacan directamente contactores ni "
            "electroválvulas. Hay que usar relés intermedios y siempre con supresor "
            "en las cargas inductivas.\n\n"
            "Los números de pin dependen de la variante: verifíquelos en el manual "
            "del equipo instalado antes de cablear."
        ),
    )

    # Fuente 24 V
    d.box(slide, Inches(0.62), Inches(2.05), Inches(2.3), Inches(0.85),
          "FUENTE 24 V CC\nde las E/S", NAVY, size=11, radius=0.10)

    # Bloque CN1
    cx, cw = Inches(4.95), Inches(3.4)
    d._rect(slide, cx, Inches(1.80), cw, Inches(4.55), fill=LIGHT, line=NAVY,
            line_w=Pt(2))
    d._text(slide, cx, Inches(1.92), cw, Inches(0.3), "`CN1` del SERVOPACK",
            size=Pt(13), color=NAVY, bold=True, align=PP_ALIGN.CENTER)

    d.box(slide, cx + Inches(0.2), Inches(2.35), cw - Inches(0.4),
          Inches(0.42), "`+24VIN`  común de entradas", AMBER, size=10)

    entradas = ["`/S-ON`  servo ON", "`P-OT` / `N-OT`  finales de carrera",
                "`/ALM-RST`  reset de alarma",
                "`/P-CL` / `/N-CL`  límite de par"]
    y = Inches(2.88)
    for texto in entradas:
        d.box(slide, cx + Inches(0.2), y, cw - Inches(0.4), Inches(0.34),
              texto, BLUE, size=9.5)
        y += Inches(0.40)

    y += Inches(0.10)
    salidas = ["`ALM`  alarma", "`/S-RDY`  servo listo",
               "`/COIN`  en posición", "`/BK`  mando de freno"]
    for texto in salidas:
        d.box(slide, cx + Inches(0.2), y, cw - Inches(0.4), Inches(0.34),
              texto, GREEN, size=9.5)
        y += Inches(0.40)

    # Contactos externos
    d._rect(slide, Inches(0.62), Inches(3.20), Inches(3.75), Inches(3.15),
            fill=LIGHT, line=GRAY_LINE)
    d._text(slide, Inches(0.85), Inches(3.35), Inches(3.3), Inches(0.3),
            "Contactos y mandos externos", size=Pt(11.5), color=NAVY,
            bold=True)
    tf = slide.shapes.add_textbox(Inches(0.85), Inches(3.72), Inches(3.3),
                                  Inches(2.5)).text_frame
    tf.word_wrap = True
    d._fill_bullets(tf, [
        "Salida digital del PLC o contacto de relé para `/S-ON`.",
        "Finales de carrera **con contacto normalmente cerrado**.",
        "Pulsador o salida del PLC para el reset de alarma.",
        "Todo con cable **apantallado** y separado de la potencia.",
    ], size=10.5)

    d.arrow(slide, Inches(4.45), Inches(2.48), Inches(0.42), Inches(0.16),
            color=AMBER)
    d.arrow(slide, Inches(4.45), Inches(4.20), Inches(0.42), Inches(0.16),
            color=BLUE)

    # Destino de salidas
    d._rect(slide, Inches(8.85), Inches(3.20), Inches(3.85), Inches(3.15),
            fill=LIGHT_BLUE, line=BLUE, line_w=Pt(0.75))
    d._text(slide, Inches(9.10), Inches(3.35), Inches(3.35), Inches(0.3),
            "Reglas de las salidas", size=Pt(11.5), color=NAVY, bold=True)
    tf = slide.shapes.add_textbox(Inches(9.10), Inches(3.72), Inches(3.35),
                                  Inches(2.5)).text_frame
    tf.word_wrap = True
    d._fill_bullets(tf, [
        "Son transistores de **baja capacidad**: usa siempre relé intermedio para "
        "cargas reales.",
        "Supresor (diodo o varistor) en toda bobina.",
        "`ALM` en serie con la bobina del contactor de línea.",
        "Respeta la polaridad: son salidas de colector abierto, no contactos "
        "libres de potencial.",
    ], size=10.5)
    d.arrow(slide, Inches(8.42), Inches(5.05), Inches(0.36), Inches(0.16),
            color=GREEN)

    d.callout(slide, Inches(0.62), Inches(6.52), Inches(12.1), Inches(0.42),
              "red", "Sin `+24VIN` alimentado, ninguna entrada digital funciona "
              "— y el drive no da ninguna alarma por ello.", "")


def _diagrama_pulsos(d: Deck) -> None:
    slide = d.canvas_slide(
        "Consigna por tren de pulsos y salida de encoder",
        "El método más extendido en máquina automática sin bus",
        notes=(
            "Los tres formatos de tren de pulsos se seleccionan con Pn200.0. Hay que "
            "configurar EXACTAMENTE el que emite el controlador; si no, el eje se "
            "mueve al revés, a media velocidad o no se mueve.\n\n"
            "Diferencia crítica entre line driver y colector abierto: el line driver "
            "(RS-422) es diferencial, admite frecuencias altas y cables largos con "
            "buena inmunidad. El colector abierto es más sencillo pero limita mucho "
            "la frecuencia y la longitud. En un eje de 3 kW con dinámica exigente, "
            "usa siempre line driver.\n\n"
            "La salida de encoder (PAO/PBO/PCO) reproduce la posición hacia el "
            "controlador con la resolución que fije Pn212. Sirve para que el CNC "
            "cierre su propio lazo o para sincronizar otro eje como esclavo. PCO es "
            "el pulso de marca por vuelta, usado en la búsqueda de origen.\n\n"
            "Ojo con Pn212: pedir una resolución de salida demasiado alta a "
            "velocidad elevada supera la frecuencia máxima de salida y dispara la "
            "alarma correspondiente."
        ),
    )

    # Entrada de pulsos
    d._rect(slide, Inches(0.62), Inches(1.78), Inches(6.0), Inches(2.55),
            fill=LIGHT, line=GRAY_LINE)
    d._text(slide, Inches(0.88), Inches(1.94), Inches(5.5), Inches(0.3),
            "Entrada: `PULS` / `SIGN`  (`Pn200.0` selecciona el formato)",
            size=Pt(12.5), color=NAVY, bold=True)

    formatos = [
        ("Pulso + sentido", "Un tren de pulsos marca el movimiento y una señal "
         "estática el sentido. El más habitual."),
        ("CW / CCW", "Dos trenes independientes, uno por sentido de giro."),
        ("Cuadratura A/B (×1, ×2, ×4)", "Dos señales desfasadas 90°; permite "
         "multiplicar la resolución por 4."),
    ]
    y = Inches(2.38)
    for titulo, desc in formatos:
        d._rect(slide, Inches(0.88), y, Inches(5.5), Inches(0.58), fill=WHITE,
                line=GRAY_LINE)
        d._rect(slide, Inches(0.88), y, Inches(0.06), Inches(0.58), fill=BLUE)
        d._text(slide, Inches(1.08), y + Inches(0.06), Inches(5.1),
                Inches(0.24), titulo, size=Pt(10.5), color=BLUE, bold=True)
        d._text(slide, Inches(1.08), y + Inches(0.30), Inches(5.1),
                Inches(0.24), desc, size=Pt(9.5), color=GRAY)
        y += Inches(0.64)

    # Salida de encoder
    d._rect(slide, Inches(6.92), Inches(1.78), Inches(5.8), Inches(2.55),
            fill=LIGHT, line=GRAY_LINE)
    d._text(slide, Inches(7.18), Inches(1.94), Inches(5.3), Inches(0.3),
            "Salida: `PAO` / `PBO` / `PCO`  (`Pn212` fija la resolución)",
            size=Pt(12.5), color=NAVY, bold=True)
    tf = slide.shapes.add_textbox(Inches(7.18), Inches(2.38), Inches(5.3),
                                  Inches(1.9)).text_frame
    tf.word_wrap = True
    d._fill_bullets(tf, [
        "`PAO` y `PBO`: dos canales en cuadratura que reproducen el movimiento.",
        "`PCO`: pulso de marca, **uno por vuelta**, para la búsqueda de origen.",
        "`Pn212` define cuántos pulsos por vuelta se emiten (valor típico de "
        "fábrica: 2.048).",
        "Comprueba que la frecuencia resultante a velocidad máxima no supera el "
        "límite del amplificador ni el del controlador.",
    ], size=10.5)

    # Comparativa eléctrica
    d._rect(slide, Inches(0.62), Inches(4.55), Inches(12.1), Inches(1.55),
            fill=LIGHT_BLUE, line=BLUE, line_w=Pt(0.75))
    d._text(slide, Inches(0.9), Inches(4.70), Inches(11.5), Inches(0.3),
            "Line driver frente a colector abierto: no es un detalle menor",
            size=Pt(12.5), color=NAVY, bold=True)
    d._text(slide, Inches(0.9), Inches(5.05), Inches(5.6), Inches(1.0),
            "**Line driver (RS-422, diferencial)**\nFrecuencias altas, cables "
            "largos, gran inmunidad al ruido. Es la opción recomendada en "
            "cualquier eje exigente.", size=Pt(11), color=INK, spacing=1.1)
    d._text(slide, Inches(6.95), Inches(5.05), Inches(5.5), Inches(1.0),
            "**Colector abierto**\nMás sencillo y barato, pero limita la "
            "frecuencia y la longitud del cable. Suele ser el origen de pérdidas "
            "de pulsos y de posiciones que 'se van'.", size=Pt(11), color=INK,
            spacing=1.1)

    d.callout(slide, Inches(0.62), Inches(6.16), Inches(12.1), Inches(0.76),
              "amber", "Síntoma clásico de formato mal configurado",
              "El eje se mueve la mitad o el cuádruple de lo pedido, o siempre en el "
              "mismo sentido. Revisa `Pn200.0` y el engranaje electrónico antes de "
              "buscar problemas mecánicos.")
