# Семья на диване — 3D-фигурки (пластилиновые игрушки на подставке). Строит сцену для ray.py.
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ray import Scene, draw

FONT = os.path.expanduser("~/.fonts/caveat-cyrillic-700-normal.ttf")
NICK = {"ru": dict(danya="Тиктокер", nika="Тиктокерша", irina="Душнила", igor="Душнила", lyuda="Динозавр", vitya="Динозавр", malysh="Малыш"),
        "uk": dict(danya="Тіктокер", nika="Тіктокерка", irina="Душнила", igor="Душнила", lyuda="Динозавр", vitya="Динозавр", malysh="Малюк")}
SKIN, CHEEK, EYE, DARK = (244, 200, 170), (236, 130, 150), (35, 28, 24), (58, 42, 32)
WHITE = (250, 247, 240)
PLATES = True

def text_img(t, w=320, h=80):
    im = Image.new("L", (w, h), 0); d = ImageDraw.Draw(im); size = 72
    while True:
        f = ImageFont.truetype(FONT, size); bb = d.textbbox((0, 0), t, font=f)
        if bb[2] - bb[0] <= w*0.9 and bb[3] - bb[1] <= h*0.85: break
        size -= 2
    d.text((w/2, h/2), t, font=f, fill=255, anchor="mm")
    return np.asarray(im, dtype=np.float32) / 255

class Toy:
    """Помощник: координаты фигурки в её собственных единицах (рост ≈ 2), масштаб s, сдвиг ox/oz."""
    def __init__(self, sc, ox=0.0, oz=0.0, s=1.0, oy=0.0, head=(0.0, 0.0), yaw=0.0, sit=False):
        self.sc, self.ox, self.oz, self.s, self.oy, self.hx, self.hy, self.inhead = sc, ox, oz, s, oy, head[0], head[1], False
        self.yaw, self.sit = yaw, sit
    def v(self, x, y, z):   # oy — прыжок всей фигурки; hx/hy — смещение головы (пока inhead); yaw — поворот к столу
        h = self.inhead; X = x*self.s + (self.hx if h else 0); Z = z*self.s
        c, sn = math.cos(self.yaw), math.sin(self.yaw)
        return (self.ox + X*c + Z*sn, self.oy + y*self.s + (self.hy if h else 0), self.oz - X*sn + Z*c)
    def r(self, a): return a*self.s
    def m(self, name, rgb, **kw): return self.sc.mat(name, rgb, **kw)
    def sphere(self, m, c, r, op=0): self.sc.sphere(m, self.v(*c), self.r(r), op)
    def cap(self, m, a, b, r, op=0): self.sc.capsule(m, self.v(*a), self.v(*b), self.r(r), op)
    def box(self, m, c, h, r, op=0): self.sc.rbox(m, self.v(*c), tuple(self.r(x) for x in h), self.r(r), op)
    def boxz(self, m, c, h, r, ang): self.sc.rboxz(m, self.v(*c), tuple(self.r(x) for x in h), self.r(r), ang)
    def ell(self, m, c, rr, op=0): self.sc.ell(m, self.v(*c), tuple(self.r(x) for x in rr), op)
    def torz(self, m, c, R, r): self.sc.torz(m, self.v(*c), self.r(R), self.r(r))
    def tory(self, m, c, R, r): self.sc.tory(m, self.v(*c), self.r(R), self.r(r))
    def cyl(self, m, c, r, h, rr): self.sc.cyly(m, self.v(*c), self.r(r), self.r(h), self.r(rr))
    def above(self, y): self.sc.above(0, self.r(y))
    def patch(self, key, text, c, hw, hh, bg=WHITE, ink=DARK):
        if not PLATES: return            # таблички с никами можно выключить
        k = self.sc.text_tex(text_img(text)); x, y, z = self.v(*c)
        m = self.sc.mat(key, bg, tex=3, tp=(x - self.r(hw), y - self.r(hh), self.r(2*hw), self.r(2*hh), k, 0), col2=ink)
        self.box(m, c, (hw, hh, 0.008), 0.012)

HC, HR = 1.43, 0.34       # центр и радиус головы
def zf(x, y, d=0.0):      # поверхность лица
    return math.sqrt(max(HR*HR - x*x - (y - HC)**2, 0.0)) + d

ARM = {"down": (0.47, 0.68, 0.08), "hold": (0.58, 0.98, 0.26), "up": (0.50, 1.88, 0.06), "wave": (0.58, 1.55, 0.14),
       "chest": (0.13, 0.92, 0.32), "face": (0.04, 1.42, 0.42), "point": (0.42, 1.95, 0.06)}

