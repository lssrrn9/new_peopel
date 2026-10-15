# Módulo 19. Filtrado digital

Un umbral sobre la muestra cruda dispara una alarma por un pico. Un filtro reparte ese pico con las muestras vecinas. El precio es el retraso: la salida va por detrás de la entrada.

**No comprobado en hardware.**

## Objetivos

- Hacer una media de ocho muestras del potenciómetro.
- Hacer un filtro de primer orden y explicar el coeficiente.
- Imprimir a la vez la señal cruda y la filtrada, y contar el retraso en muestras.

## Prerrequisitos

PA0 con el potenciómetro del [módulo 11](12-modulo-11-adc.md). USART2. El periodo de muestreo fijo: una muestra cada 20 ms, con `HAL_GetTick`, no «cuando el bucle pueda».

## Qué hace un filtro

**Analogía.** La media es preguntar a ocho compañeros y quedarte con el promedio, no con el grito de uno. El filtro recursivo es acordarte del promedio anterior y mezclarlo con la medida nueva. Si te acuerdas demasiado, tardas en aceptar que la mano ha movido el potenciómetro.

**Técnico.** Media móvil de N = 8: `y = (x0 + … + x7) / 8`. El retraso de grupo, para una señal que cambia despacio respecto a la ventana, es del orden de (N − 1) / 2 muestras, aquí 3,5. Se dirá «unas 4 muestras», no un tiempo escondido.

Filtro de primer orden: `y = y + (x − y) / 8`. El coeficiente 1/8 es «la muestra nueva pesa un octavo; el resto es memoria». También se escribe `y = y − y/8 + x/8`. Con enteros, el orden de las restas importa para no quedar en cero. Se usa un acumulado más fino o se acepta el truncado y se dice.

No es un filtro de un instrumento homologado. Es una práctica de programa.

## Ejemplo 1. Media de 8

1. **Problema.** Una cuenta suelta del ADC salta con el ruido del cable.
2. **Objetivo.** Imprimir la media de las últimas 8 muestras.
3. **Material.** Potenciómetro en PA0.
4. **Funcionamiento.** Un array circular guarda 8 lecturas. Cada 20 ms entra una y sale la más vieja. Se imprime la suma dividida por 8.
5. **Dibujo.** [Potenciómetro](img/cable-potenciometro-pa0.svg).
6. **Cableado.** El del módulo 11.
7. **Cálculos.** N = 8 porque cabe en la cabeza y la división es un desplazamiento, y porque 8 * 20 ms = 160 ms de ventana. Un pico de una muestra se diluye a un octavo. No está elegido por una norma de ruido.
8. **CubeMX.** ADC1 IN1 y USART2, como en el módulo 11.
9. **Código.**

```c
/* USER CODE BEGIN PV */
static uint16_t ventana[8];
static uint32_t indice;
static uint32_t suma;
/* USER CODE END PV */
```

```c
/* USER CODE BEGIN 0 */
static uint16_t media_nueva(uint16_t x)
{
  suma -= ventana[indice];
  ventana[indice] = x;
  suma += x;
  indice = (indice + 1U) % 8U;
  return (uint16_t)(suma / 8U);
}
/* USER CODE END 0 */
```

Cada 20 ms lees el ADC, llamas a `media_nueva` e imprimes `cruda` y `media`.

10. **Dónde.** `main.c`.
11. **Compilar y probar.** Quieto: las dos columnas se parecen. Un golpe seco al cursor: la cruda salta y la media se mueve menos, durante varias líneas.
12. **Esperado, no medido.** La media llega al nuevo valor en unas 8 muestras. No hay una captura guardada.
13. **Fallos.** La media se queda en 0: `suma` no arranca bien si el array no está a cero. Al principio, las casillas vacías cuentan como 0 y la media está baja hasta llenar las 8. Dilo en el informe. Desbordamiento: 8 * 4095 cabe en un `uint32_t`. No uses un `uint16_t` para `suma`.
14. **Variación.** N = 4 y N = 16, cambiando el array y el divisor. Con 16, el retraso se nota más.
15. **Criterio.** Puedes señalar cuántas muestras tarda la media en enterarse.

## Ejemplo 2. Filtro de primer orden

1. **Problema.** La media guarda ocho muestras. A veces basta un recuerdo del valor anterior.
2. **Objetivo.** Implementar `y = y + (x − y) / 8` y explicar el 8.
3. **Material.** El mismo potenciómetro.
4. **Funcionamiento.** `y` es la salida anterior. Cada muestra nueva la corrige un octavo del error. Si x se queda fijo, y acaba en x, salvo truncado entero.
5. **Dibujo.** El mismo.
6. **Cableado.** El mismo.
7. **Cálculos.** El 8 es el peso. Un escalón tarda varias muestras en acercarse. Después de una muestra, se ha cubierto 1/8 del escalón. Después de k muestras, queda `(7/8)^k` del escalón. Para bajar del 37 %, k es del orden de 8 muestras. Es una cuenta de diseño, no una medida.
8. **CubeMX.** El mismo.
9. **Código.**

