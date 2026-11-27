# Семья на диване — шесть комментаторов словарного тренажёра (портреты и эмоции)
# Ники на одежде: LANG = "ru" или "uk" (python3 render.py family out ... ; LANG берётся из переменной окружения FAMLANG)
import os
from kid import *

LANG = os.environ.get("FAMLANG", "ru")
NICK = {
    "ru": dict(danya="Тиктокер", nika="Тиктокерша", irina="Душнила", igor="Душнила", lyuda="Динозавр", vitya="Динозавр"),
    "uk": dict(danya="Тіктокер", nika="Тіктокерка", irina="Душнила", igor="Душнила", lyuda="Динозавр", vitya="Динозавр"),
}[LANG]

G = 196
FILT = '<g filter="url(#cr)" fill="none" stroke-linecap="round" stroke-linejoin="round">'

def geo(x, y, s):
    L, B, r = 30*s, 36*s, 13*s
    hip = y - L; yb = y - L - B; hy = yb - r + 2*s
    return hip, yb, hy, r

def label(x, y, t, size, c=INK, width=None):
    if width: size = min(size, width/(0.43*len(t)))
    return (f'</g><text x="{x:.1f}" y="{y+size*0.32:.1f}" font-family="Caveat" font-weight="700" font-size="{size:.1f}" '
            f'fill="{c}" text-anchor="middle">{t}</text>' + FILT)

def patch(x, y, w, h, t, s, c=WHITE, tc=INK, rx=2):
    """Принт / бейдж с ником (по центру x, верх y)."""
    return (f'<rect x="{x-w/2*s:.1f}" y="{y:.1f}" width="{w*s:.1f}" height="{h*s:.1f}" rx="{rx*s:.1f}" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
            + label(x, y+h*s/2, t, h*s*0.8, tc, width=(w-1.5)*s))

def panel(x, yb, s, w, c, text, size, tc=INK, top=4, h=16):
    """Светлая футболка под кофтой/рубашкой + ник."""
    o = f'<rect x="{x-w/2*s:.1f}" y="{yb+top*s:.1f}" width="{w*s:.1f}" height="{h*s:.1f}" fill="{c}" stroke="none"/>'
    return o + label(x, yb+(top+h*0.5)*s, text, size*s, tc, width=(w-1.5)*s)

def slippers(x, y, s, c, socks=False):
    o = ""
    for sd in (-1, 1):
        fx = x + sd*6*s
        if socks:
            o += P(f"M{fx:.1f} {y-6*s:.1f} L{fx:.1f} {y-1*s:.1f}", WHITE, 5*s) + P(f"M{fx-2.5*s:.1f} {y-6*s:.1f} h{5*s:.1f}", C["lgrey"], 1.2)
        o += P(f"M{fx-6*s if sd < 0 else fx-2*s:.1f} {y+1:.1f} h{8*s:.1f}", c, 4.2*s)
    return o

