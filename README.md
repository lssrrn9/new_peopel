# Curso STM32 NUCLEO-F303RE

Curso práctico, en español, sobre la tarjeta **NUCLEO-F303RE** y el microcontrolador **STM32F303RET6**. El entorno de trabajo es Visual Studio Code con la extensión oficial STM32CubeIDE for Visual Studio Code 3.x, STM32CubeMX y CMake. El ST-LINK integrado graba y depura.

Esta rama contiene el curso completo:

1. Fuentes oficiales consultadas y procedimiento de instalación.
2. Índice de 28 módulos y 4 proyectos, con el mapa de pines.
3. Matriz de prácticas y materiales.
4. Módulos 1 a 28 escritos: analogía, explicación técnica, y al menos tres ejemplos con cableado, CubeMX y código.
5. Proyectos P1 a P4 escritos, reutilizando ese mapa de pines.
6. Una ficha de cada módulo, enlazada a su lección.
7. Versión HTML con menú lateral, filtro, imágenes ampliables y bloques de código copiables.

El código de los ejemplos no se ha compilado ni se ha grabado en una placa al escribir el curso. Cada lección lo dice.

## Cómo leerlo

- Markdown, junto a las figuras: [`curso/`](curso/).
- HTML de una sola página: abre [`docs/index.html`](docs/index.html) en un navegador.

Los dibujos son SVG generados por [`tools/gen_svg_modulo01.py`](tools/gen_svg_modulo01.py) a partir de UM1724 Rev 17 y del esquema MB1136 C05. No son fotografías ni planos mecánicos a escala. Para regenerar el HTML:

```bash
python3 tools/gen_svg_modulo01.py
python3 tools/gen_svg_practicas.py
python3 tools/build_html.py
```

Hace falta el paquete de Python `markdown`.

## Qué no afirma este repositorio

El texto no dice que un programa se haya compilado, simulado o ejecutado en una placa. Las medidas de la práctica 3 las toma cada estudiante y las anota como suyas. Los límites eléctricos se citan del datasheet; no se han redescubierto en un laboratorio para escribir esta entrega.
