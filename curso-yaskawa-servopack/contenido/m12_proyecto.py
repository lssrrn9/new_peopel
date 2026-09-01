"""Módulo 12 — Proyecto integrador."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, GRAY, GRAY_LINE, GREEN, INK, LIGHT,
                     LIGHT_BLUE, NAVY, RED, WHITE, Card, Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 12",
        "Proyecto integrador",
        [
            "Una máquina real de principio a fin",
            "Entregable 1: dimensionamiento justificado",
            "Entregable 2: arquitectura eléctrica y de control",
            "Entregable 3: hoja de parámetros",
            "Entregable 4: plan de puesta en marcha y criterios de aceptación",
            "Defensa y evaluación",
        ],
        duration="8 h (trabajo guiado)",
        notes=(
            "El proyecto integrador es la parte que consolida el aprendizaje. "
            "Idealmente se trabaja en grupos de dos o tres personas a lo largo del "
            "curso, entregando cada bloque al terminar el módulo correspondiente.\n\n"
            "Si el grupo tiene una máquina real en su planta, sustituya el enunciado "
            "por esa máquina: el valor formativo se multiplica."
        ),
    )

    d.two_col_slide(
        "El encargo",
        (
            "La máquina",
            [
                "Estación de **carga y descarga** en una línea de mecanizado.",
                "Un **eje horizontal** con husillo de bolas mueve un carro con la "
                "pieza entre la posición de carga y la de mecanizado.",
                "El eje debe **sincronizarse** con el PLC de la línea y detenerse en "
                "posiciones repetibles.",
                "La línea trabaja a **tres turnos**, en una nave sin climatizar.",
                "#Datos mecánicos",
                "- Masa del carro más pieza: **400 kg** (pieza de hasta 120 kg).",
                "- Husillo de bolas: **40 mm de diámetro, 1,5 m, paso 20 mm**.",
                "- Guías lineales, coeficiente de rozamiento **0,05**.",
                "- Rendimiento del conjunto: **0,90**.",
            ],
        ),
        (
            "Los requisitos",
            [
                "**Recorrido útil**: 600 mm entre posiciones.",
                "**Tiempo de movimiento**: 1,0 s como máximo.",
                "**Tiempo de ciclo**: 2,5 s (movimiento + espera de proceso).",
                "**Repetibilidad de posición**: ±0,05 mm.",
                "**Sin búsqueda de origen** al arrancar tras un corte.",
                "**Parada segura** integrada en la cadena de seguridad de la línea.",
                "**Diagnóstico remoto** desde el sistema de supervisión de planta.",
                "#Restricciones",
                "- Armario existente con espacio limitado.",
                "- Red trifásica de 200 V con caídas ocasionales del 10 %.",
            ],
        ),
        subtitle="Lee el enunciado dos veces: la mitad de los errores nacen aquí",
        tones=("blue", "amber"),
        callout=(
            "green",
            "Primera tarea antes de calcular nada",
            "Traduce cada requisito a una decisión técnica. Por ejemplo: «sin "
            "búsqueda de origen» → encoder absoluto con batería y `Fn008`; "
            "«diagnóstico remoto» → interfaz de bus; «caídas del 10 %» → verificar la "
            "curva par-velocidad a tensión mínima.",
        ),
        notes=(
            "El ejercicio de traducir requisitos a decisiones técnicas es el más "
            "valioso del proyecto. Hágalo en común en la pizarra antes de que los "
            "grupos empiecen a calcular.\n\n"
            "Requisitos y sus consecuencias:\n"
            "· Repetibilidad ±0,05 mm → mecánica de precisión, ventana Pn522 "
            "coherente y sintonización cuidada.\n"
            "· Tres turnos en nave sin climatizar → margen térmico amplio, "
            "verificación de par RMS con holgura y atención a la condensación.\n"
            "· Parada segura → CN8 cableado y validado, no puenteado.\n"
            "· Caídas de red del 10 % → comprobar la curva a tensión mínima y "
            "considerar la alarma A.410."
        ),
    )

    d.table_slide(
        "Entregable 1 — Dimensionamiento",
        ["Apartado", "Qué debe contener", "Criterio de evaluación"],
        [
            ["Datos de partida",
             "Tabla con los once datos del Módulo 04 y las hipótesis asumidas",
             "Ninguna cifra sin origen documentado"],
            ["Perfil de movimiento",
             "Velocidad máxima, aceleración, velocidad del motor y aceleración "
             "angular", "Coherencia con el tiempo de ciclo exigido"],
            ["Inercias",
             "Carga, husillo, acoplamiento y total, con las fórmulas empleadas",
             "Todas las contribuciones consideradas"],
            ["Relación de inercias",
             "Valor obtenido y valoración de si es adecuada",
             "Justificación de la elección del motor"],
            ["Pares del ciclo",
             "Aceleración, régimen constante, deceleración y par RMS",
             "Aplicación correcta del rendimiento y de la fricción"],
            ["Verificación",
             "Comparación con la curva del motor y márgenes obtenidos",
             "Margen mínimo del 20 % en continuo y en pico"],
            ["Regeneración",
             "Energía por frenado, potencia media y decisión sobre resistencia "
             "externa", "Conclusión razonada"],
            ["Selección final",
             "Modelo de SERVOPACK y de motor propuestos, con alternativa valorada",
             "Combinación homologada y coherente con los requisitos"],
        ],
        [2.4, 5.6, 4.1],
        subtitle="Al terminar el Módulo 04",
        size=9.5,
        notes=(
            "Insista en el criterio 'ninguna cifra sin origen documentado'. En "
            "ingeniería, un número sin trazabilidad es una opinión.\n\n"
            "Valore especialmente la alternativa: pedir que comparen SGMXA-30A "
            "(3.000 rpm) con SGMXG-30A (1.500 rpm) obliga a razonar sobre par, "
            "velocidad e inercia en lugar de aplicar una receta."
        ),
    )

    d.table_slide(
        "Entregable 2 — Arquitectura eléctrica y de control",
        ["Apartado", "Qué debe contener", "Criterio de evaluación"],
        [
            ["Esquema unifilar de potencia",
             "Protección, contactor, filtro, amplificador, motor y resistencia de "
             "regeneración", "Alimentación de control tomada antes del contactor"],
            ["Selección de componentes",
             "Protecciones, secciones de cable, contactor, filtro y fuente de 24 V",
             "Coherencia con los 21 A de entrada y los 18,5 A de salida"],
            ["Plan de tierras y apantallamiento",
             "Punto de estrella, conexión de mallas y separación de canalizaciones",
             "Malla a tierra en ambos extremos con abrazadera de 360°"],
            ["Arquitectura de control",
             "Elección de interfaz (bus o analógica/pulsos) con justificación",
             "Debe satisfacer el requisito de diagnóstico remoto"],
            ["Esquema de `CN1`",
             "Señales de entrada y salida elegidas y su asignación",
             "Incluye `ALM`, `/COIN`, `/S-RDY` y finales de carrera"],
            ["Cadena de seguridad",
             "Cableado de `CN8`, módulo de seguridad y vigilancia EDM",
             "Dos canales independientes y EDM conectada"],
            ["Balance térmico del armario",
             "Pérdidas estimadas y medio de evacuación de calor",
             "Considera el escenario de verano en nave sin climatizar"],
        ],
        [2.6, 5.4, 4.1],
        subtitle="Al terminar los Módulos 05, 06 y 10",
        size=9.5,
        notes=(
            "Este entregable es el más 'de oficina técnica'. Si el grupo no tiene "
            "experiencia en esquemas, acepte croquis a mano alzada: lo importante es "
            "el razonamiento, no la herramienta de dibujo.\n\n"
            "Punto de discusión interesante: el requisito de diagnóstico remoto "
            "empuja hacia una variante de bus, lo que a su vez simplifica el cableado "
            "de CN1. Es un buen ejemplo de cómo un requisito aparentemente menor "
            "cambia la arquitectura completa."
        ),
    )

    d.table_slide(
        "Entregable 3 — Hoja de parámetros del eje",
        ["Parámetro", "Valor propuesto", "Justificación exigida"],
        [
            ["`Pn000.0` sentido de giro", "A determinar en la puesta en marcha",
             "Coherente con el sentido positivo definido en el plano"],
            ["`Pn000.1` modo de control", "Según la arquitectura elegida",
             "Debe corresponder con la interfaz seleccionada"],
            ["`Pn001.0` método de parada", "A justificar",
             "Eje horizontal: valorar freno dinámico frente a rampa"],
            ["`Pn20E` / `Pn210` engranaje", "Calculado para 1 µm por unidad",
             "Cálculo completo y fracción simplificada"],
            ["`Pn522` ventana de posicionado", "A determinar",
             "Coherente con la repetibilidad exigida de ±0,05 mm"],
            ["`Pn520` error de posición máximo", "A determinar",
             "Debe detener el eje antes de dañar la mecánica"],
            ["`Pn103` relación de inercias", "Del cálculo, a confirmar con "
             "autoajuste", "Comparación entre valor calculado y medido"],
            ["`Pn100` / `Pn101` / `Pn102`", "Resultado del autoajuste y afinado",
             "Capturas de traza antes y después"],
            ["`Pn600` capacidad de regeneración", "Según la decisión del "
             "entregable 1", "Coherente con la resistencia instalada"],
            ["`Pn304` velocidad de JOG", "50-100 rpm",
             "Velocidad segura para las primeras pruebas"],
        ],
        [3.2, 3.7, 5.2],
        subtitle="Al terminar los Módulos 07 y 09",
        size=9.5,
        foot="Entrega además el fichero exportado de SigmaWin+ (o la tabla completa "
             "de parámetros modificados respecto a fábrica).",
        notes=(
            "El detalle más formativo de este entregable es la comparación entre la "
            "relación de inercias calculada y la medida por el autoajuste. Es el "
            "momento en que la teoría se enfrenta a la realidad.\n\n"
            "Pn522 exige un razonamiento fino: la repetibilidad de ±0,05 mm es una "
            "característica del sistema mecánico completo, mientras que Pn522 es la "
            "ventana que declara 'posición alcanzada'. No son lo mismo, y conviene "
            "que lo discutan."
        ),
    )

    d.steps_slide(
        "Entregable 4 — Plan de puesta en marcha y aceptación",
        [
            ("Procedimiento por fases",
             "Las seis fases del Módulo 08 adaptadas a esta máquina, con "
             "responsables y comprobaciones concretas en cada una."),
            ("Lista de verificación previa firmada",
             "La del Módulo 05, adaptada al armario y a la mecánica de la estación."),
            ("Protocolo de pruebas de seguridad",
             "Finales de carrera, HWBB con vigilancia EDM y medida del tiempo real "
             "de parada del eje."),
            ("Criterios de aceptación medibles",
             "Tiempo de ciclo ≤ 2,5 s · repetibilidad ≤ ±0,05 mm · par RMS ≤ 80 % "
             "del nominal · temperatura estabilizada tras dos horas de "
             "producción."),
            ("Registro de resultados",
             "Trazas de SigmaWin+ del ciclo real, valores de `Un002` y `Un008`, y "
             "temperaturas medidas."),
            ("Documentación de entrega",
             "Acta del eje, ficheros de parámetros, esquemas actualizados y plan de "
             "mantenimiento preventivo."),
        ],
        subtitle="Al terminar los Módulos 08 y 11",
        callout=(
            "blue",
            "Qué se valora en la defensa del proyecto",
            "No la elegancia del documento, sino la **trazabilidad del "
            "razonamiento**: que cada decisión pueda justificarse con un dato, un "
            "cálculo o un requisito del enunciado.",
        ),
        notes=(
            "Los criterios de aceptación medibles son la parte más profesional del "
            "proyecto: convierten 'la máquina va bien' en algo verificable y "
            "contractual.\n\n"
            "Si el curso se imparte en varias sesiones, dedique la última a la "
            "defensa de los proyectos. Escuchar cómo otro grupo ha resuelto el mismo "
            "enunciado de forma distinta es enormemente formativo."
        ),
    )

    d.table_slide(
        "Rúbrica de evaluación del proyecto",
        ["Criterio", "Peso", "Qué se espera de un trabajo excelente"],
        [
            ["Dimensionamiento", "25 %",
             "Cálculo completo, hipótesis explícitas, márgenes justificados y "
             "alternativa valorada"],
            ["Arquitectura eléctrica", "20 %",
             "Esquema coherente, protecciones dimensionadas, EMC y tierras "
             "correctamente resueltas"],
            ["Configuración y parámetros", "20 %",
             "Engranaje electrónico verificado, asignación de E/S documentada, "
             "sintonización razonada con trazas"],
            ["Seguridad", "15 %",
             "HWBB correctamente integrado y validado; análisis de las limitaciones "
             "de STO en esta máquina"],
            ["Puesta en marcha y aceptación", "10 %",
             "Procedimiento por fases con criterios medibles y registro de "
             "resultados"],
            ["Documentación y defensa", "10 %",
             "Trazabilidad de las decisiones y claridad al explicarlas"],
        ],
        [3.0, 1.2, 7.9],
        subtitle="Transparencia en la evaluación desde el primer día",
        size=10.5,
        align_center=(1,),
        notes=(
            "Reparta la rúbrica al inicio del curso, no al final. Saber cómo se "
            "evalúa orienta el esfuerzo y mejora mucho la calidad de los "
            "entregables.\n\n"
            "El peso del dimensionamiento (25 %) es deliberado: es la parte con más "
            "contenido de ingeniería y la que más diferencia a un técnico "
            "competente."
        ),
    )
