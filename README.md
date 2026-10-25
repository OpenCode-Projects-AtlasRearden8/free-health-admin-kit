# Free Health Admin Kit

Warm, printable paperwork helpers for taming appointments and insurance
calls — the kind of life-admin chaos that sneaks up on everybody. Six
print-ready sheets, one build script, zero accounts, and nothing leaves your
home: the kit runs on your own computer and produces PDFs you print and fill
in by hand.

**This whole kit is household organizing help. It is never medical advice.**
If a health question comes up mid-form, write it on a card and ask your
care team at the next visit.

## What's inside

| Sheet | What it's for |
|---|---|
| `appointment-prep` | A one-page checklist for the days before any appointment: who, when, what to pack, what to call about. |
| `question-list-card` | Cut-in-half cards that live in your bag so questions get written down when they show up, not when they disappear. |
| `insurance-call-script` | Exact words and note-keeping boxes for calling an insurance company, so you never improvise over hold music. |
| `medication-wallet-card` | A blank, fold-and-cut wallet card for a pocket medication list (option of one card or a whole sheet of cards, your choice). |
| `renewal-deadlines` | A single tracker table for everything that expires quietly: insurance year, prior authorizations, IDs. |
| `annual-update-reminder` | A once-a-year sweep: minutes of refreshing all the sheets above and filing the old pile. |

Every sheet is intentionally blank-by-design. You (or the person you're
helping) write the real details in pen. Nothing here stores, sends, or
remembers anything.

## How to use it

You need Google Chrome installed (and nothing else — that's the whole
dependency list).

### Build all six PDFs

```bash
./build.sh
```

PDFs land in `build/`, ready to print on US Letter paper, "Actual size" scaling.

### Build just one sheet

```bash
./build.sh appointment-prep
```

### Prefer to edit first?

All sheets are plain HTML/CSS in `sheets/`. Change the wording, add rows,
translate a copy, whatever helps — then rerun `./build.sh`. The shared
look lives in `sheets/style.css`.

### Tip: place cards

The wallet card and question card pages include their own cutting and folding
guides right on the page. Solid lines cut, dashed lines fold.

## Tests

The test suite runs the real build and then checks every PDF: valid file,
right page size, the expected content, the friendly footer, and a privacy
sweep confirming no trackables or personal data ever got baked in.

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

Requires `pypdf` (`pip install pypdf`) alongside Chrome.

## Privacy promise

- No signups, no accounts, no telemetry, no network calls of any kind.
- No secrets or API keys in the repo — the sources are HTML, CSS, and one bash script.
- Your filled-in cards are yours alone; the kit literally cannot phone home (its code makes zero `fetch` or `<script>` tags, and the tests keep it that way).

## The story you signed up for

This kit follows the motto that got it made: plain English, step by step,
never condescending. If a blank form has ever made you feel like you were the
first person in history who didn't know what "member ID" meant, welcome —
everyone piles this paperwork, the piles are normal, and a good printed sheet
beats a web portal any day.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.

Part of Asdale Dynamics, LLC's line of beginner-friendly AI books, guides, and
practical local-first tools (the "life-admin helpers" corner). See
dylanasdale.github.io for books and quiet, kind explanations of things like AI agents.
