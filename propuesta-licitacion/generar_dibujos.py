#!/usr/bin/env python3
"""Genera dibujos técnicos SVG para propuestas de tablero IP67."""

from pathlib import Path

OUT = Path("/workspace/propuesta-licitacion/dibujos")
OUT.mkdir(parents=True, exist_ok=True)

CIRCUITS = [
    ("C01", "Portion Pack", "8.0 kW", "16A"),
    ("C02", "Shifter", "3.0 kW", "10A"),
    ("C03", "FlowPack", "3.0 kW", "10A"),
    ("C04", "Tornillo alim.", "0.7 kW", "6A"),
    ("C05", "Twin Pillow", "9.0 kW", "20A"),
    ("C06", "Tornillo Pillow", "0.7 kW", "6A"),
    ("C07", "Pta. rápida 1", "1.0 kW", "6A"),
    ("C08", "Pta. rápida 2", "1.0 kW", "6A"),
    ("C09", "Pta. rápida 3", "1.0 kW", "6A"),
    ("C10", "Pta. rápida 4", "1.0 kW", "6A"),
    ("C11", "Pta. rápida 5", "1.0 kW", "6A"),
    ("C12", "Ventilación 1", "6.0 kW", "16A"),
    ("C13", "Ventilación 2", "6.0 kW", "16A"),
    ("C14", "Ventilación 3", "6.0 kW", "16A"),
    ("C15", "Elevador tarimas", "3.7 kW", "10A"),
]


