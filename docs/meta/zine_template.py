#!/usr/bin/env python3
"""
GIRLFRAME ZINE TEMPLATE
=======================
ReportLab template: computer-terminal + trans-coded aesthetic.
Dark scanline background, pastel pink/blue/violet, monospace type,
double-border frame, stamped footer. Swap the `story` content for yours.

Usage:
    pip install reportlab pypdf
    python3 zine_template.py            # builds zine_output.pdf
    python3 zine_template.py myname.pdf # custom output path

Structure of this file:
    1. PALETTE + STYLES   - colors and text styles (tweak these first)
    2. PAGE DECORATION    - the background painter (scanlines, borders, footer)
    3. CONTENT            - the story; replace everything between the markers
    4. BUILD + VERIFY     - assembles and checks page count
"""
from typing import List, Any

from reportlab.graphics.shapes import String
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, HRFlowable, Table, TableStyle)
import sys

OUTPUT = sys.argv[1] if len(sys.argv) > 1 else "zine_output.pdf"

# ============================================================
# 1. PALETTE + STYLES
# ============================================================
# The aesthetic: CRT terminal darks + trans flag pastels.
#   DARK   - page background (near-black with violet tint)
#   PANEL  - slightly lighter, for table row stripes
#   PINK   - primary accent (headings, borders)  #ff7edb
#   BLUE   - secondary accent (subheads, borders) #7edbff
#   VIOLET - quotes and dividers                 #b8a1ff
#   TEXT   - body text (off-white)
#   MUTED  - footers, credits, small print
DARK    = HexColor("#12101a")
PANEL   = HexColor("#1c1828")
PINK    = HexColor("#ff7edb")
BLUE    = HexColor("#7edbff")
VIOLET  = HexColor("#b8a1ff")
TEXT    = HexColor("#e8e4f0")
MUTED   = HexColor("#9d94b8")

# Text styles. All Courier-family for the terminal feel.
# (If you want a softer body font, swap 'Courier' -> 'Helvetica' on st_body.)
def style(name, **kw):
    base = dict(fontName="Courier-Bold", fontSize=9.5, leading=14,
                textColor=TEXT, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(name, **base)

def select_style(name) -> ParagraphStyle:
    match name:
        case "title":
            return style("t", fontSize=34, leading=38, textColor=PINK, alignment=TA_CENTER)  # big cover title
        case "subtitle":
            return style("s", fontName="Courier", fontSize=12, leading=16, textColor=BLUE, alignment=TA_CENTER)  # cover subtitle
        case "heading":
            return style("h", fontSize=15, leading=18, textColor=PINK, spaceBefore=10, spaceAfter=4)  # page heading
        case "subheading":
            return style("h2", fontSize=11.5, leading=15, textColor=BLUE, spaceBefore=8, spaceAfter=3)  # sub-heading
        case "body":
            return style("b", fontName="Courier", alignment=TA_JUSTIFY, spaceAfter=5)  # body text
        case "quote":
            return style("q", fontName="Courier-BoldOblique", fontSize=10.5, leading=14, textColor=VIOLET, spaceAfter=6)  # pull quotes
        case "small":
            return style("sm", fontName="Courier", fontSize=8, leading=11, textColor=MUTED, spaceAfter=3)  # small print
        case "center":
            return style("c", alignment=TA_CENTER)

    return style("b", fontName="Courier", alignment=TA_JUSTIFY, spaceAfter=5)

def esc(t):
    """Escape XML specials for Paragraph markup."""
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# CRT scanlines on/off. Build scripts set this before importing page_bg
# or flip it at module level for the whole template.
CRT_SCANLINES = True

# ============================================================
# 2. PAGE DECORATION
# ============================================================
# Runs on EVERY page before flowables are drawn.
# - fills the dark background
# - draws CRT scanlines every 6pt
# - double border: thick pink outside, thin blue inside
# - stamps footer text + page number
def page_bg(cv, doc, footer_left="", show_pageno=True):
    cv.saveState()
    # background
    cv.setFillColor(DARK)
    cv.rect(0, 0, letter[0], letter[1], stroke=0, fill=1)
    # scanlines — CRT effect. Set CRT_SCANLINES=False in build scripts to disable.
    if CRT_SCANLINES:
        cv.setStrokeColor(HexColor("#1a1626"))
        cv.setLineWidth(0.5)
        for y in range(0, int(letter[1]), 6):
            cv.line(0, y, letter[0], y)
    # borders
    cv.setStrokeColor(PINK); cv.setLineWidth(1.5)
    cv.rect(0.4*inch, 0.4*inch, letter[0]-0.8*inch, letter[1]-0.8*inch)
    cv.setStrokeColor(BLUE); cv.setLineWidth(0.5)
    cv.rect(0.5*inch, 0.5*inch, letter[0]-1.0*inch, letter[1]-1.0*inch)
    # footer (optional; pass footer_left="" to suppress entirely)
    if footer_left or show_pageno:
        cv.setFont("Courier", 7); cv.setFillColor(MUTED)
        if footer_left:
            cv.drawString(0.62*inch, 0.28*inch, footer_left)
        if show_pageno:
            cv.drawRightString(letter[0]-0.62*inch, 0.28*inch, f"p{doc.page}")
    cv.restoreState()

# ============================================================
# 3. CONTENT  (replace everything between the markers)
# ============================================================
story = []
# ---- CONTENT START ----

# COVER PAGE
def add_cover_page(story:List[Any]=[],
                   title="T I T L E<br/>P A G E",
                   subtitle:str = "// subtitle //",
                   paragraphs:List[str]=["a zine about","whatever you love"]):
    story.append(Spacer(1, 1.7 * inch))
    story.append(Paragraph(title, select_style("title")))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(subtitle, select_style("subtitle")))
    story.append(Spacer(1, 0.45 * inch))
    story.append(HRFlowable(width="50%", thickness=1, color=VIOLET, hAlign="CENTER"))
    story.append(Spacer(1, 0.45 * inch))
    for p in paragraphs:
        story.append(Paragraph(p, select_style("subtitle")))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

