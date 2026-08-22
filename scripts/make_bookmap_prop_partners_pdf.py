#!/usr/bin/env python3
"""PDF: Bookmap's four named prop-firm pairings for Alexander."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/opt/cursor/artifacts/Bookmap_Prop_Firm_Partners.pdf")
REPO_OUT = Path("/workspace/docs/bookmap-prop-firm-partners.pdf")
ROOT_OUT = Path("/workspace/bookmap-prop-firm-partners.pdf")

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
        self.cell(0, 5, "Bookmap prop-firm pairings  |  10FOUR · TickTickTrader · TTP · EdgeProp", align="L")
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
        if y > 255:
            self.add_page()
            y = self.get_y()
        self.set_fill_color(*GREEN)
        self.rect(18, y + 1.0, 2.2, 5.8, "F")
        self.set_x(23)
        self.set_font("InterSB", "", 12.5)
        self.set_text_color(*INK)
        self.multi_cell(0, 7.4, text)
        self.ln(1.0)

    def h3(self, text):
        if self.get_y() > 262:
            self.add_page()
        self.set_font("InterSB", "", 10.5)
        self.set_text_color(*GREEN)
        self.multi_cell(0, 6.2, text)
        self.ln(0.6)

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
    line_h = 4.4
    if pdf.get_y() > 240:
        pdf.add_page()
    x0, y = 18, pdf.get_y()
    pdf.set_fill_color(*GREEN)
    pdf.set_text_color(*WHITE)
    pdf.set_font("InterSB", "", 7.2)
    header_h = 8
    pdf.rect(x0, y, usable, header_h, "F")
    x = x0
    for i, h in enumerate(headers):
        pdf.set_xy(x + 1.2, y + 1.6)
        pdf.multi_cell(col_widths[i] - 2.4, 4.4, h)
        x += col_widths[i]
    y += header_h
    for r_i, row in enumerate(rows):
        heights = []
        for i, cell in enumerate(row):
            pdf.set_font("Inter", "B" if i == 0 else "", 7.2)
            n = pdf.multi_cell(col_widths[i] - 2.4, line_h, cell, dry_run=True, output="LINES")
            heights.append(max(1, len(n)) * line_h + 1.8)
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
            pdf.set_xy(x + 1.2, y + 1.0)
            pdf.set_font("Inter", "B" if i == 0 else "", 7.2)
            pdf.set_text_color(*INK)
            pdf.multi_cell(col_widths[i] - 2.4, line_h, cell)
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
    pdf.set_font("Inter", "B", 20)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 8.0, "Bookmap’s four named prop-firm pairings")
    pdf.set_x(18)
    pdf.set_font("Inter", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        6,
        "10FOUR  ·  TickTickTrader  ·  Trade The Pool  ·  EdgeProp Trading   ·   22 August 2026   ·   For Alexander",
    )

    pdf.set_y(74)
    pdf.callout(
        "Bookmap does not become the evaluation engine in any of these deals. "
        "Bookmap sells heatmap seats. The prop firm sells challenge fees and simulated payouts. "
        "Joe’s email inverted that: Verodus was described as order-flow visualization."
    )
    pdf.warn(
        "None of the four is MT5 / TradeHub / forex-indices-crypto. None is publicly tied to "
        "Joe Wong, TradeMath, MoniMath, or World Traders Hub HK. A Verodus × Bookmap seat "
        "deal would be a cost line, not origination."
    )

    pdf.h2("Four commercial shapes, not one")
    add_table(
        pdf,
        ["Firm", "Pairing", "Who pays Bookmap", "Connect"],
        [
            [
                "EdgeProp",
                "Named co-brand + coupon BOOKMAP30 (Feb 2026)",
                "EdgeProp: one included license per account (Bookmap or ATAS or Jigsaw or WealthCharts or tradesea)",
                "Rithmic inside Bookmap. Can execute futures from the heatmap.",
            ],
            [
                "10FOUR",
                "Named co-brand 11 Aug 2026 — 10 days before Joe emailed you",
                "The trader. Bookmap’s page: “Purchase and install Bookmap.”",
                "Alongside TradingView + CQG as analysis. Not the account UI.",
            ],
            [
                "Trade The Pool",
                "Listed on TTP’s partners page. No bookmap.com/en/partner page",
                "TTP for 30 days (terms) / 45 days (blog) on Super/Extra/Ultimate. Trader pays after funded.",
                "Stock/ETF heatmap perk. Execution is TraderEvolution.",
            ],
            [
                "TickTickTrader",
                "Historical free Bookmap + Jigsaw bundle. No live partner page",
                "Firm, when the promo was live",
                "Rithmic / CQG / historically Tradovate. Firm now looks stalled.",
            ],
        ],
        [28, 48, 52, 46],
    )
    pdf.body(
        "Closest category analogue to Verodus Instant is 10FOUR (HK entity, Instant SKU, 90% language, Riseworks). "
        "Closest documented co-marketing template is EdgeProp. Trade The Pool is a time-boxed trial. "
        "TickTickTrader is the cautionary tale: a Bookmap bundle does not keep a firm alive after it loses feeds."
    )

    pdf.h2("How Bookmap sells into props")
    pdf.body(
        "Public page: bookmap.com/en/b2b/prop-firms. Pitch: bulk licenses, record/replay for coaching, "
        "retention (“traders return for more evaluations”), Rithmic / Tradovate / NinjaTrader. "
        "Two different things get called a “Bookmap prop firm”:"
    )
    pdf.bullet("Official B2B pair — Bookmap or CRO Ryan Hansen says “officially partnered,” often with a bookmap.com/en/partner/… page and/or a coupon.")
    pdf.bullet("Rithmic compatibility — the firm issues Rithmic credentials; the trader buys Bookmap. Apex publishes a connection guide. That is not a Bookmap commercial partnership.")
    pdf.body(
        "The four names below sit in the first bucket (or, for TickTickTrader, sat there as a bundled perk). "
        "Do not mix in Apex / Lucid / Tradeify unless someone produces a Bookmap co-brand page."
    )

    pdf.h2("1. 10FOUR — official pair, 11 August 2026")
    pdf.body(
        "Announced ten days before Joe’s Verodus email. Joe is in Hong Kong. 10FOUR is a Hong Kong–registered "
        "futures Instant shop. It is the live analogue sitting in the market when he hit send. It is not in his email. It is not Verodus."
    )
    add_table(
        pdf,
        ["Item", "Fact"],
        [
            ["Site / operator", "10four.com. Ten Four Group, HK CR 79713385, Unit D, 20/F Infotech Centre, 21 Hung To Road, Kwun Tong."],
            ["Bookmap “About”", "Says founded 2026, HQ Chicago. Treat as marketing. Independent write-ups name the HK company as operator."],
            ["CEO", "Christian Jensen. LinkedIn: Limassol. Launch ~8 Jul 2026. Earlier posts about taking the business to the US."],
            ["Product", "Futures sim-prop. INSTANT (straight-to-funded), ORIGIN (1-step EOD trail, no daily loss on eval), DAILY (funded can withdraw every trading day)."],
            ["Sizes / split", "$25k / $50k / $100k / $150k. No $200k Instant. 90/10 from first withdrawal. Discretionary Path to Live 80/20 in reviews."],
            ["Stack", "CQG data. CQG Desktop or TradingView + StoneX. Not Rithmic. Not MT5."],
            ["Payouts", "Riseworks ACH/crypto. 24-hour processing claim. Min ~$250 DAILY / ~$500 ORIGIN and INSTANT."],
            ["Consistency", "50% ORIGIN eval, 40% DAILY eval, 25% each INSTANT payout. No consistency on funded ORIGIN/DAILY — the line Bookmap repeats."],
            ["Independent", "PropFirmMap D / ~3.2, 1 Trustpilot review, composite 29/100 F as of 17 Aug 2026. New shop. Not a recommendation."],
        ],
        [36, 138],
    )
    pdf.h3("The Bookmap deal — read their own page")
    pdf.body(
        "bookmap.com/en/partner/10four. Headline: “Trade Futures with 10FOUR and Bookmap.” "
        "What you get is 10FOUR’s product copy (90% split, daily payouts, no funded consistency, CQG). "
        "Connect copy is weaker than EdgeProp’s: “At present, traders use Bookmap alongside 10FOUR’s "
        "TradingView-based trading environment… while traders manage their evaluation or funded account "
        "through 10FOUR’s existing infrastructure.” Steps: purchase a 10FOUR eval, purchase and install Bookmap, set up the workflow."
    )
    pdf.body(
        "This is co-marketing, not a free seat. Bookmap LinkedIn 11 Aug 2026 (Hansen reshare 13 Aug, Jensen comment): "
        "traders use Bookmap while trading a 10FOUR evaluation or funded account."
    )
    pdf.h3("Vs Verodus")
    pdf.body(
        "Same category language (Instant, 90%, Rise, sim eval). Different market (US futures vs forex-indices-crypto), "
        "different stack (CQG / TradingView vs Platform 5 / TradeHub), different size ladder ($25k–$150k vs your "
        "$5k–$200k 2-Step and Instant without $200k). 10FOUR is a competitor category, not a partner Joe has on paper."
    )

    pdf.h2("2. TickTickTrader — historical bundle, firm looks stalled")
    pdf.body(
        "This is the pairing that looks most like “we give traders Bookmap for free.” It did not make the firm durable. "
        "Bundled heatmap seats are a cost/perk, not origination, and they do not survive a lost data feed."
    )
    add_table(
        pdf,
        ["Item", "Fact"],
        [
            ["Site / entity", "tickticktrader.com. TickTickTrader Ltd, Isle of Man 137735C, Douglas. Also named: UAB Lithuania; Romania/Bucharest ops."],
            ["CEO / founded", "Often named Gerardo Tolivia Mariscal. ~Feb 2022."],
            ["Product (when alive)", "Futures sim-prop. S2F / S2F+ evals, TTTDirect instant. Recurring monthly eval fees in some write-ups (~$145–$285/mo)."],
            ["Distinctive", "Reported 100% split first ~3 months then 90%. $250 min payout. No algo/EA. Physical floors / Quantum Quest Abu Dhabi (JoinProp)."],
            ["Bookmap deal", "Independent reviews: complimentary Bookmap + Jigsaw DayTradr licenses (~$99–$150/mo retail each) as a conversion perk. Connect via Rithmic. No live bookmap.com/en/partner page (404)."],
        ],
        [36, 138],
    )
    pdf.h3("Status as of mid-2026 — do not treat as a going concern")
    pdf.body(
        "JoinProp last updated 11 Aug 2026, last full review 15 Jul 2026: every plan on TTT’s own homepage marked "
        "“Coming soon.” Not selling. Reported sequence: Tradovate suspends TTT Nov 2025 (firm cited operational "
        "constraints) and migrates to Project X; Project X goes Topstep-exclusive Feb 2026; some May 2026 FAQs still "
        "list a leftover Rithmic + Bookmap path. Unpaid-data allegations in secondary reporting, not confirmed here. "
        "TradingFunder 24 May 2026: same “Coming soon.” Verify tickticktrader.com live before anyone treats TTT as a current Bookmap B2B reference."
    )
    pdf.h3("Lesson")
    pdf.body(
        "A named Bookmap perk is not a moat. If Joe offers “we’ll throw Bookmap in,” ask who pays the seat, which feed "
        "it sits on, and what happens when that feed is withdrawn. Verodus cannot bolt Bookmap onto Platform 5 the way TTT bolted it onto Rithmic."
    )

    pdf.h2("3. Trade The Pool — partners-page trial, stocks not futures")
    pdf.body(
        "Bookmap as a 30–45 day evaluation perk next to Trade Ideas and TrendSpider. After funded, the trader pays. "
        "TTP’s partners page is the cleanest public example of Bookmap sitting in a tool rack, not as the prop firm."
    )
    add_table(
        pdf,
        ["Item", "Fact"],
        [
            ["Site / product", "tradethepool.com. Stock/ETF prop. ~12,000 names. Day or swing. Not futures, not forex/CFD Instant."],
            ["People / parent", "Founded Sep 2022. Michael Katz (CPO). Backed by The5ers / Five Percent Online Ltd (Gil Ben Hur). HQ Raanana + London."],
            ["Execution", "TraderEvolution. IB-style real stocks in independent write-ups."],
            ["Split / payouts", "Often 70/30; some plans 60–80% in reviews. ~14 days, min ~$300 (program terms)."],
            ["Trust", "~4.4 Trustpilot / 500+ reviews — the only firm in this four with a real review corpus."],
            ["Restriction", "Israel residents restricted despite HQ. Same forbidden-territory pattern as The5ers."],
        ],
        [36, 138],
    )
    pdf.h3("The Bookmap deal — their own documents")
    pdf.bullet("Partners page: Bookmap listed with Trade Ideas, TrendSpider, TraderSync, Tradervue. CTA: 30 days free trial with BookMap.")
    pdf.bullet("Program terms: Super/Extra/Ultimate (excluding Mini BP) get FREE Trade-Ideas or TrendSpider or BookMap for 30 days. Once funded, the user pays if they want to keep it.")
    pdf.bullet("Marketing article 5 Feb 2024: 45 days free during evaluation on Super/Extra/Ultimate. Treat 30 days (terms) vs 45 days (blog) as a copy mismatch; terms win if they conflict.")
    pdf.bullet("One-per-user booster rule: Bookmap is not a stack of free seats.")
    pdf.body(
        "No bookmap.com/en/partner/trade-the-pool page (404). This is a firm-side partnership listing, not Bookmap’s co-brand microsite. "
        "Wrong asset class for Verodus. Useful only as proof that Bookmap’s prop motion includes time-boxed trials that convert to the trader paying SaaS."
    )

    pdf.h2("4. EdgeProp Trading — cleanest documented co-marketing template")
    pdf.body(
        "This is the pairing you can screenshot. Bookmap hosts the page, prints a coupon, tells the trader to connect "
        "Rithmic inside Bookmap, and the firm’s help center says the license is included. Roles stay split. This is what a competent two-vendor letter looks like."
    )
    add_table(
        pdf,
        ["Item", "Fact"],
        [
            ["Site / Bookmap page", "edgeproptrading.com. bookmap.com/en/partner/edge-prop. LinkedIn ~17–18 Feb 2026."],
            ["Entity", "Romania Trade Registry J2025014346001. Site: Bucharest + Chicago. Bookmap “About”: founded 2024, HQ Romania."],
            ["Product", "Futures sim-prop, one-step. EdgeCore (intraday trail), EdgeOne (EOD), EdgeX (EOD). $50k–$200k. No daily loss limit. 7 min trading days. CME family; EUREX temporarily unavailable."],
            ["Split / promo", "100% to $5k, then 90/10. Weekly payouts. Up to 5 funded accounts. Live promo NOFEE40; EdgeX ~$90–$270."],
            ["Scale (self-claim)", "3,000+ traders, $350k+ paid in 2026. Young firm. Thin Trustpilot corpus (~8 reviews on the public page)."],
            ["Disclaimer", "Not a brokerage. Accounts fully simulated. No forex / CFDs / stocks / options / crypto."],
        ],
        [36, 138],
    )
    pdf.h3("The Bookmap deal — primary sources")
    pdf.bullet("Bookmap page: Bookmap users get 30% off the EdgeProp eval with code BOOKMAP30. Analyze order flow while executing under evaluation conditions.")
    pdf.bullet("Connect: open Bookmap → select Rithmic as data and trading provider → enter EdgeProp credentials → execute futures from the Bookmap interface.")
    pdf.bullet("Help center 17 Feb 2026: “Bookmap license is included with your EdgeProp account. No additional subscription is required.”")
    pdf.bullet("One active license per account. Pick Bookmap or ATAS or Jigsaw or WealthCharts or tradesea. Not all at once. Eval and funded. Switch via support.")
    pdf.body(
        "EdgeProp pays Bookmap (or ATAS/Jigsaw) seats as a cost of goods on the eval. Bookmap sends heatmap users to EdgeProp checkout with a coupon. Neither company becomes the other."
    )
    pdf.h3("Vs Verodus")
    pdf.body(
        "This is the letter Joe did not write: “Bookmap users take 30% off Instant / 1-Step / Lite with code X; they trade on your stack.” "
        "Verodus cannot offer “execute from Bookmap via Rithmic” because you are not a Rithmic futures shop. You could, in theory, "
        "bulk-license Bookmap as a perk. That is EdgeProp’s cost line, not their origination engine — and their traders are CME futures scalpers, not Platform 5 Instant buyers."
    )

    pdf.h2("Side-by-side vs Verodus")
    add_table(
        pdf,
        ["", "10FOUR", "TickTickTrader", "Trade The Pool", "EdgeProp", "Verodus"],
        [
            ["Asset", "US futures", "US futures", "US stocks/ETFs", "US futures", "Forex/indices/crypto"],
            ["Instant", "Yes", "Historically (Direct)", "No (1-step stocks)", "One-step, not Instant", "Yes"],
            ["Bookmap", "Co-brand; trader buys", "Historical free seat", "30-day trial, then trader pays", "Included seat or ATAS/Jigsaw", "None"],
            ["Stack", "CQG, TradingView", "Rithmic; lost Tradovate then Project X", "TraderEvolution", "Rithmic", "Platform 5 + TradeHub"],
            ["Entity", "HK", "Isle of Man", "Israel (The5ers)", "Romania + Chicago", "Dubai L.L.C.-FZ"],
            ["Status", "New (~Jul 2026)", "Sales appear stopped", "Operating, real Trustpilot", "Young, thin Trustpilot", "Operating (~3,000 users)"],
        ],
        [22, 28, 32, 32, 30, 30],
    )

    pdf.h2("What this changes for Verodus / Joe")
    pdf.body("Nothing in the locked commercial posture. It names the four shops his Bookmap language actually maps onto.")
    pdf.bullet("Do not accept the inverted product. In every live pair, Bookmap is the heatmap and the prop firm is the eval shop.")
    pdf.bullet("If he ever writes the competent two-vendor stack, the templates are already public: EdgeProp-shaped coupon + optional included seat; 10FOUR-shaped co-brand with the trader buying Bookmap; TTP-shaped 30-day trial. Verodus’s slice in all three is still tagged evaluation fees.")
    pdf.bullet("Do not volunteer a Bookmap integration. Platform 5 / TradeHub is not Rithmic/CQG. US futures order-flow traders are not the Instant SKU. TickTickTrader shows the feed risk.")
    pdf.bullet("10FOUR is not a partner you inherit. It is a Hong Kong futures Instant competitor that Bookmap actually signed. No public page ties it to Joe.")
    pdf.bullet("Data stays closed. These prop pairings do not create a data-sharing right. Privacy bans on this pass still hold.")
    pdf.body(
        "If Joe actually has a Bookmap conversation, that is parallel shopping. It does not put Verodus in Bookmap’s partner program, and it does not put Bookmap inside Instant."
    )

    pdf.ln(2)
    pdf.set_font("Inter", "I", 8.0)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.4,
        "Sources 22 August 2026 (primary): bookmap.com/en/b2b/prop-firms; bookmap.com/en/partner/10four; "
        "bookmap.com/en/partner/edge-prop; Bookmap LinkedIn 11 Aug 2026; edgeproptrading.com; EdgeProp help "
        "Bookmap–Rithmic 17 Feb 2026; tradethepool.com/partners/, /program-terms/, /technical-skill/bookmap/. "
        "Secondary status: PropFirmMap 10FOUR (17 Aug 2026); JoinProp TTT (11 Aug / 15 Jul 2026); TradingFunder TTT "
        "24 May 2026. Companion: docs/bookmap-prop-firm-partners.md, docs/bookmap-research.md. "
        "No Bookmap–Joe/TradeMath/MoniMath hit found. Not an audit and not legal advice.",
    )

    for path in (OUT, REPO_OUT, ROOT_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        print(f"Wrote {path} pages={pdf.pages_count} bytes={path.stat().st_size}")


if __name__ == "__main__":
    build()
