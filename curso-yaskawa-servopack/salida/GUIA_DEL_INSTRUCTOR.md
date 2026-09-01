# Guía del instructor — Curso YASKAWA SERVOPACK (3 kW)

Documento generado automáticamente a partir de las notas del orador de `CURSO_YASKAWA_SERVOPACK_3kW.pptx`.
Sirve como guion de clase y como manual de estudio en texto plano.

**Total de diapositivas:** 157

---

### 1. Servo drives YASKAWA SERVOPACK

Bienvenida. Preséntese y pregunte por la experiencia previa del grupo: ¿han trabajado con variadores de frecuencia? ¿con PLC? ¿con servos de otras marcas? El curso está diseñado para que alguien sin experiencia previa pueda seguirlo, pero avanza hasta técnicas de sintonización avanzada.

Deje claro desde el primer minuto el mensaje central: un servo no se 'instala', se DIMENSIONA, se instala, se parametriza y se SINTONIZA. Saltarse cualquiera de esos cuatro pasos es la causa de la mayoría de los problemas en campo.

### 2. Qué vas a saber hacer al terminar

Lea los objetivos en voz alta: funcionan como contrato con el alumno. Al final del curso conviene volver a esta diapositiva y verificar uno a uno los seis puntos.

Si el grupo es de mantenimiento y no de diseño, insista en los puntos 4, 5 y 6. Si es de ingeniería de proyecto, en los puntos 1, 2 y 3.

### 3. A quién va dirigido y qué necesitas saber antes

Si no dispone de hardware real, todo el curso puede seguirse con SigmaWin+ en modo offline: permite crear un proyecto, editar el juego completo de parámetros y estudiar las pantallas de ajuste sin drive.

Recuerde que las prácticas con tensión requieren autorización y EPP. El bus de continua del SERVOPACK conserva carga después de desconectar.

### 4. Mapa del curso

Explique la lógica del recorrido: primero se entiende el principio (01-03), después se justifica la selección con cálculo (04), luego se monta (05-06), se configura (07), se arranca (08), se afina (09), se protege (10) y se mantiene (11).

Es tentador saltar directamente al módulo 08 o 09. Advierta que el 80 % de los problemas de sintonización que se ven en campo son en realidad problemas de dimensionamiento (módulo 04) o de cableado y apantallamiento (módulo 05).

### 5. Metodología y convenciones del material

Insista en la advertencia: el objetivo del curso es que el alumno sepa QUÉ buscar y DÓNDE buscarlo en el manual, no que memorice tablas. Un buen técnico de servos es el que maneja el manual con agilidad.

Manual de referencia principal del curso: 'Σ-X-Series AC Servo Drive · Σ-XS SERVOPACK with Analog Voltage/Pulse Train References · Product Manual' (modelo SGDXS-□□□□00□, MANUAL NO. SIEP C710812 03I), descargable gratuitamente desde la web de YASKAWA. Complementarios: el catálogo Σ-X de 200 V y el manual de selección de periféricos.

IMPORTANTE sobre el sufijo -Y3600A: identifica un producto de especificación personalizada (Y-spec). El comportamiento base es el del SGDXS-200A00A, pero puede haber parámetros de fábrica, asignaciones de E/S o funciones modificadas. Solicite al fabricante la hoja de especificación Y antes de dar por buena cualquier configuración por defecto.

### 6. Seguridad antes que nada

No pase esta diapositiva rápido. Si el curso incluye laboratorio, haga firmar la hoja de riesgos aquí.

Dato práctico: el LED CHARGE del SERVOPACK indica que el bus de continua sigue cargado. Que esté apagado es condición necesaria, pero la verificación con multímetro sigue siendo obligatoria.

Anécdota útil para fijar el mensaje: la avería más cara y más frecuente en puesta en marcha es alimentar por U/V/W por confusión con los bornes L1/L2/L3. El SERVOPACK se destruye instantáneamente y no está cubierto por garantía.

## MÓDULO 01 — Fundamentos del servoaccionamiento

Este módulo es la base conceptual. Aunque el grupo tenga experiencia, no lo salte: la mayoría de los errores de sintonización nacen de no tener claro el modelo mental del lazo en cascada y de la relación de inercias.

### 8. ¿Qué es un servoaccionamiento?

Analogía útil: conducir un coche con los ojos cerrados (lazo abierto) frente a conducir mirando la carretera y corrigiendo el volante (lazo cerrado). El motor paso a paso es el primero; el servo, el segundo.

Pregunta para el grupo: ¿por qué un servo puede dar par a velocidad cero y un motor asíncrono con variador tiene problemas para hacerlo? Respuesta: porque el servo conoce la posición exacta del rotor gracias al encoder y puede orientar el campo con precisión (control vectorial con realimentación de posición absoluta del rotor), mientras que en lazo abierto se estima.

### 9. Los cuatro elementos del sistema servo

Recorra el diagrama dos veces: primero la cadena de mando de izquierda a derecha (quién manda a quién) y después la cadena de realimentación de derecha a izquierda (quién informa a quién).

Insista en que el encoder informa al SERVOPACK, no al controlador. El controlador sólo recibe un 'acuse' (señal /COIN de posicionado completado, o la posición real por bus). Esto explica por qué el ajuste fino del eje se hace en el drive y no en el PLC.

Pregunte: si el eje vibra, ¿dónde está el problema? Puede estar en cualquiera de los cuatro bloques y en los dos enlaces. El método de diagnóstico del Módulo 11 consiste precisamente en aislar bloque por bloque.

### 10. Servo frente a variador de frecuencia y motor paso a paso

El punto que más conviene remarcar es el de 'pierde pasos en silencio': es la razón principal por la que se sustituyen steppers por servos en máquinas de producción. El servo nunca pierde la referencia sin avisar; si no puede seguir la consigna, dispara A.d00 (exceso de error de posición) o A.710/A.720 (sobrecarga).

Matiz honesto: los variadores modernos con control vectorial en lazo cerrado y encoder se acercan mucho al servo en par a velocidad cero. La diferencia real queda en la dinámica (inercia del rotor mucho menor en el servomotor) y en la resolución de la realimentación.

### 11. El lazo cerrado en cascada

Este es el diagrama más importante del curso. Todo el Módulo 09 (sintonización) consiste en ajustar las ganancias de estos tres lazos en el orden correcto: de dentro hacia fuera.

Frecuencias de actualización típicas en la Σ-X: el lazo de corriente trabaja en el orden de decenas de kHz, el de velocidad en unos pocos kHz y el de posición algo más lento. Regla universal del control en cascada: el lazo interno debe ser al menos 4-5 veces más rápido que el externo.

Consecuencia práctica que hay que anunciar ya: si el lazo de velocidad no está bien ajustado, subir la ganancia de posición Pn102 sólo produce inestabilidad. Nunca se empieza por fuera.

### 12. Los tres modos de control

Idea clave que hay que dejar clarísima: el modo de par es el lazo interno, el de velocidad añade el lazo intermedio y el de posición añade el externo. Elegir 'modo velocidad' no desactiva el lazo de par; simplemente el drive genera internamente la consigna de par.

Pn000.1 admite además modos combinados con conmutación por entrada digital (por ejemplo velocidad↔par con /P-CON), útiles en aplicaciones de tensión de material donde se arranca en velocidad y se pasa a par.

En modelos de bus (MECHATROLINK-III / EtherCAT) el modo se selecciona por telegrama con los modos de operación del perfil CiA 402: par, velocidad, posición cíclica, homing e interpolación.

### 13. La realimentación: el encoder

La batería del encoder absoluto es una fuente clásica de paradas: genera el aviso A.930 (batería baja) y, si se agota con el equipo sin tensión, la alarma A.810 (fallo de respaldo del encoder), que obliga a repetir Fn008 y a rehacer el origen de la máquina.

Recomendación de mantenimiento: sustituir la batería con el equipo ENERGIZADO (control power ON). Así el encoder no pierde el contaje multivuelta y no hay que rehacer el origen. Anótelo, porque este truco ahorra horas de parada.

### 14. Las magnitudes que gobiernan el dimensionamiento

La fórmula del recuadro es la herramienta más rentable de todo el curso: permite verificar en dos segundos si una propuesta comercial tiene sentido.

Ejercicio en pizarra: 'necesito 15 N·m continuos a 2.000 rpm, ¿me vale un motor de 3 kW?'. P = 15 × 2π × 2000/60 = 3.140 W. Está justo en el límite: habría que ir a la versión de 1.500 rpm (SGMXG-30A, 18,6 N·m) o subir de tamaño. Este razonamiento se desarrolla en el Módulo 04.

### 15. Cómo se lee una curva par-velocidad

Dibuje mentalmente el ciclo de la máquina sobre esta curva: la aceleración debe caer dentro de la zona intermitente y el par eficaz (RMS) de todo el ciclo, dentro de la zona continua.

La caída de la curva a alta velocidad tiene una causa física: la fuerza contraelectromotriz crece con la velocidad y llega un punto en que la tensión del bus de continua ya no puede forzar más corriente. Por eso la curva depende de la tensión de red: con 200 V la curva es más baja que con 230 V. En instalaciones con red débil o larga, esto se nota.

Advertencia práctica: trabajar de forma continuada en la zona intermitente provoca A.720 (sobrecarga continua). El drive lleva un modelo térmico I²t que integra el exceso de corriente.

### 16. Vocabulario esencial del servo

Recomiende a los alumnos fotografiar esta diapositiva: es la que más se consulta durante los primeros días de trabajo con el equipo.

Cuidado con un falso amigo habitual: en castellano se dice 'ganancia alta = respuesta rápida', pero ganancia alta también significa 'menos margen de estabilidad'. Todo el Módulo 09 consiste en encontrar el punto de equilibrio.

## MÓDULO 02 — La familia SERVOPACK Σ-X

El objetivo del módulo es que el alumno pueda mirar la etiqueta de un SERVOPACK cualquiera y deducir en 10 segundos: tensión, potencia, interfaz de comando y generación. Es una habilidad muy práctica en mantenimiento y en compras de repuesto.

### 18. Evolución de la familia y qué aporta la Σ-X

Pregunte al grupo qué generación tienen instalada. En planta suele haber mezcla, y saber distinguirlas por el código (SGDH / SGDV / SGDX) evita pedir repuestos equivocados.

Dato útil: subir la resolución del encoder no da tanto 'más precisión de posicionado' como una medida de velocidad mucho más limpia a baja velocidad, lo que permite ganancias más altas sin ruido. Ese es el motivo real de que la Σ-X alcance 3,5 kHz de ancho de banda.

El modo de compatibilidad de E/S con Σ-7 (Pn50A = n.□□□1) es un detalle muy práctico en retrofit: permite reutilizar el cableado de CN1 de una máquina antigua sin rehacer el armario.

### 19. Las tres líneas de amplificador Σ-X

Criterio de decisión rápido:
· ¿El movimiento lo calcula un PLC/CNC que ya existe? → SGDXS.
· ¿Muchos ejes pequeños y armario ajustado? → evaluar SGDXW.
· ¿Máquina sencilla sin controlador de movimiento? → SGDXT.

