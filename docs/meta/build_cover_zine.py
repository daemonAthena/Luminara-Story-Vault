#!/usr/bin/env python3
"""
COVER LETTER ZINE — Cornell Integration Developer (CEMI)
Builds the cover letter as a single-page zine using the Girlframe
zine_template.py aesthetic. Run from this directory with the venv python.

Usage:
    .venv/bin/python build_cover_zine.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph, Spacer, HRFlowable, PageBreak

from zine_template import (select_style, style, esc, PINK, BLUE, VIOLET,
                           TEXT, MUTED, page_bg, ZinePage, DARK, PANEL,
                           HexColor as _HC)
from reportlab.platypus import BaseDocTemplate
from reportlab.lib.pagesizes import letter

# kill the CRT scanlines for this document
import zine_template
zine_template.CRT_SCANLINES = False

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover_zine.pdf")

story = []

# ---------- COVER / HEADER BLOCK ----------
story.append(Spacer(1, 0.35 * inch))
story.append(Paragraph("LILITH ATHENA", style("nm", fontName="Courier-Bold",
                                              fontSize=30, leading=34,
                                              textColor=PINK, alignment=1)))
story.append(Spacer(1, 6))
story.append(Paragraph("300 Rano Blvd, Apt 5, Vestal, NY &nbsp;|&nbsp; "
                       "lilith.arlette.athena@gmail.com",
                       style("ct", fontName="Courier", fontSize=8.5, leading=12,
                             textColor=MUTED, alignment=1)))
story.append(Spacer(1, 14))
story.append(HRFlowable(width="100%", thickness=1, color=VIOLET))
story.append(Spacer(1, 10))
story.append(Paragraph("APPLICATION &nbsp;//&nbsp; INTEGRATION DEVELOPER (CEMI)",
                       style("sub", fontName="Courier-Bold", fontSize=13,
                             leading=17, textColor=BLUE, alignment=1)))
story.append(Paragraph("Cornell University &nbsp;//&nbsp; Information Technology",
                       style("sub2", fontName="Courier", fontSize=10, leading=14,
                             textColor=TEXT, alignment=1)))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="40%", thickness=0.5, color=PINK, hAlign="CENTER"))
story.append(Spacer(1, 16))

BODY = style("body", fontName="Courier", fontSize=9, leading=12.5,
             textColor=TEXT, alignment=4, spaceAfter=7)

def para(t):
    story.append(Paragraph(t, BODY))

para("Dear Hiring Committee,")
para("I am applying for the <b>Integration Developer (CEMI)</b> position. I am a "
     "mathematician and software engineer with four years at Siemens Energy "
     "building and maintaining data extraction and pricing tools, and I live in "
     "Vestal, which means I can be on the Ithaca campus whenever the work calls "
     "for it.")
para("At Siemens Energy I develop AI-powered data extraction tools in Python and "
     "Snowflake SQL, and I own those tools through their full lifecycle: "
     "requirements, build, test, deploy, and the maintenance after. Every line "
     "goes into GitLab under version control, and my responsibility is that what "
     "ships is tested and maintainable. That is integration work in everything "
     "but the platform. Pulling data from one system, transforming it against "
     "requirements, and landing it where the business can use it is the core of "
     "this role, and it is what I do now.")
para("I should be direct about the gap: I have not worked with <b>Boomi</b> "
     "specifically. What I bring instead is the underlying skill the role is built "
     "on, which is translating functional requirements into technical solutions, "
     "plus Python, SQL, and the testing discipline that comes from building tools "
     "people depend on daily. I pick up platforms quickly. Reading a requirement "
     "and asking what it actually claims before writing any code is the harder "
     "habit, and I already have it.")
para("The mission alignment matters to me as much as the technical fit. I spent "
     "two years as president of Alfred University's LGBTQ+ Alliance, and Cornell's "
     "commitment to a culture of belonging across a community this diverse is the "
     "kind of environment where I do my best work. I am comfortable across "
     "technical and non-technical audiences, I work well independently and on a "
     "team, and I would give a two-year appointment the same care I would give a "
     "permanent one.")
para("I am eligible for remote work within the United States. I am local to the "
     "Ithaca area, and while I do not currently have reliable transportation for "
     "frequent travel, I can and will make the trip for scheduled meetings, "
     "training, and onboarding. Within my first months here I intend to invest in "
     "a vehicle, which would make regular campus presence straightforward.")
story.append(Spacer(1, 6))
para("Sincerely,")
story.append(Paragraph("Lilith Athena", style("sig", fontName="Courier-Bold",
                                              fontSize=10, leading=13,
                                              textColor=PINK)))

# ---------- BUILD ----------
doc = BaseDocTemplate(OUTPUT, pagesize=letter,
                      title="Cover Letter — Cornell Integration Developer (CEMI)",
                      author="Lilith Athena")
doc.addPageTemplates([ZinePage(doc)])
doc.build(story)

from pypdf import PdfReader
n = len(PdfReader(OUTPUT).pages)
print(f"built {OUTPUT} | pages: {n} | bytes: {os.path.getsize(OUTPUT)}")
