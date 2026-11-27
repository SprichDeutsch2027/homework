# Семейный вечер: сценарий по состояниям. Каждое движение чем-то вызвано (рисунок, пирожки, телевизор, чья-то реплика).
#   cd tools/art3d && python3 evening.py ../../words/img/fam/ev [состояние…]   → <состояние>.webp + ../../words/data/evening.json
# Состояния: draw (малыш рисует, на листе появляются краски, котёнок просыпается, Ника встаёт снимать),
#   done (рисунок готов: малыш радуется, бабушка несёт пирожки к столу, щенок идёт следом),
#   talk_<кто> (говорит, остальные смотрят на него), cheer (все радуются), oops_<кто> (фейспалм), tv (телевизор включился)
import json, math, os, random, sys
import numpy as np
from PIL import Image
from ray import Scene, draw
import toys
from toys import Toy, WHO, SCALE, body, HC, HR, lerp
import room as R0

toys.PLATES = False
W, H = 600, 525
CAM = dict(center=(0, 1.0, -0.55), half=2.4, yaw=0.0, pitch=0.62)
ADULTS = ["vitya", "irina", "igor", "lyuda", "danya", "nika"]
SEAT = {"irina": (-0.58, -1.72, 0.0, True), "igor": (0.58, -1.72, 0.0, True), "vitya": (-2.2, -1.0, 0.65, True), "lyuda": (2.2, -1.0, -0.65, True),
        "danya": (-1.5, 0.85, 1.0, True), "nika": (1.5, 0.85, -1.0, True)}
AFTER = dict(SEAT, nika=(1.6, 0.6, -0.9, False), lyuda=(1.1, -0.78, -1.15, False))
KID = (0.0, -0.95)
TV = (1.55, 1.95, -2.62)
PLATE_TABLE = (0.48, 0.53, -0.5)

# ---------- питомцы ----------
def kitten(sc, x, z, yaw, mode="sit", t=0.0):
    T = Toy(sc, x, z, 1.0, yaw=yaw)
    o, wt, pk = T.m("kit", (232, 140, 60)), T.m("white", (250, 247, 240)), T.m("kpink", (240, 150, 160))
    ey, dk = T.m("eye", (35, 28, 24), spec=1.0), T.m("dark", (58, 42, 32))
    sw = math.sin(2*math.pi*t*2)
    if mode == "sleep":
        T.ell(o, (0, 0.08, 0), (0.15, 0.08, 0.13)); T.sphere(o, (0.1, 0.11, 0.08), 0.085)
        for sx in (-1, 1): T.ell(o, (0.1 + sx*0.05, 0.19, 0.06), (0.03, 0.04, 0.015))
        for sx in (-1, 1): T.cap(dk, (0.1 + sx*0.03 - 0.015, 0.12, 0.16), (0.1 + sx*0.03 + 0.015, 0.12, 0.16), 0.006)
        T.cap(o, (-0.12, 0.06, -0.05), (-0.02, 0.05, 0.14), 0.03)
        return
    lift = 0.03*abs(sw) if mode == "jump" else 0.0
    by = 0.15 + (0.12*abs(math.sin(math.pi*t*2)) if mode == "jump" else 0)
    T.ell(o, (0, by, -0.02), (0.1, 0.09, 0.15)); T.ell(wt, (0, by - 0.01, 0.1), (0.07, 0.07, 0.05))
    hz = 0.15 + (0.04 if mode == "paw" else 0)
    T.sphere(o, (0, by + 0.15, hz), 0.1)
    for sx in (-1, 1): T.ell(o, (sx*0.06, by + 0.24, hz - 0.01), (0.03, 0.055, 0.018)); T.ell(pk, (sx*0.06, by + 0.235, hz + 0.005), (0.015, 0.03, 0.006))
    for sx in (-1, 1): T.sphere(ey, (sx*0.04, by + 0.17, hz + 0.085), 0.019)
    T.ell(wt, (0, by + 0.12, hz + 0.08), (0.045, 0.03, 0.025)); T.sphere(pk, (0, by + 0.14, hz + 0.1), 0.012)
    for sx in (-1, 1):
        T.cap(o, (sx*0.05, by - 0.05, 0.08), (sx*0.05, 0.02 + (0.08 if mode == "paw" and sx > 0 else 0), 0.1 + (0.08 if mode == "paw" and sx > 0 else 0)), 0.028)
        T.cap(o, (sx*0.05, by - 0.05, -0.1), (sx*0.05, 0.02, -0.1), 0.03)
    a = 0.6*sw
    T.cap(o, (0, by, -0.15), (0.06*math.sin(a), by + 0.12, -0.24), 0.025); T.cap(o, (0.06*math.sin(a), by + 0.12, -0.24), (0.12*math.sin(a), by + 0.24, -0.22), 0.022)

