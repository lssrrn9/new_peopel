# Módulo 24. Memoria no volátil

Quitar el USB borra la RAM. Este chip no trae una EEPROM aparte descrita como tal en el datasheet: el sitio para guardar un umbral es la Flash de programa. Hay que escribir poco, en un sitio que no sea el programa, y asumir que un corte a mitad de la escritura puede dejar esa copia a medias.

**No comprobado en hardware.** El tamaño de página no se copia de memoria en esta lección. Se usa el símbolo `FLASH_PAGE_SIZE` de la cabecera CMSIS que CubeMX haya puesto en el proyecto. Si ese símbolo no existe, ábrelo en el paquete y usa el que la cabecera defina. No escribas 2048 a mano.

## Objetivos

- Guardar un número, quitar alimentación y volver a leerlo.
- Guardar solo cuando se pide por el puerto serie, no en cada vuelta.
- Arrancar con la última copia íntegra, o con el valor de fábrica, si la escritura quedó a medias.

## Prerrequisitos

USART2. El mapa de memoria del STM32F303RET6: 512 KB de Flash desde `0x08000000` (datasheet, tabla 2 y línea de pedido E). La última página es la que se usa para no pisar el programa, siempre que el programa no haya crecido hasta el final. Comprueba el tamaño del `.elf` antes de elegir la dirección. Si el binario ocupa hasta el final, no hay sitio: hay que reservar la página en el enlazado, y esta lección te avisa de ese caso en vez de inventar un linker script completo.

## Escribir Flash no es escribir RAM

**Analogía.** La RAM es un encerado. La Flash es un cuaderno que solo se puede borrar por hojas enteras. Borrar la hoja donde está el programa la deja en blanco. Por eso se usa la última hoja, y no se escribe en cada paso del bucle: cada escritura gasta la hoja y, si se va la luz a mitad, la hoja puede quedar ilegible.

**Técnico.** En esta familia el HAL programa medias palabras. El procedimiento de referencia es el capítulo de Flash de RM0316: desbloquear, borrar la página, programar, bloquear. El código de abajo usa el HAL. Si tu versión nombra los campos de `FLASH_EraseInitTypeDef` de otra forma, manda la estructura generada en tu proyecto.

Dirección prevista:

```c
#define PARAM_ADDR (FLASH_BASE + (512U * 1024U) - FLASH_PAGE_SIZE)
```

512 KB está verificado para el STM32F303RET6. `FLASH_PAGE_SIZE` no se sustituye por un número en este texto.

Se guardan dos copias dentro de la página si cabe, o una marca de validez de 16 bits `0xA55A` seguida del valor. Si la marca no está, el valor es el de fábrica, 500. Un corte durante el borrado deja la marca ausente: se vuelve a fábrica. Eso es el criterio de esta práctica, y se escribe antes de probarlo. No es una EEPROM con nivelación de desgaste. No escribas en cada tecla.

## Ejemplo 1. Guardar y quitar el USB

1. **Problema.** Un umbral en RAM no sobrevive al apagado.
2. **Objetivo.** Escribir 500, quitar el cable, volver y leer 500.
3. **Material.** La placa y el monitor.
4. **Funcionamiento.** Al arrancar se lee la media palabra de la marca y la siguiente del valor. Si la marca no es `0xA55A`, se ofrece el valor de fábrica y, la primera vez, se graba. En los arranques siguientes no se graba si la marca está.
5. **Dibujo.** No hay.
6. **Cableado.** No hay.
7. **Cálculos.** Valor de fábrica 500. Marca `0xA55A`. Dirección `PARAM_ADDR`.
8. **CubeMX.** USART2. Nada de DMA sobre la Flash. No actives una protección de lectura que luego te impida borrar: déjala como viene el proyecto de prácticas.
9. **Código.**

