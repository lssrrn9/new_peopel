"""Módulo 9 — Sintonización del lazo de control."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, GRAY, GRAY_LINE, GREEN, INK, LIGHT,
                     LIGHT_BLUE, NAVY, RED, WHITE, Card, Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 09",
        "Sintonización del lazo de control",
        [
            "Qué significa 'estar bien sintonizado' y cómo se mide",
            "Las herramientas de ajuste de la Σ-7 y cuándo usar cada una",
            "Autoajuste: sin parámetros, avanzado y con referencia",
            "Ajuste manual: el orden correcto de las ganancias",
            "Resonancia mecánica: filtros notch y análisis en frecuencia",
            "Vibración de baja frecuencia y control por modelo",
            "Diagnóstico por síntomas: qué tocar en cada caso",
        ],
        duration="6 h",
        notes=(
            "El módulo más técnico y el que más practica requiere. Conviene "
            "alternar teoría con ejercicios en el banco.\n\n"
            "Advertencia pedagógica: la sintonización no es un procedimiento cerrado "
            "sino un compromiso entre rapidez, precisión y estabilidad. El alumno "
            "debe salir sabiendo qué está negociando en cada momento."
        ),
    )

    _diagrama_respuesta(d)

    d.bullets_slide(
        "Los criterios: qué es un eje bien sintonizado",
        [
            "#Los cuatro indicadores objetivos",
            "**Error de seguimiento** durante el movimiento (`Un008`): cuánto se "
            "retrasa la posición real respecto a la consigna. Depende sobre todo de "
            "`Pn102` y de la prealimentación.",
            "**Tiempo de estabilización**: cuánto tarda el eje en entrar en la "
            "ventana de posicionado y quedarse dentro.",
            "**Sobrepasamiento (overshoot)**: cuánto se pasa del destino antes de "
            "volver. En muchas aplicaciones debe ser prácticamente nulo.",
            "**Rigidez en parado**: cuánto se desvía el eje al aplicarle una "
            "perturbación externa, y cuánto tarda en recuperar.",
            "",
            "#El compromiso que hay que negociar",
            "Subir ganancias → más rapidez y más rigidez, pero **menos margen de "
            "estabilidad**: ruido audible, vibración y, en el límite, oscilación.",
            "Bajar ganancias → más suavidad y silencio, pero **más error de "
            "seguimiento** y ciclos más lentos.",
            "- No existe un ajuste 'correcto' universal: una rectificadora y una "
            "paletizadora piden cosas opuestas.",
            "",
            "#Cómo se mide en la práctica",
            "Con la **traza de SigmaWin+**: consigna, posición real, error, velocidad "
            "y par en la misma captura y con la misma base de tiempos.",
            "- Guarda las capturas de antes y después: son la prueba objetiva de la "
            "mejora y la referencia para el futuro.",
        ],
        subtitle="Sin criterio de medida no hay ajuste, sólo opinión",
        callout=(
            "blue",
            "Pregunta que hay que hacerse antes de empezar",
            "¿Qué necesita esta máquina: precisión final, velocidad de ciclo o "
            "suavidad? El ajuste óptimo es distinto en cada caso, y conviene "
            "acordarlo con el responsable del proceso antes de tocar nada.",
        ),
        notes=(
            "Ejemplos que aclaran el compromiso:\n"
            "· Máquina de corte por láser: prioridad al error de seguimiento durante "
            "la trayectoria; un error de contorno estropea la pieza.\n"
            "· Paletizadora: prioridad al tiempo de ciclo y a la suavidad; da igual "
            "un error de 0,5 mm durante el movimiento.\n"
            "· Rectificadora: prioridad a la estabilidad y al acabado; una vibración "
            "de alta frecuencia deja marcas en la pieza.\n\n"
            "El indicador de rigidez en parado se comprueba de forma muy visual: "
            "empujando el eje a mano (cuando es seguro hacerlo) y observando cuánto "
            "cede y cómo vuelve."
        ),
    )

    d.cards_slide(
        "Las herramientas de ajuste de la Σ-7",
        [
            Card(
                "Ajuste sin sintonizar (tuning-less)",
                "`Pn170`. Activo de fábrica.\n"
                "El drive se adapta solo a la carga sin necesidad de conocer la "
                "inercia.\n"
                "**Ventaja**: el eje funciona razonablemente nada más arrancar.\n"
                "**Límite**: no alcanza las prestaciones de un ajuste específico. "
                "Hay que desactivarlo al pasar a ajuste manual.",
                "green",
            ),
            Card(
                "Autoajuste avanzado (`Fn201`)",
                "El drive mueve el eje él mismo con un patrón interno, mide la "
                "inercia y calcula ganancias y filtros.\n"
                "**Ventaja**: rápido y sorprendentemente bueno.\n"
                "**Requisito**: espacio de movimiento libre y carga real acoplada.",
                "blue",
            ),
            Card(
                "Autoajuste con referencia (`Fn202`)",
                "Igual que el anterior, pero usando el **movimiento real** que envía "
                "el controlador.\n"
                "**Ventaja**: ajusta para el ciclo que la máquina hace de verdad.\n"
                "**Uso**: cuando no hay recorrido libre para el patrón interno.",
                "cyan",
            ),
            Card(
                "Ajuste de un parámetro (`Fn203`)",
                "Un único mando de 'rigidez' que escala todas las ganancias de forma "
                "coordinada.\n"
                "**Ventaja**: muy intuitivo para afinar después del autoajuste.\n"
                "**Uso típico**: subir rigidez hasta que aparece ruido y retroceder "
                "un escalón.",
                "amber",
            ),
            Card(
                "Ajuste manual",
                "Control total sobre `Pn103`, `Pn100`, `Pn101`, `Pn102` y `Pn401`.\n"
                "**Ventaja**: es la única vía para exprimir un eje difícil.\n"
                "**Requisito**: entender el orden de ajuste y disponer de traza para "
                "medir.",
                "gray",
            ),
            Card(
                "Herramientas complementarias",
                "· `Fn206` análisis en frecuencia para localizar resonancias.\n"
                "· `Fn205` supresión de vibración de baja frecuencia.\n"
                "· `Fn204` ajuste de antirresonancia.\n"
                "· Filtros notch (`Pn409`) y control por modelo (`Pn140`).",
                "red",
            ),
        ],
        subtitle="Seis niveles, del automático total al control absoluto",
        columns=3,
        body_size=10.5,
        notes=(
            "Establezca la estrategia recomendada:\n"
            "1) Empiece por el autoajuste avanzado con la carga real.\n"
            "2) Afine con el ajuste de un parámetro hasta el límite de ruido.\n"
            "3) Sólo si no basta, pase a manual y a filtros.\n\n"
            "El error típico del principiante es ir directo al ajuste manual "
            "'porque es más profesional'. El autoajuste de la Σ-7 es muy bueno y deja "
            "un punto de partida difícil de mejorar a mano en poco tiempo.\n\n"
            "El error típico del experimentado es dejar activo el tuning-less mientras "
            "intenta ajustar a mano y no entender por qué sus cambios 'no hacen "
            "nada'."
        ),
    )

    d.steps_slide(
        "Procedimiento de autoajuste avanzado (`Fn201`)",
        [
            ("Preparar el eje",
             "Carga real acoplada, recorrido libre y suficiente, finales de carrera "
             "operativos y zona despejada. Guarda antes el fichero de parámetros."),
            ("Elegir el modo de ajuste",
             "El asistente pregunta si se quiere ajustar sólo la ganancia, también "
             "los filtros de resonancia o además la supresión de vibración."),
            ("Indicar el tipo de mecánica",
             "Correa, husillo o accionamiento directo. El drive usa este dato para "
             "elegir un punto de partida razonable."),
            ("Definir la amplitud del movimiento de prueba",
             "El drive moverá el eje varias vueltas en ambos sentidos. Comprueba que "
             "cabe en el recorrido disponible."),
            ("Ejecutar y observar",
             "El eje se mueve solo, con ruido y vibración perceptibles: es normal, "
             "el drive está explorando el límite de estabilidad."),
            ("Revisar los resultados",
             "El asistente propone `Pn103` (inercia medida), ganancias y filtros. "
             "Anota especialmente la relación de inercias: valida tu cálculo."),
            ("Aceptar, guardar y verificar con el ciclo real",
             "Ejecuta el ciclo de producción y captura la traza. Compara con la "
             "situación anterior."),
        ],
        subtitle="Diez minutos que suelen dar el 90 % del resultado",
        callout=(
            "red",
            "Precauciones antes de lanzar un autoajuste",
            "El eje se moverá de forma autónoma y con vibración deliberada. Nunca lo "
            "ejecutes en un eje vertical sin freno verificado, ni en una máquina con "
            "personas cerca, ni con recorrido insuficiente.",
        ),
        notes=(
            "Comente qué hace realmente el autoajuste: excita el sistema, mide la "
            "respuesta, estima la inercia y sube la ganancia hasta detectar el "
            "principio de inestabilidad; después retrocede con un margen de "
            "seguridad y coloca filtros notch en las resonancias detectadas.\n\n"
            "Por eso hace ruido: está buscando el límite a propósito.\n\n"
            "El dato más valioso que devuelve es Pn103, la relación de inercias "
            "medida. Compárela con la calculada en el Módulo 04: si difieren mucho, "
            "alguna hipótesis del cálculo era falsa y conviene averiguar cuál."
        ),
    )

    d.steps_slide(
        "Ajuste manual: el orden es innegociable",
        [
            ("Desactivar el ajuste automático",
             "`Pn170` (tuning-less) debe estar desactivado; si no, tus cambios "
             "quedarán enmascarados por la adaptación automática."),
            ("Fijar la relación de inercias `Pn103`",
             "Con el valor medido por el autoajuste o el calculado. **Todo lo demás "
             "se escala con este número**: si está mal, nada funcionará bien."),
            ("Ajustar la ganancia del lazo de velocidad `Pn100`",
             "Súbela progresivamente hasta que aparezca ruido o vibración; después "
             "retrocede entre un 10 y un 20 %."),
            ("Ajustar la integral de velocidad `Pn101`",
             "Bájala para eliminar el error en régimen y ganar rigidez. Demasiado "
             "baja produce oscilación lenta y sobrepasamiento."),
            ("Ajustar la ganancia de posición `Pn102`",
             "Súbela hasta reducir el error de seguimiento a lo necesario. Regla "
             "práctica: debe quedar claramente por debajo de la del lazo de "
             "velocidad."),
            ("Ajustar el filtro de par `Pn401`",
             "Súbelo un poco si hay ruido de alta frecuencia; pero cada milisegundo "
             "de filtro resta rapidez al lazo."),
            ("Verificar con la traza y guardar",
             "Captura el ciclo real, comprueba error y sobrepasamiento, y guarda la "
             "configuración con fecha."),
        ],
        subtitle="De dentro hacia fuera: inercia → velocidad → posición → filtros",
        callout=(
            "amber",
            "Por qué el orden importa tanto",
            "El lazo de posición se apoya en el de velocidad. Subir `Pn102` con un "
            "lazo de velocidad mal ajustado sólo produce inestabilidad, y llevará a "
            "la conclusión equivocada de que 'el eje no da más'.",
        ),
        notes=(
            "Explique la relación entre los lazos: el lazo de velocidad debe ser "
            "sensiblemente más rápido que el de posición (una regla habitual es un "
            "factor de 4 a 5 entre sus anchos de banda). Si se violenta esa "
            "relación, el sistema oscila.\n\n"
            "Método práctico para Pn100: subir en escalones del 20 %, y en cada "
            "escalón hacer un movimiento corto y escuchar. El oído humano detecta el "
            "principio de inestabilidad antes que muchos instrumentos.\n\n"
            "Un detalle sobre Pn401: es tentador subirlo para 'silenciar' el eje, "
            "pero el filtro introduce retardo en el lazo más interno, que es "
            "exactamente donde menos se puede permitir. Si hay ruido de alta "
            "frecuencia, casi siempre es mejor un filtro notch bien colocado que un "
            "filtro de par alto."
        ),
    )

    _diagrama_resonancia(d)

    d.two_col_slide(
        "Vibración de baja frecuencia y control por modelo",
        (
            "Vibración de baja frecuencia (estructura)",
            [
                "Síntoma: el eje llega al destino y la **máquina entera oscila** "
                "durante unas décimas de segundo antes de quedarse quieta.",
                "Causa: la estructura (pórtico, brazo, torre) tiene una frecuencia "
                "propia baja, típicamente entre 1 y 100 Hz, que el movimiento excita.",
                "#Solución en el drive",
                "- Función de supresión de vibración (`Fn205`) y parámetro de "
                "frecuencia `Pn14A`.",
                "- El drive conforma la consigna para no excitar esa frecuencia.",
                "#Solución mecánica",
                "- Rigidizar la estructura o usar perfiles de movimiento en S que "
                "limiten el 'jerk'.",
            ],
        ),
        (
            "Control por modelo de referencia (`Pn140`)",
            [
                "El drive calcula internamente cómo **debería** moverse el eje ideal "
                "y usa ese modelo para anticipar el mando.",
                "Permite **reducir mucho el error de seguimiento sin subir las "
                "ganancias** del lazo de realimentación, que son las que provocan "
                "inestabilidad.",
                "Es la razón principal de que un eje Σ-7 bien configurado posicione "
                "más rápido que uno de generación anterior con las mismas ganancias.",
                "#Cuándo usarlo",
                "- En posicionado punto a punto: muy recomendable.",
                "- En interpolación con varios ejes: hay que verificar que **todos** "
                "los ejes se comportan igual, o aparecerán errores de contorno.",
            ],
        ),
        subtitle="Dos herramientas que resuelven problemas que las ganancias no pueden",
        tones=("amber", "blue"),
        callout=(
            "green",
            "Cómo identificar la frecuencia de la vibración",
            "Con la traza de SigmaWin+: captura la señal de par o de velocidad al "
            "final del posicionado, mide el periodo de la oscilación y calcula su "
            "inversa. Ese es el número que hay que introducir.",
        ),
        notes=(
            "La distinción clave para el alumno: resonancia de alta frecuencia "
            "(cientos o miles de hercios, ruido agudo, se resuelve con notch) frente "
            "a vibración de baja frecuencia (unos pocos hercios, se ve a simple "
            "vista, se resuelve con supresión de vibración o rigidizando).\n\n"
            "Sobre el control por modelo en interpolación: es un punto fino. Si un "
            "eje tiene MFC y otro no, sus respuestas dinámicas difieren y la "
            "trayectoria resultante se deforma en las esquinas. En máquinas de "
            "contorneado hay que configurar todos los ejes de forma homogénea."
        ),
    )

    d.table_slide(
        "Diagnóstico por síntomas: qué tocar en cada caso",
        ["Síntoma observado", "Causa más probable", "Qué hacer"],
        [
            ["Zumbido agudo continuo con el eje parado",
             "Ganancia de velocidad demasiado alta o resonancia mecánica",
             "Bajar `Pn100`; si persiste, buscar la frecuencia con `Fn206` y poner "
             "notch"],
            ["El eje oscila lentamente al llegar al destino",
             "Integral demasiado agresiva o relación de inercias mal ajustada",
             "Revisar `Pn103`; subir `Pn101`"],
            ["Sobrepasamiento del destino",
             "Ganancia de posición alta respecto a la de velocidad",
             "Bajar `Pn102` o subir `Pn100`; activar control por modelo `Pn140`"],
            ["Error de seguimiento grande durante el movimiento",
             "Ganancia de posición baja o falta de prealimentación",
             "Subir `Pn102`; activar `Pn140`"],
            ["El eje 'tiembla' a muy baja velocidad",
             "Fricción de arranque (stick-slip) o ganancia insuficiente",
             "Compensación de fricción; revisar mecánica y lubricación"],
            ["Toda la máquina oscila tras el posicionado",
             "Vibración de baja frecuencia de la estructura",
             "`Fn205` / `Pn14A`; considerar perfil en S"],
            ["Ruido que aparece sólo con carga acoplada",
             "Resonancia del conjunto acoplamiento-carga",
             "Filtro notch; valorar acoplamiento más rígido"],
            ["El comportamiento cambia según la posición del eje",
             "Rigidez variable del conjunto mecánico",
             "Conmutación de ganancias; ajustar para el caso más desfavorable"],
            ["El eje empeora con los meses",
             "Desgaste, holgura o lubricación deficiente",
             "Revisión mecánica **antes** de retocar ganancias"],
        ],
        [3.5, 3.9, 4.7],
        subtitle="La tabla que hay que llevar encima al ajustar un eje",
        size=9.5,
        notes=(
            "La última fila merece énfasis: cuando un eje que iba bien empieza a ir "
            "mal, la causa casi nunca está en el drive. Los parámetros no se cambian "
            "solos; la mecánica sí se desgasta.\n\n"
            "Ese es también el mejor argumento para guardar las trazas de la puesta "
            "en marcha: permiten comparar objetivamente el comportamiento de hoy con "
            "el de hace dos años y demostrar que algo ha cambiado en la máquina."
        ),
    )

    d.bullets_slide(
        "Errores frecuentes al sintonizar",
        [
            "#De método",
            "**Cambiar varios parámetros a la vez**: imposible saber qué ha "
            "funcionado.",
            "**Ajustar sin medir**: sin traza sólo hay impresiones subjetivas.",
            "**Ajustar en vacío** y suponer que valdrá con carga.",
            "**No guardar el punto de partida**: quedarse sin marcha atrás.",
            "",
            "#De concepto",
            "**Empezar por el lazo de posición** en lugar de por el de velocidad.",
            "**Olvidar `Pn103`**: con la relación de inercias mal puesta, ningún "
            "ajuste posterior es coherente.",
            "**Dejar activo el tuning-less** mientras se ajusta a mano.",
            "**Subir ganancias para tapar un problema mecánico**: el ruido "
            "desaparece un tiempo y el desgaste se acelera.",
            "",
            "#De criterio",
            "**Buscar el máximo de ganancia** en lugar del ajuste adecuado a la "
            "aplicación. Un eje al límite de estabilidad hoy será inestable cuando "
            "cambien la temperatura, la lubricación o la carga.",
            "- Deja siempre un **margen de estabilidad** razonable: la máquina tiene "
            "que funcionar en agosto y en enero, nueva y con dos años de uso.",
        ],
        subtitle="Lo que separa un ajuste que dura de uno que dura una semana",
        callout=(
            "blue",
            "El criterio del profesional",
            "Un eje bien sintonizado no es el más rápido posible: es el que cumple el "
            "ciclo con margen, sin ruido, sin desgaste anómalo y sin volver a dar "
            "problemas en dos años.",
        ),
        notes=(
            "Cierre el módulo con esta idea: el objetivo no es demostrar lo rápido "
            "que puede ir el eje, sino entregar una máquina que funcione de forma "
            "estable durante años.\n\n"
            "Comente el efecto de la temperatura: la viscosidad del lubricante cambia "
            "con la temperatura, y con ella la fricción y el amortiguamiento del "
            "sistema. Un ajuste hecho al límite con la máquina caliente puede oscilar "
            "en el primer arranque de un lunes de invierno. Por eso el margen del "
            "10-20 % no es opcional."
        ),
    )


# --------------------------------------------------------------------------
# Diagramas
# --------------------------------------------------------------------------

def _diagrama_respuesta(d: Deck) -> None:
    slide = d.canvas_slide(
        "Cómo se ve una sintonización buena y una mala",
        "Respuesta del eje ante un escalón de consigna",
        notes=(
            "Este diagrama es el vocabulario visual del módulo. Los alumnos deben "
            "aprender a clasificar de un vistazo la traza que ven en SigmaWin+.\n\n"
            "· Sobreamortiguado: llega tarde pero sin pasarse. Ganancia insuficiente. "
            "Seguro pero lento; en muchas aplicaciones industriales es un ajuste "
            "aceptable si el tiempo de ciclo lo permite.\n"
            "· Óptimo: llega rápido, con un sobrepasamiento mínimo o nulo, y se "
            "queda quieto. Es el objetivo.\n"
            "· Subamortiguado: se pasa y oscila varias veces antes de estabilizarse. "
            "Ganancia excesiva o mal repartida entre lazos. Aunque el tiempo hasta "
            "el primer cruce sea corto, el tiempo hasta estabilizar es mayor: es más "
            "lento en la práctica y castiga la mecánica.\n\n"
            "Insista en esto último, que es contraintuitivo: pasarse de ganancia no "
            "hace la máquina más rápida, la hace más lenta y más ruidosa."
        ),
    )

    casos = [
        ("SOBREAMORTIGUADO", GRAY, "Ganancia baja",
         "Llega tarde, sin pasarse.\nSeguro pero lento.", [0.0, 0.18, 0.42, 0.62,
                                                           0.76, 0.85, 0.91, 0.95,
                                                           0.97, 0.99, 1.0]),
        ("ÓPTIMO", GREEN, "Ganancia adecuada",
         "Rápido, sin apenas\nsobrepasamiento.", [0.0, 0.42, 0.78, 0.96, 1.02,
                                                  1.01, 1.0, 1.0, 1.0, 1.0, 1.0]),
        ("SUBAMORTIGUADO", RED, "Ganancia excesiva",
         "Se pasa y oscila.\nRuidoso y más lento.", [0.0, 0.62, 1.15, 1.28, 1.05,
                                                     0.86, 0.95, 1.06, 1.02, 0.98,
                                                     1.0]),
    ]

    w = Inches(3.85)
    gap = Inches(0.3)
    x = Inches(0.65)
    top = Inches(1.80)
    ph = Inches(2.55)

    for titulo, color, subt, desc, puntos in casos:
        d._rect(slide, x, top, w, Inches(3.90), fill=LIGHT, line=GRAY_LINE)
        d._rect(slide, x, top, w, Inches(0.44), fill=color)
        d._text(slide, x, top + Inches(0.10), w, Inches(0.3), titulo,
                size=Pt(12), color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        d._text(slide, x, top + Inches(0.52), w, Inches(0.3), subt,
                size=Pt(10.5), color=color, bold=True, align=PP_ALIGN.CENTER)

        gx = x + Inches(0.45)
        gw = w - Inches(0.75)
        gy = top + Inches(3.62)
        gh = Inches(1.85)
        d.line(slide, gx, gy, gx + gw, gy, color=INK, width=Pt(1.1))
        d.line(slide, gx, gy, gx, gy - gh - Inches(0.15), color=INK,
               width=Pt(1.1))
        # consigna
        d.line(slide, gx, gy - gh * 0.72, gx + gw, gy - gh * 0.72, color=GRAY,
               width=Pt(1), dash=True)
        d.label(slide, gx + gw - Inches(0.95), gy - gh * 0.72 - Inches(0.26),
                Inches(0.95), "consigna", size=8, color=GRAY,
                align=PP_ALIGN.RIGHT)
        # respuesta
        n = len(puntos)
        paso = gw / (n - 1)
        for i in range(n - 1):
            d.line(slide, gx + paso * i, gy - gh * 0.72 * puntos[i],
                   gx + paso * (i + 1), gy - gh * 0.72 * puntos[i + 1],
                   color=color, width=Pt(2))

        d._text(slide, x + Inches(0.3), top + Inches(0.92), w - Inches(0.6),
                Inches(0.7), desc, size=Pt(10.5), color=GRAY,
                align=PP_ALIGN.CENTER, spacing=1.15)
        x += w + gap

    d.callout(slide, Inches(0.65), Inches(6.32), Inches(12.05), Inches(0.60),
              "amber", "Lo que hay que retener: pasarse de ganancia no acelera la "
              "máquina, la ralentiza.", "")


def _diagrama_resonancia(d: Deck) -> None:
    slide = d.canvas_slide(
        "Resonancia mecánica y filtros notch",
        "Cuando el problema no está en las ganancias sino en la mecánica",
        notes=(
            "Explique la física: motor, acoplamiento y carga forman un sistema "
            "masa-muelle-masa con una frecuencia de resonancia propia. Si el lazo de "
            "control tiene ganancia suficiente a esa frecuencia, el sistema oscila.\n\n"
            "Hay dos formas de resolverlo: bajar la ganancia (funciona, pero "
            "sacrifica prestaciones en todo el rango) o quitar ganancia sólo en esa "
            "frecuencia concreta. Eso último es exactamente lo que hace un filtro "
            "notch.\n\n"
            "Procedimiento: se localiza la frecuencia con la función de análisis "
            "(Fn206 / análisis mecánico de SigmaWin+), se introduce en Pn409, y se "
            "ajusta la anchura con el factor Q (Pn40A) y la profundidad (Pn40B). Un "
            "notch demasiado ancho resta prestaciones; demasiado estrecho no atrapa "
            "la resonancia si esta se desplaza con la posición o la temperatura.\n\n"
            "Hay dos filtros notch disponibles, lo que permite atacar dos "
            "resonancias distintas. El autoajuste avanzado los coloca "
            "automáticamente cuando detecta resonancia.\n\n"
            "Advertencia importante: el filtro notch enmascara el síntoma pero no "
            "arregla la mecánica. Si la resonancia procede de un acoplamiento flojo o "
            "de un rodamiento dañado, hay que repararlo."
        ),
    )

    # Gráfica de respuesta en frecuencia
    ox, oy = Inches(1.35), Inches(5.05)
    gw, gh = Inches(6.2), Inches(2.85)
    d.line(slide, ox, oy, ox + gw, oy, color=INK, width=Pt(1.35))
    d.line(slide, ox, oy, ox, oy - gh - Inches(0.2), color=INK, width=Pt(1.35))
    d.label(slide, ox, oy + Inches(0.14), gw, "Frecuencia  [Hz]  →", size=10.5,
            color=INK, bold=True)
    d.label(slide, Inches(0.2), oy - gh - Inches(0.52), Inches(2.8),
            "Ganancia  ↑", size=10.5, color=INK, bold=True, align=PP_ALIGN.LEFT)

    # Curva con pico de resonancia
    perfil = [0.30, 0.30, 0.31, 0.33, 0.38, 0.55, 0.92, 0.55, 0.36, 0.30, 0.26,
              0.22, 0.18]
    n = len(perfil)
    paso = gw / (n - 1)
    for i in range(n - 1):
        d.line(slide, ox + paso * i, oy - gh * perfil[i],
               ox + paso * (i + 1), oy - gh * perfil[i + 1], color=RED,
               width=Pt(2.25))
    d.label(slide, ox + paso * 6 - Inches(1.2), oy - gh * 0.92 - Inches(0.34),
            Inches(2.4), "pico de resonancia", size=9.5, color=RED, bold=True)

    # Curva corregida
    corregido = [0.30, 0.30, 0.31, 0.33, 0.36, 0.34, 0.12, 0.34, 0.34, 0.30,
                 0.26, 0.22, 0.18]
    for i in range(n - 1):
        d.line(slide, ox + paso * i, oy - gh * corregido[i],
               ox + paso * (i + 1), oy - gh * corregido[i + 1], color=GREEN,
               width=Pt(2.25), dash=True)
    d.label(slide, ox + paso * 6 - Inches(0.2), oy - gh * 0.12 + Inches(0.02),
            Inches(2.6), "con filtro notch", size=9.5, color=GREEN, bold=True,
            align=PP_ALIGN.LEFT)

    # Panel de procedimiento
    px = Inches(8.15)
    d._rect(slide, px, Inches(1.78), Inches(4.55), Inches(4.5), fill=LIGHT,
            line=GRAY_LINE)
    d._text(slide, px + Inches(0.28), Inches(1.96), Inches(4.0), Inches(0.35),
            "Procedimiento", size=Pt(14), color=NAVY, bold=True)
    tf = slide.shapes.add_textbox(px + Inches(0.28), Inches(2.42), Inches(4.0),
                                  Inches(3.7)).text_frame
    tf.word_wrap = True
    d._fill_bullets(tf, [
        "**Detectar**: ruido agudo constante, normalmente entre cientos de hercios "
        "y algunos kilohercios.",
        "**Medir**: análisis en frecuencia (`Fn206` o análisis mecánico de "
        "SigmaWin+) para localizar el pico.",
        "**Filtrar**: introducir la frecuencia en `Pn409` y habilitar el filtro con "
        "`Pn408`.",
        "**Afinar**: factor Q (`Pn40A`) y profundidad (`Pn40B`). Hay un segundo "
        "filtro disponible para otra resonancia.",
        "**Verificar**: volver a subir la ganancia y comprobar que el ruido no "
        "reaparece.",
    ], size=11)

    d.callout(slide, Inches(0.62), Inches(6.30), Inches(12.1), Inches(0.62),
              "red", "El filtro notch no repara la mecánica: enmascara el síntoma. "
              "Si la resonancia procede de un acoplamiento flojo, arréglalo.", "")