def puppy(sc, x, z, yaw, mode="lie", t=0.0):
    T = Toy(sc, x, z, 1.0, yaw=yaw)
    wt, gi, pk = T.m("pupw", (250, 246, 238)), T.m("pupg", (226, 140, 70)), T.m("tongue", (232, 110, 120))
    ey = T.m("eye", (35, 28, 24), spec=1.0)
    wag = math.sin(2*math.pi*t*3)
    hop = 0.12*abs(math.sin(math.pi*t*2)) if mode == "jump" else 0.0
    if mode == "lie":
        by, hy = 0.12, 0.2
        T.ell(wt, (0, by, -0.02), (0.14, 0.1, 0.22)); T.ell(gi, (0.02, by + 0.07, -0.06), (0.1, 0.05, 0.12))
        for sx in (-1, 1): T.cap(wt, (sx*0.07, 0.05, 0.12), (sx*0.07, 0.05, 0.3), 0.04)
    else:
        by, hy = 0.25 + hop, 0.45 + hop
        T.ell(wt, (0, by, -0.02), (0.13, 0.12, 0.2)); T.ell(gi, (0.03, by + 0.08, -0.08), (0.1, 0.05, 0.11))
        beg = mode == "beg"
        for sx in (-1, 1):
            T.cap(wt, (sx*0.07, by - 0.05, 0.1), (sx*0.07, (0.25 if beg else 0.03) + hop, 0.12 + (0.08 if beg else 0)), 0.04)
            T.cap(wt, (sx*0.07, by - 0.05, -0.12), (sx*0.07, 0.03 + hop, -0.12), 0.045)
    hz = 0.2 if mode != "lie" else 0.25
    T.sphere(wt, (0, hy, hz), 0.13); T.ell(gi, (0.06, hy + 0.06, hz - 0.02), (0.08, 0.07, 0.09))
    tilt = 0.04 if mode == "tilt" else 0.0
    for sx in (-1, 1): T.ell(gi, (sx*0.13, hy - 0.02 + (tilt if sx > 0 else -tilt), hz - 0.02), (0.04, 0.1, 0.06))
    T.ell(wt, (0, hy - 0.04, hz + 0.11), (0.065, 0.055, 0.07)); T.sphere(T.m("dark", (58, 42, 32)), (0, hy - 0.02, hz + 0.18), 0.024)
    for sx in (-1, 1): T.sphere(ey, (sx*0.05, hy + 0.03, hz + 0.115), 0.02)
    if mode in ("beg", "jump", "sit", "bark"): T.ell(pk, (0, hy - 0.09, hz + 0.15), (0.025, 0.035, 0.012))
    a = 0.7*wag
    T.cap(gi, (0, by + 0.05, -0.2), (0.12*math.sin(a), by + 0.2, -0.3), 0.03)

# ---------- малыш ----------
def kid(sc, mode, t, look=0.0, p=1.0):
    s = 0.72; T = Toy(sc, KID[0], KID[1], s, oy=(0.1*abs(math.sin(math.pi*t*2)) if mode == "joy" else 0))
    w = math.sin(2*math.pi*t*2); w2 = math.sin(2*math.pi*t*3)
    if mode == "draw": pose = ((0.34, 0.9, 0.3), (0.15 + 0.16*w, 0.95 + 0.02*w2, 0.82 + 0.08*w2)); face, eyes = "smile", "side"; T.hx, T.hy = 0.01*w*s, -0.03*s
    elif mode == "joy": a = 0.08*w; pose = ((0.5 + a, 1.86, 0.06), (0.5 - a, 1.86, 0.06)); face, eyes = "big", "happy"; T.hy = 0.02*s
    else: pose = ("down", "down"); face, eyes = "smile", ("side" if look > 0.2 else "sideL" if look < -0.2 else "open"); T.hx = 0.03*look*s
    hands = body(T, "m", (253, 216, 53), (108, 180, 224), (229, 57, 53), pose, face, eyes)
    T.inhead = True; hair = T.m("mhair", (196, 110, 52))
    T.sphere(hair, (0, HC + 0.03, -0.02), HR + 0.012); T.above(1.62)
    T.cap(hair, (0, 1.76, 0.05), (0.06, 1.86, 0.08), 0.045); T.cap(hair, (0.06, 1.86, 0.08), (0.0, 1.9, 0.12), 0.035); T.inhead = False
    if mode == "draw":
        h = hands[1]; T.cap(T.m("cr0", (229, 57, 53)), (h[0], h[1] - 0.02, h[2] + 0.02), (h[0] + 0.03, h[1] - 0.12, h[2] + 0.1), 0.026)

