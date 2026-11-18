"""Build a labeled preview of the headbutt animation frames."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SHEET = Image.open(ROOT / "assets" / "sprites" / "player.png").convert("RGBA")
FONT = ImageFont.load_default(size=18)
PHASES = [(14, "RECUO"), (15, "CABECADA"), (16, "RETORNO")]

preview = Image.new("RGB", (780, 300), "#142b4b")
draw = ImageDraw.Draw(preview)
draw.text((20, 14), "ANIMACAO DA CABECADA", fill="#fff1c6", font=FONT)

for index, (frame_index, label) in enumerate(PHASES):
    x = 16 + index * 256
    draw.rounded_rectangle((x, 48, x + 240, 278), radius=10, fill="#20466c", outline="#4f87a9", width=2)
    bbox = draw.textbbox((0, 0), label, font=FONT)
    draw.text((x + (240 - (bbox[2] - bbox[0])) // 2, 62), label, fill="#ffe06a", font=FONT)
    frame = SHEET.crop((frame_index * 32, 0, (frame_index + 1) * 32, 32))
    frame = frame.resize((160, 160), Image.Resampling.NEAREST)
    preview.paste(frame, (x + 40, 86), frame)
    draw.line((x + 20, 250, x + 220, 250), fill="#55c987", width=4)

for arrow_x in (244, 500):
    draw.line((arrow_x - 7, 173, arrow_x + 9, 173), fill="#fff1c6", width=3)
    draw.polygon([(arrow_x + 9, 173), (arrow_x + 2, 168), (arrow_x + 2, 178)], fill="#fff1c6")

out = ROOT / "docs" / "screenshots" / "headbutt.png"
out.parent.mkdir(parents=True, exist_ok=True)
preview.save(out)
print(out)
