"""Checks that the revised agreements keep KYC with LLC-FZ and do not price each leg."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
OSA = ROOT / "2026-04-28_VerodusOperationalServicesAgreement.pdf"
SLA = ROOT / "2026-05-31_SoftwareLicenseAndDataLicensingAgreement.pdf"


def pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def assert_contains(haystack: str, needle: str, label: str) -> None:
    if needle.lower() not in haystack.lower():
        raise AssertionError(f"{label}: missing expected text: {needle!r}")


def assert_absent(haystack: str, needle: str, label: str) -> None:
    if needle.lower() in haystack.lower():
        raise AssertionError(f"{label}: unexpectedly contains {needle!r}")


def main() -> int:
    subprocess.check_call([sys.executable, str(ROOT / "generate_pdfs.py")], cwd=ROOT)
    osa = normalize(pdf_text(OSA))
    sla = normalize(pdf_text(SLA))

    # KYC sits with LLC-FZ, not Capital or the software owner.
    assert_contains(osa, "LLC-FZ shall, in its own name and for its own account, perform all KYC", "OSA")
    assert_contains(osa, "Capital shall not perform KYC for LLC-FZ", "OSA")
    assert_contains(osa, "is not LLC-FZ's KYC provider", "OSA")
    assert_absent(osa, "including KYC verification of users for LLC-FZ", "OSA")
    assert_absent(osa, "KYC verification support for LLC-FZ", "OSA")
    assert_contains(sla, "LLC-FZ shall perform all KYC of Domain users itself", "SLA")
    assert_contains(sla, "1591011 B.C. LTD. is not LLC-FZ's KYC provider", "SLA")

    # No per-leg invoices; reciprocal consideration remains.
    for label, text in (("OSA", osa), ("SLA", sla)):
        assert_contains(text, "no invoices", label)
        assert_absent(text, "transfer pricing regulations", label)
        assert_absent(text, "BCICAC", label)
        assert_contains(text, "VanIAC", label)
        assert_absent(text, "Revised:", label)
        assert_absent(text, "August 25, 2026", label)
        assert_absent(text, "Software Sublicense", label)

    # Original 5% royalty wording; no extra gloss.
    assert_contains(
        osa,
        "At LLC-FZ's sole discretion, and upon ninety (90) days written notice to Capital, LLC-FZ shall be entitled to charge Capital a royalty equal to five percent (5%) of gross sales (CAD), calculated and payable in quarterly installments based on the prior quarter's gross sales. The quarterly payment shall be made by Capital to LLC-FZ on or before the fifteenth (15th) day following the end of each applicable quarter period.",
        "OSA",
    )
    assert_absent(osa, "It is not a price for any individual service or right", "OSA")
    assert_absent(sla, "five percent", "SLA")

    # Original signature dating: OSA undated; SLA dated May 31, 2026.
    assert_contains(sla, "Date: May 31, 2026", "SLA")
    assert_absent(osa, "Date: ____________________", "OSA")
    assert_absent(osa, "Date: May", "OSA")

    # Software grant is a licence from the owner, not a sublicence.
    assert_contains(sla, "GRANT OF LICENSE", "SLA")
    assert_contains(sla, "This Agreement is a license from the owner", "SLA")
    assert_absent(sla, "grants LLC-FZ a non-exclusive, non-transferable, revocable limited sublicense", "SLA")

    # Insights are delivered during the term, not only on the last day.
    assert_contains(sla, "with each status report under Section 4.2", "SLA")

    print("all agreement checks passed")
    print(f"OSA pages: {len(PdfReader(str(OSA)).pages)}")
    print(f"SLA pages: {len(PdfReader(str(SLA)).pages)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
