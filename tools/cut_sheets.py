#!/usr/bin/env python3
"""Нарезка листов Gemini (сетка 3×3) на клетки для тренажёра.

python3 tools/cut_sheets.py листы/T001_S1.png [ещё листы…] --out words/img --size 320
Имя файла листа: T###_S#.(png|jpg|webp). Клетки: words/img/T###/T###_S#_C#.webp (C1…C9 слева направо, сверху вниз).
Клетки ищутся по полям фона между рамками; если сетка не нашлась — делится на равные части.
"""
import argparse, os, re, sys
import numpy as np
from PIL import Image


def segments(profile, thr, min_len):
    on = profile > thr
    out, start = [], None
    for i, v in enumerate(list(on) + [False]):
        if v and start is None: start = i
        if not v and start is not None:
            if i - start >= min_len: out.append((start, i))
            start = None
    return out


def cells(img, n=3):
    a = np.asarray(img.convert("RGB")).astype(int)
    h, w, _ = a.shape
    corners = np.concatenate([a[:8, :8].reshape(-1, 3), a[:8, -8:].reshape(-1, 3), a[-8:, :8].reshape(-1, 3), a[-8:, -8:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    mask = np.abs(a - bg).sum(axis=2) > 40
    cols = segments(mask.mean(axis=0), 0.25, w // 8)
    rows = segments(mask.mean(axis=1), 0.25, h // 8)
    if len(cols) != n or len(rows) != n:
        cw, ch = w // n, h // n
        cols = [(i * cw, (i + 1) * cw) for i in range(n)]; rows = [(i * ch, (i + 1) * ch) for i in range(n)]
        print(f"  сетка не найдена ({len(cols)}×{len(rows)}): делю поровну", file=sys.stderr)
    boxes = []
    for (y0, y1) in rows:
        for (x0, x1) in cols:
            m = max(4, (x1 - x0) // 60)          # срезаем тонкую рамку клетки
            boxes.append((x0 + m, y0 + m, x1 - m, y1 - m))
    return boxes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheets", nargs="+")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "words", "img"))
    ap.add_argument("--size", type=int, default=320)
    ap.add_argument("--check", help="сохранить контрольный лист нарезки в этот файл")
    x = ap.parse_args()
    done = 0
    for f in x.sheets:
        m = re.search(r"T(\d{3})_S(\d+)", os.path.basename(f))
        if not m: print("пропуск (имя не T###_S#):", f); continue
        tid, sh = m.group(1), m.group(2)
        img = Image.open(f).convert("RGB")
        d = os.path.join(x.out, f"T{tid}"); os.makedirs(d, exist_ok=True)
        thumbs = []
        for c, box in enumerate(cells(img), 1):
            cell = img.crop(box)
            s = min(cell.size); cell = cell.crop(((cell.width - s) // 2, (cell.height - s) // 2, (cell.width - s) // 2 + s, (cell.height - s) // 2 + s))
            cell = cell.resize((x.size, x.size), Image.LANCZOS)
            cell.save(os.path.join(d, f"T{tid}_S{sh}_C{c}.webp"), "WEBP", quality=82, method=6)
            thumbs.append(cell); done += 1
        if x.check:
            k = Image.new("RGB", (x.size * 3 + 20, x.size * 3 + 20), "white")
            for i, t in enumerate(thumbs): k.paste(t, (5 + (i % 3) * (x.size + 5), 5 + (i // 3) * (x.size + 5)))
            k.save(x.check)
        print(f"T{tid}_S{sh}: {len(thumbs)} клеток")
    print("готово клеток:", done)


if __name__ == "__main__":
    main()
