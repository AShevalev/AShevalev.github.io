"""Build signed Word agreements from the original .docx files.

Signatures, dates, fonts, and layout stay with the originals. Only KYC-related
body text is updated, and a Times New Roman 12 page-number footer is added.
"""

from __future__ import annotations

import shutil
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parent
ORIG_OSA = Path(
    "/home/ubuntu/.cursor/projects/workspace/uploads/"
    "2026-04-28_VerodusOperationalServicesAgreement_71b0.docx"
)
ORIG_SLA = Path(
    "/home/ubuntu/.cursor/projects/workspace/uploads/"
    "2026-05-31_SoftwareSublicenseAgreement_ecd7.docx"
)
OUT_OSA = ROOT / "2026-04-28_VerodusOperationalServicesAgreement.docx"
OUT_SLA = ROOT / "2026-05-31_SoftwareSublicenseAgreement.docx"


def has_drawing(para: Paragraph) -> bool:
    return bool(para._p.xpath('.//*[local-name()="drawing"]'))


def set_run_font(run, *, bold: bool | None = None, size: float = 12) -> None:
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:cs"), "Times New Roman")
    sz = rPr.find(qn("w:sz"))
    if sz is None:
        sz = OxmlElement("w:sz")
        rPr.append(sz)
    sz.set(qn("w:val"), str(int(size * 2)))


def replace_text(para: Paragraph, text: str, *, bold: bool | None = None) -> None:
    if has_drawing(para):
        raise RuntimeError(f"refusing to rewrite a signed paragraph: {para.text!r}")
    p = para._p
    for child in list(p):
        if child.tag != qn("w:pPr"):
            p.remove(child)
    run = para.add_run(text)
    set_run_font(run, bold=bold)


def insert_after(para: Paragraph, text: str, *, bold: bool | None = None) -> Paragraph:
    new_p = deepcopy(para._p)
    for child in list(new_p):
        if child.tag != qn("w:pPr"):
            new_p.remove(child)
    para._p.addnext(new_p)
    new_para = Paragraph(new_p, para._parent)
    run = new_para.add_run(text)
    set_run_font(run, bold=bold)
    return new_para


def delete_para(para: Paragraph) -> None:
    if has_drawing(para):
        raise RuntimeError("refusing to delete a signed paragraph")
    el = para._p
    el.getparent().remove(el)


def find_para(doc: Document, predicate) -> Paragraph:
    matches = [p for p in doc.paragraphs if predicate(p.text)]
    if len(matches) != 1:
        sample = [p.text[:80] for p in matches]
        raise LookupError(f"expected 1 match, got {len(matches)}: {sample}")
    return matches[0]


def add_field(paragraph: Paragraph, instr: str, placeholder: str = "1") -> None:
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


