# STATUS

**Free Health Admin Kit — built 2026-10-25**
Printable paperwork helpers for appointments, insurance calls, and
medication lists. Patient self-care and household organizing only;
**never medical advice**. Local-first: no signups, no accounts, no
network calls, nothing leaves your home.

## What was built

Six print-ready US-Letter sheets (HTML/CSS sources + one build script):

| Sheet (`sheets/*.html`) | PDF (`build/*.pdf`) | Purpose |
|---|---|---|
| appointment-prep | appointment-prep.pdf | 1-page pre-appointment checklist: who/when/where, call-ahead items, bag-packing, night-before, notes |
| question-list-card | question-list-card.pdf | 2 cut-in-half cards to log questions as they pop up, top-priority stars |
| insurance-call-script | insurance-call-script.pdf | Fill-in script, handy phrases, call log table, end-of-call checklist |
| medication-wallet-card | medication-wallet-card.pdf | 6 blank fold-and-cut wallet cards (front = ID/allergies, inside = 6 med lines); blank by design, test-enforced |
| renewal-deadlines | renewal-deadlines.pdf | Ground rules for insurance/prescription renewal timing + 10-row tracker table |
| annual-update-reminder | annual-update-reminder.pdf | Pick-your-month circled date + 11-item once-a-year sweep and note lines |

Supporting files: shared print stylesheet `sheets/style.css`, one build
script `build.sh` (headless Chrome, no Node/no Python deps), MIT
`LICENSE` (Copyright (c) 2026 Asdale Dynamics, LLC), warm README with
usage guide and Asdale Dynamics, LLC credit, and `tests/test_kit.py`
(15 tests).

## How to run it

```bash
./build.sh                    # build all 6 PDFs into build/
./build.sh <sheet-name>       # build one sheet
python3 -m unittest discover -s tests -p "test_*.py" -v   # run tests
```

Requirements: Google Chrome (for rendering) and `pypdf` (test suite
only, `pip install pypdf`). Nothing else.

## Verification results

- `./build.sh`: exit 0; all 6 PDFs written to `build/`.
- Test suite: **15/15 pass** (runs the real build first):
  - every sheet produces a valid PDF (header/EOF, page size 612x792pt, 1–3 pages)
  - expected content phrases extracted from each PDF via pypdf
  - every PDF carries the kit footer ("Asdale Dynamics, LLC") and friendly advice disclaimer
  - privacy sweep: no `http(s)://`, `<script>`, trackers, or forms in sources; no
    personal-data-looking strings (phone/SSN/email patterns) in sources or PDFs;
    wallet card verified blank (no "example"/"sample" text)
  - repo hygiene: MIT LICENSE with exact copyright line, README credit +
    `build.sh` mention, executable build script, all HTML use shared CSS,
    no secret-like strings
- Visual check: each PDF rendered to PNG and inspected — layout fits pages
  cleanly (5 of 6 sheets are exactly 1 page; wallet card is 2 pages: 4 cards
  + guide on page 1, 2 cards on page 2).

## Known gaps

- Needs Google Chrome installed; falls back nowhere (could add WeasyPrint
  as a fallback renderer — it's installed on this machine but untested here).
- Wallet card sheet is 2 pages (guide + 4 cards on p1, 2 cards on p2);
  squeezing 6 onto one page would lose the guide section.
- Formats are US Letter only; an A4 variant would need a CSS tweak.
- Tests depend on pypdf's text extraction (layout-based phrasing could
  need updating if Chrome's PDF engine changes output order).
- No dark/cut-mark-free variant; print as "Actual size" for best results.
