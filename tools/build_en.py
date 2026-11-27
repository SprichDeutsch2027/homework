#!/usr/bin/env python3
"""Английский вариант словарного тренажёра → words/data_en/.

  words/src_en/s*.txt   темы: NAME, SCENE_UK/RU, HOST, E <герой> (25 строк), W <слово> (11–12 полей, 11-е — уровень)
  words/data/meta.json  порядок 750 тем (ступень, нивó, линия) — общий с немецким курсом
Пишет data_en/meta.json, topics/T###.json, stufen.json, index.json. Каналы и диван — tools/build_kanal.py en.
Запуск: python3 tools/build_en.py
"""
import glob, json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "words")
OUT = os.path.join(ROOT, "data_en")
DE_META = json.load(open(os.path.join(ROOT, "data", "meta.json")))["topics"]
HEROES = json.load(open(os.path.join(ROOT, "data", "heroes.json")))
HK = [h["key"] for h in HEROES["heroes"]]

# названия тем ступени 1 по-английски (остальные пока — названия немецкого курса, темы помечены «скоро»)
EN_NAMES = """Hello & Goodbye: greetings and farewells|My name is …: name, origin & language|Spelling & saying numbers|Numbers, age & prices up to 100|Days of the week & time|My family|At the café: ordering drinks|Colors & things around me|Months, seasons & birthday|Today's weather|My apartment: rooms|Furniture & furnishings|At the supermarket: aisles & products|Checkout, bottle deposit & receipt|Morning routine & daily schedule|Hobbies at home & outside|Places in town|Asking the way & directions|Clothes & sizes|Body parts & aches|At the family doctor|Bus & tram: ticket and ride|By train: station & platform|Fruit & vegetables at the market|Bread, cheese & sausage: breakfast|Free time: planning the weekend|After work & relaxing|Pets|Relatives & family party|Friends & making plans|Phone calls & texts|Writing an email & a short message|Post office: letter & parcel|In the language class|Jobs & workplace|Working hours & breaks|Bank account & card|Cooking: simple recipes|Eating out: restaurant basics|Cleaning & laundry|Sorting the trash|Neighbors & the hallway|Sports & exercise|By bike in the city|Vacation: where are we going?|At the hotel|Christmas & New Year's Eve|Emergency: calling for help|Feelings & mood|Photos & memories|Apartment hunting: reading ads|Apartment viewing & application|Character & personality|Describing appearance|Doctor's appointment & reception|Pharmacy & medicine cabinet|Bank: transfers & online banking|Cash, tips & splitting the bill|WhatsApp & group chat|Calling companies: hotline & voicemail|Buying clothes: fitting room & exchange|Shoes & accessories|At the gym|Soccer & club life|Job ads & applications|Job interview|Ordering online & returns|Parcel lockers & parcels at the neighbor's|Snack bars & street food|Cooking for guests|Town hall: registration & appointment|Official letters & forms|Bike: repair & workshop|Car: gas station & parking|Organizing a move""".split("|")
assert len(EN_NAMES) == 75

# рисунки мелками немецкой темы 1, подходящие по смыслу
IMG = {"hello": "hallo", "goodbye": "auf-wiedersehen", "bye": "tschuess", "good morning": "guten-morgen", "good afternoon": "guten-tag",
       "good evening": "guten-abend", "good night": "gute-nacht", "how are you?": "wie-gehts", "i'm fine": "mir-gehts-gut", "and you?": "und-dir",
       "thank you": "danke", "please": "bitte", "see you tomorrow": "bis-morgen", "see you later": "bis-spaeter", "nice to meet you": "haendedruck",
       "see you soon": "bis-bald", "have a nice day": "schoenen-tag-noch", "have a nice weekend": "schoenes-wochenende", "neighbor": "nachbar",
       "to greet": "gruessen", "to wave": "winken", "to hug": "umarmen", "to shake hands": "hand-geben", "polite": "hoeflich", "friendly": "freundlich",
       "not bad": "es-geht-so", "long time no see": "lange-nicht-gesehen", "take care": "machs-gut", "mrs.": "anrede", "formal": "formell",
       "informal": "locker", "rude": "unhoeflich", "small talk": "smalltalk", "to say goodbye": "sich-verabschieden", "to thank": "sich-bedanken",
       "farewell": "abschied", "to nod": "zunicken", "to get in touch": "sich-melden", "to strike up a conversation": "ins-gespraech-kommen",
       "a set phrase": "floskel", "etiquette": "etikette", "distant": "distanziert", "to drop by": "sich-blicken-lassen", "curt": "kurz-angebunden"}

def key(w): return re.sub(r"\s+", " ", w.strip().lower())

