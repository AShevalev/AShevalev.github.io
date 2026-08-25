"""Render the Verodus agreements in the original Word/Times layout."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
)

ROOT = Path(__file__).resolve().parent
SIG_DIR = ROOT / "signatures"

pdfmetrics.registerFont(TTFont("TNR", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("TNR-Bold", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"))

SOURCES = [
    (ROOT / "2026-04-28_VerodusOperationalServicesAgreement.md", 1.0 * inch),
    (ROOT / "2026-05-31_SoftwareLicenseAndDataLicensingAgreement.md", 1.25 * inch),
]

SIG_SPECS = {
    "chun_chan": (SIG_DIR / "chun_chan.png", 93, 17),
    "kim_chen": (SIG_DIR / "kim_chen.png", 75, 44),
}


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline_md(text: str) -> str:
    parts: list[str] = []
    i = 0
    while i < len(text):
        if text.startswith("**", i):
            j = text.find("**", i + 2)
            if j != -1:
                parts.append(f"<b>{xml_escape(text[i + 2 : j])}</b>")
                i = j + 2
                continue
        nxt = text.find("**", i)
        chunk = text[i:] if nxt == -1 else text[i:nxt]
        parts.append(xml_escape(chunk))
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
        elif raw.startswith("{{signature:"):
            blocks.append(("sig", raw[len("{{signature:") :].rstrip("}").strip()))
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
    body = dict(
        parent=base["Normal"],
        fontName="TNR",
        fontSize=12,
        leading=16,
        spaceAfter=10,
    )
    return {
        "h1": ParagraphStyle(
            "Title14",
            parent=base["Title"],
            fontName="TNR-Bold",
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "h1_12": ParagraphStyle(
            "Title12",
            parent=base["Title"],
            fontName="TNR-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "h2": ParagraphStyle(
            "Heading",
            parent=base["Heading2"],
            fontName="TNR-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=6,
            spaceAfter=10,
        ),
        "p": ParagraphStyle("Body", alignment=TA_LEFT, **body),
        "center": ParagraphStyle("Center", alignment=TA_CENTER, **body),
        "indent": ParagraphStyle("Indent", alignment=TA_LEFT, leftIndent=36, **body),
        "sig": ParagraphStyle("Sig", alignment=TA_LEFT, spaceAfter=4, **{k: v for k, v in body.items() if k != "spaceAfter"}),
    }


def signature_image(key: str) -> Image:
    path, width, height = SIG_SPECS[key]
    image = Image(str(path), width=width, height=height, mask="auto")
    image.hAlign = "LEFT"
    return image


def is_centered(text: str) -> bool:
    stripped = text.strip()
    if stripped in {"Between", "And"}:
        return True
    if stripped.startswith("(") and stripped.endswith(")"):
        return True
    if stripped.startswith("**") and stripped.endswith("**") and stripped.count("**") == 2:
        inner = stripped[2:-2]
        if inner.startswith("Effective Date:"):
            return False
        return True
    return False


def is_indented(text: str) -> bool:
    stripped = text.strip()
    return stripped.startswith(("(a)", "(b)", "(c)", "(d)", "i.", "ii.", "iii."))


def build_flowables(markdown: str, title_size: int = 14):
    styles = make_styles()
    title_style = styles["h1"] if title_size == 14 else styles["h1_12"]
    story = []
    witness: list = []
    in_witness = False

    def dest() -> list:
        return witness if in_witness else story

    def flush_witness() -> None:
        nonlocal witness
        if witness:
            story.append(KeepTogether(witness))
            witness = []

    for kind, text in parse_blocks(markdown):
        if kind == "h1":
            dest().append(Paragraph(inline_md(text), title_style))
            dest().append(Spacer(1, 8))
            continue
        if kind == "h2":
            if text.strip().upper().startswith("IN WITNESS"):
                in_witness = True
                witness.append(Paragraph(inline_md(text), styles["h2"]))
            else:
                flush_witness()
                in_witness = False
                dest().append(Paragraph(inline_md(text), styles["h2"]))
            continue
        if kind == "sig":
            dest().append(Spacer(1, 4))
            dest().append(signature_image(text))
            dest().append(Spacer(1, 2))
            continue
        style = styles["p"]
        if is_centered(text) and not in_witness:
            style = styles["center"]
        elif is_indented(text):
            style = styles["indent"]
        elif in_witness:
            style = styles["sig"]
        dest().append(Paragraph(inline_md(text), style))
    flush_witness()
    return story


class NumberedCanvas(canvas.Canvas):
    """Draw original-style '-- 1 of 6 --' footers after the page count is known."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states: list[dict] = []

    def showPage(self) -> None:
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self) -> None:
        page_count = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.setFont("TNR", 12)
            label = f"-- {self._pageNumber} of {page_count} --"
            self.drawCentredString(letter[0] / 2.0, 0.55 * inch, label)
            super().showPage()
        super().save()


def render_pdf(md_path: Path, pdf_path: Path, margin: float) -> None:
    markdown = md_path.read_text(encoding="utf-8")
    title_size = 14 if "SOFTWARE" in markdown.splitlines()[0].upper() else 12
    doc = BaseDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=1.0 * inch,
        bottomMargin=0.9 * inch,
        title=md_path.stem.replace("_", " "),
        author="",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="letter", frames=frame)])
    doc.build(build_flowables(markdown, title_size=title_size), canvasmaker=NumberedCanvas)


def main() -> None:
    for src, margin in SOURCES:
        dest = src.with_suffix(".pdf")
        render_pdf(src, dest, margin)
        print(f"wrote {dest}")


if __name__ == "__main__":
    main()
