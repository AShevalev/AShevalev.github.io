#!/usr/bin/env python3
"""PDF: Verodus public perception and legitimacy analysis."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/opt/cursor/artifacts/Verodus_Legitimacy_and_Perception.pdf")
REPO_OUT = Path("/workspace/docs/verodus-legitimacy-and-perception.pdf")
ROOT_OUT = Path("/workspace/verodus-legitimacy.pdf")

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
        self.cell(0, 5, "Verodus  |  Perception and legitimacy", align="L")
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


def add_table(pdf, headers, rows, col_widths):
    usable = 174
    scale = usable / sum(col_widths)
    col_widths = [w * scale for w in col_widths]
    line_h = 5.0
    if pdf.get_y() > 248:
        pdf.add_page()
    x0, y = 18, pdf.get_y()
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
    for r_i, row in enumerate(rows):
        heights = []
        for i, cell in enumerate(row):
            pdf.set_font("Inter", "B" if i == 0 else "", 8)
            n = pdf.multi_cell(col_widths[i] - 3, line_h, cell, dry_run=True, output="LINES")
            heights.append(max(1, len(n)) * line_h + 2.2)
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
    pdf.rect(0, 8, 210, 58, "F")
    pdf.set_y(16)
    pdf.set_font("Inter", "", 9)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 5, "VERODUS INTERNAL BRIEFING", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_x(18)
    pdf.set_font("Inter", "B", 22)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 9, "How people perceive Verodus, and whether it is legitimate")
    pdf.set_x(18)
    pdf.set_font("Inter", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 6, "Public-source analysis  ·  21 August 2026")

    pdf.set_y(78)
    pdf.callout(
        "Verodus is a real operating simulated-evaluation firm, not a fake website. "
        "It is not a licensed broker, not live proprietary capital, and not independently "
        "proven as a high-trust payout shop. Public perception is mostly absence of "
        "perception: almost nobody on Reddit, PropFirmMatch, WikiFX, or ForexPeaceArmy "
        "is talking about it yet. That combination is typical of a 2026 Instant/challenge "
        "product, not of FTMO-scale legitimacy and not of an obvious clone scam."
    )

    pdf.h2("How people perceive it")
    pdf.body(
        "There is almost no independent trader conversation to measure. Searches of Reddit, "
        "PropFirmMatch-style aggregators, WikiFX, and general “scam / legit / payout” "
        "threads return the company’s own site plus SEO/content-farm articles, not trader "
        "war stories."
    )
    pdf.body("What exists instead:")
    pdf.bullet(
        "The story Verodus tells. “Funding traders worldwide,” Instant from $49, 175+ "
        "countries, +3,000 users, up to 90% split, $1M max capital, “real traders, real "
        "certificates,” 4.5/5 Trustpilot, payouts under 24 hours via Rise/crypto. Homepage "
        "testimonials are first-name + country with no review IDs."
    )
    pdf.bullet(
        "The story a skeptical prop trader hears. After MyForexFunds and a wave of Instant "
        "shops, the default read of a new UAE-FZ “prop firm” is: pay a fee, trade a demo, "
        "most people fail, a few get paid if rules and KYC cooperate. Verodus’s own FAQ "
        "answers “Is Verodus legitimate?” by saying it is not a brokerage, trading is "
        "simulated, fees are service fees, and rewards are discretionary. That is honest. "
        "It is also the opposite of how many buyers interpret “Funded on Day One.”"
    )
    pdf.bullet(
        "The story SEO farms tell. Third-party posts on generic blogs recycle Verodus copy "
        "as if it were independent journalism. That inflates perceived prestige without "
        "adding verification."
    )
    pdf.body(
        "What is missing is the perception problem. Established names get Reddit payout "
        "threads, Trustpilot volume, YouTube rule breakdowns, and aggregator ratings. "
        "Verodus currently has none of that visible footprint. To the market it looks like "
        "a new, small, self-advertised Instant brand. Silence is not proof of a scam; it is "
        "proof the brand has not earned a reputation yet."
    )

    pdf.h2("What “legitimate” means here")
    pdf.body("Traders mix four different questions:")
    add_table(
        pdf,
        ["Question", "Straight answer"],
        [
            [
                "Is it a real company with a real product?",
                "Yes. Live site, published rules (August 2026), dashboard, MT5 (Platform 5) + TradeHub, KYC, Rise/crypto rails, Discord/live chat.",
            ],
            [
                "Is it a regulated broker or investment firm?",
                "No, and it says so. UAE FZ + a payment company is a service business, not SCA/CFTC/FCA/SFC licensing.",
            ],
            [
                "Does “funded” mean live market capital?",
                "No. Simulated accounts. Rewards, if paid, come from company cash against simulated P&L.",
            ],
            [
                "Will it pay me if I pass?",
                "Unproven in public. Terms make rewards discretionary. Homepage certificates are firm-issued graphics, not bank/Rise/on-chain proof.",
            ],
        ],
        [62, 112],
    )
    pdf.body(
        "Industry-wide, simulated prop is a legal grey product: sell evaluations, fail most "
        "buyers, pay a minority. CFTC Rule 4.41 hypothetical-performance language is on "
        "Verodus’s risk page. That is more careful than many competitors. It does not make "
        "payouts a debt."
    )

    pdf.h2("Evidence that supports legitimacy")
    pdf.bullet(
        "Disclosures are unusually explicit. Instant/1-Step/2-Step pages state simulation, "
        "no live capital, rewards paid from Verodus resources. Risk disclosure (21 Feb 2026) "
        "says pass rates are historically low and the fee is money you can lose. Terms: no "
        "live routing, no matching engine."
    )
    pdf.bullet(
        "The product is specified, not vapor. Instant: 3% daily / 6% trailing that never "
        "locks / Best Day ≤20%. 1-Step: 10% target, 4%/6% hybrid, Best Day ≤50%. 2-Step Lite: "
        "8% then 5%, static 8%/4% daily. Prohibited list (HFT, latency arb, copy EAs) is "
        "standard and published."
    )
    pdf.bullet(
        "Payment and KYC vendors are real categories. Rise and Veriff (named in FAQs) are "
        "used by other prop shops. That is operational plumbing, not a regulator stamp."
    )
    pdf.bullet(
        "Sanctions and US MT5 limits exist. Restricted-country list is OFAC-style. Platform 5 "
        "is blocked for US persons. That is how a firm trying to stay on MetaQuotes/payments "
        "rails behaves."
    )
    pdf.bullet(
        "Scale claim is modest. +3,000 users is small versus FTMO/FundedNext. Inflating to "
        "hundreds of thousands would look faker."
    )

    pdf.h2("Evidence that weakens legitimacy as traders judge it")
    pdf.bullet(
        "Entity fog. Terms: Verodus L.L.C.-FZ, Dubai law. Privacy/risk: Verodus LLC. Money: "
        "Verodus Capital Inc. (all fees and rewards). No published free-zone, license number, "
        "or office address."
    )
    pdf.bullet(
        "Trustpilot claim vs independent profile. Homepage says 4.5/5. A loadable Trustpilot "
        "business unit for verodus.com was not confirmed in this research. A rating you "
        "cannot click through is a credibility leak."
    )
    pdf.bullet(
        "Payout proof is self-issued. “Verified withdrawal certificates” with first names "
        "and flags are marketing. Duplicate $9,401.23 for both Jose and Joe (US) on the "
        "carousel looks generated. Independent standard is Rise/Deel emails, bank credits, "
        "or crypto txids from many distinct traders."
    )
    pdf.bullet(
        "Copy drift. Blog still describes 10%/5% targets and 10%/5% drawdowns and “from $55.” "
        "Live Instant table does not match the “from $49” hero. Traders screenshot that."
    )
    pdf.bullet(
        "Legal right not to pay. “Performance rewards are discretionary and are not liabilities "
        "of Verodus L.L.C.-FZ.” Combined with clawback, risk interviews, and broad “spirit of "
        "the rules” language, a trader can pass the numbers and still be unpaid. Common in "
        "the sector; also why forums brand firms “legit” only after months of independent "
        "payout posts."
    )
    pdf.bullet(
        "Founders are titles only. Kim Chen (CEO) and Alexander Vladimirovich (COO) have no "
        "substantial public bios tied to the brand. Fine at 3,000 users; weak if asking "
        "strangers for fees."
    )
    pdf.bullet(
        "SEO farms, thin community. No Reddit corpus, no PropFirmMatch page found, no pile "
        "of YouTube rule reviews. Perception will be set by whoever writes first — affiliates "
        "or angry failed Instant accounts."
    )

    pdf.h2("How a typical trader will bucket it")
    pdf.bullet(
        "Retail buyer of Instant. Sees “funded day one,” cheap fee, 90% split. May not read "
        "that it is a demo with a never-locking 6% trail and 20% Best Day gate. After a fast "
        "breach, the perception becomes “rigged Instant shop,” which is the industry default "
        "complaint, not unique to Verodus."
    )
    pdf.bullet(
        "Experienced prop trader. Sees simulation + discretionary rewards + UAE FZ + no forum "
        "proof and waits. They will not call it a scam; they will call it unproven."
    )
    pdf.bullet(
        "Regulator / bank / partner. Sees a digital evaluation service, not a licensed "
        "intermediary. Legitimate as that, if marketing stays inside the simulation/"
        "discretionary box. “Funded,” “capital,” and “profit split” language still invites "
        "confusion."
    )

    pdf.h2("Bottom line")
    pdf.callout(
        "Not a fake site. Product, rules, KYC path, and legal stack exist. Not a licensed "
        "prop desk. Simulated evaluation plus company-paid bonuses. Not publicly proven to "
        "pay at scale. Certificates are not third-party proof. Not currently infamous as a "
        "scam — there is no visible complaint wave because there is almost no public user "
        "base talking. The honest label: early-stage, legally cautious simulated prop, "
        "reputation not yet earned. Legitimacy in this business is paid for with verifiable "
        "payouts and consistent public operations, not with a 4.5 badge and a certificate "
        "carousel."
    )

    pdf.ln(2)
    pdf.set_font("Inter", "I", 8.2)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.6,
        "Sources: verodus.com (home, about, Instant, 1-Step, 2-Step Lite, FAQ, Terms, Privacy "
        "21 Feb 2026, Risk Disclosure, blog); public searches of Reddit, PropFirmMatch, WikiFX, "
        "Trustpilot, and SEO reprints. Internal commercial memo from public materials. Not an "
        "audit and not legal advice.",
    )

    for path in (OUT, REPO_OUT, ROOT_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        print(f"Wrote {path} pages={pdf.pages_count} bytes={path.stat().st_size}")


if __name__ == "__main__":
    build()
