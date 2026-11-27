import sys, os, re, importlib
from PIL import Image
def slug(w):
    w = re.sub(r"^(der|die|das)\s+", "", w.strip())
    w = w.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", w).strip("-")
mod = importlib.import_module(sys.argv[1]); src = sys.argv[2]; dst = sys.argv[3]; os.makedirs(dst, exist_ok=True)
tot = 0
for w, k in mod.KEYS.items():
    im = Image.open(f"{src}/{k}.png").convert("RGB").resize((480, 480), Image.LANCZOS)
    p = f"{dst}/a_{slug(w)}.webp"; im.save(p, "WEBP", quality=78, method=6); tot += os.path.getsize(p)
print(len(mod.KEYS), "files", tot//1024, "KB")
