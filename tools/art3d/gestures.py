# Жесты-подсказки: член семьи «показывает» слово, как в «Крокодиле» (3D-ролик + плоские значки поверх).
#   cd tools/art3d && python3 gestures.py ../../words/img/fam [ru|uk]  → <lang>/g_<жест>.webp + ../../words/data/gesture.json
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ray import Scene, draw
import toys
from toys import Toy, WHO, SCALE, BASE, PAPER, NICK, SKIN, lerp

NF = 12
FL = os.path.expanduser("~/.fonts/caveat-latin-700-normal.ttf")

# ---------- добавки к фигурке ----------
def thumb_up(T, h): T.cap(T.m("skin", SKIN), h, (h[0], h[1] + 0.13, h[2]), 0.032)
def finger_fwd(T, h): T.cap(T.m("skin", SKIN), h, (h[0] - 0.02, h[1], h[2] + 0.16), 0.03)
def fingers(T, h):
    for a in (-0.7, -0.35, 0.0, 0.35, 0.7): T.cap(T.m("skin", SKIN), h, (h[0] + math.sin(a)*0.13, h[1] + math.cos(a)*0.13, h[2]), 0.026)
def phone_ear(T, h): T.box(T.m("phone", (38, 55, 90)), (h[0] - 0.02, h[1] + 0.02, h[2] + 0.02), (0.035, 0.1, 0.02), 0.012)
def tear(T, h): T.ell(T.m("drop", (108, 180, 224), spec=1.0), (0.13, 1.36, 0.33), (0.025, 0.04, 0.025))