errs = []
def parse(f):
    T, cur = {}, None
    for no, line in enumerate(open(f, encoding="utf-8"), 1):
        line = line.rstrip("\n"); where = f"{os.path.basename(f)}:{no}"
        if not line or line.startswith("#"): continue
        if line.startswith("@ "):
            cur = {"id": int(line[2:]), "entry": {}, "words": [], "scene": {}, "f": os.path.basename(f)}; T[cur["id"]] = cur; continue
        if line.startswith("NAME:"): cur["name"] = line[5:].strip(); continue
        m = re.match(r"SCENE_(UK|RU):\s*(.*)", line)
        if m: cur["scene"][m.group(1).lower()] = m.group(2); continue
        if line.startswith("HOST:"):
            p = [x.strip() for x in line[5:].split(" | ")]; cur["host"] = {"who": p[0], "de": p[1], "uk": p[2], "ru": p[3]}; continue
        if line.startswith("E "):
            p = [x.strip() for x in line[2:].split(" | ")]; cur["entry"][p[0]] = {"uk": p[1], "ru": p[2]}; continue
        if line.startswith("W "):
            p = [x.strip() for x in line[2:].split(" | ")]
            if len(p) not in (11, 12): errs.append(f"{where}: нужно 11–12 полей, а их {len(p)}"); continue
            w = {"w": p[0], "k": key(p[0]), "pos": p[1], "tr": {"uk": p[2], "ru": p[3]},
                 "ex": {"de": p[4], "uk": p[5], "ru": p[6]}, "me": {"de": p[7], "uk": p[8], "ru": p[9]}, "lvl": p[10], "where": where}
            if len(p) == 12: w["def"] = p[11]
            for k in ("ex", "me"):
                if "<u>" not in w[k]["de"]: errs.append(f"{where}: в {k} нет <u>…</u>")
                if "<u>" in w[k]["uk"] + w[k]["ru"]: errs.append(f"{where}: <u> в переводе {k}")
            if re.search(r"\{[^}]*\|", w["ex"]["uk"] + w["ex"]["ru"]): errs.append(f"{where}: {{м|ж}} в примере сцены")
            if w["lvl"] not in ("A1", "A2", "B1", "B2"): errs.append(f"{where}: уровень '{w['lvl']}'")
            cur["words"].append(w); continue
        errs.append(f"{where}: непонятная строка")
    return T

SRC = {}
for f in sorted(glob.glob(os.path.join(ROOT, "src_en", "s*.txt"))): SRC.update(parse(f))

os.makedirs(os.path.join(OUT, "topics"), exist_ok=True)
meta, index = [], {}
for t in DE_META:
    tid = t["id"]; src = SRC.get(tid)
    name = (src or {}).get("name") or (EN_NAMES[tid-1] if tid <= 75 else t["name"])
    meta.append({"id": tid, "name": name, "stufe": t["stufe"], "niveau": t["niveau"], "line": t["line"], "ready": bool(src),
                 "n": 0 if not src else sum(1 for w in src["words"] if w["lvl"] == "A1")})
    if not src: continue
    if set(src["entry"]) != set(HK): errs.append(f"{src['f']}: входы героев: нет {sorted(set(HK)-set(src['entry']))}, лишние {sorted(set(src['entry'])-set(HK))}")
    for l in ("uk", "ru"):
        if l not in src["scene"]: errs.append(f"{src['f']}: нет SCENE_{l.upper()}")
    W = src["words"]; lv = lambda *ls: [i for i, w in enumerate(W) if w["lvl"] in ls]
    a1, a2, b1, b2 = lv("A1"), lv("A2"), lv("B1"), lv("B2")
    sets = {"easy": {"core": a1[:10], "chest": []},
            "course": {"core": a1, "chest": a2},
            "hard": {"core": a2[:12], "chest": [], "quick": a1},
            "harder": {"core": (a2 + b1)[:20], "chest": (a2 + b1)[20:] + b2, "quick": (a1 + a2)[:21]}}
    words = []
    for i, w in enumerate(W):
        item = {"n": i, "w": w["w"], "k": w["k"], "lvl": w["lvl"], "first": tid, "pos": w["pos"], "tr": w["tr"], "ex": w["ex"], "me": w["me"]}
        if "def" in w: item["def"] = w["def"]
        im = IMG.get(w["k"])
        if im and os.path.exists(os.path.join(ROOT, "img", "T001", f"a_{im}.webp")): item["img"] = f"img/T001/a_{im}.webp"
        words.append(item); index[w["k"]] = tid
    de_t = json.load(open(os.path.join(ROOT, "data", "topics", f"T{tid:03d}.json")))
    out = {"id": tid, "name": meta[-1]["name"], "stufe": t["stufe"], "niveau": t["niveau"], "level": de_t.get("level"), "line": t["line"],
           "context": "", "cast": de_t.get("cast", []), "ready": True, "down": [], "deferred": b1 + b2,
           "scene": src["scene"], "host": src["host"], "entry": src["entry"], "sets": sets, "words": words}
    json.dump(out, open(os.path.join(OUT, "topics", f"T{tid:03d}.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"T{tid:03d}: {len(words)} слов (A1 {len(a1)}, A2 {len(a2)}, B1 {len(b1)}, B2 {len(b2)})")

json.dump({"topics": meta}, open(os.path.join(OUT, "meta.json"), "w"), ensure_ascii=False, separators=(",", ":"))
json.dump(index, open(os.path.join(OUT, "index.json"), "w"), ensure_ascii=False, separators=(",", ":"))
st = json.load(open(os.path.join(ROOT, "data", "stufen.json")))
st["names"]["l12de"] = {"uk": "Як це англійською?", "ru": "Как это по-английски?"}
st["names"]["def2de"] = {"uk": "Яке слово за тлумаченням (англійською)?", "ru": "Какое слово по толкованию (по-английски)?"}
json.dump(st, open(os.path.join(OUT, "stufen.json"), "w"), ensure_ascii=False, separators=(",", ":"))
for e in errs: print("ОШИБКА", e)
print(f"тем: {len(meta)} · с текстами: {len(SRC)} · ошибок: {len(errs)}")
sys.exit(1 if errs else 0)