Para 3 kW la línea SGDXW habitualmente no llega en potencia por eje, así que la decisión está prácticamente tomada.

### 20. Qué hay dentro del SERVOPACK

Recorra el camino de la energía: rectificador → bus de continua → inversor IGBT → motor. Y el camino de la información: encoder → control → modulación PWM.

Tres consecuencias prácticas que hay que extraer del diagrama:
1) El bus de continua almacena energía en condensadores: por eso hay que esperar antes de tocar los bornes y por eso existe el LED CHARGE.
2) Al frenar, el motor actúa como generador y devuelve energía al bus; si la tensión sube demasiado salta A.400 (sobretensión). La resistencia de regeneración existe para quemar ese exceso.
3) El circuito de control tiene alimentación propia (L1C/L2C), lo que permite diagnosticar con la potencia cortada.

El freno dinámico es un cortocircuito controlado de las fases del motor: frena rápido sin necesidad de electrónica, pero no mantiene la carga parada ni sirve como freno de seguridad.

### 21. Diagrama de bloques oficial del SGDXS-180A / -200A

Ésta es la misma idea del diagrama simplificado anterior, pero en la versión oficial y para el modelo exacto del alumno. Merece la pena recorrerla despacio.

Señale los elementos que el diagrama simplificado no mostraba: el varistor de entrada (absorbe sobretensiones de red), los sensores de tensión y temperatura, el detector de corriente y el ventilador.

Fíjese en que CN11 y CN12 son conectores de módulo opcional (seguridad y realimentación). En la Σ-7 no existían con esa denominación: es una de las novedades de la Σ-X.

### 22. Anatomía del SGDXS-200A00A

Haga que los alumnos localicen físicamente cada elemento en el equipo real antes de continuar. Es un ejercicio de 5 minutos que ahorra muchos errores después.

Puntos de atención:
· CN7 (USB) es la vía normal de conexión con SigmaWin+.
· CN8 viene con un conector puente de fábrica. Si se retira sin cablear la seguridad, el drive queda en baseblock y no habrá par: es la causa número uno de 'el motor no arranca y no da alarma'.
· El LED CHARGE indica bus cargado. Nunca es sustituto de la medida con multímetro.
· El display de 7 segmentos muestra el estado, la alarma y los valores durante la parametrización desde el panel.

### 23. Partes del SERVOPACK, según el fabricante

Ejercicio de cinco minutos: que cada alumno localice en el equipo real los elementos numerados de la figura. Ahorra muchos errores después.

Puntos de atención:
· CN7 (USB) es la vía normal de trabajo con SigmaWin+.
· CN8 viene con un conector puente de fábrica; retirarlo sin cablear la seguridad deja el eje sin par y sin alarma evidente.
· El LED CHARGE encendido significa bus cargado: nunca es sustituto de la medida con multímetro.
· La placa de características lleva el modelo completo, incluido el sufijo -Y3600A: fotografíela en la puesta en marcha.

### 24. Cómo se lee un código de modelo

Ejercicio recomendado: reparta fotos de etiquetas reales (o pida a los alumnos que fotografíen las de su planta) y que decodifiquen el modelo en voz alta.

El campo crítico es la interfaz de comando: determina el hardware y no se puede cambiar. El segundo campo crítico es el tamaño (200 = 3,0 kW), que fija corriente, protecciones y resistencia de regeneración interna.

Advertencia honesta que hay que trasladar al alumno: los dígitos de interfaz y de opciones varían según catálogo, región y revisión. La estructura del código es estable, los códigos concretos hay que verificarlos en el catálogo vigente antes de pedir.

### 25. Gama Σ-X monoeje en 200 V trifásica

Fíjese en un detalle muy revelador: el -180A (2 kW) da 18,5 A continuos y el -200A (3 kW) da 19,6 A. Apenas un 6 % más de corriente para un 50 % más de potencia declarada. La diferencia real está en la corriente de pico (42 A frente a 56 A) y en la capacidad térmica.

De ahí la regla: la selección se hace por COMBINACIÓN homologada motor+drive, no eligiendo cada pieza por amperios.

Regla de repuesto: nunca sustituya un SERVOPACK por otro de tamaño distinto 'porque encaja'. Cambian la protección, la resistencia de regeneración interna y la combinación admitida.

### 26. Ficha técnica del SGDXS-200A00A

Las cuatro cifras que hay que memorizar: 15 A de entrada, 19,6 A de salida continua, 56 A de pico y 130 W de pérdidas. Con ellas se dimensionan cable, magnetotérmico, contactor, filtro y climatización del armario.

Ojo con la resistencia de regeneración: la interna es de 10 Ω y 60 W, pero su consumo admisible continuo es de sólo 30 W. Ese es el número que hay que comparar con la potencia media de regeneración calculada en el Módulo 04.

La resistencia externa mínima admisible también es de 10 Ω: poner una de menor valor hace circular más corriente de la que soporta el transistor de frenado y lo destruye.

Recuerde que el sufijo -Y3600A puede alterar algún dato: contraste con la placa de características y con la hoja de especificación Y.

### 27. Interfaces de comando disponibles

Este es el error de compra más caro y más frecuente: pedir el tamaño correcto con la interfaz equivocada. La interfaz NO es una opción configurable por parámetro ni una tarjeta que se añada después; define el hardware del amplificador.

Consejo de proyecto: si el controlador aún no está decidido, la variante analógica/pulsos es la más 'neutra', pero pierde diagnóstico remoto y obliga a cablear mucha señal. En instalación nueva, EtherCAT suele ser la mejor relación coste/prestaciones.

Con bus, además, el ajuste y la monitorización se pueden hacer en remoto, algo muy valorado en mantenimiento.

### 28. Periféricos y accesorios que casi siempre hacen falta

Sugerencia: proyecte esta diapositiva cuando el grupo esté preparando un presupuesto. El coste oculto de un eje servo no está en el drive, sino en cables originales, filtro y resistencia de frenado.

Insista en los cables: fabricar cables de encoder 'a mano' es una fuente constante de alarmas intermitentes A.C90 (error de comunicación con el encoder), casi imposibles de diagnosticar. Compre siempre cable original confeccionado.

## MÓDULO 03 — El servomotor de 3 kW

El motor determina el comportamiento de la máquina mucho más que el amplificador. Dos motores de la misma potencia pueden dar resultados radicalmente distintos según su inercia y su velocidad nominal. Ese es el mensaje central del módulo.

### 30. Cómo funciona un servomotor de imanes permanentes

El punto de la f.c.e.m. explica de golpe tres cosas que preguntan siempre los alumnos: por qué la curva de par cae a alta velocidad, por qué frenar genera energía que hay que disipar, y por qué es peligroso manipular el conector del motor en un eje que puede girar por gravedad o por arrastre.

Demostración vistosa si hay motor en el aula: gire el eje a mano con el conector libre y mida tensión alterna entre dos fases con el multímetro. Con 3 kW y giro rápido se obtienen decenas de voltios.

### 31. Las familias de servomotor rotativo Σ-X

Insista: la potencia es el resultado, no el criterio. El criterio es el par necesario a la velocidad necesaria y la inercia que hay que mover.

Regla mnemotécnica para las familias: J = 'justo lo normal', A = 'ágil' (baja inercia), G = 'grande' (alto par, baja velocidad), P = 'plano'.

### 32. 3 kW a 3.000 rpm o a 1.500 rpm: la decisión clave

Este es probablemente el criterio de ingeniería más valioso del curso. La mayoría de los ejes 'que vibran y no hay manera de ajustar' son ejes con motor de baja inercia acoplado directamente a una carga de gran inercia.

Explique la física: una reducción de relación i multiplica el par por i y divide la inercia reflejada por i². La reducción es la herramienta más potente para arreglar una relación de inercias mala, pero introduce holgura y un punto de mantenimiento.

Dato que conviene remarcar, tomado de la tabla de combinaciones del manual (apartado 1.5): el SGMXG-30A figura como 2,9 kW, pero con una nota al pie que indica 2,4 kW cuando se usa con un SERVOPACK SGDXS-200A. Es exactamente el tipo de detalle que se pasa por alto en un proyecto y aparece después como falta de par.

Los valores de par son de catálogo y varían con la versión exacta del motor; verifíquelos antes de calcular.

### 33. Código de modelo del servomotor

Lo importante no es memorizar los códigos, sino saber que en la referencia del motor están codificados el freno, el tipo de eje y el encoder. Es lo que hace que dos motores 'iguales' no sean intercambiables.

Al pedir un repuesto hay que transcribir el código COMPLETO de la placa, carácter a carácter. Recomiende fotografiar la placa en lugar de copiarla a mano.

### 34. Ficha del motor de ejemplo: SGMXA-30A

Marque en la tabla los cuatro datos que se usarán en el Módulo 04: par nominal, par máximo, velocidad nominal e inercia del rotor. El resto son datos de instalación.

Una observación honesta: la inercia del rotor cambia bastante entre familias y entre versiones con y sin freno. El freno de retención añade inercia y hay que incluirla en el cálculo.

### 35. El encoder absoluto de 24 bits y su batería

Cuente el caso típico: parada de planta de tres semanas en agosto, armarios sin tensión, y a la vuelta cuatro ejes con A.810 y todos los orígenes perdidos. Es un día entero de trabajo que se evita con 20 euros de baterías y un procedimiento.

Detalle importante y poco conocido: montar batería en el drive Y en el cable a la vez puede producir corrientes de circulación entre ambas. Elija una de las dos ubicaciones.

### 36. El freno de retención y su secuencia

Concepto que hay que dejar grabado: el freno de retención es ELECTROMAGNÉTICO Y NORMALMENTE CERRADO. Sin 24 V está frenado. Sirve para sostener la carga con el servo desactivado, no para frenar en movimiento. Frenar con él a velocidad destruye el forro en pocos ciclos.

La secuencia importa mucho en ejes verticales:
· Al arrancar: primero servo ON (el motor sostiene la carga), después liberar el freno. Si se libera antes, la carga cae unos milímetros.
· Al parar: primero cerrar el freno, esperar a que agarre, y sólo entonces quitar el par. Pn506 y Pn508 gobiernan estos retardos.

Parámetros implicados: Pn506 (retardo entre orden de freno y servo OFF con el motor parado), Pn507 (velocidad por debajo de la cual se aplica el freno con el motor en marcha), Pn508 (tiempo de espera antes de quitar el par tras ordenar el freno). La señal de salida es /BK y hay que asignarla a una salida física con Pn50F.

Advertencia de seguridad: el freno de retención NO es un elemento de seguridad certificado por sí solo. Para proteger a una persona bajo una carga suspendida hace falta un análisis de riesgos específico.

### 37. Conectores, cables y protección del motor

Insista en tres cosas: cable original, malla a tierra en ambos extremos y separación física respecto a los cables de potencia (mínimo 30 cm en paralelo, cruces a 90°).

El 'efecto sifón' del último punto es real: el agua recorre el cable y entra por el conector si éste queda hacia arriba. Se resuelve dejando un bucle de goteo antes del conector.

### 38. Combinaciones homologadas motor–SERVOPACK