```c
/* USER CODE BEGIN 0 */
#define MARCA_OK 0xA55AU

static uint16_t flash_leer(void)
{
  uint16_t marca = *(__IO uint16_t *)PARAM_ADDR;
  uint16_t valor = *(__IO uint16_t *)(PARAM_ADDR + 2U);
  if (marca != MARCA_OK)
  {
    return 500U;
  }
  return valor;
}

static int flash_guardar(uint16_t valor)
{
  FLASH_EraseInitTypeDef borrar = {0};
  uint32_t error = 0U;
  if (HAL_FLASH_Unlock() != HAL_OK)
  {
    return -1;
  }
  borrar.TypeErase = FLASH_TYPEERASE_PAGES;
  borrar.PageAddress = PARAM_ADDR;
  borrar.NbPages = 1;
  if (HAL_FLASHEx_Erase(&borrar, &error) != HAL_OK)
  {
    HAL_FLASH_Lock();
    return -1;
  }
  if (HAL_FLASH_Program(FLASH_TYPEPROGRAM_HALFWORD, PARAM_ADDR, MARCA_OK) != HAL_OK)
  {
    HAL_FLASH_Lock();
    return -1;
  }
  if (HAL_FLASH_Program(FLASH_TYPEPROGRAM_HALFWORD, PARAM_ADDR + 2U, valor) != HAL_OK)
  {
    HAL_FLASH_Lock();
    return -1;
  }
  HAL_FLASH_Lock();
  return 0;
}
/* USER CODE END 0 */
```

En la zona 2, lee e imprime. Si la marca no está, llama a `flash_guardar(500)` una vez.

Los campos `PageAddress` y `NbPages` son los del HAL F3 habitual. Si tu estructura trae `Banks` o `Page` en otro sentido, adapta el campo y no este párrafo.

10. **Dónde.** `main.c`. El `#define` de `PARAM_ADDR` puede ir en el mismo USER CODE.
11. **Compilar y probar.** Primera grabación: debe imprimir 500 y haber escrito. Quita el USB cinco segundos. Vuelve a abrir el monitor. Debe imprimir 500 sin depender de que el programa vuelva a inventarlo en RAM: desconecta de verdad.
12. **Esperado, no medido.** El valor se mantiene. Si el programa no arranca, la dirección pisó el código. Recupera la placa borrando toda la Flash desde el depurador y elige otra página, o reduce el programa. No des ese fallo por un misterio del USB.
13. **Fallos.** Siempre 500 recién calculado y la marca nunca cuadra: la escritura falla y no miras el `-1`. Imprímelo. Valor que cambia solo: estás escribiendo en cada bucle. El ejemplo 2 lo prohíbe. Dirección impar: la media palabra tiene que estar alineada. `PARAM_ADDR` lo está si la página lo está.
14. **Variación.** Guarda 501 a mano en una llamada, apaga y confirma 501. Luego vuelve a 500.
15. **Criterio.** El número sobrevive a quitar el cable, y sabes en qué dirección está.

## Ejemplo 2. Guardar solo cuando se pide

1. **Problema.** Escribir en cada vuelta gasta la Flash y no aporta.
2. **Objetivo.** La letra `g` guarda la consigna actual. Cualquier otro texto no la guarda. La consigna en RAM puede cambiar con `+` y `-` sin tocar la Flash.
3. **Material.** El monitor.
4. **Funcionamiento.** `+` suma 10 en RAM, hasta 1000. `-` resta 10, sin bajar de 0. `g` llama a `flash_guardar`. Al arrancar, RAM copia la Flash.
5. **Dibujo.** No hay.
6. **Cableado.** USART2.
7. **Cálculos.** Tope 0 a 1000, de acuerdo con el rechazo del módulo 21. Paso 10.
8. **CubeMX.** El mismo.
9. **Código.** En el bucle, lee un byte. Si es `+` o `-`, modifica una variable `consigna` e imprime `ram`. Si es `g`, guarda e imprime `flash`. No llames a `flash_guardar` en otro sitio.
10. **Dónde.** El bucle.
11. **Compilar y probar.** Sube la consigna con varios `+`. Quita el USB sin pulsar `g`. Al volver, tiene que estar el valor antiguo. Repite, pulsa `g`, quita el USB. Al volver, está el nuevo.
12. **Esperado, no medido.** Ese par de ensayos. La Flash no cambia en los `+`.
13. **Fallos.** Cambia sin `g`: hay una llamada de más. No cambia con `g`: miras el valor de RAM al arrancar y no el de `flash_leer`. Imprime los dos.
14. **Variación.** `p` imprime marca y valor en hexadecimal, leídos otra vez de la dirección, para no fiarte de la variable.
15. **Criterio.** Puedes decir cuántas veces se borró la página en el ensayo: una por cada `g`, no una por cada `+`.

