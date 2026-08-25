"""Render the revised Verodus agreements to letter-size PDFs."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
)

ROOT = Path(__file__).resolve().parent

SOURCES = [
    ROOT / "2026-04-28_VerodusOperationalServicesAgreement.md",
    ROOT / "2026-05-31_SoftwareLicenseAndDataLicensingAgreement.md",
]


def italicize_quotes(text: str) -> str:
    """Turn straight double-quoted phrases into italics for defined terms."""
    out = []
    i = 0
    while i < len(text):
        if text[i] == '"':
            j = text.find('"', i + 1)
            if j == -1:
                out.append("&quot;")
                i += 1
                continue
            inner = xml_escape(text[i + 1 : j])
            out.append(f'&quot;<i>{inner}</i>&quot;')
            i = j + 1
        else:
            out.append(xml_escape(text[i]))
            i += 1
    return "".join(out)


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline_md(text: str) -> str:
    """Convert a limited markdown subset to ReportLab XML."""
    parts: list[str] = []
    i = 0
    while i < len(text):
        if text.startswith("**", i):
            j = text.find("**", i + 2)
            if j != -1:
                parts.append(f"<b>{italicize_quotes(text[i + 2 : j])}</b>")
                i = j + 2
                continue
        nxt = text.find("**", i)
        chunk = text[i:] if nxt == -1 else text[i:nxt]
        parts.append(italicize_quotes(chunk))
        if nxt == -1:
            break
        i = nxt
    return "".join(parts)


def parse_blocks(markdown: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    buf: list[str] = []

    def flush() -> None:
        nonlocal buf
        if not buf:
            return
        raw = " ".join(line.strip() for line in buf).strip()
        buf = []
        if not raw:
            return
        if raw.startswith("# "):
            blocks.append(("h1", raw[2:].strip()))
        elif raw.startswith("## "):
            blocks.append(("h2", raw[3:].strip()))
        else:
            blocks.append(("p", raw))

    for line in markdown.splitlines():
        if line.strip() == "":
            flush()
        else:
            buf.append(line)
    flush()
    return blocks


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle(
            "AgreementTitle",
            parent=base["Title"],
            fontName="Times-Bold",
            fontSize=13,
            leading=16,
            alignment=TA_CENTER,
            spaceAfter=10,
            textColor="#111111",
        ),
        "h2": ParagraphStyle(
            "AgreementHeading",
            parent=base["Heading2"],
            fontName="Times-Bold",
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=6,
            textColor="#111111",
        ),
        "p": ParagraphStyle(
            "AgreementBody",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=10.5,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
        ),
        "center": ParagraphStyle(
            "AgreementCenter",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=10.5,
            leading=14,
            alignment=TA_CENTER,
            spaceAfter=7,
        ),
        "sig": ParagraphStyle(
            "AgreementSig",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=10.5,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=3,
        ),
        "footer": ParagraphStyle(
            "AgreementFooter",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=9,
            alignment=TA_CENTER,
            textColor="#444444",
        ),
    }


def add_page_number(canvas, doc) -> None:
    canvas.saveState()
    styles = make_styles()
    page = Paragraph(f"— {doc.page} —", styles["footer"])
    w, h = page.wrap(doc.width, 20)
    page.drawOn(canvas, doc.leftMargin, 0.55 * inch)
    canvas.restoreState()


def build_flowables(markdown: str):
    styles = make_styles()
    story = []
    witness: list = []
    in_witness = False

    def flush_witness() -> None:
        nonlocal witness
        if witness:
            story.append(KeepTogether(witness))
            witness = []

    for kind, text in parse_blocks(markdown):
        if kind == "h1":
            story.append(Paragraph(inline_md(text.upper()), styles["h1"]))
            continue
        if kind == "h2":
            if text.strip().upper().startswith("IN WITNESS"):
                in_witness = True
                witness.append(Paragraph(inline_md(text.upper()), styles["h2"]))
            else:
                flush_witness()
                in_witness = False
                story.append(Paragraph(inline_md(text.upper()), styles["h2"]))
            continue
        if in_witness:
            if text.startswith("____"):
                witness.append(Spacer(1, 14))
            witness.append(Paragraph(inline_md(text), styles["sig"]))
            if text.startswith("Date:"):
                witness.append(Spacer(1, 16))
            continue
        if text in {"Between", "And"}:
            story.append(Paragraph(inline_md(text), styles["center"]))
        else:
            story.append(Paragraph(inline_md(text), styles["p"]))
    flush_witness()
    return story


def render_pdf(md_path: Path, pdf_path: Path) -> None:
    markdown = md_path.read_text(encoding="utf-8")
    doc = BaseDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=1.0 * inch,
        rightMargin=1.0 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        title=md_path.stem.replace("_", " "),
        author="Revised draft — 25 August 2026",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="letter", frames=frame, onPage=add_page_number)])
    doc.build(build_flowables(markdown))


def main() -> None:
    for src in SOURCES:
        dest = src.with_suffix(".pdf")
        render_pdf(src, dest)
        print(f"wrote {dest}")


if __name__ == "__main__":
    main()
