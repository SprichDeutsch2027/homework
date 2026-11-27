# Малыш рисует за столом: cd tools/art3d && python3 malysh3d.py ../../words/img/fam
#   → <lang>/malysh_draw.webp, malysh_joy.webp (ролики), malysh_head.webp
import os, sys
import toys
out_root = sys.argv[1]
for lang in ("ru", "uk"):
    d = os.path.join(out_root, lang)
    toys.malysh_clip(lang, "draw", os.path.join(d, "malysh_draw.webp"))
    toys.malysh_clip(lang, "joy", os.path.join(d, "malysh_joy.webp"))
    toys.malysh_head(lang, os.path.join(d, "malysh_head.webp")); print(lang, flush=True)
print("ok")