```c
static uint16_t iir(uint16_t x)
{
  static uint32_t y;
  y = y + (((uint32_t)x - y) / 8U);
  return (uint16_t)y;
}
```

Cuidado: si `x` es menor que `y`, la resta de `uint32_t` no debe envolver. Mejor:

```c
if (x > y) { y += (x - y) / 8U; }
else { y -= (y - x) / 8U; }
```

Si la diferencia es menor que 8, el entero no se mueve. Es el truncado. Se acepta en esta práctica y se dice.

10. **Dónde.** `main.c`.
11. **Compilar y probar.** Un escalón con el potenciómetro, del mínimo al máximo, y cuenta líneas hasta que la salida se acerca.
12. **Esperado, no medido.** La salida va detrás y no copia el primer pico entero. El truncado puede dejarla a unas cuentas del final.
13. **Fallos.** No se mueve nunca: siempre divides una diferencia pequeña, o `y` no es `static`. Se pega a 4095: el tipo se desbordó. Revisa que la rama sea la de arriba.
14. **Variación.** Cambia el divisor a 2 y a 32. Con 2 responde antes y filtra menos. Con 32 al revés.
15. **Criterio.** Puedes decir qué pesa más, si la memoria o la muestra nueva.

## Ejemplo 3. Cruda y filtrada, y el retraso

1. **Problema.** Ver el retraso, no solo la curva más bonita.
2. **Objetivo.** Imprimir `n`, `cruda`, `media` y `iir` en cada muestra, y un contador de muestras desde el escalón.
3. **Material.** El mismo.
4. **Funcionamiento.** Cuando la cruda pase de 3000 por primera vez en el ensayo, pones `muestra_escalon` a 0. En cada línea siguiente lo incrementas. Miras en qué número la media ha subido la mitad del escalón, y en cuál el IIR.
5. **Dibujo.** El mismo.
6. **Cableado.** El mismo.
7. **Cálculos.** Media: el retraso hasta incorporar el escalón del todo es 8 muestras, 160 ms a 20 ms. Hasta el 50 % del escalón, unas 4 muestras. IIR con /8: varias muestras, del orden de 8 para acercarse, como en el ejemplo 2. Compara con lo que cuentes. Si no coincide, manda tu conteo: la teoría de este apartado es orientativa.
8. **CubeMX.** Sin cambios. El periodo de 20 ms tiene que ser estable. Usa `HAL_GetTick`, no un bucle vacío.
9. **Código.** Una línea:

```c
snprintf(linea, sizeof(linea), "%lu %u %u %u\r\n",
         (unsigned long)muestra_escalon, cruda, media, filtrada);
```

Solo después de haber visto el escalón. Antes, imprime igual con el contador a 0.

10. **Dónde.** El bucle.
11. **Compilar y probar.** Deja el cursor abajo, empieza a grabar el monitor, súbelo de golpe y para a las dos segundos.
12. **Esperado, no medido.** La columna cruda cambia en una línea. Las otras tardan varias. Anota esas líneas. Son tu medida.
13. **Fallos.** Las tres columnas cambian en la misma línea: estás imprimiendo la cruda tres veces. El periodo no es 20 ms: hay un `Delay` distinto o el `printf` tarda más que 20 ms a 115200. Una línea de 24 caracteres tarda unos 2 ms. Cabe. Si alargas la línea, súbela de periodo.
14. **Variación.** Repite con el filtro /32 y anota que el retraso crece. Ese crecimiento es el criterio de que entendiste el coeficiente.
15. **Criterio.** El informe dice el retraso en muestras, no solo que «se ve más suave».

## Resumen

Ocho muestras de media, un IIR con memoria de 7/8, y las dos salidas al lado de la cruda. El retraso se cuenta.

## Glosario

| Término | Definición |
| --- | --- |
| Media móvil | Promedio de las últimas N muestras |
| IIR | Filtro que usa su propia salida anterior |
| Coeficiente | Cuánto pesa la muestra nueva frente a la memoria |
| Retraso | Cuántas muestras tarda la salida en seguir a la entrada |

## Preguntas

**1.** ¿Un filtro quita la necesidad de mirar el cableado?

Respuesta. No. Un divisor mal puesto no se arregla promediando.

**2.** ¿Por qué N = 8?

Respuesta. Porque la ventana dura 160 ms a 20 ms y la división es sencilla. No es un valor de norma.

**3.** ¿El retraso puede ser cero si el filtro trabaja bien?

Respuesta. No en estos dos. Suavizar un escalón implica tardar más de una muestra.

## Lista de comprobación

- [ ] La media y la cruda salen en la misma línea.
- [ ] He contado muestras de retraso en un escalón.
- [ ] El periodo entre muestras está escrito (20 ms) y no depende de un bucle vacío.

## Siguiente

[Módulo 20](21-modulo-20-pid.md): acercar una medida a una consigna, primero en un modelo.
