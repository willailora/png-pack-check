"""Local-only regression checks. Requires Python Pillow + Playwright and Chromium."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, struct, zlib, csv, io
BASE=Path(__file__).resolve().parent.parent
FIX=BASE/'qa'/'fixtures'; FIX.mkdir(exist_ok=True)
def png(name,mode,color):
 im=Image.new(mode,(160,120),color);im.save(FIX/name)
png('01-opaque.png','RGB',(56,137,126))
png('02-transparent.png','RGBA',(0,0,0,0))
im=Image.new('RGBA',(160,120),(0,0,0,0));d=ImageDraw.Draw(im);d.ellipse((20,10,140,110),fill=(242,174,94,128));im.save(FIX/'03-partial.png')
(FIX/'04-exact-copy.png').write_bytes((FIX/'01-opaque.png').read_bytes())
(FIX/'=SUM(1,2).png').write_bytes((FIX/'03-partial.png').read_bytes())
(FIX/'bad.png').write_bytes(b'not an image')
(FIX/'wrong.txt').write_bytes((FIX/'01-opaque.png').read_bytes())
a=bytearray((FIX/'01-opaque.png').read_bytes());a[-5]^=1;(FIX/'checksum.png').write_bytes(a)
def chunk(t,p):return struct.pack('>I',len(p))+t+p+struct.pack('>I',zlib.crc32(t+p))
(FIX/'huge.png').write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',9000,9000,8,2,0,0,0))+chunk(b'IDAT',b'')+chunk(b'IEND',b''))
(FIX/'oversize.png').write_bytes(b'0'*(16*1024**2+1))
pal=Image.new('P',(20,20),0);pal.putpalette([255,0,0]*256);pal.info['transparency']=0;pal.save(FIX/'palette.png')
apng=Image.new('RGBA',(20,20),(255,0,0,255));apng.save(FIX/'animated.png',save_all=True,append_images=[Image.new('RGBA',(20,20),(0,255,0,255))],duration=100,loop=0)

Image.new('RGB',(2000,2000),(30,150,120)).save(FIX/'cancellation-large.png')
