#!/usr/bin/env python3
"""Genera docs/index.html a partir de los Markdown de curso/.

No altera el texto. Copia los SVG a docs/img para que el HTML sea autónomo.
"""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
CURSO = ROOT / "curso"
DOCS = ROOT / "docs"
IMG_OUT = DOCS / "img"

PAGES = [
    ("00-fuentes-y-entorno.md", "fuentes", "Fuentes y entorno"),
    ("01-indice-y-matriz.md", "indice", "Índice y matriz"),
    ("01b-fichas-modulos.md", "fichas", "Fichas de los módulos"),
    ("02-modulo-01-arquitectura.md", "modulo-01", "Módulo 1"),
    ("03-modulo-02-alimentacion.md", "modulo-02", "Módulo 2"),
]


def slug(text: str) -> str:
    text = text.lower()
    text = (
        text.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .replace("ü", "u")
    )
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "seccion"


def build_page(md_name: str, page_id: str) -> tuple[str, list[tuple[str, str, int]]]:
    raw = (CURSO / md_name).read_text(encoding="utf-8")
    raw = raw.replace("](img/", "](img/")
    # Enlaces entre páginas: apuntan a anclas de esta misma página HTML.
    raw = raw.replace("(00-fuentes-y-entorno.md)", "(#fuentes)")
    raw = raw.replace("(01-indice-y-matriz.md)", "(#indice)")
    raw = raw.replace("(01b-fichas-modulos.md)", "(#fichas)")
    raw = raw.replace("(02-modulo-01-arquitectura.md)", "(#modulo-01)")
    raw = raw.replace("(03-modulo-02-alimentacion.md)", "(#modulo-02)")

    headings: list[tuple[str, str, int]] = []

    def add_ids(match: re.Match) -> str:
        level = int(match.group(1))
        title = match.group(2).strip()
        hid = f"{page_id}-{slug(title)}"
        if level == 1:
            hid = page_id
        headings.append((hid, title, level))
        return f'<h{level} id="{hid}">{title}</h{level}>'

    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )
    body = md.convert(raw)
    body = re.sub(
        r"<h([1-3])(?:\s[^>]*)?>(.*?)</h\1>",
        add_ids,
        body,
        flags=re.DOTALL,
    )
    body = body.replace('src="img/', 'src="img/')
    return f'<article id="pagina-{page_id}" class="page">\n{body}\n</article>\n', headings


CSS = r"""
:root {
  --bg: #f6f3ee;
  --paper: #fffcf7;
  --ink: #1c1917;
  --muted: #57534e;
  --line: #e7e5e4;
  --accent: #1e3a5f;
  --accent-2: #0f766e;
  --mark: #fef3c7;
  --sidebar: 280px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: "Liberation Sans", "Segoe UI", sans-serif;
  color: var(--ink);
  background: var(--bg);
  line-height: 1.55;
}
a { color: var(--accent); }
#sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  width: var(--sidebar);
  overflow: auto;
  background: var(--accent);
  color: #f8fafc;
  padding: 18px 14px 32px;
}
#sidebar h1 {
  font-size: 16px;
  margin: 0 0 8px;
  line-height: 1.3;
}
#sidebar p { color: #cbd5e1; font-size: 12px; margin: 0 0 12px; }
#filtro {
  width: 100%;
  padding: 8px 10px;
  border: 0;
  border-radius: 6px;
  margin-bottom: 12px;
}
#sidebar a {
  color: #e2e8f0;
  text-decoration: none;
  display: block;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 13px;
}
#sidebar a:hover, #sidebar a:focus { background: #334155; }
#sidebar a.lvl2 { padding-left: 16px; font-size: 12px; color: #cbd5e1; }
#sidebar a.lvl3 { display: none; }
main {
  margin-left: var(--sidebar);
  padding: 28px 40px 80px;
  max-width: 1080px;
}
article {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 8px 32px 28px;
  margin-bottom: 28px;
}
h1 { font-size: 1.8rem; line-height: 1.25; }
h2 { font-size: 1.35rem; margin-top: 1.8rem; border-top: 1px solid var(--line); padding-top: 1rem; }
h3 { font-size: 1.1rem; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.95rem; }
th, td { border: 1px solid var(--line); padding: 6px 8px; vertical-align: top; text-align: left; }
th { background: #eef2ff; }
tr:nth-child(even) td { background: #fafaf9; }
code {
  font-family: "Liberation Mono", ui-monospace, monospace;
  font-size: 0.92em;
  background: #f5f5f4;
  padding: 0 4px;
  border-radius: 3px;
}
pre {
  position: relative;
  background: #1c1917;
  color: #f5f5f4;
  padding: 14px 16px;
  border-radius: 8px;
  overflow: auto;
}
pre code { background: transparent; color: inherit; padding: 0; }
button.copy {
  position: absolute;
  top: 8px;
  right: 8px;
  border: 0;
  background: #44403c;
  color: white;
  border-radius: 4px;
  padding: 4px 8px;
  cursor: pointer;
}
img {
  max-width: 100%;
  height: auto;
  background: white;
  border: 1px solid var(--line);
  border-radius: 8px;
  cursor: zoom-in;
}
blockquote {
  margin: 1rem 0;
  padding: 8px 14px;
  border-left: 4px solid var(--accent-2);
  background: #f0fdfa;
}
#lightbox {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.88);
  z-index: 20;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
#lightbox.open { display: flex; }
#lightbox img { max-width: 96vw; max-height: 92vh; cursor: zoom-out; background: white; }
@media (max-width: 860px) {
  #sidebar { position: static; width: auto; }
  main { margin-left: 0; padding: 16px; }
}
"""

