"""Módulo 1 — Fundamentos del servoaccionamiento."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, GRAY, GRAY_LINE, GREEN, INK, LIGHT,
                     LIGHT_BLUE, NAVY, RED, WHITE, Card, Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 01",
        "Fundamentos del servoaccionamiento",
        [
            "Qué es un servo y por qué existe",
            "Los cuatro elementos del sistema y cómo se hablan entre sí",
            "El lazo cerrado en cascada: posición, velocidad y par",
            "Encoder, resolución y realimentación",
            "Las magnitudes que gobiernan todo: par, inercia y aceleración",
            "Cómo se lee una curva par-velocidad",
        ],
        duration="3 h",
        notes=(
            "Este módulo es la base conceptual. Aunque el grupo tenga experiencia, "
            "no lo salte: la mayoría de los errores de sintonización nacen de no "
            "tener claro el modelo mental del lazo en cascada y de la relación de "
            "inercias."
        ),
    )

    d.bullets_slide(
        "¿Qué es un servoaccionamiento?",
        [
            "#Definición práctica",
            "Un servoaccionamiento es un sistema que obliga a un eje mecánico a "
            "**seguir una consigna** de posición, velocidad o par **con error "
            "controlado**, corrigiendo continuamente a partir de la medida real.",
            "",
            "#Las tres ideas que lo definen",
            "**Realimentación**: el encoder mide lo que realmente ocurre en el eje; el "
            "drive compara medida y consigna miles de veces por segundo.",
            "**Corrección**: la diferencia (error) se transforma en corriente para el "
            "motor. Sin error no hay corrección; con error grande, corrección grande.",
            "**Dinámica**: no basta con llegar; hay que llegar **rápido**, **sin "
            "sobrepasar** y **sin vibrar**. Ahí está la dificultad y el valor técnico.",
            "",
            "#Qué aporta frente a un accionamiento convencional",
            "- Precisión de posicionado del orden de la **cuenta de encoder** "
            "(millonésimas de vuelta con encoder de 24 bits).",
            "- Par disponible desde **velocidad cero** y control del par en todo momento.",
            "- Aceleraciones y ciclos por minuto muy superiores: el motor está "
            "diseñado con baja inercia y alta densidad de par.",
        ],
        subtitle="La diferencia entre mover un eje y controlarlo",
        notes=(
            "Analogía útil: conducir un coche con los ojos cerrados (lazo abierto) "
            "frente a conducir mirando la carretera y corrigiendo el volante (lazo "
            "cerrado). El motor paso a paso es el primero; el servo, el segundo.\n\n"
            "Pregunta para el grupo: ¿por qué un servo puede dar par a velocidad cero "
            "y un motor asíncrono con variador tiene problemas para hacerlo? Respuesta: "
            "porque el servo conoce la posición exacta del rotor gracias al encoder y "
            "puede orientar el campo con precisión (control vectorial con realimentación "
            "de posición absoluta del rotor), mientras que en lazo abierto se estima."
        ),
    )

    _diagrama_cadena(d)

    d.table_slide(
        "Servo frente a variador de frecuencia y motor paso a paso",
        ["Criterio", "Servo (SERVOPACK + PMSM)", "Variador + motor asíncrono",
         "Motor paso a paso"],
        [
            ["Lazo", "Cerrado con encoder", "Normalmente abierto (V/f) o sensorless",
             "Abierto (salvo versiones closed-loop)"],
            ["Precisión de posición", "Cuenta de encoder (24 bits = 16,7 M/vuelta)",
             "Baja, no es su función", "Paso del motor; pierde pasos si sobrecarga"],
            ["Par a velocidad cero", "100 % del par nominal de forma continua",
             "Limitado, requiere ventilación forzada", "Par de mantenimiento con "
             "calentamiento"],
            ["Par pico", "≈ 300 % del nominal durante segundos", "≈ 150 %",
             "No hay reserva de par"],
            ["Dinámica", "Muy alta: milisegundos", "Media", "Baja a alta velocidad"],
            ["Comportamiento en sobrecarga", "Aumenta corriente y avisa/alarma",
             "Aumenta deslizamiento", "**Pierde pasos en silencio**"],
            ["Coste relativo", "Alto", "Bajo", "Muy bajo"],
            ["Aplicación típica", "Posicionado, sincronismo, corte, robótica",
             "Bombas, ventiladores, cintas", "Ejes auxiliares de bajo par"],
        ],
        [1.5, 3.4, 3.0, 3.0],
        subtitle="Cuándo se justifica el sobrecoste de un servo",
        size=10.0,
        foot="Regla práctica: si el eje debe posicionar con exactitud, sincronizarse "
             "con otro eje o repetir ciclos rápidos, es un servo. Si solo debe girar, "
             "es un variador.",
        notes=(
            "El punto que más conviene remarcar es el de 'pierde pasos en silencio': "
            "es la razón principal por la que se sustituyen steppers por servos en "
            "máquinas de producción. El servo nunca pierde la referencia sin avisar; "
            "si no puede seguir la consigna, dispara A.d00 (exceso de error de "
            "posición) o A.710/A.720 (sobrecarga).\n\n"
            "Matiz honesto: los variadores modernos con control vectorial en lazo "
            "cerrado y encoder se acercan mucho al servo en par a velocidad cero. La "
            "diferencia real queda en la dinámica (inercia del rotor mucho menor en el "
            "servomotor) y en la resolución de la realimentación."
        ),
    )

    _diagrama_lazos(d)

    d.cards_slide(
        "Los tres modos de control",
        [
            Card(
                "Control de PAR",
                "El drive regula la **corriente** y por tanto el par en el eje.\n"
                "· Consigna: analógica `T-REF` o por bus.\n"
                "· Se usa en bobinadoras, control de tensión de banda, apriete "
                "controlado y ejes esclavos en gantry.\n"
                "· Riesgo: sin carga, el motor se embala → hay que limitar velocidad.",
                "amber",
            ),
            Card(
                "Control de VELOCIDAD",
                "El drive regula las **rpm** del eje.\n"
                "· Consigna: analógica `V-REF` (±10 V), velocidades internas o bus.\n"
                "· Se usa cuando el lazo de posición lo cierra el CNC o el PLC.\n"
                "· Es el modo clásico de máquina-herramienta con CNC.",
                "cyan",
            ),
            Card(
                "Control de POSICIÓN",
                "El drive regula la **posición** del eje.\n"
                "· Consigna: tren de pulsos (`PULS`/`SIGN`) o telegrama de bus.\n"
                "· Es el modo más habitual en máquina automática.\n"
                "· Incluye el engranaje electrónico y la ventana de posicionado "
                "`Pn522`.",
                "blue",
            ),
        ],
        subtitle="Se seleccionan con `Pn000.1` (selección del método de control)",
        intro="Los tres modos son en realidad el mismo lazo en cascada; sólo cambia "
              "por dónde entra la consigna.",
        notes=(
            "Idea clave que hay que dejar clarísima: el modo de par es el lazo "
            "interno, el de velocidad añade el lazo intermedio y el de posición añade "
            "el externo. Elegir 'modo velocidad' no desactiva el lazo de par; "
            "simplemente el drive genera internamente la consigna de par.\n\n"
            "Pn000.1 admite además modos combinados con conmutación por entrada "
            "digital (por ejemplo velocidad↔par con /P-CON), útiles en aplicaciones "
            "de tensión de material donde se arranca en velocidad y se pasa a par.\n\n"
            "En modelos de bus (MECHATROLINK-III / EtherCAT) el modo se selecciona "
            "por telegrama con los modos de operación del perfil CiA 402: par, "
            "velocidad, posición cíclica, homing e interpolación."
        ),
    )

    d.two_col_slide(
        "La realimentación: el encoder",
        (
            "Tipos y qué implica cada uno",
            [
                "#Incremental",
                "Cuenta pulsos desde el arranque. Al quitar tensión **pierde la "
                "referencia** y obliga a hacer búsqueda de origen (homing).",
                "#Absoluto (el de la serie Σ-7)",
                "Conoce la posición dentro de la vuelta **y** el número de vueltas "
                "(multivuelta) aunque se corte la alimentación.",
                "- Requiere **batería** (3,6 V) para mantener el contaje multivuelta.",
                "- Elimina el homing: la máquina arranca sabiendo dónde está.",
                "- Se configura con `Fn008` (setup del encoder absoluto) y `Pn205` "
                "(límite multivuelta).",
            ],
        ),
        (
            "Resolución: qué significan 24 bits",
            [
                "El encoder serie de la Σ-7 entrega **2²⁴ = 16.777.216 cuentas por "
                "vuelta**.",
                "- Una cuenta equivale a **0,0000215°**, unas 77 millonésimas de grado.",
                "- Con un husillo de 10 mm de paso, una cuenta son **0,6 nanómetros** "
                "de desplazamiento teórico.",
                "#Consecuencia práctica",
                "La resolución **nunca** es el factor limitante: lo son la mecánica "
                "(holguras, rigidez, dilatación) y el ruido eléctrico.",
                "- El drive puede reescalar la resolución hacia el controlador con el "
                "**engranaje electrónico** (`Pn20E`/`Pn210`) y hacia la salida de "
                "pulsos con `Pn212`.",
            ],
        ),
        subtitle="Sin una buena medida no hay buen control",
        tones=("blue", "cyan"),
        callout=(
            "amber",
            "Error frecuente en campo",
            "Pedir al eje una precisión mayor que la que permite la mecánica y culpar "
            "al servo. Antes de tocar ganancias, comprueba holgura del acoplamiento, "
            "juego del husillo y rigidez del soporte.",
        ),
        notes=(
            "La batería del encoder absoluto es una fuente clásica de paradas: "
            "genera el aviso A.930 (batería baja) y, si se agota con el equipo sin "
            "tensión, la alarma A.810 (fallo de respaldo del encoder), que obliga a "
            "repetir Fn008 y a rehacer el origen de la máquina.\n\n"
            "Recomendación de mantenimiento: sustituir la batería con el equipo "
            "ENERGIZADO (control power ON). Así el encoder no pierde el contaje "
            "multivuelta y no hay que rehacer el origen. Anótelo, porque este truco "
            "ahorra horas de parada."
        ),
    )

    d.bullets_slide(
        "Las magnitudes que gobiernan el dimensionamiento",
        [
            "#Par (T, en N·m)",
            "Es lo que el motor 'empuja'. Se descompone en: par para **acelerar** la "
            "inercia + par para vencer **fricción** + par de **proceso** (corte, "
            "prensado) + par de **gravedad** en ejes verticales.",
            "- `T = J · α` → par de aceleración, con α en rad/s².",
            "#Inercia (J, en kg·m²)",
            "Es la resistencia del conjunto a cambiar de velocidad. Depende de la masa "
            "**y de cómo está distribuida** respecto al eje de giro.",
            "- Lo que importa es la **inercia reflejada al eje del motor**: una "
            "reducción de relación *i* divide la inercia de la carga por *i²*.",
            "#Velocidad angular (ω, en rad/s) y aceleración (α, en rad/s²)",
            "- `ω = 2π · n / 60` con *n* en rpm. A 3.000 rpm, ω ≈ 314 rad/s.",
            "- `α = Δω / Δt`. Acelerar de 0 a 3.000 rpm en 0,1 s exige α ≈ 3.140 rad/s².",
            "#Potencia (P, en W)",
            "- `P = T · ω`. Un motor de 3 kW a 3.000 rpm da un par nominal de "
            "`3000 / 314 ≈ 9,55 N·m`. **La potencia sola no dice nada: el par y la "
            "velocidad lo dicen todo.**",
        ],
        subtitle="Par, inercia, aceleración y potencia: el lenguaje del servo",
        callout=(
            "green",
            "Comprobación mental rápida",
            "Par nominal [N·m] ≈ 9,55 × Potencia [kW] / Velocidad [krpm]. "
            "Con 3 kW a 3.000 rpm → 9,55 N·m. Con 3 kW a 1.500 rpm → 19,1 N·m. "
            "Misma potencia, el doble de par.",
        ),
        notes=(
            "La fórmula del recuadro es la herramienta más rentable de todo el curso: "
            "permite verificar en dos segundos si una propuesta comercial tiene "
            "sentido.\n\n"
            "Ejercicio en pizarra: 'necesito 15 N·m continuos a 2.000 rpm, ¿me vale un "
            "motor de 3 kW?'. P = 15 × 2π × 2000/60 = 3.140 W. Está justo en el "
            "límite: habría que ir a la versión de 1.500 rpm (SGM7G-30A, 18,6 N·m) o "
            "subir de tamaño. Este razonamiento se desarrolla en el Módulo 04."
        ),
    )

    _diagrama_curva_par(d)

    d.table_slide(
        "Vocabulario esencial del servo",
        ["Término", "Significado", "Dónde aparece"],
        [
            ["SERVOPACK", "Nombre comercial YASKAWA del servoamplificador (el drive)",
             "Todo el curso"],
            ["Σ-7 / Sigma-7", "Generación de la familia de servos YASKAWA",
             "Códigos SGD7·/SGM7·"],
            ["PMSM", "Motor síncrono de imanes permanentes: el servomotor",
             "Módulo 03"],
            ["Ganancia", "Cuánto corrige el drive por cada unidad de error",
             "`Pn100`, `Pn102`"],
            ["Relación de inercias", "Inercia de la carga ÷ inercia del rotor",
             "`Pn103`, Módulo 04"],
            ["Error de seguimiento", "Retraso entre consigna y posición real durante el "
             "movimiento", "`Un008`, `Pn520`"],
            ["Ventana de posicionado", "Margen dentro del cual se considera 'en "
             "posición'", "`Pn522`, señal `/COIN`"],
            ["Regeneración", "Energía que devuelve el motor al frenar y que el drive "
             "debe disipar", "Módulos 04 y 05"],
            ["Baseblock", "Estado en que se bloquean los transistores de salida: el "
             "motor queda libre", "HWBB, Módulo 10"],
            ["Autotuning", "Ajuste automático de ganancias midiendo la respuesta real",
             "`Fn201`, Módulo 09"],
            ["Notch", "Filtro que elimina una frecuencia concreta de resonancia "
             "mecánica", "`Pn409`, Módulo 09"],
        ],
        [1.9, 6.0, 2.6],
        subtitle="Glosario de partida (se amplía en el Módulo 13)",
        size=10.5,
        notes=(
            "Recomiende a los alumnos fotografiar esta diapositiva: es la que más se "
            "consulta durante los primeros días de trabajo con el equipo.\n\n"
            "Cuidado con un falso amigo habitual: en castellano se dice 'ganancia "
            "alta = respuesta rápida', pero ganancia alta también significa 'menos "
            "margen de estabilidad'. Todo el Módulo 09 consiste en encontrar el punto "
            "de equilibrio."
        ),
    )


# --------------------------------------------------------------------------
# Diagramas
# --------------------------------------------------------------------------

def _diagrama_cadena(d: Deck) -> None:
    slide = d.canvas_slide(
        "Los cuatro elementos del sistema servo",
        "Cadena de mando y cadena de realimentación",
        notes=(
            "Recorra el diagrama dos veces: primero la cadena de mando de izquierda a "
            "derecha (quién manda a quién) y después la cadena de realimentación de "
            "derecha a izquierda (quién informa a quién).\n\n"
            "Insista en que el encoder informa al SERVOPACK, no al controlador. El "
            "controlador sólo recibe un 'acuse' (señal /COIN de posicionado "
            "completado, o la posición real por bus). Esto explica por qué el ajuste "
            "fino del eje se hace en el drive y no en el PLC.\n\n"
            "Pregunte: si el eje vibra, ¿dónde está el problema? Puede estar en "
            "cualquiera de los cuatro bloques y en los dos enlaces. El método de "
            "diagnóstico del Módulo 11 consiste precisamente en aislar bloque por "
            "bloque."
        ),
    )

    y = Inches(2.35)
    h = Inches(1.15)
    w = Inches(2.55)
    gap = Inches(0.55)
    x0 = Inches(0.75)

    bloques = [
        ("CONTROLADOR\nPLC · CNC · Motion", BLUE,
         "Genera la consigna:\nposición, velocidad o par"),
        ("SERVOPACK\nSGD7S-200A", NAVY,
         "Cierra los lazos y\nconvierte la red en corriente"),
        ("SERVOMOTOR\nSGM7A-30A · 3 kW", CYAN,
         "Convierte corriente\nen par y movimiento"),
        ("MECÁNICA\nReductor · husillo · carga", GRAY,
         "Transforma el giro\nen el movimiento útil"),
    ]

    centers = []
    for i, (texto, color, pie) in enumerate(bloques):
        x = x0 + i * (w + gap)
        d.box(slide, x, y, w, h, texto, color, size=12.5, radius=0.10)
        d.label(slide, x, y + h + Inches(0.12), w, pie, size=10, color=GRAY)
        centers.append(x + w / 2)
        if i < 3:
            d.arrow(slide, x + w + Inches(0.08), y + h / 2 - Inches(0.13),
                    gap - Inches(0.16), Inches(0.26), color=AMBER)

    d.label(slide, x0, y - Inches(0.42), w * 4 + gap * 3,
            "CADENA DE MANDO  →", size=11, color=AMBER, bold=True,
            align=PP_ALIGN.LEFT)

    # Realimentación del encoder
    y_fb = Inches(4.95)
    d.line(slide, centers[2], y + h + Inches(0.55), centers[2], y_fb, color=GREEN,
           width=Pt(1.75))
    d.line(slide, centers[2], y_fb, centers[1], y_fb, color=GREEN, width=Pt(1.75))
    d.arrow(slide, centers[1] - Inches(0.13), y_fb - Inches(0.62), Inches(0.26),
            Inches(0.62), color=GREEN, direction="up")
    d.box(slide, centers[2] - Inches(1.35), y_fb - Inches(0.22), Inches(2.7),
          Inches(0.44), "ENCODER ABSOLUTO 24 bits  (CN2)", GREEN, size=10.5)

    # Acuse hacia el controlador
    y_ack = Inches(5.75)
    d.line(slide, centers[1], y + h + Inches(0.55), centers[1], y_ack,
           color=GRAY, width=Pt(1.25), dash=True)
    d.line(slide, centers[1], y_ack, centers[0], y_ack, color=GRAY,
           width=Pt(1.25), dash=True)
    d.arrow(slide, centers[0] - Inches(0.11), y_ack - Inches(0.55), Inches(0.22),
            Inches(0.55), color=GRAY, direction="up")
    d.label(slide, centers[1] - Inches(2.0), y_ack + Inches(0.08), Inches(4.0),
            "Estado y acuse:  /COIN · /S-RDY · ALM · posición por bus",
            size=10, color=GRAY)

    d.callout(slide, Inches(0.75), Inches(6.12), Inches(11.83), Inches(0.80),
              "blue", "Qué hay que retener",
              "El controlador dice QUÉ hacer; el SERVOPACK decide CÓMO hacerlo. El "
              "ajuste dinámico del eje vive en el drive, no en el programa del PLC.")


def _diagrama_lazos(d: Deck) -> None:
    slide = d.canvas_slide(
        "El lazo cerrado en cascada",
        "Tres reguladores anidados: posición → velocidad → par",
        notes=(
            "Este es el diagrama más importante del curso. Todo el Módulo 09 "
            "(sintonización) consiste en ajustar las ganancias de estos tres lazos en "
            "el orden correcto: de dentro hacia fuera.\n\n"
            "Frecuencias de actualización típicas en la Σ-7: el lazo de corriente "
            "trabaja en el orden de decenas de kHz, el de velocidad en unos pocos kHz "
            "y el de posición algo más lento. Regla universal del control en cascada: "
            "el lazo interno debe ser al menos 4-5 veces más rápido que el externo.\n\n"
            "Consecuencia práctica que hay que anunciar ya: si el lazo de velocidad no "
            "está bien ajustado, subir la ganancia de posición Pn102 sólo produce "
            "inestabilidad. Nunca se empieza por fuera."
        ),
    )

    y = Inches(2.55)
    h = Inches(1.0)

    etapas = [
        ("Consigna", GRAY, ""),
        ("LAZO DE\nPOSICIÓN", BLUE, "`Pn102` Kp"),
        ("LAZO DE\nVELOCIDAD", CYAN, "`Pn100` · `Pn101`"),
        ("LAZO DE\nPAR / CORRIENTE", NAVY, "`Pn401` filtro"),
        ("PWM +\nIGBT", GRAY, ""),
        ("MOTOR", GREEN, ""),
    ]
    w = Inches(1.72)
    gap = Inches(0.30)
    x0 = Inches(0.62)
    xs = []
    for i, (texto, color, pie) in enumerate(etapas):
        x = x0 + i * (w + gap)
        xs.append(x)
        d.box(slide, x, y, w, h, texto, color, size=11.5, radius=0.10)
        if pie:
            d.label(slide, x, y + h + Inches(0.10), w, pie, size=10, color=BLUE,
                    bold=True, mono=True)
        if i < len(etapas) - 1:
            d.arrow(slide, x + w + Inches(0.04), y + h / 2 - Inches(0.10),
                    gap - Inches(0.08), Inches(0.20), color=AMBER)

    # Realimentaciones
    niveles = [
        (Inches(4.60), 4, 3, "Realimentación de corriente", NAVY),
        (Inches(5.25), 5, 2, "Realimentación de velocidad (derivada del encoder)", CYAN),
        (Inches(5.90), 5, 1, "Realimentación de posición (encoder)", BLUE),
    ]
    for y_fb, i_from, i_to, texto, color in niveles:
        x_from = xs[i_from] + w / 2
        x_to = xs[i_to] + w / 2
        d.line(slide, x_from, y + h, x_from, y_fb, color=color, width=Pt(1.5))
        d.line(slide, x_from, y_fb, x_to, y_fb, color=color, width=Pt(1.5))
        d.arrow(slide, x_to - Inches(0.10), y_fb - Inches(0.45), Inches(0.20),
                Inches(0.45), color=color, direction="up")
        d.label(slide, x_to + Inches(0.2), y_fb - Inches(0.24), Inches(6.0),
                texto, size=10, color=color, align=PP_ALIGN.LEFT)

    d.callout(slide, Inches(0.62), Inches(6.08), Inches(11.9), Inches(0.84),
              "amber", "Orden de ajuste (memorízalo)",
              "Siempre de dentro hacia fuera: 1) relación de inercias `Pn103` → "
              "2) lazo de velocidad `Pn100`/`Pn101` → 3) lazo de posición `Pn102` → "
              "4) filtros y prealimentación.")


def _diagrama_curva_par(d: Deck) -> None:
    slide = d.canvas_slide(
        "Cómo se lee una curva par-velocidad",
        "La hoja de datos del motor resumida en un gráfico",
        notes=(
            "Dibuje mentalmente el ciclo de la máquina sobre esta curva: la "
            "aceleración debe caer dentro de la zona intermitente y el par eficaz "
            "(RMS) de todo el ciclo, dentro de la zona continua.\n\n"
            "La caída de la curva a alta velocidad tiene una causa física: la fuerza "
            "contraelectromotriz crece con la velocidad y llega un punto en que la "
            "tensión del bus de continua ya no puede forzar más corriente. Por eso la "
            "curva depende de la tensión de red: con 200 V la curva es más baja que "
            "con 230 V. En instalaciones con red débil o larga, esto se nota.\n\n"
            "Advertencia práctica: trabajar de forma continuada en la zona "
            "intermitente provoca A.720 (sobrecarga continua). El drive lleva un "
            "modelo térmico I²t que integra el exceso de corriente."
        ),
    )

    ox, oy = Inches(1.75), Inches(6.10)
    ax_w, ax_h = Inches(6.2), Inches(3.55)

    d.line(slide, ox, oy, ox + ax_w, oy, color=INK, width=Pt(1.5))
    d.line(slide, ox, oy, ox, oy - ax_h - Inches(0.25), color=INK, width=Pt(1.5))
    d.label(slide, ox, oy + Inches(0.36), ax_w, "Velocidad  n  [rpm]  →",
            size=11, color=INK, bold=True)
    d.label(slide, ox - Inches(0.55), oy - ax_h - Inches(0.62), Inches(2.6),
            "Par  T  [N·m]  ↑", size=11, color=INK, bold=True,
            align=PP_ALIGN.LEFT)

    # Zona intermitente
    inter = d._rect(slide, ox, oy - ax_h, ax_w * 0.76, ax_h,
                    fill=None, line=RED, line_w=Pt(1.5))
    inter.fill.solid()
    inter.fill.fore_color.rgb = LIGHT_BLUE
    d._text(slide, ox + Inches(0.28), oy - ax_h + Inches(0.22), Inches(3.3),
            Inches(0.7),
            "ZONA INTERMITENTE\naceleraciones y frenados (unos segundos)",
            size=Pt(11), color=RED, bold=True, spacing=1.1)

    # Zona continua
    d._rect(slide, ox, oy - ax_h * 0.33, ax_w * 0.93, ax_h * 0.33,
            fill=GREEN, line=GREEN)
    d._text(slide, ox + Inches(0.28), oy - ax_h * 0.33 + Inches(0.22),
            Inches(4.2), Inches(0.5),
            "ZONA CONTINUA — servicio permanente (S1)", size=Pt(11),
            color=WHITE, bold=True)

    # Marcas del eje de par
    d.line(slide, ox, oy - ax_h * 0.33, ox - Inches(0.12), oy - ax_h * 0.33,
           color=INK)
    d.label(slide, ox - Inches(1.62), oy - ax_h * 0.33 - Inches(0.22),
            Inches(1.45), "T nominal\n9,55 N·m", size=9.5, color=GREEN,
            align=PP_ALIGN.RIGHT, bold=True)
    d.line(slide, ox, oy - ax_h, ox - Inches(0.12), oy - ax_h, color=INK)
    d.label(slide, ox - Inches(1.62), oy - ax_h - Inches(0.22), Inches(1.45),
            "T máximo\n≈ 28,6 N·m", size=9.5, color=RED,
            align=PP_ALIGN.RIGHT, bold=True)
    for frac, txt in ((0.0, "0"), (0.5, "3.000"), (0.76, "4.500"),
                      (0.99, "6.000")):
        x = ox + ax_w * frac
        d.line(slide, x, oy, x, oy + Inches(0.10), color=INK)
        d.label(slide, x - Inches(0.5), oy + Inches(0.12), Inches(1.0), txt,
                size=9.5, color=GRAY)

    d.label(slide, ox + ax_w * 0.48, oy - ax_h - Inches(0.30), Inches(2.9),
            "↓ el par pico cae por la f.c.e.m.", size=9.5, color=RED,
            bold=True, align=PP_ALIGN.RIGHT)

    # Panel lateral
    px = Inches(8.55)
    d._rect(slide, px, Inches(1.75), Inches(4.2), Inches(4.9), fill=LIGHT,
            line=GRAY_LINE)
    d._text(slide, px + Inches(0.25), Inches(1.95), Inches(3.7), Inches(0.35),
            "Cómo usar la curva", size=Pt(14), color=NAVY, bold=True)
    tf = slide.shapes.add_textbox(px + Inches(0.25), Inches(2.42), Inches(3.7),
                                  Inches(4.0)).text_frame
    tf.word_wrap = True
    d._fill_bullets(tf, [
        "Sitúa el punto de trabajo **continuo** (par RMS del ciclo) dentro de la "
        "zona verde, con un margen del 20 %.",
        "Sitúa el punto de **aceleración** (par máximo instantáneo) dentro de la "
        "zona azul, con un margen del 20-30 %.",
        "Comprueba la **velocidad máxima** del ciclo: en la parte derecha el par "
        "disponible cae.",
        "Si el punto continuo cae en zona intermitente → el motor se queda corto: "
        "sube de tamaño o añade reducción.",
        "Repite la comprobación con la **tensión mínima de red** del emplazamiento.",
    ], size=11.5)
