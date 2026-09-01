"""Módulo 13 — Anexos, evaluación y recursos."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, GRAY, GRAY_LINE, GREEN, INK, LIGHT,
                     LIGHT_BLUE, NAVY, RED, WHITE, Card, Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 13",
        "Anexos, evaluación y recursos",
        [
            "Fichas de consulta rápida: parámetros, alarmas y fórmulas",
            "Listas de verificación imprimibles",
            "Glosario completo",
            "Autoevaluación con respuestas comentadas",
            "Itinerario de aprendizaje y recursos oficiales",
        ],
        duration="2 h",
        notes=(
            "Los anexos están pensados para imprimirse y llevarse a planta. Anime a "
            "los alumnos a extraer estas diapositivas a PDF y tenerlas en el móvil."
        ),
    )

    d.table_slide(
        "Ficha rápida — Fórmulas de dimensionamiento",
        ["Magnitud", "Fórmula", "Unidades y notas"],
        [
            ["Par nominal a partir de la potencia", "T ≈ 9,55 × P[kW] / n[krpm]",
             "N·m — comprobación mental instantánea"],
            ["Velocidad angular", "ω = 2π · n / 60", "rad/s — n en rpm"],
            ["Aceleración angular", "α = Δω / Δt", "rad/s²"],
            ["Par de aceleración", "T = J · α", "N·m — J en kg·m² referido al motor"],
            ["Inercia de masa con husillo", "J = m · (p / 2π)²",
             "kg·m² — p en m/vuelta"],
            ["Inercia de cilindro macizo", "J = ½ · m · r²  con  m = ρ·π·r²·L",
             "kg·m² — ρ(acero) = 7.850 kg/m³"],
            ["Inercia a través de reducción", "J_reflejada = J_carga / i²",
             "El efecto i² es la clave del diseño"],
            ["Par de fricción (husillo)", "T = μ·m·g·p / (2π·η)",
             "N·m — incluye el rendimiento"],
            ["Par de gravedad (eje vertical)", "T = m·g·p / (2π·η)",
             "N·m — presente también en reposo"],
            ["Par eficaz del ciclo", "T_rms = √[ Σ(Tᵢ²·tᵢ) / T_ciclo ]",
             "N·m — incluye los tiempos de parada"],
            ["Energía cinética a frenar", "E = ½ · J_total · ω²",
             "J — base del cálculo de regeneración"],
            ["Engranaje electrónico",
             "B/A = (resolución × relación) / (unidades por vuelta de carga)",
             "`Pn20E` / `Pn210`"],
        ],
        [3.4, 4.6, 4.0],
        subtitle="Todo el Módulo 04 en una hoja",
        size=9.5,
        notes=(
            "Esta es la diapositiva que más se fotografía de todo el curso. "
            "Sugiérales que la impriman y la peguen en la contraportada de su cuaderno "
            "de trabajo.\n\n"
            "Recuerde el criterio de aceptación asociado: T_rms ≤ 0,8 × T_nominal y "
            "T_pico ≤ 0,8 × T_máximo."
        ),
    )

    d.table_slide(
        "Ficha rápida — Parámetros, funciones y monitores",
        ["Grupo", "Referencias clave"],
        [
            ["Configuración básica",
             "`Pn000.0` sentido de giro · `Pn000.1` modo de control · `Pn001.0` "
             "método de parada"],
            ["Posición",
             "`Pn20E`/`Pn210` engranaje electrónico · `Pn200.0` formato de pulsos · "
             "`Pn212` salida de encoder · `Pn522` ventana de posicionado · `Pn520` "
             "error máximo"],
            ["Velocidad y par",
             "`Pn300` escala de consigna de velocidad · `Pn400` escala de consigna de "
             "par · `Pn502` umbral de giro"],
            ["Sintonización",
             "`Pn103` relación de inercias · `Pn100` ganancia de velocidad · `Pn101` "
             "integral · `Pn102` ganancia de posición · `Pn401` filtro de par · "
             "`Pn170` tuning-less"],
            ["Filtros y vibración",
             "`Pn408` habilitación · `Pn409`/`Pn40A`/`Pn40B` primer notch · `Pn140` "
             "control por modelo · `Pn14A` supresión de vibración"],
            ["Entradas y salidas",
             "`Pn50A`/`Pn50B` entradas · `Pn50E`/`Pn50F`/`Pn510` salidas"],
            ["Freno y regeneración",
             "`Pn506`/`Pn507`/`Pn508` temporización de freno · `Pn600` capacidad de "
             "regeneración"],
            ["Encoder absoluto",
             "`Fn008` setup · `Pn205` límite multivuelta"],
            ["Funciones de utilidad",
             "`Fn000` historial de alarmas · `Fn002` JOG · `Fn004` JOG programado · "
             "`Fn005` inicialización · `Fn201` autoajuste avanzado · `Fn202` "
             "autoajuste con referencia · `Fn203` ajuste de un parámetro · `Fn205` "
             "supresión de vibración · `Fn206` análisis en frecuencia"],
            ["Monitores",
             "`Un000` velocidad · `Un002` par · `Un005`/`Un006` E/S · `Un007` "
             "consigna de pulsos · `Un008` error de posición"],
        ],
        [2.4, 9.7],
        subtitle="Chuleta de referencia (verifica siempre contra el manual de tu "
                 "modelo)",
        size=9.5,
        notes=(
            "Advierta una vez más de que la numeración puede variar entre series y "
            "variantes. El valor de esta ficha es recordar QUÉ existe; el número "
            "exacto se confirma en el manual.\n\n"
            "Si los alumnos trabajan habitualmente con un modelo concreto, "
            "recomiéndeles hacer su propia versión de esta ficha con los valores "
            "verificados de su equipo."
        ),
    )

    d.table_slide(
        "Ficha rápida — Familias de alarma",
        ["Prefijo", "Ámbito", "Primera pregunta que hay que hacerse"],
        [
            ["`A.0__`", "Parámetros, memoria interna y combinación de equipos",
             "¿Se ha cambiado algún equipo o se ha interrumpido una escritura?"],
            ["`A.1__`", "Sobrecorriente y etapa de potencia",
             "¿Hay cortocircuito en el cable o en el motor?"],
            ["`A.3__`", "Circuito de regeneración",
             "¿Está bien el puente `B2`-`B3` o la resistencia externa?"],
            ["`A.4__`", "Tensión del bus (sobre o subtensión)",
             "¿Cómo está la red? ¿Se frena demasiado enérgicamente?"],
            ["`A.5__`", "Velocidad excesiva",
             "¿Están bien las fases del motor y el engranaje electrónico?"],
            ["`A.7__`", "Sobrecarga y temperatura",
             "¿Cuánto par pide realmente el eje (`Un002`)?"],
            ["`A.8__`", "Encoder absoluto y batería",
             "¿Cuándo se cambió la batería por última vez?"],
            ["`A.9__`", "**Avisos** (el eje sigue funcionando)",
             "¿Qué me está anticipando el drive?"],
            ["`A.C__`", "Comunicación con el encoder",
             "¿Cable original, apantallado y separado de la potencia?"],
            ["`A.d__`", "Exceso de error de posición",
             "¿Hay atasco mecánico o el eje está mal dimensionado?"],
            ["`A.E__`", "Comunicación de bus",
             "¿Qué dicen los contadores de error del maestro?"],
            ["`A.F__`", "Alimentación principal (falta de fase)",
             "¿Están las tres fases presentes en los bornes?"],
        ],
        [1.4, 4.3, 6.4],
        subtitle="Identifica la familia y habrás acotado el 80 % del problema",
        size=9.5,
        notes=(
            "Este resumen por familias es más útil en campo que una lista completa "
            "de códigos: permite orientar el diagnóstico en segundos y después buscar "
            "el código exacto en el manual.\n\n"
            "Recuerde la regla: A.9__ son avisos, el resto son alarmas que detienen "
            "el eje."
        ),
    )

    d.two_col_slide(
        "Lista de verificación imprimible",
        (
            "Antes de energizar",
            [
                "☐ Modelos de drive y motor coinciden y son combinación homologada.",
                "☐ Tensión de red medida y dentro de rango.",
                "☐ `L1` `L2` `L3` y `L1C` `L2C` correctamente conectados.",
                "☐ Ninguna fase de red en `U` `V` `W`.",
                "☐ Tierra del drive y del motor con continuidad verificada.",
                "☐ Puente `B2`-`B3` o resistencia externa según cálculo.",
                "☐ Cable de encoder en `CN2`, malla a tierra, separado de potencia.",
                "☐ `+24VIN` alimentado y cableado de `CN1` verificado.",
                "☐ `CN8`: puente original o circuito de seguridad cableado.",
                "☐ Freno de retención con alimentación propia y supresor.",
                "☐ Zona mecánica despejada y motor desacoplado.",
                "☐ Parada de emergencia probada.",
            ],
        ),
        (
            "Antes de dar por terminada la puesta en marcha",
            [
                "☐ JOG en ambos sentidos suave y silencioso.",
                "☐ Sentido de giro correcto ajustado con `Pn000.0`.",
                "☐ Engranaje electrónico **verificado midiendo** un desplazamiento.",
                "☐ Finales de carrera probados físicamente.",
                "☐ `Fn008` ejecutado y origen documentado.",
                "☐ Autoajuste realizado **con la carga real**.",
                "☐ Ciclo real ejecutado al menos 30 minutos sin alarmas.",
                "☐ Par RMS y de pico medidos y comparados con el cálculo.",
                "☐ HWBB probado y tiempo de parada medido.",
                "☐ Freno de retención verificado (agarra y no arrastra).",
                "☐ Ficheros de parámetros guardados y archivados.",
                "☐ Acta del eje rellenada y firmada.",
            ],
        ),
        subtitle="Imprime, plastifica y guarda en el maletín",
        tones=("blue", "green"),
        size=11.5,
        notes=(
            "Sugiera convertir estas dos columnas en un documento A4 a doble cara. Es "
            "el entregable del curso con mayor impacto inmediato en el trabajo "
            "diario.\n\n"
            "Recuerde: una lista de verificación sólo funciona si se rellena en el "
            "momento, no de memoria al final del día."
        ),
    )

    d.table_slide(
        "Glosario",
        ["Término", "Definición"],
        [
            ["Baseblock", "Estado en que los transistores de salida están "
             "bloqueados: el motor no recibe par y queda libre"],
            ["EDM", "Salida de vigilancia que confirma al módulo de seguridad que el "
             "drive ha entrado en estado seguro"],
            ["Engranaje electrónico", "Relación programable que traduce las unidades "
             "de referencia del controlador a cuentas de encoder"],
            ["Error de seguimiento", "Diferencia entre la posición ordenada y la real "
             "durante el movimiento"],
            ["f.c.e.m.", "Fuerza contraelectromotriz: tensión que genera el motor al "
             "girar; limita la velocidad y permite la regeneración"],
            ["Freno dinámico", "Frenado por cortocircuito controlado de las fases del "
             "motor; no mantiene la carga parada"],
            ["HWBB", "Hard Wire Baseblock: implementación por hardware de la función "
             "de seguridad STO en la Σ-7"],
            ["Notch", "Filtro que elimina una banda estrecha de frecuencias para "
             "cancelar una resonancia mecánica"],
            ["PMSM", "Motor síncrono de imanes permanentes: el tipo de servomotor "
             "empleado"],
            ["Regeneración", "Energía devuelta por el motor al frenar, que debe "
             "disiparse o reinyectarse"],
            ["Relación de inercias", "Cociente entre la inercia de la carga reflejada "
             "y la del rotor; predice la dificultad de sintonización"],
            ["SERVOPACK", "Denominación comercial de YASKAWA para el servoamplificador"],
            ["STO", "Safe Torque Off: función de seguridad que garantiza ausencia de "
             "par, no ausencia de movimiento"],
            ["Tuning-less", "Función que permite operar sin ajustar ganancias "
             "adaptándose automáticamente a la carga"],
        ],
        [2.6, 9.5],
        subtitle="Vocabulario del curso",
        size=9.5,
        notes=(
            "Repase los términos que más confusión generan: baseblock, STO frente a "
            "parada de emergencia, y relación de inercias.\n\n"
            "Puede usarse como test rápido: tape la columna de la derecha y pida "
            "definiciones."
        ),
    )

    d.table_slide(
        "Autoevaluación (respuestas en la diapositiva siguiente)",
        ["#", "Pregunta"],
        [
            ["1", "Un motor de 3 kW gira a 1.500 rpm. ¿Cuál es su par nominal "
             "aproximado?"],
            ["2", "¿Por qué no se debe invertir el sentido de giro intercambiando dos "
             "fases del motor?"],
            ["3", "Una carga de 200 kg se mueve con un husillo de 10 mm de paso. "
             "¿Cuál es su inercia reflejada?"],
            ["4", "El eje vibra al llegar al destino y oscila tres o cuatro veces. "
             "¿Qué parámetro revisarías primero?"],
            ["5", "¿Qué hay que hacer antes de conectar una resistencia de "
             "regeneración externa?"],
            ["6", "El motor no da par y no aparece ninguna alarma. Cita las tres "
             "causas más probables."],
            ["7", "¿Qué diferencia hay entre la alarma `A.710` y la `A.720`?"],
            ["8", "¿Por qué hay que cambiar la batería del encoder con la "
             "alimentación de control conectada?"],
            ["9", "¿Garantiza la función STO que el eje esté parado?"],
            ["10", "Tras sustituir un SERVOPACK y cargar el fichero de parámetros, "
             "¿qué falta por hacer?"],
        ],
        [0.5, 11.6],
        subtitle="Diez preguntas para comprobar que el curso ha calado",
        size=10.5,
        align_center=(0,),
        notes=(
            "Deje tiempo real para responder (10-15 minutos) antes de pasar a las "
            "soluciones. Si es posible, que las respondan por escrito y en "
            "parejas.\n\n"
            "Las preguntas están ordenadas por módulos: 1-3 corresponden a "
            "fundamentos y dimensionamiento, 4-5 a sintonización e instalación, 6-8 a "
            "diagnóstico, 9 a seguridad y 10 a mantenimiento."
        ),
    )

    d.table_slide(
        "Autoevaluación — Respuestas comentadas",
        ["#", "Respuesta"],
        [
            ["1", "T ≈ 9,55 × 3 / 1,5 = **19,1 N·m**. El doble que a 3.000 rpm con la "
             "misma potencia."],
            ["2", "Porque la realimentación del encoder no se invierte: el lazo pasa "
             "a ser positivo y el eje se embala o dispara alarma. Se usa `Pn000.0`."],
            ["3", "J = 200 × (0,010/2π)² = 200 × (0,001592)² ≈ **5,1 × 10⁻⁴ kg·m²**. "
             "Un paso pequeño reduce mucho la inercia reflejada."],
            ["4", "`Pn103` (relación de inercias) y después la integral de velocidad "
             "`Pn101`. Antes de subir o bajar ganancias, comprobar que la inercia "
             "declarada es correcta."],
            ["5", "Retirar el puente `B2`-`B3`, respetar la resistencia mínima "
             "admisible y declarar la capacidad en `Pn600`."],
            ["6", "`CN8` sin cablear tras retirar el puente · `/S-ON` que no llega "
             "(verificable en `Un005`) · `+24VIN` sin alimentar."],
            ["7", "`A.710` es sobrecarga instantánea (un pico muy alto); `A.720` es "
             "sobrecarga continua acumulada por el modelo térmico. La segunda apunta "
             "a un problema de dimensionamiento o de fricción."],
            ["8", "Para que el encoder no pierda el contaje multivuelta. Si lo "
             "pierde, hay que ejecutar `Fn008` y **rehacer el origen** de la "
             "máquina."],
            ["9", "**No.** Garantiza ausencia de par. El eje seguirá moviéndose por "
             "inercia y, en un eje vertical, la carga caerá."],
            ["10", "Ejecutar `Fn008` si el encoder es absoluto, **rehacer el "
             "origen** (no está en el fichero de parámetros) y verificar el eje "
             "antes de devolverlo a producción."],
        ],
        [0.5, 11.6],
        subtitle="Si has acertado ocho o más, estás en condiciones de trabajar con "
                 "el equipo",
        size=9.5,
        align_center=(0,),
        notes=(
            "Comente cada respuesta brevemente, insistiendo en el razonamiento y no "
            "en el dato.\n\n"
            "Las preguntas 6, 9 y 10 son las que más fallan y, no por casualidad, las "
            "que corresponden a los errores más caros en campo."
        ),
    )

    d.two_col_slide(
        "Itinerario de aprendizaje y recursos",
        (
            "Cómo seguir avanzando",
            [
                "#Nivel 1 — Autonomía básica (este curso)",
                "Instalar, parametrizar, arrancar y diagnosticar un eje.",
                "#Nivel 2 — Especialización",
                "- Sintonización avanzada de ejes difíciles y análisis en frecuencia.",
                "- Integración en bus con maestros de terceros y perfiles CiA 402.",
                "- Sincronismo entre ejes: levas electrónicas, gantry, corte al vuelo.",
                "#Nivel 3 — Diseño de máquina",
                "- Selección de arquitecturas completas de accionamiento.",
                "- Seguridad funcional aplicada: análisis de riesgos y validación.",
                "- Eficiencia energética y gestión de la regeneración.",
            ],
        ),
        (
            "Dónde buscar información fiable",
            [
                "**Manual de producto del SERVOPACK** correspondiente a tu variante: "
                "es la fuente principal y contiene todos los parámetros, alarmas y "
                "pinouts.",
                "**Catálogo de la serie Σ-7**: datos de motores, curvas, inercias y "
                "combinaciones homologadas.",
                "**Manual de selección de periféricos**: protecciones, filtros, "
                "resistencias de regeneración y cables.",
                "**Ayuda de SigmaWin+**: describe cada función de ajuste con detalle.",
                "**Soporte técnico oficial de YASKAWA** para dudas de aplicación y "
                "para confirmar combinaciones.",
                "- Descarga los manuales y guárdalos **en local**: el día que los "
                "necesites puede que no tengas cobertura en la nave.",
            ],
        ),
        subtitle="El curso termina; el aprendizaje, no",
        tones=("blue", "green"),
        callout=(
            "amber",
            "Recordatorio final sobre los datos del curso",
            "Los valores numéricos, códigos y asignaciones que has visto son "
            "didácticos. Antes de aplicarlos a un equipo real, contrástalos siempre "
            "con el manual oficial de tu modelo y con la placa de características.",
        ),
        notes=(
            "Cierre insistiendo en el hábito profesional más valioso: consultar el "
            "manual. El objetivo del curso no era sustituir al manual, sino enseñar a "
            "usarlo con criterio y a saber qué preguntar.\n\n"
            "Anime a montar un pequeño banco de pruebas en planta si es posible: un "
            "drive y un motor sobre una placa, con SigmaWin+. Es la mejor inversión "
            "formativa para un equipo de mantenimiento."
        ),
    )

    d.quote_slide(
        "Un servo no se instala: se dimensiona, se instala,\n"
        "se parametriza y se sintoniza.",
        "Si falta cualquiera de los cuatro pasos, el problema aparecerá más tarde — "
        "y más caro.",
        notes=(
            "Diapositiva de cierre. Recupere la primera diapositiva de objetivos y "
            "repase los seis puntos con el grupo, preguntando si se sienten capaces "
            "de cada uno.\n\n"
            "Deje tiempo para preguntas abiertas y recoja las dudas que no hayan "
            "quedado resueltas: suelen indicar qué parte del curso conviene reforzar "
            "en la siguiente edición."
        ),
    )
