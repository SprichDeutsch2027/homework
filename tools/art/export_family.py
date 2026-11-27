# Экспорт семьи для тренажёра: words/img/fam/{ru,uk}/<кто>[_<эмоция>].webp, <кто>_head.webp, scene.webp
#   cd tools/art && python3 export_family.py ../../words/img/fam
import os, sys, subprocess, zlib, importlib
from PIL import Image
out_root = sys.argv[1]
import kid
EMO = ("joy", "facepalm", "wow", "told")
for lang in ("ru", "uk"):
    os.environ["FAMLANG"] = lang
    import family; importlib.reload(family)
    out = os.path.join(out_root, lang); os.makedirs(out, exist_ok=True)
    tmp = f"/tmp/famexp_{lang}"; os.makedirs(tmp, exist_ok=True)
    for k, (paper, f) in family.SC.items():
        kid.seed(zlib.crc32(k.encode())); kid._id[0] = 0
        open(f"{tmp}/{k}.svg", "w").write(kid.svg(f(), kid.PAPER[paper]))
        subprocess.run(["rsvg-convert", "-w", "520", f"{tmp}/{k}.svg", "-o", f"{tmp}/{k}.png"], check=True)
        im = Image.open(f"{tmp}/{k}.png").convert("RGB")
        im.resize((360, 360), Image.LANCZOS).save(f"{out}/{k}.webp", quality=80)
        if k in family.WHO:  # голова для аватара в диалоге
            import inspect
            sc = inspect.signature(family.WHO[k]).parameters["s"].default
            hy = family.G - 77*sc; z = 520/200; half = 30*sc*z/1.25
            box = (int(100*z-half), int(max(0, hy*z-half*1.0)), int(100*z+half), int(max(0, hy*z-half*1.0)+2*half))
            im.crop(box).resize((160, 160), Image.LANCZOS).save(f"{out}/{k}_head.webp", quality=82)
    kid.seed(7); kid._id[0] = 0
    s = kid.svg(family.scene(), kid.PAPER["cream"]).replace('viewBox="0 0 200 200" width="520" height="520"', 'viewBox="0 0 360 200" width="1080" height="600"').replace('width="200" height="200"', 'width="360" height="200"')
    open(f"{tmp}/scene.svg", "w").write(s)
    subprocess.run(["rsvg-convert", f"{tmp}/scene.svg", "-o", f"{tmp}/scene.png"], check=True)
    Image.open(f"{tmp}/scene.png").convert("RGB").resize((900, 500), Image.LANCZOS).save(f"{out}/scene.webp", quality=80)
print("ok")
