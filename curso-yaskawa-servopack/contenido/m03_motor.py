"""Módulo 3 — El servomotor de 3 kW."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, GRAY, GRAY_LINE, GREEN, INK, LIGHT,
                     LIGHT_BLUE, NAVY, RED, WHITE, Card, Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 03",
        "El servomotor de 3 kW",
        [
            "Cómo funciona un motor síncrono de imanes permanentes",
            "Las familias SGMXJ, SGMXA, SGMXG y SGMXP",
            "Elegir entre 3.000 rpm y 1.500 rpm para la misma potencia",
            "Leer el código de modelo del motor",
            "Encoder absoluto, batería y freno de retención",
            "Combinaciones homologadas motor–SERVOPACK",
        ],
        duration="3 h",
        notes=(
            "El motor determina el comportamiento de la máquina mucho más que el "
            "amplificador. Dos motores de la misma potencia pueden dar resultados "
            "radicalmente distintos según su inercia y su velocidad nominal. Ese es "
            "el mensaje central del módulo."
        ),
    )

    d.bullets_slide(
        "Cómo funciona un servomotor de imanes permanentes",
        [
            "#Principio",
            "El rotor lleva **imanes permanentes** de tierras raras; el estátor "
            "genera un campo magnético giratorio. El rotor sigue al campo de forma "
            "**síncrona**: no hay deslizamiento, la velocidad es exactamente la de "
            "la frecuencia aplicada.",
            "El SERVOPACK conoce en todo momento la posición del rotor gracias al "
            "encoder y coloca el campo del estátor **90° eléctricos adelantado**, "
            "que es la posición de par máximo por amperio.",
            "",
            "#Consecuencias prácticas",
            "**Par proporcional a la corriente**: `T ≈ Kt · I`. Medir la corriente "
            "del motor es medir el par. El monitor `Un002` muestra el par en % del "
            "nominal.",
            "**Par pleno desde 0 rpm**, de forma continua y sin calentamiento "
            "anómalo, porque la refrigeración no depende de la velocidad de giro.",
            "**Rotor de baja inercia** y alta densidad de par: por eso acelera en "
            "milisegundos donde un motor asíncrono equivalente tardaría décimas.",
            "**Fuerza contraelectromotriz**: al girar, el motor genera tensión "
            "proporcional a la velocidad. Es lo que limita la velocidad máxima y lo "
            "que permite la regeneración al frenar.",
            "",
            "#Aviso de mantenimiento",
            "Un motor girando sin drive (arrastrado por la máquina) **genera "
            "tensión en sus bornes**. Trata el conector de potencia como un elemento "
            "activo aunque el armario esté sin tensión.",
        ],
        subtitle="El PMSM: por qué se comporta como se comporta",
        notes=(
            "El punto de la f.c.e.m. explica de golpe tres cosas que preguntan "
            "siempre los alumnos: por qué la curva de par cae a alta velocidad, por "
            "qué frenar genera energía que hay que disipar, y por qué es peligroso "
            "manipular el conector del motor en un eje que puede girar por gravedad "
            "o por arrastre.\n\n"
            "Demostración vistosa si hay motor en el aula: gire el eje a mano con el "
            "conector libre y mida tensión alterna entre dos fases con el "
            "multímetro. Con 3 kW y giro rápido se obtienen decenas de voltios."
        ),
    )

    d.table_slide(
        "Las familias de servomotor rotativo Σ-X",
        ["Familia", "Perfil", "Velocidad nominal / máxima", "Aplicación típica"],
        [
            ["SGMXJ", "Inercia media, cuerpo corto", "3.000 / 6.000 rpm",
             "Uso general en máquina compacta; el más vendido en potencias bajas"],
            ["SGMXA", "Inercia baja, cuerpo largo", "3.000 / 6.000 rpm",
             "Alta dinámica: ciclos rápidos con cargas de inercia moderada"],
            ["SGMXG", "Inercia media-alta, alto par", "1.500 / 3.000 rpm",
             "Cargas de gran inercia y alto par: husillos grandes, prensas, ejes de "
             "arrastre"],
            ["SGMXP", "Inercia media, cuerpo plano", "3.000 / 6.000 rpm",
             "Cuando la longitud del motor es el problema (máquinas estrechas)"],
            ["SGMXD / lineales / directos", "Par directo y motores lineales", "Variable",
             "Accionamiento directo sin reductor: mesas rotativas, ejes lineales"],
        ],
        [1.7, 2.5, 2.6, 5.0],
        subtitle="Misma potencia, comportamientos distintos",
        size=10.5,
        foot="Combinaciones del manual (apartado 1.5): el SGDXS-200A00A se combina "
             "con SGMXA-25A, SGMXA-30A y, derateado a 2,4 kW, con SGMXG-30A.",
        notes=(
            "Insista: la potencia es el resultado, no el criterio. El criterio es el "
            "par necesario a la velocidad necesaria y la inercia que hay que "
            "mover.\n\n"
            "Regla mnemotécnica para las familias: J = 'justo lo normal', A = 'ágil' "
            "(baja inercia), G = 'grande' (alto par, baja velocidad), P = 'plano'."
        ),
    )

    d.two_col_slide(
        "3 kW a 3.000 rpm o a 1.500 rpm: la decisión clave",
        (
            "SGMXA-30A — 3,0 kW a 3.000 rpm ✔ combinación homologada",
            [
                "Par nominal ≈ **9,55 N·m**; par pico ≈ **28,6 N·m**.",
                "Inercia del rotor **baja** → acelera muy rápido y admite relaciones "
                "de inercia moderadas.",
                "#Elígelo si…",
                "- El eje debe hacer **muchos ciclos por minuto** con recorridos "
                "cortos.",
                "- Hay una **reducción** que adapta la velocidad a la carga.",
                "- La inercia de la carga es baja o media.",
                "#Cuidado",
                "- Con carga de gran inercia, la relación J_carga/J_rotor se dispara "
                "y la sintonización se vuelve difícil.",
            ],
        ),
        (
            "SGMXG-30A — 2,9 kW a 1.500 rpm ⚠ queda derateado",
            [
                "**Con un SGDXS-200A el fabricante lo limita a 2,4 kW**: la "
                "combinación plena de este motor es con un SGDXS-330A.",
                "Par nominal ≈ **18,6 N·m** a plena potencia.",
                "Inercia del rotor **alta** → mucho más tolerante a cargas de gran "
                "inercia.",
                "#Elígelo si…",
                "- Necesitas **par**, no revoluciones: accionamiento directo de "
                "husillos, rodillos o ejes pesados.",
                "- Quieres **evitar el reductor** y su holgura.",
                "- La carga tiene inercia elevada y quieres sintonizar sin dolor.",
                "#Cuidado",
                "- La velocidad máxima es la mitad: comprueba que el ciclo cabe en "
                "el tiempo disponible.",
                "- Con tu amplificador **no dispondrás de los 2,9 kW**, sino de "
                "2,4 kW. Si necesitas ese par continuo, hay que subir de "
                "amplificador.",
            ],
        ),
        subtitle="Misma potencia, el doble de par o el doble de velocidad",
        tones=("cyan", "blue"),
        callout=(
            "green",
            "Conclusión para tu equipo",
            "La pareja homologada a plena potencia del **SGDXS-200A00A** es el "
            "**SGMXA-30A** (3,0 kW, 3.000 rpm, baja inercia). El SGMXG-30A también "
            "es compatible, pero el fabricante lo declara a 2,4 kW con este "
            "amplificador. Comprueba siempre la relación de inercias antes de "
            "cerrar la elección.",
        ),
        notes=(
            "Este es probablemente el criterio de ingeniería más valioso del curso. "
            "La mayoría de los ejes 'que vibran y no hay manera de ajustar' son ejes "
            "con motor de baja inercia acoplado directamente a una carga de gran "
            "inercia.\n\n"
            "Explique la física: una reducción de relación i multiplica el par por i "
            "y divide la inercia reflejada por i². La reducción es la herramienta más "
            "potente para arreglar una relación de inercias mala, pero introduce "
            "holgura y un punto de mantenimiento.\n\n"
            "Dato que conviene remarcar, tomado de la tabla de combinaciones del "
            "manual (apartado 1.5): el SGMXG-30A figura como 2,9 kW, pero con una "
            "nota al pie que indica 2,4 kW cuando se usa con un SERVOPACK "
            "SGDXS-200A. Es exactamente el tipo de detalle que se pasa por alto en "
            "un proyecto y aparece después como falta de par.\n\n"
            "Los valores de par son de catálogo y varían con la versión exacta del "
            "motor; verifíquelos antes de calcular."
        ),
    )

    _diagrama_codigo_motor(d)

    d.table_slide(
        "Ficha del motor de ejemplo: SGMXA-30A",
        ["Característica", "Valor de referencia", "Para qué se usa el dato"],
        [
            ["Potencia nominal", "3,0 kW", "Debe coincidir con el SERVOPACK"],
            ["Par nominal (continuo)", "≈ 9,55 N·m",
             "Comparar con el par RMS del ciclo"],
            ["Par máximo instantáneo", "≈ 28,6 N·m (≈ 300 %)",
             "Comparar con el par de aceleración"],
            ["Corriente nominal", "≈ 18,5 A eficaces",
             "Dimensionar cable de motor y protecciones"],
            ["Corriente máxima instantánea", "≈ 55 A eficaces",
             "Comprobar la capacidad de pico del drive"],
            ["Velocidad nominal / máxima", "3.000 / 6.000 rpm",
             "Verificar que el ciclo cabe en el rango"],
            ["Inercia del rotor", "Orden de 10⁻³ kg·m² (ver catálogo)",
             "Base del cálculo de la relación de inercias"],
            ["Encoder", "Serie absoluto de 24 bits, multivuelta",
             "Resolución y necesidad de batería"],
            ["Aislamiento / clase térmica", "Clase F o superior",
             "Margen térmico admisible"],
            ["Grado de protección", "IP67 (excepto salida de eje y conectores)",
             "Idoneidad para entornos húmedos"],
            ["Freno de retención", "Opcional, 24 V CC",
             "Obligatorio en ejes verticales"],
            ["Vibración / equilibrado", "Clase V15 típica",
             "Calidad de acabado en aplicaciones de precisión"],
        ],
        [3.0, 3.7, 4.3],
        subtitle="Los datos que realmente se usan en el cálculo",
        size=10.0,
        foot="Los valores exactos (sobre todo la inercia del rotor) dependen de la "
             "variante concreta: consúltalos en el catálogo Σ-X antes de dimensionar.",
        notes=(
            "Marque en la tabla los cuatro datos que se usarán en el Módulo 04: par "
            "nominal, par máximo, velocidad nominal e inercia del rotor. El resto son "
            "datos de instalación.\n\n"
            "Una observación honesta: la inercia del rotor cambia bastante entre "
            "familias y entre versiones con y sin freno. El freno de retención añade "
            "inercia y hay que incluirla en el cálculo."
        ),
    )

    d.bullets_slide(
        "El encoder absoluto de 24 bits y su batería",
        [
            "#Qué aporta",
            "La máquina **conoce su posición al arrancar**: no hay búsqueda de "
            "origen, no hay riesgo de colisión en el homing y el arranque tras un "
            "corte es inmediato.",
            "Mantiene la cuenta de **vueltas completas** (multivuelta) mediante un "
            "contador alimentado por batería cuando el drive está sin tensión.",
            "",
            "#Puesta en servicio",
            "Tras la primera instalación o tras cambiar la batería con el equipo sin "
            "tensión hay que ejecutar el **setup del encoder absoluto** (`Fn008`) y "
            "volver a establecer el origen de la máquina.",
            "- `Pn205` fija el **límite multivuelta**. En ejes rotativos infinitos "
            "hay que configurarlo de acuerdo con la relación de transmisión; si no, "
            "aparecen saltos de posición al desbordar el contador.",
            "",
            "#Batería: el punto débil",
            "Vida típica de unos **3 años** según horas sin tensión. Genera aviso "
            "`A.930` (batería baja) antes de fallar.",
            "- Sustitúyela **con la alimentación de control conectada**: así no se "
            "pierde el contaje y no hay que rehacer el origen.",
            "- Si se agota sin tensión → alarma `A.810` (fallo de respaldo). Hay que "
            "ejecutar `Fn008` y **rehacer el origen de la máquina**.",
            "- Puede alojarse en el drive (unidad de batería) o en el cable de "
            "encoder. **No montes las dos a la vez.**",
        ],
        subtitle="La función que elimina el homing… si la mantienes viva",
        callout=(
            "amber",
            "Plan de mantenimiento recomendado",
            "Sustitución preventiva de baterías cada 2 años, con la máquina "
            "energizada, registrando la fecha en el historial. Y guarda siempre una "
            "copia de los parámetros y del valor de origen de cada eje.",
        ),
        notes=(
            "Cuente el caso típico: parada de planta de tres semanas en agosto, "
            "armarios sin tensión, y a la vuelta cuatro ejes con A.810 y todos los "
            "orígenes perdidos. Es un día entero de trabajo que se evita con "
            "20 euros de baterías y un procedimiento.\n\n"
            "Detalle importante y poco conocido: montar batería en el drive Y en el "
            "cable a la vez puede producir corrientes de circulación entre ambas. "
            "Elija una de las dos ubicaciones."
        ),
    )

    _diagrama_freno(d)

    d.table_slide(
        "Conectores, cables y protección del motor",
        ["Elemento", "Detalle", "Buena práctica"],
        [
            ["Conector de potencia", "Conector redondo tipo militar en tamaños "
             "medios y grandes como el de 3 kW",
             "Orientable: pídelo con el ángulo adecuado al montaje"],
            ["Conector de encoder", "Conector independiente con cable apantallado",
             "**Nunca** compartas canaleta con la potencia"],
            ["Conector del freno", "Dos hilos, 24 V CC, sin polaridad en muchos "
             "modelos", "Alimentación exclusiva; no la compartas con las E/S"],
            ["Longitud de cable", "Hasta 20 m estándar; más con cable especial",
             "Cables largos aumentan capacidad parásita y ruido"],
            ["Apantallamiento", "Malla conectada a tierra en **ambos** extremos",
             "Es la medida antirruido más eficaz"],
            ["Grado de protección", "IP67 en el cuerpo del motor",
             "La salida de eje y los conectores no son estancos"],
            ["Montaje", "Brida normalizada, chavetero opcional",
             "Verifica cargas radial y axial admisibles"],
            ["Sentido de montaje", "Conectores hacia abajo si hay riesgo de goteo",
             "Evita el efecto sifón por el cable"],
        ],
        [2.6, 4.6, 4.2],
        subtitle="El 30 % de las averías de un servo están en los cables",
        size=10.0,
        notes=(
            "Insista en tres cosas: cable original, malla a tierra en ambos extremos "
            "y separación física respecto a los cables de potencia (mínimo 30 cm en "
            "paralelo, cruces a 90°).\n\n"
            "El 'efecto sifón' del último punto es real: el agua recorre el cable y "
            "entra por el conector si éste queda hacia arriba. Se resuelve dejando un "
            "bucle de goteo antes del conector."
        ),
    )

    d.two_col_slide(
        "Combinaciones homologadas motor–SERVOPACK",
        (
            "Por qué existen",
            [
                "El SERVOPACK guarda internamente los datos del motor: constante de "
                "par, resistencia, inductancia, curva térmica y resolución del "
                "encoder.",
                "Al energizar, el drive **lee el motor a través del encoder** y "
                "comprueba que la combinación es válida.",
                "- Si no lo es, aparece una alarma de combinación no admitida "
                "(familia `A.05_`) y el eje no arranca.",
                "- Por eso no se 'parametriza' un motor de otra marca en un "
                "SERVOPACK: la Σ-X sólo trabaja con motores YASKAWA compatibles.",
            ],
        ),
        (
            "Consecuencias prácticas",
            [
                "**Compra siempre la pareja** indicada en el catálogo. Para 3 kW: "
                "SGDXS-200A00A con SGMXA-30A o con SGMXG-30A.",
                "Al sustituir un motor averiado, comprueba que el nuevo tiene el "
                "**mismo código completo**, incluidos freno y tipo de eje.",
                "Un motor con freno y otro sin freno **no son intercambiables** a "
                "efectos de inercia y de secuencia de parada.",
                "Tras cambiar el motor: ejecuta `Fn008` (encoder absoluto), rehaz el "
                "origen y **vuelve a sintonizar** el eje.",
                "- La sintonización previa puede no ser válida si cambia la inercia "
                "del conjunto.",
            ],
        ),
        subtitle="No se mezclan piezas: se eligen conjuntos",
        tones=("blue", "amber"),
        notes=(
            "Esta diapositiva evita disgustos en almacén. Explique que un motor "
            "aparentemente idéntico puede diferir en el tipo de encoder (absoluto vs "
            "incremental), en el freno o en el eje (con o sin chavetero), y que todo "
            "eso está en el código.\n\n"
            "Consejo de gestión: mantenga en el CMMS el código completo de cada "
            "conjunto motor+drive por eje, con foto de las dos etiquetas. Ahorra "
            "horas cuando hay que pedir un repuesto urgente."
        ),
    )


# --------------------------------------------------------------------------
# Diagramas
# --------------------------------------------------------------------------

def _diagrama_codigo_motor(d: Deck) -> None:
    slide = d.canvas_slide(
        "Código de modelo del servomotor",
        "Ejemplo: SGMXA-30A7A61 (estructura orientativa)",
        notes=(
            "Lo importante no es memorizar los códigos, sino saber que en la "
            "referencia del motor están codificados el freno, el tipo de eje y el "
            "encoder. Es lo que hace que dos motores 'iguales' no sean "
            "intercambiables.\n\n"
            "Al pedir un repuesto hay que transcribir el código COMPLETO de la placa, "
            "carácter a carácter. Recomiende fotografiar la placa en lugar de "
            "copiarla a mano."
        ),
    )

    campos = [
        ("SGMX", "Serie Σ-X", NAVY),
        ("A", "Familia\nA = baja inercia\nG = alto par", BLUE),
        ("30", "Capacidad\n30 → 3,0 kW", RED),
        ("A", "Tensión\nA = 200 V", CYAN),
        ("7", "Encoder\n24 bits absoluto", GREEN),
        ("A61", "Diseño, eje,\nfreno y opciones", AMBER),
    ]
    x = Inches(0.9)
    y = Inches(2.0)
    h = Inches(1.05)
    anchos = [Inches(1.75), Inches(2.05), Inches(1.6), Inches(1.35),
              Inches(2.0), Inches(2.7)]
    for (codigo, desc, color), w in zip(campos, anchos):
        d.box(slide, x, y, w, h, codigo, color, size=22, radius=0.08)
        d.label(slide, x - Inches(0.15), y + h + Inches(0.16), w + Inches(0.3),
                desc, size=10.5, color=color, bold=True)
        x += w + Inches(0.14)

    d.callout(slide, Inches(0.9), Inches(4.15), Inches(11.55), Inches(1.05),
              "amber", "Los tres campos que se olvidan y luego dan problemas",
              "1) Freno de retención: un motor con freno y otro sin freno tienen "
              "distinta inercia, distinta longitud y distinto cableado.   "
              "2) Tipo de eje: recto, con chavetero o con taladro roscado.   "
              "3) Tipo de encoder: absoluto o incremental cambia la puesta en marcha "
              "completa del eje.")

    d._rect(slide, Inches(0.9), Inches(5.45), Inches(11.55), Inches(1.2),
            fill=LIGHT, line=GRAY_LINE)
    d._text(slide, Inches(1.15), Inches(5.62), Inches(11.0), Inches(0.3),
            "Ejercicio de clase", size=Pt(12.5), color=NAVY, bold=True)
    d._text(slide, Inches(1.15), Inches(5.95), Inches(11.0), Inches(0.6),
            "Fotografía la placa del motor de tu máquina y decodifica: familia, "
            "capacidad, tensión, tipo de encoder y si lleva freno. Después busca en "
            "el catálogo la combinación de SERVOPACK homologada y comprueba que "
            "coincide con la instalada.", size=Pt(11.5), color=GRAY, spacing=1.1)


def _diagrama_freno(d: Deck) -> None:
    slide = d.canvas_slide(
        "El freno de retención y su secuencia",
        "No es un freno de servicio: sólo mantiene la carga parada",
        notes=(
            "Concepto que hay que dejar grabado: el freno de retención es "
            "ELECTROMAGNÉTICO Y NORMALMENTE CERRADO. Sin 24 V está frenado. Sirve "
            "para sostener la carga con el servo desactivado, no para frenar en "
            "movimiento. Frenar con él a velocidad destruye el forro en pocos "
            "ciclos.\n\n"
            "La secuencia importa mucho en ejes verticales:\n"
            "· Al arrancar: primero servo ON (el motor sostiene la carga), después "
            "liberar el freno. Si se libera antes, la carga cae unos milímetros.\n"
            "· Al parar: primero cerrar el freno, esperar a que agarre, y sólo "
            "entonces quitar el par. Pn506 y Pn508 gobiernan estos retardos.\n\n"
            "Parámetros implicados: Pn506 (retardo entre orden de freno y servo OFF "
            "con el motor parado), Pn507 (velocidad por debajo de la cual se aplica "
            "el freno con el motor en marcha), Pn508 (tiempo de espera antes de "
            "quitar el par tras ordenar el freno). La señal de salida es /BK y hay "
            "que asignarla a una salida física con Pn50F.\n\n"
            "Advertencia de seguridad: el freno de retención NO es un elemento de "
            "seguridad certificado por sí solo. Para proteger a una persona bajo una "
            "carga suspendida hace falta un análisis de riesgos específico."
        ),
    )

    # Línea de tiempo
    x0, x1 = Inches(1.4), Inches(11.9)
    filas = [
        ("Orden /S-ON", BLUE, [(0.10, 0.86)]),
        ("Par en el motor", CYAN, [(0.13, 0.90)]),
        ("Salida /BK (freno)", GREEN, [(0.22, 0.78)]),
        ("Movimiento", AMBER, [(0.30, 0.70)]),
    ]
    y = Inches(2.15)
    fila_h = Inches(0.82)
    for etiqueta, color, tramos in filas:
        d._text(slide, Inches(0.25), y + Inches(0.10), Inches(1.05),
                Inches(0.4), etiqueta, size=Pt(9.5), color=color, bold=True,
                align=PP_ALIGN.RIGHT)
        d.line(slide, x0, y + Inches(0.52), x1, y + Inches(0.52),
               color=GRAY_LINE, width=Pt(1))
        for a, b in tramos:
            xa = x0 + (x1 - x0) * a
            xb = x0 + (x1 - x0) * b
            d._rect(slide, xa, y + Inches(0.12), xb - xa, Inches(0.40),
                    fill=color)
        y += fila_h

    # Marcas verticales
    marcas = [
        (0.10, "1  Servo ON", NAVY),
        (0.22, "2  Liberar freno", GREEN),
        (0.30, "3  Mover", AMBER),
        (0.70, "4  Parar", AMBER),
        (0.78, "5  Aplicar freno\n`Pn507`", GREEN),
        (0.90, "6  Servo OFF\n`Pn506` / `Pn508`", NAVY),
    ]
    for frac, texto, color in marcas:
        x = x0 + (x1 - x0) * frac
        d.line(slide, x, Inches(2.05), x, Inches(5.55), color=color,
               width=Pt(1), dash=True)
        d.label(slide, x - Inches(0.95), Inches(5.58), Inches(1.9), texto,
                size=9, color=color, bold=True)

    d.callout(slide, Inches(0.62), Inches(5.98), Inches(12.05), Inches(0.94),
              "red", "Errores que cuestan un motor",
              "Usar el freno para detener el eje en marcha (se quema en semanas) · "
              "Alimentar el freno desde la misma fuente que las E/S (la caída de "
              "tensión al liberarlo provoca fallos erráticos) · Quitar el par antes "
              "de que el freno haya agarrado en un eje vertical (la carga cae).")