def svg_header(w, h, title):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
  text {{ font-family: Arial, Helvetica, sans-serif; fill: #1a1a1a; }}
  .title {{ font-size: 18px; font-weight: bold; }}
  .subtitle {{ font-size: 12px; fill: #444; }}
  .label {{ font-size: 11px; }}
  .small {{ font-size: 9px; fill: #555; }}
  .wire {{ stroke: #111; stroke-width: 2; fill: none; }}
  .box {{ fill: #f7f7f7; stroke: #333; stroke-width: 1.5; }}
  .breaker {{ fill: #e8f0fe; stroke: #1a56db; stroke-width: 1.5; }}
  .meter {{ fill: #fef3c7; stroke: #b45309; stroke-width: 1.5; }}
  .main {{ fill: #fee2e2; stroke: #b91c1c; stroke-width: 2; }}
  .load {{ fill: #ecfdf5; stroke: #047857; stroke-width: 1.2; }}
  .cabinet {{ fill: none; stroke: #374151; stroke-width: 3; }}
  .rail {{ fill: #9ca3af; stroke: #4b5563; stroke-width: 1; }}
  .dim {{ stroke: #6b7280; stroke-width: 1; fill: none; stroke-dasharray: 4 3; }}
</style>
<text x="30" y="30" class="title">{title}</text>
'''


def diagrama_unifilar(brand: str):
    w, h = 1100, 900
    s = svg_header(w, h, f"Diagrama Unifilar — Propuesta {brand}")
    s += f'<text x="30" y="50" class="subtitle">Tablero distribución 75 kW @ 460V 3Ø 60Hz | IP67 | Acero Inox. AISI 304 | Griffith Foods — Área Polvos</text>\n'

    # Source
    s += '<rect x="420" y="70" width="260" height="50" class="box"/>'
    s += '<text x="550" y="100" text-anchor="middle" class="label">Cuarto eléctrico principal</text>'
    s += '<text x="550" y="140" text-anchor="middle" class="small">Disy. alimentador 125A — SIEMENS (según cartel)</text>'
    s += '<line x1="550" y1="120" x2="550" y2="170" class="wire"/>'

    # Main breaker
    s += '<rect x="470" y="170" width="160" height="60" class="main"/>'
    s += f'<text x="550" y="195" text-anchor="middle" class="label">INT. PRINCIPAL 125A 3P</text>'
    s += f'<text x="550" y="215" text-anchor="middle" class="small">{brand}</text>'
    s += '<line x1="550" y1="230" x2="550" y2="260" class="wire"/>'

    # Meter
    s += '<rect x="470" y="260" width="160" height="50" class="meter"/>'
    s += '<text x="550" y="285" text-anchor="middle" class="label">Medidor energía + Ethernet</text>'
    s += '<line x1="550" y1="310" x2="550" y2="340" class="wire"/>'

    # Busbar
    s += '<rect x="120" y="340" width="860" height="24" class="rail"/>'
    s += '<text x="550" y="356" text-anchor="middle" class="small" fill="#fff">Barra de cobre 125A — 460V 3Ø + N + PE</text>'

    # Branch breakers row 1
    x0, y0 = 130, 380
    for i, (cid, name, kw, br) in enumerate(CIRCUITS[:8]):
        x = x0 + i * 105
        s += f'<rect x="{x}" y="{y0}" width="90" height="55" class="breaker"/>'
        s += f'<text x="{x+45}" y="{y0+18}" text-anchor="middle" class="small">{cid} {br}</text>'
        s += f'<text x="{x+45}" y="{y0+32}" text-anchor="middle" class="small">{name[:14]}</text>'
        s += f'<text x="{x+45}" y="{y0+46}" text-anchor="middle" class="small">{kw}</text>'
        s += f'<line x1="{x+45}" y1="364" x2="{x+45}" y2="{y0}" class="wire"/>'
        s += f'<line x1="{x+45}" y1="{y0+55}" x2="{x+45}" y2="520" class="wire"/>'

    # Row 2
    y0 = 460
    for i, (cid, name, kw, br) in enumerate(CIRCUITS[8:]):
        x = x0 + i * 105
        s += f'<rect x="{x}" y="{y0}" width="90" height="55" class="breaker"/>'
        s += f'<text x="{x+45}" y="{y0+18}" text-anchor="middle" class="small">{cid} {br}</text>'
        s += f'<text x="{x+45}" y="{y0+32}" text-anchor="middle" class="small">{name[:14]}</text>'
        s += f'<text x="{x+45}" y="{y0+46}" text-anchor="middle" class="small">{kw}</text>'
        s += f'<line x1="{x+45}" y1="364" x2="{x+45}" y2="{y0}" class="wire"/>'
        s += f'<line x1="{x+45}" y1="{y0+55}" x2="{x+45}" y2="520" class="wire"/>'

    # Loads area
    s += '<rect x="100" y="530" width="900" height="120" class="box"/>'
    s += '<text x="550" y="555" text-anchor="middle" class="label">Salidas a equipos 460V (canastas existentes + tubería SS/IMC Al entrada inferior)</text>'
    loads = " | ".join([c[1][:12] for c in CIRCUITS])
    s += f'<text x="550" y="580" text-anchor="middle" class="small">{loads[:120]}...</text>'
    s += '<text x="550" y="610" text-anchor="middle" class="small">Carga conectada: 51.1 kW | Demanda (Fd=0.85): 43.4 kW | Reserva: 23.9 kW (32%)</text>'
    s += '<text x="550" y="630" text-anchor="middle" class="small">Excluidos del tablero: Big bag downloader (220V) y Metal detector (240V) — tablero existente</text>'

    # Legend
    s += '<rect x="80" y="700" width="940" height="160" class="box"/>'
    s += '<text x="100" y="725" class="label">Notas de diseño:</text>'
    notes = [
        "• Sistema 460V 3F+N+PE, 60 Hz. Factor de potencia diseño: 0.85.",
        "• Protecciones termomagnéticas tipo riel DIN, curva C (motores) / B (auxiliares).",
        "• Entrada principal y circuitos por parte inferior del gabinete (IP67).",
        "• Cumplimiento RETIE / NEC aplicable, montaje higiénico industria alimenticia.",
        "• Reserva de espacio: 3 módulos DIN libres por fila para expansión futura.",
    ]
    for i, n in enumerate(notes):
        s += f'<text x="100" y="{750 + i*18}" class="small">{n}</text>'

    s += '</svg>'
    (OUT / f"unifilar_{brand.lower()}.svg").write_text(s, encoding="utf-8")


def layout_frontal(brand: str, dims: tuple):
    w, h, d = dims
    svg_w, svg_h = 900, 1100
    s = svg_header(svg_w, svg_h, f"Vista Frontal — Gabinete IP67 — {brand}")
    s += f'<text x="30" y="50" class="subtitle">Dimensiones externas: {w} × {h} × {d} mm (An × Al × Pr)</text>\n'

    ox, oy = 150, 120
    fw, fh = 600, 850
    s += f'<rect x="{ox}" y="{oy}" width="{fw}" height="{fh}" class="cabinet" rx="6"/>'
    s += f'<rect x="{ox+15}" y="{oy+15}" width="{fw-30}" height="{fh-30}" class="box"/>'

    # Door sections
    s += f'<rect x="{ox+30}" y="{oy+40}" width="{fw-60}" height="120" class="main"/>'
    s += f'<text x="{ox+fw/2}" y="{oy+90}" text-anchor="middle" class="label">Puerta principal con bisagras INOX + pestillo 2 puntos</text>'
    s += f'<text x="{ox+fw/2}" y="{oy+115}" text-anchor="middle" class="small">Ventana opcional de inspección IP67 (propuesta {brand})</text>'

    s += f'<rect x="{ox+30}" y="{oy+180}" width="{fw-60}" height="80" class="meter"/>'
    s += f'<text x="{ox+fw/2}" y="{oy+225}" text-anchor="middle" class="label">Display medidor energía + puerto RJ45 Ethernet</text>'

    # Breaker zones
    s += f'<rect x="{ox+30}" y="{oy+280}" width="{fw-60}" height="280" class="breaker"/>'
    s += f'<text x="{ox+fw/2}" y="{oy+305}" text-anchor="middle" class="label">Zona protecciones — Fila superior (8 circuitos)</text>'
    for i in range(8):
        bx = ox + 50 + i * 65
        s += f'<rect x="{bx}" y="{oy+320}" width="50" height="70" fill="#dbeafe" stroke="#2563eb"/>'
        s += f'<text x="{bx+25}" y="{oy+365}" text-anchor="middle" class="small">{CIRCUITS[i][0]}</text>'

    s += f'<text x="{ox+fw/2}" y="{oy+420}" text-anchor="middle" class="label">Zona protecciones — Fila inferior (7 circuitos + reserva)</text>'
    for i in range(7):
        bx = ox + 50 + i * 65
        s += f'<rect x="{bx}" y="{oy+440}" width="50" height="70" fill="#dbeafe" stroke="#2563eb"/>'
        s += f'<text x="{bx+25}" y="{oy+485}" text-anchor="middle" class="small">{CIRCUITS[8+i][0]}</text>'

    # Bottom glands
    s += f'<rect x="{ox+30}" y="{oy+580}" width="{fw-60}" height="120" fill="#f3f4f6" stroke="#6b7280"/>'
    s += f'<text x="{ox+fw/2}" y="{oy+610}" text-anchor="middle" class="label">Placa de fondo — Prensaestopas IP67</text>'
    for i in range(6):
        gx = ox + 80 + i * 85
        s += f'<circle cx="{gx}" cy="{oy+660}" r="18" fill="#fff" stroke="#111" stroke-width="2"/>'
    s += f'<text x="{ox+fw/2}" y="{oy+690}" text-anchor="middle" class="small">Entrada acometida principal + 5 grupos de circuitos (3F+N+PE c/u)</text>'

    # Nameplate
    s += f'<rect x="{ox+30}" y="{oy+720}" width="{fw-60}" height="100" fill="#fff" stroke="#333"/>'
    s += f'<text x="{ox+fw/2}" y="{oy+750}" text-anchor="middle" class="label">Placa de identificación</text>'
    s += f'<text x="{ox+fw/2}" y="{oy+775}" text-anchor="middle" class="small">TDP-GRF-POLVOS-01 | 75 kW | 460V 3Ø | IP67 | SS304</text>'
    s += f'<text x="{ox+fw/2}" y="{oy+795}" text-anchor="middle" class="small">Griffith Foods S.A. — Lagunilla, Heredia, CR</text>'

    # Dimensions
    s += f'<line x1="{ox}" y1="{oy+fh+30}" x2="{ox+fw}" y2="{oy+fh+30}" class="dim"/>'
    s += f'<text x="{ox+fw/2}" y="{oy+fh+50}" text-anchor="middle" class="label">{w} mm</text>'
    s += f'<line x1="{ox-30}" y1="{oy}" x2="{ox-30}" y2="{oy+fh}" class="dim"/>'
    s += f'<text x="{ox-45}" y="{oy+fh/2}" text-anchor="middle" class="label" transform="rotate(-90 {ox-45} {oy+fh/2})">{h} mm</text>'

    s += '</svg>'
    (OUT / f"frontal_{brand.lower()}.svg").write_text(s, encoding="utf-8")


def layout_planta():
    w, h = 1000, 700
    s = svg_header(w, h, "Plano de Ubicación — Tablero y Acometida (referencia cartel)")
    s += '<text x="30" y="50" class="subtitle">Griffith Foods — Área de polvos | Canasta existente + tramo nuevo 400mm pared Sur</text>\n'

    # Building outline simplified
    s += '<rect x="80" y="80" width="840" height="520" fill="#fafafa" stroke="#333" stroke-width="2"/>'
    s += '<text x="500" y="110" text-anchor="middle" class="label">Área de proceso polvos (referencia layout cartel p.7)</text>'

    # Equipment boxes
    equip = [
        (120, 150, 140, 80, "Portion Pack"),
        (120, 260, 140, 80, "Flow Pack"),
        (300, 150, 120, 100, "Vent. 1"),
        (300, 280, 120, 100, "Vent. 2"),
        (300, 410, 120, 100, "Vent. 3"),
        (500, 150, 130, 70, "Descargador\nbig bags"),
        (500, 240, 130, 70, "Twin Pillow"),
        (500, 330, 130, 70, "Shifter"),
        (500, 420, 130, 70, "Metal detector\n(240V exist.)"),
        (680, 200, 180, 120, "Zona bodega\nnueva"),
    ]
    for x, y, bw, bh, name in equip:
        s += f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" class="load"/>'
        lines = name.split("\n")
        for j, ln in enumerate(lines):
            s += f'<text x="{x+bw/2}" y="{y+30+j*16}" text-anchor="middle" class="small">{ln}</text>'

    # Panel location
    s += '<rect x="120" y="480" width="100" height="60" class="main"/>'
    s += '<text x="170" y="515" text-anchor="middle" class="label">TABLERO</text>'
    s += '<text x="170" y="530" text-anchor="middle" class="small">IP67 SS304</text>'

    # Cable tray route
    s += '<path d="M 820 540 L 620 540 L 620 510 L 220 510" fill="none" stroke="#2563eb" stroke-width="4"/>'
    s += '<text x="720" y="530" class="small" fill="#2563eb">Canasta existente</text>'
    s += '<path d="M 220 510 L 170 510" fill="none" stroke="#dc2626" stroke-width="4" stroke-dasharray="6 4"/>'
    s += '<text x="195" y="500" class="small" fill="#dc2626">Canasta nueva Al 400mm</text>'

    s += '<rect x="780" y="520" width="120" height="60" class="box"/>'
    s += '<text x="840" y="555" text-anchor="middle" class="small">Cuarto eléctrico\n125A Siemens</text>'

    # Notes
    s += '<text x="80" y="640" class="small">• Soportería SS separada 50 mm de pared Sur  • Entrada tubería por parte inferior tablero  • Dim. área ref: 8.01 m × 11.50 m</text>'
    s += '</svg>'
    (OUT / "planta_ubicacion.svg").write_text(s, encoding="utf-8")


for brand in ("SIEMENS", "SCHNEIDER"):
    diagrama_unifilar(brand)
    layout_frontal(brand, (1000, 1600, 400))

layout_planta()
print("Dibujos generados en", OUT)
