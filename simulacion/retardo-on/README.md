# Retardo ON de 10 s

ESP32 en Wokwi. El switch de la izquierda es la entrada. El LED verde es la salida.

- Switch a la izquierda: entrada en reposo, LED apagado.
- Switch a la derecha: entrada activa. El LED sigue apagado.
- Si el switch permanece a la derecha 10 segundos, el LED enciende.
- Si vuelve a la izquierda antes de esos 10 segundos, el conteo se cancela.
- Si vuelve a la izquierda con el LED ya encendido, el LED se apaga.

En el monitor serie se ve la cuenta: `Faltan 9 s` … `Faltan 1 s`, y después `Salida ON`.

## Abrirlo en Wokwi

1. Entra en https://wokwi.com/projects/new/esp32
2. En la pestaña `sketch.ino`, sustituye todo el código por el de este `sketch.ino`.
3. En la pestaña `diagram.json`, sustituye todo el texto por el de este `diagram.json`.
4. Arranca la simulación y pasa el switch a la derecha.

`diagram.pushbutton.json` y `scenarios/` sirven para repetir la misma prueba con el botón mantenido, que Wokwi CLI sí puede pulsar solo. El circuito que se usa a mano es el del switch.
