# PNG Pack Check v1.0.0

A free, offline single-file tool for checking small PNG asset packs. Download `png-pack-check-1.0.0.zip`, extract it, then open `index.html` in a modern desktop browser. No installation, account, server or API key is required.

- Inspect dimensions and alpha/transparency.
- Identify exact-file SHA-256 duplicates, not visual similarity.
- Export a filename-labeled PNG contact sheet and spreadsheet-safe CSV.
- Process files sequentially, cancel between operations and keep partial results.
- Files stay on your device; originals are not modified.

Free, with no paid tier or feature gates. Optional tips: https://ko-fi.com/ailorawill. Tips do not purchase support, updates or additional features.

Verification: 19 real-browser checks and 23 Node checks passed. Browser scope: Chromium 151.0.7922.34, Linux headless, local files, offline. Evidence: https://github.com/willailora/png-pack-check/actions/runs/39911264499 (tested functional source commit 88d59b7f5ba52684cdcad40c2e5fab287f7ebd72).

Known limits: static PNG only; maximum 100 files, 16 MiB per file, 128 MiB per batch, 8 million pixels per image and 8,192 pixels per edge. Contact-sheet labels may shorten long filenames; CSV keeps full names. Pixel analysis uses browser-decoded 8-bit alpha. Cancellation cannot interrupt a browser operation already in flight. Resource limits are not a guaranteed peak-memory cap.

Firefox, Safari, native Windows use, real mobile and low-memory hardware remain untested. Spreadsheet behavior varies; import filename/text columns as text. No custom support or ongoing updates are promised. MIT licensed; provided AS IS, without warranty to the extent permitted by law, without excluding rights that cannot legally be excluded.
