#!/usr/bin/env python3
"""PDF: Revised Joe Wong suggestions after Bookmap pairing research."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/opt/cursor/artifacts/Joe_Wong_Revised_Suggestions.pdf")
REPO_OUT = Path("/workspace/docs/joe-wong-revised-suggestions.pdf")
ROOT_OUT = Path("/workspace/joe-wong-revised-suggestions.pdf")

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
        self.cell(0, 5, "Verodus  |  Revised suggestions on Joe Wong", align="L")
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
        needed = 5.4 * max(1, len(self.multi_cell(0, 5.4, text, dry_run=True, output="LINES")))
        if self.get_y() + needed + 6 > 275:
            self.add_page()
        start = self.get_y()
        self.set_x(22)
        self.set_font("InterM", "", 10.2)
        self.set_text_color(*INK)
        self.multi_cell(168, 5.4, text)
        end = self.get_y()
        self.set_draw_color(*GREEN)
        self.set_line_width(1.6)
        self.line(18.8, start - 1.5, 18.8, end + 1.2)
        self.set_line_width(0.2)
        self.ln(3)

    def warn(self, text):
        self.ln(1)
        needed = 5.4 * max(1, len(self.multi_cell(0, 5.4, text, dry_run=True, output="LINES")))
        if self.get_y() + needed + 6 > 275:
            self.add_page()
        start = self.get_y()
        self.set_x(22)
        self.set_font("InterM", "", 10.2)
        self.set_text_color(*INK)
        self.multi_cell(168, 5.4, text)
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
    if pdf.get_y() > 238:
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
    pdf.rect(0, 8, 210, 52, "F")
    pdf.set_y(16)
    pdf.set_font("Inter", "", 9)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 5, "VERODUS INTERNAL  ·  REVISED AFTER BOOKMAP PAIRINGS", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_x(18)
    pdf.set_font("Inter", "B", 20)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 8.0, "What to do with Joe Wong, and what Verodus should consider")
    pdf.set_x(18)
    pdf.set_font("Inter", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 6, "22 August 2026  ·  For Alexander and Kim  ·  Not an offer")

    pdf.set_y(72)
    pdf.callout(
        "Do the referral. Do not do the logo, the data, or the engine-as-his-product. "
        "Three asks, three documents, never one yes."
    )
    pdf.warn(
        "The 20 August memo still treated a data license as Layer A. That is out. "
        "Live Privacy forbids external commercialization and external sharing of "
        "trading-behavior data. Do not volunteer it."
    )

    pdf.h2("Revised posture")
    add_table(
        pdf,
        ["Ask (Kim, in the room)", "Email (after Karma Lounge)", "Verodus position"],
        [
            [
                "% of “profits” from directing customers",
                "Not written. Unpaid official long-term partner instead",
                "Yes, if unique code + 15–25% of net eval fees on Instant / 1-Step / Lite. 90 days. Not trader payouts. Not company P&L.",
            ],
            [
                "No competition engine; he needs yours",
                "Bookmap leftover: order-flow visualization, free logo on a 2027 HK final",
                "Later, if the 90-day code clears a checkout floor. White-label only. Verodus keeps the stack (~70–85% GMV). No CRM fork.",
            ],
            [
                "“We share the data”",
                "Not in the letter; TAMS still needs labeled tickets",
                "No. Not as a sweetener. Not to make the championship real. Counsel would have to amend Privacy + DPA, and even then you would sell it.",
            ],
        ],
        [48, 52, 74],
    )
    pdf.body(
        "Bookmap’s live prop pairs (10FOUR, EdgeProp, Trade The Pool, historically TickTickTrader) "
        "keep heatmap vendor and eval shop separate. Joe assigned Bookmap’s product to Verodus. "
        "10FOUR — HK Instant, 90%, CQG, Rise — is the shop Bookmap actually signed on 11 August, "
        "ten days before he emailed you. Competitor category, not a partner you inherit."
    )

    pdf.h2("What to say to Joe")
    pdf.h3("1. Correct the product first")
    pdf.body(
        "Send the already-drafted reply. Do not attach a term sheet. Make him describe Verodus "
        "correctly first. His next note must name Instant / 1-Step / Lite, a unique code, one "
        "contracting entity, and — only if he still wants those words in joint copy — SFC CE "
        "numbers, an OHKF contact, and the Saudi organizer. If it still cannot name Instant vs "
        "1-Step vs Lite, do not follow up twice."
    )

    pdf.h3("2. Offer only the referral")
    add_table(
        pdf,
        ["Item", "Position"],
        [
            ["SKUs", "Instant, 1-Step, Lite. Not 2-Step Pro. Not a custom championship account."],
            ["Rules", "Unchanged. Daily loss, trail, Best Day, Instant non-refundability, KYC."],
            ["Tracking", "Unique code. No code, no commission."],
            ["Pay him", "15–25% of net evaluation fees after refunds and chargebacks. Start at 20% unless volume is proven."],
            ["Do not pay him", "Trader payouts, company profit, prize pool, untagged traffic."],
            ["Prizes", "Capped Instant accounts you price. Not live capital."],
            ["Term", "90 days. Either party walks. No exclusivity."],
            ["Brand", "Originated by TradeMath / MoniMath. Evaluated by Verodus. Verodus approves every sentence that names Verodus."],
        ],
        [36, 138],
    )
    pdf.body(
        "Kill line (Instant at $49, 20% of net): 20 unique checkouts in 90 days. Twenty is a "
        "meeting that produced a list. Five hundred is a channel. Zero codes is a template."
    )

    pdf.h3("3. Engine / PropTrade is a second document")
    pdf.body(
        "He announced MoniMath PropTrade on 18 Nov 2025 for January 2026. Still no public Instant / "
        "KYC / MT5 / TradeHub / payout stack. If the code produces real checkouts: his brand on the "
        "front; Verodus rules, Platform 5 / TradeHub, Veriff, Rise on the back; Verodus keeps ~70–85% "
        "of challenge GMV; no tickets; tail non-compete so PropTrade does not stand up off Verodus. "
        "Do not give him a logo now so he can tell the market you partnered while he shops rails elsewhere."
    )

    pdf.h3("4. Explicit nos")
    pdf.bullet("Unpaid official long-term partner / exclusive logo")
    pdf.bullet("Bookmap / heatmap / execute-from-the-tape assigned to Verodus")
    pdf.bullet("Required TradeMath education as a gate to Instant")
    pdf.bullet("Sharing or licensing trader data under current Privacy")
    pdf.bullet("Custom championship rules that loosen daily / trail / Best Day")
    pdf.bullet("% of trader payouts or company P&L")
    pdf.bullet("A clarifying call before a Verodus-specific one-pager")

    pdf.h3("5. If he brings Bookmap")
    pdf.body(
        "He had Bookmap’s partner language. He did not have Bookmap’s deal. Public templates: "
        "EdgeProp (coupon BOOKMAP30 + included seat + Rithmic execute from heatmap); 10FOUR "
        "(co-brand; trader still buys Bookmap; analysis beside CQG/TradingView); Trade The Pool "
        "(30-day trial, trader pays after funded); TickTickTrader (bundled free Bookmap, then lost "
        "Tradovate and Project X; homepage Coming soon)."
    )
    pdf.body(
        "If Joe actually has a Bookmap conversation, that is parallel shopping. Verodus does not "
        "join it. You are not a Rithmic/CQG futures shop. Bulk-licensing Bookmap would be a cost "
        "line for CME tape readers, not Instant origination. If he wants Bookmap, he deals with "
        "Bookmap. If he wants challenge volume, he names Instant / 1-Step / Lite and a code. "
        "Do not volunteer “we’ll add Bookmap later.”"
    )

    pdf.h2("Reply Alexander can send")
    pdf.body(
        "Tone: you met him; you are not hostile; you will not sign a blank partnership. "
        "Do not attach economics, a white-label, or a Bookmap comparison on this first send."
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

    pdf.h2("What Verodus should consider (internal)")
    pdf.body("These are for Kim and Alexander, not for Joe.")

    pdf.h3("A. He is a connector, not a stack")
    pdf.body(
        "LIS Group / MyAIQuit is the only name with a real org chart (Joe is Chairman; CTO is "
        "Jacky Qi Zhang). TradeMath is WordPress education plus a Rolex-essay championship. "
        "MoniMath is TAMS plus a PropTrade announcement plus broken SFC copy. World Traders Hub HK "
        "is email-only. Leftover Linear copy on the site, leftover Bookmap copy in the letter. "
        "Useful as Asia origination if a code proves a list. Not someone to whom you hand rails or tape."
    )

    pdf.h3("B. Kim is closer to the real ask than the email")
    pdf.body(
        "Pay the activity Kim heard (directing customers). Do not sign the paper he mailed (free logo). "
        "Force “profits” onto net eval fees. If he means trader payouts or company P&L, the answer is no."
    )

    pdf.h3("C. 10FOUR is the HK Instant analogue — competition, not Joe’s gift")
    pdf.body(
        "Bookmap signed 10FOUR on 11 August. Ten Four Group, HK CR 79713385. Instant / Origin / Daily, "
        "90%, Riseworks, CQG futures. Same category language as Verodus, different market and stack. "
        "If Joe is shopping a prop for the 2027 final, 10FOUR is sitting in his city. A Verodus logo "
        "does not stop him sending futures traders there. Keep no exclusivity in your favor too — "
        "you can add other Asia affiliates."
    )

    pdf.h3("D. Do not buy HK halo")
    pdf.body(
        "OHKF is a real think tank. No public page ties it to Joe. The “1,700-person Saudi government” "
        "event is not on the Algo Challenge Association / Money20/20 sponsor list under TradeMath / Joe / "
        "WTHHK. MoniMath’s SFC story is inconsistent. Repeating any of that next to Verodus is the "
        "liability, not the prize. Verodus already sells in 175+ countries from Dubai FZ. Joe cannot "
        "add a geography. He can add tagged checkouts."
    )

    pdf.h3("E. Fail-fee economics are the constraint")
    pdf.body(
        "Do not loosen Best Day, daily, trail, or Instant non-refundability for the championship. "
        "Do not make TradeMath education a gate — that kills the $49 Instant impulse and lets him "
        "capture the course fee. Prize accounts are a capped COGS line, not open-ended 2-Step Pro."
    )

    pdf.h3("F. Clone risk sits on the engine, not on the code")
    pdf.body(
        "A unique code does not teach him KYC, payouts, and risk. A white-label without a tail "
        "non-compete does. Sequence exists to stop PropTrade standing up off Verodus after he has "
        "seen the dashboard. Data sharing is the faster clone: labeled tickets train TAMS."
    )

    pdf.h3("G. Bookmap is a cost, not origination")
    pdf.body(
        "Verodus buyers are not default CME heatmap users. EdgeProp pays Bookmap seats because its "
        "traders execute futures from the tape. TickTickTrader shows bundled seats do not survive a "
        "lost feed. Platform 5 cannot bolt onto Rithmic. Do not let BD curiosity become a Bookmap invoice."
    )

    pdf.h3("H. Contracting and copy control")
    pdf.body(
        "Four names, one operator. Do not sign World Traders Hub HK until a registry number exists. "
        "Sign the entity that will receive commission, with Joe as commercial lead. Every public "
        "sentence that names Verodus is approved in writing. He does not get to paste you into the "
        "next template the way he pasted you onto Bookmap."
    )

    pdf.h3("I. Operational load of a yes")
    pdf.body(
        "A 90-day pilot still needs: unique code in checkout, refund/chargeback netting, a prize-account "
        "cap, a copy-approval mailbox, and someone to kill the code at day 90. That is cheap. A "
        "white-label is not. Do not staff PropTrade until 20+ tagged Instant checkouts (or equivalent "
        "1-Step / Lite net) actually happen."
    )

    pdf.h3("J. How to answer Kim")
    pdf.callout(
        "Joe asked in person for a cut of referred customers and for the stack behind a competition "
        "he cannot run. The email then asked for a free logo and still thinks we are Bookmap. We take "
        "the referral if it is a unique code and a share of net challenge fees, rules unchanged. We do "
        "not share trading data. We do not give him the engine as his product. Bookmap’s real pairs "
        "(10FOUR, EdgeProp) keep the heatmap and the eval shop separate — we will too. If he wants "
        "PropTrade, it runs on our rails after a 90-day checkout floor."
    )

    pdf.h2("Sequence — do not skip steps")
    pdf.bullet("This week: Alexander sends the product-correction reply. No term sheet. No call until the one-pager arrives.")
    pdf.bullet("If the one-pager names SKUs and a code: 90-day affiliate only. 20% of net. Kill at ~20 Instant checkouts unless mix is better.")
    pdf.bullet("If the code works: second document — PropTrade white-label, Verodus keeps the stack, no data.")
    pdf.bullet("Never in this pass: data license, unpaid exclusivity, Bookmap integration, OHKF/SFC/Saudi co-brand, required academy, loosened rules.")

    pdf.h2("Walk-away")
    pdf.bullet("Next email is still a template")
    pdf.bullet("Free official-partner lock")
    pdf.bullet("Needs Verodus to validate 25%/40% or OHKF")
    pdf.bullet("Asks for tickets “to run the championship”")
    pdf.bullet("Will not name Instant vs 1-Step vs Lite")

    pdf.ln(2)
    pdf.set_font("Inter", "I", 8.0)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        4.4,
        "Companion: docs/joe-wong-revised-suggestions.md, docs/kim-karma-lounge-read.md, "
        "docs/bookmap-prop-firm-partners.md, docs/joe-wong-complete-briefing.md. "
        "Does not change website copy. Privacy bans stay. Not an audit and not legal advice.",
    )

    for path in (OUT, REPO_OUT, ROOT_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        print(f"Wrote {path} pages={pdf.pages_count} bytes={path.stat().st_size}")


if __name__ == "__main__":
    build()