# ---------- плоские значки ----------
def icon(d, kind, k, t):
    S = lambda v: v*k
    ink = (58, 42, 32)
    if kind in ("sun", "sunlow", "sunrise"):
        y = {"sun": 70, "sunlow": 150, "sunrise": 170 - 90*min(1, t*1.4)}[kind]; c = (245, 166, 35) if kind != "sunlow" else (232, 96, 76)
        d.ellipse((S(40), S(y - 30), S(100), S(y + 30)), fill=c)
        for a in range(0, 360, 45):
            r = math.radians(a); d.line((S(70 + math.cos(r)*40), S(y + math.sin(r)*40), S(70 + math.cos(r)*55), S(y + math.sin(r)*55)), fill=c, width=int(S(6)))
    if kind == "moon":
        bg = d._image.getpixel((int(S(130)), int(S(28))))
        d.ellipse((S(40), S(40), S(105), S(105)), fill=(253, 216, 53)); d.ellipse((S(62), S(28), S(125), S(91)), fill=bg)
    if kind == "zzz":
        f = ImageFont.truetype(FL, int(S(44 + 10*math.sin(t*6.28))))
        d.text((S(250), S(70 - 20*t)), "Z z z", font=f, fill=(108, 130, 200))
    if kind == "clock":
        d.ellipse((S(35), S(35), S(115), S(115)), fill=(255, 255, 255), outline=ink, width=int(S(5)))
        a = t*6.28; d.line((S(75), S(75), S(75 + math.sin(a)*30), S(75 - math.cos(a)*30)), fill=ink, width=int(S(5)))
        d.line((S(75), S(75), S(95), S(75)), fill=ink, width=int(S(6)))
    if kind in ("calendar", "weekend"):
        d.rounded_rectangle((S(30), S(40), S(120), S(120)), radius=S(8), fill=(255, 255, 255), outline=ink, width=int(S(5)))
        d.rectangle((S(32), S(42), S(118), S(62)), fill=(229, 57, 53))
        for r in range(3):
            for c in range(5):
                col = (229, 57, 53) if kind == "weekend" and c >= 3 else (150, 140, 130)
                d.ellipse((S(40 + c*16), S(70 + r*15), S(48 + c*16), S(78 + r*15)), fill=col)
        if kind == "calendar": d.ellipse((S(70), S(83), S(92), S(105)), outline=(229, 57, 53), width=int(S(4)))
    if kind == "hourglass":
        d.polygon([(S(45), S(40)), (S(105), S(40)), (S(45), S(120)), (S(105), S(120))], fill=None, outline=ink, width=int(S(5)))
        lv = t; d.polygon([(S(55 + 20*lv), S(48 + 30*lv)), (S(95 - 20*lv), S(48 + 30*lv)), (S(75), S(78))], fill=(245, 166, 35))
        d.polygon([(S(75), S(110 - 25*lv)), (S(52), S(115)), (S(98), S(115))], fill=(245, 166, 35))
    if kind == "hearts":
        for j, (x, ph) in enumerate(((80, 0), (280, 0.35), (230, 0.7))):
            tt = (t + ph) % 1; y = 200 - 150*tt; r = 16 + 6*j
            c = (229, 57, 53) if j != 1 else (226, 102, 154)
            d.ellipse((S(x - r), S(y - r), S(x), S(y)), fill=c); d.ellipse((S(x), S(y - r), S(x + r), S(y)), fill=c)
            d.polygon([(S(x - r), S(y - r/2)), (S(x + r), S(y - r/2)), (S(x), S(y + r))], fill=c)
    if kind in ("q", "dots", "bla", "du", "sie", "hi"):
        d.rounded_rectangle((S(25), S(25), S(150), S(110)), radius=S(36), fill=(255, 255, 255), outline=ink, width=int(S(5)))
        d.polygon([(S(95), S(107)), (S(125), S(107)), (S(140), S(150))], fill=(255, 255, 255)); d.line((S(95), S(107), S(140), S(150), S(125), S(107)), fill=ink, width=int(S(5)))
        txt = {"q": "?", "dots": "• • •"[:1 + int(t*6) % 6], "bla": "bla bla", "du": "du", "sie": "Sie", "hi": "♥"}[kind]
        f = ImageFont.truetype(FL, int(S(58 if kind in ("q", "du", "sie") else 38)))
        d.text((S(88), S(67)), txt, font=f, fill=ink, anchor="mm")
    if kind == "storm":
        d.ellipse((S(30), S(40), S(90), S(90)), fill=(140, 140, 150)); d.ellipse((S(65), S(30), S(135), S(95)), fill=(140, 140, 150))
        if int(t*8) % 2: d.line((S(85), S(95), S(72), S(125), S(92), S(125), S(80), S(155)), fill=(253, 216, 53), width=int(S(6)))
    if kind == "door":
        d.rectangle((S(30), S(40), S(105), S(190)), fill=(138, 90, 43), outline=ink, width=int(S(5))); d.ellipse((S(88), S(110), S(98), S(120)), fill=(245, 166, 35))
        if int(t*6) % 2:
            for r in (14, 26, 38): d.arc((S(105 - r), S(115 - r), S(105 + r), S(115 + r)), -50, 50, fill=ink, width=int(S(5)))
    if kind == "wavy":
        y = 150 + 6*math.sin(t*12)
        d.line([(S(30 + x), S(y + 10*math.sin(x/12 + t*10))) for x in range(0, 100, 4)], fill=(245, 166, 35), width=int(S(7)))
    if kind == "sparkles":
        for j, (x, y) in enumerate(((60, 70), (300, 90), (270, 250), (80, 240), (180, 40))):
            r = 18 + 10*math.sin(t*12 + j); c = [(245, 166, 35), (226, 102, 154), (30, 136, 229), (67, 160, 71), (245, 166, 35)][j]
            d.line((S(x - r), S(y), S(x + r), S(y)), fill=c, width=int(S(6))); d.line((S(x), S(y - r), S(x), S(y + r)), fill=c, width=int(S(6)))

