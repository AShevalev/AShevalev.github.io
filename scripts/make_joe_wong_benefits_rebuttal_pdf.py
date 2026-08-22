#!/usr/bin/env python3
"""PDF: mark-up of the generic lead-gen + HK credibility read of Joe's email."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/opt/cursor/artifacts/Joe_Wong_Benefits_Memo_Rebuttal.pdf")
REPO_OUT = Path("/workspace/docs/joe-wong-generic-benefits-rebuttal.pdf")
ROOT_OUT = Path("/workspace/joe-wong-benefits-rebuttal.pdf")

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
        self.cell(0, 5, "Joe Wong  |  Rebuttal of the generic benefits memo", align="L")
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
    pdf.rect(0, 8, 210, 58, "F")
    pdf.set_y(16)
    pdf.set_font("Inter", "", 9)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 5, "VERODUS INTERNAL BRIEFING", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_x(18)
    pdf.set_font("Inter", "B", 20)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 8.2, "The generic benefits memo is the wrong deal")
    pdf.set_x(18)
    pdf.set_font("Inter", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        6,
        "Mark-up of lead-gen / HK credibility / education / competition branding  ·  22 August 2026",
    )

    pdf.set_y(78)
    pdf.callout(
        "Keep three sentences: the email is a Bookmap template; official long-term partner "
        "is not a deal; start with a measured pilot, not exclusivity."
    )
    pdf.warn(
        "Throw out the value thesis. It models Joe’s unverified headcount and halo as "
        "Verodus’s upside. For a Dubai FZ simulated-evaluation shop, that halo is the "
        "liability. The only number that matters is tagged Instant / 1-Step / Lite "
        "checkouts on unchanged rules. Do not take a clarifying call until he sends a "
        "one-pager that could only have been written for Verodus."
    )

    pdf.h2("What that memo gets right")
    add_table(
        pdf,
        ["Line in that memo", "Why it survives"],
        [
            [
                "Value is in execution details, not official long-term partner.",
                "Correct. The email offers a logo.",
            ],
            [
                "Bookmap / order-flow leftover means they did not research Verodus.",
                "Correct. Same class as TradeMath’s old Linear.app leftovers.",
            ],
            [
                "Start narrow. Do not give away product without measurable return.",
                "Correct. 90-day unique-code pilot.",
            ],
            [
                "Prop firms live on challenge volume.",
                "Category-true. Not proof he can send volume.",
            ],
            [
                "25%/40% returns and the 1,700-person Saudi story need verification.",
                "Correct — then the memo still uses those numbers as the TAM. Stop.",
            ],
            [
                "OHKF is a policy think tank, not a fund vehicle.",
                "Correct. Then do not treat OHKF as a credibility asset for Verodus.",
            ],
        ],
        [82, 92],
    )

    pdf.h2("Wrong geography, wrong buyer")
    pdf.body(
        "The memo is written as if Verodus were a North American prop shop hunting an HK "
        "halo. Verodus is Verodus L.L.C.-FZ (Dubai), payments via Verodus Capital Inc., "
        "~3,000 users, 175+ countries already. Joe cannot add a geography Verodus does not "
        "already sell into. He can only add named buyers, if they hit checkout with a code."
    )

    pdf.h2("1. Lower CAC off 10,000 traders and a 1,700-person Saudi event")
    pdf.body(
        "Category true, inputs false. TradeMath About still claims 10k members, 10k asset "
        "classes, 10M+ backtests, 50+ networks, a Jane Street framework — with the metric "
        "row duplicated and mislabeled. MoniMath LinkedIn posts still get ~3–5 reactions. "
        "The 2025 Saudi-government 1,700 claim has no public TradeMath / Joe / World Traders "
        "Hub match. Nearest public shape is Algo Challenge Association at Money20/20 Riyadh; "
        "they are not on the sponsor list; prizes ~USD 2k. Championship on his site is a "
        "Rolex essay + form. That is not a pre-filtered challenge buyer."
    )
    pdf.body(
        "CAC falls only if unique-code checkouts beat paid UA after refunds and chargebacks. "
        "Model 20 / 100 / 500 Instant at $49, not 10,000. Twenty tagged Instant checkouts in "
        "90 days is about $980 gross. Official partner status with no unique code and no "
        "net-fee share is the unpaid logo he asked for. That raises CAC in disguise."
    )

    pdf.h2("2. Asia / Hong Kong credibility signal — this is the trap")
    pdf.bullet(
        "Our Hong Kong Foundation is real (Tung Chee-hwa). No public page ties it to Joe, TradeMath, MoniMath, or World Traders Hub HK. Repeat it next to Verodus and you own the sentence."
    )
    pdf.bullet(
        "MoniMath Capital SFC approval is a 20 Nov 2025 LinkedIn post (~3 reactions). The live site says partners with Types 1/2/9, mislabels Type 2 as Advising on Securities (that is Type 4), and names no CE number. LinkedIn approval vs site partners is a contradiction, not a plus."
    )
    pdf.bullet(
        "Marketing claims around institutional-grade partnerships are exactly what Verodus must not do. Intros to unnamed platforms, mentors, and BofA / Crédit Lyonnais / RBC / KPMG executive members: names or drop."
    )

    pdf.h2("3. Education synergy — optional upsell, never a pathway")
    pdf.body(
        "TradeMath’s Level 1–4 ladder is still duplicated/broken. No named faculty. Making "
        "the course a gate to Instant kills the $49 impulse purchase, lets Joe capture the "
        "course fee while Verodus takes KYC/support/payouts, and can raise pass rates — "
        "which hurts fail-fee P&L if you also loosen rules for the championship. Co-branded "
        "content is free advertising of his academy unless it ends in a tagged checkout."
    )

    pdf.h2("4. Competition branding — common in the sector, not free here")
    pdf.bullet("Prize inventory = capped Instant or named 1-Step/Lite evaluation accounts, rules unchanged. Not live capital. Not uncapped 2-Step Pro.")
    pdf.bullet("Data on participant performance is either his essay-form junk or your tickets / P&L / behavior. Privacy still bans external commercialization. Do not volunteer a feed.")
    pdf.bullet("A 2027 HK final with no venue, no Companies Registry number, and no OHKF letter is a landing page. If he wants brand in HK he buys a cash sponsorship with written confirmation. He has not offered to buy it.")

    pdf.h2("5. Secondary angles — what they named vs what they missed")
    add_table(
        pdf,
        ["Angle in that memo", "Reality"],
        [
            [
                "Order-flow / MT5-Android technical integration",
                "Verodus has Platform 5 (MT5, not for US) + TradeHub. It is not Bookmap. Do not build to leftover template copy.",
            ],
            [
                "European Chamber / HSBC unnamed leads",
                "Unnamed. Same as the bank list.",
            ],
            [
                "Licensed funds / AUM adjacency",
                "25%/40% for six years is unverified. Even if true, Verodus does not take AUM and must not imply it does.",
            ],
            [
                "Missed by that memo",
                "MoniMath PropTrade (announced 18 Nov 2025, kickoff Jan 2026), no public live stack. Actual secondary: his PropTrade on Verodus rails after a checkout floor. Verodus keeps most GMV.",
            ],
        ],
        [62, 112],
    )

    pdf.h2("Dissolved company of a similar name")
    pdf.body(
        "Could not confirm a dissolved World Traders Hub HK tied to Joe. Public name "
        "collisions exist and are unrelated (World Trading Hub PPE, UAE Traders Hub). Do "
        "not treat a similar-name dissolved vehicle as diligence. Ask for the Hong Kong "
        "Companies Registry number and a current-status printout. Until then it is a letterhead."
    )

    pdf.h2("Rewrite of their next steps")
    add_table(
        pdf,
        ["Their step", "Do this instead"],
        [
            [
                "Request audited 25%/40% and 2025 competition partners as if that unlocks a prop deal",
                "Irrelevant to Instant checkout. Halo in joint copy requires SFC CE numbers, an OHKF contact, and the Saudi organizer. Otherwise those names never appear next to Verodus.",
            ],
            [
                "Clarify Bookmap; confirm they understand Verodus is a prop firm",
                "One paragraph in writing: simulated evaluations, Instant / 1-Step / Lite, no deposits, no client funds, no brokerage, no order-flow tool. If the next note still cannot name those SKUs, stop.",
            ],
            [
                "Limited co-marketing around one competition stage",
                "Only with a unique code, 15–25% of net eval fees, 90 days, no exclusivity, rules unchanged.",
            ],
            [
                "Short clarifying call on mutual economics (low-cost)",
                "Not low-cost. It spends another meeting on a template. Paper first. Call only to walk a Verodus-specific one-pager.",
            ],
            [
                "Protect brand and economics",
                "Named: no unpaid logo, no SFC/OHKF/Saudi/Jane Street adjacency, no required education, no data dump, no custom championship rules.",
            ],
        ],
        [72, 102],
    )

    pdf.h2("Bottom line vs theirs")
    pdf.body(
        "Theirs: most realistic near-term value is a lower-cost Asia channel plus a "
        "credibility boost from HK institutional framing."
    )
    pdf.callout(
        "Ours: the only realistic near-term value is tagged challenge fees. The HK "
        "institutional framing is the part you refuse to repeat. Credibility for Verodus "
        "is payout proof and careful copy, not Joe’s think-tank sentence. If the generic "
        "memo is used as the internal brief, Verodus will negotiate logo + education + halo "
        "— which is what he wants — instead of net-fee origination, which is the only "
        "thing that pays."
    )

    pdf.ln(2)
    pdf.set_font("Inter", "I", 8.2)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.6,
        "Companion: docs/joe-wong-generic-benefits-rebuttal.md, docs/joe-wong-fresh-analysis.md, "
        "docs/joe-wong-email-analysis.md. Sources as of 21–22 August 2026. Not an audit and "
        "not legal advice. Does not change website copy.",
    )

    for path in (OUT, REPO_OUT, ROOT_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        print(f"Wrote {path} pages={pdf.pages_count} bytes={path.stat().st_size}")


if __name__ == "__main__":
    build()
