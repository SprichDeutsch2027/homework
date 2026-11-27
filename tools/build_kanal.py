#!/usr/bin/env python3
"""Каналы Lindenbrück и «диван» семьи → words/data/{kanal,divan}/T###.json + words/data/extra.json.

  words/src/kanal/T###.txt   строки K <слово> | <канал> | <подпись> | <DE с <u>…</u>> | <UK> | <RU>
  words/src/divan/T###.json  диалоги семьи, вопрос-рамка, правила проверки и образцы ответов
Проверяет: слово есть среди новых слов темы, каналы и персонажи известны, правила срабатывают на образцах
(через тот же words/check.js, что и в браузере — нужен node). Запуск: python3 tools/build_kanal.py
"""
import glob, json, os, re, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "words")
EN = len(sys.argv) > 1 and sys.argv[1] == "en"          # python3 tools/build_kanal.py en — английский вариант
DATA, SRCD = ("data_en", "src_en") if EN else ("data", "src")
FAM = json.load(open(os.path.join(ROOT, DATA, "family.json")))
CH, WHO = set(FAM["channels"]), set(FAM["chars"])
errs, extra = [], {"kanal": [], "divan": []}

def topic_words(tid):
    t = json.load(open(os.path.join(ROOT, DATA, "topics", f"T{tid:03d}.json")))
    return {w["w"]: w["k"] for w in t["words"] if w.get("first") == tid and w.get("tr")}

def say_ok(x, where):
    if not isinstance(x, dict) or x.get("who") not in WHO or not x.get("uk") or not x.get("ru"):
        errs.append(f"{where}: реплика без who/uk/ru или неизвестный персонаж ({x.get('who') if isinstance(x, dict) else x})")

os.makedirs(os.path.join(ROOT, DATA, "kanal"), exist_ok=True)
os.makedirs(os.path.join(ROOT, DATA, "divan"), exist_ok=True)

for f in sorted(glob.glob(os.path.join(ROOT, SRCD, "kanal", "T*.txt"))):
    tid = int(re.search(r"T(\d+)", f).group(1)); W = topic_words(tid); out = {}
    for no, line in enumerate(open(f, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.startswith("K "): continue
        p = [x.strip() for x in line[2:].split(" | ")]; where = f"{os.path.basename(f)}:{no}"
        if len(p) != 6: errs.append(f"{where}: нужно 6 полей, а их {len(p)}"); continue
        w, ch, cap, de, uk, ru = p
        if w not in W: errs.append(f"{where}: слова '{w}' нет среди новых слов темы {tid}"); continue
        if ch not in CH: errs.append(f"{where}: неизвестный канал '{ch}'")
        if "<u>" not in de: errs.append(f"{where}: в немецкой строке нет <u>…</u>")
        if "<u>" in uk + ru: errs.append(f"{where}: <u> в переводе")
        if W[w] in out: errs.append(f"{where}: слово '{w}' уже было")
        out[W[w]] = {"ch": ch, "cap": cap, "de": de, "uk": uk, "ru": ru}
    json.dump(out, open(os.path.join(ROOT, DATA, "kanal", f"T{tid:03d}.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    extra["kanal"].append(tid); print(f"kanal T{tid:03d}: {len(out)} из {len(W)} слов")

tests = []
for f in sorted(glob.glob(os.path.join(ROOT, SRCD, "divan", "T*.json"))):
    tid = int(re.search(r"T(\d+)", f).group(1)); W = topic_words(tid); keys = set(W.values())
    src = json.load(open(f, encoding="utf-8"))
    for k, d in src.items():
        where = f"{os.path.basename(f)}:{k}"
        if k not in keys: errs.append(f"{where}: ключа нет среди новых слов темы {tid}")
        for i, x in enumerate(d.get("lines", [])): say_ok(x, f"{where} lines[{i}]")
        say_ok(d.get("ask"), f"{where} ask")
        if not d.get("frame"): errs.append(f"{where}: нет frame")
        s = d.get("sample") or {}
        if not (s.get("de") and s.get("uk") and s.get("ru")): errs.append(f"{where}: sample без de/uk/ru")
        for r in d.get("rules", []):
            for kk in ("need", "not"):
                if kk in r:
                    try: re.compile(r[kk])
                    except re.error as e: errs.append(f"{where}: плохое выражение {r[kk]!r}: {e}")
            if "say" in r: say_ok(r["say"], f"{where} say")
            if "t" in r and r["t"] not in FAM["react"]: errs.append(f"{where}: тип '{r['t']}' не описан в family.json")
        t = d.get("tests") or {}
        if not t.get("ok") or not t.get("bad"): errs.append(f"{where}: нужны образцы tests.ok и tests.bad")
        tests += [[where, x, "ok", d.get("rules", [])] for x in t.get("ok", [])]
        tests += [[where, x, typ, d.get("rules", [])] for x, typ in t.get("bad", [])]
    json.dump({k: {kk: v for kk, v in d.items() if kk != "tests"} for k, d in src.items()},
              open(os.path.join(ROOT, DATA, "divan", f"T{tid:03d}.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    extra["divan"].append(tid); print(f"divan T{tid:03d}: {len(src)} слов")

# образцы ответов — через тот же проверяльщик, что в браузере
js = ("const C=require(process.argv[1]);const T=JSON.parse(require('fs').readFileSync(0,'utf8'));"
      "for(const [w,x,want,rules] of T){const r=C.check(x,rules);if(r.t!==want)console.log(w+': «'+x+'» → '+r.t+', ожидалось '+want)}")
try:
    res = subprocess.run(["node", "-e", js, os.path.join(ROOT, "check.js")], input=json.dumps(tests), capture_output=True, text=True, check=True)
    errs += [l for l in res.stdout.splitlines() if l.strip()]
    print(f"образцов ответов проверено: {len(tests)}")
except FileNotFoundError:
    errs.append("нет node — образцы ответов не проверены")

json.dump(extra, open(os.path.join(ROOT, DATA, "extra.json"), "w"))
for e in errs: print("ОШИБКА", e)
print(f"ошибок: {len(errs)}")
sys.exit(1 if errs else 0)