def body(T, k, sleeve, pants, shoes, pose, face="smile", eyes="open", top=None, legs=True):
    """Общее тело: ноги, туловище, руки, голова и лицо. Возвращает координаты кистей."""
    ms = T.m(k + "sl", sleeve); mp = T.m(k + "pa", pants); msh = T.m(k + "sh", shoes)
    sk = T.m("skin", SKIN); ey = T.m("eye", EYE, spec=1.0); dk = T.m("dark", DARK); ck = T.m("cheek", CHEEK)
    if legs and getattr(T, "sit", False):          # сидит: бедро вперёд, голень вниз
        for sx in (-1, 1):
            T.cap(mp, (sx*0.12, 0.6, 0.02), (sx*0.12, 0.6, 0.4), 0.088)
            T.cap(mp, (sx*0.12, 0.6, 0.4), (sx*0.12, 0.14, 0.44), 0.08)
            T.ell(msh, (sx*0.12, 0.06, 0.5), (0.1, 0.065, 0.15))
    elif legs:
        for sx in (-1, 1):
            T.cap(mp, (sx*0.11, 0.14, 0), (sx*0.11, 0.6, 0), 0.085)
            T.ell(msh, (sx*0.12, 0.06, 0.05), (0.1, 0.065, 0.15))
    if top is None: T.box(ms, (0, 0.86, 0), (0.25, 0.29, 0.17), 0.08)
    hands = {}
    for sx, a in ((-1, pose[0]), (1, pose[1])):
        sh = (sx*0.31, 1.06, 0.0)
        if a == "hip":
            el = (sx*0.52, 0.9, 0.02); hd = (sx*0.33, 0.74, 0.2)
            T.cap(ms, sh, el, 0.07); T.cap(ms, el, hd, 0.065); T.sphere(sk, hd, 0.08); hands[sx] = hd; continue
        if isinstance(a, tuple): hx, hy, hz = a
        else: hx, hy, hz = ARM[a]
        hd = (sx*hx, hy, hz)
        T.cap(ms, sh, hd, 0.07); T.sphere(sk, hd, 0.085); hands[sx] = hd
        if a == "point": T.cap(sk, hd, (hd[0], hd[1] + 0.14, hd[2]), 0.03)
    # голова
    T.inhead = True
    T.sphere(sk, (0, HC, 0), HR)
    T.sphere(sk, (0, 1.385, zf(0, 1.385, -0.005)), 0.036)                      # нос
    for sx in (-1, 1): T.ell(ck, (sx*0.19, 1.355, zf(sx*0.19, 1.355, -0.035)), (0.065, 0.042, 0.03))
    for sx in (-1, 1):
        ex = sx*0.12 + (0.05 if eyes == "side" else -0.05 if eyes == "sideL" else 0)
        if eyes in ("open", "side", "sideL"): T.sphere(ey, (ex, 1.465, zf(ex, 1.465, -0.02)), 0.046)
        elif eyes == "happy":
            T.cap(dk, (ex - 0.05, 1.45, zf(ex - .05, 1.45)), (ex, 1.49, zf(ex, 1.49)), 0.017)
            T.cap(dk, (ex, 1.49, zf(ex, 1.49)), (ex + 0.05, 1.45, zf(ex + .05, 1.45)), 0.017)
        else:
            T.cap(dk, (ex - 0.05, 1.47, zf(ex - .05, 1.47)), (ex, 1.45, zf(ex, 1.45)), 0.016)
            T.cap(dk, (ex, 1.45, zf(ex, 1.45)), (ex + 0.05, 1.47, zf(ex + .05, 1.47)), 0.016)
    if face == "big":
        T.ell(T.m("mouth", (205, 60, 60)), (0, 1.31, zf(0, 1.31, -0.035)), (0.09, 0.065, 0.05))
    elif face == "o":
        T.torz(dk, (0, 1.3, zf(0, 1.3, -0.005)), 0.035, 0.014)
    elif face in ("meh", "line"):
        pts = [(-0.06, 1.31), (0, 1.32 if face == "meh" else 1.31), (0.06, 1.305 if face == "meh" else 1.31)]
        for a, b in zip(pts, pts[1:]): T.cap(dk, (*a, zf(*a)), (*b, zf(*b)), 0.016)
    else:
        pts = [(math.sin(t)*0.095, 1.40 - math.cos(t)*0.095) for t in np.linspace(-0.95, 0.95, 6)]
        for a, b in zip(pts, pts[1:]): T.cap(dk, (*a, zf(*a)), (*b, zf(*b)), 0.017)
    T.inhead = False
    return hands

def hair_cap(T, m, cut=1.5, back=True, br=(0.345, 0.32, 0.26), by=1.4):
    T.sphere(m, (0, HC + 0.035, -0.02), HR + 0.018); T.above(cut)
    if back: T.ell(m, (0, by, -0.1), br)

