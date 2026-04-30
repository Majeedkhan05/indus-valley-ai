"""
Indus Valley AI — Project Report Generator
Author: Claude (Anthropic) for Mohammed Majeed Khan, AI Hub, Mahindra University
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.colors import HexColor
import os

OUTPUT = "/Users/majeedkhan2005/Desktop/majeedkhanwebsite/indus-valley/Indus_Valley_AI_Project_Report.pdf"

# ── Palette ──────────────────────────────────────────────────────────────────
CHARCOAL   = HexColor("#0F0F0F")
DARK_BG    = HexColor("#1A1714")
GOLD       = HexColor("#D4AF37")
GOLD_SOFT  = HexColor("#C2A878")
TERRACOTTA = HexColor("#B55530")
OFF_WHITE  = HexColor("#F5F0E8")
MID_GRAY   = HexColor("#888888")
LIGHT_GRAY = HexColor("#DDDDDD")
WHITE      = colors.white
BLACK      = colors.black

# ── Custom canvas (header/footer on every page) ──────────────────────────────
class ReportCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for page_num, state in enumerate(self._saved_page_states, 1):
            self.__dict__.update(state)
            self.draw_page_decorations(page_num, num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_num, total_pages):
        w, h = A4

        # Top gold bar
        self.setFillColor(GOLD)
        self.rect(0, h - 8*mm, w, 8*mm, fill=1, stroke=0)

        # Header text (skip cover)
        if page_num > 1:
            self.setFillColor(CHARCOAL)
            self.setFont("Helvetica-Bold", 7)
            self.drawString(20*mm, h - 5.5*mm, "INDUS VALLEY AI — PROJECT REPORT")
            self.setFont("Helvetica", 7)
            self.drawRightString(w - 20*mm, h - 5.5*mm, "AI Hub · Mahindra University")

        # Bottom line
        self.setStrokeColor(GOLD_SOFT)
        self.setLineWidth(0.5)
        self.line(20*mm, 14*mm, w - 20*mm, 14*mm)

        # Page number
        if page_num > 1:
            self.setFillColor(MID_GRAY)
            self.setFont("Helvetica", 8)
            self.drawCentredString(w / 2, 8*mm, f"Page {page_num} of {total_pages}")


# ── Styles ───────────────────────────────────────────────────────────────────
def make_styles():
    s = {}

    s['cover_title'] = ParagraphStyle(
        'cover_title', fontName='Helvetica-Bold', fontSize=34,
        textColor=GOLD, leading=42, alignment=TA_CENTER, spaceAfter=6
    )
    s['cover_sub'] = ParagraphStyle(
        'cover_sub', fontName='Helvetica', fontSize=15,
        textColor=OFF_WHITE, leading=22, alignment=TA_CENTER, spaceAfter=4
    )
    s['cover_meta'] = ParagraphStyle(
        'cover_meta', fontName='Helvetica', fontSize=10,
        textColor=GOLD_SOFT, leading=16, alignment=TA_CENTER
    )
    s['h1'] = ParagraphStyle(
        'h1', fontName='Helvetica-Bold', fontSize=20,
        textColor=GOLD, leading=26, spaceBefore=18, spaceAfter=6
    )
    s['h2'] = ParagraphStyle(
        'h2', fontName='Helvetica-Bold', fontSize=14,
        textColor=GOLD_SOFT, leading=18, spaceBefore=14, spaceAfter=4
    )
    s['h3'] = ParagraphStyle(
        'h3', fontName='Helvetica-Bold', fontSize=11,
        textColor=TERRACOTTA, leading=15, spaceBefore=10, spaceAfter=3
    )
    s['body'] = ParagraphStyle(
        'body', fontName='Helvetica', fontSize=10,
        textColor=HexColor("#222222"), leading=16, alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    s['bullet'] = ParagraphStyle(
        'bullet', fontName='Helvetica', fontSize=10,
        textColor=HexColor("#222222"), leading=16, leftIndent=14,
        bulletIndent=0, spaceAfter=3
    )
    s['code'] = ParagraphStyle(
        'code', fontName='Courier', fontSize=8.5,
        textColor=HexColor("#111111"), leading=13, leftIndent=10,
        rightIndent=10, backColor=HexColor("#F3F0E8"), spaceAfter=8,
        borderPadding=(6, 8, 6, 8)
    )
    s['caption'] = ParagraphStyle(
        'caption', fontName='Helvetica-Oblique', fontSize=8.5,
        textColor=MID_GRAY, leading=12, alignment=TA_CENTER, spaceAfter=8
    )
    s['label'] = ParagraphStyle(
        'label', fontName='Helvetica-Bold', fontSize=9,
        textColor=CHARCOAL, leading=13
    )
    s['value'] = ParagraphStyle(
        'value', fontName='Helvetica', fontSize=9,
        textColor=HexColor("#333333"), leading=13
    )
    s['toc_entry'] = ParagraphStyle(
        'toc_entry', fontName='Helvetica', fontSize=11,
        textColor=HexColor("#222222"), leading=20, leftIndent=10
    )
    s['toc_num'] = ParagraphStyle(
        'toc_num', fontName='Helvetica-Bold', fontSize=11,
        textColor=GOLD, leading=20
    )
    return s

# ── Gold divider ─────────────────────────────────────────────────────────────
def divider(color=GOLD_SOFT, width=1):
    return HRFlowable(width="100%", thickness=width, color=color,
                      spaceAfter=6, spaceBefore=6)

# ── Highlighted box ──────────────────────────────────────────────────────────
def info_box(text, S):
    data = [[Paragraph(text, S['body'])]]
    t = Table(data, colWidths=[165*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#FBF6E8")),
        ('BOX', (0,0), (-1,-1), 0.8, GOLD_SOFT),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

# ── Key-value table ──────────────────────────────────────────────────────────
def kv_table(rows, S, col1=55*mm, col2=110*mm):
    data = [[Paragraph(k, S['label']), Paragraph(v, S['value'])] for k, v in rows]
    t = Table(data, colWidths=[col1, col2])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), HexColor("#F5F0E8")),
        ('BACKGROUND', (1,0), (1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('INNERGRID', (0,0), (-1,-1), 0.3, LIGHT_GRAY),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return t

# ── Two-column table ─────────────────────────────────────────────────────────
def two_col(left_items, right_items, S):
    max_r = max(len(left_items), len(right_items))
    left_items  += [''] * (max_r - len(left_items))
    right_items += [''] * (max_r - len(right_items))
    data = [
        [Paragraph(f"• {l}", S['bullet']), Paragraph(f"• {r}", S['bullet'])]
        for l, r in zip(left_items, right_items)
    ]
    t = Table(data, colWidths=[82*mm, 82*mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    return t

# ── File-entry row ───────────────────────────────────────────────────────────
def file_row(filename, size, S):
    data = [[
        Paragraph(filename, ParagraphStyle('fn', fontName='Courier-Bold', fontSize=9, textColor=CHARCOAL, leading=13)),
        Paragraph(size, ParagraphStyle('fs', fontName='Helvetica', fontSize=9, textColor=MID_GRAY, leading=13))
    ]]
    t = Table(data, colWidths=[120*mm, 45*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#F0ECE0")),
        ('BOX', (0,0), (-1,-1), 0.5, GOLD_SOFT),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    return t

# ═══════════════════════════════════════════════════════════════════════════
#  BUILD
# ═══════════════════════════════════════════════════════════════════════════
def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=22*mm, bottomMargin=22*mm,
        title="Indus Valley AI — Project Report",
        author="Mohammed Majeed Khan, AI Hub, Mahindra University",
        subject="Web-based AI platform for Indus Valley Civilization scholarship"
    )

    S = make_styles()
    story = []
    W = 165*mm  # usable width

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  COVER PAGE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Gold banner block
    cover_banner = Table(
        [[Paragraph("INDUS VALLEY AI", S['cover_title'])]],
        colWidths=[W]
    )
    cover_banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CHARCOAL),
        ('TOPPADDING', (0,0), (-1,-1), 22),
        ('BOTTOMPADDING', (0,0), (-1,-1), 18),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('BOX', (0,0), (-1,-1), 2, GOLD),
    ]))

    story.append(Spacer(1, 30*mm))
    story.append(cover_banner)
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("A Domain-Locked AI Platform for Harappan Scholarship", S['cover_sub']))
    story.append(Spacer(1, 2*mm))
    story.append(divider(GOLD, 1.5))
    story.append(Spacer(1, 6*mm))

    meta_table = Table([
        [Paragraph("Project Lead", S['label']),  Paragraph("Mohammed Majeed Khan", S['body'])],
        [Paragraph("Organization", S['label']),  Paragraph("AI Hub, Mahindra University, Hyderabad, India", S['body'])],
        [Paragraph("Category", S['label']),      Paragraph("Educational AI Web Application — Static, Zero-Cost, Privacy-First", S['body'])],
        [Paragraph("Date", S['label']),           Paragraph("April 2026", S['body'])],
        [Paragraph("Technology", S['label']),     Paragraph("Three.js · Gemini Nano · Canvas Vision · Vanilla JS · Python ReportLab", S['body'])],
        [Paragraph("Access", S['label']),         Paragraph("Open browser — no server, no API key, no account required", S['body'])],
    ], colWidths=[42*mm, 120*mm])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), HexColor("#F5F0E8")),
        ('BOX', (0,0), (-1,-1), 0.8, GOLD_SOFT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, LIGHT_GRAY),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10*mm))

    story.append(info_box(
        "This document is a complete technical and conceptual record of the Indus Valley AI project. "
        "It covers every file, every design decision, every technology layer — written plainly so that "
        "anyone from a professor to a first-year student can follow what was built and why.",
        S
    ))
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  TABLE OF CONTENTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("Table of Contents", S['h1']))
    story.append(divider())

    toc_items = [
        ("1", "Project Overview"),
        ("2", "What Makes This Different"),
        ("3", "How to Run the Website"),
        ("4", "Architecture — The Big Picture"),
        ("5", "File-by-File Walkthrough"),
        ("  5.1", "index.html — The Skeleton"),
        ("  5.2", "styles.css — The Design System"),
        ("  5.3", "knowledge-base.js — The Brain"),
        ("  5.4", "app.js — The Interactions Engine"),
        ("  5.5", "vision.js — The Eyes"),
        ("  5.6", "gemini-nano.js — On-Device LLM"),
        ("  5.7", "three-scene.js — Hero 3D Seal"),
        ("  5.8", "three-routes.js — 3D Trade Routes Globe"),
        ("  5.9", "data.js — Curated Dataset"),
        ("6", "The AI Chat System — Deep Dive"),
        ("7", "Canvas Vision — How Image Analysis Works"),
        ("8", "Gemini Nano — Free On-Device Intelligence"),
        ("9", "3D Graphics — Two WebGL Scenes"),
        ("10", "Design System & Visual Identity"),
        ("11", "Tech Stack Summary Table"),
        ("12", "What We Built vs What Others Do"),
        ("13", "Future Directions"),
        ("14", "Conclusion"),
    ]
    for num, title in toc_items:
        row = Table([[
            Paragraph(num, S['toc_num']),
            Paragraph(title, S['toc_entry'])
        ]], colWidths=[16*mm, 145*mm])
        row.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        story.append(row)

    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  1. PROJECT OVERVIEW
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("1. Project Overview", S['h1']))
    story.append(divider())

    story.append(Paragraph(
        "Indus Valley AI is a fully browser-based, zero-cost, zero-backend educational platform dedicated "
        "entirely to the Indus Valley / Harappan Civilization (c. 3300–1300 BCE). The project was built "
        "from scratch as a flagship demonstration of what modern web technology can achieve without any "
        "server infrastructure, paid APIs, or cloud fees.",
        S['body']
    ))
    story.append(Paragraph(
        "Everything runs inside the user's own browser tab. The AI chat answers questions from a hand-curated "
        "knowledge base of 49 scholarly topics. When available, an on-device language model (Gemini Nano, "
        "built into Chrome) silently enriches answers — entirely on the user's device, with no data leaving "
        "their machine. Two real-time 3D scenes render using WebGL. Image analysis runs on a pixel-level "
        "canvas algorithm with no external vision API.",
        S['body']
    ))
    story.append(Paragraph(
        "The platform was designed for three audiences: (a) the general public curious about the Indus Civilization, "
        "(b) students doing research, and (c) professors and archaeologists who want a rigorous, academically "
        "honest reference tool. Every answer is domain-locked — the system refuses to answer questions outside "
        "the Indus/Harappan domain, keeping the experience focused and trustworthy.",
        S['body']
    ))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("At a Glance", S['h2']))
    story.append(kv_table([
        ("Website type",    "Static HTML/CSS/JS — no server needed"),
        ("Backend",         "None. Zero. Everything runs in the browser."),
        ("AI model",        "Hand-built KB (49 topics) + optional Gemini Nano on-device"),
        ("3D engine",       "Three.js 0.160 — two full WebGL scenes"),
        ("Vision",          "Canvas pixel analysis — no camera API, no vision API"),
        ("Database",        "None — all data is in JS files loaded at page open"),
        ("Cost to run",     "USD $0.00 — host on GitHub Pages or any static host"),
        ("Domain coverage", "Indus Valley Civilization only — strict domain lock"),
        ("Seals dataset",   "12 real Harappan seal photographs from published corpus"),
        ("Lines of code",   "~7,000 lines across HTML, CSS, JS (all hand-written)"),
    ], S))

    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  2. WHAT MAKES THIS DIFFERENT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("2. What Makes This Different", S['h1']))
    story.append(divider())

    story.append(Paragraph(
        "Most AI chatbots are general-purpose — they will answer questions about cooking, sports, and software "
        "in the same breath as archaeology. That makes them unreliable for scholarship. Indus Valley AI is the "
        "opposite: it is hard-locked to one domain and academically honest within it.",
        S['body']
    ))

    story.append(Spacer(1, 3*mm))
    diff_data = [
        [
            Paragraph("Feature", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=10, textColor=WHITE, leading=14)),
            Paragraph("Indus Valley AI", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=10, textColor=WHITE, leading=14)),
            Paragraph("Typical AI chatbot", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=10, textColor=WHITE, leading=14)),
        ],
        [Paragraph("Domain", S['body']), Paragraph("Indus Civilization only", S['body']), Paragraph("Everything — unfocused", S['body'])],
        [Paragraph("API cost", S['body']), Paragraph("$0 forever", S['body']), Paragraph("$5–$100+/month", S['body'])],
        [Paragraph("Privacy", S['body']), Paragraph("100% — nothing sent to any server", S['body']), Paragraph("Data goes to cloud", S['body'])],
        [Paragraph("3D visuals", S['body']), Paragraph("Two live WebGL scenes", S['body']), Paragraph("None", S['body'])],
        [Paragraph("Image analysis", S['body']), Paragraph("Client-side canvas heuristics", S['body']), Paragraph("Requires paid vision API", S['body'])],
        [Paragraph("On-device LLM", S['body']), Paragraph("Gemini Nano (Chrome built-in)", S['body']), Paragraph("Cloud model required", S['body'])],
        [Paragraph("Academic honesty", S['body']), Paragraph("Flags debates, cites scholars by name", S['body']), Paragraph("May hallucinate", S['body'])],
        [Paragraph("Hosting", S['body']), Paragraph("Any static host (GitHub Pages = free)", S['body']), Paragraph("Needs server + DB", S['body'])],
        [Paragraph("Offline use", S['body']), Paragraph("Yes — after first load", S['body']), Paragraph("No", S['body'])],
    ]
    diff_table = Table(diff_data, colWidths=[50*mm, 58*mm, 55*mm])
    diff_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), CHARCOAL),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor("#FAFAFA"), HexColor("#F5F0E8")]),
        ('BOX', (0,0), (-1,-1), 0.8, GOLD_SOFT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, LIGHT_GRAY),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(diff_table)
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  3. HOW TO RUN
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("3. How to Run the Website", S['h1']))
    story.append(divider())

    story.append(Paragraph(
        "Because the site uses ES Modules (modern JavaScript imports), it must be served over HTTP — "
        "it cannot simply be opened as a file:// URL. The simplest method is Python's built-in web server, "
        "which is available on every Mac and most Linux machines.",
        S['body']
    ))

    story.append(Paragraph("Step-by-step instructions (macOS / Linux)", S['h2']))
    steps = [
        ("Step 1 — Open Terminal", "Press Cmd+Space, type Terminal, press Enter."),
        ("Step 2 — Navigate to the folder",
         "cd ~/Desktop/majeedkhanwebsite/indus-valley"),
        ("Step 3 — Start the server",
         "python3 -m http.server 8000"),
        ("Step 4 — Open the browser",
         "Open Chrome or Safari. Go to:  http://localhost:8000"),
        ("Step 5 — Stop the server",
         "When done, go back to Terminal and press Ctrl+C."),
    ]
    for step, detail in steps:
        story.append(Paragraph(f"<b>{step}</b>", S['h3']))
        story.append(Paragraph(detail, ParagraphStyle(
            'step_code', fontName='Courier', fontSize=9.5, leading=15,
            textColor=CHARCOAL, backColor=HexColor("#F3F0E8"),
            leftIndent=8, rightIndent=8, borderPadding=(5,8,5,8),
            spaceAfter=6
        )))

    story.append(Spacer(1, 3*mm))
    story.append(info_box(
        "Tip for Gemini Nano: The on-device LLM feature only works in Google Chrome 127 or newer, "
        "with the Gemini Nano flag enabled in chrome://flags. The rest of the site works perfectly "
        "in any modern browser — Firefox, Safari, Edge — without it.",
        S
    ))
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  4. ARCHITECTURE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("4. Architecture — The Big Picture", S['h1']))
    story.append(divider())

    story.append(Paragraph(
        "The project follows a single-page application (SPA) pattern implemented entirely with vanilla "
        "JavaScript — no React, no Vue, no build system, no Node.js. This was a deliberate choice: "
        "zero dependencies means zero security vulnerabilities from third-party packages, and the project "
        "will still work correctly in 10 years without any updates.",
        S['body']
    ))

    story.append(Paragraph("Script Load Order", S['h2']))
    story.append(Paragraph(
        "Scripts are loaded in a specific order inside index.html. Each script adds its module to the "
        "window object so later scripts can use it:",
        S['body']
    ))

    load_order = [
        ("1", "knowledge-base.js", "window.IVA_KB", "The 49-topic scholarly knowledge base — must load first"),
        ("2", "data.js", "window.IVA_DATA", "Seals, cities, motifs, script glyphs dataset"),
        ("3", "vision.js", "window.IVA_VISION", "Canvas pixel analysis for image uploads"),
        ("4", "gemini-nano.js", "window.IVA_NANO", "On-device Gemini Nano detection and session"),
        ("5", "three-scene.js", "module", "Three.js hero 3D seal (ES module, own scope)"),
        ("6", "three-routes.js", "module", "Three.js trade routes globe (ES module)"),
        ("7", "app.js", "IIFE", "All UI interactions — reads everything above"),
    ]
    lo_data = [[
        Paragraph("#", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=13)),
        Paragraph("File", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=13)),
        Paragraph("Exports", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=13)),
        Paragraph("Role", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=13)),
    ]] + [
        [Paragraph(n, S['body']),
         Paragraph(f, ParagraphStyle('fc', fontName='Courier-Bold', fontSize=8.5, leading=13)),
         Paragraph(e, ParagraphStyle('fc', fontName='Courier', fontSize=8.5, leading=13)),
         Paragraph(r, S['body'])]
        for n, f, e, r in load_order
    ]
    lo_table = Table(lo_data, colWidths=[8*mm, 35*mm, 28*mm, 92*mm])
    lo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, HexColor("#F5F0E8")]),
        ('BOX', (0,0), (-1,-1), 0.6, GOLD_SOFT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, LIGHT_GRAY),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(lo_table)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("Data Flow for a Chat Question", S['h2']))
    story.append(Paragraph(
        "When a user types a question and presses Send, the following happens in sequence — all inside "
        "the browser, in under one second:",
        S['body']
    ))
    flow_steps = [
        ("app.js receives the question text from the input field."),
        ("The domain gate checks: does the question contain any Indus-domain keywords? "
         "Does it match a hard out-of-scope pattern (bitcoin, recipe, etc.)?"),
        ("If in-domain: bestTopic() scores every KB topic by summing keyword match lengths. "
         "The highest-scoring topic wins."),
        ("The winning topic's title, paragraphs, and source citation are rendered into the chat as an "
         "HTML message bubble."),
        ("Asynchronously: maybeEnrich() checks if Gemini Nano is ready. If yes, it sends the question "
         "and the first paragraph of the KB answer to the on-device model and appends a green enrichment "
         "block when the response arrives."),
        ("If the user uploaded an image: vision.js analyzed it first and routed to the most relevant "
         "KB topic before step 2."),
    ]
    for i, step in enumerate(flow_steps, 1):
        story.append(Paragraph(f"<b>{i}.</b>  {step}", S['bullet']))
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  5. FILE-BY-FILE WALKTHROUGH
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("5. File-by-File Walkthrough", S['h1']))
    story.append(divider())

    story.append(Paragraph(
        "The project lives in one folder: indus-valley/. Here is every file and what it does.",
        S['body']
    ))

    files = [
        ("index.html",        "~34 KB", "Main page — all 12 sections, HTML skeleton"),
        ("styles.css",        "~45 KB", "Complete design system — 1,200+ lines of CSS"),
        ("knowledge-base.js", "~67 KB", "49 scholarly topics, domain gate, fallbacks"),
        ("app.js",            "~26 KB", "All UI — cursor, scroll, chat, upload, paths"),
        ("vision.js",         "~8 KB",  "Canvas image classifier — no API"),
        ("gemini-nano.js",    "~5 KB",  "On-device LLM bridge — Chrome only"),
        ("three-scene.js",    "~11 KB", "Three.js hero 3D seal animation"),
        ("three-routes.js",   "~9 KB",  "Three.js 3D trade routes globe"),
        ("data.js",           "~18 KB", "Seals, cities, motifs, script glyphs"),
        ("assets/seals/",     "~2 MB",  "12 real Harappan seal photographs (JPEG)"),
        ("assets/logo.png",   "user",   "AI Hub logo (user-supplied)"),
    ]
    for fname, fsize, fdesc in files:
        story.append(file_row(fname, fsize, S))
        story.append(Paragraph(fdesc, ParagraphStyle(
            'fdesc', fontName='Helvetica', fontSize=9.5, textColor=HexColor("#333333"),
            leading=14, leftIndent=4, spaceAfter=5
        )))

    story.append(Spacer(1, 4*mm))

    # 5.1
    story.append(Paragraph("5.1  index.html — The Skeleton", S['h2']))
    story.append(Paragraph(
        "The HTML file defines the visual structure of the entire page. It is a single long document with "
        "12 named sections that the browser scrolls through. Every interactive element has a data-* attribute "
        "so that app.js can find it without relying on fragile class names.",
        S['body']
    ))
    sections = [
        "Hero — full-viewport 3D canvas (the animated seal)",
        "Ticker — scrolling gold text band with civilization facts",
        "About — four key pillars of the Indus civilization",
        "AI Chat — the main AI interaction panel (centerpiece)",
        "Pillars — six achievement cards (urban planning, trade, etc.)",
        "Seal Gallery — 12 real seal photographs with modal zoom",
        "Cities — 10 excavated city cards (click for detail)",
        "Trade Routes — second 3D WebGL scene (the globe)",
        "Timeline — visual chronology from 7000 BCE to present",
        "Motifs — 8 recurring iconographic symbols",
        "Script — animated Indus sign strip",
        "Research — six academic reference links",
    ]
    for sec in sections:
        story.append(Paragraph(f"• {sec}", S['bullet']))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Key HTML features: importmap (tells the browser where to find Three.js from CDN), "
        "custom cursor divs (.cursor-dot, .cursor-ring), the spotlight gradient div, "
        "the scroll spine aside element with 10 named nodes, the drag-drop overlay, "
        "the hidden file input, the attachment preview box, and the Gemini Nano status badge.",
        S['body']
    ))

    # 5.2
    story.append(Paragraph("5.2  styles.css — The Design System", S['h2']))
    story.append(Paragraph(
        "The CSS file defines the complete visual language of the project. It uses CSS Custom Properties "
        "(variables) extensively so that the entire color palette can be changed from one block at the top.",
        S['body']
    ))
    story.append(Paragraph("Core design tokens:", S['h3']))
    tokens = [
        ("--bg", "#0F0F0F", "Page background — near-black charcoal"),
        ("--gold", "#D4AF37", "Primary accent — ancient gold"),
        ("--gold-soft", "#C2A878", "Secondary accent — warm bronze"),
        ("--terracotta", "#B55530", "Highlight accent — fired clay red"),
        ("--serif", "Cormorant Garamond", "Display typeface — elegant, historical"),
        ("--sans", "Inter", "Body typeface — clean, legible"),
        ("--mono", "JetBrains Mono", "Code typeface — technical sections"),
    ]
    tok_data = [[
        Paragraph("Variable", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=13)),
        Paragraph("Value", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=13)),
        Paragraph("Purpose", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=13)),
    ]] + [
        [Paragraph(v, ParagraphStyle('tok', fontName='Courier-Bold', fontSize=8.5, leading=13)),
         Paragraph(val, ParagraphStyle('tok', fontName='Courier', fontSize=8.5, leading=13)),
         Paragraph(p, S['body'])]
        for v, val, p in tokens
    ]
    tok_table = Table(tok_data, colWidths=[38*mm, 38*mm, 87*mm])
    tok_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, HexColor("#F5F0E8")]),
        ('BOX', (0,0), (-1,-1), 0.6, GOLD_SOFT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, LIGHT_GRAY),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tok_table)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Notable CSS techniques used:", S['h3']))
    css_techniques = [
        "Custom cursor — two pseudo-elements with different lag speeds (mix-blend-mode: difference makes it invert on hover)",
        "Spotlight — a radial gradient whose center follows the mouse via CSS custom properties --mx and --my updated in JavaScript",
        "Scroll spine — a fixed left sidebar with 10 labeled nodes; a .spine-fill bar uses scaleY() to show scroll progress",
        "Reveal animations — IntersectionObserver adds .in class; CSS transitions fire with opacity + scale (cubic-bezier timing)",
        "Magnetic buttons — pointermove listener computes offset from center and applies a CSS transform",
        "Drop zone — dashed gold pulsing border overlay that appears on file drag-enter",
        "Glass cards — backdrop-filter: blur() for frosted-glass seal cards",
        "Full-bleed 3D canvas — position:sticky + height:100vh so the WebGL scene scrolls with the page correctly",
    ]
    for t in css_techniques:
        story.append(Paragraph(f"• {t}", S['bullet']))

    story.append(PageBreak())

    # 5.3
    story.append(Paragraph("5.3  knowledge-base.js — The Brain", S['h2']))
    story.append(Paragraph(
        "This is the most important file — it is what makes the AI answers accurate and trustworthy. "
        "It contains 49 hand-curated scholarly topics, each written with care to reflect current archaeological "
        "consensus while flagging ongoing debates.",
        S['body']
    ))
    story.append(Paragraph("Structure of each topic:", S['h3']))
    story.append(Paragraph(
        "Every topic is a JavaScript object with four fields: keys (array of trigger phrases for matching), "
        "title (displayed heading), body (array of paragraphs — the actual answer), and sources (citation string). "
        "Example structure:",
        S['body']
    ))
    story.append(Paragraph(
        "{ keys: ['great bath', 'ritual bathing', 'mohenjo-daro bath'],\n"
        "  title: 'The Great Bath of Mohenjo-daro',\n"
        "  body: ['First paragraph...', 'Second paragraph...'],\n"
        "  sources: 'Marshall 1931; Jansen 1993' }",
        S['code']
    ))

    story.append(Paragraph("Coverage — all 49 topic categories:", S['h3']))
    topic_left = [
        "Civilization overview", "Chronology & phases", "Mohenjo-daro", "Harappa", "Dholavira",
        "Lothal — Bronze Age port", "Rakhigarhi", "Sutkagan-Dor", "Shortugai outpost",
        "Indus script — status", "Fish sign (most frequent)", "Parpola hypothesis", "Yajnadevam claim",
        "Seals — what they are", "Unicorn motif", "Seal manufacture", "Ernestite drill",
        "Terracotta figurines", "Priest-King statuette", "Dancing Girl bronze",
        "Daimabad bronzes", "Toys & games",
        "Brick technology", "Urban planning & drainage", "Great Bath",
    ]
    topic_right = [
        "Trade with Mesopotamia", "Meluhha (Mesopotamian name)", "Carnelian bead exports",
        "Copper & bronze metallurgy", "Pottery typology", "Weights & measures",
        "Indus religion & fire altars", "Why no kings debate", "Burials & mortuary",
        "Decline of the civilization", "4.2ka climate event", "Ghaggar-Hakra river",
        "Aryan migration context", "Rakhigarhi ancient DNA 2019", "Comparative: vs Mesopotamia",
        "Comparative: vs Egypt", "Archaeologist directory", "Motifs — pipal leaf",
        "Motifs — swastika", "Script glyphs & sign list", "Architecture",
        "Agriculture & diet", "Domain fallback", "Out-of-domain response",
        "(5 additional topics covering debates & schools)",
    ]
    story.append(two_col(topic_left, topic_right, S))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Domain gate — how out-of-scope questions are blocked:", S['h3']))
    story.append(Paragraph(
        "Two layers of protection. First, an inDomainKeywords array of ~80 Indus-related terms "
        "is checked against the question. Second, a regex pattern outOfScopeHard matches obvious "
        "non-Indus topics (bitcoin, cricket score, recipe, GPT-4, etc.) and blocks them regardless "
        "of other matches. If both checks fail AND no KB topic scores above the minimum threshold, "
        "the system returns a polite out-of-scope response.",
        S['body']
    ))

    story.append(PageBreak())

    # 5.4
    story.append(Paragraph("5.4  app.js — The Interactions Engine", S['h2']))
    story.append(Paragraph(
        "app.js is the conductor — it initializes all interactive features and wires them together. "
        "It is written as a single IIFE (Immediately Invoked Function Expression) so that all variables "
        "are scoped privately and nothing pollutes the global window object.",
        S['body']
    ))

    story.append(Paragraph("Major systems inside app.js:", S['h3']))
    systems = [
        ("Custom Cursor",
         "Two div elements (dot + ring) animate at different speeds using requestAnimationFrame. "
         "The dot follows the pointer at 30% speed; the ring follows at 12% — the lag creates "
         "a trailing effect. On touch devices (pointer:coarse), the cursor is hidden entirely."),
        ("Spotlight",
         "The mouse position is tracked via pointermove and written to CSS custom properties --mx and --my. "
         "A CSS radial-gradient centered at (--mx, --my) creates the glow effect with no canvas involved."),
        ("Magnetic Buttons",
         "On pointermove over certain buttons, the offset between the pointer and the button center "
         "is computed and applied as a CSS transform translation at 25% magnitude. The button "
         "snaps back when the pointer leaves."),
        ("Scroll Spine",
         "An IntersectionObserver tracks which section is nearest to the viewport center. "
         "The matching spine node gets the .active class. Clicking a spine node scrolls smoothly "
         "to that section. The spine fill bar's scaleY tracks overall scroll progress."),
        ("Reveal on Scroll",
         "A second IntersectionObserver watches all elements with the .reveal class. "
         "When they enter the viewport, the .in class is added and a CSS transition fires "
         "(opacity 0→1, scale 0.96→1, 800ms cubic-bezier easing)."),
        ("File Upload",
         "A hidden <input type=file> is triggered by a visible Attach button's click. "
         "On file selection, handleFile() asynchronously loads the file — images go to "
         "vision.js for pixel analysis, text files are read with FileReader. "
         "Drag-and-drop onto the window also triggers handleFile()."),
        ("Learning Paths",
         "Five curated learning sequences (Seals, Cities, Script, Trade, Decline) are "
         "pre-defined as ordered arrays of topic titles. Clicking a path button plays "
         "the topics in sequence with step badges and optional Gemini Nano enrichment."),
        ("Video Redirect",
         "The Video Gen button constructs a Veo-style prompt string based on the last "
         "topic discussed, then opens Google AI Studio in a new tab with the prompt "
         "pre-filled in the URL. No API key needed — the user's own Gemini quota is used."),
    ]
    for name, desc in systems:
        story.append(KeepTogether([
            Paragraph(name, S['h3']),
            Paragraph(desc, S['body']),
        ]))

    story.append(PageBreak())

    # 5.5
    story.append(Paragraph("5.5  vision.js — The Eyes", S['h2']))
    story.append(Paragraph(
        "vision.js provides image intelligence with zero API calls. When a user uploads an image, "
        "this module analyzes it on the client using HTML Canvas pixel data.",
        S['body']
    ))
    story.append(Paragraph("How it works (plain English):", S['h3']))
    vision_steps = [
        "The image is drawn onto a hidden 96×96 pixel canvas (tiny — fast to process).",
        "The raw pixel RGBA values are read with getImageData().",
        "Five statistics are computed from the pixel data: average brightness (0–255), "
        "sepia warmth score (how brown/cream the image is, 0–1), edge density (how sharp "
        "the outlines are), dominant hue (red/green/brown/gray/cool), and aspect ratio (width÷height).",
        "Edge density uses a lightweight Sobel approximation: for each pixel, compute the "
        "luminance gradient to the right and downward neighbor. Average all gradients, "
        "normalize to 0–1. Higher = more edges = more detailed / line-art like.",
        "Six classification rules run in order: seal (warm+square+photo), script (line-art+light+mono), "
        "map (green/brown-green hue), artifact (warm+photo), illustration (light+low-color), "
        "site-photo (photo+dark). The first matching rule wins.",
        "Each category maps to 2–3 suggested KB topic titles. The first title that "
        "exists in the KB is returned as the matched topic.",
        "The result is displayed to the user with all the raw statistics visible.",
    ]
    for i, step in enumerate(vision_steps, 1):
        story.append(Paragraph(f"<b>{i}.</b>  {step}", S['bullet']))

    story.append(Spacer(1, 3*mm))
    story.append(info_box(
        "Why not use a real computer vision API? Two reasons: (1) privacy — the user's image never "
        "leaves their device; (2) cost — zero. The heuristic approach works well for the expected "
        "inputs: seal photographs, script transcriptions, site maps, and figurine photos. "
        "For general photographs it gives a reasonable best-guess and falls back gracefully.",
        S
    ))

    # 5.6
    story.append(Paragraph("5.6  gemini-nano.js — On-Device LLM", S['h2']))
    story.append(Paragraph(
        "Gemini Nano is a small language model built directly into Google Chrome (version 127+). "
        "It runs on the user's GPU/CPU — no internet connection is used. gemini-nano.js is the "
        "bridge between the website and this model.",
        S['body']
    ))
    story.append(Paragraph("What it does:", S['h3']))
    nano_points = [
        "detect() — Checks if the browser supports window.LanguageModel (new API) or "
        "window.ai.languageModel (legacy API). Sets a badge on the chat panel showing the state: "
        "ready, downloading, or unsupported.",
        "ensureSession() — Creates a language model session lazily (only when first needed). "
        "Passes a system prompt that locks Gemini Nano to the Indus domain with the same "
        "academic honesty rules as the KB.",
        "ask(question, contextNote) — Sends the user's question plus the first paragraph of "
        "the KB answer as context. Asks the model to add one additional concise paragraph "
        "that does not repeat the KB content. Returns the text or null if unavailable.",
        "The enrichment paragraph is shown in a green block labeled 'Gemini Nano · on-device' "
        "at the bottom of the bot message.",
    ]
    for point in nano_points:
        story.append(Paragraph(f"• {point}", S['bullet']))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "The system prompt inside gemini-nano.js enforces: domain restriction to Indus topics, "
        "academic honesty (flag debates, name scholars), correct statement that the Indus script "
        "is undeciphered, correct Rakhigarhi 2019 ancient-DNA finding, and conciseness (under 200 words).",
        S['body']
    ))

    story.append(PageBreak())

    # 5.7
    story.append(Paragraph("5.7  three-scene.js — Hero 3D Seal", S['h2']))
    story.append(Paragraph(
        "The hero section shows a 3D animated Indus-style stamp seal. It is rendered using Three.js, "
        "a JavaScript library that wraps WebGL (the browser's 3D graphics API). Everything is "
        "procedurally generated — no external 3D model files are loaded.",
        S['body']
    ))
    story.append(Paragraph("What is in the scene:", S['h3']))
    scene_items = [
        "Seal body — a rounded rectangular block made with ExtrudeGeometry of a rounded Shape. "
        "Material: MeshStandardMaterial with gold color, moderate metalness, and emissive glow.",
        "Unicorn bull — the most iconic Indus motif. Built from a bezier path using THREE.Path "
        "commands that approximate the animal's outline. Extruded to give it depth.",
        "Horn mesh — a separate tapered CylinderGeometry attached to the animal's head.",
        "Manger / standard — a short rectangular object below the animal's mouth, "
        "common on real Indus unicorn seals.",
        "Script signs — a row of 7 small extruded glyphs representing Indus script signs, "
        "placed along the top of the seal face.",
        "Floating rings — two animated torus rings orbit the seal to add life.",
        "Gold dust particles — 600 Points (sprites) drift upward and reset, "
        "creating a shimmering golden atmosphere.",
        "Pointer parallax — the camera subtly tilts toward the mouse position for a "
        "3D depth illusion on desktop.",
        "IntersectionObserver — animation pauses automatically when the hero scrolls "
        "off screen to save GPU power.",
    ]
    for item in scene_items:
        story.append(Paragraph(f"• {item}", S['bullet']))

    # 5.8
    story.append(Paragraph("5.8  three-routes.js — 3D Trade Routes Globe", S['h2']))
    story.append(Paragraph(
        "A second Three.js scene shows the Indus trade network as glowing arcs over a "
        "stylized ancient world disc. Nine city nodes are placed at historically accurate "
        "relative positions.",
        S['body']
    ))
    story.append(Paragraph("Scene contents:", S['h3']))
    routes_items = [
        "Ground disc — a large CircleGeometry with concentric ring decorations, "
        "styled to look like an antique world map plate.",
        "City nodes — 9 sites (Indus, Sumer, Magan, Dilmun, Shortugai, Susa, Meluhha, "
        "Lothal, Dholavira) rendered as gold/terracotta pillars with glowing dot tops "
        "and pulsing halo rings.",
        "Trade route arcs — 8 QuadraticBezierCurve3 paths connecting the cities, "
        "rendered as TubeGeometry meshes with semi-transparent gold material.",
        "Travelling sparks — one SphereGeometry per route that travels along the "
        "Bezier curve at random speeds, representing goods in transit.",
        "Ambient gold dust — 240 floating Points particles drift upward.",
        "Slow camera orbit — the camera revolves around the scene using "
        "sin/cos of elapsed time, tilted by mouse position.",
    ]
    for item in routes_items:
        story.append(Paragraph(f"• {item}", S['bullet']))

    # 5.9
    story.append(Paragraph("5.9  data.js — Curated Dataset", S['h2']))
    story.append(Paragraph(
        "data.js provides three structured datasets that drive the visual sections of the page:",
        S['body']
    ))
    story.append(kv_table([
        ("seals[]",       "12 real seal photographs — each with id, filename, label, and tag (unicorn, zebu bull, elephant, etc.)"),
        ("cities[]",      "10 excavated cities — name, location, summary paragraph, stats chips (area, pop. estimate, key finds), and expanded detail bullet points"),
        ("motifs[]",      "8 recurring motifs — name, frequency, summary, SVG glyph path string, and detail paragraphs"),
        ("scriptGlyphs[]","16 SVG path strings representing stylized Indus signs for the animated script strip"),
    ], S))

    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  6. AI CHAT DEEP DIVE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("6. The AI Chat System — Deep Dive", S['h1']))
    story.append(divider())

    story.append(Paragraph(
        "The chat panel is the centerpiece of the project. It looks and feels like a modern AI "
        "assistant (typing indicators, streaming feel, avatar, attachment previews) but runs "
        "entirely offline from a curated knowledge base.",
        S['body']
    ))

    story.append(Paragraph("Topic Scoring Algorithm", S['h2']))
    story.append(Paragraph(
        "Each of the 49 KB topics has a keys[] array of trigger phrases. When a question arrives, "
        "every topic is scored by summing the lengths of all keys that appear in the question (lowercased). "
        "Using key length as the score weight is the key insight: longer, more specific phrases "
        "(like 'how was a seal actually made') score higher than short generic words (like 'seal'). "
        "This prevents common words from drowning out specific matches.",
        S['body']
    ))
    story.append(Paragraph(
        "Example: question = 'how did they make the indus seals?'\n"
        "  Topic A: keys=['seal','seals'] → score = 4 + 5 = 9\n"
        "  Topic B: keys=['how a seal was actually made','seal manufacture'] → score = 27 + 16 = 43\n"
        "  Winner: Topic B (seal manufacture)",
        S['code']
    ))

    story.append(Paragraph("Quick Questions Panel", S['h2']))
    story.append(Paragraph(
        "Eight pre-set question buttons let users explore without typing. Each button has a data-q "
        "attribute with the full question text, which is passed directly to handleQuestion() as if "
        "the user had typed it.",
        S['body']
    ))

    story.append(Paragraph("Learning Paths", S['h2']))
    story.append(Paragraph(
        "Five curated learning journeys walk users through a topic sequence step by step. "
        "Each step is delivered with a numbered badge (e.g. '2/5 · The unicorn motif'). "
        "Between steps, a 450ms pause is added so the user can read before the next card appears. "
        "Gemini Nano enrichment is attempted for each step.",
        S['body']
    ))

    story.append(Paragraph("Attachment + Vision Branch", S['h2']))
    story.append(Paragraph(
        "When an image is attached, the chat handler takes a different path: vision analysis runs "
        "first and its category result is shown to the user with all raw statistics. Then the "
        "matched KB topic is displayed as a follow-up card. The user's uploaded image is shown "
        "as a thumbnail inside their message bubble.",
        S['body']
    ))

    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  7. VISION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("7. Canvas Vision — How Image Analysis Works", S['h1']))
    story.append(divider())

    story.append(Paragraph(
        "Traditional image AI requires sending the image to a cloud API (Google Vision, AWS Rekognition, etc.) "
        "which costs money and involves privacy trade-offs. Indus Valley AI instead runs a "
        "statistical classification algorithm directly in the browser — no upload, no API key, "
        "zero latency beyond the pixel loop.",
        S['body']
    ))

    story.append(Paragraph("The Sepia Score (warmth metric)", S['h2']))
    story.append(Paragraph(
        "Indus seals are made of steatite (soapstone) — a warm beige/brown stone. Photographs of "
        "seals tend to have a characteristic warm sepia tone. The sepia score captures this: "
        "it computes how much redder and warmer the average pixel is compared to a neutral gray, "
        "then scales the result between 0 and 1. Seals and clay artifacts typically score above 0.45.",
        S['body']
    ))
    story.append(Paragraph(
        "Formula: warmth = (avgR - avgB) / 255\n"
        "         balance = 1 - |((avgR-avgG) - (avgG-avgB))| / 255\n"
        "         sepia = clamp(warmth * 1.6 * balance, 0, 1)",
        S['code']
    ))

    story.append(Paragraph("Edge Density (Sobel-light approximation)", S['h2']))
    story.append(Paragraph(
        "Edge density measures how much fine detail and sharp outlines are in the image. "
        "High edge density = line-art or highly detailed photograph. Low edge density = plain background "
        "or out-of-focus photo. The implementation skips every other pixel (sampling at stride 2) "
        "for speed, then computes the luminance gradient to the right and downward neighbors "
        "(a simplified one-sided Sobel operator).",
        S['body']
    ))

    story.append(Paragraph("Classification Decision Tree", S['h2']))
    clf_data = [
        [
            Paragraph("Category", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=13)),
            Paragraph("Conditions", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=13)),
            Paragraph("Routed to", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=13)),
        ],
        [Paragraph("seal", S['body']), Paragraph("warm + square-ish + photo-like + edge>0.08", S['body']), Paragraph("Seals, Unicorn motif, Manufacture", S['body'])],
        [Paragraph("script", S['body']), Paragraph("line-art: light bg + high edge + monochrome", S['body']), Paragraph("Script, Fish sign, Parpola", S['body'])],
        [Paragraph("map", S['body']), Paragraph("dominant hue = green or brown-green", S['body']), Paragraph("Urban planning, City comparisons", S['body'])],
        [Paragraph("artifact", S['body']), Paragraph("warm + photo-like (non-square)", S['body']), Paragraph("Figurines, Priest-King, Dancing Girl", S['body'])],
        [Paragraph("illustration", S['body']), Paragraph("light bg + colorSpread < 35", S['body']), Paragraph("Overview, Chronology", S['body'])],
        [Paragraph("site-photo", S['body']), Paragraph("photo-like (fallback)", S['body']), Paragraph("Urban planning, Great Bath", S['body'])],
    ]
    clf_table = Table(clf_data, colWidths=[24*mm, 78*mm, 61*mm])
    clf_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, HexColor("#F5F0E8")]),
        ('BOX', (0,0), (-1,-1), 0.6, GOLD_SOFT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, LIGHT_GRAY),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(clf_table)
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  8. GEMINI NANO
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("8. Gemini Nano — Free On-Device Intelligence", S['h1']))
    story.append(divider())

    story.append(Paragraph(
        "Gemini Nano is a compact language model distributed as part of Google Chrome itself. "
        "Unlike GPT-4, Claude, or Gemini Pro, it runs entirely on the user's own hardware — "
        "on their CPU or integrated GPU. No tokens are consumed. No API key is required. "
        "No data is transmitted. It is the closest thing to 'free AI' that currently exists.",
        S['body']
    ))

    story.append(kv_table([
        ("Availability",  "Chrome 127+ with Gemini Nano flag enabled in chrome://flags/#optimization-guide-on-device-model"),
        ("API surface",   "window.LanguageModel (new) or window.ai.languageModel (legacy) — both handled by gemini-nano.js"),
        ("Model size",    "~1.8 GB — downloaded once by Chrome, stored locally, reused across all sites"),
        ("Cost",          "Absolutely zero — uses no cloud, no tokens, no billing"),
        ("Privacy",       "100% — text never leaves the device; processed entirely in the browser"),
        ("Fallback",      "If unavailable, the KB answer is shown alone; the site is fully functional without it"),
        ("System prompt", "Hard-coded Indus domain lock — same scholarly rules as the KB"),
        ("Parameters",    "Temperature: 0.4 (focused), TopK: 3 (very constrained)"),
    ], S))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "The integration design is deliberately conservative: Gemini Nano only adds a supplementary "
        "paragraph to an already-correct KB answer. It is never the primary source. This prevents "
        "hallucinations from reaching the user without a safety net — the KB answer is always shown "
        "first, and if the Nano output contradicts it, the user has the KB content to compare against.",
        S['body']
    ))
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  9. 3D GRAPHICS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("9. 3D Graphics — Two WebGL Scenes", S['h1']))
    story.append(divider())

    story.append(Paragraph(
        "WebGL is the browser's 3D graphics API, the same technology used for browser-based games. "
        "Three.js is a JavaScript library that wraps WebGL's complex low-level commands into a "
        "clean, readable scene-graph API. The project uses Three.js 0.160 loaded via CDN "
        "(no local install, no build step).",
        S['body']
    ))

    story.append(Paragraph("Why Two Separate Scenes?", S['h2']))
    story.append(Paragraph(
        "Each WebGL renderer is independent — its own canvas, camera, scene graph, and animation loop. "
        "This allows the hero seal to have a completely different visual style (dark, intimate, close-up) "
        "from the trade routes globe (aerial, expansive, geopolitical). "
        "Both use IntersectionObserver to pause rendering when scrolled off-screen, "
        "saving GPU power on mobile devices.",
        S['body']
    ))

    story.append(Paragraph("Three.js features used across both scenes:", S['h2']))
    threejs_left = [
        "PerspectiveCamera with orbit",
        "WebGLRenderer (antialias, alpha)",
        "ACESFilmic tone mapping",
        "FogExp2 atmospheric fog",
        "AmbientLight + DirectionalLight",
        "PointLight fill lights",
        "MeshStandardMaterial (PBR)",
        "MeshBasicMaterial (flat shading)",
        "ExtrudeGeometry (seal body, motif)",
    ]
    threejs_right = [
        "TubeGeometry (trade route arcs)",
        "QuadraticBezierCurve3 (arc paths)",
        "CircleGeometry (world disc)",
        "RingGeometry (halo rings, grid)",
        "SphereGeometry (sparks, nodes)",
        "CylinderGeometry (city pillars)",
        "BufferGeometry + BufferAttribute",
        "PointsMaterial + Points (dust)",
        "AdditiveBlending (glow effects)",
    ]
    story.append(two_col(threejs_left, threejs_right, S))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Renderer Settings", S['h2']))
    story.append(kv_table([
        ("antialias: true",  "Smooths jagged edges — more GPU cost but much better visual quality"),
        ("alpha: true",      "Transparent background — the canvas blends into the page background"),
        ("outputColorSpace", "THREE.SRGBColorSpace — correct gamma for display"),
        ("toneMapping",      "ACESFilmicToneMapping — filmic HDR look, preserves highlight detail"),
        ("pixelRatio",       "Math.min(devicePixelRatio, 2) — sharp on HiDPI but caps at 2x for performance"),
    ], S))
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  10. DESIGN SYSTEM
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("10. Design System & Visual Identity", S['h1']))
    story.append(divider())

    story.append(Paragraph(
        "The visual identity of Indus Valley AI is built around a single concept: "
        "<i>ancient meets futuristic</i>. The color palette is drawn from Harappan artifacts — "
        "fired steatite (warm gray), terracotta (brick red), and carnelian (deep amber-gold). "
        "The typography pairs a classical serif (Cormorant Garamond — used in museum publications) "
        "with a modern geometric sans (Inter) and a technical monospace (JetBrains Mono).",
        S['body']
    ))

    story.append(Paragraph("UI Animation Inventory", S['h2']))
    anim_rows = [
        ("Custom cursor", "requestAnimationFrame lerp at 0.30 (dot) and 0.12 (ring)"),
        ("Spotlight glow", "CSS radial-gradient tracking mouse via custom properties"),
        ("Magnetic buttons", "transform: translate() at 25% pointer offset magnitude"),
        ("Reveal on scroll", "opacity + scale transition, 800ms cubic-bezier(0.16,1,0.3,1)"),
        ("Scroll spine fill", "scaleY() interpolated to scroll percentage"),
        ("Ticker text", "@keyframes scrollLeft — infinite horizontal marquee"),
        ("Seal gallery cards", "backdrop-filter: blur() + translateY on hover"),
        ("Halo rings (3D)", "Three.js scale pulsing via sin(t) in animation loop"),
        ("Trade sparks (3D)", "QuadraticBezierCurve3.getPoint(t) travel, t cycles 0→1"),
        ("Gold dust (3D)", "Y-position drift, reset on reaching max height"),
        ("Drop zone border", "@keyframes pulsing dashed gold border on file drag"),
        ("Typing indicator", "Three bouncing dots (CSS @keyframes, staggered delay)"),
    ]
    story.append(kv_table(anim_rows, S, col1=52*mm, col2=111*mm))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Responsive Design", S['h2']))
    story.append(Paragraph(
        "The site is fully responsive. Below 768px: the scroll spine hides, the 3D canvas height "
        "reduces, navigation collapses into a burger menu, grid layouts switch to single-column, "
        "and the custom cursor is disabled (pointer:coarse media query). The site is usable on "
        "a phone, tablet, and desktop without any layout breakage.",
        S['body']
    ))
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  11. TECH STACK TABLE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("11. Tech Stack Summary Table", S['h1']))
    story.append(divider())

    ts_data = [
        [
            Paragraph("Technology", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9.5, textColor=WHITE, leading=14)),
            Paragraph("Version / Source", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9.5, textColor=WHITE, leading=14)),
            Paragraph("Used For", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9.5, textColor=WHITE, leading=14)),
            Paragraph("Cost", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9.5, textColor=WHITE, leading=14)),
        ],
        [Paragraph("HTML5", S['body']), Paragraph("Semantic — no framework", S['body']), Paragraph("Page structure, 12 sections", S['body']), Paragraph("Free", S['body'])],
        [Paragraph("CSS3", S['body']), Paragraph("Vanilla — no preprocessor", S['body']), Paragraph("Full design system, animations", S['body']), Paragraph("Free", S['body'])],
        [Paragraph("JavaScript (ES2022)", S['body']), Paragraph("Vanilla IIFE + modules", S['body']), Paragraph("All UI, AI, vision logic", S['body']), Paragraph("Free", S['body'])],
        [Paragraph("Three.js", S['body']), Paragraph("0.160 via importmap CDN", S['body']), Paragraph("Two real-time 3D WebGL scenes", S['body']), Paragraph("Free", S['body'])],
        [Paragraph("Gemini Nano", S['body']), Paragraph("window.LanguageModel — Chrome built-in", S['body']), Paragraph("On-device LLM enrichment", S['body']), Paragraph("Free", S['body'])],
        [Paragraph("Canvas 2D API", S['body']), Paragraph("Browser built-in", S['body']), Paragraph("Image pixel analysis (vision.js)", S['body']), Paragraph("Free", S['body'])],
        [Paragraph("IntersectionObserver", S['body']), Paragraph("Browser built-in API", S['body']), Paragraph("Scroll reveals, 3D pause", S['body']), Paragraph("Free", S['body'])],
        [Paragraph("Cormorant Garamond", S['body']), Paragraph("Google Fonts CDN", S['body']), Paragraph("Display / heading typeface", S['body']), Paragraph("Free", S['body'])],
        [Paragraph("Inter", S['body']), Paragraph("Google Fonts CDN", S['body']), Paragraph("Body typeface", S['body']), Paragraph("Free", S['body'])],
        [Paragraph("JetBrains Mono", S['body']), Paragraph("Google Fonts CDN", S['body']), Paragraph("Code / technical typeface", S['body']), Paragraph("Free", S['body'])],
        [Paragraph("Python http.server", S['body']), Paragraph("Python 3 stdlib", S['body']), Paragraph("Local development server", S['body']), Paragraph("Free", S['body'])],
        [Paragraph("ReportLab", S['body']), Paragraph("4.4 — pip install", S['body']), Paragraph("This PDF report generation", S['body']), Paragraph("Free (OSS)", S['body'])],
    ]
    ts_table = Table(ts_data, colWidths=[34*mm, 42*mm, 62*mm, 22*mm])
    ts_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), CHARCOAL),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, HexColor("#F5F0E8")]),
        ('BOX', (0,0), (-1,-1), 0.8, GOLD_SOFT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, LIGHT_GRAY),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTNAME', (3,1), (3,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (3,1), (3,-1), HexColor("#1A7A1A")),
    ]))
    story.append(ts_table)
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  12. COMPARISON
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("12. What We Built vs What Others Do", S['h1']))
    story.append(divider())

    story.append(Paragraph(
        "Most digital humanities projects fall into one of two categories: "
        "(a) simple static websites with text and images but no interactivity, or "
        "(b) complex platforms requiring cloud infrastructure and ongoing maintenance costs. "
        "Indus Valley AI occupies a unique third position.",
        S['body']
    ))

    comparisons = [
        ("Wikipedia", "Comprehensive text reference. No AI, no 3D, no domain restriction. "
         "Anyone can edit, risking misinformation. No image analysis."),
        ("Google Arts & Culture", "Beautiful visuals, museum partnerships. No AI chat. "
         "No domain-specific scholarly depth. Requires internet for every asset."),
        ("ChatGPT / Claude", "General-purpose AI — powerful but unfocused and expensive to run. "
         "Will hallucinate about Indus topics. Not specialized, not offline."),
        ("Academic websites (e.g. harappa.com)", "Authoritative scholarship. Static HTML, "
         "text-only. No AI, no 3D, no interaction layer."),
        ("Indus Valley AI (this project)", "Domain-locked AI with 49 curated scholarly topics. "
         "Two real-time 3D scenes. On-device LLM enrichment. Image analysis. "
         "Zero server cost. Academic honesty built in. Works offline after first load."),
    ]
    for name, desc in comparisons:
        story.append(KeepTogether([
            Paragraph(name, S['h3']),
            Paragraph(desc, S['body']),
        ]))

    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  13. FUTURE DIRECTIONS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("13. Future Directions", S['h1']))
    story.append(divider())

    future = [
        ("Service Worker + Offline Cache",
         "Registering a Service Worker would cache all assets after the first visit, "
         "making the site fully functional with no internet connection — a true offline PWA."),
        ("WebXR / Augmented Reality",
         "Three.js supports WebXR. The 3D seal could be viewed in augmented reality on a "
         "mobile phone camera, overlaying the virtual seal over a real desk surface."),
        ("Expanded Knowledge Base",
         "The KB currently covers 49 topics. A future version could expand to 150+ topics "
         "covering every major excavated site, every known motif category, and every published "
         "decipherment hypothesis in detail."),
        ("Vector Similarity Search",
         "Instead of keyword scoring, embedding the KB topics as semantic vectors and using "
         "cosine similarity would allow the AI to match questions that use different words "
         "to describe the same concept."),
        ("Multi-language Support",
         "Adding Hindi, Telugu, and Tamil interfaces would make the platform accessible to "
         "regional audiences in India, particularly for school and university education."),
        ("Peer-Reviewed Knowledge Validation",
         "Partnering with archaeologists at DECCAN College, ASI, or IIT Gandhinagar to "
         "formally validate the KB content would make the platform citable as a scholarly source."),
    ]
    for name, desc in future:
        story.append(KeepTogether([
            Paragraph(name, S['h3']),
            Paragraph(desc, S['body']),
        ]))

    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  14. CONCLUSION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Paragraph("14. Conclusion", S['h1']))
    story.append(divider())

    story.append(Paragraph(
        "Indus Valley AI demonstrates that a sophisticated AI-powered educational platform does not "
        "require cloud infrastructure, paid APIs, or a backend server. By combining a hand-curated "
        "scholarly knowledge base, browser-native machine learning (Gemini Nano), client-side "
        "computer vision, and real-time 3D WebGL graphics — all within a single static website — "
        "the project achieves what would typically require a team of engineers and a monthly cloud bill.",
        S['body']
    ))
    story.append(Paragraph(
        "Every design decision prioritized three values: academic honesty (the AI only answers "
        "what it knows, cites scholars, and flags uncertainty), privacy (no data ever leaves the "
        "user's device), and accessibility (free to use, free to host, works on any device).",
        S['body']
    ))
    story.append(Paragraph(
        "The Indus Valley Civilization is one of the most important and least understood chapters "
        "of human history. Its script remains undeciphered. Its religion is debated. Its cities "
        "show a level of urban planning that rivals ancient Rome — 4,000 years earlier. A platform "
        "that makes this knowledge accessible, beautiful, and interactive is a small but meaningful "
        "contribution to that scholarship.",
        S['body']
    ))

    story.append(Spacer(1, 8*mm))
    story.append(divider(GOLD, 2))
    story.append(Spacer(1, 4*mm))

    final_box_data = [[Paragraph(
        "<b>Project:</b> Indus Valley AI &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Lead:</b> Mohammed Majeed Khan &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Organization:</b> AI Hub, Mahindra University &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Date:</b> April 2026<br/><br/>"
        "This report was generated programmatically using Python ReportLab. "
        "All code, content, and 3D scenes were purpose-built for this project.",
        S['body']
    )]]
    final_box = Table(final_box_data, colWidths=[W])
    final_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CHARCOAL),
        ('TEXTCOLOR', (0,0), (-1,-1), OFF_WHITE),
        ('BOX', (0,0), (-1,-1), 1.5, GOLD),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(final_box)

    # Build
    doc.multiBuild(story, canvasmaker=ReportCanvas)
    print(f"PDF saved to: {OUTPUT}")

if __name__ == "__main__":
    build()
