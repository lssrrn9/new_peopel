"""Módulo 7 — Parámetros, panel del drive y SigmaWin+."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, FIG, FUENTE, GRAY, GRAY_LINE, GREEN,
                     INK, LIGHT, LIGHT_BLUE, NAVY, NAVY_SOFT, RED, WHITE, Card,
                     Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 07",
        "Parámetros, panel y SigmaWin+",
        [
            "El panel frontal: leer el estado y navegar sin PC",
            "La lógica `Pn` / `Fn` / `Un` y cómo se editan los parámetros",
            "SigmaWin+: la herramienta que multiplica tu productividad",
            "El engranaje electrónico explicado con números",
            "Los parámetros que realmente vas a tocar",
            "Copia de seguridad y gestión de configuraciones",
        ],
        duration="4 h",
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
            "Comente que existen versiones y compatibilidades de SigmaWin+ según la "
            "serie del drive; conviene tener la versión actual descargada de la web "
            "del fabricante."
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
