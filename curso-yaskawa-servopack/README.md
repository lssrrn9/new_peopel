# Curso «Servo drives YASKAWA SERVOPACK» — de cero a experto (3 kW)

Curso técnico completo en PowerPoint sobre el trabajo con un servoaccionamiento
YASKAWA **SERVOPACK** de la serie **Σ-X (Sigma-X)** aplicado a un **servomotor
de 3 kW**. El conjunto de referencia empleado a lo largo del material es
**SGDXS-200A00A-Y3600A + SGMXA-30A**, alimentado a 200 V CA trifásicos
(interfaz analógica / tren de pulsos).

La presentación no está escrita a mano: se **genera con un script**, de forma
que el contenido es editable, revisable en control de versiones y reproducible.

## Qué contiene

| Artefacto | Ruta |
|---|---|
| Presentación PowerPoint (157 diapositivas, 16:9) | `salida/CURSO_YASKAWA_SERVOPACK_3kW.pptx` |
| Documento PDF | `salida/CURSO_YASKAWA_SERVOPACK_3kW.pdf` |
| Guion del instructor en texto (notas de todas las láminas) | `salida/GUIA_DEL_INSTRUCTOR.md` |

Cada diapositiva lleva **notas del orador** con el guion de clase, ejemplos,
advertencias de seguridad y los errores típicos de campo. Esas notas son
también el material de estudio y se exportan automáticamente al Markdown de la
guía.

## Programa

| Módulo | Contenido | Duración orientativa |
|---|---|---|
| Introducción | Objetivos, mapa del curso, convenciones y seguridad | — |
| 01 | Fundamentos del servoaccionamiento: lazo en cascada, encoder, par e inercia | 3 h |
| 02 | La familia SERVOPACK Σ-X: líneas, arquitectura interna, código de modelo | 3 h |
| 03 | El servomotor de 3 kW: familias, curvas, encoder absoluto, freno | 3 h |
| 04 | Dimensionamiento y selección, con ejemplo numérico completo | 4 h |
| 05 | Instalación mecánica y eléctrica: potencia, EMC, regeneración, freno | 4 h |
| 06 | Interfaz de control: `CN1`, analógico, tren de pulsos, MECHATROLINK y EtherCAT | 4 h |
| 07 | Parámetros `Pn`/`Fn`/`Un`, panel, SigmaWin+ Ver.7 (con capturas) y engranaje electrónico | 5 h |
| 08 | Puesta en marcha en seis fases | 5 h |
| 09 | Sintonización: autoajuste, ajuste manual, filtros notch, vibración | 6 h |
| 10 | Seguridad funcional: STO / HWBB, `CN8` y EDM | 2,5 h |
| 11 | Diagnóstico, alarmas y mantenimiento preventivo | 4 h |
| 12 | Proyecto integrador con rúbrica de evaluación | 8 h |
| 13 | Anexos: fichas rápidas, listas de verificación, glosario y autoevaluación | 2 h |

## Regenerar la presentación

```bash
pip install -r requirements.txt
python3 generar_presentacion.py
```

Opciones:

```bash
python3 generar_presentacion.py --salida /ruta/mi_curso.pptx   # otra ruta de salida
python3 generar_presentacion.py --sin-guia                     # no generar el Markdown
```

## Cómo está organizado el código

```
builder.py                  Identidad visual y plantillas de diapositiva
generar_presentacion.py     Punto de entrada; encadena los módulos y exporta la guía
contenido/
  m00_apertura.py           Portada, objetivos, mapa y seguridad
  m01_fundamentos.py        … un fichero por módulo del curso …
  m13_anexos.py             Anexos, autoevaluación y cierre
salida/                     Artefactos generados
```

`builder.py` expone plantillas de alto nivel (`bullets_slide`, `two_col_slide`,
`cards_slide`, `steps_slide`, `table_slide`, `canvas_slide`…) para que los
módulos de contenido sólo aporten texto. El tamaño de letra de las viñetas y de
los procedimientos se **ajusta automáticamente** a la caja disponible, de modo
que añadir contenido no rompe la maquetación.

En el texto se admite marcado en línea: `**negrita**` y `` `monoespaciado` ``
(este último se usa para parámetros, señales y códigos de alarma).

### Añadir o modificar contenido

Editar el fichero del módulo correspondiente en `contenido/` y volver a
ejecutar el generador. Por ejemplo, para añadir una diapositiva de viñetas:

```python
d.bullets_slide(
    "Título de la lámina",
    [
        "Idea principal con **algo destacado** y un parámetro `Pn100`.",
        "- Detalle de segundo nivel.",
        "#Encabezado interno",
        "Otra idea principal.",
    ],
    subtitle="Subtítulo opcional",
    notes="Guion del instructor para esta lámina.",
    callout=("amber", "Título del aviso", "Texto del aviso."),
)
```

### Previsualizar sin PowerPoint

Con LibreOffice instalado:

```bash
soffice --headless --convert-to pdf --outdir /tmp salida/CURSO_YASKAWA_SERVOPACK_3kW.pptx
```

## Aviso sobre los datos técnicos

Los valores de catálogo, códigos de parámetro, asignaciones de terminales y
códigos de alarma que aparecen en el curso son **de referencia didáctica**.
Antes de aplicarlos a un equipo real hay que contrastarlos con el manual
oficial del SERVOPACK correspondiente (serie, variante de interfaz y revisión
de firmware) y con la placa de características del equipo instalado. El
material está pensado para enseñar **qué** hay que comprobar y **dónde**
buscarlo, no para sustituir a la documentación del fabricante.

YASKAWA, SERVOPACK, Σ-X/Sigma-X, Σ-7/Sigma-7 y SigmaWin+ son marcas de sus
respectivos titulares. Este material es formativo e independiente. Los
esquemas extraídos del manual **SIEP C710812 03I** se citan como referencia
técnica; no sustituyen al manual oficial.

## Ver el curso sin descargar nada

**[VER_EL_CURSO.md](VER_EL_CURSO.md)** muestra las 157 diapositivas como
imágenes, con índice por módulos. Se lee directamente en el navegador, sin
PowerPoint. Las imágenes están en `diapositivas/` y el curso completo en PDF,
en `salida/CURSO_YASKAWA_SERVOPACK_3kW.pdf`.

Para regenerar la galería tras editar el contenido:

```bash
python3 generar_presentacion.py
soffice --headless --convert-to pdf --outdir salida salida/CURSO_YASKAWA_SERVOPACK_3kW.pptx
pdftoppm -r 96 -png salida/CURSO_YASKAWA_SERVOPACK_3kW.pdf diapositivas/d
python3 generar_galeria.py
```
