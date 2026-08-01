# Siemens S7-1500 — Códigos de falla (extracto piloto)

<!-- page: 40 -->

| Código | Causa | Solución |
| --- | --- | --- |
| SF | System Fault en CPU S7-1500. | Revisar buffer de diagnóstico, módulos con LED rojo y configuración de hardware vs online. |

<!-- page: 42 -->

| Código | Causa | Solución |
| --- | --- | --- |
| E-05 | Error de módulo de E/S (NO es sobrecorriente de drive). Fallo de comunicación con tarjeta de entradas. | Verificar conector del módulo, alimentación 24 VDC del rack y diagnóstico del canal en TIA Portal. |

<!-- page: 45 -->

### Pruebas de campo

- Medir 24 VDC en bornes L+/M del módulo (21.6–28.8 V).
- Verificar continuidad de bus backplane.
- No aplicar procedimientos de variadores de frecuencia a este equipo.
