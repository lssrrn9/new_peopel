"""Módulo 10 — Seguridad funcional: STO / HWBB."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, FIG, FUENTE, GRAY, GRAY_LINE, GREEN,
                     INK, LIGHT, LIGHT_BLUE, NAVY, RED, WHITE, Card, Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 10",
        "Seguridad funcional: STO / HWBB",
        [
            "El marco normativo en dos diapositivas",
            "Qué es realmente la función HWBB del SERVOPACK",
            "Cableado de `CN8` y señal de vigilancia EDM",
            "STO no es parada de emergencia: diferencias y límites",
            "Validación, documentación y pruebas periódicas",
        ],
        duration="2,5 h",
        notes=(
            "Módulo corto pero crítico. El objetivo no es convertir al alumno en "
            "experto en seguridad de máquinas, sino que sepa qué ofrece el drive, "
            "qué no ofrece, y cuándo hay que llamar a un especialista.\n\n"
            "Advertencia que hay que hacer explícita: el diseño de la función de "
            "seguridad de una máquina requiere un análisis de riesgos y competencias "
            "específicas. Este módulo explica la pieza que aporta el SERVOPACK, no "
            "sustituye a ese análisis."
        ),
    )

    d.two_col_slide(
        "El marco normativo, en lo que afecta al servo",
        (
            "Las normas que vas a oír nombrar",
            [
                "**EN ISO 12100** — Principios generales para el diseño y la "
                "evaluación de riesgos de las máquinas.",
                "**EN ISO 13849-1** — Partes de los sistemas de mando relativas a la "
                "seguridad. Habla de **niveles de prestaciones (PL a … PL e)** y de "
                "categorías de arquitectura.",
                "**IEC 61508 / IEC 62061** — Enfoque de seguridad funcional "
                "electrónica. Habla de **niveles de integridad (SIL 1 … SIL 3)**.",
                "**IEC 61800-5-2** — Define las funciones de seguridad específicas de "
                "los accionamientos: STO, SS1, SS2, SLS, SOS…",
            ],
        ),
        (
            "Lo que aporta el SERVOPACK",
            [
                "La función **STO (Safe Torque Off)**, implementada en la Σ-X como "
                "**HWBB (Hard Wire Baseblock)**.",
                "Capacidad típica declarada de **SIL 3** (IEC 61508) y **PL e / "
                "categoría 3** (ISO 13849-1) cuando se cablea correctamente.",
                "Dos canales independientes de desactivación y una salida de "
                "vigilancia (**EDM**) para que el módulo de seguridad compruebe que "
                "el drive ha respondido.",
                "#Qué NO aporta",
                "- No es una parada de emergencia por sí sola.",
                "- No mantiene la carga en un eje vertical.",
                "- No garantiza que el eje esté parado: garantiza que **no habrá "
                "par**.",
            ],
        ),
        subtitle="Dos familias de normas, un objetivo común",
        tones=("blue", "green"),
        callout=(
            "amber",
            "El nivel de seguridad es del sistema, no del componente",
            "Que el drive sea apto para SIL 3 / PL e no significa que tu máquina lo "
            "sea. El nivel resultante depende de toda la cadena: sensor, lógica de "
            "seguridad, cableado y actuador, y de su diagnóstico.",
        ),
        notes=(
            "El punto del recuadro es el más malinterpretado del módulo. Un "
            "componente 'apto para PL e' insertado en una arquitectura de categoría "
            "1 no da PL e.\n\n"
            "Sobre las funciones de IEC 61800-5-2: STO (par desactivado) es la base y "
            "la que implementa el hardware del drive. Otras funciones como SS1 "
            "(parada controlada seguida de STO) se construyen combinando el drive con "
            "un módulo de seguridad temporizado o con un drive con funciones de "
            "seguridad ampliadas."
        ),
    )

    _diagrama_hwbb(d)


    d.figure_slide(
        "Pines del conector de seguridad `CN8`",
        FIG + "cn8_seguridad.png",
        subtitle="Asignación oficial de las señales HWBB y EDM1",
        puntos=[
            "#Lo que hay que leer en la tabla",
            "Pines **1 y 2**: no se usan, están conectados a circuitos internos. "
            "**No conectes nada.**",
            "Pines **3 y 4**: `/HWBB1−` y `/HWBB1+`, primera entrada de bloqueo.",
            "Pines **5 y 6**: `/HWBB2−` y `/HWBB2+`, segunda entrada de bloqueo.",
            "Pines **7 y 8**: `EDM1−` y `EDM1+`, salida de vigilancia.",
            "#Lógica de las señales",
            "El bloqueo actúa cuando la señal está **OFF** (contacto abierto): un "
            "cable roto lleva al estado seguro.",
            "`EDM1` se activa cuando **ambas** entradas están en estado de bloqueo.",
            "- Usar o no `EDM1` no cambia el nivel de prestaciones alcanzable, pero "
            "sí el diagnóstico del sistema.",
        ],
        fuente=FUENTE + " · apartado 4.6.1",
        notes=(
            "Detalle que el manual recoge expresamente y que sorprende: los pines 1 "
            "y 2 no deben usarse porque están conectados a circuitos internos.\n\n"
            "Y una precisión importante del propio manual: el uso o no de la señal "
            "EDM1 no afecta al nivel de prestaciones de los parámetros de seguridad "
            "del drive. Aun así, sin EDM1 el módulo de seguridad no puede detectar "
            "un fallo interno del amplificador, con lo que el diagnóstico del "
            "conjunto empeora.\n\n"
            "Recuerde: CN8 se suministra con un conector puente instalado. Para usar "
            "la función de seguridad hay que retirarlo y conectar el dispositivo."
        ),
    )

    d.figure_slide(
        "Ejemplo oficial de conexión de la seguridad",
        FIG + "cn8_ejemplo.png",
        subtitle="Circuito de entrada con doble canal y común a 0 V",
        puntos=[
            "#Lo que muestra el esquema",
            "Fuente de **24 V** con **fusible** de protección.",
            "Un **interruptor de contactos de muy baja corriente** que abre "
            "simultáneamente los dos canales.",
            "Resistencias internas de **5,1 kΩ** en cada entrada.",
            "#Reglas que impone el manual",
            "Las señales de seguridad usan **común a 0 V**: es al revés que el resto "
            "de entradas de `CN1`.",
            "Hay que conectar **entradas redundantes**: los dos canales, siempre.",
            "El contacto debe ser de **baja corriente**, porque la corriente de las "
            "entradas es muy pequeña y un contacto de potencia puede no conducir de "
            "forma fiable.",
        ],
        fuente=FUENTE + " · apartado 4.6.2",
        notes=(
            "Dos advertencias del manual que hay que trasladar:\n\n"
            "1) La lógica de las señales de seguridad es la contraria a la del resto "
            "del conector: aquí el común es 0 V y la salida es de tipo source. Esto "
            "confunde a quien cablea CN1 y CN8 el mismo día.\n\n"
            "2) Hay que usar un interruptor con contactos de muy baja corriente. Los "
            "contactos de potencia forman una capa de óxido cuando conmutan "
            "corrientes muy pequeñas y pueden dejar de conducir: es un modo de fallo "
            "peligroso en un circuito de seguridad.\n\n"
            "El fusible protege el cableado frente a un cortocircuito que dejaría la "
            "función de seguridad inoperante."
        ),
    )

    d.two_col_slide(
        "STO no es parada de emergencia",
        (
            "Qué hace exactamente STO / HWBB",
            [
                "Corta por **hardware** las señales de disparo de los transistores de "
                "potencia: el motor deja de recibir par de forma segura.",
                "Actúa por **dos canales independientes**, de modo que un fallo en "
                "uno no impide la función.",
                "El eje queda **libre**: se detendrá por su propia inercia y "
                "rozamiento, o por el freno dinámico si está configurado.",
                "Es una función **de par cero**, no de posición ni de velocidad.",
                "- Tiempo de respuesta muy corto, sin depender del software del "
                "drive.",
            ],
        ),
        (
            "Qué NO hace y qué debes prever",
            [
                "**No frena** el eje: en una máquina con gran inercia, el movimiento "
                "puede continuar durante segundos.",
                "**No sostiene** la carga: en un eje vertical, la carga cae. Hay que "
                "combinarlo con freno y con un análisis específico.",
                "**No corta la tensión** del bus de continua: sigue habiendo energía "
                "peligrosa dentro del equipo.",
                "**No sustituye** al seccionamiento para trabajos de mantenimiento: "
                "para intervenir hay que consignar la instalación.",
                "#Cuando hace falta parada controlada",
                "- Combinar con un módulo de seguridad temporizado: parada controlada "
                "por el drive y, transcurrido el tiempo, STO.",
            ],
        ),
        subtitle="La confusión más peligrosa del módulo",
        tones=("green", "red"),
        callout=(
            "red",
            "Escenario que hay que evitar",
            "Un eje vertical de 3 kW con carga suspendida y sólo STO como medida de "
            "seguridad. Al activarse, el motor deja de dar par y la carga cae. La "
            "protección de una zona bajo carga suspendida exige medidas adicionales "
            "(freno con vigilancia, bloqueo mecánico) definidas en el análisis de "
            "riesgos.",
        ),
        notes=(
            "Este es el mensaje que hay que asegurarse de que se lleven a casa. Es "
            "un error que se comete con frecuencia en máquinas reales.\n\n"
            "Explique la diferencia entre 'quitar el par' y 'parar'. Con una gran "
            "inercia, quitar el par y dejar el eje libre puede ser MÁS peligroso que "
            "una parada controlada, porque el eje sigue moviéndose sin control.\n\n"
            "Por eso existe SS1: primero se frena de forma controlada con el drive y "
            "después, una vez parado, se aplica STO. Se implementa con un relé de "
            "seguridad temporizado, y el análisis de riesgos decide el tiempo."
        ),
    )

    d.steps_slide(
        "Validación y mantenimiento de la función de seguridad",
        [
            ("Verificar el cableado antes de la primera puesta en servicio",
             "Los dos canales cableados de forma independiente, sin puentes, con la "
             "salida EDM conectada al módulo de seguridad."),
            ("Probar la activación de la función",
             "Con el motor girando en condiciones controladas, activar la seguridad y "
             "comprobar que el par desaparece de inmediato."),
            ("Probar el fallo de un solo canal",
             "Interrumpir un solo canal: el módulo de seguridad debe detectar la "
             "discrepancia mediante EDM y pasar a estado seguro."),
            ("Verificar el tiempo de parada real de la máquina",
             "Medirlo, no estimarlo. Es el dato que determina las distancias de "
             "seguridad de resguardos y barreras."),
            ("Documentar la prueba",
             "Fecha, responsable, resultado y condiciones. Forma parte del expediente "
             "técnico de la máquina."),
            ("Repetir periódicamente",
             "La frecuencia la determina el análisis de riesgos; en muchos casos, al "
             "menos una vez al año y tras cualquier intervención."),
        ],
        subtitle="Una función de seguridad que no se prueba no es una función de "
                 "seguridad",
        callout=(
            "blue",
            "El error de instalación más frecuente",
            "Dejar el puente de fábrica de `CN8` y creer que la máquina tiene STO. El "
            "hardware está preparado, pero la función no está en servicio: el circuito "
            "de seguridad debe cablearse de verdad.",
        ),
        notes=(
            "El paso 4 (medir el tiempo de parada real) es el que más se omite y el "
            "que tiene consecuencias más directas: las distancias de seguridad de una "
            "barrera inmaterial se calculan a partir del tiempo de parada. Si el "
            "tiempo real es mayor que el supuesto, la protección es insuficiente.\n\n"
            "Recuerde también que el tiempo de parada aumenta con el desgaste del "
            "freno y con cambios en la carga, y que por eso hay que volver a medirlo "
            "periódicamente.\n\n"
            "Insista en que el diseño de la función de seguridad corresponde a "
            "personal cualificado y debe quedar documentado en el expediente técnico "
            "de la máquina."
        ),
    )


def _diagrama_hwbb(d: Deck) -> None:
    slide = d.canvas_slide(
        "La función HWBB y el conector `CN8`",
        "Dos canales de desactivación y una señal de vigilancia",
        notes=(
            "Explique la arquitectura de dos canales: el módulo de seguridad abre "
            "simultáneamente dos circuitos independientes. Cada uno, por separado, es "
            "capaz de bloquear los transistores de potencia. Así, un fallo en un "
            "canal (un contacto pegado, un cable cortado) no impide que la función "
            "actúe.\n\n"
            "La señal EDM (External Device Monitoring) cierra el lazo de diagnóstico: "
            "el drive informa al módulo de seguridad de que efectivamente ha entrado "
            "en estado seguro. Si el módulo abre los canales y EDM no cambia de "
            "estado, hay un fallo interno y el sistema debe pasar a estado seguro y "
            "avisar. Esta vigilancia cruzada es lo que permite alcanzar categoría 3 "
            "/ PL e.\n\n"
            "Dato práctico fundamental: CN8 se suministra con un conector puente de "
            "fábrica. Si se retira sin cablear la seguridad, el drive queda "
            "permanentemente en baseblock: no dará par y no habrá alarma evidente. Es "
            "la causa número uno de la llamada 'el motor nuevo no funciona'."
        ),
    )

    # Cadena de seguridad
    y = Inches(2.20)
    h = Inches(1.05)
    bloques = [
        ("DISPOSITIVO\nDE SEGURIDAD\nseta, barrera, puerta", RED, Inches(2.6)),
        ("MÓDULO O PLC\nDE SEGURIDAD\ndos canales", NAVY, Inches(2.6)),
        ("`CN8` del SERVOPACK\nentradas HWBB 1 y 2", BLUE, Inches(2.9)),
        ("ETAPA DE POTENCIA\nbloqueada: par cero", GRAY, Inches(2.9)),
    ]
    x = Inches(0.62)
    xs = []
    for texto, color, w in bloques:
        d.box(slide, x, y, w, h, texto, color, size=10.5, radius=0.10)
        xs.append((x, w))
        if x + w < Inches(11.5):
            d.arrow(slide, x + w + Inches(0.05), y + h / 2 - Inches(0.09),
                    Inches(0.25), Inches(0.18), color=AMBER)
        x += w + Inches(0.35)

    # EDM de vuelta
    y_edm = Inches(3.95)
    x_from = xs[2][0] + xs[2][1] / 2
    x_to = xs[1][0] + xs[1][1] / 2
    d.line(slide, x_from, y + h, x_from, y_edm, color=GREEN, width=Pt(1.75))
    d.line(slide, x_from, y_edm, x_to, y_edm, color=GREEN, width=Pt(1.75))
    d.arrow(slide, x_to - Inches(0.11), y_edm - Inches(0.55), Inches(0.22),
            Inches(0.55), color=GREEN, direction="up")
    d.box(slide, x_from - Inches(1.5), y_edm - Inches(0.22), Inches(3.0),
          Inches(0.44), "`EDM1` — confirmación de estado seguro", GREEN,
          size=10)

    # Detalles
    d._rect(slide, Inches(0.62), Inches(4.60), Inches(5.9), Inches(1.75),
            fill=LIGHT, line=GRAY_LINE)
    d._text(slide, Inches(0.90), Inches(4.75), Inches(5.3), Inches(0.3),
            "Señales del conector `CN8`", size=Pt(12.5), color=NAVY, bold=True)
    tf = slide.shapes.add_textbox(Inches(0.90), Inches(5.10), Inches(5.3),
                                  Inches(1.2)).text_frame
    tf.word_wrap = True
    d._fill_bullets(tf, [
        "**Canal 1** y **canal 2**: entradas independientes de desactivación del "
        "par.",
        "**EDM**: salida de vigilancia hacia el módulo de seguridad.",
        "Consulta la asignación exacta de pines en el manual de tu modelo.",
    ], size=10.5)

    d._rect(slide, Inches(6.82), Inches(4.60), Inches(5.9), Inches(1.75),
            fill=LIGHT_BLUE, line=BLUE, line_w=Pt(0.75))
    d._text(slide, Inches(7.10), Inches(4.75), Inches(5.3), Inches(0.3),
            "Reglas de cableado", size=Pt(12.5), color=NAVY, bold=True)
    tf = slide.shapes.add_textbox(Inches(7.10), Inches(5.10), Inches(5.3),
                                  Inches(1.2)).text_frame
    tf.word_wrap = True
    d._fill_bullets(tf, [
        "Los dos canales, **físicamente independientes**: distinto conductor y, si "
        "es posible, distinta canalización.",
        "**Nunca** puentear un canal 'para probar'.",
        "EDM conectado y vigilado: sin él se pierde el diagnóstico y el nivel de "
        "prestaciones.",
    ], size=10.5)

    d.callout(slide, Inches(0.62), Inches(6.45), Inches(12.1), Inches(0.46),
              "red", "`CN8` sale de fábrica con puente. Si lo retiras sin cablear la "
              "seguridad, el eje no dará par y no habrá alarma que lo explique.", "")
