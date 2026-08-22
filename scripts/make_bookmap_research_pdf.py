#!/usr/bin/env python3
"""PDF: Bookmap research for the Joe Wong email."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/opt/cursor/artifacts/Bookmap_Research.pdf")
REPO_OUT = Path("/workspace/docs/bookmap-research.pdf")
ROOT_OUT = Path("/workspace/bookmap-research.pdf")

FONT_DIR = Path("/usr/share/fonts/truetype/macos")
GREEN = (15, 118, 110)
INK = (22, 27, 34)
MUTED = (87, 96, 106)
RULE = (208, 215, 222)
SOFT = (246, 248, 250)
WHITE = (255, 255, 255)
RED = (159, 18, 57)


class BriefingPDF(FPDF):
    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=True, margin=22)
        self.set_margins(18, 18, 18)
        self.add_font("Inter", "", str(FONT_DIR / "Inter-Regular.ttf"))
        self.add_font("Inter", "B", str(FONT_DIR / "Inter-Bold.ttf"))
        self.add_font("Inter", "I", str(FONT_DIR / "Inter-Italic.ttf"))
        self.add_font("InterM", "", str(FONT_DIR / "Inter-Medium.ttf"))
        self.add_font("InterSB", "", str(FONT_DIR / "Inter-SemiBold.ttf"))

    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(10)
        self.set_font("Inter", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 5, "Bookmap  |  Why it is in Joe’s email", align="L")
        self.set_xy(18, 10)
        self.cell(0, 5, "Internal  ·  22 August 2026", align="R")
        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        self.line(18, 16, 192, 16)
        self.set_y(20)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(*RULE)
        self.line(18, self.get_y(), 192, self.get_y())
        self.set_y(-12)
        self.set_font("Inter", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 6, "Confidential  ·  Not a legal opinion or an offer", align="L")
        self.set_xy(18, -12)
        self.cell(0, 6, str(self.page_no()), align="R")

    def h2(self, text):
        self.ln(3.2)
        y = self.get_y()
        if y > 262:
            self.add_page()
            y = self.get_y()
        self.set_fill_color(*GREEN)
        self.rect(18, y + 1.0, 2.2, 5.8, "F")
        self.set_x(23)
        self.set_font("InterSB", "", 12.5)
        self.set_text_color(*INK)
        self.multi_cell(0, 7.4, text)
        self.ln(1.0)

    def body(self, text):
        self.set_font("Inter", "", 10)
        self.set_text_color(*INK)
        needed = 5.2 * max(1, len(self.multi_cell(0, 5.2, text, dry_run=True, output="LINES")))
        if self.get_y() + needed > 275:
            self.add_page()
        self.multi_cell(0, 5.2, text)
        self.ln(1.2)

    def bullet(self, text, indent=6):
        x = 18 + indent
        needed = 5.2 * max(1, len(self.multi_cell(0, 5.2, text, dry_run=True, output="LINES")))
        if self.get_y() + needed > 275:
            self.add_page()
        self.set_x(x)
        self.set_font("Inter", "B", 10)
        self.set_text_color(*GREEN)
        self.cell(4, 5.2, "•")
        self.set_font("Inter", "", 10)
        self.set_text_color(*INK)
        self.multi_cell(192 - x - 4, 5.2, text)
        self.ln(0.3)

    def callout(self, text):
        self.ln(1)
        needed = 5.5 * max(1, len(self.multi_cell(0, 5.5, text, dry_run=True, output="LINES")))
        if self.get_y() + needed + 6 > 275:
            self.add_page()
        start = self.get_y()
        self.set_x(22)
        self.set_font("InterM", "", 10.5)
        self.set_text_color(*INK)
        self.multi_cell(168, 5.5, text)
        end = self.get_y()
        self.set_draw_color(*GREEN)
        self.set_line_width(1.6)
        self.line(18.8, start - 1.5, 18.8, end + 1.2)
        self.set_line_width(0.2)
        self.ln(3)

    def warn(self, text):
        self.ln(1)
        needed = 5.5 * max(1, len(self.multi_cell(0, 5.5, text, dry_run=True, output="LINES")))
        if self.get_y() + needed + 6 > 275:
            self.add_page()
        start = self.get_y()
        self.set_x(22)
        self.set_font("InterM", "", 10.5)
        self.set_text_color(*INK)
        self.multi_cell(168, 5.5, text)
        end = self.get_y()
        self.set_draw_color(*RED)
        self.set_line_width(1.6)
        self.line(18.8, start - 1.5, 18.8, end + 1.2)
        self.set_line_width(0.2)
        self.ln(3)


def add_table(pdf, headers, rows, col_widths):
    usable = 174
    scale = usable / sum(col_widths)
    col_widths = [w * scale for w in col_widths]
    line_h = 4.6
    if pdf.get_y() > 248:
        pdf.add_page()
    x0, y = 18, pdf.get_y()
    pdf.set_fill_color(*GREEN)
    pdf.set_text_color(*WHITE)
    pdf.set_font("InterSB", "", 7.5)
    header_h = 8
    pdf.rect(x0, y, usable, header_h, "F")
    x = x0
    for i, h in enumerate(headers):
        pdf.set_xy(x + 1.5, y + 1.6)
        pdf.multi_cell(col_widths[i] - 3, 4.4, h)
        x += col_widths[i]
    y += header_h
    for r_i, row in enumerate(rows):
        heights = []
        for i, cell in enumerate(row):
            pdf.set_font("Inter", "B" if i == 0 else "", 7.6)
            n = pdf.multi_cell(col_widths[i] - 3, line_h, cell, dry_run=True, output="LINES")
            heights.append(max(1, len(n)) * line_h + 2.0)
        h = max(heights)
        if y + h > 275:
            pdf.add_page()
            y = pdf.get_y()
        fill = (248, 250, 252) if r_i % 2 == 0 else WHITE
        pdf.set_fill_color(*fill)
        pdf.rect(x0, y, usable, h, "F")
        pdf.set_draw_color(*RULE)
        pdf.line(x0, y + h, x0 + usable, y + h)
        x = x0
        for i, cell in enumerate(row):
            pdf.set_xy(x + 1.5, y + 1.1)
            pdf.set_font("Inter", "B" if i == 0 else "", 7.6)
            pdf.set_text_color(*INK)
            pdf.multi_cell(col_widths[i] - 3, line_h, cell)
            x += col_widths[i]
        y += h
    pdf.set_y(y + 3)


def build():
    pdf = BriefingPDF()
    pdf.add_page()
    pdf.set_fill_color(*GREEN)
    pdf.rect(0, 0, 210, 8, "F")
    pdf.set_fill_color(*SOFT)
    pdf.rect(0, 8, 210, 54, "F")
    pdf.set_y(16)
    pdf.set_font("Inter", "", 9)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 5, "VERODUS INTERNAL BRIEFING", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_x(18)
    pdf.set_font("Inter", "B", 22)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 8.5, "Bookmap — what it is, and why Joe’s email still says it")
    pdf.set_x(18)
    pdf.set_font("Inter", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 6, "Company file  ·  22 August 2026  ·  For Alexander")

    pdf.set_y(74)
    pdf.callout(
        "Bookmap is a paid order-flow heatmap. It is not a prop firm and not Verodus. "
        "On 11 August 2026 — ten days before Joe emailed you — Bookmap announced a "
        "partnership with 10FOUR, a Hong Kong futures Instant/evaluation shop. Roles in "
        "that deal stay clean: Bookmap visualizes; 10FOUR sells challenges. Joe pasted "
        "Verodus into Bookmap’s product slot instead."
    )
    pdf.warn(
        "No public link was found between Bookmap and Joe Wong, TradeMath, MoniMath, or "
        "World Traders Hub HK. He reused partner language. He did not propose Bookmap "
        "then Verodus as a two-vendor stack."
    )

    pdf.h2("What Bookmap is")
    add_table(
        pdf,
        ["Item", "Fact"],
        [
            [
                "Product",
                "Heatmap of the limit order book (historical liquidity) plus volume dots, ~40 fps. Name = order book + heat map.",
            ],
            [
                "Markets",
                "Futures (core), US stocks, crypto. Sits on Rithmic / CQG / dxFeed / Tradovate / NinjaTrader. Not the broker.",
            ],
            [
                "Revenue",
                "SaaS. 2026 public bands (data extra): Digital free; Digital+ ~$19–$39/mo; Global ~$49–$69/mo or ~$990 life; Global+ ~$99/mo or ~$1,990 life.",
            ],
            [
                "Company",
                "Bookmap Ltd, Cyprus. Founder/CEO Tsachi Galanos. ~50–60 staff. Not an SFC licensee.",
            ],
            [
                "Owner",
                "Nelogica (Porto Alegre) majority stake 1 Nov 2024. Brand continues. ~300k users claimed at deal.",
            ],
            [
                "Not",
                "A challenge seller, a payout firm, MT5, TradeHub, or Instant / 1-Step / Lite.",
            ],
        ],
        [36, 138],
    )

    pdf.h2("How they partner — the genre of Joe’s email")
    pdf.body(
        "Public pages: bookmap.com/partnering/ and bookmap.com/en/b2b/prop-firms. Broker/FCM "
        "partners sell seats. OEM/custom for props, banks, exchanges. Affiliates via FlexOffers. "
        "The prop-firm page pitches bulk licenses, record/replay for coaching, and retention "
        "(traders return for more evaluations). That is “official partner + order-flow "
        "visualization + platform adoption.” Bookmap writes it to prop firms. Joe sent it as "
        "if Verodus were Bookmap."
    )
    pdf.body(
        "Correct split: Bookmap sells heatmap seats. The prop firm sells evaluation fees. "
        "Joe inverted it."
    )

    pdf.h2("Bookmap × 10FOUR (11 Aug 2026)")
    pdf.body(
        "Bookmap’s LinkedIn: traders use Bookmap while trading a 10FOUR evaluation or funded "
        "account. 10FOUR (Ten Four Group, HK CR 79713385, Kwun Tong) is a futures sim-prop: "
        "Instant, Origin, Daily; $25k–$150k; 90% split; CQG; Riseworks. Same category as "
        "Verodus (simulated evaluation, Instant language, Rise), different stack (CQG futures "
        "vs Platform 5 / TradeHub). Mixed independent reviews; not a recommendation — it is "
        "the public pair Bookmap chose ten days before Joe hit send."
    )
    pdf.body(
        "Joe is in Hong Kong. The competent two-vendor letter would have been: Bookmap on "
        "the tape, a prop shop for challenges. He left “Proposed Partnership with Bookmap” "
        "in a letter to you. No evidence Bookmap closed with him. No evidence 10FOUR is in "
        "his email. The announcement is the model in the market when he mailed you."
    )

    pdf.h2("Bookmap vs Verodus")
    add_table(
        pdf,
        ["", "Bookmap", "Verodus"],
        [
            ["Sells", "Heatmap sub + data", "Instant / 1-Step / Lite fees"],
            ["Trader pays", "~$0–$99/mo + exchange data", "Challenge fee (e.g. Instant $49 at 35% off)"],
            ["Platform", "Own chart + Rithmic/CQG", "Platform 5 (MT5, not US) + TradeHub"],
            ["Pays the trader?", "No", "Yes, if rules + KYC"],
            ["Joe’s email called it", "Institutional-grade order flow", "The same phrase, name swapped"],
        ],
        [40, 67, 67],
    )
    pdf.body(
        "A real dual deal would be Verodus buyers buying Bookmap seats (or a bulk license). "
        "That is a cost line, not origination. Most futures props that “support Bookmap” only "
        "mean Rithmic credentials work. They do not pay the trader’s Bookmap sub. 10FOUR is "
        "a named co-marketing exception."
    )

    pdf.h2("What this changes")
    pdf.bullet("Nothing in the commercial posture. It explains the email.")
    pdf.bullet("Bookmap is real and widely used. Mis-assigning its product to Verodus is the error.")
    pdf.bullet("The live HK pattern is Bookmap + 10FOUR, not Bookmap + Verodus.")
    pdf.bullet("If he ever writes a real two-vendor stack, Verodus’s slice is still tagged evaluation fees, not heatmap revenue and not OHKF/SFC halo.")
    pdf.bullet("If he wants Bookmap, he deals with Bookmap. If he wants challenge volume, he names Instant / 1-Step / Lite and a code.")

    pdf.ln(2)
    pdf.set_font("Inter", "I", 8.2)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.6,
        "Sources 22 August 2026: bookmap.com, bookmap.com/en/b2b/prop-firms, Nelogica 1 Nov 2024 "
        "PR, Bookmap LinkedIn 10FOUR post 11 Aug 2026, Tradier Aug 2025 PR, public 2026 pricing "
        "round-ups. Companion: docs/bookmap-research.md. No Bookmap–Joe/TradeMath/MoniMath hit "
        "found. Not an audit and not legal advice.",
    )

    for path in (OUT, REPO_OUT, ROOT_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        print(f"Wrote {path} pages={pdf.pages_count} bytes={path.stat().st_size}")


if __name__ == "__main__":
    build()
