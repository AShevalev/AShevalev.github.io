#!/usr/bin/env python3
"""PDF: Kim’s Karma Lounge read vs Joe’s email vs the research."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/opt/cursor/artifacts/Kim_Karma_Lounge_Read.pdf")
REPO_OUT = Path("/workspace/docs/kim-karma-lounge-read.pdf")
ROOT_OUT = Path("/workspace/kim-karma-lounge-read.pdf")

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
        self.cell(0, 5, "Joe Wong  |  Kim’s meeting read vs the email", align="L")
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
    pdf.rect(0, 8, 210, 52, "F")
    pdf.set_y(16)
    pdf.set_font("Inter", "", 9)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 5, "VERODUS INTERNAL BRIEFING", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_x(18)
    pdf.set_font("Inter", "B", 20)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 8.2, "Kim’s meeting read is the real ask. The email is not.")
    pdf.set_x(18)
    pdf.set_font("Inter", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 6, "Kim Chen, 21 August 2026 18:03–18:05  ·  Alignment note")

    pdf.set_y(72)
    pdf.callout(
        "Kim is describing what Joe said in the room: a cut of referred customers, "
        "no competition engine of his own, he needs Verodus’s stack, and he wants the "
        "data. The follow-up email asked for an unpaid Bookmap-style logo. Paper the "
        "meeting. Do not treat the template as the deal."
    )
    pdf.warn(
        "Take the referral if it is a unique code and a share of net evaluation fees. "
        "Do not share trading data. Do not give him the engine as his product. "
        "“Profits” must not mean trader payouts or company P&L."
    )

    pdf.h2("1. Percentage of profits from directing customers")
    pdf.body(
        "Yes — that is the only cash deal worth doing (origination / affiliate). The "
        "email did not write a rate, a SKU, or a tracking code. Force the word profits:"
    )
    add_table(
        pdf,
        ["If he means", "Verodus position"],
        [
            [
                "% of net evaluation fees after refunds and chargebacks, on Instant / 1-Step / Lite he actually sent",
                "Take. 15–25%. Unique code. 90 days.",
            ],
            [
                "% of trader payouts / “profits” on qualified accounts",
                "Refuse. That taxes the reward pool. Referring a buyer who later gets paid is not a claim on payouts.",
            ],
            [
                "% of company profit",
                "Refuse. Not an equity or P&L partner.",
            ],
        ],
        [80, 94],
    )
    pdf.body("Kim’s “directing customers to us” is the right activity. No code, no percentage.")

    pdf.h2("2. He has no trading competition. He needs our engine")
    pdf.body(
        "Yes. Matches the public record. TradeMath championship is a Rolex essay + form. "
        "World Traders Hub HK is email-only. MoniMath PropTrade was announced 18 Nov 2025 "
        "for Jan 2026 with no public Instant / 1-Step / KYC / MT5 / TradeHub / payout stack. "
        "Verodus has the SKUs, rules, platforms, Veriff, fees, resets, and payouts. "
        "Promote a competition is a landing page. Competition engine is the evaluation CRM. "
        "If Verodus agrees, the engine stays yours. His brand can sit on the front later. "
        "Rules unchanged. He does not get a fork of the CRM."
    )

    pdf.h2("3. He wants our data / we share the data")
    pdf.body(
        "He wants it. You do not share it. TAMS is sold as trader behavioral analytics — "
        "the LISG vocabulary. Labeled tickets, pass/fail, daily-loss, Best Day, payout vs "
        "blow-up: Bookmap’s FAQ says they do not ingest the user’s trading activity. A shop "
        "like Verodus is the only place he can get that tape."
    )
    pdf.bullet("Live Privacy: trading-behavior data is not commercialized externally.")
    pdf.bullet("P&L, strategies, and behavior are not shared externally.")
    pdf.bullet("Personal information is not sold.")
    pdf.body(
        "“We share the data” is not available under current policy. Counsel would have to "
        "amend Privacy, put a DPA in place, and you would sell an anonymized license for "
        "cash — not throw it in to make a championship look real. Sharing the tape so he "
        "can run the event trains TAMS and helps him stand up PropTrade off Verodus. "
        "Origination does not require a data feed. Unique codes do."
    )

    pdf.h2("4. Promote competition, no engine")
    pdf.body(
        "Correct. That is the file in one sentence. He sells a 2026/27 HK final and "
        "official-partner language. He needs logo, prize Instant accounts, a cut of "
        "referrals, and if you slip, the data and the stack."
    )

    pdf.h2("One paragraph for Kim")
    pdf.callout(
        "Joe asked in person for a cut of referred customers and for the stack behind a "
        "competition he cannot run. That is real. The email then asked for a free logo "
        "and still thinks we are Bookmap. We take the referral if it is a unique code "
        "and a share of net challenge fees, rules unchanged. We do not share trading "
        "data. We do not give him the engine as his product. If he wants PropTrade, it "
        "runs on our rails and we keep most of the GMV after a 90-day checkout floor."
    )

    pdf.h2("Do not mix these three into one yes")
    pdf.bullet("Referral % — yes, on net eval fees, tracked.")
    pdf.bullet("Engine / PropTrade — later, white-label, Verodus keeps the stack.")
    pdf.bullet("Data — no, unless Privacy is amended and he pays. Not part of 1 or 2.")

    pdf.ln(2)
    pdf.set_font("Inter", "I", 8.2)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.6,
        "Kim Chen chat 21 August 2026 18:03–18:05. Companion: docs/kim-karma-lounge-read.md. "
        "Not an audit and not legal advice. Does not change website copy.",
    )

    for path in (OUT, REPO_OUT, ROOT_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        print(f"Wrote {path} pages={pdf.pages_count} bytes={path.stat().st_size}")


if __name__ == "__main__":
    build()
