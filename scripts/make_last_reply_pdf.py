#!/usr/bin/env python3
"""Render the Verodus–MoniMath briefing (last agent reply) as a PDF."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/opt/cursor/artifacts/verodus_monimath_briefing.pdf")
REPO_OUT = Path("/workspace/docs/verodus-monimath-briefing.pdf")

FONT_DIR = Path("/usr/share/fonts/truetype/macos")
GREEN = (15, 118, 110)
INK = (22, 27, 34)
MUTED = (87, 96, 106)
RULE = (208, 215, 222)
SOFT = (246, 248, 250)
WHITE = (255, 255, 255)
ACCENT_BG = (232, 245, 243)


class BriefingPDF(FPDF):
    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=True, margin=22)
        self.set_margins(18, 18, 18)
        self.add_font("Inter", "", str(FONT_DIR / "Inter-Regular.ttf"))
        self.add_font("Inter", "B", str(FONT_DIR / "Inter-Bold.ttf"))
        self.add_font("Inter", "I", str(FONT_DIR / "Inter-Italic.ttf"))
        self.add_font("Inter", "BI", str(FONT_DIR / "Inter-BoldItalic.ttf"))
        self.add_font("InterM", "", str(FONT_DIR / "Inter-Medium.ttf"))
        self.add_font("InterSB", "", str(FONT_DIR / "Inter-SemiBold.ttf"))

    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(10)
        self.set_font("Inter", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 5, "Verodus  |  MoniMath / Joe Wong briefing", align="L")
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
        self.cell(0, 6, "Confidential  ·  Not a legal opinion or an offer", align="L")
        self.set_xy(18, -12)
        self.cell(0, 6, str(self.page_no()), align="R")

    def h1(self, text):
        self.set_font("Inter", "B", 20)
        self.set_text_color(*INK)
        self.multi_cell(0, 8, text)
        self.ln(2)

    def h2(self, text):
        self.ln(4)
        y = self.get_y()
        if y > 262:
            self.add_page()
            y = self.get_y()
        self.set_fill_color(*GREEN)
        self.rect(18, y + 1.2, 2.2, 6.4, "F")
        self.set_x(23)
        self.set_font("InterSB", "", 13)
        self.set_text_color(*INK)
        self.multi_cell(0, 8, text)
        self.ln(1.5)

    def body(self, text):
        self.set_font("Inter", "", 10)
        self.set_text_color(*INK)
        needed = 5.4 * max(1, len(self.multi_cell(0, 5.4, text, dry_run=True, output="LINES")))
        if self.get_y() + needed > 275:
            self.add_page()
        self.multi_cell(0, 5.4, text)
        self.ln(1.6)

    def italic(self, text):
        self.set_font("Inter", "I", 10)
        self.set_text_color(*MUTED)
        self.multi_cell(0, 5.4, text)
        self.ln(1.6)

    def bullet(self, text, indent=6):
        x = 18 + indent
        self.set_x(x)
        self.set_font("Inter", "B", 10)
        self.set_text_color(*GREEN)
        self.cell(4, 5.4, "•")
        self.set_font("Inter", "", 10)
        self.set_text_color(*INK)
        self.multi_cell(192 - x - 4, 5.4, text)
        self.ln(0.4)

    def numbered(self, n, text):
        self.set_x(24)
        self.set_font("InterSB", "", 10)
        self.set_text_color(*GREEN)
        self.cell(7, 5.4, f"{n}.")
        self.set_font("Inter", "", 10)
        self.set_text_color(*INK)
        self.multi_cell(161, 5.4, text)
        self.ln(0.5)

    def callout(self, text):
        self.ln(1)
        start = self.get_y()
        self.set_x(22)
        self.set_font("InterM", "", 10.5)
        self.set_text_color(*INK)
        self.multi_cell(168, 5.8, text)
        end = self.get_y()
        self.set_fill_color(*ACCENT_BG)
        self.set_draw_color(*GREEN)
        self.set_line_width(0.6)
        # redraw behind: use a rectangle then reprint is messy; draw left bar
        self.set_line_width(1.6)
        self.line(18.8, start - 1.5, 18.8, end + 1.2)
        self.set_line_width(0.2)
        self.ln(3)

    def kv(self, label, value):
        self.set_x(24)
        self.set_font("InterSB", "", 10)
        self.set_text_color(*INK)
        self.cell(32, 5.4, label)
        self.set_font("Inter", "", 10)
        self.set_text_color(*INK)
        self.multi_cell(136, 5.4, value)
        self.ln(0.3)


def draw_cover(pdf: BriefingPDF):
    pdf.add_page()
    pdf.set_fill_color(*GREEN)
    pdf.rect(0, 0, 210, 8, "F")
    pdf.set_fill_color(*SOFT)
    pdf.rect(0, 8, 210, 62, "F")

    pdf.set_y(18)
    pdf.set_font("Inter", "", 9)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 6, "VERODUS INTERNAL BRIEFING", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_x(18)
    pdf.set_font("Inter", "B", 24)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 10, "Joe Wong, MoniMath, and how Verodus should get paid")
    pdf.ln(1)
    pdf.set_font("Inter", "", 11)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        6,
        "Research summary and commercial proposal  ·  20 August 2026",
    )

    pdf.set_y(82)
    pdf.callout(
        "Joe Wong is MoniMath’s co-founder. The deal worth doing is sell him "
        "anonymized CRM data for cash, and sell him Asia traffic into unchanged "
        "Verodus challenges. Do not give him data for “exposure,” and do not help "
        "him raise pass rates on the core book."
    )


def add_table(pdf: BriefingPDF, headers, rows, col_widths):
    usable = 174
    if sum(col_widths) != usable:
        scale = usable / sum(col_widths)
        col_widths = [w * scale for w in col_widths]

    line_h = 5.0
    pdf.set_font("InterSB", "", 8)
    # header
    if pdf.get_y() > 250:
        pdf.add_page()
    x0 = 18
    y = pdf.get_y()
    pdf.set_fill_color(*GREEN)
    pdf.set_text_color(*WHITE)
    x = x0
    # measure header height
    header_h = 8
    pdf.set_xy(x0, y)
    pdf.rect(x0, y, usable, header_h, "F")
    x = x0
    for i, h in enumerate(headers):
        pdf.set_xy(x + 1.5, y + 1.6)
        pdf.multi_cell(col_widths[i] - 3, 4.4, h)
        x += col_widths[i]
    y += header_h

    pdf.set_font("Inter", "", 8)
    pdf.set_text_color(*INK)
    for r_i, row in enumerate(rows):
        # estimate height
        heights = []
        for i, cell in enumerate(row):
            pdf.set_font("Inter", "B" if i == 0 else "", 8)
            n = pdf.multi_cell(col_widths[i] - 3, line_h, cell, dry_run=True, output="LINES")
            heights.append(max(1, len(n)) * line_h + 2.4)
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
            pdf.set_xy(x + 1.5, y + 1.2)
            pdf.set_font("Inter", "B" if i == 0 else "", 8)
            pdf.set_text_color(*INK)
            pdf.multi_cell(col_widths[i] - 3, line_h, cell)
            x += col_widths[i]
        y += h
    pdf.set_y(y + 3)


def build():
    pdf = BriefingPDF()
    draw_cover(pdf)

    pdf.h2("Who he actually is")
    pdf.body(
        "The person attached to trademath.ai / MoniMath is Joe Wong, Hong Kong, "
        "LinkedIn joe-wong-55b3ab262. He is not the comedian Huang Xi and not "
        "Fed Guy Joseph Wang."
    )
    pdf.body("Public record:")
    pdf.bullet(
        "1995–2017: claims commodities / financial trading, including Emperor Group "
        "in Hong Kong (not independently verified)."
    )
    pdf.bullet(
        "2017–2022: COO of Xerbal Group (hemp / extraction oil, Canada–EU). The US "
        "patent he is associated with is assigned to Xerbal USA; the inventor of "
        "record is Peter Matravers, not him."
    )
    pdf.bullet(
        "2022–present: founder of LISG, an AI smoking-cessation clinic. That is where "
        "the “behavioral data analytics” language comes from."
    )
    pdf.bullet(
        "MIT Sloan AI credential is a ~6-week online executive certificate, not a degree."
    )
    pdf.body(
        "Pattern: partnership operator (commodities → hemp → wellness AI → trading AI). "
        "Useful as a door into HK / Greater China. Not someone to hand raw edge or unpaid exclusivity."
    )

    pdf.h2("What MoniMath is trying to do")
    pdf.body("Strip the website and the plan is:")
    pdf.numbered(1, "Get trader behavioral data (this is the Verodus ask).")
    pdf.numbered(
        2,
        "Wrap it in TAMS (deep learning + behavioral overlay) for education, coaching, then a fund story.",
    )
    pdf.numbered(
        3,
        "Stand up MoniMath PropTrade (announced for January 2026: education + automation + funding).",
    )
    pdf.numbered(
        4,
        "Use academy / “championship” language as top-of-funnel in China / Asia.",
    )
    pdf.body(
        "Public footprint is thin. trademath.ai is a 2026 WordPress.com marketing site. "
        "The TAMS page still has leftover Linear.app template copy (“Linear simplifies "
        "software project management…”). The championship page is a Rolex essay plus a "
        "contact form. About-page metrics (10K+ asset classes, 10K+ members) are not serious. "
        "LinkedIn posts claiming “SFC approval” for an algo fund sit next to a website that "
        "only says they partner with SFC licensees — and they mislabel Type 2 as “Advising on "
        "Securities” (that is Type 4; Type 2 is futures dealing)."
    )
    pdf.body("They need Verodus more than Verodus needs them.")

    pdf.h2("Why this can still make Verodus money")
    pdf.body(
        "Verodus economics are evaluation fees, resets, and bounded payouts. A partnership "
        "that “makes better traders” is a cost unless volume or new cash more than offsets it."
    )
    pdf.body(
        "MoniMath wanting data is the clean fit. Data cash does not raise pass rates. Asia "
        "origination into the same rules increases the number of people who buy and fail. "
        "Education only works as a paid optional add-on, never as a required path."
    )

    add_table(
        pdf,
        ["Layer", "What you sell", "How you get paid", "Effect on failure fees"],
        [
            [
                "A. Data",
                "Anonymized pass/fail, drawdown paths, behavioral features",
                "Setup + monthly license",
                "Neutral / extra cash",
            ],
            [
                "B. Asia origination",
                "Standard Verodus challenges via their funnel",
                "15–25% of their tagged fees; you keep the rest",
                "Positive: more buyers, same fail rate",
            ],
            [
                "C. White-label",
                "Their PropTrade runs on Verodus rails",
                "You keep ~80% of that GMV",
                "Positive, and stops a clone",
            ],
            [
                "D. Academy add-on",
                "Optional coaching at checkout",
                "~50/50",
                "Extra margin; core product untouched",
            ],
        ],
        [32, 52, 48, 42],
    )
    pdf.body(
        "Illustrative Year-1 shape if they actually send traffic: data on the order of "
        "USD 100k+, plus the bulk of any Asia challenge GMV after a 20% affiliate. Even a "
        "weak origination book still beats “free data for a co-brand.”"
    )

    pdf.h2("Data sale: CRM yes, public policy currently no")
    pdf.body(
        "The CRM being allowed to sell data is necessary, not sufficient. Verodus’s live "
        "privacy policy says trading-behavior data is not commercialized externally and is "
        "shared internally only. It also says Verodus does not sell personal information."
    )
    pdf.body("What you can sell after counsel amends the policy:")
    pdf.bullet(
        "Irreversibly anonymized account-level labels and features (pass/fail, breach type, "
        "sizing volatility, news-window flags, consistency / best-day, session mix)."
    )
    pdf.bullet("Aggregated research tables.")
    pdf.body("What you should not sell even then:")
    pdf.bullet("KYC, names, wallets, IPs, device IDs.")
    pdf.bullet("Raw tickets that let them copy-trade your best funded accounts.")
    pdf.bullet("Anything they can use to rebuild your risk engine and launch a clone.")
    pdf.body(
        "Condition precedent: privacy/terms update + anonymization spec + DPA before SKU-2 "
        "data leaves the building."
    )

    pdf.h2("Proposed deal to put in front of him")
    pdf.numbered(
        1,
        "90-day paid pilot: USD 20k–35k for a capped anonymized lifecycle extract (no funded-survival pack).",
    )
    pdf.numbered(
        2,
        "Year 1: ~USD 8k–15k/month for lifecycle + behavioral features; survival pack extra.",
    )
    pdf.numbered(
        3,
        "Origination: 20% of net fees on tagged Asia checkouts. No share of funded payouts.",
    )
    pdf.numbered(
        4,
        "If they want PropTrade: it runs exclusively on Verodus for 24 months, or they do not get the rich data.",
    )
    pdf.numbered(
        5,
        "Non-compete: no competing challenge product trained on Verodus data.",
    )
    pdf.body(
        "Walk away if they want a free dump, will not name the SFC counterparty, want "
        "exclusivity without a six-figure minimum, or want raw tickets plus identity keys."
    )

    pdf.h2("What to consider before you shake hands")
    pdf.bullet(
        "They are a would-be competitor. Structure them as a customer (data buyer + affiliate "
        "+ optional white-label), not as a strategic equal."
    )
    pdf.bullet(
        "“SFC approved fund” is unverified and inconsistent. Do not let Verodus be named on those materials."
    )
    pdf.bullet(
        "China championship / provincial marketing is a separate legal problem (payments, "
        "promotions, cross-border). Do not green-light mainland campaigns from a slide."
    )
    pdf.bullet(
        "Jane Street / “institutional” language on their site is name-dropping. Keep Verodus off it."
    )
    pdf.bullet(
        "Residual model rights after termination: prefer none, or a buyout. Otherwise you train "
        "TAMS once and they keep the value."
    )

    pdf.h2("Ten questions for the next call")
    questions = [
        "Which legal entity signs, and who owns it?",
        "Exact SFC licensee and CE number behind “MoniMath Capital”?",
        "Who is the Canada-listed partner?",
        "Is PropTrade a Verodus white-label conversation, or are you already talking to other prop-tech vendors?",
        "Do you need account-level features or ticket-level tape?",
        "Will you pay a license fee / minimum, or only “revenue share later”?",
        "How many unique traders are in your CRM today?",
        "Are you buying data, origination, rails, or all three?",
        "If we stop, do your models keep the data?",
        "Will you accept a non-compete on a competing challenge product?",
    ]
    for i, q in enumerate(questions, 1):
        pdf.numbered(i, q)
    pdf.body(
        "If 2, 4, 6, and 10 are soft, stay on affiliate-only and do not open the data room."
    )

    pdf.h2("Bottom line")
    pdf.callout(
        "He needs labeled prop-trader behavior and a working evaluation stack. You have both. "
        "Charge for the data, take the Asia flow on your existing rules, and rent him the rails "
        "if he wants a prop program. That is exposure and profit. A free partnership that "
        "“improves traders” is not."
    )

    pdf.ln(4)
    pdf.set_font("Inter", "I", 8.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.8,
        "Sources used for this briefing include trademath.ai, trademath.ai/monimath/, "
        "Joe Wong’s LinkedIn (PropTrade and SFC posts), lisg.ai, USPTO patent US11602701B2, "
        "SFC licensing handbook (Type 1/2/4/9), MIT Sloan executive-education course pages, "
        "and Verodus public site / privacy policy / terms. This document is an internal "
        "commercial memo, not legal advice.",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPO_OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    pdf.output(str(REPO_OUT))
    print(f"Wrote {OUT}")
    print(f"Wrote {REPO_OUT}")
    print(f"pages={pdf.pages_count} bytes={OUT.stat().st_size}")


if __name__ == "__main__":
    build()
