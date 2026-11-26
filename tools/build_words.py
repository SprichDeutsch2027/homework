#!/usr/bin/env python3
"""Wortreise: сборка данных тренажёра слов (words/data/*) из файлов курса «10 Stufen».

Читает локальные (не публикуемые) файлы курса:
  --themes  deutsch_themen_750_v6.0.txt   (STUFE, пулы, CORE_POOL)
  --words   words_all.json                (слова тем по порядку)
  --first   word_first.json               (тема первого появления слова)
  --bilder  папка bilder (src/*.txt — SCENE/CAST, out/bilder_index.tsv)
  --src     words/src/*.txt               (контексты: сцены, входы героев, слова)
Пишет в words/data/: meta.json, heroes.json, stufen.json, index.json, topics/T###.json.
Проверяет тексты: каждое новое слово темы описано один раз, формат строк, <u>, {м|ж}.
"""
import argparse, glob, json, os, re, sys

LADDER_OLD = ["A1", "A2", "B1", "B2-C1", "Schrift"]
LADDER_NEW = ["Basis", "Haupt", "Schrift"]
POS = {"n", "v", "adj", "adv", "phr", "prep", "konj", "pron", "num", "part"}


def norm(w):
    w = w.strip().lower().replace("(pl.)", "").strip()
    return re.sub(r"^(der|die|das|sich)\s+", "", w)


def parse_quota(s):
    out = []
    for lv, n in re.findall(r"(Basis|Haupt|Schrift|B2-C1|A1|A2|B1)\s*:\s*(\d+)", s or ""):
        out.append((lv, int(n)))
    if not out and "остаток пула B2-C1" in (s or ""):
        m = re.search(r":\s*(\d+)\s*$", s)
        out.append(("B2-C1", int(m.group(1)) if m else 6))
    return out


def parse_themes(path):
    s = open(path, encoding="utf-8").read()
    T = {}
    for m in re.finditer(r'<TOPIC ([^>]*)>(.*?)</TOPIC>', s, re.S):
        a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        body = m.group(2)
        st = dict(re.findall(r'(\w+)="([^"]*)"', re.search(r"<STUFE ([^>]*)/>", body).group(1)))
        core = re.search(r"<CORE_POOL[^>]*>(.*?)</CORE_POOL>", body, re.S)
        core = [x.strip() for x in core.group(1).split(",")] if core else []
        tid = int(a["id"])
        T[tid] = {"id": tid, "name": a["name"], "line": a.get("linie", ""), "context": a.get("context", ""),
                  "stufe": int(st["n"]), "niveau": st["niveau"], "level": st["level"], "profile": st["profile"],
                  "collage": parse_quota(st.get("collage")), "up": parse_quota(st.get("second_up")),
                  "down": parse_quota(st.get("second_down")), "schrift": int(st.get("schrift", "0") or 0),
                  "core": core}
    return T


def parse_bilder(bdir):
    S = {}
    for f in sorted(glob.glob(os.path.join(bdir, "src", "*.txt"))):
        cur = None
        for ln in open(f, encoding="utf-8"):
            m = re.match(r"@ (\d+)", ln)
            if m: cur = int(m.group(1)); S[cur] = {"scene": "", "cast": []}; continue
            if cur and ln.startswith("SCENE:"): S[cur]["scene"] = ln[6:].strip()
            if cur and ln.startswith("CAST:"): S[cur]["cast"] = [x.strip() for x in ln[5:].split(",") if x.strip()]
    idx = {}
    p = os.path.join(bdir, "out", "bilder_index.tsv")
    if os.path.exists(p):
        for i, ln in enumerate(open(p, encoding="utf-8")):
            c = ln.rstrip("\n").split("\t")
            if i == 0 or len(c) < 5: continue
            idx[(int(c[1]), norm(c[4].lstrip("★")))] = c[0]
    return S, idx


