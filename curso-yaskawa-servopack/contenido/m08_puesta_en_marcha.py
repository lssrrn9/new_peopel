"""Módulo 8 — Puesta en marcha paso a paso."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, GRAY, GRAY_LINE, GREEN, INK, LIGHT,
                     LIGHT_BLUE, NAVY, RED, WHITE, Card, Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 08",
        "Puesta en marcha paso a paso",
        [
            "La filosofía: avanzar por fases, sin saltarse ninguna",
            "Primer energizado y verificación del amplificador",
            "Prueba de JOG sin carga: el momento de la verdad",
            "Sentido de giro, límites y señales de estado",
            "Encoder absoluto y establecimiento del origen",
            "Acoplar la carga, probar el ciclo y documentar",
        ],
        duration="5 h (con equipo)",
        notes=(
            "Este es el módulo más práctico del curso. Si hay banco de pruebas, "
            "dedique la mayor parte del tiempo a ejecutar el procedimiento con los "
            "alumnos.\n\n"
            "El principio rector es 'aislar variables': se prueba primero el "
            "amplificador solo, después el motor sin carga, después con carga a baja "
            "velocidad, y sólo al final el ciclo completo. Cada fase debe superarse "
            "antes de pasar a la siguiente. Cuando algo falla, se sabe exactamente "
            "qué se acaba de cambiar."
        ),
    )

    _diagrama_fases(d)

    d.steps_slide(
        "Fase 1 — Primer energizado",
        [
            ("Con el motor **desacoplado** de la máquina",
             "Si no se puede desacoplar, asegura el eje mecánicamente y despeja la "
             "zona. Nunca hagas la primera prueba con la máquina cargada."),
            ("Conectar sólo la alimentación de **control** `L1C` `L2C`",
             "El display se enciende. Comprueba que no aparece ninguna alarma y "
             "anota la versión de firmware."),
            ("Verificar la identificación del motor",
             "El drive lee el motor por el encoder. Si la combinación no es válida, "
             "aparece una alarma de combinación (familia `A.05_`)."),
            ("Conectar la alimentación de **potencia** `L1` `L2` `L3`",
             "Comprueba la tensión entre fases antes y verifica que el LED CHARGE se "
             "enciende. `A.F10` indica falta de fase."),
            ("Comprobar señales de entrada con `Un005`",
             "¿Están cerrados `P-OT` y `N-OT`? ¿Llega `/S-ON` cuando el PLC lo "
             "activa? Se ve en el monitor sin necesidad de multímetro."),
            ("Verificar que `/S-RDY` se activa",
             "Si el drive no está 'listo', no sigas: hay un problema de "
             "alimentación, de seguridad (`CN8`) o de configuración."),
        ],
        subtitle="Objetivo: comprobar que el amplificador está sano antes de mover nada",
        callout=(
            "red",
            "Si aparece cualquier alarma en esta fase, párate",
            "Resuélvela antes de continuar. Avanzar con una alarma 'que se puede "
            "resetear' es la forma más rápida de acabar con una avería mayor.",
        ),
        notes=(
            "Insista en la primera línea: motor desacoplado. Si el sentido de giro "
            "está invertido o el engranaje electrónico mal calculado, un eje acoplado "
            "puede embalarse contra el tope mecánico en menos de un segundo.\n\n"
            "La comprobación de Un005 es un truco muy útil que ahorra tiempo: en "
            "lugar de medir con el multímetro pin a pin, el drive te dice qué "
            "entradas ve activas.\n\n"
            "Recuerde el caso de CN8: si el puente de seguridad no está y el circuito "
            "HWBB no está cableado, /S-RDY no se activará o el eje no dará par sin "
            "alarma evidente."
        ),
    )

    d.steps_slide(
        "Fase 2 — Prueba de JOG sin carga (`Fn002`)",
        [
            ("Reducir la velocidad de JOG con `Pn304`",
             "Ponla en 50-100 rpm para la primera prueba. La velocidad de fábrica "
             "puede ser demasiado alta para un primer arranque."),
            ("Entrar en la función `Fn002` desde el panel o SigmaWin+",
             "En modo JOG el drive ignora la consigna externa: el movimiento lo "
             "controlas tú. Es el modo más seguro para la primera prueba."),
            ("Activar el servo y girar en sentido positivo",
             "El motor debe girar suave, sin ruido anómalo, sin vibración y sin "
             "tirones. Observa y **escucha**."),
            ("Girar en sentido negativo y comparar",
             "El comportamiento debe ser simétrico. Una asimetría clara indica "
             "problema mecánico o de fase."),
            ("Comprobar `Un000` (velocidad) y `Un002` (par)",
             "La velocidad debe coincidir con `Pn304`. Sin carga, el par debe ser "
             "muy bajo (unos pocos por ciento). Un par alto en vacío es señal de "
             "alarma."),
            ("Verificar el sentido de giro respecto a la máquina",
             "Si es el contrario del deseado, cámbialo con `Pn000.0`. **Nunca** "
             "intercambiando fases del motor."),
        ],
        subtitle="Si el motor gira bien aquí, el 60 % del trabajo está hecho",
        callout=(
            "amber",
            "Qué observar además de los números",
            "Ruido metálico o zumbido agudo (posible resonancia o ganancia "
            "excesiva), vibración a baja velocidad (posible problema de "
            "acoplamiento o de encoder) y calentamiento anómalo tras unos minutos.",
        ),
        notes=(
            "La prueba de JOG es el mejor diagnóstico inicial que existe. Un motor "
            "que gira suave y silencioso en vacío, con par casi nulo, es un motor "
            "sano bien cableado.\n\n"
            "Si el motor vibra o hace ruido en vacío, las causas más probables son: "
            "ganancias de fábrica demasiado altas para esa mecánica, problema en el "
            "cable de encoder, o fases mal conectadas.\n\n"
            "Sobre el sentido de giro: la convención de YASKAWA es que el sentido "
            "positivo se ve antihorario mirando desde el lado del eje. Pn000.0 "
            "invierte esa convención sin tocar nada más del sistema."
        ),
    )

    d.steps_slide(
        "Fase 3 — Configuración básica del eje",
        [
            ("Modo de control (`Pn000.1`)",
             "Posición, velocidad o par, según la arquitectura decidida en el "
             "Módulo 06."),
            ("Engranaje electrónico (`Pn20E` / `Pn210`)",
             "Define la unidad de referencia. Calcúlalo, escríbelo y **compruébalo "
             "midiendo** un desplazamiento conocido."),
            ("Formato de la consigna (`Pn200.0` si es tren de pulsos)",
             "Debe coincidir exactamente con lo que emite el controlador."),
            ("Asignación de entradas y salidas (`Pn50A`…`Pn510`)",
             "Servo ON, finales de carrera, reset, `/COIN`, `ALM`, `/BK`. Documenta "
             "cada asignación en el esquema eléctrico."),
            ("Límites de protección (`Pn520`, `Pn522`)",
             "Error de posición admisible y ventana de posicionado, coherentes con "
             "la tolerancia mecánica de la aplicación."),
            ("Freno de retención (`Pn506` / `Pn507` / `Pn508`)",
             "Sólo si el motor lo lleva. Verifica la secuencia con el eje asegurado "
             "antes de confiar en ella."),
            ("Guardar la configuración",
             "Exporta el fichero antes de continuar: es tu punto de retorno."),
        ],
        subtitle="Ahora el drive ya sabe qué máquina tiene delante",
        notes=(
            "Ordene los pasos por dependencia: el engranaje electrónico debe estar "
            "antes que Pn520 y Pn522, porque estos últimos se expresan en unidades "
            "de referencia y su significado cambia con el engranaje.\n\n"
            "La comprobación del engranaje midiendo un desplazamiento real es "
            "obligatoria y no admite atajos. Dos minutos aquí evitan semanas de "
            "desconcierto."
        ),
    )

    d.steps_slide(
        "Fase 4 — Encoder absoluto y origen de máquina",
        [
            ("Verificar que la batería está instalada y en buen estado",
             "Sin batería, el encoder absoluto pierde el contaje multivuelta al "
             "cortar la alimentación."),
            ("Ejecutar el setup del encoder absoluto (`Fn008`)",
             "Se hace una única vez en la instalación, o tras un fallo de respaldo "
             "(`A.810`) o un cambio de motor. Requiere confirmación explícita."),
            ("Configurar el límite multivuelta (`Pn205`) si procede",
             "Sólo en ejes rotativos infinitos. Debe ser coherente con la relación "
             "de transmisión para que no haya salto al desbordar."),
            ("Llevar el eje a la posición de origen mecánico",
             "Con JOG a baja velocidad, contra el tope o el detector de referencia "
             "de la máquina."),
            ("Registrar el desplazamiento de origen en el controlador",
             "El drive da posición absoluta; el offset entre esa posición y el cero "
             "de la máquina lo guarda el PLC o el CNC."),
            ("**Documentar el valor de origen**",
             "Anótalo en el documento del eje y en el archivo de la máquina. Este "
             "número no está en el fichero de parámetros del drive."),
        ],
        subtitle="El paso que elimina el homing… y que hay que documentar",
        callout=(
            "amber",
            "El detalle que arruina una sustitución de equipo",
            "El fichero de parámetros **no** guarda el origen de la máquina. Si "
            "sustituyes drive o motor sin haber anotado el offset de origen, tendrás "
            "que rehacer la referencia mecánica del eje con la máquina parada.",
        ),
        notes=(
            "Explique la diferencia entre 'posición absoluta del encoder' y 'cero de "
            "la máquina'. El encoder sabe dónde está el rotor; sólo la máquina sabe "
            "dónde está su cero útil. La relación entre ambos es el offset de origen, "
            "que vive en el controlador.\n\n"
            "En algunas arquitecturas ese offset se guarda en el propio drive; en "
            "otras, en el PLC. Sea cual sea, debe estar documentado y respaldado.\n\n"
            "Ejercicio recomendado: simule una sustitución de drive. Cargue los "
            "parámetros en otro equipo, ejecute Fn008 y compruebe cuánto se tarda en "
            "recuperar el eje. Es un ensayo que vale su peso en oro cuando ocurra de "
            "verdad."
        ),
    )

    d.steps_slide(
        "Fase 5 — Acoplar la carga y probar el ciclo",
        [
            ("Acoplar la carga con el eje sin tensión",
             "Verifica la alineación y el apriete del acoplamiento antes de "
             "energizar."),
            ("Repetir el JOG, ahora con carga y a baja velocidad",
             "Compara `Un002` (par) con el valor calculado en el dimensionamiento. "
             "Una desviación grande indica fricción o desalineación."),
            ("Recorrer todo el rango de movimiento a baja velocidad",
             "Comprueba que el par es uniforme en todo el recorrido: un aumento "
             "local delata un punto duro mecánico."),
            ("Probar físicamente los finales de carrera",
             "Acciónalos a mano y comprueba que el eje se detiene y que puede "
             "retirarse en sentido contrario."),
            ("Ejecutar el autoajuste (Módulo 09)",
             "Con la carga real acoplada; nunca en vacío, porque la inercia medida "
             "no sería la de trabajo."),
            ("Subir progresivamente hasta la velocidad y aceleración del ciclo",
             "Por escalones, observando par, error de seguimiento y ruido en cada "
             "escalón."),
            ("Ejecutar el ciclo real durante un tiempo prolongado",
             "Vigila la temperatura del motor y del amplificador, y la tasa de "
             "sobrecarga acumulada."),
        ],
        subtitle="De la prueba a la producción, sin saltos",
        callout=(
            "green",
            "La comprobación que valida todo el diseño",
            "Comparar el par medido en la máquina real con el par calculado en el "
            "Módulo 04. Si coinciden razonablemente, el dimensionamiento era "
            "correcto y el eje tiene el margen previsto.",
        ),
        notes=(
            "El paso 3 (recorrer todo el rango a baja velocidad observando el par) es "
            "un diagnóstico mecánico de altísimo valor y coste cero. Un husillo "
            "torcido, un rodamiento dañado o una guía sucia se detectan "
            "inmediatamente como un aumento local del par.\n\n"
            "El paso 7 es el que más se salta y el que más problemas evita: muchos "
            "ejes funcionan perfectamente durante diez ciclos y disparan A.720 "
            "(sobrecarga continua) tras media hora de producción, porque el par RMS "
            "real es mayor que el calculado."
        ),
    )

    d.table_slide(
        "Acta de puesta en marcha del eje",
        ["Apartado", "Qué se registra"],
        [
            ["Identificación",
             "Máquina, eje, modelo de SERVOPACK y de motor, números de serie, "
             "versión de firmware"],
            ["Instalación",
             "Fecha, responsable, lista de verificación de instalación firmada"],
            ["Configuración",
             "Modo de control, engranaje electrónico, asignación de E/S, ficheros de "
             "parámetros (nombre y ubicación)"],
            ["Encoder absoluto",
             "Fecha de ejecución de `Fn008`, valor de origen, fecha de instalación de "
             "la batería"],
            ["Sintonización",
             "Método empleado, `Pn103`, `Pn100`, `Pn101`, `Pn102`, filtros activos y "
             "capturas de la traza"],
            ["Verificación de prestaciones",
             "Tiempo de ciclo alcanzado, par RMS medido, par pico medido, error de "
             "seguimiento máximo, temperaturas"],
            ["Seguridad",
             "Prueba de finales de carrera, prueba de HWBB/STO, prueba del freno de "
             "retención"],
            ["Observaciones y pendientes",
             "Todo lo que quedó por hacer o por revisar, con responsable y fecha"],
        ],
        [2.6, 9.5],
        subtitle="Documenta o repetirás el trabajo dentro de seis meses",
        size=10.5,
        foot="Este documento es lo que permite que otra persona (o tú mismo dentro de "
             "un año) entienda la instalación sin tener que reconstruirla.",
        notes=(
            "Insista en el valor económico de documentar: el coste de media hora de "
            "documentación frente al coste de un día de parada por no saber cómo "
            "estaba configurado un eje.\n\n"
            "Sugerencia: convertir esta tabla en una plantilla corporativa (Word o "
            "formulario digital) que se rellene en cada puesta en marcha."
        ),
    )

    d.table_slide(
        "Los diez errores más frecuentes en puesta en marcha",
        ["#", "Error", "Consecuencia y cómo evitarlo"],
        [
            ["1", "Probar con la carga acoplada desde el primer arranque",
             "Colisión o rotura. Desacopla siempre en la primera prueba"],
            ["2", "No verificar `CN8` (puente o circuito de seguridad)",
             "El eje no da par y parece averiado. Compruébalo antes de nada"],
            ["3", "Invertir el sentido de giro cambiando fases del motor",
             "Realimentación invertida: embalamiento o alarma. Usa `Pn000.0`"],
            ["4", "No comprobar el engranaje electrónico midiendo",
             "El eje se mueve el doble o la mitad. Mide 100 mm reales"],
            ["5", "Ejecutar el autoajuste sin la carga real",
             "La inercia estimada no es la de trabajo y el ajuste no sirve"],
            ["6", "Dejar `P-OT`/`N-OT` deshabilitados tras las pruebas",
             "Colisión contra tope a velocidad plena. Documenta y revierte"],
            ["7", "No guardar el fichero de parámetros original",
             "Imposible volver atrás. Guarda antes de tocar nada"],
            ["8", "Olvidar `Fn008` tras cambiar motor o batería",
             "Alarma `A.810` y posición absoluta perdida"],
            ["9", "No probar el ciclo de forma prolongada",
             "`A.720` en producción. Prueba al menos media hora a ritmo real"],
            ["10", "No anotar el valor de origen de la máquina",
             "Sustitución de equipo convertida en un día de parada"],
        ],
        [0.5, 4.4, 5.9],
        subtitle="Aprende de los errores ajenos: salen más baratos",
        size=9.5,
        align_center=(0,),
        notes=(
            "Puede usar esta tabla como cierre del módulo y como test rápido: pida a "
            "los alumnos que expliquen por qué cada error tiene la consecuencia "
            "indicada. Si saben justificarlo, han entendido el módulo.\n\n"
            "El error número 5 (autoajuste sin carga) es sutil y muy común: el "
            "técnico prueba en vacío porque es cómodo, obtiene un ajuste 'que va "
            "bien', acopla la carga y todo se degrada. La inercia es lo que el "
            "autoajuste mide, y sin carga mide otra máquina."
        ),
    )


# --------------------------------------------------------------------------
# Diagrama
# --------------------------------------------------------------------------

def _diagrama_fases(d: Deck) -> None:
    slide = d.canvas_slide(
        "El método: seis fases, sin saltos",
        "Cada fase se supera antes de empezar la siguiente",
        notes=(
            "Explique el principio de aislamiento de variables. Si se conecta todo y "
            "se arranca, cuando algo falla hay veinte causas posibles. Avanzando por "
            "fases, cuando algo falla sólo hay una: lo último que se ha cambiado.\n\n"
            "Este método no es más lento; es mucho más rápido, porque el tiempo "
            "perdido en diagnóstico a ciegas siempre supera al tiempo invertido en "
            "hacer las cosas en orden.\n\n"
            "Insista en la fase 0: la verificación previa es la que evita destruir "
            "equipo. Cinco minutos con el multímetro antes de energizar."
        ),
    )

    fases = [
        ("0", "VERIFICAR", "Lista de comprobación\nde instalación", GRAY),
        ("1", "ENERGIZAR", "Control, potencia\ny estado del drive", NAVY),
        ("2", "JOG SIN CARGA", "El motor gira\nsuave y silencioso", BLUE),
        ("3", "CONFIGURAR", "Modo, engranaje,\nE/S y límites", CYAN),
        ("4", "ORIGEN", "Encoder absoluto\ny cero de máquina", GREEN),
        ("5", "CARGA Y CICLO", "Autoajuste y\nproducción real", AMBER),
    ]

    w = Inches(1.85)
    gap = Inches(0.19)
    x = Inches(0.62)
    y = Inches(2.25)
    h = Inches(2.1)
    for num, titulo, desc, color in fases:
        d._rect(slide, x, y, w, h, fill=LIGHT, line=color, line_w=Pt(1.5))
        d._rect(slide, x, y, w, Inches(0.52), fill=color)
        d._text(slide, x, y + Inches(0.12), w, Inches(0.3), f"FASE {num}",
                size=Pt(11), color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        d._text(slide, x + Inches(0.1), y + Inches(0.72), w - Inches(0.2),
                Inches(0.4), titulo, size=Pt(12), color=color, bold=True,
                align=PP_ALIGN.CENTER)
        d._text(slide, x + Inches(0.1), y + Inches(1.18), w - Inches(0.2),
                Inches(0.8), desc, size=Pt(10), color=GRAY,
                align=PP_ALIGN.CENTER, spacing=1.1)
        if x + w < Inches(11.5):
            d.arrow(slide, x + w + Inches(0.02), y + h / 2 - Inches(0.08),
                    gap - Inches(0.04), Inches(0.16), color=GRAY)
        x += w + gap

    d.callout(slide, Inches(0.62), Inches(4.72), Inches(12.1), Inches(0.95),
              "blue", "La regla que hace que este método funcione",
              "Un cambio cada vez. Si modificas tres cosas y el eje empieza a "
              "comportarse mal, no sabrás cuál ha sido. Y si el eje mejora, tampoco "
              "sabrás por qué.")

    d.callout(slide, Inches(0.62), Inches(5.88), Inches(12.1), Inches(1.02),
              "red", "Condiciones de seguridad durante toda la puesta en marcha",
              "Zona despejada y señalizada · Parada de emergencia accesible y "
              "probada · Velocidades reducidas hasta validar el comportamiento · "
              "Nadie en el recorrido del eje · Chavetas y herramientas retiradas del "
              "eje del motor.")