Esta diapositiva evita disgustos en almacén. Explique que un motor aparentemente idéntico puede diferir en el tipo de encoder (absoluto vs incremental), en el freno o en el eje (con o sin chavetero), y que todo eso está en el código.

Consejo de gestión: mantenga en el CMMS el código completo de cada conjunto motor+drive por eje, con foto de las dos etiquetas. Ahorra horas cuando hay que pedir un repuesto urgente.

## MÓDULO 04 — Dimensionamiento y selección

Este es el módulo con más contenido de ingeniería y el que marca la diferencia entre un técnico y un especialista. Tómese el tiempo necesario: si el grupo entiende el ejemplo numérico, entenderá cualquier eje.

Tenga a mano una calculadora y, si es posible, una hoja de cálculo proyectada para repetir el ejemplo cambiando datos.

### 40. Por qué el dimensionamiento decide el resultado

Pida ejemplos al grupo de ejes que 'nunca han ido bien'. Casi siempre aparecerán síntomas de esta diapositiva.

Mensaje que hay que repetir a lo largo del módulo: sintonizar no arregla un dimensionamiento equivocado. Sólo lo disimula.

### 41. Datos de partida: qué hay que averiguar antes de calcular

Advierta de que el dato que más se falsea es la masa: se olvidan las piezas transportadas, la herramienta, la mesa y los cables. Multiplique por un factor de seguridad si hay dudas.

El segundo dato más traicionero es el tiempo de movimiento: comercial vende '30 ciclos por minuto' y nadie ha comprobado si eso es físicamente posible con la mecánica prevista. Este cálculo sirve precisamente para responder a esa pregunta antes de comprar.

### 42. Paso 1 — Inercia reflejada al eje del motor

Deduzca en pizarra la fórmula del husillo: en una vuelta el motor avanza p metros, luego la relación de transmisión equivalente es p/2π metros por radián. La inercia equivalente de una masa m en traslación con ese 'radio efectivo' es m·(p/2π)².

Numéricamente: con p = 20 mm, el radio efectivo es 3,18 mm. Una masa de 400 kg 'pesa' inercialmente lo mismo que un volante de 400 kg a 3,18 mm de radio: 40,5×10⁻⁴ kg·m². Sorprendentemente poco, y por eso los husillos de paso fino son tan cómodos para el servo (pero limitan la velocidad).

### 43. Paso 2 — La relación de inercias

Analogía útil: llevar de la mano a un niño (relación baja, controlas el movimiento) frente a tirar de un remolque pesado con una cuerda elástica (relación alta con acoplamiento blando: el remolque hace lo que quiere).

Dato práctico: Pn103 mal ajustado es una causa muy frecuente de comportamiento extraño. Si el autotuning estima 300 % y alguien lo deja en 0 %, el lazo de velocidad queda mal escalado y el eje responde lento o inestable.

### 44. Paso 3 — Perfil de movimiento y par requerido

Este diagrama explica visualmente el corazón del dimensionamiento: el par es alto sólo mientras cambia la velocidad. A velocidad constante sólo hay que vencer la fricción.

Señale la asimetría entre aceleración y frenado: al frenar, la fricción ayuda, por lo que el par de deceleración es algo menor en valor absoluto. En ejes verticales ocurre lo contrario al subir y bajar, y hay que calcular ambos sentidos.

Mencione el perfil en S: suaviza el cambio de aceleración (limita el 'jerk'), reduce la excitación de resonancias y el desgaste mecánico, a cambio de exigir algo más de par pico para el mismo tiempo de ciclo. En máquinas con estructura elástica suele compensar.

### 45. Paso 4 — Par eficaz (RMS) y verificación térmica

Explique por qué se eleva al cuadrado: las pérdidas por efecto Joule son proporcionales a I², y el par es proporcional a I. Por eso un pico de par corto pesa mucho en el valor eficaz.

Ejercicio mental muy útil: si se duplica la cadencia de la máquina (la mitad de tiempo de ciclo con el mismo movimiento), el par RMS se multiplica por √2 ≈ 1,41. Es la forma rápida de responder a la pregunta '¿puedo ir más rápido con este motor?'.

### 46. Ejemplo completo (1/2) — Datos y cálculo cinemático

Haga el cálculo en pizarra o en hoja de cálculo en paralelo. Es importante que vean que no hay magia: son cuatro fórmulas.

Comente el resultado de la inercia: la masa de 400 kg contribuye 40,5 y el husillo, que 'sólo' pesa 14,8 kg, contribuye 29,6. En husillos largos y gruesos, el husillo puede dominar el cálculo. Es un resultado contraintuitivo que conviene remarcar.

Si el grupo quiere jugar: pregunte qué pasa si se duplica el paso a 40 mm. La inercia de la masa se multiplica por 4 (162×10⁻⁴), la velocidad del motor se reduce a la mitad (1.200 rpm) y el par sube. Es el compromiso clásico del husillo.

### 47. Ejemplo completo (2/2) — Par, verificación y regeneración

Cierre el ejemplo con la lectura de ingeniería: el eje está holgado en par, lo que da margen para aumentar cadencia en el futuro. Pero al bajar de tamaño de motor la inercia del rotor cae y la relación de inercias empeora, con lo que la sintonización se complica. Ese compromiso —par sobrado frente a relación de inercias— es la esencia del oficio.

Sobre la regeneración: el cálculo de 288 J es la energía cinética total. Parte se disipa en la fricción y en las pérdidas del motor y del drive, y parte la absorben los condensadores del bus. Lo que llega a la resistencia es bastante menos. Por eso el criterio práctico es comparar la potencia media de regeneración con la capacidad de la resistencia interna, y ante la duda, medir en la puesta en marcha con la función de traza.

Los ejes verticales son el caso crítico de regeneración: al bajar, la gravedad aporta energía de forma continua y la resistencia interna se queda corta casi siempre.

### 48. Regeneración: cuándo hace falta resistencia externa

Explique el mecanismo: al frenar, el motor genera y la corriente entra al bus de continua elevando su tensión. Cuando supera un umbral (alrededor de 400 V), el drive conecta el transistor de frenado y quema la energía en la resistencia. Si la energía es mayor que la que la resistencia puede disipar, la tensión sigue subiendo hasta A.400.

Advertencia práctica: la resistencia externa puede superar los 200 °C. Nunca se monta pegada a cables ni bajo materiales sensibles, y siempre se cablea con conductor resistente a temperatura.

Recuerde configurar Pn600: si se monta una resistencia externa y no se declara, el drive sigue calculando con la interna y protege mal.

### 49. Procedimiento de dimensionamiento en 8 pasos

El paso 8 es el que casi nadie hace y el que más valor aporta: comparar el cálculo teórico con la medida real en la máquina. Si el par medido es muy superior al calculado, hay fricción no prevista, desalineación o un problema mecánico que conviene resolver antes de que rompa algo.

Sugerencia de trabajo: crear una plantilla de hoja de cálculo corporativa con estas fórmulas y archivarla junto a la documentación de cada máquina.

## MÓDULO 05 — Instalación mecánica y eléctrica

Módulo eminentemente práctico. Si hay armario disponible, alterne diapositiva y equipo real.

Mensaje transversal: la mayoría de los fallos 'raros' de un servo (alarmas intermitentes, ruido en la medida, pérdidas de comunicación) son problemas de instalación, no de configuración.

### 51. Montaje en el armario

La condensación merece un comentario: en instalaciones estacionales o con paradas largas, la resistencia de caldeo del armario evita averías electrónicas caras. Cuesta muy poco.

Sobre las pérdidas: el dato exacto está en el manual por modelo. Lo importante es que el alumno recuerde que un eje servo no es 'frío': aporta calor real al armario y hay que incluirlo en el balance térmico junto con el resto de equipos.

Truco de mantenimiento: registrar con una cámara térmica el armario recién puesto en marcha, para tener una referencia con la que comparar años después.

### 52. Esquema de potencia, borne a borne

Recorra el esquema de izquierda a derecha. Los puntos que hay que destacar:

· La alimentación de control (L1C/L2C) se toma ANTES del contactor. Así, al abrir el contactor por emergencia el drive sigue vivo: mantiene la comunicación, el encoder absoluto y el diagnóstico. Es la diferencia entre 'la máquina paró y sé por qué' y 'la máquina se apagó'.

· El filtro va lo más cerca posible del amplificador y con carcasa a masa.

· La salida de alarma ALM del drive se cablea normalmente en serie con la bobina del contactor, de modo que una alarma grave corta la potencia.

· La resistencia de regeneración se conecta entre B1 y B2 retirando previamente el puente B2-B3.

· Todas las tierras van en estrella a la placa de montaje.

Advertencia: no usar el contactor para arrancar y parar la máquina en cada ciclo. El circuito de precarga tiene un número limitado de maniobras y se degrada.

### 53. Protecciones y cables para el SGDXS-200A00A

Insista en dos puntos que se olvidan casi siempre:
1) El diferencial debe ser tipo B. Un inversor genera corrientes de fuga de alta frecuencia y con componente continua que un diferencial tipo A o AC no detecta correctamente y que provoca disparos intempestivos.
2) Las corrientes de fuga capacitivas crecen con la longitud del cable de motor. Con varios ejes y cables largos pueden sumar cientos de miliamperios: por eso se recomienda sensibilidad de 300 mA o superior y una buena red de tierras.

El contactor de línea es opcional desde el punto de vista funcional, pero es la forma correcta de implementar el corte de potencia manteniendo el control vivo. No conviene usarlo para arrancar y parar la máquina ciclo a ciclo: se limita a maniobras de seguridad y mantenimiento.

### 54. Secuencia de energizado y de parada

La secuencia de arranque es siempre la misma: control → potencia → esperar a que el drive esté listo (/S-RDY) → servo ON → mover.

El retardo entre la potencia y el servo ON no es un capricho: el circuito de precarga necesita cargar los condensadores del bus antes de que el relé de bypass los conecte a la red. Dar servo ON demasiado pronto produce alarma de subtensión (A.410) o un aviso de secuencia inválida.

En la parada, el orden inverso protege al motor: primero quitar la consigna y esperar a velocidad cero, después servo OFF (con freno si corresponde) y sólo entonces cortar la potencia.

Comente el caso especial de la parada de emergencia: al abrir el contactor con el motor en marcha, el drive detecta pérdida de fase y detiene por freno dinámico. Es aceptable en emergencia, pero no debe ser el modo normal de parada.

### 55. Compatibilidad electromagnética: reglas de oro

Explique por qué la conexión de 360° importa: a las frecuencias en juego (MHz), un conductor de 10 cm tiene una impedancia apreciable, así que la malla deja de hacer de pantalla. La abrazadera metálica que rodea la malla completa es la solución correcta y cuesta céntimos.

Sobre la conexión de la malla en ambos extremos: la objeción clásica es el 'bucle de tierra'. En un armario industrial con red de masas correcta el beneficio de apantallamiento supera con mucho al problema del bucle. Los fabricantes de drives lo recomiendan de forma unánime.

Anécdota real muy útil: ejes que fallan sólo cuando arranca otra máquina de la nave. Es un problema de acoplamiento por red o por tierra, no del servo.