def parse_src(src_dir, errs):
    D = {}
    for f in sorted(glob.glob(os.path.join(src_dir, "*.txt"))):
        cur = None
        for no, ln in enumerate(open(f, encoding="utf-8"), 1):
            ln = ln.rstrip("\n")
            if not ln.strip() or ln.startswith("#"): continue
            where = f"{os.path.basename(f)}:{no}"
            m = re.match(r"@ (\d+)\s*$", ln)
            if m:
                cur = int(m.group(1))
                if cur in D: errs.append(f"{where}: тема {cur} повторяется")
                D[cur] = {"scene": {}, "host": None, "entry": {}, "words": {}, "f": where}
                continue
            if cur is None: errs.append(f"{where}: строка до '@ N'"); continue
            d = D[cur]
            m = re.match(r"SCENE_(UK|RU):\s*(.+)$", ln)
            if m: d["scene"][m.group(1).lower()] = m.group(2).strip(); continue
            parts = [x.strip() for x in ln.split(" | ")]
            if ln.startswith("HOST:"):
                parts = [x.strip() for x in ln[5:].split(" | ")]
                if len(parts) != 4: errs.append(f"{where}: HOST — нужно 4 поля"); continue
                d["host"] = {"who": parts[0], "de": parts[1], "uk": parts[2], "ru": parts[3]}; continue
            if ln.startswith("E "):
                parts = [x.strip() for x in ln[2:].split(" | ")]
                if len(parts) != 3: errs.append(f"{where}: E — нужно 3 поля"); continue
                d["entry"][parts[0]] = {"uk": parts[1], "ru": parts[2]}; continue
            if ln.startswith("W "):
                parts = [x.strip() for x in ln[2:].split(" | ")]
                if len(parts) not in (10, 11): errs.append(f"{where}: W — нужно 10 полей (11 с толкованием), есть {len(parts)}: {ln[:70]}"); continue
                w = {"w": parts[0], "pos": parts[1], "tr": {"uk": parts[2], "ru": parts[3]},
                     "ex": {"de": parts[4], "uk": parts[5], "ru": parts[6]},
                     "me": {"de": parts[7], "uk": parts[8], "ru": parts[9]}, "where": where}
                if len(parts) == 11: w["def"] = parts[10]
                k = norm(parts[0])
                if k in d["words"]: errs.append(f"{where}: слово '{parts[0]}' второй раз")
                d["words"][k] = w
                continue
            errs.append(f"{where}: непонятная строка: {ln[:70]}")
    return D


def check_word(w, errs):
    wh = w["where"]
    if w["pos"] not in POS: errs.append(f"{wh}: часть речи '{w['pos']}'")
    for k in ("ex", "me"):
        de = w[k]["de"]
        if "<u>" not in de or de.count("<u>") != de.count("</u>"): errs.append(f"{wh}: {k} без <u>…</u>: {de[:60]}")
        for l in ("uk", "ru"):
            if "<u>" in w[k][l]: errs.append(f"{wh}: {k}.{l} — без <u> в переводе")
            if not w[k][l]: errs.append(f"{wh}: пустой {k}.{l}")
    if w["ex"]["de"] == w["me"]["de"]: errs.append(f"{wh}: пример и реплика одинаковые")
    for l in ("uk", "ru"):
        if not w["tr"][l]: errs.append(f"{wh}: пустой перевод {l}")
        if re.search(r"\{[^}|]*\}", w["me"][l]): errs.append(f"{wh}: {{м|ж}} без '|'")
        if re.search(r"\{[^}]*\|", w["ex"][l]): errs.append(f"{wh}: {{м|ж}} в примере сцены (только в реплике «я»)")


def ranked(words, core):
    """Порядок внутри пула: сначала по CORE_POOL, потом как в пуле."""
    pos = {norm(c): i for i, c in enumerate(core)}
    return sorted(range(len(words)), key=lambda i: (pos.get(norm(words[i][1]), 999), i))