JS = r"""
const filtro = document.getElementById("filtro");
filtro.addEventListener("input", () => {
  const q = filtro.value.toLowerCase();
  document.querySelectorAll("#nav a").forEach((a) => {
    a.style.display = a.textContent.toLowerCase().includes(q) ? "block" : "none";
  });
});
document.querySelectorAll("pre").forEach((pre) => {
  const btn = document.createElement("button");
  btn.className = "copy";
  btn.type = "button";
  btn.textContent = "Copiar";
  btn.addEventListener("click", async () => {
    const code = pre.querySelector("code");
    const text = code ? code.innerText : pre.innerText;
    try {
      await navigator.clipboard.writeText(text);
      btn.textContent = "Copiado";
    } catch (err) {
      btn.textContent = "Selecciona y copia";
    }
    setTimeout(() => { btn.textContent = "Copiar"; }, 1500);
  });
  pre.appendChild(btn);
});
const box = document.getElementById("lightbox");
const zoom = document.getElementById("zoom");
document.querySelectorAll("article img").forEach((img) => {
  img.addEventListener("click", () => {
    zoom.src = img.src;
    zoom.alt = img.alt;
    box.classList.add("open");
  });
});
box.addEventListener("click", () => box.classList.remove("open"));
document.addEventListener("keydown", (ev) => {
  if (ev.key === "Escape") box.classList.remove("open");
});
"""


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    if IMG_OUT.exists():
        shutil.rmtree(IMG_OUT)
    shutil.copytree(CURSO / "img", IMG_OUT)

    nav_parts: list[str] = []
    articles: list[str] = []
    for filename, page_id, _label in PAGES:
        article, headings = build_page(filename, page_id)
        articles.append(article)
        for hid, title, level in headings:
            if level > 2:
                continue
            cls = "lvl1" if level == 1 else "lvl2"
            nav_parts.append(
                f'<a class="{cls}" href="#{html.escape(hid)}">{html.escape(title)}</a>'
            )

    page = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Curso NUCLEO-F303RE — entrega 1</title>
<style>{CSS}</style>
</head>
<body>
<aside id="sidebar">
  <h1>NUCLEO-F303RE</h1>
  <p>STM32F303RET6. Entrega 1: fuentes, índice y módulo 1.</p>
  <input id="filtro" type="search" placeholder="Filtrar el menú" aria-label="Filtrar el menú">
  <nav id="nav">
    {"".join(nav_parts)}
  </nav>
</aside>
<main>
  {"".join(articles)}
</main>
<div id="lightbox" role="dialog" aria-label="Imagen ampliada"><img id="zoom" alt=""></div>
<script>{JS}</script>
</body>
</html>
"""
    out = DOCS / "index.html"
    out.write_text(page, encoding="utf-8")
    print(out, out.stat().st_size)


if __name__ == "__main__":
    main()
