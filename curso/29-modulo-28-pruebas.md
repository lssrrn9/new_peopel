# Módulo 28. Pruebas, documentación y prototipo

El montaje que funciona en tu mesa todavía no es un prototipo que otra persona pueda repetir. Hace falta la lista de pruebas, escrita antes de ejecutarlas, el resultado que el diseño esperaba y el resultado que tú mediste, por separado.

**No comprobado en hardware.** Esta lección no trae medidas. Las columnas «medido» las rellena quien ejecuta.

## Objetivos

- Escribir la lista de pruebas de uno de los proyectos P1 a P4 antes de lanzarlas.
- Ejecutarlas y no mezclar lo esperado con lo medido.
- Redactar qué faltaría para salir del laboratorio.

## Prerrequisitos

Un proyecto elegido entre los cuatro integradores, o el último módulo que hayas montado de verdad. El cuaderno o un archivo en la carpeta del proyecto. No hace falta un pin nuevo.

## Esperado y medido

**Analogía.** El parte de puesta en marcha de un cuadro tiene dos columnas: lo que el esquema dice y lo que el polímetro dice. Si se escribe solo «correcto», nadie puede repetir la prueba. Si se copia el valor del esquema en la columna del polímetro, la prueba no se ha hecho.

**Técnico.** Cada prueba tiene un identificador, el montaje, el estímulo, el resultado esperado por el diseño y el sitio donde se anotará la medida. Lo esperado sale de los cálculos de los módulos, marcados como diseño. Lo medido sale de tu mesa y se marca como medido. Lo que no se llegó a hacer se deja en blanco, no se rellena con el esperado. Este repositorio no afirma que el código se haya compilado ni grabado.

## Ejemplo 1. La lista, antes de ejecutar

1. **Problema.** Probar «a ver qué pasa» no deja un registro.
2. **Objetivo.** Una tabla de al menos ocho pruebas del proyecto elegido, escrita antes de la primera de ellas.
3. **Material.** El proyecto P1, P2, P3 o P4, aunque todavía no lo ejecutes en este ejemplo.
4. **Funcionamiento.** Cada fila se puede fallar. Si no se puede fallar, no es una prueba. «El LED hace cosas» no sirve. «PA5 está a nivel alto cuando el estado es alarma» sí sirve.
5. **Dibujo.** No hay.
6. **Cableado.** El del proyecto elegido, citado con el nombre del SVG, no redibujado de memoria.
7. **Cálculos.** Los umbrales numéricos se copian del proyecto: consigna, RPM, registro Modbus, corriente del LED. Si el proyecto no tiene el número, la prueba no se escribe todavía.
8. **CubeMX.** No se cambia. Se anota la versión de la extensión, del paquete STM32CubeF3 que se haya descargado y el nombre del `.ioc`.
9. **Código.** No se añade lógica. Se añade un archivo `PRUEBAS.md` en la carpeta del proyecto, fuera de `Core` si no quieres que nadie lo confunda con un fuente. Plantilla:

```markdown
| Id | Estímulo | Esperado por diseño | Medido | Fecha |
| --- | --- | --- | --- | --- |
| T1 | | | | |
```

Ocho filas vacías en «Medido».

10. **Dónde.** Junto al proyecto, no dentro de una zona que CubeMX borre.
11. **Compilar y probar.** No se graba nada en este ejemplo. Se revisa que cada fila tenga un esperado comprobable.
12. **Esperado, no medido.** La tabla existe y la columna medido está vacía. Ese vacío es el criterio de que no has copiado el diseño.
13. **Fallos.** Filas que dicen «funciona». Umbrales que no están en el código. Pruebas de 230 V o de agua junto a la placa: no pertenecen a este curso.
14. **Variación.** Añade una fila que deba fallar a propósito, como el registro Modbus 1001 rechazado, si ese es tu proyecto.
15. **Criterio.** Otra persona puede ejecutar la tabla sin preguntarte qué querías decir.

## Ejemplo 2. Ejecutar y separar columnas

1. **Problema.** Rellenar la tabla sin maquillarla.
2. **Objetivo.** Ejecutar las filas y escribir en «Medido» solo lo que hayas observado. Donde no haya instrumento, escribir «no medido».
3. **Material.** El montaje real del proyecto, el polímetro y el monitor serie.
4. **Funcionamiento.** Una fila, una acción, una anotación. Si el resultado no coincide con el esperado, la fila se queda en fallo y se anota la diferencia. No se edita el esperado para que coincida.
5. **Dibujo.** El del proyecto.
6. **Cableado.** El de la tabla de cableado del proyecto, comprobado pin a pin antes de la primera prueba de señal.
7. **Cálculos.** No se rehacen durante la prueba, salvo para explicar un fallo después.
8. **CubeMX.** El del proyecto. Anota si regeneraste a mitad del ensayo: esa regeneración puede cambiar el resultado.
9. **Código.** El del proyecto. Si corriges un fallo, la fila se repite con un id nuevo (`T3b`), no se borra la fila fallida.
10. **Dónde.** El mismo `PRUEBAS.md`.
11. **Compilar y probar.** Graba y recorre la tabla. Esto sí es una ejecución tuya. Este texto sigue sin decir que se haya hecho.
12. **Esperado, no medido.** La columna medido deja de estar vacía en las filas que hiciste, y sigue vacía o dice «no medido» en las que no.
13. **Fallos.** Copiar 3,30 V porque «el regulador es de 3,3 V» sin poner la punta. Borrar un fallo. Medir 24 V en el GPIO y seguir: eso es un fallo de cableado, se corta y se anota.
14. **Variación.** Pide a otra persona que ejecute una fila leyendo solo el archivo. Si necesita llamarte, la fila no estaba escrita.
15. **Criterio.** Se distingue, en cada fila, el diseño de la medida.

