"""Módulo 5 — Instalación mecánica y eléctrica."""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from builder import (AMBER, BLUE, CYAN, FIG, FUENTE, GRAY, GRAY_LINE, GREEN,
                     INK, LIGHT, LIGHT_BLUE, NAVY, NAVY_SOFT, RED, WHITE, Card,
                     Deck)


def build(d: Deck) -> None:
    d.section_slide(
        "MÓDULO 05",
        "Instalación mecánica y eléctrica",
        [
            "Montaje en armario: espacio, orientación y temperatura",
            "El esquema de potencia completo, borne a borne",
            "Protecciones, contactor y secuencia de energizado",
            "Compatibilidad electromagnética: filtro, tierra y apantallamiento",
            "Resistencia de regeneración y freno de retención",
            "Acoplamiento y alineación del motor",
        ],
        duration="4 h",
        notes=(
            "Módulo eminentemente práctico. Si hay armario disponible, alterne "
            "diapositiva y equipo real.\n\n"
            "Mensaje transversal: la mayoría de los fallos 'raros' de un servo "
            "(alarmas intermitentes, ruido en la medida, pérdidas de comunicación) "
            "son problemas de instalación, no de configuración."
        ),
    )

    d.two_col_slide(
        "Montaje en el armario",
        (
            "Reglas de montaje",
            [
                "Montaje **vertical**, con los bornes hacia abajo y la etiqueta "
                "legible: el ventilador está diseñado para tiro vertical.",
                "Fijación sobre placa metálica **desnuda** (sin pintura en la zona de "
                "contacto) para asegurar la continuidad de masa.",
                "Distancias mínimas orientativas: **40 mm** a los lados, **50 mm** "
                "arriba y abajo entre unidades; más si hay varios amplificadores en "
                "fila.",
                "Nunca por encima de elementos que generen calor (resistencias de "
                "frenado, transformadores).",
                "Deja acceso frontal a `CN7` (USB) y al display: los necesitarás en "
                "cada intervención.",
            ],
        ),
        (
            "Condiciones ambientales",
            [
                "Temperatura de servicio **0 a 55 °C**; por encima de 45 °C hay que "
                "reducir la carga (derating).",
                "Humedad hasta el 90 % **sin condensación**. Ojo con las máquinas que "
                "se paran el fin de semana en naves frías.",
                "Altitud hasta 1.000 m sin corrección; por encima, menor capacidad de "
                "disipación y de aislamiento.",
                "Ambiente **sin polvo conductor, niebla de aceite ni gases "
                "corrosivos**: el amplificador es IP20.",
                "Vibración: montar sobre estructura rígida, alejado de prensas y "
                "punzonadoras.",
                "- En ambientes agresivos, armario cerrado con intercambiador o "
                "climatizador, nunca ventilación directa del exterior.",
            ],
        ),
        subtitle="Temperatura y limpieza son las dos variables que marcan la vida útil",
        tones=("blue", "cyan"),
        callout=(
            "amber",
            "Cálculo rápido de disipación",
            "Estima las pérdidas del amplificador en torno al 5-8 % de la potencia "
            "que entrega. Para 3 kW trabajando al 50 % son aproximadamente 100-150 W "
            "que hay que evacuar del armario, más la resistencia de regeneración si "
            "es interna.",
        ),
        notes=(
            "La condensación merece un comentario: en instalaciones estacionales o "
            "con paradas largas, la resistencia de caldeo del armario evita averías "
            "electrónicas caras. Cuesta muy poco.\n\n"
            "Sobre las pérdidas: el dato exacto está en el manual por modelo. Lo "
            "importante es que el alumno recuerde que un eje servo no es 'frío': "
            "aporta calor real al armario y hay que incluirlo en el balance térmico "
            "junto con el resto de equipos.\n\n"
            "Truco de mantenimiento: registrar con una cámara térmica el armario "
            "recién puesto en marcha, para tener una referencia con la que comparar "
            "años después."
        ),
    )

    _diagrama_potencia(d)

    d.table_slide(
        "Protecciones y cables para el SGDXS-200A00A",
        ["Elemento", "Criterio de selección", "Valor orientativo para 3 kW"],
        [
            ["Interruptor automático / fusibles",
             "Protección de cortocircuito de la línea; coordinar con la corriente de "
             "entrada (≈ 21 A) y con la corriente de arranque de precarga",
             "Curva D o fusibles tipo gG; consulta la tabla del manual"],
            ["Sección del cable de red",
             "Corriente de entrada continua y caída de tensión admisible",
             "Del orden de 4 mm² (verificar según norma, longitud y agrupamiento)"],
            ["Contactor de línea",
             "Categoría AC-1/AC-3 según el criterio de la instalación; debe cortar "
             "el circuito principal, no el de control",
             "Dimensionado para ≥ 25 A"],
            ["Sección del cable de motor",
             "Corriente nominal del motor (≈ 18,5 A) y pico (≈ 55 A) de corta "
             "duración", "Del orden de 4 mm², **apantallado**"],
            ["Cable de encoder", "Cable original apantallado y confeccionado",
             "No fabricarlo artesanalmente"],
            ["Cable de E/S (`CN1`)", "Par trenzado apantallado, señales de 24 V",
             "0,2-0,5 mm²"],
            ["Fuente de 24 V CC", "Alimenta E/S y, en su caso, el freno del motor",
             "Fuente independiente y dimensionada con margen"],
            ["Filtro de red EMC", "Corriente nominal ≥ corriente de entrada; modelo "
             "recomendado por el fabricante", "≥ 25 A, monofásico o trifásico según "
             "el caso"],
            ["Diferencial (si procede)",
             "Tipo B (sensible a corriente continua) por los armónicos del inversor",
             "Sensibilidad ≥ 300 mA para evitar disparos intempestivos"],
        ],
        [2.7, 5.1, 4.3],
        subtitle="Valores de partida que hay que confirmar con el manual y la norma",
        size=9.5,
        foot="La selección definitiva de protecciones depende del régimen de neutro, "
             "de la norma aplicable y del estudio de cortocircuito de la instalación. "
             "Consulta la guía de periféricos de YASKAWA.",
        notes=(
            "Insista en dos puntos que se olvidan casi siempre:\n"
            "1) El diferencial debe ser tipo B. Un inversor genera corrientes de fuga "
            "de alta frecuencia y con componente continua que un diferencial tipo A o "
            "AC no detecta correctamente y que provoca disparos intempestivos.\n"
            "2) Las corrientes de fuga capacitivas crecen con la longitud del cable "
            "de motor. Con varios ejes y cables largos pueden sumar cientos de "
            "miliamperios: por eso se recomienda sensibilidad de 300 mA o superior y "
            "una buena red de tierras.\n\n"
            "El contactor de línea es opcional desde el punto de vista funcional, "
            "pero es la forma correcta de implementar el corte de potencia manteniendo "
            "el control vivo. No conviene usarlo para arrancar y parar la máquina "
            "ciclo a ciclo: se limita a maniobras de seguridad y mantenimiento."
        ),
    )

    _diagrama_secuencia_arranque(d)

    d.bullets_slide(
        "Compatibilidad electromagnética: reglas de oro",
        [
            "#El problema",
            "El inversor conmuta cientos de amperios en decenas de nanosegundos. Esos "
            "flancos generan interferencias que se acoplan a los cables cercanos y a "
            "la red.",
            "",
            "#Las siete reglas que resuelven el 95 % de los casos",
            "**1. Filtro de red** en la entrada, montado **junto al amplificador** y "
            "con la carcasa en contacto metal-metal con la placa.",
            "**2. Cable de motor apantallado**, con la malla conectada a tierra en "
            "**ambos extremos** y por **360°** (abrazadera EMC), no con un latiguillo.",
            "**3. Separación física**: mínimo **30 cm** entre cables de potencia y "
            "cables de señal/encoder que discurran en paralelo.",
            "**4. Cruces a 90°** cuando sea inevitable que se crucen.",
            "**5. Canaletas metálicas separadas** para potencia y para señal, "
            "conectadas a tierra.",
            "**6. Cable de motor lo más corto posible**: la longitud aumenta las "
            "corrientes de fuga y la emisión.",
            "**7. Un único punto de referencia de masa** en el armario: placa de "
            "montaje desnuda, con todas las tierras en estrella hacia ella.",
            "",
            "#Cómo se manifiesta un problema de EMC",
            "- Alarmas intermitentes de encoder (`A.C90`, `A.840`) que 'aparecen y "
            "desaparecen' sin patrón.",
            "- Ruido en la medida de velocidad, entradas digitales que conmutan solas, "
            "pérdidas de comunicación de bus.",
        ],
        subtitle="El apantallamiento no es opcional: es parte del diseño eléctrico",
        callout=(
            "red",
            "El error más frecuente",
            "Conectar la malla del cable de motor sólo en un extremo, o hacerlo con un "
            "cable trenzado largo hasta el borne de tierra. A alta frecuencia ese "
            "latiguillo es una inductancia: hay que usar abrazadera de 360°.",
        ),
        notes=(
            "Explique por qué la conexión de 360° importa: a las frecuencias en juego "
            "(MHz), un conductor de 10 cm tiene una impedancia apreciable, así que la "
            "malla deja de hacer de pantalla. La abrazadera metálica que rodea la "
            "malla completa es la solución correcta y cuesta céntimos.\n\n"
            "Sobre la conexión de la malla en ambos extremos: la objeción clásica es "
            "el 'bucle de tierra'. En un armario industrial con red de masas correcta "
            "el beneficio de apantallamiento supera con mucho al problema del bucle. "
            "Los fabricantes de drives lo recomiendan de forma unánime.\n\n"
            "Anécdota real muy útil: ejes que fallan sólo cuando arranca otra máquina "
            "de la nave. Es un problema de acoplamiento por red o por tierra, no del "
            "servo."
        ),
    )

    _diagrama_regeneracion_freno(d)


    d.figure_slide(
        "Esquema de conexiones completo del SGDXS-□□□A",
        FIG + "conexiones_generales.png",
        subtitle="La lámina de referencia: todo el eje en un solo dibujo",
        fuente=FUENTE + " · apartado 4.2.1",
        notes=(
            "Ésta es probablemente la figura más útil de todo el manual y conviene "
            "imprimirla en A3 y tenerla en el armario durante la instalación.\n\n"
            "Recórrala por zonas, no de golpe:\n"
            "1) Arriba a la izquierda, el circuito de potencia: 1QF (interruptor "
            "automático), 1FLT (filtro), 2KM (contactor de potencia), 1KM "
            "(contactor de control) y la maniobra de marcha/paro con 1Ry y la "
            "lámpara 1PL de alarma.\n"
            "2) Arriba a la derecha, motor (U, V, W) y encoder por CN2, más los "
            "monitores analógicos de CN5.\n"
            "3) En el centro-izquierda, las consignas: V-REF (velocidad), T-REF "
            "(par) y el tren de pulsos PULS/SIGN con su señal de borrado CLR.\n"
            "4) En el centro-derecha, las salidas: códigos de alarma ALO1-3, "
            "salidas de encoder PAO/PBO/PCO, salida de posición absoluta PSO y las "
            "tres salidas de propósito general /SO1, /SO2 y /SO3, más la de alarma "
            "ALM.\n"
            "5) Abajo, las entradas de secuencia /SI0 a /SI6 alimentadas desde "
            "+24VIN, y el conector de seguridad CN8 con sus dos canales HWBB y la "
            "salida EDM1.\n\n"
            "Detalle importante que aparece en el pie de la figura: la fuente de "
            "24 V CC no la suministra YASKAWA y debe ser de aislamiento doble o "
            "reforzado."
        ),
    )

    d.figure_slide(
        "Circuito de potencia con sus protecciones",
        FIG + "potencia_protecciones.png",
        subtitle="Ejemplo oficial para entrada trifásica de 200 V CA",
        puntos=[
            "#Elementos del esquema",
            "**1QF** — interruptor automático de caja moldeada.",
            "**1FLT** — filtro de red para compatibilidad electromagnética.",
            "**1KM** — contactor de la alimentación de **control**.",
            "**2KM** — contactor de la alimentación de **potencia**.",
            "**1SA / 2SA / 3SA** — absorbedores de sobretensión.",
            "**1D** — diodo volante sobre la bobina del relé.",
            "**1Ry** — relé de la maniobra · **1PL** — lámpara de alarma.",
            "#La lógica de la maniobra",
            "La salida `ALM` del drive (`CN1-31` / `CN1-32`) está en serie con la "
            "maniobra: **una alarma corta la potencia** y enciende la lámpara.",
            "- El pulsador de marcha excita 1KM, que se automantiene, y a "
            "continuación 2KM da potencia.",
        ],
        fuente=FUENTE + " · apartado 4.3.4",
        notes=(
            "Este esquema responde exactamente a la petición de 'potencia y "
            "protecciones eléctricas'. Es el circuito recomendado por el fabricante "
            "y conviene tomarlo como referencia de diseño.\n\n"
            "Puntos que hay que explicar:\n"
            "· Los absorbedores de sobretensión (1SA, 2SA, 3SA) van sobre las "
            "bobinas de los contactores y en la entrada: protegen frente a los picos "
            "de maniobra, que son una fuente clásica de averías electrónicas.\n"
            "· El diodo 1D en la bobina del relé cumple la misma función en "
            "continua.\n"
            "· La cadena de alarma es lo que convierte un fallo del drive en un "
            "corte real de potencia, en lugar de dejar la máquina energizada con un "
            "eje muerto.\n\n"
            "Para el SGDXS-200A00A: 15 A de entrada, luego el 1QF y el 2KM se "
            "dimensionan por encima de ese valor, consultando la tabla de "
            "periféricos del manual."
        ),
    )

    d.figure_slide(
        "Secuencia de encendido, según el manual",
        FIG + "secuencia_encendido.png",
        subtitle="Cronograma oficial y la advertencia de descarga del bus",
        puntos=[
            "#Lo que fija el cronograma",
            "La alimentación de **control** se establece antes o a la vez que la de "
            "**potencia**.",
            "Existe un **retardo** entre dar potencia y que el drive acepte el "
            "servo ON: es la precarga de los condensadores.",
            "La señal `ALM` sólo es válida una vez transcurrido ese tiempo.",
            "#La advertencia en rojo",
            "Tras cortar la alimentación, el bus de continua **conserva tensión "
            "peligrosa**. Espera al menos **15 minutos** desde que se apaga el "
            "indicador CHARGE antes de tocar nada.",
            "- No toques los bornes de potencia ni los del motor mientras el "
            "indicador CHARGE esté encendido.",
        ],
        fuente=FUENTE + " · apartado 4.3.3",
        notes=(
            "Este cronograma es la versión oficial de la secuencia que vimos en la "
            "lámina anterior. Merece la pena compararlas.\n\n"
            "El dato de seguridad más importante de todo el módulo está aquí: el "
            "manual exige esperar al menos 15 minutos tras cortar la alimentación "
            "antes de manipular los bornes. Es más de lo que la mayoría de los "
            "técnicos supone, y es tiempo de seguridad, no una recomendación "
            "conservadora.\n\n"
            "Insista: el indicador CHARGE apagado es condición necesaria pero no "
            "suficiente. Siempre verificación de ausencia de tensión con "
            "multímetro."
        ),
    )

    d.figure_slide(
        "Resistencia de regeneración externa: el puente `B2`-`B3`",
        FIG + "regeneracion_externa.png",
        subtitle="Figura oficial del procedimiento en los modelos 180A a 330A",
        puntos=[
            "#Procedimiento",
            "**1.** Retirar el puente (cable corto) entre `B2` y `B3`.",
            "**2.** Conectar la resistencia externa entre `B1/⊕` y `B2`.",
            "**3.** Declarar la resistencia en los parámetros.",
            "#Datos de tu amplificador",
            "Resistencia interna: **10 Ω · 60 W**, con **30 W** de consumo continuo "
            "admisible.",
            "Resistencia externa **mínima admisible: 10 Ω**.",
            "#Parámetros que hay que ajustar",
            "`Pn600` — capacidad de la resistencia de regeneración [W].",
            "`Pn603` — valor óhmico de la resistencia de regeneración.",
            "- Si no los declaras, la protección térmica del drive calculará con la "
            "resistencia interna y protegerá mal.",
        ],
        fuente=FUENTE + " · apartado 4.3.5",
        notes=(
            "Novedad de la Σ-X frente a la Σ-7: además de Pn600 (capacidad en "
            "vatios) hay que ajustar Pn603 (resistencia en ohmios). En la Σ-7 sólo "
            "existía el primero. Es un error habitual en quien viene de la serie "
            "anterior.\n\n"
            "Si se dejan las dos resistencias en paralelo por no retirar el puente, "
            "la resistencia total baja de los 10 Ω mínimos y el transistor de "
            "frenado puede destruirse.\n\n"
            "Recuerde que la resistencia externa se monta ventilada, con termostato "
            "de seguridad, y que alcanza temperaturas muy altas."
        ),
    )

    d.figure_slide(
        "Cableado del encoder absoluto y de la batería",
        FIG + "cableado_encoder.png",
        subtitle="Conexión por `CN2` y ubicación de la batería",
        puntos=[
            "#Las dos ubicaciones posibles de la batería",
            "En el **cable de encoder** (unidad de batería intercalada).",
            "En el **controlador anfitrión**, a través de los pines `BAT+` / `BAT-` "
            "de `CN1` (21 y 22).",
            "- **Nunca las dos a la vez**: se producirían corrientes de circulación "
            "entre ambas.",
            "#Reglas de cableado",
            "Cable **original y apantallado**, con la malla a tierra.",
            "Separado de los cables de potencia; cruces a 90°.",
            "- La mayoría de las alarmas intermitentes de encoder son problemas de "
            "cable, conector o apantallamiento.",
        ],
        fuente=FUENTE + " · apartado 4.4.3",
        notes=(
            "La figura muestra las dos formas de alimentar el respaldo del encoder "
            "absoluto. Insista en que hay que elegir una.\n\n"
            "Recuerde el procedimiento de mantenimiento: sustituir la batería con la "
            "alimentación de control conectada evita perder el contaje multivuelta y "
            "tener que rehacer el origen de la máquina."
        ),
    )

    d.figure_slide(
        "Cableado del freno de retención",
        FIG + "freno_retencion.png",
        subtitle="Circuito oficial con relé intermedio y fuente independiente",
        puntos=[
            "#Lo que muestra la figura",
            "La salida `/BK` del drive ataca un **relé intermedio**, no la bobina "
            "del freno directamente.",
            "El freno se alimenta con una **fuente de 24 V independiente** de la de "
            "las E/S.",
            "Se intercala un **supresor de sobretensión** en el circuito de la "
            "bobina.",
            "#Por qué esas tres precauciones",
            "La corriente de conexión del freno es alta y perturba las señales si "
            "comparte fuente.",
            "Al cortar una bobina se generan picos de cientos de voltios.",
            "- La salida del drive es un transistor de baja capacidad.",
            "#Parámetros asociados",
            "`Pn506`, `Pn507` y `Pn508` gobiernan la temporización; la señal `/BK` "
            "se asigna con `Pn50F`.",
        ],
        fuente=FUENTE + " · apartado 4.4.4",
        notes=(
            "Compare esta figura con el esquema simplificado que vimos antes: es la "
            "misma idea, con el detalle real del fabricante.\n\n"
            "El manual advierte expresamente de que, si se usa un freno de 24 V, hay "
            "que instalar una fuente separada de la de las señales de E/S del "
            "conector CN1; si se comparte, las señales pueden funcionar mal."
        ),
    )

    d.figure_slide(
        "Condiciones de instalación para compatibilidad electromagnética",
        FIG + "emc_instalacion.png",
        subtitle="Disposición recomendada por el fabricante",
        puntos=[
            "#Lo que exige la figura",
            "**Placa de montaje metálica** con superficie conductora como "
            "referencia de masas.",
            "**Filtro de red** montado sobre la propia placa, junto al "
            "amplificador.",
            "**Abrazaderas de pantalla** que rodean la malla de los cables por "
            "360°, no latiguillos.",
            "Cables de motor, encoder y E/S **apantallados**.",
            "#Errores que anulan la protección",
            "- Conectar la malla con un cable trenzado largo hasta un borne.",
            "- Pintar la zona de contacto de la placa de montaje.",
            "- Llevar potencia y señal por la misma canaleta.",
        ],
        fuente=FUENTE + " · apartado 3.7",
        notes=(
            "Ésta es la figura que hay que enseñar al montador del armario. La "
            "diferencia entre un eje que funciona y uno con alarmas intermitentes "
            "está muchas veces en estos detalles.\n\n"
            "La tabla que acompaña a la figura en el manual indica qué cables deben "
            "ser apantallados: el de señales de E/S, el del dispositivo de "
            "seguridad, el del encoder y el del motor.\n\n"
            "Recuerde el porqué físico de la abrazadera de 360°: a frecuencias de "
            "MHz un conductor de 10 cm tiene impedancia apreciable y la pantalla "
            "deja de serlo."
        ),
    )

    d.figure_slide(
        "Puesta a tierra de varios SERVOPACK en el armario",
        FIG + "puesta_a_tierra.png",
        subtitle="Tierra en estrella sobre la placa de montaje, no en cadena",
        puntos=[
            "Todas las tierras van a un **único punto** de la placa de montaje.",
            "El filtro de red se monta **sobre la misma placa** y su carcasa hace "
            "contacto metal-metal.",
            "No encadenes las tierras de un amplificador a otro: se forma un bucle "
            "y el ruido recorre todo el armario.",
            "- Máxima resistencia de tierra: **100 Ω** según el manual.",
        ],
        fuente=FUENTE + " · apartado 4.1.3",
        notes=(
            "La figura es pequeña porque el recorte del manual lo es: el mensaje es "
            "el de la tierra en estrella. Explíquela junto a la de EMC.\n\n"
            "El valor de 100 Ω es el criterio de aceptación de la lista de "
            "verificación del módulo."
        ),
    )

    d.steps_slide(
        "Instalación mecánica del motor",
        [
            ("Verificar el eje y la brida antes de montar",
             "Limpieza, ausencia de golpes y presencia de la chaveta correcta. Nunca "
             "golpear el eje con martillo: se daña el rodamiento y el encoder."),
            ("Montar el acoplamiento sin esfuerzo axial",
             "Calentar el buje o usar extractor. Comprobar la carga axial y radial "
             "máxima admisible del motor en el catálogo."),
            ("Alinear con precisión",
             "La desalineación genera par pulsante, ruido y desgaste prematuro del "
             "rodamiento. Usar comparador o alineador láser; seguir la tolerancia del "
             "acoplamiento."),
            ("Elegir bien el acoplamiento",
             "Rígido o de fuelle metálico para máxima rigidez torsional; los "
             "elastoméricos introducen elasticidad que limita la ganancia alcanzable."),
            ("Cuidar la posición de los conectores",
             "Orientados hacia abajo si hay riesgo de goteo, con bucle de goteo antes "
             "del conector y sin tensión mecánica en el cable."),
            ("Prever el radio de curvatura y el movimiento",
             "En ejes móviles, cable de cadena portacables específico. Un cable "
             "estándar en cadena falla en meses."),
            ("Conectar la tierra del motor",
             "Al borne de tierra del amplificador, con la sección adecuada. Es "
             "requisito de seguridad y de EMC."),
        ],
        subtitle="La mecánica define el techo de lo que podrás sintonizar después",
        callout=(
            "blue",
            "Por qué el acoplamiento importa tanto",
            "El acoplamiento y el eje forman un sistema masa-muelle con la carga. Su "
            "frecuencia de resonancia marca el límite superior de las ganancias: "
            "cuanto más rígido, más alta la resonancia y más rápido puede ser el eje.",
        ),
        notes=(
            "Este es el puente entre el módulo de instalación y el de sintonización. "
            "Si el alumno entiende que la rigidez mecánica fija el techo de las "
            "ganancias, entenderá por qué en el Módulo 09 a veces no hay nada más que "
            "hacer desde el drive.\n\n"
            "Dato práctico: sustituir un acoplamiento elastomérico por uno de fuelle "
            "metálico puede permitir subir la ganancia un 50 % o más en ejes "
            "exigentes. Es una mejora barata cuando un eje 'no llega'."
        ),
    )

    d.table_slide(
        "Lista de verificación antes de energizar",
        ["#", "Comprobación", "Criterio de aceptación"],
        [
            ["1", "Modelo de amplificador y de motor",
             "Combinación homologada; coinciden con el proyecto"],
            ["2", "Tensión de red medida en el armario",
             "Dentro de 200-240 V CA, −15 % / +10 %, equilibrada"],
            ["3", "Conexión `L1` `L2` `L3` y `L1C` `L2C`",
             "Apriete al par indicado; ninguna fase en `U` `V` `W`"],
            ["4", "Conexión `U` `V` `W` al motor",
             "**Orden correcto y misma fase en ambos extremos**"],
            ["5", "Tierra del amplificador y del motor",
             "Continuidad verificada con multímetro; < 100 Ω a tierra de "
             "instalación"],
            ["6", "Puente `B2`-`B3` o resistencia externa",
             "Coherente con el cálculo de regeneración y con `Pn600`"],
            ["7", "Cable de encoder en `CN2`",
             "Conector encajado, malla a tierra, sin compartir canaleta con potencia"],
            ["8", "Cableado de `CN1` y fuente de 24 V",
             "Polaridad correcta; `+24VIN` alimentado"],
            ["9", "Conector `CN8` de seguridad",
             "Puente original colocado **o** circuito HWBB correctamente cableado"],
            ["10", "Freno de retención (si existe)",
             "Alimentación propia de 24 V; eje mecánicamente asegurado"],
            ["11", "Zona mecánica despejada",
             "Sin herramientas, chavetas sueltas ni personas en el recorrido"],
            ["12", "Finales de carrera y parada de emergencia",
             "Probados eléctricamente antes de dar potencia"],
        ],
        [0.5, 4.3, 5.5],
        subtitle="Imprime esta lista y fírmala: es tu registro de instalación",
        size=9.5,
        align_center=(0,),
        notes=(
            "Recomiende convertir esta lista en un documento de calidad firmado por "
            "el instalador. En caso de incidencia, tener el registro de que se "
            "verificó cada punto cambia por completo la conversación.\n\n"
            "El punto 4 merece un comentario: si se intercambian dos fases del motor, "
            "el eje puede embalarse al activar el servo o disparar alarma de "
            "sobrecorriente inmediatamente. Se comprueba en la prueba de JOG del "
            "Módulo 08, siempre con la carga desacoplada la primera vez.\n\n"
            "El punto 9 es el que más veces provoca la llamada 'el motor no hace "
            "nada y no da alarma'."
        ),
    )