# ---------- жесты: кто, поза по времени, значки ----------
def W(t, n=2): return math.sin(2*math.pi*t*n)
def G(name, t):
    w = W(t); w2 = 0.5 - 0.5*math.cos(2*math.pi*t)
    wave = lambda who, x=0.55: dict(who=who, kw=dict(pose=("down", (x + 0.12*w, 1.62, 0.12)), eyes="happy"))
    one = lambda **kw: [dict(**kw)]
    if name == "wave": return one(**wave("danya")), []
    if name == "wave2": return one(who="nika", kw=dict(pose=((0.55 - 0.12*w, 1.62, 0.12), (0.55 + 0.12*w, 1.62, 0.12)), face="big", eyes="happy")), []
    if name == "greet": return one(who="igor", kw=dict(pose=("down", (0.55 + 0.1*w, 1.6, 0.12)), eyes="happy", head=(0, -0.04*w2))), []
    if name == "handshake":
        y = 1.0 + 0.06*W(t, 3)
        return [dict(who="igor", ox=-0.46, kw=dict(pose=("down", (0.4, y, 0.48)), eyes="happy")),
                dict(who="vitya", ox=0.46, kw=dict(pose=((0.4, y, 0.48), "down"), eyes="happy"))], []
    if name in ("hug", "hugwelcome"):
        a = 0.06*w
        return [dict(who="lyuda", ox=-0.3, kw=dict(pose=("down", (0.62, 1.05 + a, -0.08)), face="big", eyes="happy", head=(0.03, 0))),
                dict(who="danya", ox=0.3, kw=dict(pose=((0.62, 1.05 - a, -0.08), (0.5, 1.6 + a, 0.1)), eyes="happy", head=(-0.03, 0)))], (["hearts"] if name == "hugwelcome" else [])
    if name == "nod": return one(who="vitya", kw=dict(pose=("down", "down"), eyes="happy", head=(0, -0.05*abs(W(t, 2))))), []
    if name == "bow": return one(who="irina", kw=dict(pose=((0.12, 0.92, 0.32), (0.12, 0.92, 0.32)), eyes="closed", head=(0, -0.07*w2))), []
    if name == "thanks": return one(who="lyuda", kw=dict(pose=((0.1, 1.0, 0.33), (0.12, 0.92, 0.33)), eyes="happy", head=(0, -0.04*w2))), ["hearts"]
    if name == "please": return one(who="irina", kw=dict(pose=((0.05, 1.08 + 0.03*w, 0.4), (0.05, 1.08 + 0.03*w, 0.4)), eyes="happy", head=(0, -0.02*w2))), []
    if name == "morning": return one(who="danya", kw=dict(pose=((0.4 + 0.1*w2, 1.5 + 0.35*w2, 0.05),)*2, face="o" if w2 > 0.5 else "smile", eyes="closed" if w2 > 0.4 else "open")), ["sunrise"]
    if name == "day": return one(**wave("igor")), ["sun"]
    if name == "evening": return one(**wave("vitya")), ["sunlow"]
    if name == "night": return one(who="lyuda", kw=dict(pose=((0.12, 1.32, 0.3), (-0.12 + 0.3, 1.25, 0.3)), face="line", eyes="closed", head=(0.05, -0.03))), ["moon", "zzz"]
    if name == "howareyou": return one(who="nika", kw=dict(pose=((0.55, 0.95 + 0.05*w2, 0.2),)*2, eyes="open", head=(0.03*w, 0))), ["q"]
    if name == "fine": return one(who="igor", kw=dict(pose=("down", (0.45, 1.05 + 0.04*w, 0.35)), face="big", eyes="happy"), extra=[("r", thumb_up)]), ["sparkles"]
    if name == "soso": return one(who="danya", kw=dict(pose=("down", (0.45, 1.05, 0.35)), face="meh", eyes="side", head=(0.03*w, 0)), extra=[("r", fingers)]), ["wavy"]
    if name == "andyou": return one(who="irina", kw=dict(pose=((0.36, 0.8, 0.2), (0.22, 1.06 + 0.03*w, 0.5)), eyes="open"), extra=[("r", finger_fwd)]), ["q"]
    if name in ("tomorrow", "later", "soon"):
        who = {"tomorrow": "danya", "later": "nika", "soon": "irina"}[name]
        return one(**wave(who)), [{"tomorrow": "calendar", "later": "clock", "soon": "hourglass"}[name]]
    if name == "phone": return one(who="nika", kw=dict(pose=("down", (0.36, 1.4, 0.3)), face="big" if int(t*8) % 2 else "smile", eyes="happy"), extra=[("r", phone_ear)]), []
    if name == "weekend": return one(who="danya", kw=dict(pose=("up", "up"), face="big", eyes="happy", oy=0.12*abs(W(t, 1)))), ["weekend"]
    if name == "feierabend": return one(who="igor", kw=dict(pose=((0.2, 1.62, -0.12),)*2, eyes="closed", head=(0.03*w, 0))), ["sunlow"]
    if name == "heart": return one(who="lyuda", kw=dict(pose=((0.12, 1.0, 0.33), (0.12, 1.0, 0.33)), face="big", eyes="happy", head=(0.02*w, 0))), ["hearts"]
    if name == "rude": return one(who="vitya", kw=dict(pose=((0.2, 0.95, 0.3), (0.2, 0.9, 0.28)), face="line", eyes="side", head=(0.02*w, 0))), ["storm"]
    if name == "relaxed": return one(who="danya", kw=dict(pose=((0.22, 1.58, -0.14),)*2, eyes="happy", head=(0.03*w, 0))), []
    if name == "talk": return one(who="igor", kw=dict(pose=("down", (0.55 + 0.08*w, 1.0, 0.25)), face="big" if int(t*8) % 2 else "smile")), ["dots"]
    if name == "bla": return one(who="nika", kw=dict(pose=("down", (0.55 + 0.1*w, 1.05, 0.2)), face="big" if int(t*8) % 2 else "meh", eyes="side")), ["bla"]
    if name == "knock": return one(who="vitya", kw=dict(pose=("down", (0.15, 1.1 + 0.06*abs(W(t, 3)), 0.45)), eyes="open")), ["door"]
    if name == "du": return one(**wave("danya")), ["du"]
    if name == "sie": return one(who="irina", kw=dict(pose=((0.12, 0.92, 0.32), (0.12, 0.92, 0.32)), eyes="closed", head=(0, -0.06*w2))), ["sie"]
    if name == "farewell": return one(who="lyuda", kw=dict(pose=("down", (0.55 + 0.08*W(t, 1), 1.6, 0.12)), face="line", eyes="closed"), extra=[("r", tear)]), []
    if name == "joybig": return one(who="nika", kw=dict(pose=((0.5 + 0.1*w, 1.86, 0.06), (0.5 - 0.1*w, 1.86, 0.06)), face="big", eyes="happy", oy=0.16*abs(W(t, 1)))), ["sparkles"]
    if name == "hand": return one(who="vitya", kw=dict(pose=("down", (0.45, 1.25 + 0.03*w, 0.35)), eyes="open"), extra=[("r", fingers)]), []
    if name == "takecare": return one(who="lyuda", kw=dict(pose=((0.12, 1.0, 0.33), (0.55 + 0.1*w, 1.6, 0.12)), eyes="happy")), ["hearts"]
    if name == "niceday": return one(**wave("nika")), ["sun"]
    raise KeyError(name)

