# Короткие 3D-ролики эмоций семьи (анимированный webp, 240 px, 12 кадров + пауза):
#   cd tools/art3d && python3 anim3d.py ../../words/img/fam [ru|uk]   → <lang>/<кто>_<эмоция>.webp
import os, sys
import toys
out_root = sys.argv[1]; langs = sys.argv[2:] or ["ru", "uk"]
for lang in langs:
    for who in toys.WHO:
        for emo in toys.EMO:
            toys.anim(who, lang, emo, os.path.join(out_root, lang, f"{who}_{emo}.webp"))
        print(lang, who, flush=True)
print("ok")