# --------------------------------------------------------------------------
# Diagramas
# --------------------------------------------------------------------------

def _diagrama_potencia(d: Deck) -> None:
    slide = d.canvas_slide(
        "Esquema de potencia, borne a borne",
        "Arquitectura recomendada: potencia conmutada, control permanente",
        notes=(
            "Recorra el esquema de izquierda a derecha. Los puntos que hay que "
            "destacar:\n\n"
            "· La alimentación de control (L1C/L2C) se toma ANTES del contactor. Así, "
            "al abrir el contactor por emergencia el drive sigue vivo: mantiene la "
            "comunicación, el encoder absoluto y el diagnóstico. Es la diferencia "
            "entre 'la máquina paró y sé por qué' y 'la máquina se apagó'.\n\n"
            "· El filtro va lo más cerca posible del amplificador y con carcasa a "
            "masa.\n\n"
            "· La salida de alarma ALM del drive se cablea normalmente en serie con "
            "la bobina del contactor, de modo que una alarma grave corta la potencia.\n\n"
            "· La resistencia de regeneración se conecta entre B1 y B2 retirando "
            "previamente el puente B2-B3.\n\n"
            "· Todas las tierras van en estrella a la placa de montaje.\n\n"
            "Advertencia: no usar el contactor para arrancar y parar la máquina en "
            "cada ciclo. El circuito de precarga tiene un número limitado de "
            "maniobras y se degrada."
        ),
    )

    y = Inches(2.30)
    h = Inches(0.95)
    cadena = [
        ("RED\n3~ 200-240 V", GRAY, Inches(1.28)),
        ("INTERRUPTOR\nautomático", NAVY, Inches(1.28)),
        ("CONTACTOR\nde línea", NAVY, Inches(1.28)),
        ("FILTRO EMC", BLUE, Inches(1.28)),
    ]
    x = Inches(0.62)
    xs = []
    for texto, color, w in cadena:
        d.box(slide, x, y, w, h, texto, color, size=9.5, radius=0.10)
        xs.append((x, w))
        d.arrow(slide, x + w + Inches(0.03), y + h / 2 - Inches(0.08),
                Inches(0.16), Inches(0.16), color=AMBER)
        x += w + Inches(0.22)

    # SERVOPACK
    sp_x, sp_w = x, Inches(2.55)
    d._rect(slide, sp_x, Inches(1.95), sp_w, Inches(3.55), fill=LIGHT,
            line=NAVY, line_w=Pt(2))
    d._text(slide, sp_x, Inches(2.06), sp_w, Inches(0.3), "SGDXS-200A00A",
            size=Pt(13), color=NAVY, bold=True, align=PP_ALIGN.CENTER)

    bornes = [
        ("`L1` `L2` `L3`", NAVY, Inches(2.45)),
        ("`L1C` `L2C`", NAVY_SOFT, Inches(3.00)),
        ("`B1/⊕` `B2` `B3`", RED, Inches(3.55)),
        ("`U` `V` `W`", CYAN, Inches(4.10)),
        ("⏚", GREEN, Inches(4.65)),
        ("`CN2` encoder", GREEN, Inches(5.05)),
    ]
    for texto, color, yy in bornes:
        d.box(slide, sp_x + Inches(0.18), yy, sp_w - Inches(0.36), Inches(0.38),
              texto, color, size=10)

    # Motor
    mx = sp_x + sp_w + Inches(0.55)
    m_w = Inches(2.55)
    d.box(slide, mx, Inches(3.85), m_w, Inches(1.0),
          "SERVOMOTOR\nSGMXA-30A", CYAN, size=11.5, radius=0.10)
    d.arrow(slide, sp_x + sp_w + Inches(0.05), Inches(4.19), Inches(0.42),
            Inches(0.20), color=CYAN)
    d.box(slide, mx, Inches(5.05), m_w, Inches(0.45),
          "ENCODER 24 bits", GREEN, size=10)
    d.line(slide, sp_x + sp_w, Inches(5.27), mx, Inches(5.27), color=GREEN,
           width=Pt(1.5))

    # Resistencia de regeneración
    d.box(slide, mx, Inches(2.55), m_w, Inches(0.85),
          "RESISTENCIA DE\nREGENERACIÓN\n(si el cálculo lo exige)", RED,
          size=9.5, radius=0.10)
    d.line(slide, sp_x + sp_w, Inches(3.74), mx, Inches(2.98), color=RED,
           width=Pt(1.5), dash=True)

    # Derivación de control antes del contactor
    x_ctl = xs[1][0] + xs[1][1] + Inches(0.14)
    d.line(slide, x_ctl, y + h, x_ctl, Inches(6.05), color=NAVY_SOFT,
           width=Pt(1.5))
    d.line(slide, x_ctl, Inches(6.05), sp_x + Inches(0.4), Inches(6.05),
           color=NAVY_SOFT, width=Pt(1.5))
    d.line(slide, sp_x + Inches(0.4), Inches(6.05), sp_x + Inches(0.4),
           Inches(3.38), color=NAVY_SOFT, width=Pt(1.5))
    d.label(slide, x_ctl + Inches(0.15), Inches(6.10), Inches(5.2),
            "Alimentación del control tomada **antes** del contactor: el drive sigue "
            "vivo con la potencia cortada", size=9.5, color=NAVY_SOFT,
            align=PP_ALIGN.LEFT, bold=False)

    # Tierra
    d.box(slide, Inches(0.62), Inches(6.55), Inches(12.1), Inches(0.36),
          "TIERRA EN ESTRELLA A LA PLACA DE MONTAJE — amplificador, motor, filtro y "
          "pantallas de todos los cables", GREEN, size=10)