### 56. Conexión de la regeneración y del freno de retención

Regeneración: el puente entre B2 y B3 conecta la resistencia interna. Si se monta una externa hay que RETIRARLO; si no, quedan las dos en paralelo, baja la resistencia total por debajo del mínimo admisible y se puede dañar el transistor de frenado. Además hay que declarar la capacidad de la resistencia externa en Pn600 para que la protección térmica del drive calcule bien.

Freno: es un electroimán de 24 V CC normalmente cerrado. Tres reglas:
1) Fuente propia o al menos circuito propio: la corriente de conexión/desconexión es alta y perturba las E/S.
2) Supresor de sobretensión (varistor o diodo) en la bobina; al cortar una bobina se generan picos de cientos de voltios que destruyen contactos y perturban la electrónica.
3) El contacto de mando debe estar dimensionado para carga inductiva de continua, que es mucho más exigente que la alterna.

Recuerde: /BK es una señal lógica del drive que hay que asignar a una salida física con Pn50F y que normalmente ataca a un relé intermedio.

### 57. Esquema de conexiones completo del SGDXS-□□□A

Ésta es probablemente la figura más útil de todo el manual y conviene imprimirla en A3 y tenerla en el armario durante la instalación.

Recórrala por zonas, no de golpe:
1) Arriba a la izquierda, el circuito de potencia: 1QF (interruptor automático), 1FLT (filtro), 2KM (contactor de potencia), 1KM (contactor de control) y la maniobra de marcha/paro con 1Ry y la lámpara 1PL de alarma.
2) Arriba a la derecha, motor (U, V, W) y encoder por CN2, más los monitores analógicos de CN5.
3) En el centro-izquierda, las consignas: V-REF (velocidad), T-REF (par) y el tren de pulsos PULS/SIGN con su señal de borrado CLR.
4) En el centro-derecha, las salidas: códigos de alarma ALO1-3, salidas de encoder PAO/PBO/PCO, salida de posición absoluta PSO y las tres salidas de propósito general /SO1, /SO2 y /SO3, más la de alarma ALM.
5) Abajo, las entradas de secuencia /SI0 a /SI6 alimentadas desde +24VIN, y el conector de seguridad CN8 con sus dos canales HWBB y la salida EDM1.

Detalle importante que aparece en el pie de la figura: la fuente de 24 V CC no la suministra YASKAWA y debe ser de aislamiento doble o reforzado.

### 58. Circuito de potencia con sus protecciones

Este esquema responde exactamente a la petición de 'potencia y protecciones eléctricas'. Es el circuito recomendado por el fabricante y conviene tomarlo como referencia de diseño.

Puntos que hay que explicar:
· Los absorbedores de sobretensión (1SA, 2SA, 3SA) van sobre las bobinas de los contactores y en la entrada: protegen frente a los picos de maniobra, que son una fuente clásica de averías electrónicas.
· El diodo 1D en la bobina del relé cumple la misma función en continua.
· La cadena de alarma es lo que convierte un fallo del drive en un corte real de potencia, en lugar de dejar la máquina energizada con un eje muerto.

Para el SGDXS-200A00A: 15 A de entrada, luego el 1QF y el 2KM se dimensionan por encima de ese valor, consultando la tabla de periféricos del manual.

### 59. Secuencia de encendido, según el manual

Este cronograma es la versión oficial de la secuencia que vimos en la lámina anterior. Merece la pena compararlas.

El dato de seguridad más importante de todo el módulo está aquí: el manual exige esperar al menos 15 minutos tras cortar la alimentación antes de manipular los bornes. Es más de lo que la mayoría de los técnicos supone, y es tiempo de seguridad, no una recomendación conservadora.

Insista: el indicador CHARGE apagado es condición necesaria pero no suficiente. Siempre verificación de ausencia de tensión con multímetro.

### 60. Resistencia de regeneración externa: el puente `B2`-`B3`

Novedad de la Σ-X frente a la Σ-7: además de Pn600 (capacidad en vatios) hay que ajustar Pn603 (resistencia en ohmios). En la Σ-7 sólo existía el primero. Es un error habitual en quien viene de la serie anterior.

Si se dejan las dos resistencias en paralelo por no retirar el puente, la resistencia total baja de los 10 Ω mínimos y el transistor de frenado puede destruirse.

Recuerde que la resistencia externa se monta ventilada, con termostato de seguridad, y que alcanza temperaturas muy altas.

### 61. Cableado del encoder absoluto y de la batería

La figura muestra las dos formas de alimentar el respaldo del encoder absoluto. Insista en que hay que elegir una.

Recuerde el procedimiento de mantenimiento: sustituir la batería con la alimentación de control conectada evita perder el contaje multivuelta y tener que rehacer el origen de la máquina.

### 62. Cableado del freno de retención

Compare esta figura con el esquema simplificado que vimos antes: es la misma idea, con el detalle real del fabricante.

El manual advierte expresamente de que, si se usa un freno de 24 V, hay que instalar una fuente separada de la de las señales de E/S del conector CN1; si se comparte, las señales pueden funcionar mal.

### 63. Condiciones de instalación para compatibilidad electromagnética

Ésta es la figura que hay que enseñar al montador del armario. La diferencia entre un eje que funciona y uno con alarmas intermitentes está muchas veces en estos detalles.

La tabla que acompaña a la figura en el manual indica qué cables deben ser apantallados: el de señales de E/S, el del dispositivo de seguridad, el del encoder y el del motor.

Recuerde el porqué físico de la abrazadera de 360°: a frecuencias de MHz un conductor de 10 cm tiene impedancia apreciable y la pantalla deja de serlo.

### 64. Puesta a tierra de varios SERVOPACK en el armario

La figura es pequeña porque el recorte del manual lo es: el mensaje es el de la tierra en estrella. Explíquela junto a la de EMC.

El valor de 100 Ω es el criterio de aceptación de la lista de verificación del módulo.

### 65. Instalación mecánica del motor

Este es el puente entre el módulo de instalación y el de sintonización. Si el alumno entiende que la rigidez mecánica fija el techo de las ganancias, entenderá por qué en el Módulo 09 a veces no hay nada más que hacer desde el drive.

Dato práctico: sustituir un acoplamiento elastomérico por uno de fuelle metálico puede permitir subir la ganancia un 50 % o más en ejes exigentes. Es una mejora barata cuando un eje 'no llega'.

### 66. Lista de verificación antes de energizar

Recomiende convertir esta lista en un documento de calidad firmado por el instalador. En caso de incidencia, tener el registro de que se verificó cada punto cambia por completo la conversación.

El punto 4 merece un comentario: si se intercambian dos fases del motor, el eje puede embalarse al activar el servo o disparar alarma de sobrecorriente inmediatamente. Se comprueba en la prueba de JOG del Módulo 08, siempre con la carga desacoplada la primera vez.

El punto 9 es el que más veces provoca la llamada 'el motor no hace nada y no da alarma'.

## MÓDULO 06 — Interfaz de control: CN1, analógico, pulsos y bus

Este módulo conecta el drive con el mundo exterior. El objetivo es que el alumno sea capaz de leer el esquema de un armario ajeno y entender qué señal hace qué, y de diseñar el suyo propio.

Recuerde a lo largo del módulo que los números de pin concretos dependen de la variante de interfaz del amplificador: hay que verificarlos en el manual del modelo instalado.

### 68. Los conectores del SERVOPACK y para qué sirve cada uno

Insista en CN7 y CN8. CN7 porque es la puerta de entrada al equipo para cualquier trabajo serio, y CN8 porque su puente de fábrica es la causa más frecuente de 'no da par y no da alarma'.

CN5 (monitor analógico) es una joya poco conocida: permite sacar velocidad y par a un osciloscopio con una escala configurable por parámetro. En sintonización de ejes difíciles, ver la señal real en un osciloscopio de verdad sigue siendo insustituible.

### 69. Cableado típico de `CN1`

Explique el concepto de alimentación de las entradas: el drive no alimenta sus propias entradas digitales. Hay que llevar los 24 V a un terminal común (+24VIN) y desde ahí los contactos externos cierran cada entrada. Es la causa número uno de 'las entradas no responden' en un primer montaje.

Las entradas son por optoacoplador con común configurable, lo que permite trabajar en lógica positiva (source) o negativa (sink) según cómo se alimente el común. Hay que decidirlo al diseñar el armario y mantener el criterio en toda la máquina.

Las salidas son transistores de colector abierto con capacidad limitada (decenas de miliamperios): no atacan directamente contactores ni electroválvulas. Hay que usar relés intermedios y siempre con supresor en las cargas inductivas.

Los números de pin dependen de la variante: verifíquelos en el manual del equipo instalado antes de cablear.

### 70. Entradas digitales: asignación de fábrica y remapeo

Explique el concepto de asignación: en la Σ-X las señales lógicas no están atadas a un pin. Con Pn50A/Pn50B se decide qué terminal físico (SI0…SI6) activa cada señal lógica, e incluso se puede fijar una señal como 'siempre activa' sin cablearla.

Eso último es muy práctico en un banco de pruebas (por ejemplo, forzar P-OT y N-OT a inactivo para no tener que cablear finales de carrera), pero es PELIGROSO dejarlo así en una máquina de producción. Debe quedar documentado y revisado.

Detalle que confunde a todo el mundo la primera vez: P-OT y N-OT son señales de seguridad con lógica negativa. El contacto debe estar CERRADO en funcionamiento normal, de modo que un cable roto detenga el eje. Es la filosofía correcta, pero sorprende a quien viene de otras marcas.

### 71. Salidas digitales y señales de estado

El ajuste de Pn522 merece una explicación con dibujo: es una ventana alrededor del destino. Se fija en unidades de referencia, es decir, después del engranaje electrónico.

Método práctico para ajustarla: haz un posicionado, mira el error final estabilizado en Un008 y pon Pn522 en un valor unas 3-5 veces mayor que ese error residual, siempre dentro de la tolerancia mecánica de la aplicación.

Un fallo clásico: /COIN se activa antes de que el eje esté realmente quieto porque la ventana es enorme. La máquina empieza la siguiente operación y aparecen defectos de calidad intermitentes.

### 72. Consigna analógica: velocidad y par

Explique la arquitectura clásica de máquina-herramienta: el CNC lee la posición (por el encoder del drive o por una regla), cierra el lazo de posición y envía una consigna de velocidad analógica al drive. El drive es un 'regulador de velocidad de alta calidad'.

El ajuste del offset es un procedimiento clásico de puesta en marcha: con consigna a cero, el eje debe quedar completamente parado. La Σ-X tiene funciones de utilidad específicas para el ajuste automático y manual del offset de las entradas analógicas.

### 73. Consigna por tren de pulsos y salida de encoder

Los tres formatos de tren de pulsos se seleccionan con Pn200.0. Hay que configurar EXACTAMENTE el que emite el controlador; si no, el eje se mueve al revés, a media velocidad o no se mueve.

Diferencia crítica entre line driver y colector abierto: el line driver (RS-422) es diferencial, admite frecuencias altas y cables largos con buena inmunidad. El colector abierto es más sencillo pero limita mucho la frecuencia y la longitud. En un eje de 3 kW con dinámica exigente, usa siempre line driver.

