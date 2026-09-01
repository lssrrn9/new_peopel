"""Motor de maquetación para el curso YASKAWA SERVOPACK.

Encapsula la identidad visual (paleta, tipografías, rejilla) y expone
plantillas de diapositiva de alto nivel para que los módulos de contenido
sólo tengan que aportar el texto.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt
from lxml import etree


# --------------------------------------------------------------------------
# Identidad visual
# --------------------------------------------------------------------------

NAVY = RGBColor(0x0B, 0x25, 0x45)
NAVY_SOFT = RGBColor(0x14, 0x3A, 0x63)
BLUE = RGBColor(0x1B, 0x5E, 0xA8)
CYAN = RGBColor(0x00, 0xA9, 0xCE)
AMBER = RGBColor(0xE8, 0x9B, 0x1F)
RED = RGBColor(0xC0, 0x39, 0x2B)
GREEN = RGBColor(0x2E, 0x8B, 0x57)
GRAY = RGBColor(0x5A, 0x6B, 0x7B)
GRAY_LINE = RGBColor(0xD3, 0xDA, 0xE2)
LIGHT = RGBColor(0xF2, 0xF5, 0xF8)
LIGHT_BLUE = RGBColor(0xE4, 0xEE, 0xF7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x1C, 0x24, 0x30)

FONT_H = "Segoe UI Semibold"
FONT_B = "Segoe UI"
FONT_M = "Consolas"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

MARGIN = Inches(0.62)
BODY_TOP = Inches(1.62)
BODY_BOTTOM = Inches(6.92)
BODY_W = SLIDE_W - 2 * MARGIN
BODY_H = BODY_BOTTOM - BODY_TOP


def _clear_shadow(shape) -> None:
    """python-pptx no expone sombras: se eliminan a nivel XML."""
    spPr = shape._element.spPr
    for tag in ("a:effectLst", "a:effectDag"):
        for el in spPr.findall(qn(tag)):
            spPr.remove(el)
    spPr.append(etree.SubElement(spPr, qn("a:effectLst")))


def _bullet_char(paragraph, char: str, color: RGBColor, font: str = "Arial",
                 size_pct: int = 90) -> None:
    pPr = paragraph._p.get_or_add_pPr()
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum", "a:buFont", "a:buSzPct",
                "a:buClr"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    bu_clr = etree.SubElement(pPr, qn("a:buClr"))
    srgb = etree.SubElement(bu_clr, qn("a:srgbClr"))
    srgb.set("val", str(color))
    bu_sz = etree.SubElement(pPr, qn("a:buSzPct"))
    bu_sz.set("val", str(size_pct * 1000))
    bu_font = etree.SubElement(pPr, qn("a:buFont"))
    bu_font.set("typeface", font)
    bu_ch = etree.SubElement(pPr, qn("a:buChar"))
    bu_ch.set("char", char)


def _no_bullet(paragraph) -> None:
    pPr = paragraph._p.get_or_add_pPr()
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum", "a:buFont", "a:buSzPct",
                "a:buClr"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    etree.SubElement(pPr, qn("a:buNone"))


def _indent(paragraph, mar_l: Emu, hanging: Emu) -> None:
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set("marL", str(int(mar_l)))
    pPr.set("indent", str(-int(hanging)))


def write_runs(paragraph, text: str, size: Pt, color: RGBColor,
               font: str = FONT_B, bold: bool = False) -> None:
    """Escribe texto admitiendo **negrita** y `monoespaciado` en línea."""
    tokens: list[tuple[str, str]] = []
    buf = ""
    mode = "n"
    i = 0
    while i < len(text):
        if text.startswith("**", i):
            tokens.append((mode, buf))
            buf = ""
            mode = "n" if mode == "b" else "b"
            i += 2
            continue
        if text[i] == "`":
            tokens.append((mode, buf))
            buf = ""
            mode = "n" if mode == "m" else "m"
            i += 1
            continue
        buf += text[i]
        i += 1
    tokens.append((mode, buf))

    for kind, chunk in tokens:
        if not chunk:
            continue
        run = paragraph.add_run()
        run.text = chunk
        run.font.size = size
        run.font.bold = bold or kind == "b"
        run.font.color.rgb = color
        run.font.name = FONT_M if kind == "m" else font


@dataclass
class Card:
    head: str
    body: str
    tone: str = "blue"


TONES = {
    "blue": (LIGHT_BLUE, BLUE),
    "cyan": (RGBColor(0xE0, 0xF5, 0xFA), CYAN),
    "amber": (RGBColor(0xFD, 0xF2, 0xDC), AMBER),
    "red": (RGBColor(0xFA, 0xE6, 0xE3), RED),
    "green": (RGBColor(0xE4, 0xF2, 0xEA), GREEN),
    "gray": (LIGHT, GRAY),
}


class Deck:
    """Constructor de la presentación con plantillas reutilizables."""

    def __init__(self, footer: str) -> None:
        self.prs = Presentation()
        self.prs.slide_width = SLIDE_W
        self.prs.slide_height = SLIDE_H
        self.footer = footer
        self.module = ""
        self.outline: list[tuple[str, str, str]] = []  # (tipo, título, notas)

    # ---------------------------------------------------------------- utils
    def save(self, path: str) -> None:
        self.prs.save(path)

    def _blank(self):
        return self.prs.slides.add_slide(self.prs.slide_layouts[6])

    def _rect(self, slide, left, top, width, height, fill=None, line=None,
              line_w=Pt(1), shape=MSO_SHAPE.RECTANGLE, adj=None):
        sh = slide.shapes.add_shape(shape, int(left), int(top), int(width),
                                    int(height))
        if adj is not None:
            try:
                sh.adjustments[0] = adj
            except (IndexError, ValueError):
                pass
        if fill is None:
            sh.fill.background()
        else:
            sh.fill.solid()
            sh.fill.fore_color.rgb = fill
        if line is None:
            sh.line.fill.background()
        else:
            sh.line.color.rgb = line
            sh.line.width = line_w
        _clear_shadow(sh)
        sh.text_frame.word_wrap = True
        return sh

    def _text(self, slide, left, top, width, height, text, size=Pt(14),
              color=INK, bold=False, font=FONT_B, align=PP_ALIGN.LEFT,
              anchor=MSO_ANCHOR.TOP, spacing=1.0):
        box = slide.shapes.add_textbox(int(left), int(top), int(width),
                                       int(height))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = 0
        tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = anchor
        for i, line in enumerate(str(text).split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            p.line_spacing = spacing
            _no_bullet(p)
            write_runs(p, line, size, color, font=font, bold=bold)
        return box

    def _shape_text(self, shape, text, size=Pt(13), color=INK, bold=False,
                    align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE,
                    font=FONT_B, spacing=1.0, margin=Inches(0.12)):
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = margin
        tf.margin_top = tf.margin_bottom = Inches(0.06)
        tf.vertical_anchor = anchor
        lines = text.split("\n")
        for idx, line in enumerate(lines):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.alignment = align
            p.line_spacing = spacing
            _no_bullet(p)
            write_runs(p, line, size, color, font=font, bold=bold)
        return shape

    def _notes(self, slide, text: str) -> None:
        if not text:
            return
        slide.notes_slide.notes_text_frame.text = text.strip()

    # ------------------------------------------------------------ chrome
    def _chrome(self, slide, title: str, subtitle: str = "",
                tag: str | None = None):
        self._rect(slide, 0, 0, SLIDE_W, Inches(1.18), fill=NAVY)
        self._rect(slide, 0, Inches(1.18), SLIDE_W, Inches(0.045), fill=CYAN)
        t_w = BODY_W - Inches(2.3)
        self._text(slide, MARGIN, Inches(0.20), t_w, Inches(0.55), title,
                   size=Pt(25), color=WHITE, bold=True, font=FONT_H)
        if subtitle:
            self._text(slide, MARGIN, Inches(0.76), t_w, Inches(0.32),
                       subtitle, size=Pt(12.5),
                       color=RGBColor(0xA9, 0xC6, 0xE0))
        label = tag if tag is not None else self.module
        if label:
            self._text(slide, SLIDE_W - MARGIN - Inches(2.2), Inches(0.30),
                       Inches(2.2), Inches(0.3), label, size=Pt(11),
                       color=CYAN, align=PP_ALIGN.RIGHT, bold=True)
        n = len(self.prs.slides)
        self._text(slide, MARGIN, Inches(7.02), Inches(9.0), Inches(0.26),
                   self.footer, size=Pt(9), color=GRAY)
        self._text(slide, SLIDE_W - MARGIN - Inches(1.2), Inches(7.02),
                   Inches(1.2), Inches(0.26), str(n), size=Pt(9), color=GRAY,
                   align=PP_ALIGN.RIGHT)

    # ------------------------------------------------------------ plantillas
    def title_slide(self, title: str, subtitle: str, meta: Sequence[str],
                    notes: str = ""):
        slide = self._blank()
        self._rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=NAVY)
        self._rect(slide, 0, 0, Inches(0.42), SLIDE_H, fill=CYAN)
        self._rect(slide, Inches(8.4), 0, Inches(4.933), SLIDE_H,
                   fill=NAVY_SOFT)
        # Motivo gráfico: eje servo estilizado
        cx, cy = Inches(10.85), Inches(3.6)
        self._rect(slide, cx - Inches(1.55), cy - Inches(1.55), Inches(3.1),
                   Inches(3.1), fill=None, line=RGBColor(0x24, 0x55, 0x84),
                   line_w=Pt(1.25), shape=MSO_SHAPE.OVAL)
        self._rect(slide, cx - Inches(1.1), cy - Inches(1.1), Inches(2.2),
                   Inches(2.2), fill=None, line=CYAN, line_w=Pt(2.5),
                   shape=MSO_SHAPE.OVAL)
        self._rect(slide, cx - Inches(0.42), cy - Inches(0.42), Inches(0.84),
                   Inches(0.84), fill=CYAN, shape=MSO_SHAPE.OVAL)
        self._rect(slide, cx - Inches(0.09), cy - Inches(2.55), Inches(0.18),
                   Inches(1.1), fill=AMBER)
        self._text(slide, Inches(9.15), Inches(5.55), Inches(3.5),
                   Inches(0.4), "SGD7S-200A  +  SGM7A-30A", size=Pt(13),
                   color=WHITE, bold=True, align=PP_ALIGN.CENTER,
                   font=FONT_M)
        self._text(slide, Inches(9.15), Inches(5.95), Inches(3.5),
                   Inches(0.4), "3,0 kW / 200 VCA trifásico", size=Pt(11),
                   color=RGBColor(0xA9, 0xC6, 0xE0), align=PP_ALIGN.CENTER)

        self._rect(slide, Inches(1.05), Inches(1.55), Inches(1.9),
                   Inches(0.34), fill=AMBER)
        self._text(slide, Inches(1.05), Inches(1.61), Inches(1.9),
                   Inches(0.3), "CURSO TÉCNICO", size=Pt(11), color=NAVY,
                   bold=True, align=PP_ALIGN.CENTER)
        self._text(slide, Inches(1.05), Inches(2.15), Inches(6.9),
                   Inches(2.0), title, size=Pt(40), color=WHITE, bold=True,
                   font=FONT_H, spacing=1.05)
        self._rect(slide, Inches(1.05), Inches(4.30), Inches(1.4),
                   Inches(0.05), fill=CYAN)
        self._text(slide, Inches(1.05), Inches(4.60), Inches(6.9),
                   Inches(0.9), subtitle, size=Pt(16),
                   color=RGBColor(0xC9, 0xDC, 0xEE), spacing=1.15)
        top = Inches(5.75)
        for line in meta:
            self._text(slide, Inches(1.05), top, Inches(6.9), Inches(0.3),
                       line, size=Pt(11.5), color=RGBColor(0x8F, 0xB2, 0xD1))
            top += Inches(0.30)
        self._notes(slide, notes)
        self.outline.append(("Portada", title, notes))
        return slide

    def section_slide(self, number: str, title: str, points: Sequence[str],
                      duration: str = "", notes: str = ""):
        self.module = number
        slide = self._blank()
        self._rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=NAVY)
        self._rect(slide, 0, 0, Inches(0.42), SLIDE_H, fill=CYAN)
        self._text(slide, Inches(1.15), Inches(1.35), Inches(6.0),
                   Inches(1.2), number, size=Pt(58), color=NAVY_SOFT,
                   bold=True, font=FONT_H)
        self._text(slide, Inches(1.15), Inches(2.55), Inches(10.8),
                   Inches(1.3), title, size=Pt(34), color=WHITE, bold=True,
                   font=FONT_H, spacing=1.05)
        self._rect(slide, Inches(1.15), Inches(4.05), Inches(1.4),
                   Inches(0.05), fill=AMBER)
        top = Inches(4.45)
        for pt in points:
            self._rect(slide, Inches(1.15), top + Inches(0.085), Inches(0.1),
                       Inches(0.1), fill=CYAN)
            self._text(slide, Inches(1.45), top, Inches(10.2), Inches(0.32),
                       pt, size=Pt(13.5), color=RGBColor(0xC9, 0xDC, 0xEE))
            top += Inches(0.40)
        if duration:
            self._text(slide, Inches(1.15), Inches(6.75), Inches(8.0),
                       Inches(0.3), f"Duración orientativa: {duration}",
                       size=Pt(11), color=AMBER, bold=True)
        self._notes(slide, notes)
        self.outline.append(("Módulo", f"{number} — {title}", notes))
        return slide

    def bullets_slide(self, title: str, items: Sequence[str],
                      subtitle: str = "", notes: str = "",
                      callout: tuple[str, str, str] | None = None,
                      size: float = 14.5):
        """`items`: prefijos '- ' y '-- ' marcan los niveles 2 y 3."""
        slide = self._blank()
        self._chrome(slide, title, subtitle)
        width = BODY_W
        height = BODY_H
        if callout:
            height -= Inches(1.12)
        box = slide.shapes.add_textbox(MARGIN, BODY_TOP, width, height)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = 0
        tf.margin_top = tf.margin_bottom = 0
        size = self.fit_bullets(items, size, width / Inches(1),
                                height / Inches(1))
        self._fill_bullets(tf, items, size)
        if callout:
            self.callout(slide, MARGIN, BODY_BOTTOM - Inches(0.95), BODY_W,
                         Inches(0.95), *callout)
        self._notes(slide, notes)
        self.outline.append(("Diapositiva", title, notes))
        return slide

    # Métrica aproximada de Segoe UI para estimar el alto de un bloque de
    # viñetas: permite reducir el cuerpo de letra antes de que el texto se
    # salga de la diapositiva.
    _LEVEL_INDENT_IN = (0.30, 0.62, 0.95)
    _LEVEL_SIZE_OFF = (0.0, 1.5, 2.5)
    _LEVEL_SPACE_PT = (9.0, 5.0, 4.0)
    _CHAR_WIDTH_EM = 0.52

    @classmethod
    def _bullets_height_pt(cls, items: Sequence[str], size: float,
                           width_in: float) -> float:
        total = 0.0
        for raw in items:
            level = 0
            text = raw
            while text.startswith("- "):
                level += 1
                text = text[2:]
            level = min(level, 2)
            plain = text.replace("**", "").replace("`", "").lstrip("#").strip()
            if not plain:
                total += 8.0
                continue
            if text.startswith("#"):
                fsize = size - 0.5
                indent = cls._LEVEL_INDENT_IN[level] - 0.30
                total += 8.0
            else:
                fsize = size - cls._LEVEL_SIZE_OFF[level]
                indent = cls._LEVEL_INDENT_IN[level]
            usable_pt = max((width_in - indent), 0.8) * 72.0
            per_line = max(int(usable_pt / (cls._CHAR_WIDTH_EM * fsize)), 8)
            lines = max(1, -(-len(plain) // per_line))
            total += lines * fsize * 1.06 * 1.21
            total += cls._LEVEL_SPACE_PT[level]
        return total

    @classmethod
    def fit_bullets(cls, items: Sequence[str], size: float, width_in: float,
                    height_in: float, minimum: float = 9.0) -> float:
        """Reduce el cuerpo de letra hasta que el bloque quepa en la caja."""
        limit = height_in * 72.0
        candidate = size
        while candidate > minimum:
            if cls._bullets_height_pt(items, candidate, width_in) <= limit:
                return candidate
            candidate -= 0.25
        return minimum

    def _fill_bullets(self, tf, items: Sequence[str], size: float = 14.5,
                      first: bool = True) -> None:
        specs = {
            0: (Inches(0.30), Pt(size), INK, "■", BLUE, Pt(9), True),
            1: (Inches(0.62), Pt(size - 1.5), RGBColor(0x33, 0x3F, 0x4C),
                "▸", CYAN, Pt(5), False),
            2: (Inches(0.95), Pt(size - 2.5), GRAY, "–", GRAY, Pt(4), False),
        }
        idx = 0
        for raw in items:
            level = 0
            text = raw
            while text.startswith("- "):
                level += 1
                text = text[2:]
            level = min(level, 2)
            mar, fsize, color, char, bcolor, space, bold = specs[level]
            p = tf.paragraphs[0] if (first and idx == 0) else tf.add_paragraph()
            p.space_after = space
            p.line_spacing = 1.06
            if text.startswith("#"):  # encabezado interno sin viñeta
                _no_bullet(p)
                _indent(p, mar - Inches(0.30), Emu(0))
                p.space_before = Pt(8) if idx else Pt(0)
                write_runs(p, text[1:].strip(), Pt(size - 0.5), BLUE,
                           font=FONT_H, bold=True)
            elif not text.strip():
                _no_bullet(p)
                write_runs(p, " ", Pt(6), INK)
            else:
                _bullet_char(p, char, bcolor)
                _indent(p, mar, Inches(0.22))
                write_runs(p, text, fsize, color, bold=bold)
            idx += 1

    def two_col_slide(self, title: str, left: tuple[str, Sequence[str]],
                      right: tuple[str, Sequence[str]], subtitle: str = "",
                      notes: str = "", tones: tuple[str, str] = ("blue", "cyan"),
                      size: float = 13.5,
                      callout: tuple[str, str, str] | None = None):
        slide = self._blank()
        self._chrome(slide, title, subtitle)
        gap = Inches(0.34)
        col_w = (BODY_W - gap) / 2
        height = BODY_H - (Inches(1.12) if callout else Emu(0))
        for i, ((head, items), tone) in enumerate(zip((left, right), tones)):
            x = MARGIN + i * (col_w + gap)
            bg, accent = TONES[tone]
            self._rect(slide, x, BODY_TOP, col_w, height, fill=LIGHT,
                       line=GRAY_LINE)
            self._rect(slide, x, BODY_TOP, col_w, Inches(0.46), fill=accent)
            self._text(slide, x + Inches(0.22), BODY_TOP + Inches(0.11),
                       col_w - Inches(0.4), Inches(0.3), head, size=Pt(13.5),
                       color=WHITE, bold=True, font=FONT_H)
            box_w = col_w - Inches(0.44)
            box_h = height - Inches(0.8)
            box = slide.shapes.add_textbox(x + Inches(0.22),
                                           BODY_TOP + Inches(0.62),
                                           box_w, box_h)
            tf = box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = 0
            tf.margin_top = tf.margin_bottom = 0
            self._fill_bullets(tf, items,
                               self.fit_bullets(items, size,
                                                box_w / Inches(1),
                                                box_h / Inches(1)))
        if callout:
            self.callout(slide, MARGIN, BODY_BOTTOM - Inches(0.95), BODY_W,
                         Inches(0.95), *callout)
        self._notes(slide, notes)
        self.outline.append(("Diapositiva", title, notes))
        return slide

    def cards_slide(self, title: str, cards: Sequence[Card],
                    subtitle: str = "", notes: str = "", columns: int = 3,
                    intro: str = "", body_size: float = 12.0):
        slide = self._blank()
        self._chrome(slide, title, subtitle)
        top = BODY_TOP
        if intro:
            self._text(slide, MARGIN, top, BODY_W, Inches(0.4), intro,
                       size=Pt(13.5), color=GRAY)
            top += Inches(0.52)
        gap = Inches(0.28)
        rows = (len(cards) + columns - 1) // columns
        card_w = (BODY_W - gap * (columns - 1)) / columns
        card_h = (BODY_BOTTOM - top - gap * (rows - 1)) / rows
        for i, card in enumerate(cards):
            r, c = divmod(i, columns)
            x = MARGIN + c * (card_w + gap)
            y = top + r * (card_h + gap)
            bg, accent = TONES[card.tone]
            self._rect(slide, x, y, card_w, card_h, fill=bg, line=accent,
                       line_w=Pt(0.75))
            self._rect(slide, x, y, Inches(0.055), card_h, fill=accent)
            self._text(slide, x + Inches(0.28), y + Inches(0.20),
                       card_w - Inches(0.5), Inches(0.5), card.head,
                       size=Pt(14), color=NAVY, bold=True, font=FONT_H,
                       spacing=1.02)
            box = slide.shapes.add_textbox(x + Inches(0.28), y + Inches(0.78),
                                           card_w - Inches(0.5),
                                           card_h - Inches(0.95))
            tf = box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = 0
            tf.margin_top = tf.margin_bottom = 0
            for j, line in enumerate(card.body.split("\n")):
                p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
                p.space_after = Pt(4)
                p.line_spacing = 1.05
                _no_bullet(p)
                write_runs(p, line, Pt(body_size), RGBColor(0x2B, 0x36, 0x44))
        self._notes(slide, notes)
        self.outline.append(("Diapositiva", title, notes))
        return slide

    def steps_slide(self, title: str, steps: Sequence[tuple[str, str]],
                    subtitle: str = "", notes: str = "", intro: str = "",
                    callout: tuple[str, str, str] | None = None):
        slide = self._blank()
        self._chrome(slide, title, subtitle)
        top = BODY_TOP
        if intro:
            self._text(slide, MARGIN, top, BODY_W, Inches(0.4), intro,
                       size=Pt(13.5), color=GRAY)
            top += Inches(0.5)
        bottom = BODY_BOTTOM - (Inches(1.05) if callout else Emu(0))
        gap = Inches(0.12)
        n = len(steps)
        row_h = (bottom - top - gap * (n - 1)) / n
        for i, (head, body) in enumerate(steps):
            y = top + i * (row_h + gap)
            self._rect(slide, MARGIN, y, BODY_W, row_h, fill=LIGHT,
                       line=GRAY_LINE, line_w=Pt(0.75))
            self._rect(slide, MARGIN, y, Inches(0.72), row_h, fill=NAVY)
            self._text(slide, MARGIN, y, Inches(0.72), row_h, str(i + 1),
                       size=Pt(20), color=CYAN, bold=True, font=FONT_H,
                       align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            has_body = bool(body)
            self._text(slide, MARGIN + Inches(0.95),
                       y + (Inches(0.12) if has_body else Emu(0)),
                       BODY_W - Inches(1.3),
                       row_h if not has_body else Inches(0.3), head,
                       size=Pt(13.5), color=NAVY, bold=True, font=FONT_H,
                       anchor=MSO_ANCHOR.TOP if has_body else MSO_ANCHOR.MIDDLE)
            if has_body:
                self._text(slide, MARGIN + Inches(0.95), y + Inches(0.44),
                           BODY_W - Inches(1.3), row_h - Inches(0.5), body,
                           size=Pt(11.5), color=RGBColor(0x3A, 0x46, 0x54),
                           spacing=1.05)
        if callout:
            self.callout(slide, MARGIN, BODY_BOTTOM - Inches(0.9), BODY_W,
                         Inches(0.9), *callout)
        self._notes(slide, notes)
        self.outline.append(("Diapositiva", title, notes))
        return slide

    def table_slide(self, title: str, headers: Sequence[str],
                    rows: Sequence[Sequence[str]], widths: Sequence[float],
                    subtitle: str = "", notes: str = "", intro: str = "",
                    foot: str = "", size: float = 11.0,
                    align_center: Sequence[int] = ()):
        slide = self._blank()
        self._chrome(slide, title, subtitle)
        top = BODY_TOP
        if intro:
            self._text(slide, MARGIN, top, BODY_W, Inches(0.4), intro,
                       size=Pt(13), color=GRAY)
            top += Inches(0.48)
        bottom = BODY_BOTTOM - (Inches(0.42) if foot else Emu(0))
        self.table(slide, MARGIN, top, BODY_W, bottom - top, headers, rows,
                   widths, size=size, align_center=align_center)
        if foot:
            self._text(slide, MARGIN, bottom + Inches(0.10), BODY_W,
                       Inches(0.3), foot, size=Pt(10), color=GRAY)
        self._notes(slide, notes)
        self.outline.append(("Diapositiva", title, notes))
        return slide

    def table(self, slide, left, top, width, height, headers, rows, widths,
              size: float = 11.0, align_center: Sequence[int] = ()):
        n_rows = len(rows) + 1
        head_h = Inches(0.38)
        row_h = max(Inches(0.26), (height - head_h) / max(len(rows), 1))
        shape = slide.shapes.add_table(n_rows, len(headers), int(left),
                                       int(top), int(width),
                                       int(head_h + row_h * len(rows)))
        tbl = shape.table
        tbl.first_row = True
        tbl.horz_banding = False
        total = sum(widths)
        for i, w in enumerate(widths):
            tbl.columns[i].width = int(width * w / total)
        tbl.rows[0].height = int(head_h)
        for r in range(1, n_rows):
            tbl.rows[r].height = int(row_h)
        for c, head in enumerate(headers):
            cell = tbl.cell(0, c)
            self._cell(cell, head, size=size, color=WHITE, bold=True,
                       fill=NAVY,
                       align=PP_ALIGN.CENTER if c in align_center else PP_ALIGN.LEFT)
        for r, row in enumerate(rows, start=1):
            fill = WHITE if r % 2 else LIGHT
            for c, val in enumerate(row):
                cell = tbl.cell(r, c)
                self._cell(cell, str(val), size=size, color=INK, fill=fill,
                           align=PP_ALIGN.CENTER if c in align_center else PP_ALIGN.LEFT)
        return tbl

    def _cell(self, cell, text, size=11.0, color=INK, bold=False, fill=WHITE,
              align=PP_ALIGN.LEFT):
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill
        cell.margin_left = cell.margin_right = Inches(0.09)
        cell.margin_top = cell.margin_bottom = Inches(0.03)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        for i, line in enumerate(str(text).split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            p.line_spacing = 1.0
            _no_bullet(p)
            write_runs(p, line, Pt(size), color, bold=bold)

    def callout(self, slide, left, top, width, height, kind: str, head: str,
                body: str):
        bg, accent = TONES[kind]
        self._rect(slide, left, top, width, height, fill=bg, line=accent,
                   line_w=Pt(0.75))
        self._rect(slide, left, top, Inches(0.075), height, fill=accent)
        self._text(slide, left + Inches(0.30), top + Inches(0.15),
                   width - Inches(0.55), Inches(0.28), head, size=Pt(12),
                   color=accent, bold=True, font=FONT_H)
        self._text(slide, left + Inches(0.30), top + Inches(0.45),
                   width - Inches(0.55), height - Inches(0.55), body,
                   size=Pt(11.5), color=RGBColor(0x2B, 0x36, 0x44),
                   spacing=1.06)

    def canvas_slide(self, title: str, subtitle: str = "", notes: str = ""):
        slide = self._blank()
        self._chrome(slide, title, subtitle)
        self.outline.append(("Diapositiva", title, notes))
        self._pending_notes = (slide, notes)
        self._notes(slide, notes)
        return slide

    def quote_slide(self, text: str, author: str = "", notes: str = ""):
        slide = self._blank()
        self._rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=NAVY)
        self._rect(slide, 0, 0, Inches(0.42), SLIDE_H, fill=AMBER)
        self._text(slide, Inches(1.5), Inches(2.4), Inches(10.3),
                   Inches(2.4), text, size=Pt(28), color=WHITE, bold=True,
                   font=FONT_H, spacing=1.2)
        if author:
            self._text(slide, Inches(1.5), Inches(5.1), Inches(10.3),
                       Inches(0.4), author, size=Pt(14), color=CYAN)
        self._notes(slide, notes)
        self.outline.append(("Cita", text[:60], notes))
        return slide

    # --------------------------------------------------------- primitivas
    def box(self, slide, left, top, width, height, text, fill, text_color=WHITE,
            size=12.0, bold=True, line=None, radius=0.12, mono=False,
            align=PP_ALIGN.CENTER):
        sh = self._rect(slide, left, top, width, height, fill=fill, line=line,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=radius)
        self._shape_text(sh, text, size=Pt(size), color=text_color, bold=bold,
                         align=align, font=FONT_M if mono else FONT_B,
                         margin=Inches(0.06))
        return sh

    def arrow(self, slide, left, top, width, height, color=BLUE,
              direction="right"):
        shape = {"right": MSO_SHAPE.RIGHT_ARROW, "down": MSO_SHAPE.DOWN_ARROW,
                 "left": MSO_SHAPE.LEFT_ARROW, "up": MSO_SHAPE.UP_ARROW}[direction]
        return self._rect(slide, left, top, width, height, fill=color,
                          shape=shape)

    def line(self, slide, x1, y1, x2, y2, color=GRAY, width=Pt(1.25),
             dash: bool = False):
        conn = slide.shapes.add_connector(1, int(x1), int(y1), int(x2), int(y2))
        conn.line.color.rgb = color
        conn.line.width = width
        if dash:
            ln = conn.line._get_or_add_ln()
            dash_el = etree.SubElement(ln, qn("a:prstDash"))
            dash_el.set("val", "dash")
        return conn

    def label(self, slide, left, top, width, text, size=10.5, color=GRAY,
              align=PP_ALIGN.CENTER, bold=False, mono=False):
        return self._text(slide, left, top, width, Inches(0.26), text,
                          size=Pt(size), color=color, align=align, bold=bold,
                          font=FONT_M if mono else FONT_B)