# ---------- шестеро ----------
def danya(T, nick, pose=("down", "hold"), face="smile", eyes="open", prop=True):
    hood = T.m("dhood", (139, 195, 74)); hair = T.m("dhair", (93, 58, 26))
    T.inhead = True; T.sphere(hood, (0, 1.42, -0.07), 0.41); T.sphere(hood, (0, 1.42, 0.34), 0.37, op=1); T.inhead = False
    hands = body(T, "d", (139, 195, 74), (112, 107, 100), (250, 247, 240), pose, face, eyes)
    T.inhead = True
    hair_cap(T, hair, 1.53, back=False)
    T.cap(hair, (-0.22, 1.66, 0.2), (0.12, 1.55, 0.29), 0.065)                 # чёлка на глаза
    T.inhead = False
    T.cap(T.m("white", WHITE), (-0.06, 1.12, 0.24), (-0.06, 0.99, 0.26), 0.012); T.cap(T.m("white", WHITE), (0.06, 1.12, 0.24), (0.06, 0.99, 0.26), 0.012)
    T.tory(T.m("navy", (38, 55, 90)), (0, 1.13, 0), 0.21, 0.03)                 # наушники на шее
    for sx in (-1, 1): T.ell(T.m("red", (229, 57, 53)), (sx*0.22, 1.14, 0.05), (0.06, 0.075, 0.055))
    T.box(T.m("dpock", (118, 170, 60)), (0, 0.69, 0.25), (0.15, 0.05, 0.01), 0.01)
    T.patch("dpatch", nick, (0, 0.94, 0.256), 0.18, 0.065)
    for sx in (-1, 1):
        zz = 0.44 if T.sit else 0.0
        T.cap(T.m("white", WHITE), (sx*0.11, 0.07, zz), (sx*0.11, 0.2, zz), 0.092)   # носки
        T.box(T.m("slide", (13, 71, 161)), (sx*0.12, 0.018, zz + 0.05), (0.1, 0.018, 0.15), 0.02)
    if prop:
        h = hands[1]; T.box(T.m("chips", (245, 166, 35)), (h[0] + 0.02, h[1] + 0.12, h[2] + 0.04), (0.1, 0.13, 0.03), 0.025)
        T.sphere(T.m("red", (229, 57, 53)), (h[0] + 0.02, h[1] + 0.12, h[2] + 0.085), 0.045)
    return hands

def nika(T, nick, pose=("down", "wave"), face="smile", eyes="open", prop=True):
    hood = (38, 166, 154); hb = T.m("black", (35, 32, 30))
    T.box(T.m("nhood", hood), (0, 0.84, 0), (0.3, 0.31, 0.2), 0.09)
    hands = body(T, "n", hood, (40, 38, 36), (250, 247, 240), pose, face, eyes, top=False)
    T.inhead = True
    hair_cap(T, hb, 1.5, br=(0.35, 0.33, 0.27))
    T.cap(hb, (0, 1.76, -0.02), (0, 1.97, -0.02), 0.055)                          # хвост-«пальма»
    T.tory(T.m("rasp", (226, 102, 154)), (0, 1.86, -0.02), 0.06, 0.035)
    for dx, dy, dz in ((-0.2, -0.06, 0), (-0.12, 0.08, 0.03), (0, 0.12, 0.05), (0.12, 0.08, 0.03), (0.2, -0.06, 0), (0, 0.05, -0.12)):
        T.cap(hb, (0, 1.97, -0.02), (dx, 1.97 + dy, dz - 0.02), 0.04)
    T.inhead = False
    for sx in (-1, 1): T.ell(T.m("white", WHITE), (sx*0.12, 0.06, 0.5 if T.sit else 0.06), (0.12, 0.075, 0.17))
    T.box(T.m("nrib", (30, 140, 130)), (0, 0.56, 0), (0.3, 0.03, 0.2), 0.03)
    T.patch("npatch", nick, (0, 0.95, 0.296), 0.22, 0.065)
    if prop:
        h = hands[1]; c = (h[0] + 0.02, h[1] + 0.17, h[2] + 0.04)
        T.box(T.m("phone", (38, 55, 90)), c, (0.065, 0.11, 0.015), 0.015)
        T.torz(T.m("ring", (255, 241, 118), spec=1.0), (c[0], c[1], c[2] - 0.01), 0.15, 0.028)
    return hands

def irina(T, nick, pose=((0.36, 0.8, 0.2), "hold"), face="smile", eyes="open", prop=True):
    hair = T.m("ihair", (62, 39, 35)); navy = (13, 71, 161)
    hands = body(T, "i", navy, (38, 55, 90), (109, 76, 65), pose, face, eyes)
    T.inhead = True
    hair_cap(T, hair, 1.5)
    T.ell(hair, (0, 1.63, 0.2), (0.27, 0.075, 0.14))                              # ровная чёлка
    for sx in (-1, 1): T.ell(hair, (sx*0.3, 1.35, 0.0), (0.09, 0.19, 0.21))       # каре
    ink = T.m("dark", DARK); lens = T.m("lens", (179, 229, 252), spec=1.0)
    for sx in (-1, 1):                                                             # очки на голове
        T.torz(ink, (sx*0.12, 1.75, 0.16), 0.07, 0.016); T.ell(lens, (sx*0.12, 1.75, 0.155), (0.06, 0.06, 0.012))
    T.inhead = False
    T.box(T.m("white", WHITE), (0, 0.95, 0.25), (0.15, 0.17, 0.006), 0.02)
    T.patch("ipatch", nick, (0, 0.98, 0.262), 0.165, 0.055)
    for sx in (-1, 1): T.cap(T.m("isl", navy), (sx*0.2, 1.13, 0.25), (sx*0.17, 0.76, 0.27), 0.035)
    T.sphere(T.m("amber", (245, 166, 35)), (0, 0.72, 0.27), 0.022)
    if prop:
        T.box(T.m("folder", (108, 180, 224)), (-0.38, 0.86, 0.09), (0.035, 0.17, 0.14), 0.012)
        for k, col in enumerate(((229, 57, 53), (253, 216, 53), (67, 160, 71), (226, 102, 154))):
            T.box(T.m(f"tab{k}", col), (-0.34, 0.97 - k*0.06, 0.22), (0.02, 0.018, 0.03), 0.008)
        h = hands[1]; T.cap(T.m("yellow", (253, 216, 53)), (h[0] - 0.03, h[1], h[2] + 0.02), (h[0] + 0.05, h[1] + 0.2, h[2] + 0.05), 0.028)
        T.sphere(T.m("dark", DARK), (h[0] + 0.05, h[1] + 0.21, h[2] + 0.05), 0.026)
    return hands

