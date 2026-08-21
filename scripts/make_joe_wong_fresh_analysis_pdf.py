#!/usr/bin/env python3
"""PDF: fresh map of Joe Wong, the Karma Lounge email, and Verodus benefit."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/opt/cursor/artifacts/Joe_Wong_Fresh_Analysis.pdf")
REPO_OUT = Path("/workspace/docs/joe-wong-fresh-analysis.pdf")
ROOT_OUT = Path("/workspace/joe-wong-fresh-analysis.pdf")

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
        self.cell(0, 5, "Joe Wong  |  Fresh map for Verodus", align="L")
        self.set_xy(18, 10)
        self.cell(0, 5, "Internal  ·  21 August 2026", align="R")
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
    pdf.rect(0, 8, 210, 62, "F")
    pdf.set_y(16)
    pdf.set_font("Inter", "", 9)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 5, "VERODUS INTERNAL BRIEFING", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_x(18)
    pdf.set_font("Inter", "B", 21)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 8.5, "Joe Wong — everything he is in, the email, and what Verodus can take")
    pdf.set_x(18)
    pdf.set_font("Inter", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        6,
        "Fresh map after Karma Lounge  ·  21 August 2026  ·  For Alexander",
    )

    pdf.set_y(82)
    pdf.callout(
        "Joe chairs a real smoking-cessation company (LIS Group / MyAIQuit), markets a "
        "trading-education brand (TradeMath), markets an institutional/HNWI brand (MoniMath), "
        "and the email adds a fourth name — World Traders Hub HK — that has no independent "
        "public footprint. The follow-up is a Bookmap partnership template with Verodus pasted "
        "in. It asks for an unpaid official long-term partner slot. It does not name Instant, "
        "1-Step, Lite, Platform 5, TradeHub, fee, or payout mechanics."
    )
    pdf.warn(
        "Verodus’s only real take: tracked Asia origination on unchanged Instant / 1-Step / "
        "Lite rules, paid as a share of net evaluation fees, then maybe PropTrade on Verodus "
        "rails. Do not take the unpaid logo, the SFC/OHKF/Saudi halo, required education, or "
        "any data dump. Privacy still bans external commercialization of trading behavior."
    )

    pdf.h2("1. Who he is")
    pdf.body(
        "Public name on the email: Joe M.Y. Wong. LinkedIn joe-wong-55b3ab262, Hong Kong. "
        "Email sign-off: Founder / CTO / TradeMath / MoniMath / World Traders Hub HK. "
        "LIS Group About page: Founder | Chairman of Board of Director — not CTO. "
        "LISG’s actual CTO is Jacky Qi Zhang. Not comedian Huang Xi. Not Fed Guy Joseph Wang."
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
                "COO, Xerbal Group (hemp extraction)",
                "Xerbal exists. Patent US11602701B2 is Xerbal USA; inventor is Peter Matravers, not Joe. LIS/MyAIQuit brands later sit under Xerbal Asia Limited.",
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
                "WordPress marketing. Thin LinkedIn (MoniMath posts often ~3 reactions).",
            ],
            [
                "21 Aug 2026",
                "World Traders Hub HK",
                "Named in the Verodus email only. No matching site, registry hit, or OHKF page found.",
            ],
        ],
        [28, 58, 88],
    )
    pdf.body(
        "Operating pattern: serial partnership operator. He stacks brands, borrows language "
        "from the last vertical (LISG behavioral analytics → MoniMath TAMS), and hunts "
        "distribution partners. TradeMath historically carried leftover Linear.app copy. "
        "This email carries leftover Bookmap copy. Same operator, not a one-off paste error."
    )

    pdf.h2("2. Everything he is involved in")
    pdf.body(
        "Four names. Only one has a real org chart. Only one overlaps Verodus. The email "
        "asks Verodus to underwrite the other two with a logo."
    )

    pdf.set_font("InterSB", "", 11)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 6, "LIS Group / MyAIQuit — the operating company")
    pdf.ln(0.6)
    pdf.body(
        "lisg.ai. Site says founded 2016; Joe’s LinkedIn puts the chair role from 2022. "
        "Product is MyAIQuit, an AI smoking-cessation app, still in beta language in 2026. "
        "About page lists Joe as Founder/Chairman, Dr Alan Kwok as CEO, Vincent Cho as COO, "
        "Jacky Qi Zhang as CTO, Vincent Lai as CFO, plus respiratory and lifestyle advisors. "
        "Joe’s listed achievements mix “revolutionary extraction technology” (the Xerbal hemp "
        "story) with the smoking product. Relevance to Verodus as a product: none. Relevance "
        "as character: he already has a health-tech company, a COO, a CTO, and a CFO. "
        "TradeMath/MoniMath are a parallel brand stack, not his only job, and he is not the "
        "CTO there either despite the email sign-off."
    )

    pdf.set_font("InterSB", "", 11)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 6, "TradeMath (trademath.ai) — retail education and championships")
    pdf.ln(0.6)
    pdf.body(
        "Live WordPress.com marketing. Education + coaching + championships. About page still "
        "claims 35+ years, 50+ institutional networks, 10M+ backtests, 10,000+ asset classes, "
        "10,000+ members, and a “Jane Street” framework — with the metric row duplicated and "
        "in places mislabeled. Championship is a Rolex essay + form, plus “City & Provincial” "
        "China tournament language. No named faculty, no audited member count, no evidence of "
        "10,000 asset classes. This can theoretically send students to an evaluation shop. "
        "It cannot replace Instant / 1-Step / Lite. If education is made mandatory, Verodus’s "
        "conversion dies and Joe captures the course fee."
    )

    pdf.set_font("InterSB", "", 11)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 6, "MoniMath — institutional / HNWI / “funded” language")
    pdf.ln(0.6)
    pdf.body(
        "trademath.ai/monimath/. Headline on 21 August 2026 still includes a CMS glitch: "
        "“Bluetooth mode.” Also: “Join the next generation of funded traders.” TAMS is sold "
        "as deep learning plus behavioral analytics — the LISG vocabulary. Claims 5+ years "
        "verified trading, SFC Types 1 / 2 / 9 via partners, and a Canada-listed partner, "
        "none named. Type 2 is mislabeled as “Advising on Securities” (that is Type 4; Type 2 "
        "is futures). LinkedIn 20 Nov 2025 said “SFC approval” for an algo fund (~3 reactions). "
        "LinkedIn 18 Nov 2025 announced MoniMath PropTrade, kickoff January 2026. No SFC CE "
        "number, no named licensed corporation, no fund docs, no public live PropTrade stack. "
        "This is the only brand that overlaps Verodus. PropTrade is a competing or needing "
        "prop-evaluation stack. He is shopping a partner because he does not have Instant / "
        "1-Step / Lite / MT5 / TradeHub / KYC / payout rails."
    )

    pdf.set_font("InterSB", "", 11)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 6, "World Traders Hub HK — email-only vehicle")
    pdf.ln(0.6)
    pdf.body(
        "Named in the 21 August email as the competition vehicle. Claimed backers: Our Hong "
        "Kong Foundation (ourhkfoundation.org.hk — Tung Chee-hwa think tank, a real "
        "institution) and a 1,700-person 2025 event “with the Saudi government.” No World "
        "Traders Hub HK website. No OHKF page, press release, or programme listing Joe / "
        "TradeMath / MoniMath / World Traders Hub. Closest public 2025 Riyadh trading-"
        "competition shape: Algo Challenge Association at Money20/20 Middle East — TradeMath "
        "/ Joe not on the sponsor list; prizes on the order of USD 2k; few named teams. "
        "Search collisions: unrelated Traders Hub (UAE) and World Trading Hub (PPE). Until "
        "OHKF and the Saudi organizer are named in writing, treat World Traders Hub HK as "
        "a letterhead."
    )

    pdf.h2("3. How the four names fit")
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
                "Retail education + championships (WordPress)",
                "Founder in marketing; email says CTO",
                "Possible top-of-funnel. Must not gate Instant.",
            ],
            [
                "MoniMath",
                "Institutional/HNWI; TAMS; PropTrade announced",
                "Founder; SFC-partner claims unverified",
                "The overlap. Needs rails Verodus already has.",
            ],
            [
                "World Traders Hub HK",
                "2026/27 competition; OHKF / Saudi name-drops",
                "Named on the email only",
                "Logo ask. No public infrastructure.",
            ],
        ],
        [40, 50, 42, 42],
    )
    pdf.body(
        "He is not bringing Verodus a fund. He is bringing a distribution story and asking "
        "Verodus to underwrite it with a logo."
    )

    pdf.h2("4. The email — what he actually asked for")
    pdf.body(
        "From Joe M.Y. Wong after Karma Lounge. Subject: Strategic Partnership Proposal: "
        "Expanding Verodus’s Global Footprint via World Traders Hub HK. Ask in one line: "
        "be the unpaid official long-term partner of a 2026/2027 global trading competition "
        "with a Hong Kong final."
    )
    pdf.bullet("He offers: logo, “official partner” status, access to a claimed network, a path into Asia / Middle East, long-term not a one-off cheque.")
    pdf.bullet("He does not offer: cash, Instant / 1-Step / Lite, a unique tracking code, a data license, PropTrade on Verodus rails, SFC CE numbers, OHKF contacts, or a Saudi organizer.")
    pdf.bullet("He does not prove he opened Verodus.com after the meeting.")
    pdf.warn(
        "Fatal tell: the body is a Bookmap template. Verodus is described as if it were an "
        "order-flow visualization vendor, and a heading remains in the shape of Proposed "
        "Partnership with Bookmap. Same class of error as TradeMath’s old Linear.app leftovers. "
        "Karma Lounge was a meeting. This follow-up was not custom work."
    )

    pdf.h2("5. Claim table")
    add_table(
        pdf,
        ["Claim", "Source", "Verdict", "Why it matters"],
        [
            [
                "25% algo / 40% US equities for 6 years on two licensed HK funds",
                "Email",
                "Unverified. No fund names, no audited returns, no SFC CE.",
                "Do not let this become Verodus’s implied track record.",
            ],
            [
                "BofA / Crédit Lyonnais / RBC / KPMG “executive members”",
                "Email",
                "Unnamed. Crédit Lyonnais as a going concern is historical.",
                "Ask for names or drop it.",
            ],
            [
                "10,000+ algo traders",
                "Email / TradeMath members",
                "Implausible vs ~3 LinkedIn reactions and a WordPress funnel.",
                "Size the pilot off unique codes, not this number.",
            ],
            [
                "1,700-person 2025 event with the Saudi government",
                "Email",
                "No public TradeMath/Joe/WTHHK match. Money20/20 ACA is the nearest shape and does not list them.",
                "Highest reputational risk if Verodus repeats it.",
            ],
            [
                "Our Hong Kong Foundation backing",
                "Email",
                "OHKF is real. Link to Joe is not public.",
                "Do not sit Verodus next to Tung Chee-hwa’s think tank without a letter.",
            ],
            [
                "SFC Types 1/2/9 partners",
                "MoniMath site",
                "Unnamed. Type 2 mislabeled. LinkedIn said approval; site says partners.",
                "Verodus must not imply SFC cover.",
            ],
            [
                "Canada-listed partner",
                "MoniMath site",
                "Unnamed.",
                "Ignore until named.",
            ],
            [
                "TAMS (DL + behavioral)",
                "Both sites",
                "Marketing language transplanted from LISG smoking-cessation copy.",
                "Not a Verodus dependency. Do not integrate.",
            ],
            [
                "MIT Sloan AI",
                "LISG About",
                "Certificate, not a degree.",
                "Fine as exec-ed. Not a credential for running a fund.",
            ],
            [
                "MoniMath PropTrade Jan 2026",
                "LinkedIn 18 Nov 2025",
                "Announced. No public live stack.",
                "This is the product he needs Verodus for.",
            ],
            [
                "Joe as CTO of TradeMath / MoniMath / WTHHK",
                "Email sign-off",
                "Contradicts LISG (Chairman) and LISG’s actual CTO (Jacky Zhang).",
                "He inflates his technical role when selling.",
            ],
            [
                "“Bluetooth mode” in MoniMath H1",
                "Live site 21 Aug 2026",
                "CMS leftover.",
                "Quality signal. Matches Bookmap / Linear leftovers.",
            ],
        ],
        [44, 28, 52, 50],
    )

    pdf.h2("6. What benefit Verodus can get")
    pdf.body(
        "Verodus is a live simulated-evaluation shop: Instant, 1-Step, 2-Step Lite/Pro; "
        "Platform 5 (MT5, not for US) + TradeHub; KYC; Rise/crypto; ~3,000 users; 175+ "
        "countries. Entity: Verodus L.L.C.-FZ. Payments affiliate: Verodus Capital Inc. "
        "Not a licensed broker. Not live client funds."
    )
    pdf.body(
        "Joe cannot add a license, a fund, or a payout reputation Verodus does not already "
        "have. He can add people in Asia who buy evaluations, if and only if those people "
        "hit Verodus checkout with a code."
    )

    pdf.set_font("InterSB", "", 11)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 6, "Take — origination on unchanged rules")
    pdf.ln(0.6)
    add_table(
        pdf,
        ["Item", "Verodus position"],
        [
            ["Product", "Instant, 1-Step, Lite only for the pilot. Not a custom championship account."],
            ["Rules", "Unchanged. Daily loss, trailing, Best Day, refund policy, KYC stay Verodus’s. Protects fail-fee P&L."],
            ["Tracking", "Unique code / link per campaign. No code, no commission."],
            ["Economics", "15–25% of net evaluation fees after refunds, chargebacks, and Instant-fee non-refund. Not of GMV, not of prize pool."],
            ["Prizes", "If he needs prize accounts, issue capped evaluation accounts (e.g. Instant at a defined size), not live capital and not uncapped 2-Step Pro."],
            ["Term", "90 days. Either party walks. No exclusivity."],
            ["Brand", "Originated by TradeMath / MoniMath. Evaluated by Verodus. He does not say SFC, OHKF, Saudi, or Jane Street in the same sentence as Verodus."],
        ],
        [36, 138],
    )
    pdf.body(
        "This is the only cash path. Education shops that actually have a list convert some "
        "of it to challenge fees. Joe has not proven he has a list. The unique code is the proof."
    )

    pdf.set_font("InterSB", "", 11)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 6, "Take later — PropTrade on Verodus rails")
    pdf.ln(0.6)
    pdf.body(
        "MoniMath announced PropTrade for January 2026 and does not appear to have Instant / "
        "1-Step / KYC / MT5 / TradeHub. If the 90-day pilot produces real checkout, offer "
        "white-label: his brand on the front; Verodus rules, platforms, KYC, payouts on the "
        "back; Verodus keeps most of GMV (example 70–85% to Verodus, 15–30% origination to "
        "him). He does not get raw tickets, a CRM dump, or behavioral telemetry. That turns "
        "a competitor announcement into Verodus volume. It is the strategic prize. It is not "
        "owed on an unpaid logo email."
    )

    pdf.set_font("InterSB", "", 11)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 6, "Optional, never required — academy add-on")
    pdf.ln(0.6)
    pdf.body(
        "TradeMath courses can sit next to checkout as an upsell. They must not be a gate. "
        "If education is required to start Instant, conversion falls and he captures the "
        "course revenue while Verodus takes the support load."
    )

    pdf.h2("7. Do not take")
    add_table(
        pdf,
        ["Offer", "Why refuse"],
        [
            ["Unpaid official long-term partner", "Logo without economics. Exclusive smell. You underwrite his next template email."],
            ["Bookmap / order-flow visualization story", "Not the product. Signals he did not look."],
            ["Required TradeMath education", "Kills Instant impulse purchase."],
            ["CRM / ticket / behavioral data", "Live Privacy: trading-behavior data is not commercialized externally and not shared externally. Counsel would have to amend + DPA before any license."],
            ["SFC / OHKF / Saudi / two HK funds as co-brand", "Unverified. If a reporter asks, Verodus owns the sentence."],
            ["Custom championship rules", "He will ask for looser daily loss for the final. That is how fail-fee P&L disappears."],
            ["Exclusivity", "He will shop the same Bookmap email to the next prop shop. Keep the right to other Asia partners."],
            ["Free data to train TAMS", "Same as a CRM dump. No."],
        ],
        [62, 112],
    )

    pdf.h2("8. Economics so the pilot has a kill line")
    pdf.body(
        "Assume a tracked Instant at the discounted $49 headline (35% off list). Commission "
        "20% of net fee. Instant fees are not refunded on Verodus’s current rules, so net ≈ "
        "gross minus chargebacks."
    )
    add_table(
        pdf,
        ["Unique checkouts in 90 days", "Gross fees (at $49)", "Verodus keeps (~80%)", "His 20%"],
        [
            ["20", "$980", "$784", "$196"],
            ["100", "$4,900", "$3,920", "$980"],
            ["500", "$24,500", "$19,600", "$4,900"],
        ],
        [50, 42, 42, 40],
    )
    pdf.body(
        "Twenty checkouts is a meeting that produced a list. Five hundred is a real channel. "
        "Zero unique codes after 90 days is a template. Kill the partnership at 20 unless mix "
        "includes 1-Step / Lite at similar net. Do not model 10,000 algo traders. Model unique "
        "codes. If he insists the value is brand in HK, price that as a cash sponsorship with "
        "a written OHKF/Saudi confirmation, not as equity in Verodus’s logo."
    )

    pdf.h2("9. Risk if you say yes to the email as written")
    pdf.bullet("False halo. Official partner of a Saudi-government / OHKF competition will be read as Verodus’s claim. None of it is evidenced.")
    pdf.bullet("SFC adjacency. MoniMath already confuses Type 2 with Type 4 and approval with partners. A joint page would import that mess.")
    pdf.bullet("Product mismatch. Instant is simulated evaluation. His page says funded traders. His email says order-flow platform. Customers will not parse the difference if he writes the copy.")
    pdf.bullet("Template risk. Next partner gets the same email with Verodus’s name left in, the way Bookmap’s name was left in.")
    pdf.bullet("PropTrade fork. If you give him a logo and no contract, he can still launch PropTrade elsewhere and tell the market Verodus partnered. Lock language: originator, not owner; no SFC; no OHKF; no Saudi.")

    pdf.h2("10. What to send back")
    pdf.body(
        "The reply already drafted in docs/joe-wong-email-analysis.md still holds. Substance only:"
    )
    pdf.bullet("Correct the product in one paragraph: simulated evaluations, Instant / 1-Step / Lite, no deposits, no client funds, no brokerage, no order-flow tool.")
    pdf.bullet("Ask for a Verodus-specific one-pager. No Bookmap/Linear leftovers. Named SKU, unique code, 90-day term, commission on net fees.")
    pdf.bullet("Ask for paper on the halo: SFC CE numbers; OHKF contact who will confirm World Traders Hub HK; Saudi organizer who will confirm the 2025 event and 2026/27 role.")
    pdf.bullet("No unpaid exclusivity. No data license. No required education.")
    pdf.bullet("If he wants PropTrade, that is a second document after the pilot clears a checkout floor.")
    pdf.body("If he cannot produce the one-pager and ignores the paper requests, there is no deal. Polite walk-away.")

    pdf.h2("11. Walk-away lines")
    pdf.bullet("Free partnership with no unique code and no net-fee share")
    pdf.bullet("Unnamed SFC partner used in joint copy")
    pdf.bullet("Exclusivity without a six-figure minimum over a defined term")
    pdf.bullet("Raw tickets, CRM, or behavioral feeds")
    pdf.bullet("Education as a gate to Instant")
    pdf.bullet("Championship rules that loosen daily / trailing / Best Day")
    pdf.bullet("Repeat of Bookmap / Saudi / OHKF language after you asked for paper")

    pdf.h2("Bottom line")
    pdf.callout(
        "Joe is involved in four names: a real smoking-cessation company he chairs, a "
        "trading-education site, an institutional trading site with a PropTrade announcement "
        "and broken SFC copy, and an email-only competition vehicle. The Verodus email is a "
        "Bookmap template asking for a free logo. Verodus’s benefit is Asia origination on "
        "Instant / 1-Step / Lite, paid on net fees, rules unchanged, then maybe PropTrade on "
        "Verodus rails. Everything else in the email is either unverified or actively harmful "
        "to repeat. The meeting was useful as a filter. The email is not a proposal. Wait for "
        "a one-pager that could only have been written for Verodus. If it does not arrive, "
        "do not follow up twice."
    )

    pdf.ln(2)
    pdf.set_font("Inter", "I", 8.2)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.6,
        "Sources checked 21 August 2026: trademath.ai, trademath.ai/monimath/, lisg.ai/about-us, "
        "Joe’s LinkedIn (MoniMath PropTrade 18 Nov 2025; SFC approval 20 Nov 2025), Karma Lounge "
        "follow-up email as pasted, Our Hong Kong Foundation public site, Money20/20 / Algo "
        "Challenge Association public listings. Companion notes: docs/joe-wong-fresh-analysis.md, "
        "docs/joe-wong-email-analysis.md. Not an audit and not legal advice. Does not change "
        "website copy.",
    )

    for path in (OUT, REPO_OUT, ROOT_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        print(f"Wrote {path} pages={pdf.pages_count} bytes={path.stat().st_size}")


if __name__ == "__main__":
    build()