# краски на листе: заранее заданные мазки, рисуются по мере готовности p
rnd = random.Random(7)
STROKES = []
for k in range(26):
    x0 = rnd.uniform(-0.3, 0.3); z0 = rnd.uniform(-0.3, 0.14); a = rnd.uniform(0, math.pi); L = rnd.uniform(0.06, 0.16)
    STROKES.append(((x0, z0), (x0 + math.cos(a)*L, z0 + math.sin(a)*L*0.6), rnd.choice([(229, 57, 53), (30, 136, 229), (67, 160, 71), (253, 216, 53), (226, 102, 154), (245, 166, 35)])))

def sheet_paint(sc, p):
    y = R0.SHEET["y"] + 0.004
    for k, (a, b, col) in enumerate(STROKES[:int(round(p*len(STROKES)))]):
        sc.capsule(sc.mat(f"paint{k%6}", col), (a[0], y, a[1]), (b[0], y, b[1]), 0.016)

def tv(sc, on):
    sc.rbox(sc.mat("tvbody", (45, 40, 38)), TV, (0.58, 0.38, 0.05), 0.03)
    col = {0: (40, 46, 56), 1: (250, 250, 250), 2: (180, 215, 240)}[on]
    sc.rbox(sc.mat(f"tvscr{on}", col, spec=1.0 if on else 0.0), (TV[0], TV[1], TV[2] + 0.04), (0.5, 0.31, 0.01), 0.01)
    if on == 2:
        sc.sphere(sc.mat("tvsun", (245, 166, 35)), (TV[0] - 0.25, TV[1] + 0.12, TV[2] + 0.055), 0.07)
        sc.rbox(sc.mat("tvhill", (120, 180, 90)), (TV[0], TV[1] - 0.2, TV[2] + 0.052), (0.48, 0.08, 0.005), 0.01)

# ---------- взгляд ----------
def look_eyes(fx, tx):
    d = tx - fx
    return ("side" if d > 0.35 else "sideL" if d < -0.35 else "open"), max(-1, min(1, d))*0.03

def adult(sc, who, pos, kw, look_x=None, tape=0.14, oy=0.0):
    x, z, yaw, sit = pos; kw = dict(kw)
    if look_x is not None and "eyes" not in kw:
        e, hx = look_eyes(x, look_x); kw["eyes"] = e; kw.setdefault("head", (hx, 0))
    T = Toy(sc, x, z, SCALE[who], oy=oy, head=kw.pop("head", (0, 0)), yaw=yaw, sit=sit); T.tape = tape
    WHO[who](T, "", **kw)

def scene_base(sc, plate_on_table, tv_on=0, paint=1.0):
    R0.room(sc); tv(sc, tv_on); sheet_paint(sc, paint)
    if plate_on_table:
        P = PLATE_TABLE; sc.cyly(sc.mat("plate", (250, 247, 240), spec=1.0), P, 0.2, 0.014, 0.008)
        for dx in (-0.08, 0.0, 0.08): sc.ell(sc.mat("pie", (224, 168, 58)), (P[0] + dx, P[1] + 0.04, P[2] + (0.04 if dx == 0 else 0)), (0.06, 0.035, 0.045))

def render(sc):
    img = draw(sc, W, H, CAM["center"], CAM["half"], yaw=CAM["yaw"], pitch=CAM["pitch"], bg=((60, 45, 35), (40, 30, 25)), light=(-0.35, 0.8, 0.55))
    return Image.fromarray((img*255).clip(0, 255).astype(np.uint8))

TBL = 0.0   # x стола для взгляда

