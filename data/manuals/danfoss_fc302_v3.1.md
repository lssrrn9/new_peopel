# Manual Danfoss FC-302 v3.1 (extracto piloto)

<!-- page: 114 -->

## Tabla de códigos de falla

| Código | Causa | Solución |
| --- | --- | --- |
| E-05 | Sobrecorriente en etapa de potencia. Corriente de salida supera el límite del drive. | Verificar aislamiento del motor, cableado de potencia U/V/W, longitud de cable y rampa de aceleración. Medir resistencia de aislamiento > 1 MΩ. |
| E-07 | Sobretensión en bus DC durante desaceleración. | Aumentar tiempo de desaceleración o instalar resistor de frenado. Verificar suministro de red. |

<!-- page: 115 -->

### Detalle E-05

| Código | Causa | Solución |
| --- | --- | --- |
| E-05 | Sobrecorriente en etapa de potencia (detalle). Causas comunes: motor en cortocircuito, rampa demasiado corta, carga mecánica trabada. | 1) Desconectar motor y medir aislamiento fase-fase y fase-tierra. 2) Verificar torque de bornes. 3) Aumentar tiempo de rampa (par. 3-41/3-42). 4) Liberar carga mecánica del transportador. |

<!-- page: 116 -->

### Pruebas eléctricas ante E-05

- Multímetro en bornes U-V, V-W, W-U del motor: resistencia equilibrada ±5%.
- Megóhmetro 500 VDC fase-tierra: mínimo 1 MΩ en frío.
- Verificar tensión DC bus dentro de rango nominal del manual.
- No puentear protecciones del drive.
