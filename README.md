# Manual KK-5S — Sierra volante de corte en frío

Edición web del manual de operación **KK-5S Cold-Cut Flying Saw** (Shijiazhuang Aogang Machinery Co., Ltd., mayo 2019 V1.36). Sistema de control KaiKong KK-5S.

## Descargas

| Archivo | Qué es |
|---|---|
| [descargas/KK-5S-Manual-Operacion-ES.pdf](descargas/KK-5S-Manual-Operacion-ES.pdf) | Manual completo en español (PDF, ~36 páginas) |
| [descargas/KK-5S-User-Manual-EN.pdf](descargas/KK-5S-User-Manual-EN.pdf) | Full English manual (PDF) |
| [descargas/KK-5S-manual-offline.zip](descargas/KK-5S-manual-offline.zip) | Sitio web para abrir sin internet |
| [original/Cold_Cutting_Flying_Saw_Instruction_Manual.docx](original/Cold_Cutting_Flying_Saw_Instruction_Manual.docx) | Word original de fábrica |

**Español (web):** [`index.html`](index.html).  
**English (web):** [`en/index.html`](en/index.html).

```bash
python3 -m http.server 8080
```

Luego visite `http://localhost:8080` (español) o `http://localhost:8080/en/` (inglés).

| Página | Contenido |
|---|---|
| [index.html](index.html) | Portada, inicio rápido, vocabulario del HMI |
| [safety.html](safety.html) | Seguridad mecánica y eléctrica |
| [parameters.html](parameters.html) | Mapa de pantalla y parámetros de producción / servo |
| [functions.html](functions.html) | Modos, energía, jog, origen, amarre/corte, memoria |
| [operation.html](operation.html) | Encendido, automático, programas, sincronismo del encoder |

Las capturas del HMI están en inglés, como en la máquina. Los nombres de botones se citan tal cual (`Manual Cut`, `Calculate`, `Continue`).

Imágenes: [`assets/img/`](assets/img/). Word original: [`original/Cold_Cutting_Flying_Saw_Instruction_Manual.docx`](original/Cold_Cutting_Flying_Saw_Instruction_Manual.docx).

Regenerar HTML:

```bash
python3 tools/build_manual.py
```

## Source

*76 Cold-Cut Flying Saw User Manual*, Aogang Machinery / KaiKong, May 2019 V1.36.
