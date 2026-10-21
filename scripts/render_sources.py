"""Review sheets are temporary evidence, not course illustrations."""
from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "tmp" / "source-review"
out.mkdir(parents=True, exist_ok=True)
doc = pdfium.PdfDocument(str(ROOT / "bv_cvxslides.pdf"))
for start in range(0, len(doc), 12):
    sheet = Image.new("RGB", (1920, 1536), "#d8dde4")
    for j in range(12):
        i = start + j
        if i >= len(doc):
            break
        im = doc[i].render(scale=0.9).to_pil().convert("RGB")
        im.thumbnail((630, 360))
        x, y = (j % 3) * 640, (j // 3) * 384
        sheet.paste(im, (x + (640 - im.width)//2, y + 22))
        ImageDraw.Draw(sheet).text((x+10, y+5), f"PDF {i+1}", fill="black")
    sheet.save(out / f"sheet-{start//12+1:02d}.jpg", quality=88)
for n in [17,30,36,52,55,56,60,67,73,74,76,85,112,115,119,135,136,139,149,160,170,171,183,191,197,198,202,207,210,211,214,216,225,228,234,240,242,250,253,259,266,271,276,282,285,305,309,312,316,319,320,321,322,326,330,339,342,349,359,362,363,374,379,380,382,386,388,393,394]:
    doc[n-1].render(scale=1.8).to_pil().save(out / f"page-{n:03d}.png")
print("Rendered",len(doc),"lecture pages into",len(list(out.glob('sheet-*.jpg'))),"sheets, plus selected detailed pages.")
