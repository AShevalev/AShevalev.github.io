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
        "Label after this pass: an unproven Instant/challenge simulated-evaluation firm "
        "with careful FAQ and Terms, one UAE FZ name, and a search title of Up to $1M "
        "capital, 90% reward split. The first screen already says no deposits, no client "
        "funds, no brokerage. $49 is Instant at 35% off. $1M is combined account cap. "
        "Trustpilot already links. Bios already sit in modals. Not a scam site. Not a "
        "licensed broker. Not live capital. Not a known payer."
    )

    pdf.h2("The remaining pass (only this)")
    pdf.body(
        "Light phrase swaps plus one homepage title change. No hero rewrite. No extra "
        "line under the CTAs. No meta-description rewrite. No Instant pricing rewrite. "
        "No Trustpilot rewrite. No Why Verodus rewrite. No How it works rewrite. No FAQ "
        "rewrite except two phrases. Bios stay in the existing Read Bio modals as written."
    )
    add_table(
        pdf,
        ["In", "Out"],
        [
            [
                "Homepage title / og:title / twitter:title: Verodus | Up to $1M capital, 90% reward split.",
                "Hero H1, subhead, no deposits / no client funds / no brokerage pill, CTAs. No extra line under CTAs.",
            ],
            [
                "FAQ: drop discretionary. Terms: pay if rules + KYC; withhold for breaches.",
                "Meta description (locked): Funded on day one from $49. 1-Step from $45. Lite from $39. $5k-$200k. Keep 80%. No deposit.",
            ],
            [
                "One legal name: Verodus L.L.C.-FZ. Payments: Capital Inc. affiliate.",
                "Instant pricing module. Instant $200k is not sold; $5k-$200k is 2-Step.",
            ],
            [
                "Instant label, FAQ Instant line, dashboard, Privacy: Instant / Qualified Performance, not Funded.",
                "Trustpilot 4.5/5 (already links). Quotes. Why Verodus cards. Bio modal copy.",
            ],
            [
                "Stat strip: 3,000+ traders; 90% reward split. Keep $1M (combined cap) and <24h.",
                "How it works, calculator, bottom CTA. About opening / mission copy.",
            ],
            [
                "About: Leadership heading. Behavioral analysis -> risk control. Leave Read Bio modals.",
                "Adding Simulated accounts under the hero CTAs. Rewriting founder bios.",
            ],
            [
                "Certificates: unique IDs or hide duplicates. Copy stays Real traders. Real certificates.",
                "We sell trading data on marketing pages.",
            ],
            [
                "Privacy (counsel-gated): anonymized/aggregated data license clauses. Not on homepage.",
                "Any other section rewrite.",
            ],
        ],
        [87, 87],
    )

    pdf.h2("Product facts (stop treating these as leaks)")
    pdf.bullet(
        "$49 in the meta description is Instant at the 35% discount, not a rogue price versus the Instant table."
    )
    pdf.bullet(
        "$5k-$200k in the meta description is 2-Step account sizes. Instant does not offer $200k."
    )
    pdf.bullet(
        "$1M Max Capital is the combined cap across accounts a trader can hold, not a single Instant SKU. The new title uses that number on purpose."
    )
    pdf.bullet(
        "Trustpilot 4.5 / 5 already links to the Trustpilot site. Do not call it unclickable."
    )
    pdf.bullet(
        "Kim Chen and Alexander Vladimirovich already have photos and full bios in Read Bio modals. Keep that UI and that copy this pass."
    )

    pdf.h2("Where it puts Verodus")
    add_table(
        pdf,
        ["Audience", "Before this pass", "After this pass"],
        [
            [
                "Google / Instant buyer",
                "Title: Instant from $49. Funded on Day One. Description: Funded on day one from $49.",
                "Title: Verodus | Up to $1M capital, 90% reward split. Description unchanged ($49 Instant at 35% off; $5k-$200k = 2-Step).",
            ],
            [
                "First screen",
                "Funding Traders Worldwide. No deposits, no client funds, no brokerage.",
                "Same. No extra line under the CTAs.",
            ],
            [
                "Trader who reads FAQ / Terms",
                "Rewards are discretionary. Two legal names. Instant labeled Funded.",
                "Pays if you meet the rules and KYC. One company. Instant labeled Instant.",
            ],
            [
                "Experienced prop trader",
                "Unproven Instant shop with sloppy contradictions.",
                "Unproven Instant shop with fewer self-inflicted leaks. Still waits on payout proof.",
            ],
            [
                "Partner / bank / counsel",
                "Simulated service; entity fog; discretionary bonuses.",
                "Simulated service; one FZ entity + payment affiliate; rules-based bonuses.",
            ],
            [
                "Data buyer (if Privacy ships)",
                "Public Privacy forbids external commercialization of trading behavior.",
                "Still no PII sale. Counsel-gated anonymized feature tables only. Invisible on the homepage.",
            ],
        ],
        [40, 67, 67],
    )
    pdf.body(
        "Sector ladder: 1 clone scam  2 unproven Instant shop with sloppy copy  "
        "3 unproven Instant shop with careful copy  4 known payer with a public track record  "
        "5 licensed or live-capital firm. This pass moves Verodus from 2 toward 3. "
        "The new title sells combined cap and top split in search. It does not reach 4. "
        "Copy cannot buy 4. Verifiable payouts and independent talk can."
    )

    pdf.h2("Scorecard")
    add_table(
        pdf,
        ["Dimension", "Before", "After"],
        [
            ["Search title", "Instant from $49. Funded on Day One.", "Verodus | Up to $1M capital, 90% reward split"],
            ["Search description", "Funded on day one from $49 ... $5k-$200k. Keep 80%.", "Unchanged (correct: $49 = 35% Instant; range = 2-Step)"],
            ["Payout promise", "Discretionary", "Rules + KYC; clawback for breaches"],
            ["Legal identity", "LLC vs L.L.C.-FZ", "One FZ name + Capital Inc. affiliate"],
            ["Funded vs simulation", "Hero already: no deposits, no client funds, no brokerage. Instant cards still say Funded.", "Hero honesty stays. Instant cards say Instant."],
            ["Stat strip", "Profit split + $1M combined cap", "Reward split; $1M combined cap stays"],
            ["Social proof", "4.5 Trustpilot (linked), first-name quotes, duplicate certificates", "Trustpilot stays linked; quotes stay; duplicates should go"],
            ["About / bios", "Smashed heading; behavioral analysis; bios already in modals with photos", "Leadership; risk control; modal bios unchanged"],
            ["Public payout proof", "None independent", "Unchanged"],
        ],
        [40, 67, 67],
    )

    pdf.h2("What gets better")
    pdf.bullet(
        "Discretionary was the worst leak. Is Verodus legitimate? currently tells a careful "
        "reader you might not pay even if they followed the rules. After the swap, the same "
        "answer says you pay when rules and identity checks are met."
    )
    pdf.bullet(
        "One legal name kills the two-company / shell-stack read. Same FZ firm, one public name."
    )
    pdf.bullet(
        "Search title now matches the stat strip: combined $1M cap and 90% top split, instead of "
        "only Instant from $49. Description still sells the 35% Instant fee and 2-Step sizes."
    )
    pdf.bullet(
        "Instant as the phase label, Simulated Instant account in FAQ, and Qualified "
        "Performance on the dashboard stop repeating Funded next to simulated on every card. "
        "Hero keeps no deposits, no client funds, no brokerage."
    )
    pdf.bullet(
        "Reward split on the first strip matches Global reach and the new title."
    )
    pdf.bullet(
        "If duplicate certificate amounts go, the payout strip stops looking generated."
    )
    pdf.bullet(
        "Leadership and risk control remove two amateur tells. Bios already have faces and "
        "titles in modals. Leave that copy this pass."
    )

    pdf.h2("What still hurts")
    pdf.bullet(
        "The homepage Instant selector can still show $200k even though Instant does not "
        "sell $200k. Pricing module was skipped this pass. Meta $5k-$200k is 2-Step and is fine."
    )
    pdf.bullet(
        "Founder modals have photos and titles but no school names, prior employers, years, "
        "or LinkedIn. A stranger still cannot confirm the people from the copy alone. That "
        "is registry / LinkedIn / one filmed AMA, not a bio rewrite this pass."
    )
    pdf.bullet(
        "First-name testimonials stay. Duplicate certificates, if they remain, still cost trust."
    )
    pdf.bullet(
        "No Reddit, PropFirmMatch, or independent payout corpus. Wording does not create "
        "that. Until it exists the honest public label is unproven, not scam, not FTMO-grade."
    )

    pdf.h2("Founder bios (as they already are)")
    pdf.body(
        "Keep the existing Read Bio modals. Do not paste them onto About. Do not rewrite "
        "the paragraphs this pass."
    )
    pdf.bullet(
        "Kim Chen, Co-Founder and CEO. Photo. Finance graduate; digital-asset background; "
        "strategist and roadmap; infrastructure access. Closing quote on world-class resources."
    )
    pdf.bullet(
        "Alexander Vladimirovich, Co-Founder and COO. Photo. Honors finance graduate; "
        "FX and risk-managed trading; UX, infrastructure, processing, support. Closing quote "
        "on a reliable ecosystem."
    )
    pdf.bullet(
        "What is still missing for founder proof is off-site: same names on the FZ record, "
        "LinkedIn that opens with the same faces, one filmed AMA. That answers are these "
        "people real. It does not answer do they pay."
    )

    pdf.h2("Privacy amendment (counsel-gated, not marketing)")
    pdf.body(
        "If counsel does not sign, skip the data-sale clauses. Current Privacy still "
        "bans external commercialization of trading behavior. Shipping a MoniMath license "
        "against that text is a policy breach."
    )
    pdf.body(
        "If counsel signs and the extract is aggregated or irreversibly anonymized, "
        "Verodus can license feature tables and research labels. That does not change "
        "the homepage. Still never: PII, KYC, wallets, IPs, raw tickets that reconstruct "
        "a named trader's edge."
    )

    pdf.h2("Clean verdict")
    pdf.callout(
        "Do the edits. They close discretionary, two names, Funded as a phase label, and "
        "the smashed About heading, and they put combined $1M and 90% in the search title. "
        "After they ship, Verodus is a careful Instant shop, not a new kind of firm. "
        "Google sees $1M / 90%. The description still sells Instant from $49 at 35% off. "
        "The first screen already says no deposits, no client funds, no brokerage. "
        "Trustpilot already links. Bios already have faces. Unchanged for anyone waiting "
        "on third-party payout proof."
    )

    pdf.ln(2)
    pdf.set_font("Inter", "I", 8.2)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.6,
        "Scope: remaining items in docs/verodus-website-wording-changes.md as of 21 August "
        "2026 only. Facts from Verodus on $49 (35% Instant), $5k-$200k (2-Step), $1M "
        "(combined cap), Trustpilot link, and founder modals. Not an audit and not legal advice.",
    )

    for path in (OUT, REPO_OUT, ROOT_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        print(f"Wrote {path} pages={pdf.pages_count} bytes={path.stat().st_size}")


if __name__ == "__main__":
    build()