def igor(T, nick, pose=("down", "hold"), face="smile", eyes="open", prop=True):
    plaid = T.m("plaid", (220, 60, 55), tex=1, tp=(9, 0.22, 0, 0, 0, 0), col2=(25, 60, 140))
    hands = body(T, "g", (220, 60, 55), (94, 88, 79), (138, 131, 121), pose, face, eyes, top=False)
    T.box(plaid, (0, 0.86, 0), (0.26, 0.29, 0.17), 0.08)
    hair = T.m("ghair", (128, 122, 114)); T.inhead = True
    T.sphere(hair, (0, HC + 0.03, -0.03), HR + 0.012); T.above(1.6)
    T.ell(hair, (0, 1.45, -0.12), (0.33, 0.28, 0.22))
    for k in range(9):                                                             # ёжик
        a = -1.1 + k*0.275; T.sphere(T.m("ghair2", (170, 164, 156)), (math.sin(a)*0.3, HC + math.cos(a)*0.31, 0.06), 0.03)
    dk = T.m("dark", DARK)
    for sx in (-1, 1): T.cap(dk, (sx*0.19, 1.545, zf(sx*.19, 1.545)), (sx*0.06, 1.535, zf(sx*.06, 1.535)), 0.028)
    for k in range(12):                                                            # щетина
        t = -0.8 + k*0.145; x, y = math.sin(t)*0.2, 1.37 - math.cos(t)*0.12
        T.sphere(T.m("stub", (120, 110, 100)), (x, y, zf(x, y, -0.006)), 0.009)
    T.inhead = False
    blue = T.m("blue", (30, 136, 229))
    if PLATES:
        for sx in (-1, 1): T.cap(blue, (sx*0.13, 1.13, 0.22), (sx*0.03, 0.99, 0.265), 0.013)
    T.patch("gpatch", nick, (0, 0.91, 0.27), 0.17, 0.075)
    if prop:
        h = hands[1]; c = (h[0] + 0.02, h[1] + 0.03, h[2] + 0.05)
        T.box(T.m("yellow", (253, 216, 53)), c, (0.08, 0.08, 0.05), 0.02)
        T.sphere(T.m("dark", DARK), (c[0], c[1], c[2] + 0.06), 0.025)
        L = getattr(T, "tape", 0.14)
        T.box(T.m("amber", (245, 166, 35)), (c[0] + 0.06 + L, c[1] - 0.06, c[2]), (L, 0.012, 0.03), 0.006)
    return hands

def lyuda(T, nick, pose=((0.24, 0.98, 0.36), (0.24, 0.98, 0.36)), face="smile", eyes="open", prop=True):
    body_c = (232, 96, 76)
    T.box(T.m("lcard", body_c), (0, 0.93, 0), (0.24, 0.21, 0.16), 0.08)
    T.box(T.m("lskirt", (109, 76, 65)), (0, 0.6, 0), (0.29, 0.15, 0.19), 0.08)
    hands = body(T, "l", body_c, (170, 120, 100), (226, 102, 154), pose, face, eyes, top=False)
    lav, pg = T.m("lav", (179, 157, 219)), T.m("pgrey", (232, 225, 212)); T.inhead = True
    for k in range(13):                                                            # укладка «облачком»
        a = math.pi*(0.02 + 0.96*k/12)
        T.sphere(lav if k % 2 else pg, (-math.cos(a)*0.33, HC + 0.08 + math.sin(a)*0.28, -0.06), 0.14)
    for k, x in enumerate((-0.16, 0.0, 0.16)): T.sphere(pg if k % 2 else lav, (x, 1.74, 0.1), 0.11)
    ink = T.m("dark", DARK)
    for sx in (-1, 1): T.torz(ink, (sx*0.12, 1.465, zf(sx*0.12, 1.465, 0.01)), 0.075, 0.014)
    T.cap(ink, (-0.045, 1.47, zf(-.045, 1.47, 0.01)), (0.045, 1.47, zf(.045, 1.47, 0.01)), 0.01)
    T.inhead = False
    T.cap(T.m("amber", (245, 166, 35)), (-0.2, 1.46, zf(-.2, 1.46)), (-0.2, 1.12, 0.2), 0.008)
    for k in range(7):                                                             # бусы
        t = k/6; col = [(245, 166, 35), WHITE, (229, 57, 53)][k % 3]
        T.sphere(T.m(f"bead{k%3}", col, spec=1.0), (-0.16 + 0.32*t, 1.09 - 0.06*math.sin(math.pi*t), 0.22), 0.034)
    apr = T.m("apron", WHITE, tex=2, tp=(11, 0.17, 0, 0, 0, 0), col2=(229, 57, 53))
    T.box(apr, (0, 0.6, 0.27), (0.21, 0.13, 0.01), 0.02)
    T.patch("lpatch", nick, (0, 0.8, 0.275), 0.19, 0.07)
    if prop:
        py, pz = (hands[-1][1] + hands[1][1])/2 - 0.01, (hands[-1][2] + hands[1][2])/2 + 0.04
        T.cyl(T.m("plate", WHITE, spec=1.0), (0, py, pz), 0.24, 0.016, 0.01)
        for dx in (-0.1, 0.0, 0.1): T.ell(T.m("pie", (224, 168, 58)), (dx, py + 0.05, pz + (0.05 if dx == 0 else 0)), (0.07, 0.04, 0.05))
    return hands

