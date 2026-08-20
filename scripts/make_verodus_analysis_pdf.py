#!/usr/bin/env python3
"""Render an internal Verodus company analysis PDF (same format as the MoniMath briefing)."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/opt/cursor/artifacts/verodus_company_analysis.pdf")
REPO_OUT = Path("/workspace/docs/verodus-company-analysis.pdf")

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
        self.cell(0, 5, "Verodus  |  Company analysis", align="L")
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
        self.set_draw_color(*GREEN)
        self.set_line_width(1.6)
        self.line(18.8, start - 1.5, 18.8, end + 1.2)
        self.set_line_width(0.2)
        self.ln(3)


def add_table(pdf: BriefingPDF, headers, rows, col_widths):
    usable = 174
    scale = usable / sum(col_widths)
    col_widths = [w * scale for w in col_widths]
    line_h = 5.0
    if pdf.get_y() > 248:
        pdf.add_page()
    x0 = 18
    y = pdf.get_y()
    pdf.set_fill_color(*GREEN)
    pdf.set_text_color(*WHITE)
    pdf.set_font("InterSB", "", 8)
    header_h = 8
    pdf.rect(x0, y, usable, header_h, "F")
    x = x0
    for i, h in enumerate(headers):
        pdf.set_xy(x + 1.5, y + 1.6)
        pdf.multi_cell(col_widths[i] - 3, 4.4, h)
        x += col_widths[i]
    y += header_h
    pdf.set_text_color(*INK)
    for r_i, row in enumerate(rows):
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
    pdf.multi_cell(0, 10, "Verodus: what the firm actually is, how it makes money, and what to consider")
    pdf.ln(1)
    pdf.set_font("Inter", "", 11)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 6, "Research summary and strategic analysis  ·  20 August 2026")
    pdf.set_y(82)
    pdf.callout(
        "Verodus is a small, live simulated evaluation firm with a working CRM, "
        "MT5/TradeHub stack, and unusually careful legal language for this industry. "
        "It is not a broker and not a capital allocator. Economics are evaluation fees "
        "plus tightly gated discretionary payouts. Scale is the constraint: about 3,000 "
        "users against a market where the top five firms take most of the flow. The "
        "scarce asset is labeled trader-behavior data. The risk is copy drift, entity "
        "inconsistency, and a Trustpilot claim that is not easy to verify independently."
    )

    pdf.h2("Who Verodus actually is")
    pdf.body(
        "Public identity: a simulated proprietary-trading evaluation firm at verodus.com. "
        "Traders pay a service fee, trade a market-referenced demo under published rules, "
        "and, if they qualify, can request performance rewards paid from Verodus’s own "
        "resources. No client funds, no brokerage, no live order routing."
    )
    pdf.body("Legal entities named on the public site (they do not all match):")
    pdf.bullet("Verodus L.L.C.-FZ — Terms of Service; Dubai / UAE governing law and courts.")
    pdf.bullet("Verodus LLC — Privacy Policy data controller; Risk Disclosure.")
    pdf.bullet(
        "Verodus Capital Inc. — all registration fees and performance rewards. "
        "Terms state no payments are processed by or payable to the FZ entity."
    )
    pdf.body(
        "That split is a standard free-zone plus payment-company pattern. It is also a "
        "diligence item: three names for one brand, no published free-zone (IFZA, Meydan, "
        "DMCC, etc.), no license number, no registered address on the pages reviewed. "
        "Kim Chen is listed as Co-Founder & CEO; Alexander Vladimirovich as Co-Founder & COO. "
        "Public bios beyond those titles were not found."
    )
    pdf.body(
        "What it is not: not SFC/FCA/CFTC licensed, not a fund, not live prop capital. "
        "FAQ last updated 9 February 2026: Platform 5 (MT5) is unavailable to US citizens "
        "or residents; TradeHub remains. Restricted countries follow OFAC-style sanctions "
        "(Russia, Iran, DPRK, Syria, Venezuela, Belarus, and others)."
    )

    pdf.h2("What Verodus is trying to do")
    pdf.body(
        "The operating plan, stripped of marketing: sell cheap simulated evaluations at "
        "global scale; fail most buyers against tight risk rules; pay a minority who stay "
        "inside drawdown, consistency, and payout gates; keep the brand on the right side "
        "of “this is a simulation, rewards are discretionary.” Instant Funding is the "
        "acquisition wedge (“from $49, funded on day one”). 1-Step and 2-Step Lite/Pro "
        "are the classic challenge funnel. The dashboard, mobile app, Rise/crypto payouts, "
        "and withdrawal certificates are the trust layer."
    )
    pdf.body(
        "Stated scale as of the homepage: +3,000 users, 175+ countries, up to 90% split, "
        "$1M max capital. Household cap in Terms is USD 400,000 of allocated simulated "
        "capital. Industry context: Track360’s 2026 retail-prop estimate is on the order "
        "of USD 850 million revenue and 12 million challenge purchases, with the top five "
        "firms taking most acquisition. At 3,000 users Verodus is an early operator, not "
        "a category leader. That is the exposure problem."
    )

    pdf.h2("Product and rules (as published, August 2026)")
    add_table(
        pdf,
        ["Program", "How you get in", "Risk gates", "Payout gates"],
        [
            [
                "Instant",
                "Pay and trade. No profit target. Sizes $5k–$100k.",
                "3% daily from that day’s equity high; 6% trailing max that never locks.",
                "Best Day ≤20% of Positive Days’ Profit. $100 min. Instant fees not refunded.",
            ],
            [
                "1-Step",
                "10% profit target. No min trading days. Up to $200k.",
                "4% daily; 6% hybrid max (trails, then locks at initial balance).",
                "Best Day ≤50%. First payout refunds the challenge fee.",
            ],
            [
                "2-Step Lite",
                "8% then 5%. 5 trading days per phase. Static 8% max, 4% daily. Leverage 1:100 FX.",
                "Static floor (example: $100k cannot go below $92k).",
                "3 trading days in Qualified Performance. Fee refund on first payout.",
            ],
            [
                "2-Step Pro",
                "Two-phase evaluation (site lists as a separate SKU alongside Lite).",
                "Published on the objectives / Pro pages; same payout-cycle add-ons.",
                "Same 70/80/90% weekly / bi-weekly / on-demand structure.",
            ],
        ],
        [28, 48, 50, 48],
    )
    pdf.body(
        "Shared plumbing: unlimited time, 30-day inactivity kill, Friday flatten 22:00 UTC "
        "(weekend holding is an add-on), news trading allowed but news-bracketing / gap "
        "holds banned, EAs allowed except HFT, latency arb, mass-distributed copy EAs, "
        "and >2,000 server requests/day. KYC via a third party (Veriff is named in FAQs) "
        "before Qualified Performance. Rewards via Rise (bank, local rails, crypto) or wallet. "
        "Default split 80%; 90% with On-Demand add-on; 70% weekly add-on."
    )
    pdf.body(
        "Legal character of payouts: Terms say performance rewards are discretionary and "
        "are not liabilities of the FZ company. That is the model that keeps this a "
        "service business rather than an investment contract — and the clause counterparties "
        "and regulators will read first."
    )

    pdf.h2("How the money actually works")
    pdf.body(
        "Gross profit is evaluation / Instant fees, resets, and add-ons (weekend holding, "
        "payout-speed splits). Cost is payouts, payment processing, chargebacks, MT5/TradeHub "
        "infra, KYC, support, and acquisition. Instant is the high-margin SKU: no fee refund, "
        "tighter trailing drawdown that never locks, and a 20% Best Day rule that delays "
        "payouts even after a lucky day. 1-Step / 2-Step refund the challenge fee on first "
        "successful payout, so those SKUs only pay if most buyers never reach a clean payout."
    )
    pdf.body(
        "This is why “make traders better” is not automatically good for Verodus. A higher "
        "pass rate without a matching jump in volume or a new cash line (data license, "
        "education add-on, white-label GMV) transfers margin to payouts. Volume at the "
        "current rule set is the growth that fits the P&L."
    )
    add_table(
        pdf,
        ["Revenue lever", "What it is", "Strategic note"],
        [
            [
                "Challenge / Instant fees",
                "One-time, non-refundable once trading starts.",
                "Core. Protect fail rate. Grow units.",
            ],
            [
                "Add-ons",
                "Weekend holding, weekly 70%, on-demand 90%.",
                "High margin. Do not hide them; price them.",
            ],
            [
                "Funded profit share",
                "10–30% of simulated profit after gates.",
                "Secondary. Real only if survivors last.",
            ],
            [
                "Data (latent)",
                "Anonymized CRM behavioral / lifecycle labels.",
                "Not live. Privacy policy currently forbids external commercialization.",
            ],
            [
                "White-label / affiliate",
                "Other brands originate flow onto Verodus rails.",
                "Best path to Asia exposure without raising pass rates.",
            ],
        ],
        [40, 62, 72],
    )

    pdf.h2("The data asset")
    pdf.body(
        "The CRM already produces what most “AI trading” shops cannot buy: labeled sequences "
        "of how retail traders pass, fail, and blow up under known rules (sizing volatility, "
        "news-window flags, best-day concentration, time-to-breach, evaluation vs later "
        "survival). About-page language already says activity is for performance evaluation "
        "and behavioral analysis."
    )
    pdf.body(
        "Constraint: the 21 February 2026 Privacy Policy says Verodus does not commercialize "
        "or exploit user trading strategies externally, and that trader P&L / behavior data "
        "is shared internally only. “The CRM vendor allows resale” does not override that. "
        "Anonymized aggregates and irreversible feature tables can be licensed after a policy "
        "amendment, DPA, and counsel memo. PII, KYC, wallets, IPs, and copy-tradable tickets "
        "should not be sold. That is the same gate used in the MoniMath analysis."
    )

    pdf.h2("Competitive position")
    pdf.body(
        "Category: retail simulated prop, 2026. Competitors (FTMO, FundedNext, The5ers, E8, "
        "Apex, Topstep) compete on price, payout speed, Trustpilot volume, affiliate armies, "
        "and whether traders believe payouts actually land. Verodus’s differentiation on "
        "paper is clarity (rules on the site, not only in a PDF), Instant as a lead SKU, "
        "free trials with no cap stated, dual platforms from one account, and unusually "
        "explicit “this is simulated / discretionary” legal copy — a lesson from CFTC v. "
        "MyForexFunds-style enforcement."
    )
    pdf.body(
        "Gaps versus leaders: user count, independent review density, named banking/free-zone "
        "footprint, and US MT5 access. Instant trailing-never-locks plus 20% Best Day is "
        "trader-hostile relative to looser Instant shops; that is good for P&L and bad for "
        "YouTube affiliates unless payouts are visibly real."
    )

    pdf.h2("What looks strong")
    pdf.bullet(
        "Product is real: published rule pages dated August 2026, dashboard, two platforms, "
        "KYC, Rise/crypto, inactivity and household caps, prohibited-practice taxonomy."
    )
    pdf.bullet(
        "Legal posture is more careful than typical prop marketing: simulation disclaimers "
        "on Instant/1-Step/2-Step pages; FAQ “is Verodus legitimate?” answers the model "
        "honestly; rewards called discretionary."
    )
    pdf.bullet(
        "Instant + Best Day + trailing drawdown is a coherent fail-heavy machine, not an accident."
    )
    pdf.bullet(
        "Data exhaust is scarce and valuable if licensed without leaking edge or PII."
    )
    pdf.bullet(
        "Global payment and sanctions list exist; US is handled by dropping MT5 rather than pretending."
    )

    pdf.h2("What to consider / fix")
    pdf.numbered(
        1,
        "Entity hygiene. Align Privacy (Verodus LLC), Terms (Verodus L.L.C.-FZ), payments "
        "(Verodus Capital Inc.), and Risk Disclosure. Publish free-zone, license activity, "
        "and a service address. Counterparties (MoniMath, Rise, MetaQuotes, banks) will ask.",
    )
    pdf.numbered(
        2,
        "Trustpilot. Homepage says 4.5/5. An independent, loadable review profile was not "
        "confirmed in this research; third-party snippets conflict. Either claim a live "
        "Trustpilot URL with a real score, or drop the number. Review inflation is how this "
        "category gets punished in public.",
    )
    pdf.numbered(
        3,
        "Copy drift. Blog “best simulated prop firm 2026” still describes 10%/5% targets "
        "and 10%/5% drawdowns that do not match live Instant/1-Step/Lite pages. Homepage "
        "hero “from $49” vs Instant table ($72 struck from $110 on the $5k tier, and $100k "
        "Instant at $399/$614). Payout carousel repeats $9,401.23 for both “Jose” and “Joe” "
        "in the US. Traders screenshot this.",
    )
    pdf.numbered(
        4,
        "Certificate authenticity. If withdrawal certificates are real, make the unique ID "
        "verifiable. Duplicate round numbers on the homepage look generated.",
    )
    pdf.numbered(
        5,
        "Privacy vs data strategy. Do not sell behavioral data under the current policy. "
        "Amend first: anonymized research license yes; strategy replication no.",
    )
    pdf.numbered(
        6,
        "Scale without destroying the model. Growth should be more buyers at current rules "
        "(affiliates, Asia white-label, SEO) not easier rules. Education only as a paid add-on.",
    )
    pdf.numbered(
        7,
        "MetaQuotes / US. Platform 5 blocked for US persons is correct and fragile. Have a "
        "written fallback if MT5 prop access tightens further.",
    )
    pdf.numbered(
        8,
        "Discretionary payouts vs brand. The clause protects you; slow or opaque payouts "
        "kill affiliates. Publish a monthly payout total or certificate verifier.",
    )
    pdf.numbered(
        9,
        "Founder surface area. Kim Chen and Alexander Vladimirovich have titles and almost "
        "no public bios. For a 3,000-user shop that is fine; for banking, listing, or a "
        "Hong Kong partner it is a gap.",
    )
    pdf.numbered(
        10,
        "SEO farms. Third-party posts (content-mill style) already recycle Verodus copy. "
        "Own the narrative or those pages will define you in search.",
    )

    pdf.h2("Strategic recommendations")
    pdf.body("If the goals are exposure and financial profit, in this order:")
    pdf.numbered(
        1,
        "Keep Instant as the paid front door. Do not loosen the 6% never-lock trail or 20% "
        "Best Day to win affiliate YouTube. Show payouts instead.",
    )
    pdf.numbered(
        2,
        "Buy distribution, do not donate data. Affiliates and white-label (including a paid "
        "MoniMath origination deal) add fail-heavy volume. Data is a separate cash SKU after "
        "counsel updates the privacy policy.",
    )
    pdf.numbered(
        3,
        "Fix public consistency this month: entity names, Trustpilot, pricing hero vs table, "
        "blog vs live rules, duplicate certificate amounts.",
    )
    pdf.numbered(
        4,
        "Productize the CRM: anonymized benchmark reports, partner API, optional coaching "
        "add-on. That is high-margin and does not require raising pass rates.",
    )
    pdf.numbered(
        5,
        "Treat 3,000 users as a data moat in training, not as a finished market. The firm "
        "that reaches 30,000–50,000 evaluations with the same risk engine has a sellable "
        "behavior dataset and a real affiliate story. The firm that stays at 3,000 with "
        "messy Trustpilot copy does not.",
    )

    pdf.h2("Bottom line")
    pdf.callout(
        "Verodus is a real, small, legally cautious simulated-evaluation business whose "
        "P&L depends on people buying challenges and mostly not getting paid. That is a "
        "valid service model if disclosures stay honest and payouts that do go out are "
        "visible. The upside is volume plus a later data license. The downside is looking "
        "like every other Instant shop with unverifiable social proof. Fix the public "
        "inconsistencies, do not loosen rules for “exposure,” and only sell anonymized "
        "data after the privacy policy says you can."
    )
    pdf.ln(3)
    pdf.set_font("Inter", "I", 8.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.8,
        "Sources: verodus.com (home, about, Instant, 1-Step, 2-Step Lite, trading objectives, "
        "FAQ, Terms, Privacy 21 Feb 2026, Risk Disclosure, Responsible Trading, blog). "
        "Industry context: Track360 2026 retail-prop estimates. This is an internal "
        "commercial memo from public materials, not an audit and not legal advice.",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPO_OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    pdf.output(str(REPO_OUT))
    print(f"Wrote {OUT} pages={pdf.pages_count} bytes={OUT.stat().st_size}")
    print(f"Wrote {REPO_OUT}")


if __name__ == "__main__":
    build()
