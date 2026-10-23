"""Real browser regression checks. Generates synthetic fixtures. No publication."""
from pathlib import Path
from PIL import Image
import json, csv, io, os, runpy
from playwright.sync_api import sync_playwright
BASE=Path(__file__).resolve().parent.parent
FIX=BASE/'qa'/'fixtures'
runpy.run_path(str(BASE/'qa'/'generate_fixtures.py'))
results=[]
def check(name,ok):
 results.append({'test':name,'passed':bool(ok)});assert ok,name
with sync_playwright() as p:
 browser=p.chromium.launch(**({'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}),headless=True)
 page=browser.new_page(viewport={'width':1280,'height':1000});page.set_default_timeout(60000);page.context.set_offline(True);errors=[];requests=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url))
 page.goto(BASE.as_uri()+'/index.html')
 names=['01-opaque.png','02-transparent.png','03-partial.png','04-exact-copy.png','=SUM(1,2).png','bad.png','wrong.txt','checksum.png','huge.png','oversize.png','palette.png','animated.png']
 page.locator('#file').set_input_files([str(FIX/n) for n in names]);page.wait_for_function("!busy && rows.length === 12")
 r=page.evaluate('rows.map(({thumb,...r})=>r)')
 check('RGB opaque dimensions and alpha',r[0]['ok'] and r[0]['w']==160 and r[0]['h']==120 and r[0]['transparent']==0 and not r[0]['alpha'])
 check('RGBA full transparency',r[1]['transparent']==19200 and r[1]['alpha'])
 check('Partial alpha',r[2]['partial']>0)
 check('Exact SHA256 duplicate',r[3]['duplicate']==1 and r[3]['hash']==r[0]['hash'])
 check('Bad signature, extension, CRC, dimensions, bytes rejected',all(not r[i]['ok'] for i in [5,6,7,8,9]))
 check('Palette tRNS transparency',r[10]['ok'] and r[10]['trns'] and r[10]['transparent']==400)
 check('APNG rejected',not r[11]['ok'] and 'Animated' in r[11]['error'])
 with page.expect_download() as download:page.locator('#csv').click()
 csvpath=BASE/'qa'/'sample-report.csv';download.value.save_as(csvpath)
 parsed=list(csv.reader(io.StringIO(csvpath.read_text(encoding='utf-8-sig'))))
 check('CSV formula filename neutralized',parsed[5][1]=="'=SUM(1,2).png")
 check('CSV edge cases',page.evaluate("csvCell('  @x').startsWith(\"\\\"'\") && csvCell('a\\\"b') === '\\\"a\\\"\\\"b\\\"'") )
 with page.expect_download() as download:page.locator('#sheet').click()
 sheetpath=BASE/'qa'/'sample-contact-sheet.png';download.value.save_as(sheetpath)
 check('Contact sheet PNG export',Image.open(sheetpath).size==(1000,514))
 page.wait_for_function('!busy')
 page.screenshot(path=str(BASE/'screenshot.png'),full_page=True)
 page.evaluate("run(Array.from({length:101},()=>new File(['x'],'x.png')))")
 check('Count guard preserves results',page.evaluate('rows.length===12') and 'Batch rejected' in page.locator('#status').inner_text())
 page.evaluate("run(Array.from({length:9},()=>new File([new Uint8Array(16*1024*1024)],'x.png')))")
 check('Total byte guard', 'Batch rejected' in page.locator('#status').inner_text())
 page.locator('#clear').click();check('Clear releases results',page.evaluate('rows.length===0'))
 page.locator('#file').set_input_files([str(FIX/'cancellation-large.png')]*100);page.locator('#cancel').click();page.wait_for_function('!busy')
 check('Cancellation keeps partial results', 'Cancelled.' in page.locator('#status').inner_text() and page.evaluate('rows.length<100'))
 page.locator('#file').set_input_files(str(FIX/'01-opaque.png'));page.wait_for_function('!busy && rows.length===1')
 check('Reselect after cancellation',page.evaluate('rows[0].ok'))
 page.locator('#file').set_input_files(str(FIX/'cancellation-large.png'));page.wait_for_function('!busy && rows.length===1')
 check('Four-million-pixel decode and scan',page.evaluate('rows[0].ok && rows[0].w===2000 && rows[0].transparent===0'))
 page.set_viewport_size({'width':390,'height':844});check('Mobile width no horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
 page.screenshot(path=str(BASE/'qa'/'mobile.png'),full_page=True)
 check('No JS errors',not errors);check('No network requests',all(u.startswith('file:') or u.startswith('data:') or u.startswith('blob:') for u in requests))
 (BASE/'qa'/'browser-manifest.json').write_text(json.dumps({'browser':'Chromium '+browser.version,'platform':'Linux, headless local file://','date':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'checks':results,'errors':errors,'network_requests':[u for u in requests if u.startswith('http')],'not_tested':['Firefox','Safari','mobile hardware','low-memory hardware','every PNG encoding'],'note':'Limits are conservative guards, not a guaranteed peak-memory cap.'},indent=2))
 browser.close()
print(json.dumps(results,indent=2))