# ---------------- Даня, 17 ----------------
def danya(x, y=G, s=1.92, face="smile", arms=("down", "low"), eyes="open", hands=(None, None), chips=True, **kw):
    hip, yb, hy, r = geo(x, y, s)
    o = [fillc(x, hy+1*s, r+4.5*s, C["lgreen"], ow=2.4)]                   # капюшон
    o.append(person(x, y, s, body="shirt", c=C["lgreen"], c2=C["dgrey"], hair=("short", C["hbrown"]),
                    arms=arms, face=face, eyes=eyes, hands=hands, **kw))
    # чёлка на глаза
    o.append(solid(f"M{x-r+1:.1f} {hy-6*s:.1f} Q{x-2*s:.1f} {hy-r-2*s:.1f} {x+r-1:.1f} {hy-7*s:.1f} L{x+2*s:.1f} {hy+1*s:.1f} L{x-1*s:.1f} {hy-4*s:.1f} L{x-5*s:.1f} {hy-0.5*s:.1f} Z", C["hbrown"]))
    # шнурки худи и наушники на шее
    o.append(P(f"M{x-3*s:.1f} {yb+1*s:.1f} v{9*s:.1f} M{x+3*s:.1f} {yb+1*s:.1f} v{9*s:.1f}", WHITE, 1.4))
    o.append(P(f"M{x-10*s:.1f} {yb+2*s:.1f} Q{x:.1f} {yb+9*s:.1f} {x+10*s:.1f} {yb+2*s:.1f}", C["night"], 2.6*s))
    o.append(fillc(x-10*s, yb+2.5*s, 3.6*s, C["red"], ow=2) + fillc(x+10*s, yb+2.5*s, 3.6*s, C["red"], ow=2))
    o.append(patch(x, yb+13*s, 19, 8, NICK["danya"], s))
    o.append(slippers(x, y, s, C["navy"], socks=True))
    if chips:  # пачка чипсов в правой руке
        ax, ay = ARM[arms[1]] if isinstance(arms[1], str) else arms[1]
        hx, hy2 = x+10*s+ax*s, yb+7*s+ay*s
        o.append(fillrect(round(hx-1*s, 1), round(hy2-12*s, 1), round(11*s, 1), round(14*s, 1), C["amber"], ow=2.2))
        o.append(P(f"M{hx-1*s:.1f} {hy2-12*s:.1f} l2 -2 l2 2 l2 -2 l2 2 l2 -2", INK, 1.6))
        o.append(smiley(hx+4.5*s, hy2-4*s, 2.6*s, C["red"]))
    return "".join(o)

# ---------------- Ника, 16 ----------------
def nika(x, y=G, s=1.8, face="smile", arms=("down", "hi"), eyes="open", hands=(None, "dot"), phone=True, **kw):
    hip, yb, hy, r = geo(x, y, s)
    o = []
    # хвост-«пальма» на макушке
    tx, ty = x+1*s, hy-r-1*s
    o.append(P(f"M{tx:.1f} {ty:.1f} v{-8*s:.1f}", C["black"], 4.4*s))
    for dx, dy in ((-13, 2), (-10, -8), (-3, -14), (4, -14), (11, -8), (13, 2)):
        o.append(P(f"M{tx:.1f} {ty-8*s:.1f} Q{tx+dx*s*.4:.1f} {ty-8*s+dy*s*.9:.1f} {tx+dx*s:.1f} {ty-8*s+dy*s*.2+4*s:.1f}", C["black"], 2.8*s))
    o.append(fillc(tx, ty-6*s, 4*s, C["rasp"], ow=2))              # огромная резинка
    # худи оверсайз — шире туловища
    o.append(fillrect(round(x-15*s, 1), round(yb, 1), round(30*s, 1), round(30*s, 1), C["emerald"], ow=2.8))
    o.append(person(x, y, s, body="shirt", c=C["emerald"], c2=C["black"], hair=("short", C["black"]),
                    arms=arms, face=face, eyes=eyes, hands=hands, **kw))
    o.append(P(f"M{x-15*s:.1f} {yb+30*s:.1f} h{30*s:.1f}", C["teal"], 3*s))  # резинка худи
    o.append(patch(x, yb+9*s, 25, 8, NICK["nika"], s))
    for sd in (-1, 1):  # массивные кроссовки
        o.append(f'<rect x="{x+sd*6*s-(7*s if sd < 0 else 1*s):.1f}" y="{y-3*s:.1f}" width="{8*s:.1f}" height="{5*s:.1f}" rx="2" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>')
    if phone:  # телефон с кольцевой лампой в правой руке
        ax, ay = ARM[arms[1]] if isinstance(arms[1], str) else arms[1]
        hx, hy2 = x+10*s+ax*s, yb+7*s+ay*s
        o.append(circ(hx+2*s, hy2-9*s, 9*s, C["lemon"], 3.4*s))
        o.append(circ(hx+2*s, hy2-9*s, 11*s, C["yellow"], 1.2))
        o.append(mobile(hx+2*s, hy2-9*s, C["night"], 0.55*s))
        o.append(P(f"M{hx:.1f} {hy2:.1f} L{hx+2*s:.1f} {hy2-3*s:.1f}", INK, 2))
    return "".join(o)

