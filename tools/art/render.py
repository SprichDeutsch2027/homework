import sys, os, subprocess, importlib, zlib
from PIL import Image, ImageDraw, ImageFont
mod = importlib.import_module(sys.argv[1]); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
import kid
only = sys.argv[3].split(",") if len(sys.argv) > 3 and sys.argv[3] else None
done = []
for k, (paper, f) in mod.SC.items():
    if only and k not in only: continue
    kid.seed(zlib.crc32(k.encode())); kid._id[0] = 0
    s = kid.svg(f(), kid.PAPER[paper])
    open(f"{out}/{k}.svg", "w").write(s)
    subprocess.run(["rsvg-convert", f"{out}/{k}.svg", "-o", f"{out}/{k}.png"], check=True)
    done.append(k)
# контактные листы по 12
font = ImageFont.load_default()
for i in range(0, len(done), 12):
    ks = done[i:i+12]; sheet = Image.new("RGB", (4*270, 3*290), "white"); d = ImageDraw.Draw(sheet)
    for n, k in enumerate(ks):
        im = Image.open(f"{out}/{k}.png").convert("RGB").resize((260, 260))
        x, y = (n % 4)*270, (n//4)*290; sheet.paste(im, (x+5, y+5)); d.text((x+8, y+268), k, fill="black", font=font)
    sheet.save(f"{out}/sheet_{i//12+1}.png")
print(len(done))