def groups(t, words):
    """Группы слов темы и наборы обязательных для 4 положений сложности."""
    new_style = any(l in ("Basis", "Haupt") for l, _ in words)
    ladder = LADDER_NEW if new_style else LADDER_OLD
    pools = {l: [] for l in ladder}
    stufe_lvl = t["collage"][-1][0] if t["collage"] else ladder[1]
    for i, (l, w) in enumerate(words):
        l = stufe_lvl if l == "CORE" else l
        pools.setdefault(l, []).append(i)
    order = {i: r for r, i in enumerate(ranked(words, t["core"]))}
    for l in pools: pools[l].sort(key=lambda i: order[i])
    taken = set()

    def take(quota):
        out = []
        for l, n in quota:
            c = [i for i in pools.get(l, []) if i not in taken][:n]
            taken.update(c); out += c
        return out
    core = take(t["collage"])
    chest = take(t["up"])
    top = max(ladder.index(l) for l, _ in t["collage"]) if t["collage"] else 1
    down = take(t["down"])
    # остаток пулов уровня ступени — тоже сундук
    for l in ladder[:top + 1]:
        chest += [i for i in pools.get(l, []) if i not in taken]; taken.update(pools.get(l, []))
    deferred = [i for l in ladder[top + 1:] for i in pools.get(l, []) if i not in taken]
    if not new_style and t["id"] < 101:
        pass  # Schrift до темы 101 — только отложенные (уже в deferred)
    lvl_of = {i: (stufe_lvl if l == "CORE" else l) for i, (l, w) in enumerate(words)}
    sets = {"course": {"core": core, "chest": chest}}
    if new_style:
        haupt = pools.get("Haupt", [])
        sets["easy"] = {"core": pools.get("Basis", []) + haupt[:10], "chest": []}
        sets["hard"] = {"core": haupt[:28], "chest": [i for i in pools.get("Schrift", [])]}
        sets["harder"] = {"core": haupt + pools.get("Schrift", []), "chest": []}
    else:
        lower = [i for l in ladder[:top] for i in pools.get(l, [])]
        lower.sort(key=lambda i: order[i])
        sets["easy"] = {"core": lower[:15] if len(lower) >= 8 else core[:10], "chest": []}
        up1 = [i for i in pools.get(ladder[top + 1], [])] if top + 1 < len(ladder) else []
        up2 = [i for l in ladder[top + 1:top + 3] for i in pools.get(l, [])]
        sets["hard"] = {"core": up1[:15] or chest[:15], "chest": up1[15:], "quick": core}
        sets["harder"] = {"core": up2[:20], "chest": up2[20:], "quick": core + chest[:6]}
    return {"ladder": ladder, "stufe_lvl": stufe_lvl, "sets": sets, "down": down,
            "deferred": deferred, "lvl": lvl_of}


def art_slug(w):
    w = re.sub(r"^(der|die|das)\s+", "", w.strip())
    w = w.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", w).strip("-")