def vitya(T, nick, pose=("down", "hold"), face="smile", eyes="open", prop=True):
    vest = (224, 168, 58)
    hands = body(T, "v", (240, 236, 228), (109, 76, 65), (109, 76, 65), pose, face, eyes, top=False)
    T.box(T.m("vvest", vest), (0, 0.86, 0), (0.25, 0.29, 0.17), 0.08)
    gr = T.m("vhair", (200, 194, 184)); T.inhead = True
    for sx in (-1, 1):                                                             # волосы торчком
        for dy, dx in ((0.12, 0.13), (0.0, 0.16), (-0.12, 0.12)):
            T.cap(gr, (sx*0.3, 1.45 + dy*0.6, -0.02), (sx*(0.3 + dx), 1.45 + dy*1.3, 0.0), 0.045)
    T.cap(gr, (-0.03, 1.76, 0.0), (-0.08, 1.88, 0.0), 0.03); T.cap(gr, (0.03, 1.76, 0.0), (0.07, 1.9, 0.0), 0.03)
    for sx in (-1, 1): T.ell(gr, (sx*0.085, 1.335, zf(sx*0.085, 1.335, -0.01)), (0.105, 0.05, 0.05))   # усы
    T.inhead = False
    T.box(T.m("white", WHITE), (-0.03, 0.92, 0.25), (0.14, 0.2, 0.006), 0.02)
    T.patch("vpatch", nick, (-0.03, 0.97, 0.262), 0.135, 0.048)

    sc = T.m("scarf", (67, 160, 71), tex=4, tp=(T.ox, T.oz, 6, 0, 0, 0), col2=WHITE)
    T.tory(sc, (0, 1.12, 0), 0.2, 0.065)
    T.box(T.m("scarfend", (67, 160, 71), tex=5, tp=(0, 18/T.s, 0, 0, 0, 0), col2=WHITE), (0.215, 0.9, 0.27), (0.05, 0.18, 0.02), 0.02)
    if prop:
        h = hands[1]; c = (h[0] + 0.03, h[1] + 0.1, h[2] + 0.05)
        T.box(T.m("book", (183, 28, 28)), c, (0.11, 0.14, 0.055), 0.015)
        T.box(T.m("pages", (232, 225, 212)), (c[0] + 0.02, c[1], c[2]), (0.1, 0.13, 0.04), 0.005)
    return hands

WHO = dict(danya=danya, nika=nika, irina=irina, igor=igor, lyuda=lyuda, vitya=vitya)
SCALE = dict(danya=1.06, nika=0.96, irina=1.0, igor=1.07, lyuda=0.94, vitya=1.0)
PAPER = dict(danya=((228, 241, 233), (210, 229, 217)), nika=((250, 232, 238), (238, 214, 222)), irina=((224, 234, 242), (205, 220, 232)),
             igor=((236, 233, 227), (220, 215, 206)), lyuda=((250, 233, 218), (238, 216, 196)), vitya=((251, 242, 214), (240, 226, 188)))
BASE = dict(danya=(170, 205, 185), nika=(232, 184, 200), irina=(160, 190, 214), igor=(196, 188, 176), lyuda=(232, 190, 160), vitya=(226, 200, 140))

EMO = {"joy": dict(pose=("up", "up"), face="big", eyes="happy"),
       "facepalm": dict(pose=("down", "face"), face="line", eyes="closed"),
       "wow": dict(pose=("up", "up"), face="o", eyes="open"),
       "told": dict(pose=("hip", "point"), face="meh", eyes="side")}

