"""Print only this project's synthetic test evidence; no uploads or persistence."""
from pathlib import Path
import base64
BASE = Path(__file__).resolve().parent.parent
for label, relative in [('NODE_MANIFEST', 'qa/manifest.json'), ('BROWSER_MANIFEST', 'qa/browser-manifest.json')]:
    path = BASE / relative
    print('BEGIN_PNG_QA_' + label, flush=True)
    print(path.read_text() if path.is_file() else 'NOT PRODUCED: this stage did not complete successfully.', flush=True)
    print('END_PNG_QA_' + label, flush=True)
for label, relative in [('DESKTOP', 'screenshot.png'), ('MOBILE', 'qa/mobile.png'), ('CONTACT_SHEET', 'qa/sample-contact-sheet.png')]:
    path = BASE / relative
    print('BEGIN_PNG_QA_' + label + '_PNG_BASE64', flush=True)
    if path.is_file() and path.stat().st_size > 512 * 1024:
        print('OMITTED: synthetic screenshot exceeds the 512 KiB log-evidence cap.', flush=True)
    elif path.is_file():
        value = base64.b64encode(path.read_bytes()).decode('ascii')
        for start in range(0, len(value), 4000):
            print(value[start:start + 4000], flush=True)
    else:
        print('NOT PRODUCED', flush=True)
    print('END_PNG_QA_' + label + '_PNG_BASE64', flush=True)