# ---------------- Ирина, 39 ----------------
def irina(x, y=G, s=1.85, face="smile", arms=("chest", "fwd"), eyes="open", hands=(None, None), marker=True, **kw):
    hip, yb, hy, r = geo(x, y, s)
    o = []
    # каре: пряди до подбородка
    for sd in (-1, 1):
        o.append(fillrect(round(x+sd*(r-1*s)-(5*s if sd < 0 else 0), 1), round(hy-6*s, 1), round(5*s, 1), round(15*s, 1), C["dbrown"], ow=0.01, outline=False))
    o.append(person(x, y, s, body="shirt", c=C["navy"], c2=C["night"], hair=("short", C["dbrown"]),
                    arms=arms, face=face, eyes=eyes, hands=hands, **kw))
    # ровная чёлка
    o.append(solid(f"M{x-r+1:.1f} {hy-5*s:.1f} Q{x:.1f} {hy-r-4*s:.1f} {x+r-1:.1f} {hy-5*s:.1f} Z", C["dbrown"]))
    # очки подняты на голову
    o.append(circ(x-4.6*s, hy-r+1*s, 3.4*s, INK, 1.6, C["ice"])); o.append(circ(x+4.6*s, hy-r+1*s, 3.4*s, INK, 1.6, C["ice"]))
    o.append(P(f"M{x-1.2*s:.1f} {hy-r+1*s:.1f} h{2.4*s:.1f}", INK, 1.4))
    # белая футболка между лацканами жакета + ник
    o.append(panel(x, yb, s, 17, WHITE, NICK["irina"], 8, top=3, h=17))
    o.append(P(f"M{x-8.5*s:.1f} {yb:.1f} L{x-5*s:.1f} {yb+22*s:.1f} M{x+8.5*s:.1f} {yb:.1f} L{x+5*s:.1f} {yb+22*s:.1f}", C["navy"], 2.2*s))
    o.append(fillrect(round(x-1.5*s, 1), round(yb+24*s, 1), round(3*s, 1), round(3*s, 1), C["amber"], ow=1.4))  # пуговица
    # папка с цветными закладками под левой рукой
    o.append(fillrect(round(x-26*s, 1), round(yb+12*s, 1), round(12*s, 1), round(17*s, 1), C["sky"], ow=2.2))
    for k, cc in enumerate((C["red"], C["yellow"], C["green"], C["rasp"])):
        o.append(P(f"M{x-14*s:.1f} {yb+(14+k*4)*s:.1f} h{3*s:.1f}", cc, 2.4))
    o.append(slippers(x, y, s, C["dbrown"]))
    if marker:
        ax, ay = ARM[arms[1]] if isinstance(arms[1], str) else arms[1]
        hx, hy2 = x+10*s+ax*s, yb+7*s+ay*s
        o.append(f'<rect x="{hx-1.5*s:.1f}" y="{hy2-14*s:.1f}" width="{4*s:.1f}" height="{13*s:.1f}" rx="1" fill="{C["yellow"]}" stroke="{INK}" stroke-width="1.8" transform="rotate(14 {hx:.1f} {hy2:.1f})"/>')
    return "".join(o)

