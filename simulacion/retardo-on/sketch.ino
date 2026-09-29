#include <stdint.h>

// Temporizador TON (retardo a la conexión).
// La salida pasa a ON solo si la entrada se mantiene activa durante delay_ms.
// Si la entrada cae antes, el conteo se cancela y la salida sigue en OFF.
// Si la entrada cae con la salida ya en ON, la salida vuelve a OFF.

enum class OnDelayEvent : uint8_t {
  None = 0,
  InputOn,
  Tick,
  OutputOn,
  OutputOff,
  Cancelled,
};

struct OnDelayResult {
  OnDelayEvent event;
  uint32_t seconds_left;
};

struct OnDelay {
  uint32_t delay_ms;
  uint32_t debounce_ms;
  bool output;
  bool input_on;
  bool timing;
  bool have_sample;
  bool raw;
  uint32_t raw_since;
  uint32_t started_at;
  uint32_t announced_seconds;
};

inline void on_delay_init(OnDelay &timer, uint32_t delay_ms, uint32_t debounce_ms) {
  timer = {};
  timer.delay_ms = delay_ms;
  timer.debounce_ms = debounce_ms;
}

inline OnDelayResult on_delay_update(OnDelay &timer, bool level, uint32_t now) {
  OnDelayResult result{OnDelayEvent::None, 0};

  if (!timer.have_sample) {
    timer.have_sample = true;
    timer.raw = level;
    timer.raw_since = now;
    return result;
  }

  if (level != timer.raw) {
    timer.raw = level;
    timer.raw_since = now;
    return result;
  }

  if (static_cast<uint32_t>(now - timer.raw_since) < timer.debounce_ms) {
    return result;
  }

  const bool stable = timer.raw;
  if (stable != timer.input_on) {
    if (stable) {
      timer.input_on = true;
      timer.timing = true;
      timer.output = false;
      timer.started_at = now;
      timer.announced_seconds = 0;
      result.event = OnDelayEvent::InputOn;
      result.seconds_left = timer.delay_ms / 1000;
      return result;
    }

    const bool was_on = timer.output;
    timer.input_on = false;
    timer.timing = false;
    timer.output = false;
    result.event = was_on ? OnDelayEvent::OutputOff : OnDelayEvent::Cancelled;
    return result;
  }

  if (!timer.timing) {
    return result;
  }

  const uint32_t elapsed = static_cast<uint32_t>(now - timer.started_at);
  if (elapsed >= timer.delay_ms) {
    timer.timing = false;
    timer.output = true;
    result.event = OnDelayEvent::OutputOn;
    return result;
  }

  const uint32_t whole_seconds = elapsed / 1000;
  const uint32_t delay_seconds = timer.delay_ms / 1000;
  if (whole_seconds > timer.announced_seconds && whole_seconds < delay_seconds) {
    timer.announced_seconds = whole_seconds;
    result.event = OnDelayEvent::Tick;
    result.seconds_left = delay_seconds - whole_seconds;
  }
  return result;
}

#ifndef HOST_TEST
// Entrada mantenida en GPIO13 (switch a la derecha = 3,3 V).
// Salida en GPIO4, a través de una resistencia de 220 ohm hacia el LED.
constexpr int kPinEntrada = 13;
constexpr int kPinSalida = 4;
constexpr uint32_t kRetardoMs = 10000;
constexpr uint32_t kAntireboteMs = 50;

OnDelay temporizador;

void setup() {
  Serial.begin(115200);
  pinMode(kPinEntrada, INPUT_PULLDOWN);
  pinMode(kPinSalida, OUTPUT);
  digitalWrite(kPinSalida, LOW);
  on_delay_init(temporizador, kRetardoMs, kAntireboteMs);
  Serial.println("Listo");
  Serial.println("Switch a la derecha: entrada ON. El LED enciende 10 s despues.");
}

void loop() {
  const bool activa = digitalRead(kPinEntrada) == HIGH;
  const OnDelayResult resultado = on_delay_update(temporizador, activa, millis());

  switch (resultado.event) {
    case OnDelayEvent::InputOn:
      Serial.printf("Entrada ON. Retardo %u s\n", kRetardoMs / 1000);
      break;
    case OnDelayEvent::Tick:
      Serial.printf("Faltan %u s\n", resultado.seconds_left);
      break;
    case OnDelayEvent::OutputOn:
      digitalWrite(kPinSalida, HIGH);
      Serial.println("Salida ON");
      break;
    case OnDelayEvent::OutputOff:
      digitalWrite(kPinSalida, LOW);
      Serial.println("Entrada OFF. Salida OFF");
      break;
    case OnDelayEvent::Cancelled:
      digitalWrite(kPinSalida, LOW);
      Serial.println("Entrada OFF. Retardo cancelado");
      break;
    case OnDelayEvent::None:
      break;
  }
}
#endif
