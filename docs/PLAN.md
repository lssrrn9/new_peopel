# Casa con ESP32 — plan por etapas

Este documento fija el alcance, la arquitectura y los pasos de cada etapa.
No se escribe firmware, no se abre Wokwi y no se toca el servidor hasta cerrar
la etapa anterior con su criterio de salida.

## Alcance de esta versión

- Encender y apagar luces desde el celular.
- Aviso en el celular cuando un sensor de movimiento detecta presencia, solo
  dentro de una franja horaria configurable.
- La misma lógica se prueba primero en Wokwi y después en hardware real.
- El transporte entre la casa, el servidor y el celular es MQTT.
- El broker vive en un VPS de Hetzner.

Fuera de esta versión: cámaras, voz, persianas, medición de consumo, OTA y
más de un nodo físico. El diseño deja sitio para clonar nodos, pero el piloto
es un solo nodo: una luz y un sensor de movimiento.

## Decisiones ya cerradas para no replanificar

| Tema | Decisión |
| --- | --- |
| Piloto | 1 ESP32, 1 luz, 1 PIR, 1 botón local |
| Simulación | Wokwi con el mismo contrato MQTT que el hardware |
| Broker | Mosquitto en Docker, solo TLS en el puerto 8883, usuario y ACL por dispositivo |
| Horario de avisos | Lo evalúa un servicio en el VPS, no el ESP32 |
| Arranque del relé | Apagado. Un comando viejo no enciende la luz al volver la energía |
| Si se cae internet | La luz se queda como está. El botón local sigue funcionando |
| Celular | Panel web con login (sirve en Android e iPhone) y avisos con ntfy en el mismo VPS |
| Secretos | WiFi, claves MQTT y tokens no se suben al repositorio |

Home Assistant queda como alternativa posterior. No entra en el piloto: añade
otro producto antes de tener el contrato de mensajes y el hardware estables.

## Arquitectura

```
Celular
  |  HTTPS :443  (panel: encender / apagar, ver estado)
  |  app ntfy    (aviso de movimiento)
  v
VPS Hetzner
  Caddy  ->  panel web (login)
  ntfy   ->  avisos
  reglas ->  suscrito a movimiento; avisa solo dentro de la franja
  Mosquitto :8883 TLS
        ^  publica estado, disponibilidad y movimiento
        |  se suscribe solo a su comando de luz
        |
ESP32 en casa (WiFi)
  botón local ----+
  PIR ------------+--> lógica local --> relé (luz) + MQTT
```

El celular no habla MQTT directo con el ESP32. Habla HTTPS con el VPS.
El VPS publica el comando en el broker. Así el broker no queda abierto a
cualquier cliente del teléfono y las claves de los dispositivos no viven en
el celular.

Cada nodo futuro repite el mismo bloque (ESP32 + relé + PIR + botón). Si un
nodo falla, los demás siguen. No hay un solo ESP32 para toda la casa.

## Contrato MQTT

Se congela antes de escribir código. Simulación, firmware y panel usan estos
mismos temas.

| Tema | Quién publica | Retenido | Carga |
| --- | --- | --- | --- |
| `casa/piloto/luz/set` | solo el panel, vía broker | no | `ON` o `OFF` |
| `casa/piloto/luz/state` | solo el ESP32 | sí | `ON` o `OFF` |
| `casa/piloto/motion` | solo el ESP32 | no | `ON` en flanco de subida |
| `casa/piloto/availability` | ESP32 y LWT del broker | sí | `online` / `offline` |

Reglas:

- El comando `set` no se retiene. Si se retuviera, un `ON` guardado
  encendería la luz al reconectar.
- El estado `state` sí se retiene, para que el panel muestre la última luz
  conocida.
- El movimiento solo se publica al pasar de reposo a detección. No se republica
  mientras la persona sigue delante del sensor.
- El ESP32 tiene cooldown (60 s) entre eventos de movimiento.
- El servicio de reglas tiene otro cooldown (60 s) antes de repetir el aviso.
- ACL: el usuario del nodo solo puede publicar `state`, `motion` y
  `availability`, y solo puede suscribirse a `luz/set`.
- El panel usa otro usuario, que solo publica `luz/set` y solo lee estado,
  movimiento y disponibilidad.

La franja horaria no viaja al ESP32 en el piloto. Vive en el servicio de
reglas (`AVISO_DESDE`, `AVISO_HASTA`, zona horaria). Así se cambia el horario
sin regrabar la placa.

## Hardware del nodo piloto

Lado de baja tensión (lo que documenta y prueba este proyecto):

- ESP32 DevKit como controlador. WiFi, watchdog y pin de relé en estado
  seguro antes de activar la salida.
- Módulo de relé con optoacoplador. La bobina la alimenta la fuente de 5 V,
  no un pin del ESP32. El GPIO solo entra a la entrada lógica del módulo.
- PIR HC-SR501 o AM312 a 5 V. Salida al GPIO con antirrebote por software.
- Botón a GND con pull-up interno. Alterna la luz en local y publica `state`.
- LED de estado de la luz (en Wokwi representa la lámpara).
- Fuente de 5 V estable, común para ESP32, relé y PIR. Masa común en el lado
  de baja tensión.

