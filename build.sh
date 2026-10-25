#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Free Health Admin Kit - build script
# Renders every sheet in sheets/ to a PDF in build/ using headless Chrome.
# Usage: ./build.sh            (build all)
#        ./build.sh <name>     (build one sheet, e.g. ./build.sh appointment-prep)
# ---------------------------------------------------------------------------
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/sheets"
OUT="$ROOT/build"
CHROME="${CHROME:-google-chrome}"

mkdir -p "$OUT"

build_sheet() {
  local file="$1"
  local name
  name="$(basename "$file" .html)"
  echo "  building $name.pdf"
  "$CHROME" --headless=new --disable-gpu --no-sandbox --no-pdf-header-footer \
    --print-to-pdf="$OUT/$name.pdf" \
    --virtual-time-budget=10000 \
    "$SRC/$(basename "$file")" 2>/dev/null
  [[ -s "$OUT/$name.pdf" ]] || { echo "error: $name.pdf was not produced" >&2; return 1; }
}

if [[ $# -gt 0 ]]; then
  if [[ ! -f "$SRC/$1.html" ]]; then
    echo "error: no such sheet: $1 (sheets live in $SRC)" >&2
    exit 1
  fi
  build_sheet "$1.html"
else
  echo "Building Free Health Admin Kit -> $OUT/"
  for f in "$SRC"/*.html; do
    build_sheet "$f"
  done
  echo "Done."
fi