def frame_draw(i, n=14):
    p = i/(n - 1); t = i/n; sc = Scene(); scene_base(sc, False, 0, p)
    kid(sc, "draw", t)
    # Даня ест чипсы, пока не заметил рисунок (кадр 5) — потом смотрит, удивляется
    if i < 5:
        w2 = 0.5 - 0.5*math.cos(2*math.pi*i/5)
        adult(sc, "danya", SEAT["danya"], dict(pose=("down", lerp((0.58, 0.98, 0.26), (0.2, 1.2, 0.42), w2)), face="big" if w2 > 0.6 else "smile"))
    else: adult(sc, "danya", SEAT["danya"], dict(pose=("down", "hold"), face="o" if i in (5, 6) else "smile"), look_x=TBL)
    # Ника снимает с пуфа, на кадре 4 встаёт и подходит ближе
    if i < 4: adult(sc, "nika", SEAT["nika"], dict(pose=("down", (0.5, 1.5, 0.25)), eyes="happy"))
    else:
        f = min(1.0, (i - 4)/5); a, b = SEAT["nika"], AFTER["nika"]
        pos = (a[0] + (b[0] - a[0])*f, a[1] + (b[1] - a[1])*f, a[2] + (b[2] - a[2])*f, False)
        adult(sc, "nika", pos, dict(pose=("down", (0.45, 1.5, 0.3)), eyes="happy"), oy=0.03*abs(math.sin(math.pi*f*4)) if f < 1 else 0)
    # Ирина показывает маркером на рисунок (кадр 7+), Игорь меряет рисунок рулеткой (кадр 9+)
    adult(sc, "irina", SEAT["irina"], dict(pose=((0.36, 0.8, 0.2), (0.3, 1.0, 0.5) if i >= 7 else "hold"), face="smile"), look_x=TBL if i >= 7 else None)
    adult(sc, "igor", SEAT["igor"], dict(pose=("down", "hold")), look_x=TBL if i >= 8 else None, tape=0.04 + (0.3*min(1, (i - 9)/3) if i >= 9 else 0))
    # Дедушка читает, на кадре 6 опускает словарь и смотрит
    adult(sc, "vitya", SEAT["vitya"], dict(pose=("down", (0.45, 1.08, 0.34) if i < 6 else "hold")), look_x=TBL if i >= 6 else None)
    adult(sc, "lyuda", SEAT["lyuda"], dict(pose=((0.24, 0.9, 0.38), (0.24, 0.9, 0.38)), eyes="happy" if i >= 10 else "open"), look_x=TBL)
    # котёнок спит, просыпается от шуршания мелка (кадр 6), подходит к столу (9–12)
    if i < 6: kitten(sc, 0.4, 1.15, 0.0, "sleep")
    else:
        f = min(1.0, max(0.0, (i - 8)/4)); kitten(sc, 0.4 - 0.15*f, 1.15 - 0.4*f, math.pi*0.9 if 0 < f < 1 else 0.0, "sit", t)
    puppy(sc, 1.85, -0.3, -0.5, "lie", t)       # щенок лежит у бабушки и смотрит на пирожки
    return render(sc)

def after_people(sc, t, kw_over=None, look_x=TBL, plate=True, tape=0.14, skip=()):
    kw_over = kw_over or {}
    base = {"danya": dict(pose=("down", "hold")), "nika": dict(pose=("down", (0.45, 1.5, 0.3))), "irina": dict(pose=((0.36, 0.8, 0.2), "hold")),
            "igor": dict(pose=("down", "hold")), "vitya": dict(pose=("down", "hold")), "lyuda": dict(pose=("down", "down"), prop=False)}
    for who in ADULTS:
        if who in skip: continue
        kw = kw_over.get(who, base[who])
        adult(sc, who, AFTER[who], kw, look_x=look_x, tape=tape)

def frame_done(i, n=8):
    t = i/n; sc = Scene(); scene_base(sc, i >= 6, 0, 1.0)
    kid(sc, "joy", t)
    # бабушка встаёт и несёт пирожки к столу; щенок идёт следом
    f = min(1.0, max(0.0, (i - 1)/4)); a, b = SEAT["lyuda"], AFTER["lyuda"]
    pos = (a[0] + (b[0] - a[0])*f, a[1] + (b[1] - a[1])*f, a[2] + (b[2] - a[2])*f, i == 0)
    adult(sc, "lyuda", pos, dict(pose=((0.24, 0.95, 0.42),)*2 if i < 6 else ("down", "down"), eyes="happy", prop=i < 6), oy=0.03*abs(math.sin(math.pi*f*4)) if 0 < f < 1 else 0)
    over = {"danya": dict(pose=((0.1, 1.0, 0.36), (0.1, 1.0, 0.36)), face="big", eyes="happy"), "vitya": dict(pose=("down", "hold"), face="big"),
            "irina": dict(pose=((0.36, 0.8, 0.2), "hold"), eyes="happy"), "igor": dict(pose=("down", "hold"), face="big")}
    after_people(sc, t, over, skip=("lyuda",))
    pf = min(1.0, max(0.0, (i - 1)/5)); puppy(sc, 1.85 - 0.45*pf, -0.3 + 0.12*pf, -0.5 - 0.8*pf, "sit" if pf < 1 else "beg", t)
    kitten(sc, 0.25, 0.75, 0.0, "jump" if i in (1, 2, 3) else "sit", t)
    return render(sc)

