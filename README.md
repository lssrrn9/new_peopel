# Industrial RAG — Troubleshooting con Router de Metadatos

Pipeline RAG para diagnóstico de fallas en línea de producción. Evita el error clásico de volcar todos los PDFs en un solo índice sin filtros (que mezcla códigos de un VFD con un PLC de otra marca).

## Flujo estricto

```
[ Trigger de Falla ]
  ├── A: Alarma PLC/SCADA (MQTT → webhook)
  └── B: Técnico (AppSheet / UI: Equipo + Código)
           │
           ▼
[ Router por Metadatos ]  → filtra solo el manual del equipo
           │
           ▼
[ Buscador Vectorial ]    → páginas de fallas / diagramas / tablas
           │
           ▼
[ LLM Diagnóstico ]       → Causa, Pruebas, Solución, Página
           │
           ▼
[ Interfaz del Técnico ]
```

## Los 3 bloques

1. **Ingesta** — cada chunk lleva metadatos obligatorios (`equipment_id`, fabricante, modelo, línea, versión, página). Tablas de falla se conservan en Markdown.
2. **Router** — la búsqueda vectorial **nunca** barre toda la biblioteca; filtro duro `metadata.equipment_id == …`.
3. **Prompt estricto** — el modelo solo usa el extracto del manual; si no hay dato, responde *Información no disponible en el manual oficial*.

## Arranque rápido (piloto VFD)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Diagnóstico en memoria (sin Docker), con datos piloto
industrial-rag troubleshoot \
  --equipment-id VFD-LINE1-02 \
  --query "Falla E-05" \
  --memory --reindex
```

### Stack con Qdrant

```bash
cp .env.example .env
docker compose up --build
curl -s http://localhost:8000/health
curl -s -X POST http://localhost:8000/troubleshoot \
  -H 'Content-Type: application/json' \
  -d '{"equipment_id":"VFD-LINE1-02","query":"Falla E-05","source":"appsheet"}'
```

## Registro de equipos

`data/equipment_registry.json` relaciona **ID de equipo → archivo de manual**:

| equipment_id   | manufacturer | model   | line           |
|----------------|--------------|---------|----------------|
| VFD-LINE1-02   | Danfoss      | FC-302  | Linea_Empaque  |
| PLC-LINE1-01   | Siemens      | S7-1500 | Linea_Empaque  |

El piloto incluye el mismo código `E-05` en VFD y PLC con significados distintos. El router garantiza aislamiento total.

## API

| Método | Ruta                 | Uso                                      |
|--------|----------------------|------------------------------------------|
| GET    | `/health`            | Estado                                   |
| POST   | `/troubleshoot`      | AppSheet / UI manual                     |
| POST   | `/webhook/alarm`     | Alarma SCADA vía n8n                     |
| POST   | `/admin/reindex-pilot` | Recarga `data/sample_chunks/*.jsonl`   |

Ejemplo de payload:

```json
{
  "equipment_id": "VFD-LINE1-02",
  "query": "Falla E-05",
  "source": "appsheet"
}
```

## Opción Low-Code (AppSheet + n8n)

Plantilla de flujo en `n8n/troubleshoot_webhook.json`:

1. AppSheet envía `equipment_id` + código de falla al webhook n8n.
2. n8n llama a `POST /troubleshoot`.
3. Devuelve el reporte formateado al técnico (< 3 s en red local típica).

## LLM

- Con `ANTHROPIC_API_KEY` o `GEMINI_API_KEY` en `.env`, el generador usa la API.
- Sin clave, usa un fallback extractivo **solo** con el texto recuperado (útil para validar en planta sin costo).

## Indexar manuales Markdown

```bash
python scripts/index_markdown_manuals.py --memory
```

Los manuales usan marcadores `<!-- page: N -->`. Para PDFs reales, asegúrese de OCR con capa de texto; páginas de códigos de falla conviene convertirlas a Markdown o usar visión multimodal.

## Tests

```bash
pytest -q
```

La suite valida que `E-05` del VFD no se contamine con el manual del PLC Siemens.
