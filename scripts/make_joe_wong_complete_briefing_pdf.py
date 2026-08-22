#!/usr/bin/env python3
"""Master PDF: Joe Wong / Bookmap / Kim’s meeting / Verodus terms. 22 August 2026."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/opt/cursor/artifacts/Joe_Wong_Briefing_Download.pdf")
REPO_OUT = Path("/workspace/docs/joe-wong-complete-briefing.pdf")
ROOT_OUT = Path("/workspace/joe-wong-complete-briefing.pdf")
EXTRA_OUT = Path("/workspace/Verodus_Joe_Wong_Full_Briefing.pdf")

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
        self.cell(0, 5, "Verodus  |  Joe Wong full briefing", align="L")
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

    def h3(self, text):
        needed = 8
        if self.get_y() + needed > 270:
            self.add_page()
        self.set_font("InterSB", "", 11)
        self.set_text_color(*INK)
        self.multi_cell(0, 6, text)
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
    pdf.rect(0, 8, 210, 68, "F")
    pdf.set_y(16)
    pdf.set_font("Inter", "", 9)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 5, "VERODUS INTERNAL BRIEFING  ·  UPDATED COMPLETE FILE", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_x(18)
    pdf.set_font("Inter", "B", 20)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 8.2, "Joe Wong — full briefing (meeting, email, Bookmap, terms)")
    pdf.set_x(18)
    pdf.set_font("Inter", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        6,
        "Karma Lounge meeting  ·  follow-up email  ·  public record  ·  22 August 2026\n"
        "For Alexander and Kim  ·  Does not change website copy",
    )

    pdf.set_y(88)
    pdf.callout(
        "Joe asked in the room for a cut of referred customers, for Verodus’s evaluation "
        "engine, and for the trading data. The follow-up email asked for an unpaid official "
        "partner logo and still describes Verodus as Bookmap. Believe the meeting. Paper "
        "net evaluation-fee origination. Do not share data. Do not give him the engine as "
        "his product."
    )
    pdf.warn(
        "Three separate asks. Referral %: yes, unique code, 15–25% of net Instant / 1-Step / "
        "Lite fees, rules unchanged, 90 days. Engine / PropTrade: later, white-label, Verodus "
        "keeps the stack. Data: no under current Privacy. Mixing them into one yes trains "
        "TAMS and helps him clone PropTrade off your tape."
    )
    pdf.body(
        "This file replaces the shorter 21–22 August notes as the single download. "
        "Inside: Kim’s four lines; what Joe seeks vs what each side gets; who he is; "
        "the four brand names; the claim table; the Bookmap leftover and the 10FOUR "
        "analogue; Bookmap data collection; the generic HK-credibility memo; Verodus "
        "terms and kill line; the reply Alexander can send; walk-away."
    )

    # --- 1 ---
    pdf.h2("1. What Joe is seeking, what he would get, what Verodus gets")
    add_table(
        pdf,
        ["", "If Verodus agrees to the email as written", "If Verodus agrees on Verodus terms"],
        [
            [
                "Joe gets",
                "Free long-term logo; prize accounts; your name next to OHKF / SFC / Saudi; a live shop to point PropTrade at; the list stays his",
                "A tracked referral cut; later a front-end brand on Verodus rails; no data; no exclusivity",
            ],
            [
                "Verodus gets",
                "Almost nothing in checkout. Reputational liability. He can still launch PropTrade elsewhere and say you partnered",
                "Tagged Asia challenge fees now; PropTrade GMV on your rails later if the pilot clears a floor",
            ],
            [
                "He asked in the room (Kim, 21 Aug 18:03)",
                "Not in the email",
                "% of directed customers; he has no competition engine; he wants the data",
            ],
            [
                "He asked on paper",
                "Unpaid official long-term partner of a 2026/27 HK-final competition via World Traders Hub HK",
                "Bookmap leftover: order-flow visualization, heading still Proposed Partnership with Bookmap",
            ],
        ],
        [32, 71, 71],
    )
    pdf.body(
        "He is not buying evaluations. He is not paying a sponsorship. He is shopping machinery "
        "for a competition and a PropTrade announcement he cannot run, plus a tape Bookmap "
        "does not even collect."
    )

    pdf.h2("1a. The email leftover — he did not stack Bookmap with Verodus")
    pdf.body(
        "Subject: Strategic Partnership Proposal: Expanding Verodus’s Global Footprint via "
        "World Traders Hub HK. Ask on paper: unpaid official long-term partner of a 2026/2027 "
        "global competition with a Hong Kong final. No cash, no SKU, no tracking code, no data "
        "license. The body is a Bookmap partnership template:"
    )
    add_table(
        pdf,
        ["His words", "What that is"],
        [
            [
                "Given Bookmap’s status as a premier institutional-grade order flow platform",
                "Bookmap is a heatmap / order-flow terminal. Verodus is not.",
            ],
            [
                "Proposed Partnership with Bookmap",
                "Section heading never swapped. You are still in the Bookmap slot.",
            ],
            [
                "Combining Verodus’s advanced order flow visualization and infrastructure",
                "Verodus name pasted onto Bookmap product copy.",
            ],
        ],
        [82, 92],
    )
    pdf.body(
        "If he wanted both vendors he would say Bookmap on the tape, Verodus for Instant / "
        "1-Step / Lite. He assigned Bookmap’s product to you. Same class of error as "
        "TradeMath’s old Linear.app leftovers. He is shopping a platform partner. Last draft "
        "that partner was Bookmap. This send, it was supposed to be you."
    )

    # --- 2 ---
    pdf.h2("2. Kim’s four lines (21 August 18:03–18:05)")
    pdf.h3("“He wants a percentage of the profits from directing customers to us”")
    pdf.body(
        "Yes. That is the only cash deal. The email never wrote a rate, SKU, or code. "
        "Force the word profits:"
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
                "Refuse. That taxes the reward pool.",
            ],
            [
                "% of company profit",
                "Refuse. Not an equity or P&L partner.",
            ],
        ],
        [88, 86],
    )

    pdf.h3("“He has no trading competition. He needs our engine”")
    pdf.body(
        "Yes. TradeMath championship is a Rolex essay + form plus City & Provincial China "
        "language. World Traders Hub HK is email-only — no site, no CR number produced, no "
        "OHKF letter. MoniMath PropTrade announced 18 Nov 2025 for January 2026 with no public "
        "Instant / 1-Step / KYC / MT5 / TradeHub / payout stack. Verodus has the SKUs, rules, "
        "Platform 5, TradeHub, Veriff, fees, resets, Rise/crypto, ~3,000 users. Promote a "
        "competition is a landing page. Competition engine is the evaluation CRM. If you agree, "
        "the engine stays yours. His brand can sit on the front later. He does not get a fork."
    )

    pdf.h3("“He wants our data too / we share the data”")
    pdf.body(
        "He wants it. You do not share it. TAMS is sold as trader behavioral analytics — the "
        "LISG/MyAIQuit vocabulary. Labeled tickets, pass/fail, daily-loss, Best Day, payout vs "
        "blow-up: Bookmap’s FAQ says they do not ingest the user’s trading activity. A shop "
        "like Verodus is the only place he can get that tape. Live Privacy: trading-behavior "
        "data is not commercialized externally; P&L, strategies, and behavior are not shared "
        "externally; personal information is not sold. Counsel would have to amend Privacy, "
        "put a DPA in place, and you would sell an anonymized license for cash — not throw it "
        "in to make a championship look real."
    )

    pdf.h3("“He wants to promote competition but he doesn’t have the engine”")
    pdf.body("Correct. That is the file in one sentence.")

    pdf.callout(
        "One paragraph for Kim: Joe asked in person for a cut of referred customers and for "
        "the stack behind a competition he cannot run. That is real. The email then asked for "
        "a free logo and still thinks we are Bookmap. We take the referral if it is a unique "
        "code and a share of net challenge fees, rules unchanged. We do not share trading data. "
        "We do not give him the engine as his product. If he wants PropTrade, it runs on our "
        "rails and we keep most of the GMV after a 90-day checkout floor."
    )

    # --- 3 ---
    pdf.h2("3. Who Joe is")
    pdf.body(
        "Joe M.Y. Wong. LinkedIn joe-wong-55b3ab262, Hong Kong. Email sign-off: Founder / CTO / "
        "TradeMath / MoniMath / World Traders Hub HK. LIS Group About: Founder | Chairman — "
        "not CTO. LISG’s actual CTO is Jacky Qi Zhang. Not comedian Huang Xi. Not Fed Guy "
        "Joseph Wang."
    )
    add_table(
        pdf,
        ["Period", "Claim", "What is public"],
        [
            [
                "1995–2017",
                "Emperor Group / commodities; BRF, JBS, Vitol, Glencore",
                "Unverified. No filing or press tying this Joe Wong to those desks.",
            ],
            [
                "2017–2022",
                "COO, Xerbal Group (hemp)",
                "Xerbal exists. Patent US11602701B2 inventor is Peter Matravers, not Joe. LIS/MyAIQuit brands later sit under Xerbal Asia Limited.",
            ],
            [
                "MIT Sloan",
                "AI Technology for Business Strategy",
                "Short executive-education certificate (~6 weeks), not an MIT degree.",
            ],
            [
                "2022–now",
                "Founder / Chairman, LIS Group (lisg.ai)",
                "Live. MyAIQuit still in beta language in 2026. COO Vincent Cho. CTO Jacky Qi Zhang. CFO Vincent Lai.",
            ],
            [
                "2025–2026",
                "TradeMath + MoniMath",
                "WordPress marketing. Thin LinkedIn (MoniMath posts often ~3–5 reactions).",
            ],
            [
                "21 Aug 2026",
                "World Traders Hub HK",
                "Named in the Verodus email only. No matching site or OHKF page found.",
            ],
        ],
        [28, 58, 88],
    )
    pdf.body(
        "Pattern: serial partnership operator. Stacks brands, transplants LISG behavioral "
        "analytics into TAMS, hunts partners. TradeMath historically carried leftover Linear.app "
        "copy. This email carries leftover Bookmap copy. Same operator, not a one-off paste error."
    )

    # --- 4 ---
    pdf.h2("4. Everything he is in right now")
    add_table(
        pdf,
        ["Name", "What it is", "Joe’s role", "Overlap with Verodus"],
        [
            [
                "LIS Group / MyAIQuit",
                "AI smoking cessation; real org chart",
                "Founder / Chairman (site). Not CTO.",
                "None as a product. Character sample only.",
            ],
            [
                "TradeMath",
                "Retail education + championships (WordPress). About still claims 35+ years, 50+ networks, 10M+ backtests, 10k asset classes, 10k members, a Jane Street framework — metrics duplicated and mislabeled",
                "Founder in marketing; email says CTO",
                "Possible top-of-funnel. Must not gate Instant.",
            ],
            [
                "MoniMath",
                "Institutional/HNWI; TAMS; live H1 still says Bluetooth mode; Type 2 mislabeled as advising (that is Type 4); unnamed SFC partners vs LinkedIn approval 20 Nov 2025 (~3 reactions); PropTrade announced 18 Nov 2025",
                "Co-founder",
                "The overlap. Needs rails Verodus already has.",
            ],
            [
                "World Traders Hub HK",
                "2026/27 competition; OHKF / Saudi name-drops",
                "Named on the email only",
                "Logo ask. No public infrastructure.",
            ],
        ],
        [36, 54, 40, 44],
    )

    # --- 5 ---
    pdf.h2("5. Claim table")
    add_table(
        pdf,
        ["Claim", "Source", "Verdict"],
        [
            [
                "25% algo / 40% US equities for 6 years on two licensed HK funds",
                "Email",
                "Unverified. No fund names, no audited returns, no SFC CE.",
            ],
            [
                "BofA / Crédit Lyonnais / RBC / KPMG executive members",
                "Email",
                "Unnamed. Crédit Lyonnais as a going concern is historical.",
            ],
            [
                "10,000+ algo traders",
                "Email / TradeMath",
                "Implausible vs ~3–5 LinkedIn reactions and a WordPress funnel.",
            ],
            [
                "1,700-person 2025 event with the Saudi government",
                "Email",
                "No public TradeMath/Joe/WTHHK match. Nearest shape: Algo Challenge Association at Money20/20 Riyadh; they are not on the sponsor list; prizes ~USD 2k.",
            ],
            [
                "Our Hong Kong Foundation backing",
                "Email",
                "OHKF is real (Tung Chee-hwa think tank). Link to Joe is not public. Do not sit Verodus next to it without a letter.",
            ],
            [
                "SFC Types 1/2/9 partners / MoniMath Capital approval",
                "Site + LinkedIn 20 Nov 2025",
                "Unnamed. Type 2 mislabeled. LinkedIn said approval; site says partners. No CE number.",
            ],
            [
                "Canada-listed partner",
                "MoniMath site",
                "Unnamed. Ignore until named.",
            ],
            [
                "Joe as CTO of TradeMath / MoniMath / WTHHK",
                "Email sign-off",
                "Contradicts LISG (Chairman) and LISG’s actual CTO (Jacky Zhang).",
            ],
            [
                "Dissolved similar-name HK company",
                "Generic memo",
                "Could not confirm one tied to Joe. Name collisions exist (PPE World Trading Hub, UAE Traders Hub). Ask for CR number.",
            ],
        ],
        [58, 36, 80],
    )

    # --- 6 ---
    pdf.h2("6. Bookmap — why the email still says it")
    pdf.body(
        "Bookmap is a paid order-flow heatmap, not a prop firm. Founder Tsachi Galanos. "
        "Bookmap Ltd, Cyprus. Majority-owned by Brazilian fintech Nelogica since 1 November 2024. "
        "~300,000 users claimed at the deal. ~50–60 staff. Software subscription (data extra): "
        "free Digital up to ~$99/mo Global+. Name = order book + heat map. Sits on Rithmic / "
        "CQG / dxFeed. Not MT5, not Instant, not a payout firm."
    )
    pdf.body(
        "They publish a partner network and a page aimed at prop firms (bulk seats, heatmap "
        "inside evaluations, record/replay, retention). That is the genre of Joe’s letter. "
        "Bookmap writes it to prop firms. Joe sent it as if Verodus were Bookmap. Correct split: "
        "Bookmap sells seats; the prop firm sells challenge fees. Joe inverted it."
    )
    pdf.h3("Bookmap × 10FOUR (11 August 2026)")
    pdf.body(
        "Ten days before Joe emailed you, Bookmap announced traders can use Bookmap while "
        "trading a 10FOUR evaluation or funded account. Roles stay separate. 10FOUR (Ten Four "
        "Group, HK CR 79713385, Kwun Tong) is a futures sim-prop: Instant, Origin, Daily; "
        "$25k–$150k; 90% split; CQG; Riseworks. Same category as Verodus, different stack. "
        "Joe is in Hong Kong. No public page ties Bookmap to Joe, TradeMath, MoniMath, or "
        "World Traders Hub. He had the language. He did not have the deal. The competent "
        "two-vendor letter would have been Bookmap on the tape, Verodus for Instant / 1-Step / "
        "Lite. He left Proposed Partnership with Bookmap in a letter to you."
    )
    pdf.h3("Does Bookmap collect trader data?")
    pdf.body(
        "Ticks / P&L / strategy: Bookmap’s FAQ says no. The app runs on the PC. They say they "
        "have no access to personal account information or trading activity. License activation "
        "sends OS version and screen resolution. API: orders and live market data do not go "
        "through Bookmap servers except Bookmap Data (their own feed). The heatmap is exchange "
        "order flow, not a dossier on that user."
    )
    pdf.body(
        "Account and website: yes. Privacy Policy (Bookmap Limited, Nicosia): name, email, "
        "phone, VAT, profession, country, payment; cookies; unique device ID; Google Analytics; "
        "Hotjar session recording; Facebook/Twitter ads; Zoho CRM. A SaaS CRM, not a "
        "Verodus-style ticket tape. That is why Joe wants your data, not Bookmap’s."
    )

    # --- 7 ---
    pdf.h2("7. The generic “lead-gen + HK credibility” memo")
    pdf.body(
        "Keep three sentences: Bookmap is a tell; official long-term partner is not a deal; "
        "start with a measured pilot. Kill the value thesis. Verodus is already Dubai FZ "
        "(Verodus L.L.C.-FZ; payments via Verodus Capital Inc.), ~3,000 users, 175+ countries. "
        "Joe cannot add a geography. 10k traders and a 1,700-person Saudi event are marketing, "
        "not TAM. OHKF/SFC next to Verodus is the liability. Required education kills Instant. "
        "A clarifying call without a Verodus-specific one-pager spends another meeting on a "
        "template. Paper first."
    )

    # --- 8 ---
    pdf.h2("8. What Verodus takes (on Verodus terms)")
    pdf.body(
        "Verodus is a live simulated-evaluation shop: Instant, 1-Step, 2-Step Lite/Pro; "
        "Platform 5 (MT5, not for US) + TradeHub; KYC; Rise/crypto. Not a licensed broker. "
        "Not live client funds. $49 in marketing is Instant at 35% off. $5k–$200k is 2-Step "
        "sizes. $1M is combined account cap."
    )
    add_table(
        pdf,
        ["Item", "Position"],
        [
            ["Product", "Instant, 1-Step, Lite only for the pilot. Not a custom championship account."],
            ["Rules", "Unchanged. Daily loss, trailing, Best Day, refund policy, KYC stay Verodus’s."],
            ["Tracking", "Unique code / link. No code, no commission."],
            ["Economics", "15–25% of net evaluation fees after refunds, chargebacks, Instant-fee non-refund."],
            ["Prizes", "Capped evaluation accounts (e.g. Instant at a defined size). Not live capital. Not uncapped 2-Step Pro."],
            ["Term", "90 days. Either party walks. No exclusivity."],
            ["Brand", "Originated by TradeMath / MoniMath. Evaluated by Verodus. No SFC, OHKF, Saudi, or Jane Street in the same sentence as Verodus."],
            ["Later", "PropTrade white-label on Verodus rails. Verodus keeps ~70–85% of GMV. He does not get raw tickets."],
            ["Academy", "Optional paid add-on at checkout. Never a gate to Instant."],
        ],
        [32, 142],
    )

    pdf.h3("Kill line (Instant at $49, 20% of net)")
    add_table(
        pdf,
        ["Unique checkouts in 90 days", "Gross fees", "Verodus keeps (~80%)", "His 20%"],
        [
            ["20", "$980", "$784", "$196"],
            ["100", "$4,900", "$3,920", "$980"],
            ["500", "$24,500", "$19,600", "$4,900"],
        ],
        [50, 42, 42, 40],
    )
    pdf.body(
        "Twenty is a meeting that produced a list. Five hundred is a channel. Zero unique "
        "codes is a template. Kill at 20 unless mix includes 1-Step / Lite at similar net. "
        "Do not model 10,000 algo traders."
    )

    pdf.h2("9. Refuse")
    pdf.bullet("Unpaid official long-term partner / exclusive logo")
    pdf.bullet("Bookmap / order-flow story assigned to Verodus")
    pdf.bullet("Required TradeMath education")
    pdf.bullet("CRM / tickets / behavioral data (Privacy bans). Free data to train TAMS")
    pdf.bullet("SFC / OHKF / Saudi / two HK funds / Jane Street as co-brand")
    pdf.bullet("Custom championship rules that loosen daily / trail / Best Day")
    pdf.bullet("% of trader payouts or company P&L")
    pdf.bullet("A clarifying call before a Verodus-specific one-pager")

    pdf.h2("10. What to send back")
    pdf.bullet("Correct the product: simulated Instant / 1-Step / Lite; no deposits; no client funds; no brokerage; no order-flow tool. If he wants Bookmap, that is another company.")
    pdf.bullet("Verodus-specific one-pager: named SKU, unique code, 90-day term, 15–25% of net fees. No Bookmap/Linear leftovers.")
    pdf.bullet("Paper on halo if he wants those names in joint copy: SFC CE numbers; OHKF contact; Saudi organizer. Otherwise those names never appear next to Verodus.")
    pdf.bullet("No unpaid exclusivity. No data license. No required education.")
    pdf.bullet("PropTrade is a second document after the pilot clears a checkout floor.")
    pdf.body(
        "If the next note still cannot name Instant vs 1-Step vs Lite, there is no deal. "
        "Do not follow up twice."
    )

    pdf.h2("11. Reply Alexander can send")
    pdf.body(
        "Tone: you met him; you are not hostile; you will not sign a blank partnership. "
        "Do not attach a term sheet on the first reply. Make him describe Verodus correctly first."
    )
    pdf.callout(
        "Hi Joe, Good to hear from you after Karma Lounge. Quick clarification so we don’t "
        "waste a cycle: Verodus is a simulated evaluation firm (Instant and challenge programs, "
        "published rules, cash performance rewards). We are not an order-flow visualization "
        "platform, and we don’t run client brokerage books. If the collaboration you have in "
        "mind is challenges / Asia origination / a 2027 competition funnel onto those products, "
        "we can talk. If it was scoped for a terminal like Bookmap, that’s a different company. "
        "For a first discussion I need a short Verodus-specific note covering: (1) which Verodus "
        "products you want (Instant, 1-Step, 2-Step Lite/Pro) and whether prize accounts are "
        "paid or comped; (2) how you would send buyers (tracked links / codes) — we only share "
        "net evaluation fees on tagged checkouts, after refunds and chargebacks, on unchanged "
        "public rules; (3) contracting entity, and the SFC CE number for any licensed fund you "
        "want associated with this — if there isn’t one, we can’t be named next to SFC approval; "
        "(4) a contact at Our Hong Kong Foundation if you want that name in any joint material, "
        "and the same for the Saudi 2025 event (organizer, participant-count source, TradeMath’s "
        "role). We don’t do unpaid exclusive official long-term partner appointments, and we "
        "don’t license trader data under the current Privacy Policy. Happy to do 30 minutes "
        "once that note is in. Alexander"
    )

    pdf.h2("Walk-away")
    pdf.bullet("Free partnership with no unique code and no net-fee share")
    pdf.bullet("Unnamed SFC partner in joint copy")
    pdf.bullet("Exclusivity without a six-figure minimum over a defined term")
    pdf.bullet("Raw tickets, CRM, or behavioral feeds")
    pdf.bullet("Education as a gate to Instant")
    pdf.bullet("Championship rules that loosen daily / trailing / Best Day")
    pdf.bullet("Repeat of Bookmap / Saudi / OHKF language after you asked for paper")

    pdf.h2("Bottom line")
    pdf.callout(
        "Joe chairs a real smoking-cessation company, markets TradeMath and MoniMath, and "
        "named World Traders Hub HK on a Bookmap template. In the room he asked for a "
        "referral cut, your engine, and your data. On paper he asked for a free logo. "
        "Verodus’s benefit is tagged Instant / 1-Step / Lite fees on unchanged rules, then "
        "maybe PropTrade on Verodus rails. Everything else is either unverified or actively "
        "harmful to repeat. Three asks, not one yes."
    )

    pdf.ln(2)
    pdf.set_font("Inter", "I", 8.2)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.6,
        "Sources 21–22 August 2026: trademath.ai and /about /monimath; lisg.ai/about-us; "
        "Joe LinkedIn (PropTrade 18 Nov 2025; SFC approval 20 Nov 2025); Karma Lounge email "
        "as pasted; Kim Chen chat 21 Aug 18:03–18:05; bookmap.com, /en/b2b/prop-firms, "
        "/privacy-policy, FAQ; Nelogica 1 Nov 2024 PR; Bookmap LinkedIn 10FOUR 11 Aug 2026; "
        "OHKF public site; Money20/20 / Algo Challenge Association listings. Companion notes "
        "in docs/. Not an audit and not legal advice. Does not change website copy.",
    )

    for path in (OUT, REPO_OUT, ROOT_OUT, EXTRA_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        print(f"Wrote {path} pages={pdf.pages_count} bytes={path.stat().st_size}")


if __name__ == "__main__":
    build()