## Ejemplo 3. Corte a mitad

1. **Problema.** Si se va la alimentación mientras se borra, la marca puede desaparecer.
2. **Objetivo.** Definir el criterio y provocarlo: o queda el valor anterior íntegro, o se vuelve a 500. No se acepta un valor «a medias» sin marca.
3. **Material.** El cable USB, que vas a quitar en el momento de la escritura.
4. **Funcionamiento.** El criterio, escrito antes de la prueba: si la marca no es `0xA55A`, el valor de trabajo es 500. Un corte durante el borrado cae en ese caso. Un corte antes de empezar deja la copia anterior, porque no se ha borrado. No hay una tercera copia en este módulo. El ensayo es quitar el USB justo después de pedir `g`, varias veces, hasta observar uno de los dos resultados. No se garantiza cuál de los dos verás en un intento concreto.
5. **Dibujo.** No hay.
6. **Cableado.** No hay.
7. **Cálculos.** No hay un instante exacto. Por eso se repite el ensayo.
8. **CubeMX.** Sin cambios.
9. **Código.** El de los ejemplos 1 y 2 ya cumple el criterio si `flash_leer` rechaza una marca mala. Añade un retardo de 50 ms entre el borrado y la programación, solo en este ensayo, para tener más probabilidad de cortar en medio. Quítalo al acabar: no forma parte del producto.

```c
HAL_Delay(50); /* solo el ensayo del corte; quitar después */
```

10. **Dónde.** Dentro de `flash_guardar`, entre el erase y el program, y luego fuera.
11. **Compilar y probar.** Anota el valor, pulsa `g` y quita el USB enseguida. Restaura. Apunta si volvió el valor previo, el nuevo o 500.
12. **Esperado, no medido.** Uno de esos tres, y nunca un número con la marca mal leída tratada como válida. 500 es el resultado aceptable del corte durante el borrado. El valor previo es el resultado aceptable si no llegó a borrar.
13. **Fallos.** Un valor distinto de los tres: la marca coincidió por casualidad con basura. Amplía la comprobación con una segunda marca al final del registro y exige las dos. Si no quieres ampliarla, repite el ensayo y no des por bueno un valor fuera de rango: `flash_leer` puede rechazar también valores mayores que 1000.
14. **Variación.** Quita el `HAL_Delay` del ensayo y deja el módulo listo para el proyecto.
15. **Criterio.** El informe dice qué hiciste al cortar y qué valor salió, y el `Delay` de ensayo ya no está.

## Resumen

La última página, el símbolo de tamaño de página de la cabecera, una marca de validez y escritura solo bajo demanda. Un corte vuelve a fábrica o deja la copia que aún no se borró.

## Glosario

| Término | Definición |
| --- | --- |
| Flash | Memoria que conserva el dato sin alimentación y se borra por páginas |
| Página | El bloque mínimo que el borrado limpia |
| Marca | Un valor conocido que dice que lo que sigue es válido |
| Valor de fábrica | El que se usa cuando la marca no está. Aquí, 500 |

## Preguntas

**1.** ¿Por qué no 2 KB escritos a mano?

Respuesta. Porque esta lección no da por verificado el tamaño de página. Lo dice la cabecera del paquete que generaste.

**2.** ¿Puedo guardar en cada muestra del ADC?

Respuesta. No. La Flash no es un registro continuo, y un corte te dejaría sin la última copia buena.

**3.** ¿Dónde miro el procedimiento si el HAL no coincide?

Respuesta. En el capítulo de Flash de RM0316 y en la estructura que tenga tu proyecto, no en un ejemplo de otra familia.

## Lista de comprobación

- [ ] El valor sobrevive a quitar el USB después de `g`.
- [ ] Los `+` no escriben en la Flash.
- [ ] He anotado el resultado de al menos un corte durante `g`.
- [ ] He quitado el retardo que solo servía para ese corte.
- [ ] La dirección usa `FLASH_PAGE_SIZE`.

## Siguiente

[Módulo 25](26-modulo-25-bajo-consumo.md): medir la corriente y bajarla cuando no hay nada que hacer.
