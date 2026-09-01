"""Módulo 0 — Apertura del curso: objetivos, alcance, mapa y convenciones."""

from builder import Card, Deck


def build(d: Deck) -> None:
    d.module = "INTRODUCCIÓN"

    d.title_slide(
        "Servo drives YASKAWA SERVOPACK",
        "De cero a experto: selección, instalación, parametrización, puesta en "
        "marcha y sintonización de un servoaccionamiento de 3 kW",
        [
            "Curso técnico completo · Serie Σ-7 (Sigma-7) · SGD7S + SGM7A/SGM7G",
            "Nivel: desde principiante absoluto hasta puesta a punto avanzada",
            "Formato: 14 módulos · teoría, práctica guiada y proyecto integrador",
        ],
        notes=(
            "Bienvenida. Preséntese y pregunte por la experiencia previa del grupo: "
            "¿han trabajado con variadores de frecuencia? ¿con PLC? ¿con servos de "
            "otras marcas? El curso está diseñado para que alguien sin experiencia "
            "previa pueda seguirlo, pero avanza hasta técnicas de sintonización "
            "avanzada.\n\n"
            "Deje claro desde el primer minuto el mensaje central: un servo no se "
            "'instala', se DIMENSIONA, se instala, se parametriza y se SINTONIZA. "
            "Saltarse cualquiera de esos cuatro pasos es la causa de la mayoría de "
            "los problemas en campo."
        ),
    )

    d.bullets_slide(
        "Qué vas a saber hacer al terminar",
        [
            "#Competencias de salida",
            "**Seleccionar** el SERVOPACK y el servomotor correctos para una máquina "
            "concreta, justificando el cálculo de par, inercia y ciclo de trabajo.",
            "**Instalar** el conjunto conforme al manual: potencia, control, "
            "apantallamiento, regeneración, freno de retención y seguridad funcional.",
            "**Parametrizar** el drive desde el panel frontal y desde SigmaWin+, "
            "incluyendo engranaje electrónico, límites y asignación de E/S.",
            "**Poner en marcha** un eje siguiendo un procedimiento verificable, desde "
            "el JOG sin carga hasta el ciclo de producción.",
            "**Sintonizar** el lazo de control: autoajuste, ajuste manual de ganancias, "
            "filtros notch y supresión de vibración.",
            "**Diagnosticar** alarmas y averías con un método sistemático y realizar el "
            "mantenimiento preventivo del equipo.",
            "",
            "#Entregable del curso",
            "Un eje de 3 kW dimensionado, cableado, parametrizado, sintonizado y "
            "documentado (proyecto integrador del Módulo 12).",
        ],
        subtitle="Objetivos de aprendizaje del curso",
        notes=(
            "Lea los objetivos en voz alta: funcionan como contrato con el alumno. "
            "Al final del curso conviene volver a esta diapositiva y verificar uno a "
            "uno los seis puntos.\n\n"
            "Si el grupo es de mantenimiento y no de diseño, insista en los puntos 4, "
            "5 y 6. Si es de ingeniería de proyecto, en los puntos 1, 2 y 3."
        ),
    )

    d.cards_slide(
        "A quién va dirigido y qué necesitas saber antes",
        [
            Card(
                "Perfiles destinatarios",
                "· Técnicos de mantenimiento eléctrico e industrial.\n"
                "· Integradores y programadores de PLC/CNC.\n"
                "· Ingenieros de automatización y diseño de máquina.\n"
                "· Personal de puesta en marcha y servicio técnico.",
                "blue",
            ),
            Card(
                "Requisitos previos",
                "· Electricidad básica: tensión, corriente, trifásica, protecciones.\n"
                "· Lectura de esquemas eléctricos.\n"
                "· Nociones de mecánica: par, velocidad, reducción.\n"
                "· No se requiere experiencia previa con servos.",
                "cyan",
            ),
            Card(
                "Equipo recomendado para la práctica",
                "· SERVOPACK SGD7S-200A + motor SGM7A-30A o SGM7G-30A.\n"
                "· Cables de potencia y encoder originales.\n"
                "· PC con SigmaWin+ y cable USB (CN7).\n"
                "· Multímetro, pinza amperimétrica y EPP.",
                "amber",
            ),
        ],
        subtitle="Público objetivo, prerrequisitos y laboratorio",
        notes=(
            "Si no dispone de hardware real, todo el curso puede seguirse con "
            "SigmaWin+ en modo offline: permite crear un proyecto, editar el juego "
            "completo de parámetros y estudiar las pantallas de ajuste sin drive.\n\n"
            "Recuerde que las prácticas con tensión requieren autorización y EPP. "
            "El bus de continua del SERVOPACK conserva carga después de desconectar."
        ),
    )

    d.table_slide(
        "Mapa del curso",
        ["Módulo", "Contenido", "Qué resuelve"],
        [
            ["01", "Fundamentos del servoaccionamiento",
             "Entender qué es un servo y en qué se diferencia de un variador"],
            ["02", "La familia SERVOPACK Σ-7",
             "Leer un código de modelo y elegir la variante correcta"],
            ["03", "El servomotor de 3 kW",
             "Interpretar curvas, encoder, freno y combinaciones válidas"],
            ["04", "Dimensionamiento y selección",
             "Justificar con números que el conjunto 3 kW es el adecuado"],
            ["05", "Instalación mecánica y eléctrica",
             "Cablear potencia, tierra, regeneración y freno sin errores"],
            ["06", "Interfaz de control: CN1, analógico, pulsos y bus",
             "Conectar el drive al PLC/CNC con el modo de control correcto"],
            ["07", "Parámetros, panel y SigmaWin+",
             "Manejar Pn/Fn/Un y el engranaje electrónico con soltura"],
            ["08", "Puesta en marcha paso a paso",
             "Arrancar el eje con un procedimiento seguro y repetible"],
            ["09", "Sintonización del lazo de control",
             "Conseguir precisión y rapidez sin vibración"],
            ["10", "Seguridad funcional (STO / HWBB)",
             "Integrar el eje en la cadena de seguridad de la máquina"],
            ["11", "Diagnóstico, alarmas y mantenimiento",
             "Reducir el tiempo de parada ante una avería"],
            ["12", "Proyecto integrador", "Aplicar todo a una máquina real"],
            ["13", "Anexos, evaluación y recursos",
             "Tablas de consulta rápida y autoevaluación"],
        ],
        [0.8, 4.2, 6.0],
        subtitle="13 módulos encadenados: cada uno se apoya en el anterior",
        size=10.5,
        align_center=(0,),
        notes=(
            "Explique la lógica del recorrido: primero se entiende el principio "
            "(01-03), después se justifica la selección con cálculo (04), luego se "
            "monta (05-06), se configura (07), se arranca (08), se afina (09), se "
            "protege (10) y se mantiene (11).\n\n"
            "Es tentador saltar directamente al módulo 08 o 09. Advierta que el 80 % "
            "de los problemas de sintonización que se ven en campo son en realidad "
            "problemas de dimensionamiento (módulo 04) o de cableado y "
            "apantallamiento (módulo 05)."
        ),
    )

    d.two_col_slide(
        "Metodología y convenciones del material",
        (
            "Cómo trabajaremos",
            [
                "Cada módulo: teoría breve → parámetros implicados → práctica guiada → "
                "errores frecuentes.",
                "Las diapositivas incluyen **notas del instructor**: úsalas como guion "
                "y como manual de estudio.",
                "Los procedimientos están numerados para poder seguirlos con el equipo "
                "delante, sin la presentación.",
                "Al final de cada bloque hay una lista de verificación imprimible "
                "(Módulo 13).",
            ],
        ),
        (
            "Convenciones tipográficas",
            [
                "`Pn___` → parámetro de configuración (p. ej. `Pn100`).",
                "`Fn___` → función de utilidad ejecutable (p. ej. `Fn002`, JOG).",
                "`Un___` → variable de monitorización (p. ej. `Un000`, velocidad).",
                "`A.___` → código de alarma (p. ej. `A.710`, sobrecarga).",
                "`/XXX` → señal activa a nivel bajo (p. ej. `/S-ON`).",
                "Los valores numéricos concretos corresponden al conjunto de ejemplo "
                "SGD7S-200A + SGM7A-30A.",
            ],
        ),
        subtitle="Cómo sacar el máximo partido a este material",
        callout=(
            "red",
            "Advertencia importante sobre los datos numéricos",
            "Todos los valores de catálogo, códigos de parámetro y pinouts que aparecen "
            "en el curso son de referencia didáctica. Antes de aplicar cualquiera de "
            "ellos a un equipo real, contrasta con el manual oficial de tu SERVOPACK "
            "(SIEP S800001 xx) y con la placa de características: las asignaciones "
            "cambian entre series (Σ-V / Σ-7), variantes de interfaz y revisiones de "
            "firmware.",
        ),
        notes=(
            "Insista en la advertencia: el objetivo del curso es que el alumno sepa "
            "QUÉ buscar y DÓNDE buscarlo en el manual, no que memorice tablas. Un "
            "buen técnico de servos es el que maneja el manual con agilidad.\n\n"
            "Manuales de referencia: 'Σ-7S SERVOPACK with Analog Voltage/Pulse Train "
            "References Product Manual' (SIEP S800001 26), 'Σ-7 Series Product Manual' "
            "y 'Σ-7 Series Peripheral Device Selection Manual'. Todos son descargables "
            "gratuitamente desde la web de YASKAWA."
        ),
    )

    d.bullets_slide(
        "Seguridad antes que nada",
        [
            "#Riesgos eléctricos",
            "El circuito principal trabaja a **200–240 V CA trifásicos**; el bus de "
            "continua alcanza unos **310 V CC** y mantiene carga tras desconectar.",
            "- Espera al menos **5 minutos** tras cortar la alimentación y **verifica "
            "ausencia de tensión** entre `B1/⊕` y `⊖2` antes de tocar bornes.",
            "- Nunca conectes la red a los bornes `U`, `V`, `W`: destruirías el equipo "
            "de forma inmediata e irreversible.",
            "#Riesgos mecánicos",
            "Un motor de 3 kW entrega un par pico de más de **28 N·m** y acelera en "
            "milisegundos: cualquier elemento suelto en el eje se convierte en un "
            "proyectil.",
            "- Retira chavetas sueltas antes de girar el motor sin carga.",
            "- En ejes verticales, la carga **cae** al desactivar el servo: el freno de "
            "retención es obligatorio y debe verificarse.",
            "#Riesgos térmicos",
            "El disipador y el motor pueden superar los **70 °C** en servicio normal. "
            "Señalízalo y espera a que enfríen.",
        ],
        subtitle="Lee esta diapositiva antes de tocar el equipo",
        callout=(
            "red",
            "Regla de oro",
            "Consignación (LOTO) → verificación de ausencia de tensión → trabajo. "
            "Ninguna prisa justifica saltarse este orden.",
        ),
        notes=(
            "No pase esta diapositiva rápido. Si el curso incluye laboratorio, haga "
            "firmar la hoja de riesgos aquí.\n\n"
            "Dato práctico: el LED CHARGE del SERVOPACK indica que el bus de continua "
            "sigue cargado. Que esté apagado es condición necesaria, pero la "
            "verificación con multímetro sigue siendo obligatoria.\n\n"
            "Anécdota útil para fijar el mensaje: la avería más cara y más frecuente "
            "en puesta en marcha es alimentar por U/V/W por confusión con los bornes "
            "L1/L2/L3. El SERVOPACK se destruye instantáneamente y no está cubierto "
            "por garantía."
        ),
    )
