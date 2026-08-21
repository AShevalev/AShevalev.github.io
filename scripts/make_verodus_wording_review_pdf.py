#!/usr/bin/env python3
"""PDF: where Verodus sits if the remaining wording changes ship."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/opt/cursor/artifacts/Verodus_Wording_Changes_Review.pdf")
REPO_OUT = Path("/workspace/docs/verodus-after-wording-review.pdf")
ROOT_OUT = Path("/workspace/verodus-wording-review.pdf")

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
        self.cell(0, 5, "Verodus  |  After wording changes", align="L")
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
    pdf.multi_cell(0, 9, "Where these wording changes put Verodus")
    pdf.set_x(18)
    pdf.set_font("Inter", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        6,
        "Clean review of the remaining copy brief  ·  21 August 2026",
    )

    pdf.set_y(78)
    pdf.callout(
        "These edits move Verodus one step up inside the Instant/challenge category: "
        "from an unproven shop that sounds like it might not pay, to an unproven shop "
        "that says it pays when you follow the rules. They do not move it out of that "
        "category. Hero and meta still sell Instant funding. Public payout proof, "
        "Trustpilot, $1M max capital, and the $49 vs $72 price gap are unchanged."
    )

    pdf.h2("What actually ships")
    pdf.body(
        "The brief is now light phrase swaps, not a site rewrite. If implemented as written:"
    )
    pdf.bullet(
        "One legal name. Footer, Privacy, and Terms say Verodus L.L.C.-FZ. Payments stay "
        "with Verodus Capital Inc. as an affiliate. LLC and L.L.C.-FZ are no longer "
        "presented as two firms."
    )
    pdf.bullet(
        "Payouts are rules-based. The legitimacy FAQ no longer says rewards are "
        "discretionary. Terms say you pay when published rules, eligibility, and KYC "
        "are met, and you withhold or claw back for breaches."
    )
    pdf.bullet(
        "Funded is used less below the fold. Instant phase label becomes Instant. FAQ "
        "says Simulated Instant account. Dashboard and Privacy say Qualified Performance "
        "instead of funded accounts. Hero and meta still say Funded on Day One."
    )
    pdf.bullet(
        "Stat strip: 3,000+ traders and up to 90% reward split. $1M Max Capital and "
        "<24h Reward Processing stay."
    )
    pdf.bullet(
        "About: smashed Architects of Scale heading becomes Leadership. Behavioral "
        "analysis becomes risk control. Bios stay in Read Bio modals."
    )
    pdf.bullet(
        "Certificates: unique IDs or hide duplicates. Headline and body copy stay "
        "Real traders. Real certificates."
    )
    pdf.bullet(
        "Blog body numbers aligned to live Instant/1-Step/Lite, or the article is unpublished."
    )

    pdf.h2("What does not change")
    pdf.bullet(
        "Hero: Funding Traders Worldwide. Instant from $49. Funded on Day One. Same "
        "subhead and CTAs."
    )
    pdf.bullet(
        "Meta description stays: Funded on day one from $49. Pass a 1-Step from $45 or "
        "Lite from $39. Trade Forex, indices and crypto on $5k-$200k. Keep 80%. No deposit."
    )
    pdf.bullet(
        "Instant pricing module: $200k Instant still in the homepage table, leftover "
        "$296 / -35% line, no new refund sentence."
    )
    pdf.bullet(
        "Trustpilot 4.5/5 stays. Generic testimonials stay. Why Verodus cards stay. "
        "How it works stays. FAQ What is Verodus stays a proprietary trading evaluation "
        "firm. No Personal Capital does not add Trading is simulated."
    )

    pdf.h2("Where it puts Verodus")
    add_table(
        pdf,
        ["Audience", "Before", "After these edits"],
        [
            [
                "Google / Instant buyer",
                "Funded on day one from $49. Keep 80%. $5k-$200k.",
                "Unchanged. First impression is still Instant funding at a cheap fee.",
            ],
            [
                "Trader who reads FAQ / Terms",
                "Rewards are discretionary. Two legal names. Instant labeled Funded.",
                "Pays if you meet the rules and KYC. One company name. Instant labeled Instant.",
            ],
            [
                "Experienced prop trader",
                "Unproven Instant shop with sloppy contradictions.",
                "Unproven Instant shop with fewer contradictions. Still waits for payout proof.",
            ],
            [
                "Partner / bank / counsel",
                "Simulated service; entity fog; discretionary bonuses.",
                "Simulated service; one FZ entity + payment affiliate; rules-based bonuses.",
            ],
        ],
        [42, 66, 66],
    )
    pdf.body(
        "On the sector ladder this is a move from step 2 toward step 3, not a jump to "
        "step 4. 1) clone scam  2) unproven Instant shop with sloppy copy  3) unproven "
        "Instant shop with careful copy  4) known payer with public track record  "
        "5) licensed / live-capital firm. Copy cannot buy step 4. Payouts and independent "
        "talk can."
    )

    pdf.h2("What gets better")
    pdf.bullet(
        "The highest-trust leak on the site was discretionary. A trader who asked Is "
        "Verodus legitimate? was told you might not pay even if they followed the rules. "
        "After the swap, the same answer says you pay when rules and identity checks "
        "are met. That is the one line that actually changes how a careful reader buckets "
        "the firm."
    )
    pdf.bullet(
        "One legal name removes the two-company read. Privacy saying Verodus LLC and "
        "Terms saying Verodus L.L.C.-FZ looked like a shell stack. Same company, one "
        "public name, is what a real FZ operator should show."
    )
    pdf.bullet(
        "Funded as an Instant phase label next to simulated capital was the bait-and-switch "
        "feel below the fold. Instant / Simulated Instant account / Qualified Performance "
        "lets the hero keep search language without repeating it on every card."
    )
    pdf.bullet(
        "Reward split on the first stat strip matches the later Global reach strip. "
        "Profit split implied live P&L."
    )
    pdf.bullet(
        "If duplicate certificate amounts disappear, the payout block stops looking generated. "
        "If they do not, that block still costs more trust than it buys."
    )
    pdf.bullet(
        "Leadership instead of Architects of ScaleEngineering, and risk control instead of "
        "behavioral analysis, remove two amateur tells. They do not create founder proof; "
        "bios stay in modals."
    )

    pdf.h2("What still hurts")
    pdf.bullet(
        "$49 in hero and meta vs Instant table from $72. You chose not to touch this. "
        "Screenshotters still will."
    )
    pdf.bullet(
        "Meta says $5k-$200k and Keep 80%. Instant FAQ still says no $200k Instant and "
        "default 80% / 90% with On-Demand. Homepage Instant selector can still show $200k. "
        "Pricing module was skipped, so that SKU mismatch stays live."
    )
    pdf.bullet(
        "$1M Max Capital stays on the first strip while live SKUs top out at $100k Instant "
        "/ $200k evaluation. That number still looks invented."
    )
    pdf.bullet(
        "Rated 4.5 / 5 on Trustpilot stays without a confirmed clickable profile. "
        "First-name testimonials stay. Social proof is still self-issued."
    )
    pdf.bullet(
        "Simulation honesty still lives in FAQ, Instant rules, and legal pages, not next "
        "to Funding Traders Worldwide. Retail Instant buyers will still hear funded. "
        "Experienced traders will still hear demo."
    )
    pdf.bullet(
        "No Reddit, PropFirmMatch, or independent payout corpus. Wording does not create "
        "that. Until it exists, the honest public label remains unproven, not scam and "
        "not FTMO-grade."
    )

    pdf.h2("Clean verdict")
    pdf.callout(
        "After these changes Verodus is a careful Instant/challenge simulated-evaluation "
        "firm with one UAE FZ name and a rules-based payout promise. It is still not a "
        "broker, still not live capital, still not publicly proven to pay at scale, and "
        "still marketed in search as Funded on day one from $49. Attractive to Instant "
        "buyers on Google. Less alarming to traders who read FAQ and Terms. Unchanged "
        "for anyone waiting on third-party payout proof."
    )
    pdf.body(
        "Do these edits. They are cheap and they close the worst self-inflicted leaks "
        "(discretionary, two names, Funded as a phase label, smashed About heading). "
        "Do not expect them to reposition the brand. Reputation in this category is paid "
        "for with verifiable payouts, a Trustpilot people can open, and numbers that match "
        "checkout. Those are still outside this pass."
    )

    pdf.ln(2)
    pdf.set_font("Inter", "I", 8.2)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.6,
        "Scope: remaining items in docs/verodus-website-wording-changes.md as of 21 August "
        "2026. Compared with live verodus.com (hero, meta, Instant table, FAQ, About, "
        "Terms, Privacy). Not an audit and not legal advice.",
    )

    for path in (OUT, REPO_OUT, ROOT_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        print(f"Wrote {path} pages={pdf.pages_count} bytes={path.stat().st_size}")


if __name__ == "__main__":
    build()
