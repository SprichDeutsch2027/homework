# Векторные копии рисунков мелками (для анимации «рисуется мелками»): python3 export_svg.py t001 ../../words/img/T001
import sys, os, zlib, importlib, re
import kid
def slug(w):
    w = re.sub(r"^(der|die|das)\s+", "", w.strip())
    w = w.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", w).strip("-")
mod = importlib.import_module(sys.argv[1]); dst = sys.argv[2]; tot = 0
for w, k in mod.KEYS.items():
    paper, f = mod.SC[k]; kid.seed(zlib.crc32(k.encode())); kid._id[0] = 0
    s = kid.svg(f(), kid.PAPER[paper]).replace(' width="520" height="520"', "")
    s = re.sub(r"(\d+\.\d)\d+", r"\1", s)           # короче числа
    p = f"{dst}/a_{slug(w)}.svg"; open(p, "w").write(s); tot += os.path.getsize(p)
print(len(mod.KEYS), "svg", tot//1024, "KB")
