# Módulo 12. DAC

El STM32F303RET6 tiene dos salidas de DAC. PA4 es DAC1_OUT1 y está en A2, CN8 pin 3. PA5 es DAC1_OUT2 y también es el LED verde LD2. Este curso usa PA4. No usa PA5 como DAC.

Con el DAC o un operacional en uso, VDDA tiene que estar entre 2,4 V y 3,6 V (datasheet, tabla 19). En la placa lo está: 3,3 V por SB57. **No comprobado en hardware.**

## Objetivos

- Sacar una tensión fija por PA4 y medirla con el polímetro.
- Recorrer una rampa e imprimir el código por USART2.
- Explicar por qué la tercera práctica no usa el comparador en el pin que ya está ocupado.

## Prerrequisitos

Módulos 7 y 11. Polímetro. PA4 libre: si lo tenías como entrada analógica, deja de usarlo como ADC en este proyecto.

## Generar, no leer

**Analogía.** El ADC era la regla que mide. El DAC es una fuente que tú mandas: eliges la marca y el pin se acerca a esa tensión. No es una fuente de potencia. No alimenta un relé ni un LED de potencia.

**Técnico.** El dato de 12 bits se escribe alineado a la derecha. La tensión de salida, que debes confirmar en RM0316, sigue la misma escala que el ADC:

`V = código * VDDA / 4096`

Código 0 acerca la salida a 0 V. Código 4095 se queda un escalón por debajo de VDDA. La corriente que puede salir del pin de DAC no es la de un GPIO de 8 mA: mira la característica eléctrica del DAC en el datasheet antes de colgarle una carga. Para este módulo, la carga es el polímetro, de impedancia alta.

PA4 es TTa. No apliques 5 V en A2 «para probar el fondo de escala».

## Ejemplo 1. Tensión fija

1. **Problema.** Necesitas una referencia lenta, sin potenciómetro.
2. **Objetivo.** Dejar PA4 en un valor estable y leerlo con el polímetro entre PA4 y GND.
3. **Material.** Polímetro. Ningún LED en PA4.
4. **Funcionamiento.** El DAC convierte el código y mantiene la tensión hasta que escribas otro.
5. **Dibujo.** No hay más que la punta del polímetro. CN8 pin 3 (PA4 / A2) y CN6 pin 6 (GND).
6. **Cableado.** Solo esas dos puntas. No pongas un LED directo en PA4.
7. **Cálculos.** Para 1,65 V con VDDA = 3,3 V: código = 1,65 / 3,3 * 4096 = 2048. Ejemplo de diseño.
8. **CubeMX.** DAC1, OUT1 conectado a PA4, sin disparo externo o con disparo por software, el modo que ofrezca tu versión como salida normal. Buffer de salida activado si la opción está, para que el polímetro no cargue el nodo interno. VDDA queda en 3,3 V por la placa. No actives OUT2.
9. **Código.**

```c
/* USER CODE BEGIN 2 */
HAL_DAC_Start(&hdac, DAC_CHANNEL_1);
HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_12B_R, 2048);
/* USER CODE END 2 */
```

El nombre del handle puede ser `hdac` o `hdac1` según la versión de CubeMX. Usa el que haya generado el proyecto.

10. **Dónde.** `USER CODE BEGIN 2`, después de la inicialización.
11. **Compilar y probar.** Graba. Mide entre CN8 pin 3 y GND. No midas en PA5.
12. **Esperado, no medido.** Cerca de 1,65 V. El error del buffer, de VDDA y del polímetro es tuyo. Anótalo. LD2 no es esta salida.
13. **Fallos.** 0 V: canal no arrancado, o el polímetro está en PA5. Cerca de 3,3 V: el código escrito es 4095, o PA4 está como GPIO a 1. El chip no cumple VDDA mínima: no es el caso de esta placa si CN6 pin 4 está a 3,3 V.
14. **Variación.** Escribe 0 y luego 4095. El polímetro debe ir de cerca de 0 V a cerca de 3,3 V.
15. **Criterio.** La tensión leída corresponde al código, y PA5 sigue siendo el LED.

## Ejemplo 2. Rampa

1. **Problema.** Ver que el código y la tensión caminan juntos.
2. **Objetivo.** Recorrer de 0 a 4095 en un tiempo conocido e imprimir el código.
3. **Material.** Polímetro y monitor serie. Opcional: osciloscopio en PA4.
4. **Funcionamiento.** Cada paso suma 64 al código, espera 20 ms y lo escribe. De 0 a 4095 hay 64 pasos de 64 cuentas: 64 * 20 ms = 1,28 s por recorrido. Es un tiempo de diseño para poder seguirlo con el polímetro en modo lento; si el polímetro no sigue, mira el monitor.
5. **Dibujo.** El mismo punto de medida, más el USB para el texto.
6. **Cableado.** PA4 y GND al polímetro. USART2 al PC por el ST-LINK.
7. **Cálculos.** Paso 64 cuentas: 64 * 3,3 / 4096 ≈ 0,052 V. 1,28 s el recorrido completo. No medido.
8. **CubeMX.** DAC1 OUT1 y USART2 a 115200 8N1.
9. **Código.**

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  static uint16_t codigo;
  char linea[32];
  HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_12B_R, codigo);
  int n = snprintf(linea, sizeof(linea), "dac %u\r\n", codigo);
  if (n > 0)
  {
    HAL_UART_Transmit(&huart2, (uint8_t *)linea, (uint16_t)n, 20);
  }
  codigo = (uint16_t)(codigo + 64U);
  if (codigo >= 4096U)
  {
    codigo = 0U;
  }
  HAL_Delay(20);
  /* USER CODE END WHILE */