La salida de encoder (PAO/PBO/PCO) reproduce la posición hacia el controlador con la resolución que fije Pn212. Sirve para que el CNC cierre su propio lazo o para sincronizar otro eje como esclavo. PCO es el pulso de marca por vuelta, usado en la búsqueda de origen.

Ojo con Pn212: pedir una resolución de salida demasiado alta a velocidad elevada supera la frecuencia máxima de salida y dispara la alarma correspondiente.

### 74. Disposición de pines del conector `CN1`

Aviso del propio manual que conviene leer en voz alta: el conector de este SERVOPACK es el mismo que el del Σ-XT, así que antes de la prueba de funcionamiento hay que confirmar que se ha conectado el conector correcto.

Insista en la comprobación con los monitores Un005 y Un006: es la forma más rápida de validar un cableado de CN1 sin multímetro.

### 75. Asignación de fábrica de `CN1` (SGDXS analógica / pulsos)

Ésta es la tabla de consulta que hay que tener delante al cablear. Dos señales son nuevas respecto de la serie Σ-7 y conviene señalarlas:
· PSO / /PSO (pines 48-49): salida de posición absoluta, que permite al controlador leer la posición sin secuencia SEN.
· TH (pin 50): entrada de protección contra sobrecalentamiento, pensada para el sensor térmico de motores lineales y de accionamiento directo.

Recuerde el pin 47 (+24VIN): sin él alimentado, ninguna entrada digital funciona y el drive no da ninguna alarma por ello.

### 76. Ejemplo oficial de cableado: control de velocidad

Recorra la figura por zonas:
· Izquierda arriba: la consigna de velocidad V-REF y el límite externo de par T-REF, ambos ±12 V máximo, con par trenzado.
· Izquierda centro: la batería del encoder absoluto y la señal SEN.
· Izquierda abajo: las siete entradas de secuencia alimentadas desde +24VIN, con contactos secos.
· Derecha arriba: códigos de alarma y salidas de encoder, que exigen receptor de línea en el controlador.
· Derecha abajo: las salidas por fotoacoplador, con sus límites de 30 V CC y 50 mA.

Dos notas del manual que conviene leer: la fuente de 24 V no la suministra YASKAWA y debe ser de aislamiento doble o reforzado; y si se usa freno de 24 V hay que alimentarlo con una fuente distinta de la de las señales de CN1.

### 77. Ejemplo oficial de cableado: control de posición

La diferencia respecto del ejemplo de velocidad está en la entrada: aquí aparecen PULS//PULS, SIGN//SIGN y CLR//CLR en lugar de la consigna analógica.

Observe que la señal de borrado del error de posición (CLR) es parte del interfaz: el controlador la usa al hacer el origen y al habilitar el eje. Si queda activa por error, el eje no se mueve aunque lleguen pulsos; es una causa de avería recogida en el capítulo de resolución de problemas del manual.

El parámetro Pn200 define el formato del tren de pulsos y también la forma de la señal CLR.

### 78. Circuitos de entrada de referencia: line driver o colector abierto

Esta figura es la respuesta técnica a la pregunta '¿por qué mi eje pierde pulsos?'. La mayoría de los casos son un colector abierto mal adaptado o un cable demasiado largo.

La tabla de resistencias de pull-up del manual es muy concreta y casi nadie la consulta. Si el controlador tiene salida a colector abierto con fuente propia, hay que verificarla antes de cablear.

Recomendación general: en un eje de 3 kW con dinámica exigente, siempre line driver.

### 79. Circuitos de salida por fotoacoplador

Los 50 mA son el dato que hay que retener. Un relé industrial pequeño consume del orden de 20-40 mA, así que está en el límite; conviene elegir relés de bajo consumo o interponer una tarjeta de acondicionamiento.

Un error clásico es conectar una lámpara de señalización directamente a la salida de alarma: consume más de lo admisible y acaba destruyendo la salida.

### 80. Circuitos de entrada analógica

La figura del manual muestra dos casos: la conexión desde un convertidor D/A del controlador y el ejemplo de cableado para marcha en un solo sentido con una fuente de 12 V y resistencias.

El dato de 30 kΩ de impedancia importa cuando el controlador tiene una salida de baja capacidad o cuando se usan divisores resistivos.

### 81. Sobrerrecorrido, límites y métodos de parada

Comente la diferencia entre parada de sobrerrecorrido y parada de emergencia: la primera es una función del drive, la segunda es una función de seguridad de la máquina que debe resolverse con la cadena de seguridad (Módulo 10).

Detalle importante en ejes verticales: si al detectar sobrerrecorrido el eje queda libre, la carga cae. Hay que configurar la parada con enclavamiento y coordinar con el freno de retención.

Consejo de puesta en marcha: pruebe físicamente los finales de carrera moviendo el eje a baja velocidad y accionándolos a mano antes de trabajar a velocidad nominal.

### 82. Buses de movimiento: MECHATROLINK-III y EtherCAT

Aclare un malentendido habitual: aunque se use bus, la seguridad (CN8/HWBB) y normalmente los finales de carrera siguen siendo cableado físico. El bus transporta el mando, no la seguridad, salvo que se use una capa de seguridad certificada (FSoE).

Sobre los modos CiA 402: el que se usa en el 90 % de las máquinas es csp (cyclic synchronous position), en el que el maestro envía una posición objetivo cada ciclo de bus (típicamente 1-2 ms) y el drive interpola entre puntos. Toda la trayectoria la calcula el maestro.

Ventaja de mantenimiento poco valorada: con bus, los parámetros y el estado del drive son accesibles desde el PLC, lo que permite diagnóstico remoto y sustitución de equipo con recarga automática de parámetros.

### 83. Cómo elegir la arquitectura de control

Cierre el módulo con una recomendación clara: en proyecto nuevo, bus. En retrofit, analógica o pulsos, salvo que también se cambie el controlador.

Un aviso de coste: el bus reduce mucho el cableado y el tiempo de montaje, pero exige competencias de red industrial en el equipo de mantenimiento. Si la planta no las tiene, hay que formar antes de instalar; si no, el primer fallo de comunicación será un día de parada.

## MÓDULO 07 — Parámetros, panel y SigmaWin+

A partir de aquí el curso se vuelve práctico con el equipo. Si dispone de un drive, mantenga este módulo con el equipo encendido y el PC conectado.

Regla que hay que establecer desde el principio: antes de tocar nada, guardar una copia de la configuración actual. Siempre.

### 85. El panel frontal: leer el estado sin PC

Enseñe a interpretar el display en el equipo real. Al energizar, el drive muestra su estado; ante un fallo, el código de alarma con el formato A.xxx.

La navegación por el panel sigue siempre el mismo patrón: se elige la familia de función (parámetros, monitores, funciones de utilidad), se navega hasta el número deseado, se entra en el valor, se modifica y se confirma.

El panel es suficiente para diagnóstico y para cambios puntuales, pero para sintonizar o para cargar una configuración completa hay que usar SigmaWin+. Nadie sintoniza un eje con cinco dígitos y cuatro teclas.

Detalle útil: el punto decimal parpadeante en algunos dígitos indica estados concretos (por ejemplo, que el valor mostrado está pendiente de confirmación). Consulte la leyenda del manual.

### 86. La lógica de la Σ-X: `Pn`, `Fn` y `Un`

Truco didáctico: pida a los alumnos que asocien cada familia con un verbo. Pn = configurar. Fn = hacer. Un = mirar.

Los monitores Un son la herramienta de diagnóstico más rápida que existe: sin PC, sin cables, directamente en el display. Un005 y Un006 (estado de entradas y salidas) resuelven en 30 segundos la pregunta '¿le está llegando la señal de servo ON o no?'.

### 87. Editar un parámetro: procedimiento y precauciones

El paso 5 es el más importante desde el punto de vista metodológico. En sintonización, cambiar varias cosas a la vez es la forma más rápida de perderse.

Sobre los avisos de reinicio: es una fuente de confusión clásica. El técnico cambia el parámetro, prueba, no ve diferencia, y concluye que el parámetro 'no hace nada'. En realidad hacía falta un ciclo de alimentación.

Recomiende una convención de nombres para los ficheros de parámetros: MAQUINA_EJE_FECHA_motivo.  Por ejemplo: LINEA3_EJEX_20240115_ajuste_ganancias.

### 88. SigmaWin+: la herramienta imprescindible

Insista en la función de traza: es lo que separa el ajuste 'por oído' del ajuste con criterio. Ver el error de seguimiento en función del tiempo, superpuesto al perfil de velocidad, permite decidir con datos qué ganancia tocar.

El modo offline es un argumento de venta interno muy potente: permite que un ingeniero prepare toda la configuración desde la oficina y que la puesta en marcha en cliente se reduzca a volcar y verificar.

Comente que el SGDXS (Σ-X) se trabaja con **SigmaWin+ Ver.7**. La versión 5 es otra generación de interfaz: no la mezcle en el aula. Descargue siempre la última versión compatible desde la web de YASKAWA.

Las láminas siguientes son capturas oficiales de SigmaWin+ Ver.7 tomadas del manual SIEP C710812 03I. El aspecto puede variar ligeramente según la revisión del software, pero los bloques del menú y el flujo son los mismos.

### 89. Conexión del operador digital al SERVOPACK

La figura del operador digital es textual en el manual: el mensaje importante es usar el cable original y el conector correcto.

CN7 es USB; CN3 es el operador. No se intercambian.

### 90. El mapa de SigmaWin+: estado del eje y menú de funciones

Esta es la lámina de orientación. El alumno debe poder señalar, sin pensar, en qué bloque está cada tarea.

Truco de aula: pida nueve voluntarios y asigne un bloque a cada uno. Luego lance situaciones ('el eje no gira', 'quiero ver el error de seguimiento', 'hay una alarma A.720') y que el grupo diga el bloque.

HBB encendido = el CN8 está abriendo el HWBB: el eje no dará par aunque todo lo demás esté bien. Es el primer LED que hay que mirar.

### 91. Flujo de trabajo la primera vez que abres SigmaWin+

Haga este flujo en el banco, en voz alta, la primera vez. Luego pida a cada alumno que lo repita solo.

Sobre el driver USB: si el PC no ve el drive, no es un problema de SigmaWin+, es de Windows. Compruebe el Administrador de dispositivos antes de reinstalar el software.

Modo offline: se puede preparar un proyecto sin drive (útil en oficina). Al llegar a planta se conecta y se vuelca. No sustituye la copia 'como llegó' del equipo real.

### 92. Editar parámetros: nombre, rango, unidades y escritura

Demuestre en vivo el ciclo verde → Write → blanco. Es el gesto que hay que automatizar.

Compare con el panel: en el display no ves el nombre, ni el rango, ni las unidades. Por eso se edita mal y se confirma peor.

Edited Parameters vs All Parameters: lo normal es escribir sólo lo cambiado. All Parameters se usa al clonar un eje o al restaurar un fichero completo.

### 93. JOG desde SigmaWin+: el primer movimiento del motor