## Ejemplo 3. Qué falta para salir del laboratorio

1. **Problema.** Un prototipo de mesa se parece poco a un equipo que se deja funcionando.
2. **Objetivo.** Una lista de ausencias, honesta, al final de `PRUEBAS.md`.
3. **Material.** Ninguno nuevo.
4. **Funcionamiento.** Recorre esta lista y marca qué tienes y qué no. No se compra nada en este ejemplo. Se escribe.

- Alimentación distinta del USB del PC, con el límite de corriente que ya calculaste.
- Conector distinto de los cables de protoboard.
- Aislamiento, si el módulo 27 dijo que las tierras no se podían unir y aún no hay aislador.
- Watchdog probado con la fila correspondiente, no solo activado en CubeMX.
- Versión del firmware identificable: un texto al arrancar con un número que tú cambias cuando cambias el programa.
- Lo que este curso no cubre y el equipo necesitaría: marcado, ensayo de aislamiento, bornero, temperatura ambiente, un lazo de verdad.

5. **Dibujo.** No hay.
6. **Cableado.** No se añade.
7. **Cálculos.** No hay.
8. **CubeMX.** Anota la versión. No hace falta cambiarla.
9. **Código.** Si aún no hay un texto de versión, añádelo una vez en `USER CODE BEGIN 2`:

```c
static const uint8_t version[] = "firmware 0.1\r\n";
HAL_UART_Transmit(&huart2, (uint8_t *)version, sizeof(version) - 1U, 100);
```

Ese 0.1 es una etiqueta tuya. Súbela cuando cambies el comportamiento. No demuestra una validación.

10. **Dónde.** `PRUEBAS.md` y, si añades la línea, `main.c`.
11. **Compilar y probar.** La línea de versión aparece al pulsar reset. El archivo de pruebas tiene la lista de ausencias.
12. **Esperado, no medido.** Quien lea el archivo sabe qué no está demostrado. No hay una frase que diga que el prototipo está listo para una máquina.
13. **Fallos.** Escribir «listo para producción» porque las ocho filas de mesa pasaron. Esas filas no cubren la lista de ausencias.
14. **Variación.** Separa «lo cerraré en el laboratorio» de «esto ya no es una práctica de este curso».
15. **Criterio.** La última página no promete un equipo de cuadro.

## Resumen

La tabla se escribe antes, se mide después y no se maquilla. La versión se imprime al arrancar. Lo que falta para salir del laboratorio se enumera, incluido lo que este curso no pretende cubrir.

## Glosario

| Término | Definición |
| --- | --- |
| Esperado | Lo que el diseño calcula o especifica |
| Medido | Lo que el instrumento o el monitor mostraron en tu mesa |
| No medido | La prueba que no se hizo. No se rellena con el esperado |
| Versión | La etiqueta que tú cambias cuando cambia el programa |

## Preguntas

**1.** ¿Una fila «correcto» vale?

Respuesta. No. Tiene que decir qué número o qué nivel se esperaba y cuál se vio.

**2.** ¿Puedo borrar la fila que falló si ya la corregí?

Respuesta. No. Se añade otra con el resultado nuevo. La fallida explica por qué cambiaste el programa.

**3.** ¿Ocho pruebas de mesa convierten el montaje en un producto?

Respuesta. No. La lista de ausencias del ejemplo 3 sigue siendo cierta.

## Lista de comprobación

- [ ] `PRUEBAS.md` existe y se escribió antes de ejecutar.
- [ ] La columna medido no copia el esperado en las filas que no hice.
- [ ] Hay un texto de versión al arrancar, o he anotado que aún no.
- [ ] La última sección dice qué falta, sin llamar a esto un equipo terminado.

## Siguiente

Los cuatro proyectos integradores usan estos módulos. Empieza por el que tus materiales permitan: [P1 temperatura](30-proyecto-01-temperatura.md), [P2 tanque](31-proyecto-02-tanque.md), [P3 motor](32-proyecto-03-motor.md) o [P4 nodo Modbus](33-proyecto-04-nodo-modbus.md).