# ---------------- Игорь, 45 ----------------
def igor(x, y=G, s=2.0, face="smile", arms=("down", "fwd"), eyes="open", hands=(None, None), tape=True, **kw):
    hip, yb, hy, r = geo(x, y, s)
    o = [person(x, y, s, body="shirt", c=C["red"], c2=C["dgrey"], hair=None,
                arms=arms, face=face, eyes=eyes, hands=hands, **kw)]
    # ёжик с проседью: короткие штрихи по макушке
    for a in range(200, 341, 10):
        aa = math.radians(a)
        bx, by = x+math.cos(aa)*(r-1*s), hy+math.sin(aa)*(r-1*s)
        o.append(P(f"M{bx:.1f} {by:.1f} l{math.cos(aa)*4*s:.1f} {math.sin(aa)*4*s:.1f}", C["dgrey"] if a % 20 else C["lgrey"], 2.2*s))
    # клетка рубашки
    for k in range(1, 6):
        o.append(P(f"M{x-11*s:.1f} {yb+k*6*s:.1f} h{22*s:.1f}", C["navy"], 2.6*s))
    for k in (-7, -2, 3, 8):
        o.append(P(f"M{x+k*s:.1f} {yb:.1f} v{36*s:.1f}", C["navy"], 2.2*s))
    # офисный бейдж на шнурке с ником
    o.append(P(f"M{x-5*s:.1f} {yb+1*s:.1f} L{x-2*s:.1f} {yb+15*s:.1f} M{x+5*s:.1f} {yb+1*s:.1f} L{x+2*s:.1f} {yb+15*s:.1f}", C["blue"], 1.8*s))
    o.append(patch(x, yb+15*s, 19, 9, NICK["igor"], s, rx=1))
    # ёжик с проседью, густые брови, щетина
    o.append(P(f"M{x-8*s:.1f} {hy-6*s:.1f} l{6*s:.1f} {1*s:.1f} M{x+8*s:.1f} {hy-6*s:.1f} l{-6*s:.1f} {1*s:.1f}", INK, 3.2*s))
    for k in range(9):
        o.append(dot(x-6*s+k*1.5*s+j(.4), hy+9*s+j(.8), .55*s, C["dgrey"]))
    # сандалии с носками? нет — кроссовки «папины»
    o.append(slippers(x, y, s, C["grey"]))
    if tape:  # рулетка
        ax, ay = ARM[arms[1]] if isinstance(arms[1], str) else arms[1]
        hx, hy2 = x+10*s+ax*s, yb+7*s+ay*s
        o.append(fillrect(round(hx-2*s, 1), round(hy2-7*s, 1), round(10*s, 1), round(10*s, 1), C["yellow"], ow=2.2))
        o.append(dot(hx+3*s, hy2-2*s, 1.8*s, INK))
        o.append(P(f"M{hx+8*s:.1f} {hy2+1*s:.1f} h{14*s:.1f}", C["amber"], 2.6*s))
        for k in range(5):
            o.append(P(f"M{hx+(10+k*2.6)*s:.1f} {hy2:.1f} v{1.6*s:.1f}", INK, 1))
    return "".join(o)

