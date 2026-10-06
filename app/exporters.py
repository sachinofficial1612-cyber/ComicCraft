from pathlib import Path
from fpdf import FPDF
from PIL import Image
from .config import settings
ROOT=Path(__file__).resolve().parent.parent
EXPORT_DIR=ROOT/'static'/'exports'
def save_pdf(layout):
    EXPORT_DIR.mkdir(parents=True,exist_ok=True)
    pdf=FPDF(); pdf.set_margins(10,10,10); pdf.set_auto_page_break(True,15)
    for i,p in enumerate(layout):
        pdf.add_page(); pdf.set_font("Helvetica","B",18); pdf.cell(0,12,f"Panel {p['panel_number']}: {p['title']}",ln=True)
        img_path=ROOT/p['image'].lstrip('/')
        with Image.open(img_path) as im:
            iw,ih=im.size
        maxw=180; h=min(maxw*ih/iw,105)
        pdf.image(str(img_path),x=15,y=28,w=maxw,h=h)
        y=35+h+5
        if y > 270:
            y = 270
        pdf.set_xy(10,y)
        pdf.set_font("Helvetica","I",10); pdf.multi_cell(190,6,p.get("scene_description", ""))
        pdf.ln(2); pdf.set_font("Helvetica","",11)
        pdf.set_x(10); pdf.multi_cell(190,6,"Caption: "+p.get("caption",""))
        pdf.set_x(10); pdf.multi_cell(190,6,"Narration: "+p.get("narration",""))
        pdf.set_x(10); pdf.multi_cell(190,6,"Dialogue: "+p.get("dialogue",""))
    path=EXPORT_DIR/'comiccraft-comic.pdf'; pdf.output(str(path)); return '/static/exports/comiccraft-comic.pdf'