def build_osa(src: Path, dest: Path) -> None:
    shutil.copy2(src, dest)
    doc = Document(str(dest))

    replace_text(
        find_para(doc, lambda t: t.startswith("C. LLC-FZ intends to engage Capital")),
        "C. LLC-FZ performs, in its own name and for its own account, all identity verification and know-your-customer checks of users of the Domain. Capital does not provide KYC services to LLC-FZ.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith('1.2 "Services"')),
        '1.2 "KYC" means identity verification, know-your-customer, anti-money-laundering, and counter-terrorist-financing onboarding checks of Domain users.',
    )
    kyc_def = find_para(doc, lambda t: t.startswith('1.2 "KYC"'))
    insert_after(
        kyc_def,
        '1.3 "Services" means the marketing and traffic-driving services provided by Capital to LLC-FZ as described in Section 2.1.',
    )
    replace_text(
        find_para(doc, lambda t: t.startswith('1.3 "Effective Date"') or t.startswith('1.4 "Effective Date"')),
        '1.4 "Effective Date" means the date first written above.',
    )

    old_a = find_para(doc, lambda t: t.startswith("(a) Administrative and operational support"))
    replace_text(
        old_a,
        "(a) Marketing and traffic-driving services directed exclusively to the Domain, including the use of LLC-FZ's affiliate software.",
    )
    delete_para(
        find_para(
            doc,
            lambda t: t.startswith("(b) Marketing and traffic-driving services directed exclusively to the Domain"),
        )
    )

    replace_text(
        find_para(doc, lambda t: t.startswith("2.3 Capital shall perform all payment processing")),
        "2.3 Capital shall perform all payment processing on its own rails and platform evaluations on its own behalf and shall have no access to or involvement in the software or merchant accounts of LLC-FZ for LLC-FZ's isolated payment rails.",
    )
    p24 = find_para(doc, lambda t: t.startswith("2.4 LLC-FZ shall independently establish"))
    replace_text(
        p24,
        "2.4 LLC-FZ shall independently establish and operate its own isolated merchant accounts for its payment rails (deposits and same-method payouts only). There shall be no crossover or commingling of funds between Capital's payment rails and LLC-FZ's payment rails. Capital has no operational control over LLC-FZ's merchant accounts.",
    )
    cursor = p24
    for text, bold in [
        ("2.5 KYC by LLC-FZ.", True),
        ("(a) LLC-FZ shall, in its own name and for its own account, perform all KYC of Domain users.", False),
        ("(b) Capital shall not perform KYC for LLC-FZ, shall not collect identity documents or KYC files on LLC-FZ's behalf, and is not LLC-FZ's KYC provider, outsourced compliance function, or KYC processor.", False),
        ("(c) LLC-FZ may give Capital only the minimum user-status information reasonably required for Capital's independent payment-processing and performance-reward activities (for example, verified, unverified, or restricted). LLC-FZ is not required to give Capital underlying KYC documents unless Capital's payment processors or applicable law require it, in which case LLC-FZ shall provide only what is required.", False),
        ("(d) Capital may collect and process payment-instrument, fraud-prevention, sanctions, and settlement data on its own payment rails as required by its processors and applicable law. That activity is Capital's own payment-rail compliance. It is not KYC performed for LLC-FZ.", False),
    ]:
        cursor = insert_after(cursor, text, bold=bold)

    replace_text(
        find_para(doc, lambda t: t.startswith("(c) It will comply with all applicable laws, including anti-money-laundering")),
        "(c) It will comply with all applicable laws that apply to its own activities, including anti-money-laundering and payment-processing regulations.",
    )
    c_rep = find_para(doc, lambda t: t.startswith("(c) It will comply with all applicable laws that apply to its own activities, including anti-money-laundering"))
    r62 = insert_after(c_rep, "6.2 LLC-FZ represents that it, and not Capital, is responsible for KYC of Domain users.")
    insert_after(r62, "6.3 Capital represents that it is responsible for legal and processor obligations arising from merchant accounts held in Capital's name.")

    replace_text(
        find_para(doc, lambda t: t.startswith("7.1 Each party shall maintain the confidentiality")),
        "7.1 Each party shall maintain the confidentiality of the other party's non-public information and use it solely for the purposes of this Agreement. KYC documents and identity-verification files of Domain users are LLC-FZ's confidential information. Capital shall not use or retain them except as Section 2.5(c) or applicable law requires. This obligation survives termination.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("8.3 Upon termination, the Domain and Evaluation Rights")),
        "8.3 Upon termination, the Domain and Evaluation Rights license granted herein shall terminate immediately. Capital shall stop using the Domain and the affiliate software, and shall return or securely delete KYC documents (if any) in its possession, except as applicable law requires Capital to retain.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("9.1 Each party shall indemnify the other against claims")),
        "9.1 Each party shall indemnify the other against claims, losses, or damages arising from its own breach or violation of law, including, in LLC-FZ's case, claims arising from LLC-FZ's KYC of Domain users, and in Capital's case, claims arising from Capital's merchant accounts and payment rails.",
    )
    replace_text(
        find_para(doc, lambda t: "British Columbia International Commercial Arbitration Centre" in t and t.startswith("11.2")),
        "11.2 Any disputes arising out of or in connection with this Agreement shall be finally settled by arbitration administered by the Vancouver International Arbitration Centre (VanIAC) in Vancouver, British Columbia, before a single arbitrator, in accordance with the VanIAC International Commercial Arbitration Rules. The language of arbitration shall be English.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("12.1 This Agreement is bilateral")),
        "12.1 This Agreement is bilateral.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("12.2 Capital has no access or rights to the software")),
        "12.2 Capital has no access or rights to the software of LLC-FZ (other than the limited license to use the affiliate software for traffic-driving purposes), no operational involvement in LLC-FZ's isolated merchant accounts, and no KYC role for LLC-FZ.",
    )

    add_page_numbers(doc)
    doc.save(str(dest))