add_cover_page(story)

# CONTENT PAGE SKELETON
story.append(Paragraph("PAGE HEADING", select_style("header")))
story.append(HRFlowable(width="100%", thickness=1, color=PINK))
story.append(Spacer(1, 8))
story.append(Paragraph("Body paragraph. Note that Paragraph() takes simple "
                       "markup: <b>bold</b>, <i>italic</i>, &lt;br/&gt; line breaks, "
                       "&amp; escaped entities.", select_style("body")))
story.append(Paragraph("A pull quote in violet italic.", select_style("quote")))
story.append(Paragraph("SUB-HEADING", select_style("header")))
story.append(Paragraph("More body text.", select_style("body")))
story.append(PageBreak())

# TABLE EXAMPLE (dark striped, pink header)
data = [
    [Paragraph("COL ONE", style("th", fontName="Courier-Bold", fontSize=8.8, textColor=white)),
     Paragraph("COL TWO", style("th2", fontName="Courier-Bold", fontSize=8.8, textColor=white))],
    [Paragraph("cell", select_style("small")), Paragraph("cell", select_style("small"))],
    [Paragraph("cell", select_style("small")), Paragraph("cell", select_style("small"))],
]
avail = letter[0] - 1.4*inch
t = Table(data, colWidths=[avail/2]*2)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), PINK),                       # header row pink
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [DARK, PANEL]),         # zebra stripes
    ("GRID", (0,0), (-1,-1), 0.5, BLUE),                       # blue grid lines
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
]))
story.append(t)
story.append(Spacer(1, 8))
story.append(Paragraph("credits . small print", select_style("small")))

# ---- CONTENT END ----

# ---- BUILD FUNCTIONS ----


# ============================================================
# 4. BUILD + VERIFY
# ============================================================
class ZinePage(PageTemplate):
    def __init__(self, doc):
        # content frame: generous margins so text clears the border
        f = Frame(0.7*inch, 0.6*inch, letter[0]-1.4*inch, letter[1]-1.2*inch, id="z")
        super().__init__(id="Zine", frames=[f],
                         onPage=lambda cv, d: page_bg(cv, d, footer_left="",
                                                      show_pageno=False))

doc = BaseDocTemplate(OUTPUT, pagesize=letter,
                      title="Girlframe Zine", author="aelwen")
doc.addPageTemplates([ZinePage(doc)])
doc.build(story)

# verify
from pypdf import PdfReader
n = len(PdfReader(OUTPUT).pages)
print(f"built {OUTPUT} | pages: {n}")