GEST = ["wave", "wave2", "greet", "handshake", "hug", "hugwelcome", "nod", "bow", "thanks", "please", "morning", "day", "evening", "night",
        "howareyou", "fine", "soso", "andyou", "tomorrow", "later", "soon", "phone", "weekend", "feierabend", "heart", "rude", "relaxed",
        "talk", "bla", "knock", "du", "sie", "farewell", "joybig", "hand", "takecare", "niceday"]

MAP = {
 "de": {"hallo": "wave", "tschüss": "wave", "guten morgen": "morning", "guten tag": "day", "guten abend": "evening", "auf wiedersehen": "farewell",
        "mir geht's gut": "fine", "grüßen": "greet", "bis morgen": "tomorrow", "bis später": "later", "bis bald": "soon", "gute nacht": "night",
        "schönes wochenende": "weekend", "anrede": "sie", "hand geben": "handshake", "es geht so": "soso", "hallo zusammen": "wave2", "bis dann": "later",
        "morgen": "morning", "tag": "day", "abend": "evening", "nacht": "night", "danke": "thanks", "bitte": "please", "hand": "hand", "herzlich": "heart",
        "mach's gut": "takecare", "freundlich": "heart", "nett": "heart", "bedanken": "thanks", "auf wiederhören": "phone", "lange nicht gesehen": "hugwelcome",
        "sympathisch": "heart", "besuch": "knock", "nachbar": "knock", "formell": "sie", "moin": "wave", "servus": "wave", "duzen": "du", "siezen": "sie",
        "schönen tag noch": "niceday", "schönen feierabend": "feierabend", "verabschieden": "farewell", "ansprechen": "talk", "höflich": "bow",
        "unhöflich": "rude", "locker": "relaxed", "winken": "wave", "abschied": "farewell", "umarmen": "hug", "melden": "phone", "händedruck": "handshake",
        "begrüßen": "greet", "begrüßung": "greet", "jemanden herzlich begrüßen": "hugwelcome", "vertraut": "heart", "grüß gott": "bow", "zunicken": "nod",
        "smalltalk": "talk", "du anbieten": "du", "tschau": "wave", "per du sein": "du", "distanziert": "rude", "förmlich": "sie", "flüchtig kennen": "nod",
        "ins gespräch kommen": "talk", "blicken lassen": "knock", "kurz angebunden": "rude", "zuwinken": "wave", "umgangsform": "bow", "floskel": "bla",
        "etikette": "bow", "überschwänglich": "joybig", "wie geht's?": "howareyou", "und dir?": "andyou", "und ihnen?": "andyou"},
 "en": {"hello": "wave", "hi": "wave", "goodbye": "farewell", "bye": "wave", "good morning": "morning", "good afternoon": "day", "good evening": "evening",
        "good night": "night", "how are you?": "howareyou", "i'm fine": "fine", "and you?": "andyou", "thank you": "thanks", "please": "please",
        "see you tomorrow": "tomorrow", "see you later": "later", "nice to meet you": "handshake", "see you soon": "soon", "have a nice day": "niceday",
        "have a nice weekend": "weekend", "neighbor": "knock", "to greet": "greet", "to wave": "wave", "to hug": "hug", "to shake hands": "handshake",
        "polite": "bow", "friendly": "heart", "not bad": "soso", "long time no see": "hugwelcome", "take care": "takecare", "to introduce": "handshake",
        "mrs.": "sie", "formal": "sie", "informal": "relaxed", "rude": "rude", "small talk": "talk", "to say goodbye": "farewell", "to thank": "thanks",
        "farewell": "farewell", "to nod": "nod", "to get in touch": "phone", "to strike up a conversation": "talk", "a set phrase": "bla", "etiquette": "bow",
        "distant": "rude", "to drop by": "knock", "curt": "rude"}}