def build_sla(src: Path, dest: Path) -> None:
    shutil.copy2(src, dest)
    doc = Document(str(dest))

    replace_text(
        find_para(doc, lambda t: t.startswith("C. LLC-FZ is the registered owner of the domain name verodus.com.")),
        "C. LLC-FZ is the registered owner of the domain name verodus.com. LLC-FZ performs, in its own name and for its own account, all identity verification and know-your-customer checks of users of that domain.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("D. The parties desire to enter into a bilateral arrangement")),
        "D. The parties desire to enter into a bilateral arrangement whereby 1591011 B.C. LTD. grants LLC-FZ a sublicense to use the Software for data collection and analysis (including LLC-FZ's own KYC and classification activities), and LLC-FZ in return grants 1591011 B.C. LTD. a license to the Aggregated Insights generated through that use.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith('1.1 "Aggregated Insights"')),
        '1.1 "Aggregated Insights" means anonymized, amalgamated data and analytical outputs derived from the application of the Software, excluding any raw client-identifying information, KYC documents, and identity-verification files.',
    )
    data_def = find_para(doc, lambda t: t.startswith('1.2 "Data"'))
    insert_after(data_def, '1.3 "Domain" means the domain name verodus.com.')
    replace_text(
        find_para(doc, lambda t: t.startswith('1.3 "Effective Date"') or t.startswith('1.4 "Effective Date"')),
        '1.4 "Effective Date" means the date first written above.',
    )
    eff = find_para(doc, lambda t: t.startswith('1.4 "Effective Date"'))
    insert_after(
        eff,
        '1.5 "KYC" means identity verification, know-your-customer, anti-money-laundering, and counter-terrorist-financing onboarding checks of Domain users.',
    )
    replace_text(
        find_para(doc, lambda t: t.startswith('1.4 "Software"') or t.startswith('1.6 "Software"')),
        '1.6 "Software" means the pre-existing software, CRM systems, and related technology owned and operated by 1591011 B.C. LTD.',
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("2.1 1591011 B.C. LTD. hereby grants LLC-FZ")),
        "2.1 1591011 B.C. LTD. hereby grants LLC-FZ a non-exclusive, non-transferable, revocable limited sublicense to install, access, and use the Software in connection with LLC-FZ's Meydan-authorized business activities, including data collection, classification, analysis, and LLC-FZ's own KYC of Domain users.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("3.1 LLC-FZ shall collect, classify, analyze")),
        "3.1 LLC-FZ shall collect, classify, analyze, and aggregate Data through the Software, including trading performance metrics across supported instruments. LLC-FZ shall perform all KYC of Domain users itself. LLC-FZ shall not be required to share KYC documents or identity-verification files with 1591011 B.C. LTD.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("3.2 All raw Data")),
        "3.2 All raw Data, client-identifying information, and KYC records derived from or stored in the Software shall be the sole and exclusive property of LLC-FZ.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("3.3 LLC-FZ hereby grants 1591011 B.C. LTD. a perpetual")),
        "3.3 LLC-FZ hereby grants 1591011 B.C. LTD. a perpetual, irrevocable, royalty-free, worldwide, non-exclusive license to use, reproduce, modify, adapt, resell, sublicense to third parties, commercialize and otherwise exploit the Aggregated Insights in any manner whatsoever. That license does not include raw Data, client-identifying information, or KYC records.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("(c) It will comply with all applicable laws, including data protection")),
        "(c) It will comply with all applicable laws that apply to its own activities, including data protection and export-control laws.",
    )
    c_rep = find_para(doc, lambda t: t.startswith("(c) It will comply with all applicable laws that apply to its own activities, including data protection"))
    insert_after(
        c_rep,
        "6.2 LLC-FZ represents that it, and not 1591011 B.C. LTD., is responsible for KYC of Domain users and for privacy and anti-money-laundering laws applicable to that activity. 1591011 B.C. LTD. is not LLC-FZ's KYC provider.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("7.1 Each party shall keep the other party's non-public information")),
        "7.1 Each party shall keep the other party's non-public information strictly confidential and use it only for the purposes of this Agreement. KYC records and client-identifying information are LLC-FZ's confidential information. 1591011 B.C. LTD. shall not use them except as technically required to operate the Software for LLC-FZ, and shall not include them in Aggregated Insights. This obligation survives termination.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("8.3 Upon termination, the sublicense granted under Section 2")),
        "8.3 Upon termination, the sublicense granted under Section 2 ends immediately, but the perpetual license to Aggregated Insights granted under Section 3.3 survives. 1591011 B.C. LTD. shall not retain KYC records or raw client-identifying information after termination except as required by law, or as residual Aggregated Insights already delivered in anonymized form.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("9.1 Each party shall indemnify, defend, and hold harmless")),
        "9.1 Each party shall indemnify, defend, and hold harmless the other party against any claims, losses, or damages arising from its own breach of this Agreement or violation of applicable law, including, in LLC-FZ's case, claims arising from LLC-FZ's KYC of Domain users or LLC-FZ's handling of Data.",
    )
    replace_text(
        find_para(doc, lambda t: "British Columbia International Commercial Arbitration Centre" in t and t.startswith("11.2")),
        "11.2 Any disputes arising out of or in connection with this Agreement shall be finally settled by arbitration administered by the Vancouver International Arbitration Centre (VanIAC) in Vancouver, British Columbia, before a single arbitrator, in accordance with the VanIAC International Commercial Arbitration Rules. The language of arbitration shall be English.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("12.1 This Agreement is bilateral")),
        "12.1 This Agreement is bilateral.",
    )
    replace_text(
        find_para(doc, lambda t: t.startswith("12.2 This Agreement constitutes the entire understanding")),
        "12.2 This Agreement constitutes the entire understanding and supersedes all prior discussions.",
    )

    add_page_numbers(doc)
    doc.save(str(dest))


def main() -> None:
    build_osa(ORIG_OSA, OUT_OSA)
    build_sla(ORIG_SLA, OUT_SLA)
    print(f"wrote {OUT_OSA}")
    print(f"wrote {OUT_SLA}")


if __name__ == "__main__":
    main()
