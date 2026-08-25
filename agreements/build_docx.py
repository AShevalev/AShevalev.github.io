"""Build signed Word agreements from the markdown sources."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
SIG_DIR = ROOT / "signatures"

SOURCES = [
    ROOT / "2026-04-28_VerodusOperationalServicesAgreement.md",
    ROOT / "2026-05-31_SoftwareLicenseAndDataLicensingAgreement.md",
]

SIG_SPECS = {
    "chun_chan": (SIG_DIR / "chun_chan.png", Inches(1.3), Inches(0.24)),
    "kim_chen": (SIG_DIR / "kim_chen.png", Inches(1.05), Inches(0.61)),
}


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


def set_run_font(run, *, bold: bool = False, size: float = 12) -> None:
    run.bold = bold
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor(0, 0, 0)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:cs"), "Times New Roman")
    rFonts.set(qn("w:eastAsia"), "Times New Roman")
    sz = rPr.find(qn("w:sz"))
    if sz is None:
        sz = OxmlElement("w:sz")
        rPr.append(sz)
    sz.set(qn("w:val"), str(int(size * 2)))
    szCs = rPr.find(qn("w:szCs"))
    if szCs is None:
        szCs = OxmlElement("w:szCs")
        rPr.append(szCs)
    szCs.set(qn("w:val"), str(int(size * 2)))


def add_field(paragraph, instr: str, placeholder: str = "1") -> None:
    run = paragraph.add_run()
    set_run_font(run)
    r = run._r
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    inst = OxmlElement("w:instrText")
    inst.set(qn("xml:space"), "preserve")
    inst.text = f" {instr} "
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    r.append(begin)
    r.append(inst)
    r.append(sep)
    r.append(text)
    r.append(end)


def configure_paragraph(paragraph, *, align: str = "left", space_after: float = 10, indent: bool = False) -> None:
    if align == "center":
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = paragraph.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.line_spacing = 1.0
    pf.left_indent = Inches(0.5) if indent else Inches(0)


def add_mixed_runs(paragraph, text: str, *, bold_all: bool = False, size: float = 12) -> None:
    remaining = text
    while remaining:
        if remaining.startswith("**"):
            end = remaining.find("**", 2)
            if end != -1:
                run = paragraph.add_run(remaining[2:end])
                set_run_font(run, bold=True, size=size)
                remaining = remaining[end + 2 :]
                continue
        nxt = remaining.find("**")
        chunk = remaining if nxt == -1 else remaining[:nxt]
        if chunk:
            run = paragraph.add_run(chunk)
            set_run_font(run, bold=bold_all, size=size)
        if nxt == -1:
            break
        remaining = remaining[nxt:]


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


def add_page_numbers(doc: Document) -> None:
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    for child in list(p._p):
        if child.tag != qn("w:pPr"):
            p._p.remove(child)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    lead = p.add_run("-- ")
    set_run_font(lead)
    add_field(p, "PAGE")
    mid = p.add_run(" of ")
    set_run_font(mid)
    add_field(p, "NUMPAGES")
    tail = p.add_run(" --")
    set_run_font(tail)


def set_narrowish_margins(doc: Document, left_right: float) -> None:
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(left_right)
    section.right_margin = Inches(left_right)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(0.9)


def add_signature(doc: Document, key: str) -> None:
    path, width, height = SIG_SPECS[key]
    p = doc.add_paragraph()
    configure_paragraph(p, space_after=2)
    run = p.add_run()
    run.add_picture(str(path), width=width, height=height)


def build_docx(md_path: Path) -> Path:
    markdown = md_path.read_text(encoding="utf-8")
    title_size = 14 if "SOFTWARE" in markdown.splitlines()[0].upper() else 12
    margin = 1.25 if "SOFTWARE" in markdown.splitlines()[0].upper() else 1.0
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    set_narrowish_margins(doc, margin)
    add_page_numbers(doc)

    for kind, text in parse_blocks(markdown):
        if kind == "h1":
            p = doc.add_paragraph()
            configure_paragraph(p, align="center", space_after=12)
            add_mixed_runs(p, text, bold_all=True, size=title_size)
            continue
        if kind == "h2":
            p = doc.add_paragraph()
            configure_paragraph(p, space_after=10)
            add_mixed_runs(p, text, bold_all=True)
            continue
        if kind == "sig":
            add_signature(doc, text)
            continue
        p = doc.add_paragraph()
        align = "center" if is_centered(text) else "left"
        configure_paragraph(p, align=align, indent=is_indented(text) and align == "left")
        add_mixed_runs(p, text)

    dest = md_path.with_suffix(".docx")
    doc.save(str(dest))
    return dest


def main() -> None:
    for src in SOURCES:
        dest = build_docx(src)
        print(f"wrote {dest}")


if __name__ == "__main__":
    main()