El JOG es la prueba de que potencia, encoder y motor están bien. Si el motor no gira aquí, no tiene sentido pasar al PLC.

Insista en el 'dead-man': sólo se mueve mientras se mantiene el botón. Eso evita que un clic accidental deje el eje lanzado.

Pn304 a 500 min⁻¹ como en la captura del manual es demasiado para un primer arranque didáctico. Bájelo.

### 94. Monitor en vivo: lo que el panel muestra, pero entero

Rutina de tres pestañas: Operation (¿qué hace el eje?), Status (¿está listo?) e I/O (¿le llegan las señales?).

A.810 es un ejemplo didáctico excelente: mucha gente busca un fallo de sintonización y es la pila del encoder absoluto.

Compare con Un005/Un006 del panel: misma información, menos cómoda.

### 95. La traza: el osciloscopio que lleva el SERVOPACK dentro

Esta es la herramienta que separa al técnico que 'o ye el eje' del que decide con datos. Dedíquele tiempo de práctica.

Ejercicio: capture un posicionamiento, identifique sobrepaso, tiempo de establecimiento y par de punta. Luego suba Pn102 un 20 % y repita. La comparación enseña más que diez láminas.

Real Time Trace es la versión continua; Trace es la de disparo, más útil para un ciclo concreto.

### 96. Autoajuste guiado: el drive propone las ganancias

Muestre la tabla before/after: es la prueba de que el software no es 'magia', escribe Pn100, Pn101, Pn102, Pn103, filtros…

Después del autoajuste, verifique con el ciclo real y con la traza. Aceptar a ciegas el resultado es tan malo como no usarlo.

El detalle de Pn103 (inercia) es el puente con el Módulo 04: compare el valor medido con el calculado.

### 97. Análisis mecánico: ver la resonancia en un diagrama de Bode

Conecte esta lámina con el Módulo 09: notch, EasyFFT y análisis en frecuencia dejan de ser abstractos cuando se ve la gráfica.

Interpretación mínima: un pico de ganancia = la mecánica 'canta' a esa frecuencia. El notch la atenúa para poder subir ganancias sin que el eje silbe o oscile.

### 98. Alarmas e historial: el primer sitio al que ir cuando el eje para

El historial es oro en mantenimiento: '¿esto es nuevo o ya pasaba hace dos semanas?'. Enséñeles a no pulsar Clear por higiene.

Puente con el Módulo 11: el método de diagnóstico empieza siempre aquí, no en cambiar ganancias.

### 99. Qué pantalla abrir según lo que necesites

Cierre del bloque de software con una chuleta. Imprímala y péguela en el maletín junto al cable USB.

Recuerde: el panel frontal sigue siendo válido para JOG, Un y Fn cuando no hay PC. SigmaWin+ no sustituye el criterio; lo acelera.

### 100. Monitor analógico `CN5`

CN5 es una herramienta poco conocida y muy valiosa. En ejes difíciles, ver la señal real en un osciloscopio sigue siendo insustituible.

### 101. El engranaje electrónico

Este concepto genera muchas dudas, así que conviene explicarlo con una pregunta: ¿en qué unidades quieres programar la máquina? ¿En milímetros? ¿En micras? ¿En grados? El engranaje electrónico es lo que traduce esa unidad de referencia a cuentas del encoder.

Fórmula general: B/A = (resolución del encoder × relación de transmisión) / (unidades de referencia por vuelta del eje de carga).

Ejemplo del diagrama: encoder de 24 bits (16.777.216 cuentas/vuelta), husillo de 20 mm de paso, y queremos programar en micras. Una vuelta de motor son 20 mm = 20.000 micras. Luego B/A = 16.777.216 / 20.000.

Dos advertencias:
1) Si la fracción no es exacta, hay error de redondeo que se acumula. Elija unidades que den fracciones exactas siempre que pueda.
2) Cambiar el engranaje cambia el significado de TODOS los parámetros expresados en unidades de referencia (Pn522, Pn520, velocidades de consigna). Hay que revisarlos después.

### 102. Engranaje electrónico: tres ejemplos resueltos

El caso de la mesa rotativa merece atención: si la fracción no es exacta, el error se acumula vuelta tras vuelta y al cabo de miles de posicionados la mesa se ha 'ido'. En ejes rotativos infinitos hay que elegir la unidad de referencia de modo que la fracción sea exacta, o usar la función de límite multivuelta coherente con la relación de transmisión.

Comprobación práctica infalible tras configurar el engranaje: ordena un movimiento de 100 mm (o de 100 unidades conocidas) y **mídelo con un metro o un comparador**. Si no coincide, el engranaje está mal. Esta comprobación de 2 minutos evita fallos que aparecerían meses después.

### 103. Los parámetros que más vas a tocar (1/2)

Pn000.0 merece un comentario: cambiar el sentido de giro por parámetro es lo correcto. Intercambiar dos fases del motor 'para que gire al revés' es un error grave: el encoder sigue indicando el sentido original, la realimentación queda invertida y el eje se embala o dispara alarma.

Pn520 es el guardián de la mecánica: si el eje no puede seguir la consigna (choque, atasco, dimensionamiento insuficiente), esta alarma detiene el movimiento antes de romper algo. No lo suba sin entender por qué está saltando.

### 104. Los parámetros que más vas a tocar (2/2)

No entre en detalle aquí: es un mapa, no el territorio. Basta con que el alumno sepa que existe un conjunto reducido de parámetros que resuelve el 95 % de los casos.

Mensaje importante: el manual tiene cientos de parámetros, pero en la práctica un especialista toca habitualmente unos veinte. Eso tranquiliza mucho a quien empieza.

### 105. Monitores `Un` para diagnóstico rápido

Enseñe la rutina de diagnóstico en tres monitores: Un005 (¿llegan las señales?), Un002 (¿cuánto par está pidiendo?) y Un008 (¿está siguiendo la consigna?). Con esos tres se descarta el 70 % de las causas en cinco minutos.

Un002 tiene un valor especial para el ingeniero: permite comparar el par real con el calculado en el Módulo 04. Si el eje pide un 90 % de par donde el cálculo decía 47 %, hay un problema mecánico que hay que resolver antes de que rompa algo.

### 106. Copia de seguridad y gestión de configuraciones

Este es el módulo donde conviene hablar de gestión: el mejor técnico del mundo no puede arreglar en una hora una máquina cuya configuración se perdió.

Proponga un formato de etiqueta para pegar dentro del armario, junto al drive, con: modelo de drive, modelo de motor, versión de firmware, fecha de puesta en marcha, fecha del último cambio de batería y ruta del fichero de parámetros en el servidor.

## MÓDULO 08 — Puesta en marcha paso a paso

Este es el módulo más práctico del curso. Si hay banco de pruebas, dedique la mayor parte del tiempo a ejecutar el procedimiento con los alumnos.

El principio rector es 'aislar variables': se prueba primero el amplificador solo, después el motor sin carga, después con carga a baja velocidad, y sólo al final el ciclo completo. Cada fase debe superarse antes de pasar a la siguiente. Cuando algo falla, se sabe exactamente qué se acaba de cambiar.

### 108. El método: seis fases, sin saltos

Explique el principio de aislamiento de variables. Si se conecta todo y se arranca, cuando algo falla hay veinte causas posibles. Avanzando por fases, cuando algo falla sólo hay una: lo último que se ha cambiado.

Este método no es más lento; es mucho más rápido, porque el tiempo perdido en diagnóstico a ciegas siempre supera al tiempo invertido en hacer las cosas en orden.

Insista en la fase 0: la verificación previa es la que evita destruir equipo. Cinco minutos con el multímetro antes de energizar.

### 109. Fase 1 — Primer energizado

Insista en la primera línea: motor desacoplado. Si el sentido de giro está invertido o el engranaje electrónico mal calculado, un eje acoplado puede embalarse contra el tope mecánico en menos de un segundo.

La comprobación de Un005 es un truco muy útil que ahorra tiempo: en lugar de medir con el multímetro pin a pin, el drive te dice qué entradas ve activas.

Recuerde el caso de CN8: si el puente de seguridad no está y el circuito HWBB no está cableado, /S-RDY no se activará o el eje no dará par sin alarma evidente.

### 110. Fase 2 — Prueba de JOG sin carga (`Fn002`)

La prueba de JOG es el mejor diagnóstico inicial que existe. Un motor que gira suave y silencioso en vacío, con par casi nulo, es un motor sano bien cableado.

Si el motor vibra o hace ruido en vacío, las causas más probables son: ganancias de fábrica demasiado altas para esa mecánica, problema en el cable de encoder, o fases mal conectadas.

Sobre el sentido de giro: la convención de YASKAWA es que el sentido positivo se ve antihorario mirando desde el lado del eje. Pn000.0 invierte esa convención sin tocar nada más del sistema.

### 111. Fase 3 — Configuración básica del eje

Ordene los pasos por dependencia: el engranaje electrónico debe estar antes que Pn520 y Pn522, porque estos últimos se expresan en unidades de referencia y su significado cambia con el engranaje.

La comprobación del engranaje midiendo un desplazamiento real es obligatoria y no admite atajos. Dos minutos aquí evitan semanas de desconcierto.

### 112. Fase 4 — Encoder absoluto y origen de máquina

Explique la diferencia entre 'posición absoluta del encoder' y 'cero de la máquina'. El encoder sabe dónde está el rotor; sólo la máquina sabe dónde está su cero útil. La relación entre ambos es el offset de origen, que vive en el controlador.

En algunas arquitecturas ese offset se guarda en el propio drive; en otras, en el PLC. Sea cual sea, debe estar documentado y respaldado.

Ejercicio recomendado: simule una sustitución de drive. Cargue los parámetros en otro equipo, ejecute Fn008 y compruebe cuánto se tarda en recuperar el eje. Es un ensayo que vale su peso en oro cuando ocurra de verdad.

### 113. Fase 5 — Acoplar la carga y probar el ciclo

El paso 3 (recorrer todo el rango a baja velocidad observando el par) es un diagnóstico mecánico de altísimo valor y coste cero. Un husillo torcido, un rodamiento dañado o una guía sucia se detectan inmediatamente como un aumento local del par.

El paso 7 es el que más se salta y el que más problemas evita: muchos ejes funcionan perfectamente durante diez ciclos y disparan A.720 (sobrecarga continua) tras media hora de producción, porque el par RMS real es mayor que el calculado.

### 114. Acta de puesta en marcha del eje

Insista en el valor económico de documentar: el coste de media hora de documentación frente al coste de un día de parada por no saber cómo estaba configurado un eje.

Sugerencia: convertir esta tabla en una plantilla corporativa (Word o formulario digital) que se rellene en cada puesta en marcha.

### 115. Los diez errores más frecuentes en puesta en marcha

Puede usar esta tabla como cierre del módulo y como test rápido: pida a los alumnos que expliquen por qué cada error tiene la consecuencia indicada. Si saben justificarlo, han entendido el módulo.

El error número 5 (autoajuste sin carga) es sutil y muy común: el técnico prueba en vacío porque es cómodo, obtiene un ajuste 'que va bien', acopla la carga y todo se degrada. La inercia es lo que el autoajuste mide, y sin carga mide otra máquina.

