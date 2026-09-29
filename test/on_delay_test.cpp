#define HOST_TEST 1
#include "sketch.ino"

#include <stdio.h>
#include <stdlib.h>

static int g_failures = 0;

static void expect(bool condition, const char *message) {
  if (!condition) {
    fprintf(stderr, "FALLO: %s\n", message);
    g_failures++;
  }
}

static void hold(OnDelay &timer, bool level, uint32_t from, uint32_t to, OnDelayEvent wanted,
                 uint32_t wanted_seconds) {
  bool seen = false;
  for (uint32_t now = from; now <= to; now++) {
    const OnDelayResult result = on_delay_update(timer, level, now);
    if (result.event == OnDelayEvent::None) {
      continue;
    }
    if (result.event == wanted && result.seconds_left == wanted_seconds && !seen) {
      seen = true;
      continue;
    }
    fprintf(stderr, "FALLO: evento %u a t=%u (segundos %u), se esperaba %u\n",
            static_cast<unsigned>(result.event), now, result.seconds_left,
            static_cast<unsigned>(wanted));
    g_failures++;
  }
  expect(seen, "no aparecio el evento esperado");
}

static void quiet(OnDelay &timer, bool level, uint32_t from, uint32_t to) {
  for (uint32_t now = from; now <= to; now++) {
    const OnDelayResult result = on_delay_update(timer, level, now);
    if (result.event != OnDelayEvent::None) {
      fprintf(stderr, "FALLO: evento inesperado %u a t=%u\n",
              static_cast<unsigned>(result.event), now);
      g_failures++;
      return;
    }
  }
}

static void test_stays_off_without_input() {
  OnDelay timer;
  on_delay_init(timer, 10000, 50);
  quiet(timer, false, 0, 20000);
  expect(!timer.output, "salida encendida sin entrada");
}

static void test_output_at_10_seconds() {
  OnDelay timer;
  on_delay_init(timer, 10000, 50);
  on_delay_update(timer, false, 0);
  quiet(timer, false, 1, 100);
  on_delay_update(timer, true, 1000);
  quiet(timer, true, 1001, 1049);
  hold(timer, true, 1050, 1050, OnDelayEvent::InputOn, 10);
  expect(!timer.output, "la salida no debe encender al aceptar la entrada");

  for (uint32_t second = 1; second <= 9; second++) {
    const uint32_t at = 1050 + second * 1000;
    quiet(timer, true, at - 1, at - 1);
    hold(timer, true, at, at, OnDelayEvent::Tick, 10 - second);
    expect(!timer.output, "la salida se adelanto");
  }

  quiet(timer, true, 11049, 11049);
  hold(timer, true, 11050, 11050, OnDelayEvent::OutputOn, 0);
  expect(timer.output, "la salida sigue apagada a los 10 s");
  quiet(timer, true, 11051, 13000);
  expect(timer.output, "la salida no se mantuvo");
}

static void test_cancel_before_delay() {
  OnDelay timer;
  on_delay_init(timer, 10000, 50);
  on_delay_update(timer, false, 0);
  on_delay_update(timer, true, 100);
  hold(timer, true, 150, 150, OnDelayEvent::InputOn, 10);
  on_delay_update(timer, false, 5001);
  quiet(timer, false, 5002, 5050);
  hold(timer, false, 5051, 5051, OnDelayEvent::Cancelled, 0);
  expect(!timer.output, "cancelar dejo la salida en ON");
  quiet(timer, false, 5052, 20000);
}

static void test_release_turns_output_off() {
  OnDelay timer;
  on_delay_init(timer, 10000, 50);
  on_delay_update(timer, true, 0);
  hold(timer, true, 50, 50, OnDelayEvent::InputOn, 10);
  hold(timer, true, 10050, 10050, OnDelayEvent::OutputOn, 0);
  on_delay_update(timer, false, 12000);
  hold(timer, false, 12050, 12050, OnDelayEvent::OutputOff, 0);
  expect(!timer.output, "soltar la entrada dejo la salida en ON");
}

static void test_retrigger_starts_again() {
  OnDelay timer;
  on_delay_init(timer, 10000, 50);
  on_delay_update(timer, false, 0);
  on_delay_update(timer, true, 100);
  hold(timer, true, 150, 150, OnDelayEvent::InputOn, 10);
  on_delay_update(timer, false, 4000);
  hold(timer, false, 4050, 4050, OnDelayEvent::Cancelled, 0);

  on_delay_update(timer, true, 5000);
  hold(timer, true, 5050, 5050, OnDelayEvent::InputOn, 10);
  hold(timer, true, 15050, 15050, OnDelayEvent::OutputOn, 0);
  expect(timer.output, "el segundo ciclo no encendio la salida");
}

static void test_short_glitch_does_not_reset() {
  OnDelay timer;
  on_delay_init(timer, 10000, 50);
  on_delay_update(timer, true, 0);
  hold(timer, true, 50, 50, OnDelayEvent::InputOn, 10);

  const OnDelayResult fell = on_delay_update(timer, false, 5000);
  expect(fell.event == OnDelayEvent::None, "el flanco corto no debe cancelar al instante");
  const OnDelayResult back = on_delay_update(timer, true, 5020);
  expect(back.event == OnDelayEvent::None, "volver a ON no abre otro retardo");
  quiet(timer, true, 5021, 5069);
  expect(timer.timing, "un glitch corto cancelo el temporizador");
  expect(!timer.output, "un glitch encendio la salida");
  hold(timer, true, 10050, 10050, OnDelayEvent::OutputOn, 0);
}

static void test_millis_wrap() {
  OnDelay timer;
  on_delay_init(timer, 10000, 50);
  const uint32_t edge = 0xFFFFFFF0u;
  on_delay_update(timer, false, edge - 100);
  on_delay_update(timer, true, edge);
  const uint32_t accepted = edge + 50;
  hold(timer, true, accepted, accepted, OnDelayEvent::InputOn, 10);
  const uint32_t done = accepted + 10000;
  hold(timer, true, done, done, OnDelayEvent::OutputOn, 0);
  expect(timer.output, "el desborde de millis impidio encender");
}

int main() {
  test_stays_off_without_input();
  test_output_at_10_seconds();
  test_cancel_before_delay();
  test_release_turns_output_off();
  test_retrigger_starts_again();
  test_short_glitch_does_not_reset();
  test_millis_wrap();

  if (g_failures != 0) {
    fprintf(stderr, "%d fallos\n", g_failures);
    return 1;
  }
  printf("on-delay: ok\n");
  return 0;
}