def figure(who, lang="ru", emo=None, size=720, head=False):
    sc = Scene(); s = SCALE[who]; T = Toy(sc, 0, 0, s)
    T.cyl(T.m("base", BASE[who]), (0, -0.07, 0), 0.66, 0.07, 0.035)
    kw = dict(EMO[emo]) if emo else {}
    if emo: kw["prop"] = False
    WHO[who](T, NICK[lang][who], **kw)
    if emo == "facepalm": T.ell(T.m("drop", (108, 180, 224), spec=1.0), (0.42, 1.72, 0.2), (0.045, 0.07, 0.045))
    if head: img = draw(sc, size, size, (0, 1.5*s, 0), 0.47*s, yaw=0.12, pitch=0.1, bg=PAPER[who])
    else: img = draw(sc, size, size, (0, 0.96*s, 0), 1.26, yaw=0.32, pitch=0.2, bg=PAPER[who])
    return Image.fromarray((img*255).clip(0, 255).astype(np.uint8))

def overlay(im, emo):
    """Плоские значки эмоций поверх рендера: искры, восклицательные знаки, облачко «!!»."""
    d = ImageDraw.Draw(im); W = im.width; k = W/720
    def spark(x, y, r, c):
        d.line((x - r, y, x + r, y), fill=c, width=int(7*k)); d.line((x, y - r, x, y + r), fill=c, width=int(7*k))
    def excl(x, y, c=(229, 57, 53)):
        d.rounded_rectangle((x - 9*k, y - 50*k, x + 9*k, y + 10*k), radius=8*k, fill=c); d.ellipse((x - 10*k, y + 22*k, x + 10*k, y + 42*k), fill=c)
    if emo == "joy": spark(110*k, 160*k, 28*k, (245, 166, 35)); spark(610*k, 210*k, 24*k, (226, 102, 154)); spark(590*k, 470*k, 18*k, (30, 136, 229))
    if emo == "wow": excl(110*k, 220*k); excl(620*k, 220*k)
    if emo == "told":
        d.rounded_rectangle((40*k, 40*k, 230*k, 150*k), radius=40*k, fill=(255, 255, 255), outline=(58, 42, 32), width=int(6*k))
        d.polygon([(120*k, 147*k), (170*k, 147*k), (190*k, 205*k)], fill=(255, 255, 255)); d.line((120*k, 147*k, 190*k, 205*k, 170*k, 147*k), fill=(58, 42, 32), width=int(6*k))
        excl(115*k, 95*k, (245, 166, 35)); excl(155*k, 95*k, (245, 166, 35))
    return im

def group(lang="ru", W=1800, H=1000):
    sc = Scene(); sofa = sc.mat("sofa", (140, 190, 225)); wood = sc.mat("wood", (138, 90, 43))
    sc.rbox(sofa, (0, 0.75, -0.75), (3.0, 0.55, 0.22), 0.12); sc.rbox(sofa, (0, 0.38, -0.3), (3.1, 0.2, 0.45), 0.1)
    for sx in (-1, 1): sc.rbox(sofa, (sx*3.25, 0.6, -0.35), (0.18, 0.4, 0.5), 0.1)
    sc.rbox(sc.mat("floor", (226, 206, 176)), (0, -0.06, 0.1), (3.9, 0.06, 1.1), 0.04)
    pos = (("vitya", -2.6), ("danya", -1.56), ("irina", -0.52), ("igor", 0.52), ("nika", 1.56), ("lyuda", 2.6))
    for who, x in pos:
        T = Toy(sc, x, 0.35, SCALE[who]); WHO[who](T, NICK[lang][who])
    img = draw(sc, W, H, (0, 0.95, 0), 1.78, yaw=0.1, pitch=0.22, bg=((246, 240, 228), (236, 226, 208)))
    return Image.fromarray((img*255).clip(0, 255).astype(np.uint8))


# ---------- анимация эмоций (кадры для коротких роликов) ----------
NF = 12
def lerp(a, b, t): return tuple(x + (y - x)*t for x, y in zip(a, b))
def frame_kw(emo, i, n=NF):
    """Параметры кадра i: позы рук, лицо, глаза, прыжок, смещение головы."""
    t = i/(n - 1); ph = 2*math.pi*t
    if emo == "joy":
        w = math.sin(ph*2)*0.09
        return dict(pose=((0.5 + w, 1.86, 0.06), (0.5 - w, 1.86, 0.06)), face="big", eyes="happy", oy=0.13*abs(math.sin(ph)), head=(0, 0.02*abs(math.sin(ph))))
    if emo == "facepalm":
        up = min(1.0, t/0.3); hx = 0.035*math.sin((t - 0.3)*4*math.pi) if t > 0.3 else 0.0
        hand = lerp((0.47, 0.68, 0.08), (0.04 + hx, 1.42, 0.42), up)
        return dict(pose=("down", hand), face="line" if up >= 1 else "smile", eyes="closed" if up >= 0.8 else "open", head=(hx, -0.02*up), drop=t > 0.45)
    if emo == "wow":
        up = min(1.0, t/0.25); a = lerp((0.47, 0.68, 0.08), (0.5, 1.88, 0.06), up)
        tr = 0.02*math.sin(ph*6) if up >= 1 else 0
        hop = 0.1*math.sin(math.pi*min(1, max(0, (t - 0.2)/0.4)))
        return dict(pose=((a[0] + tr, a[1], a[2]), (a[0] - tr, a[1], a[2])), face="o" if up > 0.5 else "smile", eyes="open", oy=hop, head=(0, 0.03*up))
    if emo == "told":
        up = min(1.0, t/0.25); wag = 0.08*math.sin((t - 0.25)*4*math.pi) if t > 0.25 else 0
        a = lerp((0.47, 0.68, 0.08), (0.42 + wag, 1.95, 0.06), up)
        return dict(pose=("hip", a), face="meh", eyes="side", head=(wag*0.25, 0), point=up >= 0.9)
    raise KeyError(emo)

