#!/usr/bin/env python3
"""PDF of the Verodus-only analysis (last reply). No MoniMath content."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/opt/cursor/artifacts/verodus_analysis_only.pdf")
REPO_OUT = Path("/workspace/docs/verodus-analysis-only.pdf")

FONT_DIR = Path("/usr/share/fonts/truetype/macos")
GREEN = (15, 118, 110)
INK = (22, 27, 34)
MUTED = (87, 96, 106)
RULE = (208, 215, 222)
SOFT = (246, 248, 250)
WHITE = (255, 255, 255)


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
        self.cell(0, 5, "Verodus analysis", align="L")
        self.set_xy(18, 10)
        self.cell(0, 5, "Internal  ·  20 August 2026", align="R")
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
        self.cell(0, 6, "Confidential  ·  Verodus only  ·  Not a legal opinion", align="L")
        self.set_xy(18, -12)
        self.cell(0, 6, str(self.page_no()), align="R")

    def h2(self, text):
        self.ln(2.4)
        y = self.get_y()
        if y > 262:
            self.add_page()
            y = self.get_y()
        self.set_fill_color(*GREEN)
        self.rect(18, y + 1.0, 2.2, 5.8, "F")
        self.set_x(23)
        self.set_font("InterSB", "", 12)
        self.set_text_color(*INK)
        self.multi_cell(0, 7.2, text)
        self.ln(0.8)

    def body(self, text):
        self.set_font("Inter", "", 10)
        self.set_text_color(*INK)
        needed = 5.0 * max(1, len(self.multi_cell(0, 5.0, text, dry_run=True, output="LINES")))
        if self.get_y() + needed > 275:
            self.add_page()
        self.multi_cell(0, 5.0, text)
        self.ln(1.0)

    def bullet(self, text, indent=6):
        x = 18 + indent
        self.set_x(x)
        self.set_font("Inter", "B", 10)
        self.set_text_color(*GREEN)
        self.cell(4, 5.0, "•")
        self.set_font("Inter", "", 10)
        self.set_text_color(*INK)
        self.multi_cell(192 - x - 4, 5.0, text)
        self.ln(0.2)

    def callout(self, text):
        self.ln(1)
        start = self.get_y()
        self.set_x(22)
        self.set_font("InterM", "", 10.5)
        self.set_text_color(*INK)
        self.multi_cell(168, 5.4, text)
        end = self.get_y()
        self.set_draw_color(*GREEN)
        self.set_line_width(1.6)
        self.line(18.8, start - 1.5, 18.8, end + 1.2)
        self.set_line_width(0.2)
        self.ln(3)


def build():
    pdf = BriefingPDF()
    pdf.add_page()
    pdf.set_fill_color(*GREEN)
    pdf.rect(0, 0, 210, 8, "F")
    pdf.set_fill_color(*SOFT)
    pdf.rect(0, 8, 210, 42, "F")
    pdf.set_y(14)
    pdf.set_font("Inter", "", 9)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 5, "VERODUS ONLY", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_x(18)
    pdf.set_font("Inter", "B", 22)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 9, "Verodus analysis")
    pdf.set_x(18)
    pdf.set_font("Inter", "", 10)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 5.5, "Internal briefing  ·  20 August 2026")

    pdf.set_y(56)
    pdf.callout(
        "Verodus is a real, small simulated-evaluation shop whose P&L is evaluation "
        "fees plus tightly gated discretionary payouts. It is not a broker and not live "
        "capital. Scale (about 3,000 users) is the constraint; labeled trader-behavior "
        "data is the scarce asset."
    )

    pdf.h2("What it is")
    pdf.body(
        "Dual stack (Platform 5 / MT5 + TradeHub), Instant / 1-Step / 2-Step Lite / Pro, "
        "KYC, Rise/crypto payouts. Public legal names do not match:"
    )
    pdf.bullet("Verodus L.L.C.-FZ — Terms of Service; Dubai / UAE governing law.")
    pdf.bullet("Verodus LLC — Privacy Policy data controller and Risk Disclosure.")
    pdf.bullet("Verodus Capital Inc. — all fees and performance rewards.")
    pdf.body(
        "Kim Chen is CEO; Alexander Vladimirovich is COO. No free-zone, license number, "
        "or registered address is published on the pages reviewed."
    )

    pdf.h2("How money works")
    pdf.body(
        "Instant is the high-margin door: no fee refund, 3% daily / 6% trailing max that "
        "never locks, Best Day ≤20%. 1-Step and 2-Step refund the fee on first payout, "
        "so they only work if most buyers never get there. “Make traders better” without "
        "more volume or a new cash line (data, add-ons, white-label) is a cost."
    )

    pdf.h2("What is strong")
    pdf.bullet("Live product and published rule pages (Instant, 1-Step, 2-Step Lite/Pro).")
    pdf.bullet("Unusually honest simulation and discretionary-reward legal language.")
    pdf.bullet("A coherent fail-heavy Instant design, not an accident.")
    pdf.bullet("CRM data that most “AI trading” firms cannot buy: labeled pass/fail paths.")

    pdf.h2("What to fix before selling data or buying exposure")
    pdf.bullet("Align the three legal names and publish a free-zone / service address.")
    pdf.bullet(
        "Either put a live Trustpilot URL behind the 4.5 claim or drop the number."
    )
    pdf.bullet(
        "Stop copy drift: blog still cites 10%/5% targets; hero “from $49” vs Instant "
        "table; homepage payout carousel repeats $9,401.23 for both Jose and Joe."
    )
    pdf.bullet(
        "Do not license behavioral data until the 21 February 2026 privacy policy is "
        "amended. It currently forbids external commercialization of trading-behavior data."
    )

    pdf.h2("Recommendation")
    pdf.callout(
        "Grow units at current rules (affiliates / paid white-label). Keep Instant tight. "
        "Productize anonymized data only after counsel updates privacy. Make payouts "
        "verifiable. Loosening rules for “exposure” is the wrong trade."
    )

    pdf.ln(2)
    pdf.set_font("Inter", "I", 8)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.4,
        "Sources: verodus.com public pages (home, about, Instant, 1-Step, 2-Step Lite, "
        "objectives, FAQ, Terms, Privacy 21 Feb 2026, Risk Disclosure). Verodus only. "
        "Not an audit. Not legal advice.",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPO_OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    pdf.output(str(REPO_OUT))
    print(f"Wrote {OUT} pages={pdf.pages_count} bytes={OUT.stat().st_size}")


if __name__ == "__main__":
    build()
