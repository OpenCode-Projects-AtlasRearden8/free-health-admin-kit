"""Tests for the Free Health Admin Kit.

Runs the real build script, then verifies that every sheet produces a valid,
rendered PDF and that nothing with real personal data or plain copy mistakes
slips through. Run with:

    python3 -m unittest discover -s tests -p "test_*.py" -v

(From the project root.)
"""

import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    print("error: pypdf is required for the test suite: pip install pypdf", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sheets"
BUILD = ROOT / "build"

SHEETS = {
    "annual-update-reminder": ["annual paperwork day", "once-a-year sweep"],
    "appointment-prep": ["appointment prep sheet", "night before"],
    "insurance-call-script": ["before you dial", "handy phrases"],
    "medication-wallet-card": ["medication list wallet card", "dashed"],
    "question-list-card": ["question list card", "plain language"],
    "renewal-deadlines": ["renewal deadlines tracker", "anti-surprise"],
}

DISCLAIMER = "Asdale Dynamics, LLC"


def build():
    """Run build.sh exactly as a real user would."""
    proc = subprocess.run(
        ["bash", str(ROOT / "build.sh")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=300,
    )
    return proc


def pdf_text(name):
    reader = PdfReader(BUILD / f"{name}.pdf")
    text = " ".join(page.extract_text() or "" for page in reader.pages)
    return re.sub(r"\s+", " ", text).lower()


class TestBuild(unittest.TestCase):
    """The one build script must render a PDF for every sheet."""

    def test_build_script_runs_clean(self):
        proc = build()
        self.assertEqual(
            proc.returncode,
            0,
            f"build.sh failed:\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
        )
        self.assertIn("Done.", proc.stdout)

    def test_every_sheet_has_a_pdf(self):
        build()
        for name in SHEETS:
            with self.subTest(sheet=name):
                pdf = BUILD / f"{name}.pdf"
                self.assertTrue(pdf.exists(), f"{name}.pdf missing from build/")
                self.assertGreater(pdf.stat().st_size, 10_000, f"{name}.pdf looks empty")

    def test_build_single_sheet(self):
        proc = subprocess.run(
            ["bash", str(ROOT / "build.sh"), "annual-update-reminder"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_build_rejects_unknown_sheet(self):
        proc = subprocess.run(
            ["bash", str(ROOT / "build.sh"), "not-a-real-sheet"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertNotEqual(proc.returncode, 0)


class TestPdfOutput(unittest.TestCase):
    """Every PDF must be a real, printable US-Letter document."""

    @classmethod
    def setUpClass(cls):
        build()

    def test_each_pdf_is_valid_letter_sized(self):
        for name in SHEETS:
            with self.subTest(sheet=name):
                pdf = BUILD / f"{name}.pdf"
                data = pdf.read_bytes()
                self.assertTrue(data.startswith(b"%PDF-"), f"{name}.pdf: no PDF header")
                self.assertIn(b"%%EOF", data, f"{name}.pdf: missing EOF marker")
                reader = PdfReader(pdf)
                self.assertGreaterEqual(len(reader.pages), 1)
                self.assertLessEqual(len(reader.pages), 3, f"{name}.pdf: unexpectedly long")
                box = reader.pages[0].mediabox
                self.assertAlmostEqual(float(box.width), 612.0, delta=2)
                self.assertAlmostEqual(float(box.height), 792.0, delta=2)

    def test_each_pdf_contains_expected_text(self):
        for name, phrases in SHEETS.items():
            text = pdf_text(name)
            for phrase in phrases:
                with self.subTest(sheet=name, phrase=phrase):
                    self.assertIn(phrase, text)

    def test_each_pdf_carries_the_kit_footer(self):
        for name in SHEETS:
            with self.subTest(sheet=name):
                text = pdf_text(name)
                self.assertIn(DISCLAIMER.lower(), text, f"{name}: missing kit footer")
                self.assertIn("not medical", text, f"{name}: missing friendly disclaimer")


class TestPrivacy(unittest.TestCase):
    """Nothing leaves your home: no accounts, beacons, or personal data."""

    @classmethod
    def setUpClass(cls):
        build()

    def test_no_network_calls_or_trackers_in_html(self):
        for html in SRC.glob("*.html"):
            content = html.read_text().lower()
            for bad in ["http://", "https://", "//cdn", "analytics", "tracking",
                        "<script", "<iframe", "fetch(", "xmlhttprequest", "<form"]:
                with self.subTest(file=html.name, pattern=bad):
                    self.assertNotIn(bad, content)

    def test_no_real_personal_data_in_sources(self):
        # The wallet card is blank by design; nobody's name, number, or
        # address should ever be baked into the kit's sources or PDFs.
        pattern = re.compile(
            r"\b\d{3}[-.]\s?\d{3}[-.]\s?\d{4}\b"   # phone numbers
            r"|\b\d{3}-\d{2}-\d{4}\b"               # SSN-style
            r"|[\w.+-]+@[\w-]+\.[\w.]+"             # email addresses
        )
        for text in (f.read_text() for f in SRC.glob("*")):
            with self.subTest():
                self.assertIsNone(pattern.search(text), "real-looking personal data in a source file")
        for name in SHEETS:
            with self.subTest(sheet=name):
                self.assertIsNone(
                    pattern.search(pdf_text(name)),
                    f"{name}.pdf: real-looking personal data baked in",
                )

    def test_wallet_card_stays_blank(self):
        text = pdf_text("medication-wallet-card")
        self.assertNotIn("example", text)
        self.assertNotIn("sample", text)


class TestRepoHygiene(unittest.TestCase):
    """LICENSE text, README credit, and executable build script."""

    def test_license_is_mit_with_exact_copyright(self):
        license_text = (ROOT / "LICENSE").read_text()
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", license_text)

    def test_readme_exists_and_credits_llc(self):
        readme = (ROOT / "README.md").read_text()
        self.assertIn("Asdale Dynamics, LLC", readme)
        self.assertIn("build.sh", readme)
        self.assertIn("medical advice", readme.lower())

    def test_build_script_is_executable(self):
        mode = (ROOT / "build.sh").stat().st_mode
        self.assertTrue(mode & 0o111, "build.sh must be executable")

    def test_every_html_uses_shared_stylesheet(self):
        for html in SRC.glob("*.html"):
            with self.subTest(file=html.name):
                content = html.read_text()
                self.assertIn('href="style.css"', content)
                self.assertIn("<title>", content)

    def test_sources_have_no_secrets_or_api_keys(self):
        pattern = re.compile(
            r"(api[_-]?key|secret|token|password)\s*[:=]", re.IGNORECASE
        )
        for f in SRC.glob("*"):
            with self.subTest(file=f.name):
                self.assertIsNone(pattern.search(f.read_text()), f"{f.name}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