def _diagrama_secuencia_arranque(d: Deck) -> None:
    slide = d.canvas_slide(
        "Secuencia de energizado y de parada",
        "El orden correcto evita alarmas y protege el equipo",
        notes=(
            "La secuencia de arranque es siempre la misma: control → potencia → "
            "esperar a que el drive esté listo (/S-RDY) → servo ON → mover.\n\n"
            "El retardo entre la potencia y el servo ON no es un capricho: el "
            "circuito de precarga necesita cargar los condensadores del bus antes de "
            "que el relé de bypass los conecte a la red. Dar servo ON demasiado "
            "pronto produce alarma de subtensión (A.410) o un aviso de secuencia "
            "inválida.\n\n"
            "En la parada, el orden inverso protege al motor: primero quitar la "
            "consigna y esperar a velocidad cero, después servo OFF (con freno si "
            "corresponde) y sólo entonces cortar la potencia.\n\n"
            "Comente el caso especial de la parada de emergencia: al abrir el "
            "contactor con el motor en marcha, el drive detecta pérdida de fase y "
            "detiene por freno dinámico. Es aceptable en emergencia, pero no debe "
            "ser el modo normal de parada."
        ),
    )

    y0 = Inches(1.95)
    col_w = Inches(5.85)

    # Arranque
    d.box(slide, Inches(0.62), y0, col_w, Inches(0.45),
          "SECUENCIA DE ARRANQUE", GREEN, size=12)
    pasos_on = [
        ("Conectar la alimentación de **control** `L1C` `L2C`",
         "El display se ilumina; el drive arranca su electrónica"),
        ("Conectar la alimentación de **potencia** `L1` `L2` `L3`",
         "Se cargan los condensadores del bus (precarga)"),
        ("Esperar a que el drive esté **listo** (`/S-RDY`)",
         "Unas décimas de segundo; no fuerces el paso"),
        ("**Servo ON** (`/S-ON`), liberar el freno y mover",
         "Primero el motor sostiene la carga, después se libera el freno"),
    ]
    y = y0 + Inches(0.62)
    for i, (titulo, detalle) in enumerate(pasos_on, start=1):
        d._rect(slide, Inches(0.62), y, col_w, Inches(0.80), fill=LIGHT,
                line=GRAY_LINE)
        d._rect(slide, Inches(0.62), y, Inches(0.42), Inches(0.80), fill=GREEN)
        d._text(slide, Inches(0.62), y + Inches(0.23), Inches(0.42),
                Inches(0.3), str(i), size=Pt(14), color=WHITE, bold=True,
                align=PP_ALIGN.CENTER)
        d._text(slide, Inches(1.20), y + Inches(0.11), col_w - Inches(0.75),
                Inches(0.3), titulo, size=Pt(11), color=NAVY, bold=True)
        d._text(slide, Inches(1.20), y + Inches(0.43), col_w - Inches(0.75),
                Inches(0.3), detalle, size=Pt(9.5), color=GRAY)
        y += Inches(0.86)

    # Parada
    d.box(slide, Inches(6.88), y0, col_w, Inches(0.45),
          "SECUENCIA DE PARADA", RED, size=12)
    pasos_off = [
        ("Llevar la consigna a **cero** y esperar velocidad cero",
         "Nunca cortar en movimiento si puede evitarse"),
        ("**Aplicar el freno** (`/BK`) y esperar a que agarre",
         "`Pn507` fija el umbral de velocidad; `Pn508`, la espera"),
        ("Desactivar **servo OFF**",
         "El motor deja de dar par; el freno sostiene la carga"),
        ("Cortar la **potencia** y, por último, el **control**",
         "El control se corta al final para no perder el diagnóstico"),
    ]
    y = y0 + Inches(0.62)
    for i, (titulo, detalle) in enumerate(pasos_off, start=1):
        d._rect(slide, Inches(6.88), y, col_w, Inches(0.80), fill=LIGHT,
                line=GRAY_LINE)
        d._rect(slide, Inches(6.88), y, Inches(0.42), Inches(0.80), fill=RED)
        d._text(slide, Inches(6.88), y + Inches(0.23), Inches(0.42),
                Inches(0.3), str(i), size=Pt(14), color=WHITE, bold=True,
                align=PP_ALIGN.CENTER)
        d._text(slide, Inches(7.46), y + Inches(0.11), col_w - Inches(0.75),
                Inches(0.3), titulo, size=Pt(11), color=NAVY, bold=True)
        d._text(slide, Inches(7.46), y + Inches(0.43), col_w - Inches(0.75),
                Inches(0.3), detalle, size=Pt(9.5), color=GRAY)
        y += Inches(0.86)

    d.callout(slide, Inches(0.62), Inches(6.10), Inches(12.1), Inches(0.82),
              "amber", "Dos errores de secuencia muy frecuentes",
              "Dar servo ON inmediatamente después de la potencia (alarma de "
              "subtensión o de secuencia inválida) · Cortar el contactor de línea con "
              "el motor girando como forma habitual de parar la máquina (desgasta el "
              "circuito de precarga y provoca paradas por freno dinámico).")