def anim_frame(who, lang, emo, i, size=240, n=NF):
    kw = frame_kw(emo, i, n); sc = Scene(); s = SCALE[who]
    base = Toy(sc, 0, 0, s); base.cyl(base.m("base", BASE[who]), (0, -0.07, 0), 0.66, 0.07, 0.035)
    T = Toy(sc, 0, 0, s, oy=kw.pop("oy", 0.0), head=kw.pop("head", (0, 0)))
    drop = kw.pop("drop", False); point = kw.pop("point", False)
    WHO[who](T, NICK[lang][who], prop=False, **kw)
    if point:   # палец вверх у поднятой руки
        hx, hy, hz = kw["pose"][1]; T.cap(T.m("skin", SKIN), (hx, hy, hz), (hx, hy + 0.14, hz), 0.03)
    if drop: T.ell(T.m("drop", (108, 180, 224), spec=1.0), (0.42, 1.72, 0.2), (0.045, 0.07, 0.045))
    img = draw(sc, size, size, (0, 0.96*s, 0), 1.26, yaw=0.32, pitch=0.2, bg=PAPER[who])
    im = Image.fromarray((img*255).clip(0, 255).astype(np.uint8))
    if i >= n//3: overlay(im, emo)
    return im

def anim(who, lang, emo, path, size=240, n=NF):
    frames = [anim_frame(who, lang, emo, i, size*3//2, n).resize((size, size), Image.LANCZOS) for i in range(n)]
    dur = [90]*(n - 1) + [1400]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=dur, loop=0, quality=78, method=4)


# ---------- фирменные движения с предметами (ролик <кто>_act.webp) ----------
def act_kw(who, t):
    w = math.sin(2*math.pi*t); w2 = 0.5 - 0.5*math.cos(2*math.pi*t)      # туда-обратно
    if who == "danya":   # подносит чипсы ко рту и жуёт
        return dict(pose=("down", lerp((0.58, 0.98, 0.26), (0.2, 1.2, 0.42), w2)), face="big" if w2 > 0.6 else "smile", eyes="happy" if w2 > 0.6 else "open", head=(0, -0.02*w2))
    if who == "nika":    # снимает всех, ведёт телефоном
        return dict(pose=("down", (0.58 - 0.22*w2, 1.55 + 0.05*w, 0.18 + 0.1*w2)), eyes="happy", head=(0.02*w, 0))
    if who == "irina":   # выделяет маркером в воздухе
        return dict(pose=((0.36, 0.8, 0.2), (0.5 - 0.55*w2, 1.0 + 0.04*w, 0.34)), eyes="side" if w2 > 0.5 else "open", head=(-0.03*w2, 0))
    if who == "igor":    # вытягивает рулетку
        return dict(pose=("down", "hold"), tape=0.04 + 0.32*w2, eyes="side" if w2 > 0.4 else "open", head=(0.02*w2, 0))
    if who == "lyuda":   # протягивает пирожки
        return dict(pose=((0.24, 0.96 + 0.06*w2, 0.36 + 0.18*w2), (0.24, 0.96 + 0.06*w2, 0.36 + 0.18*w2)), eyes="happy" if w2 > 0.5 else "open", head=(0, 0.02*w2))
    if who == "vitya":   # поднимает словарь, как гирю
        return dict(pose=("down", (0.56, 0.98 + 0.4*w2, 0.24)), face="o" if w2 > 0.7 else "smile", head=(0, 0.015*w2))

def act_frame(who, lang, i, size=360, n=NF):
    kw = act_kw(who, i/n); sc = Scene(); s = SCALE[who]
    base = Toy(sc, 0, 0, s); base.cyl(base.m("base", BASE[who]), (0, -0.07, 0), 0.66, 0.07, 0.035)
    T = Toy(sc, 0, 0, s, head=kw.pop("head", (0, 0))); T.tape = kw.pop("tape", 0.14)
    WHO[who](T, NICK[lang][who], **kw)
    img = draw(sc, size, size, (0, 0.96*s, 0), 1.26, yaw=0.32, pitch=0.2, bg=PAPER[who])
    return Image.fromarray((img*255).clip(0, 255).astype(np.uint8))

def act(who, lang, path, size=240, n=NF):
    frames = [act_frame(who, lang, i, size*3//2, n).resize((size, size), Image.LANCZOS) for i in range(n)]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=[110]*n, loop=0, quality=78, method=4)


# ---------- малыш рисует за столом ----------
def malysh_scene(lang, t, mode="draw"):
    """mode: draw — водит мелком по листу; joy — показывает рисунок, руки вверх."""
    sc = Scene(); s = 0.72; T = Toy(sc, 0, 0, s)
    yel, wood = (253, 216, 53), (170, 120, 70)
    w = math.sin(2*math.pi*t*2); w2 = math.sin(2*math.pi*t*3)
    if mode == "draw":
        pose = ((0.36, 0.86, 0.3), (0.18 + 0.12*w, 0.86 + 0.02*w2, 0.52 + 0.08*w2)); face, eyes = "smile", "side"; head = (0.01*w, -0.04)
    else:
        a = 0.08*math.sin(2*math.pi*t*2)
        pose = ((0.5 + a, 1.86, 0.06), (0.5 - a, 1.86, 0.06)); face, eyes = "big", "happy"; head = (0, 0.02)
    T.hy = head[1]*s; T.hx = head[0]*s
    hands = body(T, "m", yel, (108, 180, 224), (229, 57, 53), pose, face, eyes)
    T.inhead = True
    hair = T.m("mhair", (196, 110, 52))
    T.sphere(hair, (0, HC + 0.03, -0.02), HR + 0.012); T.above(1.62)
    T.cap(hair, (0, 1.76, 0.05), (0.06, 1.86, 0.08), 0.045); T.cap(hair, (0.06, 1.86, 0.08), (0.0, 1.9, 0.12), 0.035)   # хохолок
    T.inhead = False
    T.patch("mpatch", NICK[lang]["malysh"], (0, 0.93, 0.256), 0.17, 0.065)
    # стол, лист, мелки
    tb = T.m("table", wood)
    T.box(tb, (0, 0.72, 0.62), (0.62, 0.035, 0.3), 0.02)
    for sx in (-1, 1): T.box(tb, (sx*0.55, 0.35, 0.82), (0.035, 0.35, 0.035), 0.01)
    T.box(T.m("sheet", WHITE), (0.05, 0.765, 0.62), (0.3, 0.008, 0.22), 0.004)
    for k, col in enumerate(((229, 57, 53), (30, 136, 229), (67, 160, 71))):
        T.cap(T.m(f"crayon{k}", col), (-0.45 + k*0.07, 0.775, 0.5), (-0.42 + k*0.07, 0.775, 0.68), 0.022)
    if mode == "draw":
        h = hands[1]; T.cap(T.m("crayon0", (229, 57, 53)), (h[0], h[1] - 0.02, h[2] + 0.02), (h[0] + 0.03, h[1] - 0.12, h[2] + 0.1), 0.026)
        for k in range(4):   # каракули на листе
            T.cap(T.m("scrib", (229, 57, 53)), (-0.12 + k*0.07, 0.775, 0.55 + 0.05*(k % 2)), (-0.06 + k*0.07, 0.775, 0.68 - 0.05*(k % 2)), 0.008)
    else:
        T.box(T.m("sheet", WHITE), (0.0, 1.95, 0.25), (0.26, 0.2, 0.006), 0.004)    # поднял рисунок над головой
        for k in range(4): T.cap(T.m("scrib", (229, 57, 53)), (-0.15 + k*0.09, 1.85 + 0.08*(k % 2), 0.26), (-0.1 + k*0.09, 2.02 - 0.08*(k % 2), 0.26), 0.012)
    img = draw(sc, 360, 360, (0, 0.95*s + 0.1, 0.2), 1.0, yaw=0.38, pitch=0.42, bg=((250, 243, 226), (240, 228, 204)))
    return Image.fromarray((img*255).clip(0, 255).astype(np.uint8))

def malysh_clip(lang, mode, path, size=240, n=12):
    frames = [malysh_scene(lang, i/n, mode).resize((size, size), Image.LANCZOS) for i in range(n)]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=[110]*n, loop=0, quality=78, method=4)

def malysh_head(lang, path):
    sc = Scene(); s = 0.72; T = Toy(sc, 0, 0, s)
    body(T, "m", (253, 216, 53), (108, 180, 224), (229, 57, 53), ("down", "down"))
    T.inhead = True; hair = T.m("mhair", (196, 110, 52))
    T.sphere(hair, (0, HC + 0.03, -0.02), HR + 0.012); T.above(1.62)
    T.cap(hair, (0, 1.76, 0.05), (0.06, 1.86, 0.08), 0.045); T.inhead = False
    img = draw(sc, 320, 320, (0, 1.5*s, 0), 0.47*s, yaw=0.12, pitch=0.1, bg=((250, 243, 226), (240, 228, 204)))
    Image.fromarray((img*255).clip(0, 255).astype(np.uint8)).resize((160, 160), Image.LANCZOS).save(path, quality=84)