Lado de red eléctrica (no se cablea en este repositorio):

- El contacto del relé conmuta la lámpara. Esa conexión la hace alguien
  habilitado para trabajar con la instalación de la casa.
- Relé dimensionado por encima de la carga, fusible en el circuito, módulo
  dentro de caja aislante, y el interruptor de pared existente se mantiene
  como corte local.
- Al arrancar, al resetear y si el firmware no llega a conectar, el relé
  queda abierto (luz apagada).

Comportamiento local obligatorio:

1. Al encender la placa, la luz queda apagada y se publica `state=OFF`.
2. El botón cambia la luz aunque el WiFi o el broker estén caídos.
3. Un comando MQTT `ON`/`OFF` hace lo mismo que el botón y publica el estado
   real, no el estado deseado.
4. Si el broker corta, el testamento LWT pasa `availability` a `offline`.
5. Al reconectar, el nodo no aplica comandos atrasados.

## Etapas

Cada etapa tiene pasos, entregables y un criterio de salida. La siguiente no
empieza hasta cumplir ese criterio.

### Etapa 0 — Plan (esta etapa)

Pasos:

1. Fijar alcance del piloto (una luz, un PIR, un botón).
2. Fijar arquitectura: celular → HTTPS → VPS → MQTT → ESP32.
3. Congelar temas, retención, ACL y arranque en apagado.
4. Definir el hardware de baja tensión y el límite del trabajo en red eléctrica.
5. Dejar escritas las etapas 1 a 6 con su criterio de salida.

Entregable: este documento.

Criterio de salida: el plan está en el repositorio y no hay firmware,
diagrama de Wokwi ni configuración del VPS todavía.

### Etapa 1 — Simulación en Wokwi, sin servidor

Objetivo: probar la lógica del nodo sin Hetzner y sin placa real.

Pasos:

1. Crear el proyecto Wokwi: ESP32, relé, PIR, botón y LED de lámpara.
2. Firmware en modo local (sin red):
   - arranque con relé apagado;
   - botón alterna la luz;
   - PIR emite un solo evento por detección y respeta 60 s de cooldown.
3. Añadir un reloj simulado (hora inyectada por monitor serie) y una franja
   de prueba, solo para ver en el monitor si ese evento *habría* generado
   aviso. El aviso real lo hará el VPS en la etapa 4; aquí solo se observa
   la decisión.
4. Escribir una lista de pruebas y ejecutarla en el simulador:
   - al iniciar, la luz está apagada;
   - cada pulsación cambia la luz;
   - el PIR no repite el evento si se queda activo;
   - el PIR no emite otro evento antes de 60 s;
   - dentro de la franja, el monitor marca aviso pendiente;
   - fuera de la franja, el monitor marca evento ignorado para aviso.

Entregables: `firmware/piloto/`, `wokwi/diagram.json`, `wokwi/wokwi.toml` y
la lista de pruebas con el resultado.

Criterio de salida: las seis pruebas pasan en Wokwi. No hay broker todavía.

### Etapa 2 — Los mismos mensajes, contra un broker de prueba

Objetivo: el firmware de Wokwi habla MQTT con el contrato congelado, todavía
sin el VPS de casa.

Pasos:

1. Sustituir la hora simulada como fuente de avisos: el nodo solo publica
   `motion=ON`. Ya no decide la franja.
2. Conectar el ESP32 de Wokwi a un Mosquitto local de esta máquina (sin TLS,
   solo para la simulación).
3. Publicar `availability` con LWT.
4. Suscribirse a `casa/piloto/luz/set` y reflejar `ON`/`OFF` en el relé y en
   `luz/state`.
5. Probar con un cliente MQTT:
   - `OFF` y `ON` cambian la luz del diagrama;
   - el estado retenido se lee al reconectar el cliente;
   - cortar el broker marca `offline` por LWT;
   - al volver, la luz no cambia sola;
   - el botón sigue cambiando la luz con el broker caído y publica el estado
     al reconectar.

Entregables: compose de un Mosquitto de desarrollo, firmware con MQTT detrás
de la misma lógica de la etapa 1, y el resultado de las pruebas.

Criterio de salida: las pruebas de la etapa 1 siguen pasando y las cinco
pruebas MQTT de esta etapa pasan. El broker de desarrollo no se expone a
internet.

### Etapa 3 — Broker en Hetzner

Objetivo: el mismo contrato, con transporte defendible, en el VPS.

Pasos:

1. Confirmar VPS, dominio y acceso SSH. Sin eso no se despliega.
2. Docker: Mosquitto, Caddy y, más adelante, ntfy y el servicio de reglas.
3. Certificado TLS (Let's Encrypt vía Caddy o el mecanismo equivalente del
   dominio).
4. Mosquitto solo en 8883. Sin 1883 público y sin usuario anónimo.
5. Usuarios separados: `piloto` (nodo) y `panel` (aplicación), con la ACL
   del contrato.
