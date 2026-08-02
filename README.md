# Industrial RAG Multi-Máquina

Arquitectura reutilizable para consultar fallas e información técnica de equipos
de distintos fabricantes **sin enviar los PDFs al LLM**.

Caso típico: formadora de tubos (VFD Danfoss + PLC Siemens + …) u otra línea.
La ingestión es local y cuesta **0 tokens / 0 créditos**. Solo la consulta
opcional usa un LLM barato con 3–5 fragmentos (~1 000 tokens).

## Principio

```
PDFs de manuales (1000+ págs)
        │
        ▼
Python local (0 tokens)
  • divide por página
  • extrae texto / tablas
  • detecta fault_codes (AL 38, E-05…)
  • embeddings locales (FastEmbed)
        │
        ▼
Qdrant (índice con metadatos)
  machine_id + equipment_id + fabricante + modelo + página
        │
        ▼
Consulta del técnico
  Router filtra por máquina/equipo
  Búsqueda híbrida (vector + código exacto)
        │
        ▼
LLM opcional (solo 3–5 chunks)  o  fallback extractivo (0 créditos)
        │
        ▼
Diagnóstico + página del manual
```

## Por qué no se mandan los PDFs al modelo

| Momento | ¿Usa LLM? | Tokens | Costo |
|---------|-----------|--------|-------|
| Ingesta (una vez por manual) | No | 0 | $0 |
| Consulta (cada falla) | Opcional | ~1 000 | ~$0.001 o $0 sin API |

## Reutilizable para otras máquinas

Cada equipo lleva `machine_id`. El mismo sistema sirve a:

- `TUBE-FORMER-01` — formadora de tubos
- `PACK-LINE-01` — línea de empaque
- cualquier máquina nueva: añada filas en `data/equipment_registry.json`

El router **nunca** busca en toda la biblioteca: filtra por
`machine_id` + `equipment_id` (+ fabricante/modelo).

## Arranque rápido (piloto, sin Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Diagnóstico en memoria (0 créditos; fallback extractivo)
industrial-rag troubleshoot \
  --equipment-id VFD-TUBE-01 \
  --query "AL 38" \
  --memory --reindex
```

## Ingestar un PDF real (0 tokens LLM)

1. Registre el equipo en `data/equipment_registry.json`.
2. Ejecute:

```bash
industrial-rag ingest-pdf \
  --pdf "manuales/Danfoss_FC302_1000pag.pdf" \
  --equipment-id VFD-TUBE-01 \
  --memory
```

O todo el registro:

```bash
industrial-rag ingest-registry --memory
```

## Stack con Qdrant (Hetzner / Docker)

```bash
cp .env.example .env
docker compose up --build

# Salud
curl -s http://localhost:8000/health

# Ingesta PDF (0 tokens)
curl -s -X POST http://localhost:8000/ingestar \
  -F "file=@manuales/Danfoss_FC302.pdf" \
  -F "equipment_id=VFD-TUBE-01"

# Consulta
curl -s -X POST http://localhost:8000/troubleshoot \
  -H 'Content-Type: application/json' \
  -d '{"machine_id":"TUBE-FORMER-01","equipment_id":"VFD-TUBE-01","query":"AL 38"}'
```

## Registro de equipos (ejemplo)

| machine_id | equipment_id | manufacturer | model |
|------------|--------------|--------------|-------|
| TUBE-FORMER-01 | VFD-TUBE-01 | Danfoss | FC-302 |
| TUBE-FORMER-01 | PLC-TUBE-01 | Siemens | S7-1500 |
| PACK-LINE-01 | VFD-LINE1-02 | Danfoss | FC-302 |

El piloto incluye el mismo código `E-05` en VFD y PLC con significados distintos,
y `AL 38` / `AL 39` para validar coincidencia exacta de códigos.

## API

| Método | Ruta | Uso |
|--------|------|-----|
| GET | `/health` | Estado |
| POST | `/troubleshoot` | Diagnóstico AppSheet / UI |
| POST | `/webhook/alarm` | Alarma SCADA vía n8n |
| POST | `/ingestar` | Subir PDF (0 tokens LLM) |
| POST | `/admin/ingest-registry` | Reindexar registro |
| POST | `/admin/reindex-pilot` | Recarga chunks de muestra |

## LLM en consulta (opcional)

- Con `GEMINI_API_KEY` o `ANTHROPIC_API_KEY` en `.env`, genera el reporte con API.
- Sin clave: fallback extractivo **solo** con el texto recuperado (útil en planta sin costo).
- No se recomienda LLM local en VPS de 4 GB RAM (Qdrant + embeddings + modelo → OOM).

## Tests

```bash
pytest -q
```

Validan aislamiento entre equipos/máquinas y preferencia de `AL 38` sobre `AL 39`.
