# Browser verification

Run only in a test environment where local browser execution is permitted. These are development dependencies, not app dependencies. No server or publication is needed.

1. Create a virtual environment: `python -m venv .venv`
2. Activate it using your operating system's standard command.
3. Install test dependencies: `python -m pip install -r qa/requirements.txt`
4. Install the official Playwright Chromium build: `python -m playwright install chromium`
5. Run: `python qa/test.py`

Alternatively, set CHROMIUM_PATH to an existing official Chromium executable before step 5. Linux browser dependencies may also be needed; follow the official Playwright setup documentation for that environment. Do not circumvent permission denials.

The browser runs the actual local HTML with networking set offline. The suite checks real decoding and alpha counts, duplicate hashes, rejected corrupt/oversized/APNG files, CSV download escaping, PNG contact-sheet download dimensions, batch limits, clear, cancellation/reselection and a mobile-width layout. It records page errors and network requests. It writes qa/browser-manifest.json only if every assertion passes, plus exported samples and real screenshots. Failure exits nonzero. The recorded run on 2026-10-23 passed all 19 browser checks in Chromium 151.0.7922.34 on Linux. See qa/browser-manifest.json and https://github.com/willailora/png-pack-check/actions/runs/39911264499. Future runs must complete before claiming a new pass. Node's qa/manifest.json remains separate to avoid overwriting the actual non-browser evidence.

Manual checks after the suite:
- Open index.html directly, not just served over HTTP. Pick and drop real PNGs; verify visual previews against originals.
- Use Tab/Shift+Tab to reach the file chooser and buttons; press Enter/Space as appropriate. Check focus visibility and screen-reader labels/status announcements.
- Verify the contact sheet visually: filenames, numbering, checkerboard, long labels and image placement; compare transparency counts for known fixtures.
- Import CSV as text into your spreadsheet application. Test names starting =, +, -, @, whitespace and tabs, and names containing quotes, commas and newlines. Confirm no formula execution.
- Repeatedly select the same batch, cancel during scan/export, clear, and select again. Check downloads and responsive controls.
- Test the maximum allowed image and a 100-file batch on representative low-memory hardware. Browser decode/encode cannot be interrupted mid-operation.
- Check Firefox/Safari separately before claiming support. Test real mobile hardware before claiming mobile support.
- Verify normal use makes no network requests. The optional tip link should be the sole intentional external navigation, opened only by clicking it.

Record exact browser/version/platform, date, passed/failed checks and unresolved limitations. Do not convert mock-based or parser-only checks into a browser-tested claim.

## GitHub Actions

`.github/workflows/qa.yml` runs only on push or manual dispatch, on the standard `ubuntu-latest` runner with a 10-minute job timeout. It requests contents-read permission only and does not persist checkout credentials. It uses no secrets, artifact uploads, Actions cache, paid/larger runners or automatic result commits. A repository guard restricts execution to `willailora/png-pack-check`. It logs synthetic screenshots (maximum 512 KiB each) as base64 between explicit BEGIN/END markers; these are QA fixtures, never user files. A missing browser manifest is not a pass. Inspect successful checks and their scope before making release-support claims.

Development dependencies are pinned to versions verified on the official registry: https://pypi.org/project/pillow/12.3.0/ and https://pypi.org/project/playwright/1.62.0/.
