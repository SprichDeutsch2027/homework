# Экспорт 3D-фигурок семьи в тренажёр (те же имена файлов, что у рисунков мелками):
#   cd tools/art3d && python3 export3d.py ../../words/img/fam [ru|uk]
# → <lang>/<кто>.webp, <кто>_<эмоция>.webp (360 px), <кто>_head.webp (160 px), scene.webp (900×500)
import os, sys
from PIL import Image
import toys

out_root = sys.argv[1]; langs = sys.argv[2:] or ["ru", "uk"]
for lang in langs:
    out = os.path.join(out_root, lang); os.makedirs(out, exist_ok=True)
    for who in toys.WHO:
        toys.figure(who, lang, size=540).resize((360, 360), Image.LANCZOS).save(f"{out}/{who}.webp", quality=82)
        toys.figure(who, lang, size=320, head=True).resize((160, 160), Image.LANCZOS).save(f"{out}/{who}_head.webp", quality=84)
        for emo in toys.EMO:
            im = toys.overlay(toys.figure(who, lang, emo, size=540), emo)
            im.resize((360, 360), Image.LANCZOS).save(f"{out}/{who}_{emo}.webp", quality=82)
        print(lang, who, flush=True)
    toys.group(lang, 1350, 750).resize((900, 500), Image.LANCZOS).save(f"{out}/scene.webp", quality=82)
    print(lang, "scene", flush=True)
print("ok")
