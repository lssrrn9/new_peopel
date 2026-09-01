"""Módulo 11 — Diagnóstico, alarmas y mantenimiento."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, GRAY, GRAY_LINE, GREEN, INK, LIGHT,
                     LIGHT_BLUE, NAVY, RED, WHITE, Card, Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 11",
        "Diagnóstico, alarmas y mantenimiento",
        [
            "Un método de diagnóstico que funciona siempre",
            "Alarmas y avisos: cómo leerlos, cómo reiniciarlos",
            "Las alarmas que verás de verdad, ordenadas por familia",
            "Árboles de decisión para los tres fallos más frecuentes",
            "Mantenimiento preventivo y vida útil de los componentes",
            "Sustitución de equipo sin perder un día de producción",
        ],
        duration="4 h",
        notes=(
            "Módulo orientado a mantenimiento. El objetivo es reducir el tiempo "
            "medio de reparación, y eso se consigue con método, no con memoria.\n\n"
            "Si el grupo es de mantenimiento, este es probablemente el módulo que "
            "más van a usar. Dedique tiempo a los árboles de decisión y practique "
            "con averías simuladas si dispone de banco."
        ),
    )

    _diagrama_metodo(d)

    d.two_col_slide(
        "Alarmas y avisos: cómo se comportan",
        (
            "Alarma (`A.___`)",
            [
                "El drive **desactiva el par** y detiene el eje según el método "
                "configurado en `Pn001`.",
                "Se activa la salida `ALM`, que normalmente corta el contactor y "
                "avisa al PLC.",
                "Queda registrada en el **historial de alarmas** (`Fn000`), con las "
                "últimas ocurrencias.",
                "#Cómo se reinicia",
                "- Con `/ALM-RST` o desde el panel/SigmaWin+, **después** de eliminar "
                "la causa.",
                "- Algunas alarmas graves exigen **ciclo completo de alimentación** "
                "(no basta el reset).",
                "- Si la alarma vuelve inmediatamente, la causa sigue presente: no "
                "insistas con el reset.",
            ],
        ),
        (
            "Aviso (`A.9__`)",
            [
                "El eje **sigue funcionando**: es una advertencia anticipada.",
                "Se puede señalizar con la salida `/WARN` hacia el PLC.",
                "#Ejemplos típicos",
                "- Aviso de sobrecarga: el modelo térmico se acerca al límite.",
                "- Aviso de batería del encoder: quedan semanas de margen.",
                "- Aviso de regeneración: la resistencia se está calentando.",
                "- Aviso de cambio de parámetro pendiente de reinicio.",
                "#Por qué importan",
                "Un aviso es una **oportunidad de intervenir con la máquina "
                "parada por producción** en lugar de sufrir una parada no "
                "planificada.",
            ],
        ),
        subtitle="La diferencia entre reaccionar y anticiparse",
        tones=("red", "amber"),
        callout=(
            "green",
            "Recomendación de integración",
            "Cablea o mapea la señal de aviso (`/WARN`) hacia el PLC y muéstrala en "
            "el HMI. La mayoría de las instalaciones ignoran los avisos, y son "
            "exactamente la información que evita las paradas.",
        ),
        notes=(
            "Insista en el valor de los avisos: el drive dispone de un modelo térmico "
            "que sabe cuánto margen de sobrecarga queda. Esa información, llevada al "
            "HMI, permite planificar.\n\n"
            "Sobre el historial de alarmas: es la primera herramienta a consultar en "
            "cualquier avería. Muchas veces la alarma que ve el operario es "
            "consecuencia de otra anterior, y sólo el historial lo revela.\n\n"
            "Advertencia sobre el reset compulsivo: reiniciar una alarma de "
            "sobrecarga sin resolver la causa térmica es una manera eficaz de "
            "destruir un motor."
        ),
    )

    d.table_slide(
        "Alarmas frecuentes (1/2): potencia, sobrecarga y movimiento",
        ["Familia", "Significado", "Causas habituales", "Primeras "
         "comprobaciones"],
        [
            ["`A.1__`", "Sobrecorriente / fallo de la etapa de potencia",
             "Cortocircuito en el cable o en el motor, fases mal conectadas, "
             "amplificador dañado",
             "Medir aislamiento y continuidad del motor con el cable "
             "desconectado"],
            ["`A.3__`", "Fallo de regeneración",
             "Resistencia desconectada, puente `B2`-`B3` retirado por error, "
             "`Pn600` mal declarado",
             "Verificar el cableado de `B1`/`B2`/`B3` y el valor de `Pn600`"],
            ["`A.400`", "Sobretensión del bus de continua",
             "Frenado demasiado enérgico, regeneración insuficiente, tensión de red "
             "alta", "Medir la red; revisar el cálculo de regeneración"],
            ["`A.410`", "Subtensión del bus de continua",
             "Caída de red, falta de fase, servo ON demasiado pronto tras energizar",
             "Medir tensión entre fases; revisar la secuencia de arranque"],
            ["`A.51_`", "Sobrevelocidad",
             "Fases del motor intercambiadas, consigna errónea, engranaje electrónico "
             "mal calculado", "Comprobar `U` `V` `W` y el engranaje"],
            ["`A.7__`", "Sobrecarga (instantánea o continua)",
             "Dimensionamiento insuficiente, fricción excesiva, freno sin liberar, "
             "colisión", "Medir el par real con `Un002` y comparar con el cálculo"],
            ["`A.7A_`", "Sobretemperatura del disipador",
             "Ventilador parado, filtros del armario obstruidos, temperatura "
             "ambiente alta", "Comprobar ventilador y ventilación del armario"],
            ["`A.d__`", "Exceso de error de posición",
             "El eje no puede seguir la consigna: atasco, ganancia insuficiente o "
             "aceleración excesiva",
             "Revisar mecánica primero; después sintonización"],
        ],
        [1.2, 2.9, 4.2, 3.8],
        subtitle="Los prefijos indican la familia: identifícala antes de buscar el "
                 "código exacto",
        size=9.0,
        foot="Los códigos concretos y su comportamiento están en el capítulo de "
             "resolución de problemas del manual: tenlo siempre a mano en el "
             "portátil o en el móvil.",
        notes=(
            "Enseñe a razonar por familias en lugar de memorizar códigos. Con el "
            "prefijo ya se sabe si el problema es de potencia, térmico, de "
            "seguimiento o del encoder.\n\n"
            "A.7__ (sobrecarga) es la alarma que más aparece en producción y casi "
            "siempre tiene causa mecánica: guías secas, rodamiento agarrotado, freno "
            "que no libera del todo, o producto atascado. Antes de tocar el drive, "
            "compruebe el par con Un002 y compare con el histórico.\n\n"
            "A.d__ (error de posición) merece una regla: nunca se resuelve subiendo "
            "el umbral Pn520. Eso es apagar la alarma de incendios."
        ),
    )

    d.table_slide(
        "Alarmas frecuentes (2/2): encoder, parámetros y comunicación",
        ["Familia", "Significado", "Causas habituales", "Primeras comprobaciones"],
        [
            ["`A.0__`", "Error de parámetros o de memoria interna",
             "Escritura interrumpida, memoria degradada, combinación no válida",
             "Recargar la copia de parámetros; si persiste, el equipo puede estar "
             "dañado"],
            ["`A.05_`", "Combinación motor-amplificador no admitida",
             "Motor de capacidad o tipo incompatible con el amplificador",
             "Verificar códigos completos de ambos equipos"],
            ["`A.81_` / `A.82_`", "Fallo de respaldo o de suma de verificación del "
             "encoder absoluto",
             "Batería agotada con el equipo sin tensión, cable de encoder "
             "desconectado",
             "Sustituir batería, ejecutar `Fn008` y **rehacer el origen**"],
            ["`A.83_`", "Aviso o alarma de batería del encoder",
             "Batería próxima al final de su vida",
             "Sustituir **con la alimentación de control conectada**"],
            ["`A.84_`", "Datos del encoder erróneos",
             "Ruido eléctrico, cable dañado, apantallamiento deficiente",
             "Revisar apantallamiento, separación de cables y estado del conector"],
            ["`A.C__`", "Error de comunicación con el encoder",
             "Cable de encoder defectuoso, conector flojo, interferencias",
             "Sustituir el cable por uno original y revisar tierras"],
            ["`A.E__`", "Error de comunicación de bus (MECHATROLINK / EtherCAT)",
             "Cable de red, configuración del maestro, ciclo mal ajustado",
             "Contadores de error por puerto; sustituir latiguillo"],
            ["`A.F__`", "Falta de fase en la alimentación principal",
             "Fusible fundido, contactor con un polo pegado, cable suelto",
             "Medir las tres fases en los bornes del drive"],
        ],
        [1.4, 2.9, 4.0, 3.8],
        subtitle="La familia del encoder concentra las averías intermitentes más "
                 "difíciles",
        size=9.0,
        foot="Las alarmas intermitentes del encoder casi siempre son un problema de "
             "cable, de conector o de apantallamiento, no del encoder en sí.",
        notes=(
            "Cuente la estrategia para alarmas intermitentes de encoder, que son las "
            "más frustrantes:\n"
            "1) Mover el cable con la máquina en marcha (con seguridad) para ver si "
            "se reproduce: delata rotura por fatiga en cadena portacables.\n"
            "2) Comprobar que la malla está a tierra en ambos extremos con "
            "abrazadera de 360°.\n"
            "3) Comprobar separación respecto a cables de potencia.\n"
            "4) Sustituir el cable por uno nuevo original antes de sustituir el "
            "motor: es mucho más barato y resuelve la mayoría de los casos.\n\n"
            "Sobre A.81_: es la alarma que aparece tras las paradas largas de planta. "
            "La solución es preventiva: cambiar baterías cada dos años con el equipo "
            "energizado."
        ),
    )

    _diagrama_arbol(d)

    d.table_slide(
        "Mantenimiento preventivo del conjunto",
        ["Elemento", "Qué le pasa con el tiempo", "Periodicidad orientativa",
         "Acción"],
        [
            ["Ventilador del amplificador", "Rodamientos gastados, ruido, caudal "
             "insuficiente", "Revisar anualmente; sustituir según horas de servicio",
             "Sustitución preventiva antes de que provoque `A.7A_`"],
            ["Condensadores del bus", "Envejecimiento por temperatura",
             "Vigilar a partir de varios años de servicio continuo",
             "Sustitución del equipo o revisión por el servicio técnico"],
            ["Batería del encoder", "Descarga natural",
             "Cada 2 años (preventivo)",
             "Cambio **con la alimentación de control conectada**"],
            ["Filtros y ventilación del armario", "Obstrucción por polvo",
             "Trimestral o según el entorno", "Limpieza y sustitución de filtros"],
            ["Cables de motor y encoder", "Fatiga en cadena portacables, roce",
             "Inspección semestral",
             "Sustitución preventiva en ejes móviles de alto ciclo"],
            ["Acoplamiento", "Desgaste del elemento elástico, holgura",
             "Inspección semestral", "Sustitución del elastómero; verificar "
             "alineación"],
            ["Freno de retención", "Desgaste del forro, pérdida de par de retención",
             "Prueba anual", "Verificar par de retención según especificación"],
            ["Resistencia de regeneración", "Envejecimiento térmico, aflojamiento de "
             "bornes", "Inspección anual", "Verificar resistencia y estado de los "
             "terminales"],
            ["Aprietes de bornes de potencia", "Aflojamiento por ciclos térmicos",
             "Anual", "Reapriete al par indicado con la instalación consignada"],
        ],
        [2.3, 3.3, 2.9, 3.6],
        subtitle="Un plan simple que evita la mayoría de las paradas no planificadas",
        size=9.0,
        foot="Las periodicidades son orientativas: ajústalas al entorno real "
             "(temperatura, polvo, horas de servicio) y a las indicaciones del manual.",
        notes=(
            "La Σ-X dispone de monitores de vida útil de componentes (ventilador, "
            "condensadores, relés internos) que estiman el porcentaje consumido. "
            "Consúltelos en SigmaWin+ y llévelos al plan de mantenimiento: es "
            "mantenimiento predictivo gratuito que casi nadie usa.\n\n"
            "El reapriete de bornes es una tarea humilde y muy rentable: un borne "
            "flojo en un cable de motor de 18 A provoca calentamiento, caída de "
            "tensión asimétrica y, con el tiempo, un incendio o una avería del "
            "amplificador."
        ),
    )

    d.steps_slide(
        "Sustitución de un SERVOPACK o de un motor",
        [
            ("Consignar la instalación y esperar la descarga del bus",
             "LOTO, espera de al menos 5 minutos y verificación de ausencia de "
             "tensión. El LED CHARGE apagado no es suficiente."),
            ("Anotar y fotografiar todo antes de desmontar",
             "Etiquetas de los dos equipos, conexiones, posición de los cables y "
             "estado de los puentes (`B2`-`B3`, `CN8`)."),
            ("Verificar que el repuesto es idéntico",
             "Código completo, no sólo la potencia. Un sufijo distinto puede "
             "significar otra interfaz de comando."),
            ("Montar, cablear y comprobar antes de energizar",
             "Usa la lista de verificación de instalación del Módulo 05."),
            ("Cargar el fichero de parámetros",
             "Desde SigmaWin+ o desde el operador digital. Verifica después algunos "
             "parámetros críticos a mano."),
            ("Ejecutar `Fn008` si el encoder es absoluto y rehacer el origen",
             "El fichero de parámetros no contiene el origen de la máquina."),
            ("Verificar el eje y volver a documentar",
             "JOG sin carga, ciclo a baja velocidad, ciclo real. Actualiza el acta "
             "del eje con la fecha y el motivo de la sustitución."),
        ],
        subtitle="Con preparación, una hora; sin preparación, un día",
        callout=(
            "amber",
            "Repuestos que conviene tener en planta",
            "Un amplificador y un motor de los modelos más críticos, baterías de "
            "encoder, un cable de encoder y uno de motor de las longitudes "
            "habituales, y ventiladores de repuesto. Y sobre todo: las copias de "
            "parámetros actualizadas de todos los ejes.",
        ),
        notes=(
            "El paso 6 es el que convierte una sustitución rutinaria en un problema. "
            "Insista de nuevo: el origen no viaja en el fichero de parámetros.\n\n"
            "Sobre el paso 3: en almacén acaban conviviendo equipos parecidos con "
            "sufijos distintos. Un SGDXS-200A00A con interfaz de bus no sirve para "
            "sustituir a uno con interfaz analógica, aunque físicamente encaje.\n\n"
            "Recomiende ensayar el procedimiento una vez en condiciones controladas, "
            "por ejemplo durante una parada programada. La primera vez siempre "
            "aparecen sorpresas, y es mejor que aparezcan un martes por la mañana."
        ),
    )


# --------------------------------------------------------------------------
# Diagramas
# --------------------------------------------------------------------------

def _diagrama_metodo(d: Deck) -> None:
    slide = d.canvas_slide(
        "Un método de diagnóstico que funciona siempre",
        "Del síntoma a la causa en pasos verificables",
        notes=(
            "El error clásico en diagnóstico es empezar cambiando piezas. Este "
            "método obliga a recoger información antes de actuar.\n\n"
            "Los pasos 1 y 2 (qué dice el drive y qué dice el historial) resuelven "
            "una parte muy grande de los casos en dos minutos, sin herramientas.\n\n"
            "El paso 4, dividir el sistema, es la idea central: el sistema tiene "
            "cuatro bloques (controlador, drive, motor, mecánica) y dos enlaces "
            "(cableado de mando, cableado de potencia y encoder). Cada prueba debe "
            "descartar un bloque. Por ejemplo, un JOG desde el panel descarta de "
            "golpe el controlador y todo el cableado de mando.\n\n"
            "El paso 6 (documentar) es el que convierte una reparación en "
            "conocimiento de planta."
        ),
    )

    pasos = [
        ("1", "OBSERVAR", "¿Qué muestra el display? ¿Alarma, aviso o nada?\n"
         "¿Qué estaba haciendo la máquina cuando falló?", NAVY),
        ("2", "CONSULTAR EL HISTORIAL", "`Fn000` o SigmaWin+: ¿hay alarmas previas?\n"
         "¿Es la primera vez o se repite con un patrón?", BLUE),
        ("3", "MEDIR", "Monitores `Un`: entradas, salidas, par, error de posición.\n"
         "Tensión de red, continuidad, aislamiento.", CYAN),
        ("4", "DIVIDIR EL SISTEMA", "JOG desde el panel: descarta controlador y "
         "cableado de mando.\nDesacoplar la carga: separa drive+motor de la "
         "mecánica.", GREEN),
        ("5", "ACTUAR SOBRE UNA SOLA VARIABLE",
         "Un cambio cada vez, verificando el efecto antes del siguiente.", AMBER),
        ("6", "DOCUMENTAR", "Causa, solución y medida preventiva.\n"
         "La próxima vez, la avería durará diez minutos.", GRAY),
    ]

    y = Inches(1.78)
    h = Inches(0.72)
    for num, titulo, desc, color in pasos:
        d._rect(slide, Inches(0.62), y, Inches(12.1), h, fill=LIGHT,
                line=GRAY_LINE)
        d._rect(slide, Inches(0.62), y, Inches(0.62), h, fill=color)
        d._text(slide, Inches(0.62), y + Inches(0.17), Inches(0.62), Inches(0.4),
                num, size=Pt(18), color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        d._text(slide, Inches(1.42), y + Inches(0.06), Inches(3.1), Inches(0.35),
                titulo, size=Pt(12), color=color, bold=True)
        d._text(slide, Inches(4.60), y + Inches(0.07), Inches(7.9), Inches(0.60),
                desc, size=Pt(10), color=INK, spacing=1.08)
        y += Inches(0.775)

    d.callout(slide, Inches(0.62), Inches(6.42), Inches(12.1), Inches(0.48),
              "blue", "Regla de oro: nunca sustituyas una pieza sin una hipótesis que "
              "explique el síntoma.", "")


def _diagrama_arbol(d: Deck) -> None:
    slide = d.canvas_slide(
        "Árbol de decisión: «el eje no se mueve»",
        "El fallo más reportado y el más rápido de acotar",
        notes=(
            "Recorra el árbol de izquierda a derecha con el grupo, planteando cada "
            "pregunta en voz alta.\n\n"
            "La primera bifurcación (¿hay alarma?) es decisiva: con alarma, el drive "
            "ya ha hecho el diagnóstico y sólo hay que interpretarlo. Sin alarma, el "
            "problema está casi siempre en las condiciones de habilitación: servo ON, "
            "seguridad CN8, finales de carrera o consigna.\n\n"
            "El caso 'sin alarma y sin par' es el más confuso para el principiante y "
            "tiene tres sospechosos habituales: CN8 sin cablear tras retirar el "
            "puente, /S-ON no llega (comprobable en Un005) o falta la alimentación de "
            "+24VIN de las entradas.\n\n"
            "El caso 'con par pero sin movimiento' apunta a consigna ausente (Un007 "
            "sin pulsos, o telegrama de bus sin actualizar) o a bloqueo mecánico, "
            "que se distingue porque el par sube al máximo."
        ),
    )

    # Nodo raíz
    d.box(slide, Inches(0.62), Inches(3.35), Inches(2.1), Inches(0.95),
          "EL EJE NO\nSE MUEVE", NAVY, size=12, radius=0.10)

    ramas = [
        ("¿Hay ALARMA en el display?", RED, Inches(1.80),
         "**Sí** → identifica la familia y aplica la tabla de alarmas. El drive ya "
         "ha diagnosticado por ti."),
        ("¿El motor tiene par (el eje está 'duro')?", AMBER, Inches(3.10),
         "**No** → revisa `/S-ON` en `Un005`, el conector `CN8` de seguridad y la "
         "alimentación `+24VIN` de las entradas."),
        ("¿Llega consigna del controlador?", BLUE, Inches(4.40),
         "**No** → comprueba `Un007` (pulsos) o el estado del bus. Revisa el "
         "programa del PLC y el modo de control `Pn000.1`."),
        ("¿Están activos los finales de carrera?", GREEN, Inches(5.70),
         "**Sí** → `P-OT`/`N-OT` abiertos detienen el eje en ese sentido. Míralo en "
         "`Un005` y retira el eje en sentido contrario."),
    ]

    for pregunta, color, y, respuesta in ramas:
        d.line(slide, Inches(1.67), Inches(3.82), Inches(3.05), Inches(3.82),
               color=GRAY, width=Pt(1))
        d.line(slide, Inches(3.05), Inches(3.82), Inches(3.05), y + Inches(0.35),
               color=GRAY, width=Pt(1))
        d.line(slide, Inches(3.05), y + Inches(0.35), Inches(3.35),
               y + Inches(0.35), color=GRAY, width=Pt(1))
        d.box(slide, Inches(3.35), y, Inches(3.55), Inches(0.72), pregunta,
              color, size=10.5, radius=0.12)
        d._rect(slide, Inches(7.15), y, Inches(5.57), Inches(0.72), fill=LIGHT,
                line=GRAY_LINE)
        d._text(slide, Inches(7.35), y + Inches(0.09), Inches(5.2), Inches(0.6),
                respuesta, size=Pt(10), color=INK, spacing=1.1)

    d.callout(slide, Inches(0.62), Inches(6.55), Inches(12.1), Inches(0.42),
              "amber", "Si el par sube al máximo y el eje sigue sin moverse: "
              "bloqueo mecánico o freno sin liberar. Corta y comprueba a mano.", "")
