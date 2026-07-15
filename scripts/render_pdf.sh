#!/usr/bin/env bash
# PaperKraken LEGACY fallback renderer (one-shot Chromium CLI print).
# Prefer scripts/render_pdf.mjs — it deterministically waits for MathJax+Paged.js.
# This CLI path cannot wait for Paged.js: strip the paged.polyfill.js script tag
# and PagedConfig/PagedPolyfill lines from the HTML before using it.
# Usage: render_pdf.sh <report.html> <out.pdf>
# Env: PK_TIME_BUDGET (ms, default 45000) — virtual time budget for MathJax typesetting.
set -euo pipefail

HTML="${1:?usage: render_pdf.sh <report.html> <out.pdf>}"
OUT="${2:?usage: render_pdf.sh <report.html> <out.pdf>}"
BUDGET="${PK_TIME_BUDGET:-45000}"

[ -f "$HTML" ] || { echo "ERROR: HTML not found: $HTML" >&2; exit 1; }

# Locate a Chromium binary: playwright headless shell (newest), playwright chromium, then system.
BIN=""
for glob in \
  "$HOME/.cache/ms-playwright"/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell \
  "$HOME/.cache/ms-playwright"/chromium-*/chrome-linux*/chrome; do
  for c in $glob; do [ -x "$c" ] && BIN="$c"; done
done
if [ -z "$BIN" ]; then
  for c in google-chrome chromium chromium-browser; do
    command -v "$c" >/dev/null 2>&1 && BIN="$(command -v "$c")" && break
  done
fi
[ -n "$BIN" ] || { echo "ERROR: no Chromium found. Run: npx playwright install chromium" >&2; exit 2; }

ABS="$(realpath "$HTML")"
"$BIN" --headless --disable-gpu --no-sandbox --disable-dev-shm-usage \
  --allow-file-access-from-files \
  --run-all-compositor-stages-before-draw \
  --virtual-time-budget="$BUDGET" \
  --no-pdf-header-footer \
  --print-to-pdf="$OUT" \
  "file://$ABS" 2>&1 | grep -v "^\[" || true

[ -s "$OUT" ] || { echo "ERROR: PDF was not produced" >&2; exit 3; }

# Report page count if poppler is available.
if command -v pdfinfo >/dev/null 2>&1; then
  PAGES="$(pdfinfo "$OUT" | awk '/^Pages:/{print $2}')"
  echo "OK: $OUT ($PAGES pages)"
else
  echo "OK: $OUT ($(du -h "$OUT" | cut -f1))"
fi