# ---------------- Людмила Ивановна, 69 ----------------
def lyuda(x, y=G, s=1.8, face="smile", arms=("fwd", "fwd"), eyes="open", hands=(None, None), plate=True, **kw):
    hip, yb, hy, r = geo(x, y, s)
    o = []
    o.append(person(x, y, s, body="topskirt", c=C["coral"], c2=C["brown"], hair=None,
                    arms=arms, face=face, eyes=eyes, hands=hands, glasses=True, **kw))
    # укладка «облачком» с лавандовым оттенком
    for a in range(170, 375, 17):
        aa = math.radians(a)
        o.append(dot(x+math.cos(aa)*r*1.05, hy+math.sin(aa)*r*1.0-2*s, 5.6*s, C["pgrey"] if a % 2 else C["lavender"]))
    for k in range(-2, 3):
        o.append(dot(x+k*4.5*s, hy-r-4*s+abs(k)*1.5*s, 4.8*s, C["lavender"] if k % 2 else C["pgrey"]))
    o.append(face_(x, hy, s, face, eyes))
    o.append(circ(x-4.6*s, hy-1*s, 3.6*s, INK, 1.4)); o.append(circ(x+4.6*s, hy-1*s, 3.6*s, INK, 1.4))
    o.append(P(f"M{x-8.2*s:.1f} {hy-1*s:.1f} Q{x-12*s:.1f} {hy+8*s:.1f} {x-7*s:.1f} {yb+4*s:.1f}", C["amber"], 1.1))  # шнурок очков
    if face not in ("sad", "frown"):
        o.append(f'<g opacity="0.85">{dot(x-8*s, hy+4*s, 2.2*s, CHEEK)}{dot(x+8*s, hy+4*s, 2.2*s, CHEEK)}</g>')
    # крупные бусы
    for k in range(7):
        t = k/6
        o.append(dot(x-8*s+16*s*t, yb+3*s+5*s*math.sin(math.pi*t), 1.9*s, [C["amber"], WHITE, C["red"]][k % 3]))
    # фартук в горошек с ником
    ax0, ay0 = x-12*s, yb+14*s
    o.append(f'<rect x="{ax0:.1f}" y="{ay0:.1f}" width="{24*s:.1f}" height="{36*s:.1f}" rx="3" fill="{WHITE}" stroke="{INK}" stroke-width="2.2"/>')
    for k in range(10):
        o.append(dot(ax0+(3+(k*7) % 21)*s, ay0+(16+(k//3)*6)*s, 1.2*s, C["red"]))
    o.append(label(x, ay0+8*s, NICK["lyuda"], 9*s, width=22*s))
    o.append(slippers(x, y, s, C["rasp"]))
    if plate:  # тарелка пирожков в руках
        px, py = x, yb+12*s
        o.append(f'<ellipse cx="{px+30*s:.1f}" cy="{py+1*s:.1f}" rx="{13*s:.1f}" ry="{3.5*s:.1f}" fill="{WHITE}" stroke="{C["sky"]}" stroke-width="2"/>')
        for dx in (-7, 0, 7):
            o.append(fillc(px+30*s+dx*s, py-2*s, 3.6*s, C["ochre"], ow=1.8))
        o.append(P(f"M{px+24*s:.1f} {py-10*s:.1f} q-2 -4 0 -7 M{px+33*s:.1f} {py-10*s:.1f} q-2 -4 0 -7", C["grey"], 1.6))
    return "".join(o)

# ---------------- Виктор Петрович, 68 ----------------
def vitya(x, y=G, s=1.9, face="smile", arms=("chest", "fwd"), eyes="open", hands=(None, None), book=True, scarf=True, **kw):
    hip, yb, hy, r = geo(x, y, s)
    o = [person(x, y, s, body="shirt", c=C["ochre"], c2=C["brown"], hair=("bald", C["pgrey"]),
                arms=arms, face=face, eyes=eyes, hands=hands, **kw)]
    # волосы торчком по бокам
    for sd in (-1, 1):
        for k, (dx, dy) in enumerate(((4, -8), (7, -3), (7, 3), (5, 8))):
            o.append(P(f"M{x+sd*(r-2*s):.1f} {hy-3*s+k*3*s:.1f} l{sd*dx*s:.1f} {dy*s*.6-3*s:.1f}", C["lgrey"], 2.6*s))
    o.append(P(f"M{x-3*s:.1f} {hy-r:.1f} l-1 {-5*s:.1f} M{x+2*s:.1f} {hy-r:.1f} l2 {-6*s:.1f}", C["lgrey"], 2.2*s))
    # пышные усы
    o.append(solid(f"M{x:.1f} {hy+3*s:.1f} Q{x-6*s:.1f} {hy+1*s:.1f} {x-10*s:.1f} {hy+7*s:.1f} Q{x-5*s:.1f} {hy+6*s:.1f} {x:.1f} {hy+6*s:.1f} Q{x+5*s:.1f} {hy+6*s:.1f} {x+10*s:.1f} {hy+7*s:.1f} Q{x+6*s:.1f} {hy+1*s:.1f} {x:.1f} {hy+3*s:.1f} Z", C["lgrey"]))
    # белая футболка в вырезе жилетки + ник
    o.append(panel(x, yb, s, 17, WHITE, NICK["vitya"], 8, top=7, h=13))
    o.append(P(f"M{x-8.5*s:.1f} {yb+7*s:.1f} v{29*s:.1f} M{x+8.5*s:.1f} {yb+7*s:.1f} v{29*s:.1f}", C["brown"], 1.4))
    for k in range(3):
        o.append(dot(x-9*s, yb+(26+k*4)*s, 1*s, C["brown"]))
    # шарф футбольного клуба
    if scarf:
        for k in range(5):
            cc = C["green"] if k % 2 == 0 else WHITE
            o.append(P(f"M{x-11*s+k*5.5*s:.1f} {yb-1*s:.1f} l{3*s:.1f} {6*s:.1f}", cc, 4*s))
        for k in range(4):
            cc = C["green"] if k % 2 == 0 else WHITE
            o.append(P(f"M{x-13.5*s:.1f} {yb+(2+k*4)*s:.1f} v{4*s:.1f}", cc, 4.6*s))
        o.append(P(f"M{x-15*s:.1f} {yb+18*s:.1f} l-1 3 M{x-13.5*s:.1f} {yb+18*s:.1f} v3 M{x-12*s:.1f} {yb+18*s:.1f} l1 3", C["green"], 1.2))
    o.append(slippers(x, y, s, C["brown"]))
    if book:  # толстый старый словарь
        ax, ay = ARM[arms[1]] if isinstance(arms[1], str) else arms[1]
        hx, hy2 = x+10*s+ax*s, yb+7*s+ay*s
        o.append(fillrect(round(hx-2*s, 1), round(hy2-15*s, 1), round(12*s, 1), round(16*s, 1), C["dred"], ow=2.4))
        o.append(P(f"M{hx+10*s:.1f} {hy2-15*s:.1f} v{16*s:.1f}", C["pgrey"], 2.4*s))
        o.append(P(f"M{hx:.1f} {hy2-11*s:.1f} h{8*s:.1f} M{hx:.1f} {hy2-3*s:.1f} h{8*s:.1f}", C["amber"], 1.4))
    return "".join(o)

WHO = dict(danya=danya, nika=nika, irina=irina, igor=igor, lyuda=lyuda, vitya=vitya)
PAP = dict(danya="mint", nika="pink", irina="blue", igor="grey", lyuda="peach", vitya="yellow")

# ---------- эмоции ----------
FACEPALM = (-7, -18)   # правая рука к лицу
def emo(who, kind, x=100):
    f = WHO[who]
    import inspect; sc = inspect.signature(f).parameters["s"].default
    hip, yb, hy, r = geo(x, G, sc)
    if kind == "joy":
        return f(x, face="big", eyes="happy", arms=("up", "up"), hands=("spikes", "spikes"), **_noprops(who)) \
            + sparkle(30, 40) + sparkle(170, 50, C["rasp"]) + sparkle(160, 120, C["blue"], 4)
    if kind == "facepalm":
        return f(x, face="line", eyes="closed", arms=("down", FACEPALM), hands=(None, "dot"), **_noprops(who)) \
            + dot(x+3*sc, hy, 5.5*sc, C["skin2"]) + P(f"M{x+16} {hy-26} q4 6 0 10", C["sky"], 3)
    if kind == "wow":
        return f(x, face="o", arms=("up", "up"), hands=("spikes", "spikes"), **_noprops(who)) \
            + excl(32, 60, C["red"], 1.6) + excl(168, 60, C["red"], 1.6)
    if kind == "told":  # «ну я же говорил(а)»: палец вверх, хитрая мина
        fx, fy = x+10*sc+15*sc, yb+7*sc-30*sc          # кисть поднятой руки
        return f(x, face="meh", eyes="side", arms=("hip", "up"), hands=(None, "dot"), **_noprops(who)) \
            + P(f"M{fx:.1f} {fy:.1f} l{1*sc:.1f} {-7*sc:.1f}", INK, 3*sc) \
            + bubble(8, 10, 54, 30, 40, 58, excl(27, 26, C["amber"], 1.1) + excl(41, 26, C["amber"], 1.1))
    raise KeyError(kind)

def _noprops(who):
    return {"danya": dict(chips=False), "nika": dict(phone=False), "irina": dict(marker=False),
            "igor": dict(tape=False), "lyuda": dict(plate=False), "vitya": dict(book=False)}[who]

SC = {}
for w, f in WHO.items():
    SC[w] = (PAP[w], (lambda f=f: f(100) + grass(G+4, C["lgreen"])))
for w in WHO:
    for k in ("joy", "facepalm", "wow", "told"):
        SC[f"{w}_{k}"] = (PAP[w], (lambda w=w, k=k: emo(w, k)))


# ---------- общая сцена «вечер у телевизора» (холст 360×200) ----------
def tv(x, y):
    o = [fillrect(x-4, y+50, 70, 44, C["wood"], ow=2.8)]                         # тумба
    o.append(P(f"M{x+31} {y+50} v44", INK, 2) + dot(x+25, y+72, 1.6) + dot(x+37, y+72, 1.6))
    o.append(f'<rect x="{x}" y="{y}" width="62" height="50" rx="7" fill="{C["tan"]}" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<rect x="{x+5}" y="{y+5}" width="42" height="40" rx="6" fill="{C["ice"]}" stroke="{INK}" stroke-width="2.4"/>')
    o.append(dot(x+55, y+14, 2.6, C["dred"]) + dot(x+55, y+25, 2.6, C["dred"]))
    o.append(P(f"M{x+24} {y} l-12 -18 M{x+38} {y} l10 -20", INK, 2.2))
    # на экране: мяч и ворота (футбол)
    o.append(P(f"M{x+10} {y+38} h32", C["green"], 3) + P(f"M{x+12} {y+36} v-16 h12 v16", WHITE, 2) + circ(x+34, y+30, 4, INK, 1.6, WHITE))
    return "".join(o)

LIGHT = {C["sky"]: "#cfe4f2", C["olive"]: "#d3dcb6"}
def block(x, y, w, h, c):
    """Непрозрачный предмет мебели: светлая заливка + штриховка мелком."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{LIGHT.get(c, WHITE)}"/>' + fillrect(x, y, w, h, c, ow=3))

def armchair(x, y, c=C["olive"]):
    return (fillrect(x-26, y-62, 52, 40, c, ow=3) + fillrect(x-32, y-36, 12, 36, c, ow=3)
            + fillrect(x+20, y-36, 12, 36, c, ow=3) + P(f"M{x-28} {y} v6 M{x+28} {y} v6", C["wood"], 4))

def scene():
    F = 188
    o = [scribble(f"M0 {F} H360 V200 H0 Z", (0, F, 360, 200), C["sand"], outline=False, w=3, step=4)]
    o.append(f'<ellipse cx="160" cy="{F+5}" rx="120" ry="7" fill="{C["lav"] if "lav" in C else C["lavender"]}" opacity=".5"/>')
    o.append(P("M20 30 h40 v30 h-40 Z", C["wood"], 3) + sun(40, 45, 6, face=False, rays=6))   # картина на стене
    o.append(tv(286, 92))
    # дедушка в кресле кричит на футбол
    o.append(block(12, 102, 52, 40, C["olive"]))
    o.append(vitya(38, 176, 0.82, face="big", arms=("chest", "up"), hands=(None, "spikes"), book=False))
    o.append(block(16, 156, 44, 32, C["olive"]) + block(8, 146, 12, 42, C["olive"]) + block(56, 146, 12, 42, C["olive"]))
    # диван: спинка, родители, сиденье
    o.append(block(112, 112, 130, 46, C["sky"]))
    o.append(irina(150, 176, 0.82, arms=("chest", "fwd")))
    o.append(igor(200, 176, 0.86, face="big", arms=("down", "point"), tape=False))
    o.append(block(110, 152, 134, 30, C["sky"]) + block(100, 132, 14, 50, C["sky"]) + block(240, 132, 14, 50, C["sky"]))
    o.append(P("M114 182 v6 M240 182 v6", C["wood"], 4))
    # Ника на подлокотнике снимает всех
    o.append(nika(247, 134, 0.72, arms=("down", (26, -16)), face="big", eyes="happy"))
    # Даня на кресле-мешке перед диваном
    o.append(danya(92, 190, 0.8, arms=("low", "fwd")))
    o.append(solid("M66 190 Q64 160 92 158 Q122 160 118 190 Z", "#f6c48f") + scribble("M66 190 Q64 160 92 158 Q122 160 118 190 Z", (64, 156, 122, 190), C["orange"], ow=3))
    # бабушка с пирожками заслоняет телевизор
    o.append(lyuda(318, 190, 0.86, arms=("fwd", "fwd")))
    return "".join(o)