## MÓDULO 09 — Sintonización del lazo de control

El módulo más técnico y el que más practica requiere. Conviene alternar teoría con ejercicios en el banco.

Advertencia pedagógica: la sintonización no es un procedimiento cerrado sino un compromiso entre rapidez, precisión y estabilidad. El alumno debe salir sabiendo qué está negociando en cada momento.

### 117. Cómo se ve una sintonización buena y una mala

Este diagrama es el vocabulario visual del módulo. Los alumnos deben aprender a clasificar de un vistazo la traza que ven en SigmaWin+.

· Sobreamortiguado: llega tarde pero sin pasarse. Ganancia insuficiente. Seguro pero lento; en muchas aplicaciones industriales es un ajuste aceptable si el tiempo de ciclo lo permite.
· Óptimo: llega rápido, con un sobrepasamiento mínimo o nulo, y se queda quieto. Es el objetivo.
· Subamortiguado: se pasa y oscila varias veces antes de estabilizarse. Ganancia excesiva o mal repartida entre lazos. Aunque el tiempo hasta el primer cruce sea corto, el tiempo hasta estabilizar es mayor: es más lento en la práctica y castiga la mecánica.

Insista en esto último, que es contraintuitivo: pasarse de ganancia no hace la máquina más rápida, la hace más lenta y más ruidosa.

### 118. Los criterios: qué es un eje bien sintonizado

Ejemplos que aclaran el compromiso:
· Máquina de corte por láser: prioridad al error de seguimiento durante la trayectoria; un error de contorno estropea la pieza.
· Paletizadora: prioridad al tiempo de ciclo y a la suavidad; da igual un error de 0,5 mm durante el movimiento.
· Rectificadora: prioridad a la estabilidad y al acabado; una vibración de alta frecuencia deja marcas en la pieza.

El indicador de rigidez en parado se comprueba de forma muy visual: empujando el eje a mano (cuando es seguro hacerlo) y observando cuánto cede y cómo vuelve.

### 119. Las herramientas de ajuste de la Σ-X

Establezca la estrategia recomendada:
1) Empiece por el autoajuste avanzado con la carga real.
2) Afine con el ajuste de un parámetro hasta el límite de ruido.
3) Sólo si no basta, pase a manual y a filtros.

El error típico del principiante es ir directo al ajuste manual 'porque es más profesional'. El autoajuste de la Σ-X es muy bueno y deja un punto de partida difícil de mejorar a mano en poco tiempo.

El error típico del experimentado es dejar activo el tuning-less mientras intenta ajustar a mano y no entender por qué sus cambios 'no hacen nada'.

### 120. Procedimiento de autoajuste avanzado (`Fn201`)

Comente qué hace realmente el autoajuste: excita el sistema, mide la respuesta, estima la inercia y sube la ganancia hasta detectar el principio de inestabilidad; después retrocede con un margen de seguridad y coloca filtros notch en las resonancias detectadas.

Por eso hace ruido: está buscando el límite a propósito.

El dato más valioso que devuelve es Pn103, la relación de inercias medida. Compárela con la calculada en el Módulo 04: si difieren mucho, alguna hipótesis del cálculo era falsa y conviene averiguar cuál.

### 121. Ajuste manual: el orden es innegociable

Explique la relación entre los lazos: el lazo de velocidad debe ser sensiblemente más rápido que el de posición (una regla habitual es un factor de 4 a 5 entre sus anchos de banda). Si se violenta esa relación, el sistema oscila.

Método práctico para Pn100: subir en escalones del 20 %, y en cada escalón hacer un movimiento corto y escuchar. El oído humano detecta el principio de inestabilidad antes que muchos instrumentos.

Un detalle sobre Pn401: es tentador subirlo para 'silenciar' el eje, pero el filtro introduce retardo en el lazo más interno, que es exactamente donde menos se puede permitir. Si hay ruido de alta frecuencia, casi siempre es mejor un filtro notch bien colocado que un filtro de par alto.

### 122. Resonancia mecánica y filtros notch

Explique la física: motor, acoplamiento y carga forman un sistema masa-muelle-masa con una frecuencia de resonancia propia. Si el lazo de control tiene ganancia suficiente a esa frecuencia, el sistema oscila.

Hay dos formas de resolverlo: bajar la ganancia (funciona, pero sacrifica prestaciones en todo el rango) o quitar ganancia sólo en esa frecuencia concreta. Eso último es exactamente lo que hace un filtro notch.

Procedimiento: se localiza la frecuencia con la función de análisis (Fn206 / análisis mecánico de SigmaWin+), se introduce en Pn409, y se ajusta la anchura con el factor Q (Pn40A) y la profundidad (Pn40B). Un notch demasiado ancho resta prestaciones; demasiado estrecho no atrapa la resonancia si esta se desplaza con la posición o la temperatura.

Hay dos filtros notch disponibles, lo que permite atacar dos resonancias distintas. El autoajuste avanzado los coloca automáticamente cuando detecta resonancia.

Advertencia importante: el filtro notch enmascara el síntoma pero no arregla la mecánica. Si la resonancia procede de un acoplamiento flojo o de un rodamiento dañado, hay que repararlo.

### 123. Vibración de baja frecuencia y control por modelo

La distinción clave para el alumno: resonancia de alta frecuencia (cientos o miles de hercios, ruido agudo, se resuelve con notch) frente a vibración de baja frecuencia (unos pocos hercios, se ve a simple vista, se resuelve con supresión de vibración o rigidizando).

Sobre el control por modelo en interpolación: es un punto fino. Si un eje tiene MFC y otro no, sus respuestas dinámicas difieren y la trayectoria resultante se deforma en las esquinas. En máquinas de contorneado hay que configurar todos los ejes de forma homogénea.

### 124. Diagnóstico por síntomas: qué tocar en cada caso

La última fila merece énfasis: cuando un eje que iba bien empieza a ir mal, la causa casi nunca está en el drive. Los parámetros no se cambian solos; la mecánica sí se desgasta.

Ese es también el mejor argumento para guardar las trazas de la puesta en marcha: permiten comparar objetivamente el comportamiento de hoy con el de hace dos años y demostrar que algo ha cambiado en la máquina.

### 125. Errores frecuentes al sintonizar

Cierre el módulo con esta idea: el objetivo no es demostrar lo rápido que puede ir el eje, sino entregar una máquina que funcione de forma estable durante años.

Comente el efecto de la temperatura: la viscosidad del lubricante cambia con la temperatura, y con ella la fricción y el amortiguamiento del sistema. Un ajuste hecho al límite con la máquina caliente puede oscilar en el primer arranque de un lunes de invierno. Por eso el margen del 10-20 % no es opcional.

## MÓDULO 10 — Seguridad funcional: STO / HWBB

Módulo corto pero crítico. El objetivo no es convertir al alumno en experto en seguridad de máquinas, sino que sepa qué ofrece el drive, qué no ofrece, y cuándo hay que llamar a un especialista.

Advertencia que hay que hacer explícita: el diseño de la función de seguridad de una máquina requiere un análisis de riesgos y competencias específicas. Este módulo explica la pieza que aporta el SERVOPACK, no sustituye a ese análisis.

### 127. El marco normativo, en lo que afecta al servo

El punto del recuadro es el más malinterpretado del módulo. Un componente 'apto para PL e' insertado en una arquitectura de categoría 1 no da PL e.

Sobre las funciones de IEC 61800-5-2: STO (par desactivado) es la base y la que implementa el hardware del drive. Otras funciones como SS1 (parada controlada seguida de STO) se construyen combinando el drive con un módulo de seguridad temporizado o con un drive con funciones de seguridad ampliadas.

### 128. La función HWBB y el conector `CN8`

Explique la arquitectura de dos canales: el módulo de seguridad abre simultáneamente dos circuitos independientes. Cada uno, por separado, es capaz de bloquear los transistores de potencia. Así, un fallo en un canal (un contacto pegado, un cable cortado) no impide que la función actúe.

La señal EDM (External Device Monitoring) cierra el lazo de diagnóstico: el drive informa al módulo de seguridad de que efectivamente ha entrado en estado seguro. Si el módulo abre los canales y EDM no cambia de estado, hay un fallo interno y el sistema debe pasar a estado seguro y avisar. Esta vigilancia cruzada es lo que permite alcanzar categoría 3 / PL e.

Dato práctico fundamental: CN8 se suministra con un conector puente de fábrica. Si se retira sin cablear la seguridad, el drive queda permanentemente en baseblock: no dará par y no habrá alarma evidente. Es la causa número uno de la llamada 'el motor nuevo no funciona'.

### 129. Pines del conector de seguridad `CN8`

Detalle que el manual recoge expresamente y que sorprende: los pines 1 y 2 no deben usarse porque están conectados a circuitos internos.

Y una precisión importante del propio manual: el uso o no de la señal EDM1 no afecta al nivel de prestaciones de los parámetros de seguridad del drive. Aun así, sin EDM1 el módulo de seguridad no puede detectar un fallo interno del amplificador, con lo que el diagnóstico del conjunto empeora.

Recuerde: CN8 se suministra con un conector puente instalado. Para usar la función de seguridad hay que retirarlo y conectar el dispositivo.

### 130. Ejemplo oficial de conexión de la seguridad

Dos advertencias del manual que hay que trasladar:

1) La lógica de las señales de seguridad es la contraria a la del resto del conector: aquí el común es 0 V y la salida es de tipo source. Esto confunde a quien cablea CN1 y CN8 el mismo día.

2) Hay que usar un interruptor con contactos de muy baja corriente. Los contactos de potencia forman una capa de óxido cuando conmutan corrientes muy pequeñas y pueden dejar de conducir: es un modo de fallo peligroso en un circuito de seguridad.

El fusible protege el cableado frente a un cortocircuito que dejaría la función de seguridad inoperante.

### 131. STO no es parada de emergencia

Este es el mensaje que hay que asegurarse de que se lleven a casa. Es un error que se comete con frecuencia en máquinas reales.

Explique la diferencia entre 'quitar el par' y 'parar'. Con una gran inercia, quitar el par y dejar el eje libre puede ser MÁS peligroso que una parada controlada, porque el eje sigue moviéndose sin control.

Por eso existe SS1: primero se frena de forma controlada con el drive y después, una vez parado, se aplica STO. Se implementa con un relé de seguridad temporizado, y el análisis de riesgos decide el tiempo.

### 132. Validación y mantenimiento de la función de seguridad

El paso 4 (medir el tiempo de parada real) es el que más se omite y el que tiene consecuencias más directas: las distancias de seguridad de una barrera inmaterial se calculan a partir del tiempo de parada. Si el tiempo real es mayor que el supuesto, la protección es insuficiente.

Recuerde también que el tiempo de parada aumenta con el desgaste del freno y con cambios en la carga, y que por eso hay que volver a medirlo periódicamente.

Insista en que el diseño de la función de seguridad corresponde a personal cualificado y debe quedar documentado en el expediente técnico de la máquina.

## MÓDULO 11 — Diagnóstico, alarmas y mantenimiento

Módulo orientado a mantenimiento. El objetivo es reducir el tiempo medio de reparación, y eso se consigue con método, no con memoria.