def main():
    ap = argparse.ArgumentParser()
    W0 = "/home/claude/work"
    ap.add_argument("--themes", default=f"{W0}/deutsch_themen_750_v6.0.txt")
    ap.add_argument("--words", default=f"{W0}/words_all.json")
    ap.add_argument("--first", default=f"{W0}/word_first.json")
    ap.add_argument("--bilder", default=f"{W0}/bilder")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "words"))
    ap.add_argument("--strict", action="store_true", help="ошибка, если у темы с текстами не хватает слов")
    x = ap.parse_args()
    root = os.path.abspath(x.root)
    T = parse_themes(x.themes)
    WA = {t["id"]: t for t in json.load(open(x.words, encoding="utf-8"))}
    F = json.load(open(x.first, encoding="utf-8"))["first"]
    B, BI = parse_bilder(x.bilder)
    errs, warns = [], []
    S = parse_src(os.path.join(root, "src"), errs)
    heroes = json.load(open(os.path.join(root, "data", "heroes.json"), encoding="utf-8"))
    hero_keys = [h["key"] for h in heroes["heroes"]]
    os.makedirs(os.path.join(root, "data", "topics"), exist_ok=True)
    meta = []
    index = {}
    for tid in sorted(T):
        t = T[tid]; words = [(l, w) for l, w in WA[tid]["words"]]
        g = groups(t, words)
        src = S.get(tid)
        out = {"id": tid, "name": t["name"], "stufe": t["stufe"], "niveau": t["niveau"], "level": t["level"],
               "line": t["line"], "context": t["context"], "cast": B.get(tid, {}).get("cast", []),
               "ready": bool(src), "sets": g["sets"], "down": g["down"], "deferred": g["deferred"], "words": []}
        seen = set()
        for i, (l, w) in enumerate(words):
            k = norm(w)
            first = F.get(k, tid)
            item = {"n": i, "w": w, "k": k, "lvl": g["lvl"][i], "first": first}
            if k in seen: item["dup"] = 1
            seen.add(k)
            if first == tid and src:
                sw = src["words"].get(k)
                if sw:
                    check_word(sw, errs)
                    if sw["w"] != w: warns.append(f"{tid}: '{sw['w']}' записано иначе, чем в теме: '{w}'")
                    item.update({kk: sw[kk] for kk in ("pos", "tr", "ex", "me", "def") if kk in sw})
                elif not item.get("dup"):
                    (errs if x.strict else warns).append(f"{tid}: нет текста для слова '{w}'")
            if first == tid:
                index[k] = tid
                art = f"img/T{tid:03d}/a_{art_slug(w)}.webp"   # рисунки мелками (приоритет)
                code = BI.get((tid, k))
                if os.path.exists(os.path.join(root, art)): item["img"] = art
                elif code:
                    img = f"img/T{tid:03d}/{code}.webp"
                    if os.path.exists(os.path.join(root, img)): item["img"] = img
            out["words"].append(item)
        if src:
            used = {norm(w) for l, w in words if F.get(norm(w)) == tid}
            for k in src["words"]:
                if k not in used: errs.append(f"{src['words'][k]['where']}: слова '{src['words'][k]['w']}' нет среди новых слов темы {tid}")
            for l in ("uk", "ru"):
                if l not in src["scene"]: errs.append(f"{src['f']}: нет SCENE_{l.upper()}")
            if not src["host"]: errs.append(f"{src['f']}: нет HOST")
            miss = [h for h in hero_keys if h not in src["entry"]]
            if miss: errs.append(f"{src['f']}: нет входов героев: {', '.join(miss)}")
            extra = [h for h in src["entry"] if h not in hero_keys]
            if extra: errs.append(f"{src['f']}: лишние ключи героев: {', '.join(extra)}")
            out.update({"scene": src["scene"], "host": src["host"], "entry": src["entry"]})
        json.dump(out, open(os.path.join(root, "data", "topics", f"T{tid:03d}.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, separators=(",", ":"))
        meta.append({"id": tid, "name": t["name"], "stufe": t["stufe"], "niveau": t["niveau"], "line": t["line"],
                     "ready": bool(src), "n": len(g["sets"]["course"]["core"])})
    json.dump({"topics": meta}, open(os.path.join(root, "data", "meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    json.dump(index, open(os.path.join(root, "data", "index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    ready = [m["id"] for m in meta if m["ready"]]
    for w in warns[:40]: print("ПРЕДУПРЕЖДЕНИЕ:", w)
    if len(warns) > 40: print(f"… и ещё {len(warns) - 40} предупреждений")
    for e in errs: print("ОШИБКА:", e)
    print(f"тем: {len(meta)} · с текстами: {len(ready)} ({ready[:1] and ready[0]}–{ready[-1:] and ready[-1]}) · ошибок: {len(errs)}")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