def _diagrama_regeneracion_freno(d: Deck) -> None:
    slide = d.canvas_slide(
        "Conexión de la regeneración y del freno de retención",
        "Dos detalles de cableado que provocan muchas averías",
        notes=(
            "Regeneración: el puente entre B2 y B3 conecta la resistencia interna. "
            "Si se monta una externa hay que RETIRARLO; si no, quedan las dos en "
            "paralelo, baja la resistencia total por debajo del mínimo admisible y se "
            "puede dañar el transistor de frenado. Además hay que declarar la "
            "capacidad de la resistencia externa en Pn600 para que la protección "
            "térmica del drive calcule bien.\n\n"
            "Freno: es un electroimán de 24 V CC normalmente cerrado. Tres reglas:\n"
            "1) Fuente propia o al menos circuito propio: la corriente de "
            "conexión/desconexión es alta y perturba las E/S.\n"
            "2) Supresor de sobretensión (varistor o diodo) en la bobina; al cortar "
            "una bobina se generan picos de cientos de voltios que destruyen "
            "contactos y perturban la electrónica.\n"
            "3) El contacto de mando debe estar dimensionado para carga inductiva de "
            "continua, que es mucho más exigente que la alterna.\n\n"
            "Recuerde: /BK es una señal lógica del drive que hay que asignar a una "
            "salida física con Pn50F y que normalmente ataca a un relé intermedio."
        ),
    )

    # Panel regeneración
    d._rect(slide, Inches(0.62), Inches(1.80), Inches(5.9), Inches(4.35),
            fill=LIGHT, line=GRAY_LINE)
    d._text(slide, Inches(0.90), Inches(1.98), Inches(5.3), Inches(0.35),
            "1 · Resistencia de regeneración", size=Pt(14), color=RED,
            bold=True)

    d.box(slide, Inches(1.00), Inches(2.55), Inches(2.15), Inches(1.55),
          "SERVOPACK\n\n`B1/⊕`\n`B2`\n`B3`", NAVY, size=10.5, radius=0.08)

    d.box(slide, Inches(3.85), Inches(2.55), Inches(2.35), Inches(0.68),
          "CONFIGURACIÓN DE FÁBRICA\npuente `B2`-`B3` colocado", GREEN,
          size=9.5, radius=0.08)
    d.box(slide, Inches(3.85), Inches(3.42), Inches(2.35), Inches(0.68),
          "RESISTENCIA EXTERNA\nretirar el puente y conectar `B1`-`B2`", RED,
          size=9.5, radius=0.08)
    d.line(slide, Inches(3.15), Inches(2.89), Inches(3.85), Inches(2.89),
           color=GREEN, width=Pt(1.5))
    d.line(slide, Inches(3.15), Inches(3.76), Inches(3.85), Inches(3.76),
           color=RED, width=Pt(1.5))

    tf = slide.shapes.add_textbox(Inches(0.95), Inches(4.30), Inches(5.25),
                                  Inches(1.75)).text_frame
    tf.word_wrap = True
    d._fill_bullets(tf, [
        "Retira **siempre** el puente antes de conectar una resistencia externa.",
        "Respeta la **resistencia mínima admisible** del amplificador.",
        "Declara la capacidad en `Pn600` para que la protección térmica funcione.",
        "Móntala ventilada y con termostato de seguridad: alcanza temperaturas muy "
        "altas.",
    ], size=10.5)

    # Panel freno
    d._rect(slide, Inches(6.82), Inches(1.80), Inches(5.9), Inches(4.35),
            fill=LIGHT, line=GRAY_LINE)
    d._text(slide, Inches(7.10), Inches(1.98), Inches(5.3), Inches(0.35),
            "2 · Freno de retención del motor", size=Pt(14), color=GREEN,
            bold=True)

    d.box(slide, Inches(7.15), Inches(2.55), Inches(1.85), Inches(0.72),
          "Salida `/BK`\ndel `CN1`", NAVY, size=10, radius=0.08)
    d.arrow(slide, Inches(9.05), Inches(2.82), Inches(0.35), Inches(0.18),
            color=AMBER)
    d.box(slide, Inches(9.45), Inches(2.55), Inches(1.6), Inches(0.72),
          "RELÉ\nintermedio", BLUE, size=10, radius=0.08)
    d.arrow(slide, Inches(11.10), Inches(2.82), Inches(0.35), Inches(0.18),
            color=AMBER)
    d.box(slide, Inches(11.50), Inches(2.55), Inches(1.05), Inches(0.72),
          "FRENO\n24 V", GREEN, size=10, radius=0.08)
    d.box(slide, Inches(9.45), Inches(3.45), Inches(1.6), Inches(0.55),
          "Supresor\n(varistor/diodo)", RED, size=9, radius=0.08)
    d.line(slide, Inches(10.25), Inches(3.27), Inches(10.25), Inches(3.45),
           color=RED, width=Pt(1.25))

    tf = slide.shapes.add_textbox(Inches(7.15), Inches(4.25), Inches(5.25),
                                  Inches(1.8)).text_frame
    tf.word_wrap = True
    d._fill_bullets(tf, [
        "Alimentación de 24 V **independiente** de la de las E/S.",
        "Supresor de sobretensión **obligatorio** en la bobina.",
        "Asigna la señal `/BK` a una salida física con `Pn50F`.",
        "Ajusta `Pn506`, `Pn507` y `Pn508` según el eje (ver Módulo 03).",
    ], size=10.5)

    d.callout(slide, Inches(0.62), Inches(6.20), Inches(12.1), Inches(0.72),
              "amber", "Comprobación en la puesta en marcha",
              "Con el eje asegurado mecánicamente, verifica que el freno **agarra** "
              "al quitar los 24 V y que **no arrastra** con el motor en movimiento.")
