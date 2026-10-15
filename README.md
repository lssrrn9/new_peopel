# Curso STM32 NUCLEO-F303RE

Curso práctico, en español, sobre la tarjeta **NUCLEO-F303RE** y el microcontrolador **STM32F303RET6**. El entorno de trabajo es Visual Studio Code con la extensión oficial STM32CubeIDE for Visual Studio Code 3.x, STM32CubeMX y CMake. El ST-LINK integrado graba y depura.

Esta rama contiene la primera entrega y las fichas de todos los módulos:

1. Fuentes oficiales consultadas y procedimiento de instalación.
2. Índice completo de 28 módulos y 4 proyectos integradores.
3. Matriz de prácticas y materiales, con el mapa de pines que el resto del curso va a respetar.
4. Módulo 1 desarrollado: arquitectura de la tarjeta, diagramas SVG y tres prácticas guiadas.
5. Módulo 2 desarrollado: alimentación, tipos de pin y límites de corriente, con el cálculo del LED.
6. Una ficha de cada módulo del 1 al 28 y de los cuatro proyectos: problema, prácticas, pines y límites.
7. Versión HTML con menú lateral, filtro, imágenes ampliables y bloques de código copiables.

Del módulo 3 en adelante la ficha fija el contenido. El código y el cableado de cada ejemplo se publican con ese módulo.

## Cómo leerlo

- Markdown, junto a las figuras: [`curso/`](curso/).
- HTML de una sola página: abre [`docs/index.html`](docs/index.html) en un navegador.

Los dibujos son SVG generados por [`tools/gen_svg_modulo01.py`](tools/gen_svg_modulo01.py) a partir de UM1724 Rev 17 y del esquema MB1136 C05. No son fotografías ni planos mecánicos a escala. Para regenerar el HTML:

```bash
python3 tools/gen_svg_modulo01.py
python3 tools/build_html.py
```

Hace falta el paquete de Python `markdown`.

## Qué no afirma este repositorio

El texto no dice que un programa se haya compilado, simulado o ejecutado en una placa. Las medidas de la práctica 3 las toma cada estudiante y las anota como suyas. Los límites eléctricos se citan del datasheet; no se han redescubierto en un laboratorio para escribir esta entrega.