6. Cortafuegos del VPS: 22, 443 y 8883. Nada más.
7. Repetir desde Wokwi, ya contra `mqtts://broker.<dominio>:8883`, las cinco
   pruebas de la etapa 2.

Entregables: `deploy/` con compose, plantillas de ACL y un `README` de
despliegue. Secretos solo en el servidor, fuera de git.

Criterio de salida: Wokwi controla la luz simulada a través del broker real
con TLS y ACL, y un cliente anónimo no puede publicar ni suscribirse.

### Etapa 4 — Avisos de movimiento por horario

Objetivo: el celular recibe un aviso solo dentro de la franja.

Pasos:

1. Servicio pequeño en el VPS, suscrito a `casa/piloto/motion`.
2. Configuración: zona horaria, `AVISO_DESDE`, `AVISO_HASTA`. Si la franja
   cruza medianoche (por ejemplo 22:00–07:00), el cálculo lo contempla.
3. Fuera de la franja: no hay aviso. Dentro: un aviso, y silencio de 60 s
   aunque lleguen más eventos.
4. ntfy en el mismo VPS, con usuario. El servicio publica ahí.
5. App ntfy en el celular, suscrita a ese tema.
6. Pruebas con la hora real del servidor y con la franja ajustada a
   "ahora" y a "fuera de ahora". No se espera a la noche para probar.

Entregables: servicio de reglas, configuración de ntfy documentada, pruebas
de dentro/fuera de franja y de cooldown.

Criterio de salida: un `motion=ON` dentro de la franja llega al celular una
sola vez; el mismo evento fuera de la franja no llega; un segundo evento
antes de 60 s no repite el aviso.

### Etapa 5 — Control desde el celular

Objetivo: encender y apagar la luz simulada desde el teléfono, y ver si el
nodo está en línea.

Pasos:

1. Panel web mínimo detrás de Caddy: login, indicador online/offline, botón
   de encendido y apagado, estado real leído de `luz/state`.
2. El panel no abre el puerto MQTT al teléfono. Un proceso en el VPS publica
   `luz/set` con el usuario `panel`.
3. Sesión con contraseña (una cuenta en el piloto). HTTPS obligatorio.
4. Probar en el celular, contra Wokwi:
   - el botón del panel enciende y apaga la luz del diagrama;
   - si se pulsa el botón simulado, el panel cambia solo;
   - con el nodo desconectado, el panel muestra offline y no finge un estado
     nuevo.

Entregables: código del panel, proxy autenticado y prueba hecha desde el
celular (o, si el teléfono no está a mano, desde el navegador de esta
máquina contra la URL pública).

Criterio de salida: desde el celular se controla la luz de Wokwi y se
distingue nodo caído de luz apagada.

### Etapa 6 — Nodo físico

Objetivo: pasar del diagrama al ESP32 comprado, sin cambiar el contrato.

Pasos:

1. Inventario real: modelo exacto de placa, relé, PIR y fuente.
2. Cablear solo baja tensión según el apartado de hardware. Red eléctrica
   aparte, con el corte de pared existente.
3. Grabar el mismo firmware. WiFi y clave MQTT por variables de entorno de
   compilación, no en el código versionado.
4. Repetir en la mesa (relé sin lámpara de red, solo el LED o el clic del
   relé) las pruebas de las etapas 2, 4 y 5.
5. Solo después, conectar la lámpara por el contacto del relé.
6. Dejar escrito el procedimiento de puesta en marcha: qué pin es cuál, qué
   pasa al quitar la corriente y cómo volver a un estado apagado.

Entregables: tabla de pines real, notas de puesta en marcha y las mismas
pruebas pasadas con la placa.

Criterio de salida: el celular enciende y apaga la luz real; el botón de la
pared o el botón local la cambia aunque se caiga el WiFi; un movimiento
dentro de la franja avisa en el celular; al volver la corriente la luz
arranca apagada.

## Qué no se hace en ninguna etapa anterior a su turno

- No se compra ni se cablea nada en la etapa 1.
- No se abre el broker a internet antes de tener TLS, usuarios y ACL.
- No se manda la franja horaria al ESP32.
- No se retiene el comando `luz/set`.
- No se da por buena una etapa con pruebas sin ejecutar.

## Datos que hacen falta al llegar a cada etapa

No bloquean la etapa 1.

| Dato | Se necesita en |
| --- | --- |
| Modelo exacto de los ESP32, relé y PIR | Etapa 6 |
| Dominio apuntando al VPS y acceso SSH | Etapa 3 |
| Zona horaria y franja (propuesta inicial: 22:00–07:00) | Etapa 4 |
| Sistema del celular (Android, iPhone o ambos) | Etapa 5, solo para elegir la app ntfy |

## Después del piloto

Cuando el nodo piloto cumpla la etapa 6, el siguiente nodo es una copia:
otro usuario MQTT, otro prefijo `casa/<habitacion>/...` y el mismo firmware.
Eso no se diseña en detalle hasta tener el primero funcionando en casa.