```

`codigo` cabe en 16 bits. Al sumar 64 desde 4032 se pasa de 4095: el `if` lo devuelve a 0. Ajusta el último tramo si quieres parar en 4095 exacto.

10. **Dónde.** El bucle. El `HAL_DAC_Start` sigue en la zona 2, una sola vez.
11. **Compilar y probar.** Monitor y polímetro a la vez.
12. **Esperado, no medido.** El texto recorre los códigos de 64 en 64 y la tensión del polímetro sube y vuelve a empezar. No hay una captura guardada en el repositorio.
13. **Fallos.** El texto avanza y la tensión no: estás midiendo otro pin. La tensión sube una vez y se queda: el código no vuelve a 0, o el DAC se paró. Texto ilegible: velocidad del monitor.
14. **Variación.** Paso de 1 cuenta y sin `printf`, con 1 ms entre pasos, si tienes osciloscopio y quieres una rampa más seguida. El tiempo de ese recorrido sería unos 4 s.
15. **Criterio.** El código impreso y la tensión van en el mismo sentido.

## Ejemplo 3. Por qué no hay comparador en este mapa

1. **Problema.** El chip tiene comparadores. Usarlos parece el tercer ejemplo natural.
2. **Objetivo.** Decidir si queda un pin libre para la entrada del comparador sin deshacer el mapa del curso.
3. **Material.** Ninguno, si la conclusión es no montarlo.
4. **Funcionamiento.** Un comparador necesita una entrada y una salida o una interrupción. PA4 ya es la salida del DAC. PA0, PA1 y PB0 son las entradas analógicas de los módulos 11, 19 y 20. PA5 es LD2 y el otro canal del DAC, que no usamos. Montar el comparador obligaría a quitar una de esas funciones o a elegir un pin analógico que el módulo siguiente también quiere.
5. **Dibujo.** No se añade.
6. **Cableado.** No se añade.
7. **Cálculos.** No hay.
8. **CubeMX.** No actives el comparador en este proyecto.
9. **Código.** No hay código de comparador. El programa válido de este ejemplo es la rampa del ejemplo 2, que ya enseña a generar la tensión. Documenta en un comentario de USER CODE la razón:

```c
/* USER CODE BEGIN 0 */
/* El comparador no se monta: sus pines de entrada coinciden con PA0, PA1 o PB0,
   reservados a los módulos de medida. PA4 es el DAC. */
/* USER CODE END 0 */
```

10. **Dónde.** Un comentario en `main.c` basta. No es un periférico a medias.
11. **Compilar y probar.** El ejemplo 2 sigue compilando. No hay un tercer cable.
12. **Esperado, no medido.** La rampa continúa. No aparece un pin de comparador en el mapa.
13. **Fallos.** Activar el comparador «para completar» y pisar PA0. No lo hagas en el proyecto que vas a reutilizar.
14. **Variación.** Si más adelante un proyecto no usa PA1, se podrá estudiar el comparador ahí. No en este módulo.
15. **Criterio.** Puedes explicar la omisión sin decir que el chip no tiene comparadores. Sí los tiene: siete, según la tabla 2 del datasheet. No se usan aquí por el mapa de pines.

## Resumen

PA4 genera la tensión. PA5 no. VDDA está en el rango que el DAC exige en esta placa. El comparador se deja fuera para no ocupar las entradas de medida.

## Glosario

| Término | Definición |
| --- | --- |
| DAC | Conversor de código a tensión |
| Buffer de salida | Etapa que permite medir el pin sin cargar el nodo interno |
| VDDA | Alimentación analógica. Aquí, unida a 3,3 V por SB57 |

## Preguntas

**1.** ¿Por qué no se calibra el brillo de LD2 con el DAC de PA5?

Respuesta. Porque este curso reserva PA5 al LED como GPIO, y el canal de DAC que se enseña es PA4.

**2.** ¿El DAC puede mover el relé del módulo 10?

Respuesta. No. No es una salida de potencia.

**3.** ¿El chip no tiene comparadores?

Respuesta. Sí los tiene. Este módulo no los cablea.

## Lista de comprobación

- [ ] He medido PA4, no PA5, con el código 2048.
- [ ] La rampa imprime el código que escribe.
- [ ] No he activado el comparador sobre PA0, PA1 o PB0.

## Siguiente

[Módulo 13](14-modulo-13-i2c.md): dos hilos compartidos, en PB8 y PB9.
