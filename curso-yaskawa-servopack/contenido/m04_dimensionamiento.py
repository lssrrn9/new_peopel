"""Módulo 4 — Dimensionamiento y selección del conjunto."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, GRAY, GRAY_LINE, GREEN, INK, LIGHT,
                     LIGHT_BLUE, NAVY, RED, WHITE, Card, Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 04",
        "Dimensionamiento y selección",
        [
            "Los datos de partida que hay que obtener de la máquina",
            "Cálculo de la inercia reflejada al eje del motor",
            "La relación de inercias y por qué condiciona la sintonización",
            "Perfil de movimiento, par de aceleración y par eficaz (RMS)",
            "Energía regenerativa y resistencia de frenado",
            "Ejemplo numérico completo de un eje de 3 kW",
        ],
        duration="4 h",
        notes=(
            "Este es el módulo con más contenido de ingeniería y el que marca la "
            "diferencia entre un técnico y un especialista. Tómese el tiempo "
            "necesario: si el grupo entiende el ejemplo numérico, entenderá "
            "cualquier eje.\n\n"
            "Tenga a mano una calculadora y, si es posible, una hoja de cálculo "
            "proyectada para repetir el ejemplo cambiando datos."
        ),
    )

    d.bullets_slide(
        "Por qué el dimensionamiento decide el resultado",
        [
            "#Lo que ocurre cuando el motor se queda corto",
            "El eje **no alcanza** la aceleración pedida: el ciclo se alarga y la "
            "producción no llega al objetivo.",
            "Aparecen alarmas de **sobrecarga** (`A.710` instantánea, `A.720` "
            "continua) que paran la máquina de forma intermitente e inexplicable "
            "para el operario.",
            "Se dispara el **error de seguimiento** (`A.d00`) porque el eje no "
            "puede seguir la consigna.",
            "",
            "#Lo que ocurre cuando el motor está sobredimensionado",
            "Coste innecesario en motor, drive, cable y armario.",
            "**Relación de inercias muy baja**: el sistema es fácil de sintonizar, "
            "pero se paga precisión por la resolución relativa y se aumenta el "
            "consumo en vacío.",
            "En muchos casos el problema real es que el motor grande no cabe o "
            "exige rediseñar la mecánica.",
            "",
            "#Lo que ocurre cuando la relación de inercias es mala",
            "El eje **vibra** y no hay ajuste de ganancias que lo arregle: se oscila "
            "entre 'lento pero estable' y 'rápido pero ruidoso'.",
            "- Este caso es el más frustrante porque parece un problema de "
            "sintonización y en realidad es un problema de selección.",
        ],
        subtitle="El 80 % de los problemas de un eje nacen aquí",
        callout=(
            "blue",
            "Objetivo del módulo",
            "Aprender a justificar con números, en menos de una hora, que un conjunto "
            "SGD7S-200A + motor de 3 kW es (o no es) el adecuado para una máquina "
            "concreta.",
        ),
        notes=(
            "Pida ejemplos al grupo de ejes que 'nunca han ido bien'. Casi siempre "
            "aparecerán síntomas de esta diapositiva.\n\n"
            "Mensaje que hay que repetir a lo largo del módulo: sintonizar no arregla "
            "un dimensionamiento equivocado. Sólo lo disimula."
        ),
    )

    d.table_slide(
        "Datos de partida: qué hay que averiguar antes de calcular",
        ["Dato", "Símbolo", "Cómo obtenerlo", "Ejemplo del curso"],
        [
            ["Masa que se desplaza", "m [kg]", "Plano de la máquina o báscula",
             "400 kg"],
            ["Recorrido por ciclo", "s [m]", "Especificación del proceso", "0,6 m"],
            ["Tiempo de movimiento", "t [s]", "Objetivo de producción", "1,0 s"],
            ["Tiempo total de ciclo", "T [s]", "Cadencia exigida",
             "2,5 s"],
            ["Paso del husillo", "p [m/vuelta]", "Catálogo del husillo",
             "0,020 m"],
            ["Diámetro y longitud del husillo", "D, L [m]", "Plano mecánico",
             "40 mm × 1,5 m"],
            ["Relación de transmisión", "i", "Reductor o polea", "1 : 1 (directo)"],
            ["Coeficiente de rozamiento", "μ", "Tipo de guía (0,003-0,05)", "0,05"],
            ["Rendimiento mecánico", "η", "Husillo + acoplamiento (0,85-0,95)",
             "0,90"],
            ["Fuerza de proceso", "F_p [N]", "Corte, prensado, empuje",
             "0 (traslado libre)"],
            ["Orientación del eje", "—", "Horizontal, vertical o inclinado",
             "Horizontal"],
        ],
        [3.1, 1.5, 3.9, 2.3],
        subtitle="Sin estos once datos no se puede dimensionar nada",
        size=10.0,
        foot="Si algún dato no se conoce, hay que estimarlo por exceso y dejarlo "
             "documentado como hipótesis: el cálculo se revisa cuando se confirme.",
        notes=(
            "Advierta de que el dato que más se falsea es la masa: se olvidan las "
            "piezas transportadas, la herramienta, la mesa y los cables. Multiplique "
            "por un factor de seguridad si hay dudas.\n\n"
            "El segundo dato más traicionero es el tiempo de movimiento: comercial "
            "vende '30 ciclos por minuto' y nadie ha comprobado si eso es físicamente "
            "posible con la mecánica prevista. Este cálculo sirve precisamente para "
            "responder a esa pregunta antes de comprar."
        ),
    )

    d.bullets_slide(
        "Paso 1 — Inercia reflejada al eje del motor",
        [
            "#La regla fundamental",
            "El motor sólo 'siente' la inercia **vista desde su eje**. Todo lo que "
            "hay detrás de una reducción de relación *i* se divide por *i²*.",
            "",
            "#Fórmulas que necesitas",
            "**Masa en traslación con husillo**: `J = m · (p / 2π)²`  [kg·m²], con "
            "*p* en m/vuelta.",
            "**Cilindro macizo (husillo, rodillo, acoplamiento)**: "
            "`J = ½ · m · r²`, con `m = ρ · π · r² · L` y ρ(acero) = 7.850 kg/m³.",
            "**A través de una reducción i:1**: `J_reflejada = J_carga / i²`.",
            "**Correa/piñón-cremallera**: `J = m · r²` con *r* el radio primitivo del "
            "piñón motriz.",
            "",
            "#Qué no hay que olvidar",
            "- El **acoplamiento** y las poleas: en ejes rápidos pueden ser una parte "
            "importante del total.",
            "- El propio **husillo**: en husillos largos y gruesos puede superar a la "
            "carga.",
            "- El **freno de retención**, si el motor lo lleva: suma inercia al rotor.",
            "- La **carga transportada variable**: calcula con el caso más "
            "desfavorable.",
        ],
        subtitle="Todo se traduce a kg·m² en el eje del motor",
        callout=(
            "green",
            "La reducción es la herramienta más potente que tienes",
            "Una reducción 3:1 multiplica el par por 3 y divide la inercia reflejada "
            "por 9. Es la forma habitual de convertir un eje imposible de sintonizar "
            "en uno cómodo… a cambio de holgura, coste y mantenimiento.",
        ),
        notes=(
            "Deduzca en pizarra la fórmula del husillo: en una vuelta el motor "
            "avanza p metros, luego la relación de transmisión equivalente es "
            "p/2π metros por radián. La inercia equivalente de una masa m en "
            "traslación con ese 'radio efectivo' es m·(p/2π)².\n\n"
            "Numéricamente: con p = 20 mm, el radio efectivo es 3,18 mm. Una masa de "
            "400 kg 'pesa' inercialmente lo mismo que un volante de 400 kg a 3,18 mm "
            "de radio: 40,5×10⁻⁴ kg·m². Sorprendentemente poco, y por eso los "
            "husillos de paso fino son tan cómodos para el servo (pero limitan la "
            "velocidad)."
        ),
    )

    d.two_col_slide(
        "Paso 2 — La relación de inercias",
        (
            "Qué es y cómo se calcula",
            [
                "`R = J_carga reflejada / J_rotor del motor`",
                "Es el parámetro que mejor predice si un eje va a ser fácil o difícil "
                "de sintonizar.",
                "El SERVOPACK lo necesita: se guarda en `Pn103` (relación de inercias, "
                "en %). El autotuning lo estima automáticamente.",
                "- `Pn103` = 100 significa que la carga tiene la misma inercia que el "
                "rotor (relación 1:1).",
                "#Por qué importa",
                "Con inercia de carga muy superior, la elasticidad del acoplamiento "
                "hace que motor y carga oscilen entre sí: aparece **resonancia** y el "
                "límite de ganancia baja mucho.",
            ],
        ),
        (
            "Valores de referencia",
            [
                "**Hasta 3:1** — Excelente. Sintonización trivial, dinámica máxima.",
                "**De 3:1 a 10:1** — Zona normal de trabajo. Se ajusta bien con "
                "autotuning.",
                "**De 10:1 a 20:1** — Exigente. Requiere acoplamiento muy rígido, "
                "filtros notch y ajuste manual.",
                "**Más de 20:1** — Sólo con motores de alta inercia (SGM7G), "
                "mecánica muy rígida y expectativas de dinámica moderadas.",
                "#Cómo mejorar una relación mala",
                "- Añadir o aumentar la **reducción** (efecto i²).",
                "- Cambiar a un motor de **mayor inercia de rotor**.",
                "- Aumentar la **rigidez** del acoplamiento y de los soportes.",
                "- Reducir la masa desplazada.",
            ],
        ),
        subtitle="El indicador que predice si el eje va a dar guerra",
        tones=("blue", "cyan"),
        callout=(
            "amber",
            "Matiz importante",
            "Los límites anteriores son orientativos: con una mecánica muy rígida se "
            "trabajan bien relaciones de 15:1, y con una mecánica elástica una "
            "relación de 5:1 ya puede resonar. La rigidez importa tanto como la "
            "relación.",
        ),
        notes=(
            "Analogía útil: llevar de la mano a un niño (relación baja, controlas el "
            "movimiento) frente a tirar de un remolque pesado con una cuerda elástica "
            "(relación alta con acoplamiento blando: el remolque hace lo que quiere).\n\n"
            "Dato práctico: Pn103 mal ajustado es una causa muy frecuente de "
            "comportamiento extraño. Si el autotuning estima 300 % y alguien lo deja "
            "en 0 %, el lazo de velocidad queda mal escalado y el eje responde lento "
            "o inestable."
        ),
    )

    _diagrama_perfil(d)

    d.bullets_slide(
        "Paso 4 — Par eficaz (RMS) y verificación térmica",
        [
            "#Por qué el par RMS",
            "El motor puede dar un par muy alto durante poco tiempo, pero lo que "
            "determina su **calentamiento** es el valor eficaz del par a lo largo "
            "del ciclo completo, incluidas las paradas.",
            "",
            "#Fórmula",
            "`T_rms = √[ (T₁²·t₁ + T₂²·t₂ + … + Tₙ²·tₙ) / T_ciclo ]`",
            "- Los tiempos de parada **entran en el denominador** con par cero: "
            "alargar la pausa reduce el par eficaz. Por eso un mismo movimiento puede "
            "ser válido a 20 ciclos/min y no serlo a 40.",
            "",
            "#Criterios de aceptación",
            "**T_rms ≤ 0,8 × par nominal** del motor → margen del 20 % para "
            "desgaste, suciedad, temperatura ambiente y variación de la carga.",
            "**T_pico ≤ 0,8 × par máximo** del motor.",
            "**n_máx del ciclo ≤ 0,9 × velocidad máxima** del motor, y siempre dentro "
            "de la curva par-velocidad a la tensión mínima de red.",
            "",
            "#Correcciones que suelen olvidarse",
            "- Temperatura ambiente elevada dentro del armario o junto a la máquina.",
            "- Altitud superior a 1.000 m (menor capacidad de refrigeración).",
            "- Motor con freno o con reductor montado: más inercia y más pérdidas.",
        ],
        subtitle="La comprobación que evita las alarmas `A.720`",
        notes=(
            "Explique por qué se eleva al cuadrado: las pérdidas por efecto Joule son "
            "proporcionales a I², y el par es proporcional a I. Por eso un pico "
            "de par corto pesa mucho en el valor eficaz.\n\n"
            "Ejercicio mental muy útil: si se duplica la cadencia de la máquina (la "
            "mitad de tiempo de ciclo con el mismo movimiento), el par RMS se "
            "multiplica por √2 ≈ 1,41. Es la forma rápida de responder a la pregunta "
            "'¿puedo ir más rápido con este motor?'."
        ),
    )

    d.table_slide(
        "Ejemplo completo (1/2) — Datos y cálculo cinemático",
        ["Paso", "Cálculo", "Resultado"],
        [
            ["Perfil de movimiento",
             "Trapezoidal simétrico: t_acel = t_decel = 0,25 s, t_const = 0,5 s, "
             "t_mov = 1,0 s", "—"],
            ["Velocidad lineal máxima", "v = s / (t_mov − t_acel) = 0,6 / 0,75",
             "**0,8 m/s**"],
            ["Aceleración lineal", "a = v / t_acel = 0,8 / 0,25", "**3,2 m/s²**"],
            ["Velocidad del motor", "n = v / p × 60 = 0,8 / 0,020 × 60",
             "**2.400 rpm** (< 3.000 ✔)"],
            ["Aceleración angular", "α = 2π·n/60 / t_acel = 251,3 / 0,25",
             "**1.005 rad/s²**"],
            ["Inercia de la masa", "J₁ = m·(p/2π)² = 400 × (0,020/6,2832)²",
             "**40,5 × 10⁻⁴ kg·m²**"],
            ["Inercia del husillo",
             "m_h = ρ·π·r²·L = 14,8 kg → J₂ = ½·m_h·r² = ½ × 14,8 × 0,02²",
             "**29,6 × 10⁻⁴ kg·m²**"],
            ["Acoplamiento (catálogo)", "J₃", "**2,0 × 10⁻⁴ kg·m²**"],
            ["Inercia total de carga", "J_L = J₁ + J₂ + J₃",
             "**72,1 × 10⁻⁴ kg·m²**"],
            ["Relación de inercias",
             "R = J_L / J_rotor (≈ 19 × 10⁻⁴ kg·m² para el SGM7A-30A)",
             "**≈ 3,8 : 1 ✔ zona cómoda**"],
        ],
        [2.7, 5.9, 3.5],
        subtitle="Eje horizontal con husillo de bolas, 400 kg, 600 mm en 1 s",
        size=9.5,
        foot="La inercia del rotor es un valor de catálogo que depende de la variante "
             "exacta del motor (con o sin freno): confírmala antes de dar el cálculo "
             "por bueno.",
        notes=(
            "Haga el cálculo en pizarra o en hoja de cálculo en paralelo. Es "
            "importante que vean que no hay magia: son cuatro fórmulas.\n\n"
            "Comente el resultado de la inercia: la masa de 400 kg contribuye 40,5 y "
            "el husillo, que 'sólo' pesa 14,8 kg, contribuye 29,6. En husillos largos "
            "y gruesos, el husillo puede dominar el cálculo. Es un resultado "
            "contraintuitivo que conviene remarcar.\n\n"
            "Si el grupo quiere jugar: pregunte qué pasa si se duplica el paso a "
            "40 mm. La inercia de la masa se multiplica por 4 (162×10⁻⁴), la "
            "velocidad del motor se reduce a la mitad (1.200 rpm) y el par sube. Es "
            "el compromiso clásico del husillo."
        ),
    )

    d.table_slide(
        "Ejemplo completo (2/2) — Par, verificación y regeneración",
        ["Paso", "Cálculo", "Resultado"],
        [
            ["Par de fricción",
             "F = μ·m·g = 0,05 × 400 × 9,81 = 196 N → T_f = F·p/(2π·η) + precarga",
             "**≈ 1,0 N·m**"],
            ["Par de aceleración de la carga", "T = J_L·α/η = 72,1e-4 × 1005 / 0,9",
             "**8,05 N·m**"],
            ["Par de aceleración del rotor", "T = J_rotor·α = 19e-4 × 1005",
             "**1,91 N·m**"],
            ["**Par pico (aceleración)**", "T_pico = 8,05 + 1,91 + 1,0",
             "**≈ 10,95 N·m**"],
            ["Par a velocidad constante", "Sólo fricción", "**≈ 1,0 N·m**"],
            ["Par de deceleración", "T = −(8,05 + 1,91) + 1,0 (la fricción ayuda)",
             "**≈ −8,96 N·m**"],
            ["**Par eficaz del ciclo**",
             "T_rms = √[(10,95²×0,25 + 1,0²×0,5 + 8,96²×0,25) / 2,5]",
             "**≈ 4,5 N·m**"],
            ["Verificación continua", "4,5 N·m frente a 9,55 N·m nominales",
             "**47 % ✔ margen amplio**"],
            ["Verificación de pico", "10,95 N·m frente a ≈ 28,6 N·m máximos",
             "**38 % ✔**"],
            ["Energía cinética a frenar", "E = ½·J_total·ω² = ½ × 91e-4 × 251,3²",
             "**≈ 288 J por frenado**"],
            ["Potencia media de regeneración",
             "Descontando fricción y pérdidas (≈ 60 %) y repartido en 2,5 s",
             "**≈ 70 W → resistencia interna suficiente**"],
        ],
        [2.9, 6.0, 3.2],
        subtitle="Conclusión: el conjunto SGD7S-200A + SGM7A-30A es adecuado",
        size=9.5,
        foot="Los porcentajes de utilización (47 % continuo y 38 % de pico) indican "
             "que incluso podría estudiarse un motor menor; conviene comprobar antes "
             "la relación de inercias resultante.",
        notes=(
            "Cierre el ejemplo con la lectura de ingeniería: el eje está holgado en "
            "par, lo que da margen para aumentar cadencia en el futuro. Pero al bajar "
            "de tamaño de motor la inercia del rotor cae y la relación de inercias "
            "empeora, con lo que la sintonización se complica. Ese compromiso —par "
            "sobrado frente a relación de inercias— es la esencia del oficio.\n\n"
            "Sobre la regeneración: el cálculo de 288 J es la energía cinética total. "
            "Parte se disipa en la fricción y en las pérdidas del motor y del drive, "
            "y parte la absorben los condensadores del bus. Lo que llega a la "
            "resistencia es bastante menos. Por eso el criterio práctico es comparar "
            "la potencia media de regeneración con la capacidad de la resistencia "
            "interna, y ante la duda, medir en la puesta en marcha con la función de "
            "traza.\n\n"
            "Los ejes verticales son el caso crítico de regeneración: al bajar, la "
            "gravedad aporta energía de forma continua y la resistencia interna se "
            "queda corta casi siempre."
        ),
    )

    d.two_col_slide(
        "Regeneración: cuándo hace falta resistencia externa",
        (
            "Cuándo la interna no basta",
            [
                "**Ejes verticales** que bajan con carga: la gravedad inyecta energía "
                "durante todo el descenso.",
                "**Grandes inercias** que frenan con frecuencia: volantes, bobinas, "
                "mesas rotativas pesadas.",
                "**Ciclos muy rápidos**: aunque cada frenado devuelva poca energía, "
                "la potencia media se acumula.",
                "**Frenados de emergencia** repetidos desde velocidad máxima.",
                "- Síntoma inequívoco: alarma `A.400` (sobretensión) al frenar, o "
                "`A.320` (sobrecarga de regeneración).",
            ],
        ),
        (
            "Cómo se resuelve",
            [
                "Retirar el puente `B2`-`B3` y conectar la resistencia externa entre "
                "`B1/⊕` y `B2`.",
                "Configurar la capacidad de la resistencia en el parámetro "
                "correspondiente (`Pn600`, capacidad de regeneración) para que el "
                "cálculo térmico del drive sea correcto.",
                "- Respetar la **resistencia mínima admisible** del amplificador: un "
                "valor menor daña el transistor de frenado.",
                "- Montarla **fuera del armario** o con ventilación: disipa calor real "
                "y alcanza temperaturas altas.",
                "- Prever **termostato de seguridad** en serie con el circuito de "
                "parada.",
                "#Alternativa",
                "En ejes de gran potencia con regeneración continua, valorar una "
                "unidad de realimentación a red en lugar de quemar la energía.",
            ],
        ),
        subtitle="Qué hacer con la energía que devuelve el motor",
        tones=("red", "green"),
        notes=(
            "Explique el mecanismo: al frenar, el motor genera y la corriente entra "
            "al bus de continua elevando su tensión. Cuando supera un umbral "
            "(alrededor de 400 V), el drive conecta el transistor de frenado y quema "
            "la energía en la resistencia. Si la energía es mayor que la que la "
            "resistencia puede disipar, la tensión sigue subiendo hasta A.400.\n\n"
            "Advertencia práctica: la resistencia externa puede superar los 200 °C. "
            "Nunca se monta pegada a cables ni bajo materiales sensibles, y siempre "
            "se cablea con conductor resistente a temperatura.\n\n"
            "Recuerde configurar Pn600: si se monta una resistencia externa y no se "
            "declara, el drive sigue calculando con la interna y protege mal."
        ),
    )

    d.steps_slide(
        "Procedimiento de dimensionamiento en 8 pasos",
        [
            ("Recoger los datos de la máquina",
             "Masa, recorrido, tiempos, transmisión, fricción, orientación y fuerza "
             "de proceso. Documenta las hipótesis."),
            ("Definir el perfil de movimiento",
             "Trapezoidal o en S. Calcular velocidad máxima, aceleración y velocidad "
             "del motor."),
            ("Calcular la inercia reflejada",
             "Sumar carga, husillo, acoplamiento y transmisión, todo referido al eje "
             "del motor."),
            ("Preseleccionar el motor",
             "Por par nominal ≈ par RMS estimado y por velocidad máxima. Comprobar la "
             "relación de inercias."),
            ("Calcular los pares del ciclo",
             "Aceleración, régimen constante, deceleración y mantenimiento. Incluir "
             "fricción, gravedad y proceso."),
            ("Verificar pico y RMS contra la curva",
             "T_pico ≤ 80 % del máximo y T_rms ≤ 80 % del nominal, a la tensión "
             "mínima de red."),
            ("Comprobar la regeneración",
             "Energía por frenado y potencia media; decidir si hace falta resistencia "
             "externa."),
            ("Documentar y validar en la puesta en marcha",
             "Guardar la hoja de cálculo y comparar después con el par real medido "
             "(`Un002`) y con la traza de SigmaWin+."),
        ],
        subtitle="La secuencia que hay que seguir siempre, en este orden",
        callout=(
            "blue",
            "Herramientas que ahorran tiempo",
            "YASKAWA ofrece software de selección (familia SigmaSelect / SigmaSize) "
            "que automatiza estos cálculos y propone la combinación motor-drive. "
            "Úsalo, pero **entiende primero el cálculo a mano**: sólo así puedes "
            "detectar cuándo el resultado no tiene sentido.",
        ),
        notes=(
            "El paso 8 es el que casi nadie hace y el que más valor aporta: comparar "
            "el cálculo teórico con la medida real en la máquina. Si el par medido es "
            "muy superior al calculado, hay fricción no prevista, desalineación o un "
            "problema mecánico que conviene resolver antes de que rompa algo.\n\n"
            "Sugerencia de trabajo: crear una plantilla de hoja de cálculo corporativa "
            "con estas fórmulas y archivarla junto a la documentación de cada máquina."
        ),
    )


# --------------------------------------------------------------------------
# Diagrama
# --------------------------------------------------------------------------

def _diagrama_perfil(d: Deck) -> None:
    slide = d.canvas_slide(
        "Paso 3 — Perfil de movimiento y par requerido",
        "El par sigue a la aceleración, no a la velocidad",
        notes=(
            "Este diagrama explica visualmente el corazón del dimensionamiento: el "
            "par es alto sólo mientras cambia la velocidad. A velocidad constante "
            "sólo hay que vencer la fricción.\n\n"
            "Señale la asimetría entre aceleración y frenado: al frenar, la fricción "
            "ayuda, por lo que el par de deceleración es algo menor en valor "
            "absoluto. En ejes verticales ocurre lo contrario al subir y bajar, y "
            "hay que calcular ambos sentidos.\n\n"
            "Mencione el perfil en S: suaviza el cambio de aceleración (limita el "
            "'jerk'), reduce la excitación de resonancias y el desgaste mecánico, a "
            "cambio de exigir algo más de par pico para el mismo tiempo de ciclo. En "
            "máquinas con estructura elástica suele compensar."
        ),
    )

    x0, x1 = Inches(1.55), Inches(8.35)
    ancho = x1 - x0

    # --- Gráfica de velocidad
    yv = Inches(3.05)
    hv = Inches(1.15)
    d.line(slide, x0, yv, x1 + Inches(0.35), yv, color=INK, width=Pt(1.25))
    d.line(slide, x0, yv, x0, yv - hv - Inches(0.25), color=INK, width=Pt(1.25))
    d.label(slide, Inches(0.15), yv - hv - Inches(0.55), Inches(2.6),
            "Velocidad  [rpm]", size=10.5, color=INK, bold=True,
            align=PP_ALIGN.LEFT)

    t_a, t_c = 0.25, 0.50
    fa, fc, fd = 0.10, 0.30, 0.20   # fracciones del ancho para acel/const/decel
    xa = x0 + ancho * fa
    xb = xa + ancho * fc
    xc = xb + ancho * fd
    trap = slide.shapes.build_freeform(int(x0), int(yv))
    trap.add_line_segments([(int(xa), int(yv - hv)), (int(xb), int(yv - hv)),
                            (int(xc), int(yv)), (int(x0), int(yv))],
                           close=True)
    shp = trap.convert_to_shape()
    shp.fill.solid()
    shp.fill.fore_color.rgb = LIGHT_BLUE
    shp.line.color.rgb = BLUE
    shp.line.width = Pt(1.75)
    d.label(slide, xa - Inches(0.6), yv - hv - Inches(0.32), Inches(2.2),
            "2.400 rpm", size=10, color=BLUE, bold=True, align=PP_ALIGN.LEFT)

    # --- Gráfica de par
    yt = Inches(5.75)
    ht = Inches(0.95)
    d.line(slide, x0, yt, x1 + Inches(0.35), yt, color=INK, width=Pt(1.25))
    d.line(slide, x0, yt - ht - Inches(0.25), x0, yt + Inches(0.85),
           color=INK, width=Pt(1.25))
    d.label(slide, Inches(0.15), yt - ht - Inches(0.55), Inches(2.6),
            "Par  [N·m]", size=10.5, color=INK, bold=True, align=PP_ALIGN.LEFT)

    # aceleración
    d._rect(slide, x0, yt - ht, xa - x0, ht, fill=RED, line=RED)
    d.label(slide, x0 - Inches(0.05), yt - ht - Inches(0.30), Inches(1.6),
            "+10,95 N·m", size=9.5, color=RED, bold=True)
    # constante
    d._rect(slide, xa, yt - Inches(0.16), xb - xa, Inches(0.16), fill=GREEN,
            line=GREEN)
    d.label(slide, xa, yt - Inches(0.48), Inches(1.9), "+1,0 N·m (fricción)",
            size=9.5, color=GREEN, bold=True, align=PP_ALIGN.LEFT)
    # deceleración
    d._rect(slide, xb, yt, xc - xb, ht * 0.82, fill=AMBER, line=AMBER)
    d.label(slide, xb, yt + ht * 0.82 + Inches(0.04), Inches(1.7),
            "−8,96 N·m", size=9.5, color=AMBER, bold=True, align=PP_ALIGN.LEFT)
    # reposo
    d.label(slide, xc + Inches(0.1), yt - Inches(0.42), Inches(2.6),
            "reposo: par ≈ 0", size=9.5, color=GRAY, align=PP_ALIGN.LEFT)

    for x, txt in ((x0, "0"), (xa, "0,25 s"), (xb, "0,75 s"), (xc, "1,0 s"),
                   (x1 + Inches(0.35), "2,5 s")):
        d.line(slide, x, yt + Inches(0.82), x, yt + Inches(0.92), color=GRAY)
        d.label(slide, x - Inches(0.55), yt + Inches(0.94), Inches(1.1), txt,
                size=9, color=GRAY)
    d.label(slide, x0, yt + Inches(1.22), ancho, "tiempo →", size=10,
            color=INK, bold=True, align=PP_ALIGN.LEFT)

    # Panel de fórmulas
    px = Inches(9.05)
    d._rect(slide, px, Inches(1.72), Inches(3.65), Inches(4.95), fill=LIGHT,
            line=GRAY_LINE)
    d._text(slide, px + Inches(0.25), Inches(1.92), Inches(3.15), Inches(0.35),
            "Los cuatro pares", size=Pt(14), color=NAVY, bold=True)
    tf = slide.shapes.add_textbox(px + Inches(0.25), Inches(2.38), Inches(3.15),
                                  Inches(4.1)).text_frame
    tf.word_wrap = True
    d._fill_bullets(tf, [
        "**Aceleración**: `T = J_total · α`  → el más alto del ciclo.",
        "**Fricción**: `T = μ·m·g·p / (2π·η)` → presente siempre que hay "
        "movimiento.",
        "**Gravedad** (ejes verticales): `T = m·g·p / (2π·η)` → presente **también "
        "en reposo**.",
        "**Proceso**: corte, prensado o empuje, según la fase del ciclo.",
        "",
        "El par que hay que comparar con el catálogo es la **suma** de los que "
        "actúan a la vez.",
    ], size=11)