def frame_after(state, i, n):
    t = i/n; sc = Scene(); kind, _, who = state.partition("_")
    scene_base(sc, True, (1 if (kind == "tv" and i == 0) else 2) if kind == "tv" else 0, 1.0)
    if kind == "talk":
        sx = AFTER[who][0]; mouth = "big" if i % 2 == 0 else "smile"
        over = {who: dict(pose=("down", (0.42, 1.42 + 0.04*(i % 2), 0.32)), face=mouth, prop=False)}
        kid(sc, "look", t, look=max(-1, min(1, sx/2)))
        after_people(sc, t, over, look_x=sx)
        puppy(sc, 1.4, -0.18, -1.3, "beg" if i % 2 else "sit", t); kitten(sc, 0.25, 0.75, 0.3*math.copysign(1, sx), "sit", t)
    elif kind == "cheer":
        over = {w: dict(pose=("up", "up"), face="big", eyes="happy", prop=False) for w in ADULTS}
        kid(sc, "joy", t); after_people(sc, t, over)
        puppy(sc, 1.4, -0.18, -1.3, "jump", t); kitten(sc, 0.25, 0.75, 0.0, "jump", t)
    elif kind == "oops":
        sx = AFTER[who][0]
        over = {who: dict(pose=("down", (0.04, 1.42, 0.42)), face="line", eyes="closed", prop=False)}
        for w in ADULTS:
            if w != who: over[w] = dict(pose=dict(danya=("down", "hold"), nika=("down", (0.45, 1.5, 0.3)), irina=((0.36, 0.8, 0.2), "hold"), igor=("down", "hold"), vitya=("down", "hold"), lyuda=("down", "down"))[w], face="big" if w in ("danya", "nika") else "smile", **({"prop": False} if w == "lyuda" else {}))
        kid(sc, "look", t, look=max(-1, min(1, sx/2))); after_people(sc, t, over, look_x=sx)
        puppy(sc, 1.4, -0.18, -1.3, "tilt", t); kitten(sc, 0.25, 0.75, 0.0, "sit", t)
    elif kind == "tv":
        over = {"danya": dict(pose=("down", (0.5, 1.6, 0.0)), face="o" if i == 0 else "smile", prop=False)}
        kid(sc, "look", t, look=1.0); after_people(sc, t, over, look_x=TV[0])
        puppy(sc, 1.4, -0.18, -0.2, "bark" if i % 2 else "sit", t); kitten(sc, 0.25, 0.75, -0.4, "sit", t)
    return render(sc)

def project(p):
    W0, H0 = R0.W, R0.H
    R0.W, R0.H, R0.CAM = W, H, CAM
    q = R0.project(p, W, H); R0.W, R0.H = W0, H0
    return q

STATES = {"draw": (14, 230, 1), "done": (8, 200, 1), "cheer": (6, 160, 0), "tv": (6, 260, 0)}
for w in ADULTS: STATES[f"talk_{w}"] = (2, 300, 0); STATES[f"oops_{w}"] = (2, 400, 0)

def clip(state, path):
    n, dur, once = STATES[state]
    if state == "draw": fr = [frame_draw(i, n) for i in range(n)]
    elif state == "done": fr = [frame_done(i, n) for i in range(n)]
    else: fr = [frame_after(state, i, n) for i in range(n)]
    fr[0].save(path, save_all=True, append_images=fr[1:], duration=[dur]*n, loop=1 if once else 0, quality=74, method=4)
    if state == "done": fr[-1].save(path.replace("done.webp", "still.webp"), quality=80)

def meta(path):
    heads = {w: project((AFTER[w][0], HC*SCALE[w] + 0.15, AFTER[w][1])) for w in ADULTS}
    heads["malysh"] = project((KID[0], HC*0.72 + 0.1, KID[1]))
    y = R0.SHEET["y"]; x0, x1 = R0.SHEET["x"]; z0, z1 = R0.SHEET["z"]
    quad = [project((x0, y, z0)), project((x1, y, z0)), project((x1, y, z1)), project((x0, y, z1))]
    tvq = project((TV[0], TV[1] + 0.31, TV[2]))
    json.dump({"w": W, "h": H, "heads": heads, "sheet": quad, "tv": tvq, "states": {k: v[0]*v[1] for k, v in STATES.items()}}, open(path, "w"))

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "words", "data", "evening.json")
    meta(root)
    for st in (sys.argv[2:] or list(STATES)):
        clip(st, os.path.join(out, f"{st}.webp")); print(st, flush=True)
    print("ok")
