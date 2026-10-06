from __future__ import annotations
import hashlib, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from .config import settings

ROOT=Path(__file__).resolve().parent.parent
PANEL_DIR=ROOT/'static'/'panels'

def safe_name(prompt: str, n: int)->str:
    slug=re.sub(r"[^a-zA-Z0-9]+","-",prompt.lower()).strip("-")[:50] or "panel"
    digest=hashlib.sha1(prompt.encode()).hexdigest()[:10]
    return f"panel-{n}-{slug}-{digest}.png"

def _font(size):
    for p in ["C:/Windows/Fonts/arialbd.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def generate_image(prompt: str, panel_number: int) -> str:
    PANEL_DIR.mkdir(parents=True, exist_ok=True)
    name=safe_name(prompt,panel_number); path=PANEL_DIR/name
    if not path.exists():
        w,h=1200,760
        img=Image.new("RGB",(w,h),(239,228,205)); d=ImageDraw.Draw(img)
        # comic-style fallback illustration, deliberately local/no external dependency
        d.rectangle((25,25,w-25,h-25),outline=(25,25,25),width=12)
        d.ellipse((w*0.36, h*0.15, w*0.64, h*0.55),fill=(245,190,120),outline=(20,20,20),width=8)
        d.arc((w*0.43,h*0.31,w*0.57,h*0.48),0,180,fill=(20,20,20),width=6)
        d.ellipse((w*0.43,h*0.28,w*0.47,h*0.32),fill=(20,20,20)); d.ellipse((w*0.53,h*0.28,w*0.57,h*0.32),fill=(20,20,20))
        d.polygon([(120,h-100),(250,h-350),(380,h-120),(520,h-320),(700,h-100)],fill=(95,130,90),outline=(20,20,20))
        d.polygon([(650,h-100),(820,h-330),(1050,h-100)],fill=(75,105,145),outline=(20,20,20))
        d.rounded_rectangle((60,55,1140,145),radius=20,fill=(255,255,245),outline=(20,20,20),width=5)
        d.text((85,78),f"PANEL {panel_number}",font=_font(38),fill=(20,20,20))
        d.text((85,165),"AI COMICCRAFT",font=_font(28),fill=(40,40,40))
        img.save(path)
    return f"/static/panels/{name}"