Si el grupo es de mantenimiento, este es probablemente el módulo que más van a usar. Dedique tiempo a los árboles de decisión y practique con averías simuladas si dispone de banco.

### 134. Un método de diagnóstico que funciona siempre

El error clásico en diagnóstico es empezar cambiando piezas. Este método obliga a recoger información antes de actuar.

Los pasos 1 y 2 (qué dice el drive y qué dice el historial) resuelven una parte muy grande de los casos en dos minutos, sin herramientas.

El paso 4, dividir el sistema, es la idea central: el sistema tiene cuatro bloques (controlador, drive, motor, mecánica) y dos enlaces (cableado de mando, cableado de potencia y encoder). Cada prueba debe descartar un bloque. Por ejemplo, un JOG desde el panel descarta de golpe el controlador y todo el cableado de mando.

El paso 6 (documentar) es el que convierte una reparación en conocimiento de planta.

### 135. Alarmas y avisos: cómo se comportan

Insista en el valor de los avisos: el drive dispone de un modelo térmico que sabe cuánto margen de sobrecarga queda. Esa información, llevada al HMI, permite planificar.

Sobre el historial de alarmas: es la primera herramienta a consultar en cualquier avería. Muchas veces la alarma que ve el operario es consecuencia de otra anterior, y sólo el historial lo revela.

Advertencia sobre el reset compulsivo: reiniciar una alarma de sobrecarga sin resolver la causa térmica es una manera eficaz de destruir un motor.

### 136. Alarmas frecuentes (1/2): potencia, sobrecarga y movimiento

Enseñe a razonar por familias en lugar de memorizar códigos. Con el prefijo ya se sabe si el problema es de potencia, térmico, de seguimiento o del encoder.

A.7__ (sobrecarga) es la alarma que más aparece en producción y casi siempre tiene causa mecánica: guías secas, rodamiento agarrotado, freno que no libera del todo, o producto atascado. Antes de tocar el drive, compruebe el par con Un002 y compare con el histórico.

A.d__ (error de posición) merece una regla: nunca se resuelve subiendo el umbral Pn520. Eso es apagar la alarma de incendios.

### 137. Alarmas frecuentes (2/2): encoder, parámetros y comunicación

Cuente la estrategia para alarmas intermitentes de encoder, que son las más frustrantes:
1) Mover el cable con la máquina en marcha (con seguridad) para ver si se reproduce: delata rotura por fatiga en cadena portacables.
2) Comprobar que la malla está a tierra en ambos extremos con abrazadera de 360°.
3) Comprobar separación respecto a cables de potencia.
4) Sustituir el cable por uno nuevo original antes de sustituir el motor: es mucho más barato y resuelve la mayoría de los casos.

Sobre A.81_: es la alarma que aparece tras las paradas largas de planta. La solución es preventiva: cambiar baterías cada dos años con el equipo energizado.

### 138. Árbol de decisión: «el eje no se mueve»

Recorra el árbol de izquierda a derecha con el grupo, planteando cada pregunta en voz alta.

La primera bifurcación (¿hay alarma?) es decisiva: con alarma, el drive ya ha hecho el diagnóstico y sólo hay que interpretarlo. Sin alarma, el problema está casi siempre en las condiciones de habilitación: servo ON, seguridad CN8, finales de carrera o consigna.

El caso 'sin alarma y sin par' es el más confuso para el principiante y tiene tres sospechosos habituales: CN8 sin cablear tras retirar el puente, /S-ON no llega (comprobable en Un005) o falta la alimentación de +24VIN de las entradas.

El caso 'con par pero sin movimiento' apunta a consigna ausente (Un007 sin pulsos, o telegrama de bus sin actualizar) o a bloqueo mecánico, que se distingue porque el par sube al máximo.

### 139. Mantenimiento preventivo del conjunto

La Σ-X dispone de monitores de vida útil de componentes (ventilador, condensadores, relés internos) que estiman el porcentaje consumido. Consúltelos en SigmaWin+ y llévelos al plan de mantenimiento: es mantenimiento predictivo gratuito que casi nadie usa.

El reapriete de bornes es una tarea humilde y muy rentable: un borne flojo en un cable de motor de 18 A provoca calentamiento, caída de tensión asimétrica y, con el tiempo, un incendio o una avería del amplificador.

### 140. Sustitución de un SERVOPACK o de un motor

El paso 6 es el que convierte una sustitución rutinaria en un problema. Insista de nuevo: el origen no viaja en el fichero de parámetros.

Sobre el paso 3: en almacén acaban conviviendo equipos parecidos con sufijos distintos. Un SGDXS-200A00A con interfaz de bus no sirve para sustituir a uno con interfaz analógica, aunque físicamente encaje.

Recomiende ensayar el procedimiento una vez en condiciones controladas, por ejemplo durante una parada programada. La primera vez siempre aparecen sorpresas, y es mejor que aparezcan un martes por la mañana.

## MÓDULO 12 — Proyecto integrador

El proyecto integrador es la parte que consolida el aprendizaje. Idealmente se trabaja en grupos de dos o tres personas a lo largo del curso, entregando cada bloque al terminar el módulo correspondiente.

Si el grupo tiene una máquina real en su planta, sustituya el enunciado por esa máquina: el valor formativo se multiplica.

### 142. El encargo

El ejercicio de traducir requisitos a decisiones técnicas es el más valioso del proyecto. Hágalo en común en la pizarra antes de que los grupos empiecen a calcular.

Requisitos y sus consecuencias:
· Repetibilidad ±0,05 mm → mecánica de precisión, ventana Pn522 coherente y sintonización cuidada.
· Tres turnos en nave sin climatizar → margen térmico amplio, verificación de par RMS con holgura y atención a la condensación.
· Parada segura → CN8 cableado y validado, no puenteado.
· Caídas de red del 10 % → comprobar la curva a tensión mínima y considerar la alarma A.410.

### 143. Entregable 1 — Dimensionamiento

Insista en el criterio 'ninguna cifra sin origen documentado'. En ingeniería, un número sin trazabilidad es una opinión.

Valore especialmente la alternativa: pedir que comparen SGMXA-30A (3.000 rpm) con SGMXG-30A (1.500 rpm) obliga a razonar sobre par, velocidad e inercia en lugar de aplicar una receta.

### 144. Entregable 2 — Arquitectura eléctrica y de control

Este entregable es el más 'de oficina técnica'. Si el grupo no tiene experiencia en esquemas, acepte croquis a mano alzada: lo importante es el razonamiento, no la herramienta de dibujo.

Punto de discusión interesante: el requisito de diagnóstico remoto empuja hacia una variante de bus, lo que a su vez simplifica el cableado de CN1. Es un buen ejemplo de cómo un requisito aparentemente menor cambia la arquitectura completa.

### 145. Entregable 3 — Hoja de parámetros del eje

El detalle más formativo de este entregable es la comparación entre la relación de inercias calculada y la medida por el autoajuste. Es el momento en que la teoría se enfrenta a la realidad.

Pn522 exige un razonamiento fino: la repetibilidad de ±0,05 mm es una característica del sistema mecánico completo, mientras que Pn522 es la ventana que declara 'posición alcanzada'. No son lo mismo, y conviene que lo discutan.

### 146. Entregable 4 — Plan de puesta en marcha y aceptación

Los criterios de aceptación medibles son la parte más profesional del proyecto: convierten 'la máquina va bien' en algo verificable y contractual.

Si el curso se imparte en varias sesiones, dedique la última a la defensa de los proyectos. Escuchar cómo otro grupo ha resuelto el mismo enunciado de forma distinta es enormemente formativo.

### 147. Rúbrica de evaluación del proyecto

Reparta la rúbrica al inicio del curso, no al final. Saber cómo se evalúa orienta el esfuerzo y mejora mucho la calidad de los entregables.

El peso del dimensionamiento (25 %) es deliberado: es la parte con más contenido de ingeniería y la que más diferencia a un técnico competente.

## MÓDULO 13 — Anexos, evaluación y recursos

Los anexos están pensados para imprimirse y llevarse a planta. Anime a los alumnos a extraer estas diapositivas a PDF y tenerlas en el móvil.

### 149. Ficha rápida — Fórmulas de dimensionamiento

Esta es la diapositiva que más se fotografía de todo el curso. Sugiérales que la impriman y la peguen en la contraportada de su cuaderno de trabajo.

Recuerde el criterio de aceptación asociado: T_rms ≤ 0,8 × T_nominal y T_pico ≤ 0,8 × T_máximo.

### 150. Ficha rápida — Parámetros, funciones y monitores

Advierta una vez más de que la numeración puede variar entre series y variantes. El valor de esta ficha es recordar QUÉ existe; el número exacto se confirma en el manual.

Si los alumnos trabajan habitualmente con un modelo concreto, recomiéndeles hacer su propia versión de esta ficha con los valores verificados de su equipo.

### 151. Ficha rápida — Familias de alarma

Este resumen por familias es más útil en campo que una lista completa de códigos: permite orientar el diagnóstico en segundos y después buscar el código exacto en el manual.

Recuerde la regla: A.9__ son avisos, el resto son alarmas que detienen el eje.

### 152. Lista de verificación imprimible

Sugiera convertir estas dos columnas en un documento A4 a doble cara. Es el entregable del curso con mayor impacto inmediato en el trabajo diario.

Recuerde: una lista de verificación sólo funciona si se rellena en el momento, no de memoria al final del día.

### 153. Glosario

Repase los términos que más confusión generan: baseblock, STO frente a parada de emergencia, y relación de inercias.

Puede usarse como test rápido: tape la columna de la derecha y pida definiciones.

### 154. Autoevaluación (respuestas en la diapositiva siguiente)

Deje tiempo real para responder (10-15 minutos) antes de pasar a las soluciones. Si es posible, que las respondan por escrito y en parejas.

Las preguntas están ordenadas por módulos: 1-3 corresponden a fundamentos y dimensionamiento, 4-5 a sintonización e instalación, 6-8 a diagnóstico, 9 a seguridad y 10 a mantenimiento.

### 155. Autoevaluación — Respuestas comentadas

Comente cada respuesta brevemente, insistiendo en el razonamiento y no en el dato.

Las preguntas 6, 9 y 10 son las que más fallan y, no por casualidad, las que corresponden a los errores más caros en campo.

### 156. Itinerario de aprendizaje y recursos

Cierre insistiendo en el hábito profesional más valioso: consultar el manual. El objetivo del curso no era sustituir al manual, sino enseñar a usarlo con criterio y a saber qué preguntar.

Anime a montar un pequeño banco de pruebas en planta si es posible: un drive y un motor sobre una placa, con SigmaWin+. Es la mejor inversión formativa para un equipo de mantenimiento.

### 157. Un servo no se instala: se dimensiona, se instala,
se parame

Diapositiva de cierre. Recupere la primera diapositiva de objetivos y repase los seis puntos con el grupo, preguntando si se sienten capaces de cada uno.

Deje tiempo para preguntas abiertas y recoja las dudas que no hayan quedado resueltas: suelen indicar qué parte del curso conviene reforzar en la siguiente edición.
