# Ролики «фирменных движений» семьи: cd tools/art3d && python3 act3d.py ../../words/img/fam [ru|uk] → <lang>/<кто>_act.webp
import os, sys
import toys
out_root = sys.argv[1]; langs = sys.argv[2:] or ["ru", "uk"]
for lang in langs:
    for who in toys.WHO:
        toys.act(who, lang, os.path.join(out_root, lang, f"{who}_act.webp")); print(lang, who, flush=True)
print("ok")
