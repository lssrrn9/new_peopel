"""Módulo 2 — La familia SERVOPACK Σ-X y el modelo de 3 kW."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, FIG, FUENTE, GRAY, GRAY_LINE, GREEN,
                     INK, LIGHT, LIGHT_BLUE, NAVY, NAVY_SOFT, RED, WHITE, Card,
                     Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 02",
        "La familia SERVOPACK Σ-X",
        [
            "De la Σ-II a la Σ-X: qué cambió y por qué importa",
            "Las tres líneas de amplificador: SGDXS, SGDXW y SGDXT",
            "Qué hay dentro: etapa de potencia y control",
            "Anatomía externa: bornes, conectores y elementos de diagnóstico",
            "Leer y escribir un código de modelo sin equivocarse",
            "Por qué el SGDXS-200A00A es el amplificador de 3 kW",
        ],
        duration="3 h",
        notes=(
            "El objetivo del módulo es que el alumno pueda mirar la etiqueta de un "
            "SERVOPACK cualquiera y deducir en 10 segundos: tensión, potencia, "
            "interfaz de comando y generación. Es una habilidad muy práctica en "
            "mantenimiento y en compras de repuesto."
        ),
    )

    d.two_col_slide(
        "Evolución de la familia y qué aporta la Σ-X",
        (
            "Generaciones",
            [
                "**Σ-II (SGDH)** — años 2000. Encoder de 17 bits. Todavía se "
                "encuentra en máquinas antiguas.",
                "**Σ-V (SGDV)** — 2008. Encoder de 20 bits, autotuning avanzado, "
                "MECHATROLINK-II/III.",
"**Σ-7 (SGD7S/W/C)** — 2014. Encoder de 24 bits, control por modelo "
                "de referencia y ajuste sin sintonizar.",
                "**Σ-X (SGDXS/XW/XT)** — la generación actual y **la de tu equipo**. "
                "Ancho de banda del lazo de velocidad de **3,5 kHz**, encoders de "
                "hasta **26 bits**, compensación de rizado y de fricción, y "
                "`Σ-LINK II` para conectar sensores y E/S al propio drive.",
                "- La lógica `Pn___` se mantiene muy parecida entre Σ-V, Σ-7 y Σ-X: "
                "quien conoce una se mueve con soltura en las otras.",
            ],
        ),
        (
            "Qué gana el usuario con la Σ-X",
            [
                "**Tiempo de puesta en marcha**: el autoajuste sin parámetros previos "
                "arranca un eje razonable en minutos.",
                "**Tiempo de posicionado** menor gracias al control por modelo "
                "(Model Following Control) y a la supresión de vibración.",
                "**Diagnóstico**: registro de alarmas, monitor de vida útil de "
                "componentes y función de traza integrada.",
                "**Seguridad funcional** de serie: entradas HWBB (STO) hasta "
                "SIL 3 / PL e.",
                "**Modo de compatibilidad con Σ-7**: `Pn50A = n.□□□1` reproduce la "
                "asignación de E/S de la serie anterior, lo que facilita mucho el "
                "retrofit de una máquina existente.",
                "- La sustitución de un Σ-V o un Σ-7 por un Σ-X suele ser directa "
                "mecánicamente, pero **no** copies los parámetros a ciegas.",
            ],
        ),
        subtitle="Sigma-X: la generación que probablemente tengas delante",
        callout=(
            "amber",
            "Aviso de repuestos",
            "No se pueden volcar sin más los parámetros de un SGDV en un SGDXS: "
            "cambian rangos, resoluciones y algunos significados de bit. Utiliza la "
            "función de conversión de SigmaWin+ y revisa después el eje completo.",
        ),
        notes=(
            "Pregunte al grupo qué generación tienen instalada. En planta suele "
            "haber mezcla, y saber distinguirlas por el código (SGDH / SGDV / SGDX) "
            "evita pedir repuestos equivocados.\n\n"
            "Dato útil: subir la resolución del encoder no da tanto 'más precisión "
            "de posicionado' como una medida de velocidad mucho más limpia a baja "
            "velocidad, lo que permite ganancias más altas sin ruido. Ese es el "
            "motivo real de que la Σ-X alcance 3,5 kHz de ancho de banda.\n\n"
            "El modo de compatibilidad de E/S con Σ-7 (Pn50A = n.□□□1) es un detalle "
            "muy práctico en retrofit: permite reutilizar el cableado de CN1 de una "
            "máquina antigua sin rehacer el armario."
        ),
    )

    d.cards_slide(
        "Las tres líneas de amplificador Σ-X",
        [
            Card(
                "SGDXS — un eje",
                "Amplificador **monoeje**, el más habitual y el que usaremos en el "
                "curso.\n"
                "· Cubre de 50 W a 15 kW en 200 V.\n"
                "· Todas las interfaces de comando disponibles.\n"
                "· Nuestro modelo: **SGDXS-200A00A-Y3600A** (3,0 kW).",
                "blue",
            ),
            Card(
                "SGDXW — dos ejes",
                "Amplificador **de dos ejes** en un solo cuerpo.\n"
                "· Ahorra espacio en el armario y comparte el bus de continua entre "
                "los dos ejes.\n"
                "· Limitado a potencias medias-bajas por eje.\n"
                "· Interesante en máquinas con muchos ejes pequeños.",
                "cyan",
            ),
            Card(
                "SGDXT — tres ejes",
                "Amplificador **de tres ejes** en un solo cuerpo.\n"
                "· Máxima densidad por metro de armario.\n"
                "· Pensado para máquinas con muchos ejes de potencia baja.\n"
                "· Comparte el conector de E/S con el SGDXS: el cableado de "
                "control es familiar.",
                "green",
            ),
        ],
        subtitle="Elegir la línea correcta antes de mirar la potencia",
        intro="Para un eje de 3 kW en una máquina con PLC o CNC externo, la elección "
              "natural es SGDXS.",
        notes=(
            "Criterio de decisión rápido:\n"
            "· ¿El movimiento lo calcula un PLC/CNC que ya existe? → SGDXS.\n"
            "· ¿Muchos ejes pequeños y armario ajustado? → evaluar SGDXW.\n"
            "· ¿Máquina sencilla sin controlador de movimiento? → SGDXT.\n\n"
            "Para 3 kW la línea SGDXW habitualmente no llega en potencia por eje, "
            "así que la decisión está prácticamente tomada."
        ),
    )

    _diagrama_bloques_internos(d)

    d.figure_slide(
        "Diagrama de bloques oficial del SGDXS-180A / -200A",
        FIG + "diagrama_bloques_200a.png",
        subtitle="El interior del amplificador, según el manual del fabricante",
        puntos=[
            "#Camino de la energía",
            "Entrada `L1` `L2` `L3` con **varistor** → rectificador → bus de "
            "continua con condensadores → inversor IGBT → `U` `V` `W`.",
            "El **relé de precarga** limita la corriente de arranque al cargar los "
            "condensadores.",
            "#Protecciones que verás en el esquema",
            "- Sensores de tensión en la entrada y en el bus.",
            "- Sensor de temperatura y protección de **sobrecalentamiento y "
            "sobrecorriente**.",
            "- Detector de corriente en la salida al motor.",
            "- **Circuito de freno dinámico** en las fases del motor.",
            "#Control",
            "Alimentación propia por `L1C` `L2C`, procesador de lazos y conectores "
            "`CN1`, `CN2`, `CN5`, `CN8`, `CN11` y `CN12`.",
        ],
        fuente=FUENTE + " · apartado 2.2.6",
        notes=(
            "Ésta es la misma idea del diagrama simplificado anterior, pero en la "
            "versión oficial y para el modelo exacto del alumno. Merece la pena "
            "recorrerla despacio.\n\n"
            "Señale los elementos que el diagrama simplificado no mostraba: el "
            "varistor de entrada (absorbe sobretensiones de red), los sensores de "
            "tensión y temperatura, el detector de corriente y el ventilador.\n\n"
            "Fíjese en que CN11 y CN12 son conectores de módulo opcional (seguridad "
            "y realimentación). En la Σ-7 no existían con esa denominación: es una "
            "de las novedades de la Σ-X."
        ),
    )

    _diagrama_anatomia(d)

    d.figure_slide(
        "Partes del SERVOPACK, según el fabricante",
        FIG + "partes_servopack.png",
        subtitle="Vista externa con la numeración del manual",
        puntos=[
            "#Lo que hay que localizar físicamente",
            "**Bornes de circuito principal** y **bornes de motor** (`U` `V` `W`), "
            "en el lateral izquierdo.",
            "**Indicador CHARGE**: bus cargado, peligro de descarga eléctrica.",
            "`CN1` señales de E/S · `CN2` encoder · `CN3` operador digital / RS-422 "
            "· `CN5` monitor analógico · `CN7` USB para SigmaWin+ · `CN8` seguridad.",
            "`CN11` módulo opcional de seguridad · `CN12` módulo opcional de "
            "realimentación.",
            "**Código QR** para el servicio MechatroCloud.",
            "Bajo la tapa frontal: **panel de operación** y visualizador.",
        ],
        fuente=FUENTE + " · apartado 1.3 Part Names",
        notes=(
            "Ejercicio de cinco minutos: que cada alumno localice en el equipo real "
            "los elementos numerados de la figura. Ahorra muchos errores después.\n\n"
            "Puntos de atención:\n"
            "· CN7 (USB) es la vía normal de trabajo con SigmaWin+.\n"
            "· CN8 viene con un conector puente de fábrica; retirarlo sin cablear la "
            "seguridad deja el eje sin par y sin alarma evidente.\n"
            "· El LED CHARGE encendido significa bus cargado: nunca es sustituto de "
            "la medida con multímetro.\n"
            "· La placa de características lleva el modelo completo, incluido el "
            "sufijo -Y3600A: fotografíela en la puesta en marcha."
        ),
    )

    _diagrama_codigo_modelo(d)

    d.table_slide(
        "Gama Σ-X monoeje en 200 V trifásica",
        ["Modelo SGDXS-", "Motor máx.", "Corriente continua", "Corriente de pico",
         "Corriente de entrada"],
        [
            ["-R70A", "50 W", "0,66 A", "2,1 A", "0,4 A"],
            ["-R90A", "100 W", "0,91 A", "3,2 A", "0,8 A"],
            ["-1R6A", "200 W", "1,6 A", "5,9 A", "1,3 A"],
            ["-2R8A", "400 W", "2,8 A", "9,3 A", "2,5 A"],
            ["-3R8A", "500 W", "3,8 A", "11 A", "3,0 A"],
            ["-5R5A", "750 W", "5,5 A", "16,9 A", "4,1 A"],
            ["-7R6A", "1,0 kW", "7,6 A", "17 A", "5,7 A"],
            ["-120A", "1,5 kW", "11,6 A", "28 A", "7,3 A"],
            ["-180A", "2,0 kW", "18,5 A", "42 A", "10 A"],
            ["**-200A**", "**3,0 kW**", "**19,6 A**", "**56 A**", "**15 A**"],
            ["-330A", "5,0 kW", "32,9 A", "84 A", "25 A"],
            ["-470A", "6,0 kW", "46,9 A", "110 A", "29 A"],
            ["-550A", "7,5 kW", "54,7 A", "130 A", "37 A"],
            ["-780A", "15 kW", "78,0 A", "170 A", "73 A"],
        ],
        [2.0, 1.8, 2.4, 2.2, 2.4],
        subtitle="La cifra central del código es el indicador de tamaño",
        size=9.5,
        align_center=(0, 1, 2, 3, 4),
        foot="Valores del manual SIEP C710812 03I, tabla 2.1.1 (trifásica 200 VAC). "
             "Corrientes eficaces; la de pico es admisible sólo de forma "
             "instantánea.",
        notes=(
            "Fíjese en un detalle muy revelador: el -180A (2 kW) da 18,5 A continuos "
            "y el -200A (3 kW) da 19,6 A. Apenas un 6 % más de corriente para un "
            "50 % más de potencia declarada. La diferencia real está en la corriente "
            "de pico (42 A frente a 56 A) y en la capacidad térmica.\n\n"
            "De ahí la regla: la selección se hace por COMBINACIÓN homologada "
            "motor+drive, no eligiendo cada pieza por amperios.\n\n"
            "Regla de repuesto: nunca sustituya un SERVOPACK por otro de tamaño "
            "distinto 'porque encaja'. Cambian la protección, la resistencia de "
            "regeneración interna y la combinación admitida."
        ),
    )

    d.table_slide(
        "Ficha técnica del SGDXS-200A00A",
        ["Concepto", "Valor oficial", "Para qué lo necesitas"],
        [
            ["Capacidad máxima de motor", "3,0 kW",
             "Debe coincidir con la del motor combinado"],
            ["Corriente de salida continua", "19,6 A eficaces",
             "Corresponde al par nominal sostenido"],
            ["Corriente de salida instantánea máxima", "56 A eficaces",
             "Corresponde al par de aceleración"],
            ["Alimentación del circuito principal",
             "Trifásica 200–240 V CA, 50/60 Hz, −15 % / +10 %",
             "Bornes `L1` `L2` `L3`"],
            ["Corriente de entrada del circuito principal", "15 A eficaces",
             "Dimensiona cable, protección y contactor"],
            ["Alimentación del circuito de control",
             "200–240 V CA, 0,25 A eficaces",
             "Bornes `L1C` `L2C`, independientes de la potencia"],
            ["Capacidad de alimentación requerida", "5,9 kVA",
             "Dato para la acometida o el transformador"],
            ["Pérdidas totales", "130,2 W (114,2 W potencia + 16 W control)",
             "**Balance térmico del armario**"],
            ["Resistencia de regeneración incorporada",
             "10 Ω · 60 W · 30 W de consumo admisible",
             "Suficiente para frenados moderados"],
            ["Resistencia externa mínima admisible", "10 Ω",
             "**Nunca** conectes una resistencia de menor valor"],
            ["Categoría de sobretensión", "III",
             "Coordinación de aislamiento de la instalación"],
            ["Realimentación", "Encoder serie (hasta 26 bits en motores Σ-X)",
             "Conector `CN2`"],
        ],
        [3.4, 3.9, 3.7],
        subtitle="Datos tomados del manual oficial del fabricante",
        size=9.5,
        foot="Fuente: Σ-XS SERVOPACK with Analog Voltage/Pulse Train References "
             "Product Manual, SIEP C710812 03I, apartado 2.1 (YASKAWA).",
        notes=(
            "Las cuatro cifras que hay que memorizar: 15 A de entrada, 19,6 A de "
            "salida continua, 56 A de pico y 130 W de pérdidas. Con ellas se "
            "dimensionan cable, magnetotérmico, contactor, filtro y climatización "
            "del armario.\n\n"
            "Ojo con la resistencia de regeneración: la interna es de 10 Ω y 60 W, "
            "pero su consumo admisible continuo es de sólo 30 W. Ese es el número "
            "que hay que comparar con la potencia media de regeneración calculada "
            "en el Módulo 04.\n\n"
            "La resistencia externa mínima admisible también es de 10 Ω: poner una "
            "de menor valor hace circular más corriente de la que soporta el "
            "transistor de frenado y lo destruye.\n\n"
            "Recuerde que el sufijo -Y3600A puede alterar algún dato: contraste con "
            "la placa de características y con la hoja de especificación Y."
        ),
    )

    d.table_slide(
        "Interfaces de comando disponibles",
        ["Interfaz", "Cómo llega la consigna", "Cuándo elegirla"],
        [
            ["Tensión analógica y tren de pulsos",
             "±10 V para velocidad/par y `PULS`/`SIGN` para posición",
             "Retrofit, CNC clásicos, controladores con salida de pulsos. Cableado "
             "sencillo y sin latencia de red."],
            ["MECHATROLINK-II / III",
             "Bus de movimiento propietario YASKAWA sobre cable dedicado",
             "Máquinas con controlador YASKAWA (MP2000/MP3000). Sincronismo entre "
             "ejes excelente."],
            ["EtherCAT (CoE, perfil CiA 402)",
             "Telegramas cíclicos sobre Ethernet industrial",
             "La opción más habitual en instalaciones nuevas con PLC de terceros "
             "(Beckhoff, Omron, Codesys…)."],
            ["Modo indexador / posicionamiento interno",
             "Tablas de posiciones almacenadas en el drive, disparadas por E/S",
             "Máquinas sencillas sin controlador de movimiento."],
        ],
        [3.0, 4.0, 4.0],
        subtitle="La variante se decide **al comprar**: forma parte del código de modelo",
        size=10.5,
        foot="El sufijo del código identifica la interfaz. Verifica el sufijo exacto "
             "en el catálogo antes de emitir el pedido: no se puede cambiar después.",
        notes=(
            "Este es el error de compra más caro y más frecuente: pedir el tamaño "
            "correcto con la interfaz equivocada. La interfaz NO es una opción "
            "configurable por parámetro ni una tarjeta que se añada después; define "
            "el hardware del amplificador.\n\n"
            "Consejo de proyecto: si el controlador aún no está decidido, la variante "
            "analógica/pulsos es la más 'neutra', pero pierde diagnóstico remoto y "
            "obliga a cablear mucha señal. En instalación nueva, EtherCAT suele ser "
            "la mejor relación coste/prestaciones.\n\n"
            "Con bus, además, el ajuste y la monitorización se pueden hacer en "
            "remoto, algo muy valorado en mantenimiento."
        ),
    )

    d.table_slide(
        "Periféricos y accesorios que casi siempre hacen falta",
        ["Elemento", "Para qué sirve", "¿Obligatorio?"],
        [
            ["Interruptor automático o fusibles", "Protección de cortocircuito de la "
             "línea de entrada", "Sí"],
            ["Contactor de línea", "Cortar la potencia manteniendo el control vivo",
             "Muy recomendable"],
            ["Filtro de red (EMC)", "Cumplir la directiva de compatibilidad "
             "electromagnética", "Sí en marcado CE"],
            ["Reactancia de línea de CA/CC", "Reducir armónicos y proteger frente a "
             "red dura", "Recomendable"],
            ["Resistencia de regeneración externa", "Disipar la energía de frenado "
             "cuando la interna no basta", "Según cálculo (Módulo 04)"],
            ["Cable de potencia de motor apantallado", "Alimentar `U` `V` `W` sin "
             "radiar interferencias", "Sí"],
            ["Cable de encoder apantallado", "Realimentación por `CN2`",
             "Sí, y siempre el cable original"],
            ["Batería del encoder absoluto", "Mantener el contaje multivuelta sin "
             "tensión", "Sí, si se usa como absoluto"],
            ["Fuente de 24 V CC", "Alimentar las E/S de `CN1` y el freno del motor",
             "Sí"],
            ["Cable USB y SigmaWin+", "Parametrizar, ajustar, diagnosticar y hacer "
             "copia de seguridad", "Imprescindible en la práctica"],
            ["Operador digital JUSP-OP05A", "Parametrizar sin PC",
             "Opcional (el panel frontal ya permite casi todo)"],
        ],
        [3.4, 5.4, 2.2],
        subtitle="Lista de la compra del armario",
        size=10.0,
        notes=(
            "Sugerencia: proyecte esta diapositiva cuando el grupo esté preparando "
            "un presupuesto. El coste oculto de un eje servo no está en el drive, "
            "sino en cables originales, filtro y resistencia de frenado.\n\n"
            "Insista en los cables: fabricar cables de encoder 'a mano' es una fuente "
            "constante de alarmas intermitentes A.C90 (error de comunicación con el "
            "encoder), casi imposibles de diagnosticar. Compre siempre cable original "
            "confeccionado."
        ),
    )


# --------------------------------------------------------------------------
# Diagramas
# --------------------------------------------------------------------------

def _diagrama_bloques_internos(d: Deck) -> None:
    slide = d.canvas_slide(
        "Qué hay dentro del SERVOPACK",
        "De la red trifásica a la corriente controlada en el motor",
        notes=(
            "Recorra el camino de la energía: rectificador → bus de continua → "
            "inversor IGBT → motor. Y el camino de la información: encoder → control "
            "→ modulación PWM.\n\n"
            "Tres consecuencias prácticas que hay que extraer del diagrama:\n"
            "1) El bus de continua almacena energía en condensadores: por eso hay que "
            "esperar antes de tocar los bornes y por eso existe el LED CHARGE.\n"
            "2) Al frenar, el motor actúa como generador y devuelve energía al bus; "
            "si la tensión sube demasiado salta A.400 (sobretensión). La resistencia "
            "de regeneración existe para quemar ese exceso.\n"
            "3) El circuito de control tiene alimentación propia (L1C/L2C), lo que "
            "permite diagnosticar con la potencia cortada.\n\n"
            "El freno dinámico es un cortocircuito controlado de las fases del motor: "
            "frena rápido sin necesidad de electrónica, pero no mantiene la carga "
            "parada ni sirve como freno de seguridad."
        ),
    )

    y = Inches(1.95)
    h = Inches(1.25)
    w = Inches(2.15)
    gap = Inches(0.30)
    x0 = Inches(0.65)

    etapas = [
        ("RED\n3 × 200-240 V", GRAY),
        ("RECTIFICADOR\n+ precarga", NAVY),
        ("BUS DE CONTINUA\n≈ 310 V CC", BLUE),
        ("INVERSOR IGBT\nPWM senoidal", CYAN),
        ("MOTOR\nSGMXA-30A", GREEN),
    ]
    xs = []
    for i, (texto, color) in enumerate(etapas):
        x = x0 + i * (w + gap)
        xs.append(x)
        d.box(slide, x, y, w, h, texto, color, size=12, radius=0.10)
        if i < len(etapas) - 1:
            d.arrow(slide, x + w + Inches(0.05), y + h / 2 - Inches(0.12),
                    gap - Inches(0.10), Inches(0.24), color=AMBER)

    # Regeneración colgando del bus
    y_reg = Inches(3.75)
    d.line(slide, xs[2] + w / 2, y + h, xs[2] + w / 2, y_reg, color=RED,
           width=Pt(1.5))
    d.box(slide, xs[2] + w / 2 - Inches(1.35), y_reg, Inches(2.7), Inches(0.72),
          "RESISTENCIA DE\nREGENERACIÓN  `B1`-`B2`", RED, size=10.5)
    d.label(slide, xs[2] + w / 2 - Inches(1.55), y_reg + Inches(0.80),
            Inches(3.1), "Quema la energía que el motor\ndevuelve al frenar",
            size=9.5, color=GRAY)

    # Freno dinámico
    d.line(slide, xs[3] + w / 2, y + h, xs[3] + w / 2, y_reg, color=GRAY,
           width=Pt(1.25), dash=True)
    d.box(slide, xs[3] + w / 2 - Inches(1.0), y_reg, Inches(2.0), Inches(0.72),
          "FRENO DINÁMICO", GRAY, size=10.5)
    d.label(slide, xs[3] + w / 2 - Inches(1.25), y_reg + Inches(0.80),
            Inches(2.5), "Cortocircuita las fases\npara detener por inercia",
            size=9.5, color=GRAY)

    # Bloque de control
    y_ctl = Inches(5.60)
    d.box(slide, Inches(0.65), y_ctl, Inches(8.95), Inches(0.85),
          "CIRCUITO DE CONTROL — lazos, parámetros, protecciones y diagnóstico   ·   "
          "alimentación propia por `L1C` / `L2C`", NAVY_SOFT, size=11.5)
    d.arrow(slide, xs[3] + w / 2 - Inches(0.12), y_ctl - Inches(0.52),
            Inches(0.24), Inches(0.52), color=NAVY_SOFT, direction="up")

    d.box(slide, Inches(9.85), y_ctl, Inches(2.85), Inches(0.85),
          "ENCODER 24 bits → `CN2`\nposición y velocidad reales", GREEN,
          size=11)
    d.arrow(slide, Inches(9.62), y_ctl + Inches(0.30), Inches(0.20),
            Inches(0.25), color=GREEN, direction="left")


def _diagrama_anatomia(d: Deck) -> None:
    slide = d.canvas_slide(
        "Anatomía del SGDXS-200A00A",
        "Dónde está cada cosa en el frontal del amplificador",
        notes=(
            "Haga que los alumnos localicen físicamente cada elemento en el equipo "
            "real antes de continuar. Es un ejercicio de 5 minutos que ahorra muchos "
            "errores después.\n\n"
            "Puntos de atención:\n"
            "· CN7 (USB) es la vía normal de conexión con SigmaWin+.\n"
            "· CN8 viene con un conector puente de fábrica. Si se retira sin cablear "
            "la seguridad, el drive queda en baseblock y no habrá par: es la causa "
            "número uno de 'el motor no arranca y no da alarma'.\n"
            "· El LED CHARGE indica bus cargado. Nunca es sustituto de la medida con "
            "multímetro.\n"
            "· El display de 7 segmentos muestra el estado, la alarma y los valores "
            "durante la parametrización desde el panel."
        ),
    )

    # Cuerpo del drive
    body_x, body_y = Inches(0.85), Inches(1.75)
    body_w, body_h = Inches(3.5), Inches(5.0)
    d._rect(slide, body_x, body_y, body_w, body_h, fill=LIGHT, line=NAVY,
            line_w=Pt(2))
    d.label(slide, body_x, body_y - Inches(0.34), body_w,
            "Vista frontal (esquemática)", size=10.5, color=GRAY, bold=True)

    elementos = [
        ("Display + teclas de operación", CYAN, Inches(0.50)),
        ("`CN7` USB → SigmaWin+", BLUE, Inches(0.42)),
        ("`CN3` operador digital / RS-422", BLUE, Inches(0.42)),
        ("`CN1` E/S de control (50 pines)", NAVY, Inches(0.46)),
        ("`CN2` encoder del motor", GREEN, Inches(0.42)),
        ("`CN8` seguridad HWBB", RED, Inches(0.42)),
        ("`CN5` monitor analógico", GRAY, Inches(0.42)),
        ("`CN11` / `CN12` módulos opcionales", GRAY, Inches(0.42)),
    ]
    y = body_y + Inches(0.22)
    for texto, color, alto in elementos:
        d.box(slide, body_x + Inches(0.22), y, body_w - Inches(0.44), alto,
              texto, color, size=10.5, radius=0.15)
        y += alto + Inches(0.11)

    # Bornero
    tx, ty = Inches(5.05), Inches(1.75)
    tw = Inches(3.5)
    d._rect(slide, tx, ty, tw, Inches(5.0), fill=WHITE, line=GRAY_LINE)
    d.label(slide, tx, ty - Inches(0.34), tw, "Bornes de potencia", size=10.5,
            color=GRAY, bold=True)

    bornes = [
        ("`L1` `L2` `L3`", "Entrada trifásica 200-240 V", NAVY),
        ("`L1C` `L2C`", "Alimentación del control (monofásica)", NAVY_SOFT),
        ("`B1/⊕` `B2` `B3`", "Resistencia de regeneración", RED),
        ("`⊖1` `⊖2`", "Bus de continua (negativo)", GRAY),
        ("`U` `V` `W`", "Salida al motor — ¡respetar el orden!", CYAN),
        ("⏚ Tierra", "Puesta a tierra del equipo y del motor", GREEN),
    ]
    y = ty + Inches(0.25)
    for borne, desc, color in bornes:
        d._rect(slide, tx + Inches(0.18), y, tw - Inches(0.36), Inches(0.68),
                fill=LIGHT, line=GRAY_LINE)
        d._rect(slide, tx + Inches(0.18), y, Inches(0.07), Inches(0.68),
                fill=color)
        d._text(slide, tx + Inches(0.38), y + Inches(0.08), tw - Inches(0.62),
                Inches(0.26), borne, size=Pt(11), color=color, bold=True)
        d._text(slide, tx + Inches(0.38), y + Inches(0.36), tw - Inches(0.62),
                Inches(0.26), desc, size=Pt(9.5), color=GRAY)
        y += Inches(0.79)

    # Notas laterales
    nx = Inches(9.25)
    d._rect(slide, nx, Inches(1.75), Inches(3.45), Inches(5.0), fill=LIGHT_BLUE,
            line=BLUE, line_w=Pt(0.75))
    d._text(slide, nx + Inches(0.25), Inches(1.95), Inches(2.95), Inches(0.35),
            "Detalles que dan problemas", size=Pt(13.5), color=NAVY, bold=True)
    tf = slide.shapes.add_textbox(nx + Inches(0.25), Inches(2.42), Inches(2.95),
                                  Inches(4.1)).text_frame
    tf.word_wrap = True
    d._fill_bullets(tf, [
        "El **LED CHARGE** encendido significa bus cargado: peligro de muerte.",
        "`CN8` sale de fábrica con un **puente**. Si lo quitas sin cablear el "
        "circuito de seguridad, el eje no dará par.",
        "El puente `B2`-`B3` conecta la resistencia interna: al montar una externa "
        "hay que **retirarlo**.",
        "El ventilador es un consumible: prevé su sustitución.",
        "La **etiqueta lateral** lleva el modelo exacto y la revisión de firmware: "
        "fotografíala en la puesta en marcha.",
    ], size=11)


def _diagrama_codigo_modelo(d: Deck) -> None:
    slide = d.canvas_slide(
        "Cómo se lee un código de modelo",
        "Ejemplo: SGDXS-200A00A00A",
        notes=(
            "Ejercicio recomendado: reparta fotos de etiquetas reales (o pida a los "
            "alumnos que fotografíen las de su planta) y que decodifiquen el modelo "
            "en voz alta.\n\n"
            "El campo crítico es la interfaz de comando: determina el hardware y no "
            "se puede cambiar. El segundo campo crítico es el tamaño (200 = 3,0 kW), "
            "que fija corriente, protecciones y resistencia de regeneración "
            "interna.\n\n"
            "Advertencia honesta que hay que trasladar al alumno: los dígitos de "
            "interfaz y de opciones varían según catálogo, región y revisión. La "
            "estructura del código es estable, los códigos concretos hay que "
            "verificarlos en el catálogo vigente antes de pedir."
        ),
    )

    campos = [
        ("SGDX", "Serie\nΣ-X", NAVY),
        ("S", "Línea\nS = 1 eje", BLUE),
        ("200", "Tamaño\n3,0 kW", RED),
        ("A", "Tensión\nA = 200 V", CYAN),
        ("00", "Interfaz de comando\n(analógica/pulsos,\nbus…)", AMBER),
        ("A", "Opciones de diseño\ny hardware", GRAY),
    ]

    x = Inches(0.9)
    y = Inches(2.05)
    h = Inches(1.05)
    anchos = [Inches(1.75), Inches(1.15), Inches(1.45), Inches(1.15),
              Inches(2.6), Inches(2.4)]
    for (codigo, desc, color), w in zip(campos, anchos):
        d.box(slide, x, y, w, h, codigo, color, size=22, radius=0.08)
        d.label(slide, x - Inches(0.18), y + h + Inches(0.16), w + Inches(0.36),
                desc, size=10.5, color=color, bold=True)
        x += w + Inches(0.16)

    d.label(slide, Inches(0.9), Inches(1.65), Inches(11.5),
            "Estructura del código (los separadores se omiten en la etiqueta)",
            size=10.5, color=GRAY, align=PP_ALIGN.LEFT)

    # Tabla de apoyo
    headers = ["Campo", "Qué codifica", "Por qué es crítico"]
    rows = [
        ["Serie", "Generación del amplificador (SGDX, SGDV, SGDH)",
         "Determina parámetros, encoder compatible y herramienta software"],
        ["Línea", "S = monoeje · W = dos ejes · C = con control integrado",
         "Cambia por completo la arquitectura del sistema"],
        ["Tamaño", "Capacidad máxima de motor (200 → 3,0 kW)",
         "Fija corriente, protecciones y regeneración interna"],
        ["Tensión", "A = 200 V clase · D = 400 V clase",
         "Un error aquí destruye el equipo al energizar"],
        ["Interfaz", "Analógica/pulsos, MECHATROLINK, EtherCAT…",
         "**No se puede cambiar después de la compra**"],
    ]
    d.table(slide, Inches(0.9), Inches(3.95), Inches(11.55), Inches(2.65),
            headers, rows, [1.4, 4.2, 5.4], size=10.0)