def frame(name, lang, i, size=360):
    t = i/NF; specs, icons = G(name, t); sc = Scene(); two = len(specs) > 1
    who0 = specs[0]["who"]
    b = Toy(sc); b.cyl(b.m("base", BASE[who0]), (0, -0.07, 0), 1.1 if two else 0.66, 0.07, 0.035)
    for sp in specs:
        kw = dict(sp["kw"]); s = SCALE[sp["who"]]
        T = Toy(sc, sp.get("ox", 0.0), 0, s, oy=kw.pop("oy", 0.0), head=kw.pop("head", (0, 0)))
        hands = WHO[sp["who"]](T, NICK[lang][sp["who"]], prop=False, **kw)
        for side, fn in sp.get("extra", []): fn(T, hands[1 if side == "r" else -1])
    half = 1.45 if two else 1.26
    img = draw(sc, size, size, (0, 0.98, 0), half, yaw=0.22 if two else 0.32, pitch=0.2, bg=PAPER[who0])
    im = Image.fromarray((img*255).clip(0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    for ic in icons: icon(d, ic, size/360, t)
    return im

def clip(name, lang, path, size=240):
    frames = [frame(name, lang, i, size*3//2).resize((size, size), Image.LANCZOS) for i in range(NF)]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=[120]*NF, loop=0, quality=78, method=4)

if __name__ == "__main__":
    out_root = sys.argv[1]; langs = sys.argv[2:] or ["ru", "uk"]
    for lang in langs:
        for g in GEST:
            clip(g, lang, os.path.join(out_root, lang, f"g_{g}.webp")); print(lang, g, flush=True)
    who = {g: G(g, 0)[0][0]["who"] for g in GEST}
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "words")
    for tl, dr in (("de", "data"), ("en", "data_en")):
        json.dump({"who": who, "map": MAP[tl]}, open(os.path.join(root, dr, "gesture.json"), "w"), ensure_ascii=False)
    print("ok")
