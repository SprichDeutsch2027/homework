# Библиотека детских рисунков мелками для Wortreise (SVG 200x200)
import math, random

INK = "#3a2a20"; SKIN = "#fbe9d7"; CHEEK = "#f29bb0"; WHITE = "#fbf8f2"
BOX = dict(  # коробка мелков
    red="#e53935", dred="#b71c1c", coral="#e8604c", pink="#f48fb1", rasp="#e2669a", cherry="#ad1457",
    dorange="#e65100", orange="#fb8c00", amber="#f5a623", yellow="#fdd835", lemon="#fff176", ochre="#e0a83a",
    dgreen="#1b5e20", green="#43a047", lgreen="#8bc34a", mint="#c5e1a5", olive="#6b8e23", emerald="#26a69a",
    navy="#0d47a1", blue="#1e88e5", sky="#6cb4e0", ice="#b3e5fc", teal="#2f8f8a", night="#26375a",
    dviolet="#4a148c", violet="#7d5ba6", purple="#9b6bd0", lilac="#ce93d8", lavender="#b39ddb", plum="#8e244d",
    dbrown="#3e2723", brown="#6d4c41", wood="#8a5a2b", tan="#c8a27a", sand="#d7a86e", taupe="#a1887f",
    skin=SKIN, skin2="#f1c9a5", skin3="#d9a066", hbrown="#5d3a1a", copper="#c0602a", black="#1f1d1a",
    grey="#8a8379", dgrey="#5e584f", lgrey="#bdb6ab", pgrey="#e8e1d4", white=WHITE)
C = BOX
PAPER = dict(cream="#f4eedf", blue="#dde7ec", peach="#f8e6d4", mint="#e3f1ea", lav="#ebe5f2",
             yellow="#fbf1cf", white="#fbf8f2", night="#26375a", dusk="#f3dccb", grey="#e9e5de", pink="#f8e4e8")

_id = [0]
def uid(p="c"):
    _id[0] += 1
    return f"{p}{_id[0]}"

R = random.Random(1)
def seed(s): R.seed(s)
def j(a=1.0): return R.uniform(-a, a)

def P(d, c=INK, w=3, fill="none", extra=""):
    return f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="{fill}" {extra}/>'
def circ(x, y, r, c=INK, w=3, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" stroke="{c}" stroke-width="{w}" fill="{fill}"/>'
def dot(x, y, r, c=INK): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c}" stroke="none"/>'
def cpath(x, y, r):
    return f"M{x-r:.1f} {y:.1f} a{r:.1f} {r:.1f} 0 1 0 {2*r:.1f} 0 a{r:.1f} {r:.1f} 0 1 0 {-2*r:.1f} 0 Z"

def scribble(d, box, c, w=2.3, step=3.4, outline=True, ow=3, vertical=True):
    """Заштриховать фигуру d зигзагом (как мелком)."""
    x0, y0, x1, y1 = box
    i = uid("k")
    pts = []
    if vertical:
        x = x0 - 2; top = True
        while x <= x1 + 2:
            pts.append(f"{x+j(.6):.1f} {(y0-2 if top else y1+2)+j(1.5):.1f}"); x += step; top = not top
    else:
        y = y0 - 2; left = True
        while y <= y1 + 2:
            pts.append(f"{(x0-2 if left else x1+2)+j(1.5):.1f} {y+j(.6):.1f}"); y += step; left = not left
    z = "M" + " L".join(pts)
    s = f'<clipPath id="{i}"><path d="{d}"/></clipPath><g clip-path="url(#{i})">{P(z, c, w)}</g>'
    if outline: s += P(d, c, ow)
    return s

def fillc(x, y, r, c, w=2.3, ow=3, outline=True):
    return scribble(cpath(x, y, r), (x-r, y-r, x+r, y+r), c, w, outline=outline, ow=ow)
def fillrect(x, y, w_, h, c, sw=2.3, ow=3, outline=True, vertical=True):
    d = f"M{x} {y} h{w_} v{h} h{-w_} Z"
    return scribble(d, (x, y, x+w_, y+h), c, sw, outline=outline, ow=ow, vertical=vertical)
def solid(d, c): return f'<path d="{d}" fill="{c}" stroke="{c}" stroke-width="2"/>'

# ---------- человечек ----------
ARM = dict(down=(20, 26), wave=(18, -24), up=(15, -30), out=(28, -2), fwd=(26, 8), low=(24, 18),
           give=(26, 4), point=(30, -4), hi=(22, -14))

def hand(x, y, kind, c=INK, s=1.0, side=1):
    if kind == "spikes":
        out = ""
        for a in (-150, -110, -70, -30, 10):
            aa = math.radians(a if side > 0 else 180 - a)
            out += P(f"M{x:.1f} {y:.1f} l{math.cos(aa)*7*s:.1f} {math.sin(aa)*7*s:.1f}", c, 2.6*s)
        return out
    return dot(x, y, 2.6*s, c)

def person(x, y, s=1.0, body="shirt", c=C["teal"], c2=C["navy"], hair=("short", C["hbrown"]), skin=SKIN,
           arms=("down", "down"), face="smile", glasses=False, shawl=None, hat=None, tie=None,
           hands=(None, None), handc=(INK, INK), beard=None, cane=False, bag=None, eyes="open", blush=True):
    L, B, r = 30*s, 36*s, 13*s
    hip = y - L; yb = y - L - B; hy = yb - r + 2*s
    o = []
    # ноги
    if body in ("shirt",):
        o.append(P(f"M{x-5*s:.1f} {hip:.1f} L{x-6*s:.1f} {y:.1f}", c2, 6*s))
        o.append(P(f"M{x+5*s:.1f} {hip:.1f} L{x+6*s:.1f} {y:.1f}", c2, 6*s))
        o.append(P(f"M{x-6*s:.1f} {y:.1f} l-6 1 M{x+6*s:.1f} {y:.1f} l6 1", INK, 3*s))
    else:
        o.append(P(f"M{x-5*s:.1f} {hip:.1f} L{x-6*s:.1f} {y:.1f} l-6 1 M{x+5*s:.1f} {hip:.1f} L{x+6*s:.1f} {y:.1f} l6 1", INK, 3*s))
    if cane:
        o.append(P(f"M{x+24*s:.1f} {yb+26*s:.1f} L{x+26*s:.1f} {y:.1f} M{x+24*s:.1f} {yb+26*s:.1f} q4 -6 8 0", C["wood"], 3.4*s))
    # туловище
    if body == "dress":
        d = f"M{x:.1f} {yb:.1f} L{x-16*s:.1f} {hip:.1f} L{x+16*s:.1f} {hip:.1f} Z"
        o.append(scribble(d, (x-16*s, yb, x+16*s, hip), c))
    elif body == "topskirt":
        d1 = f"M{x-10*s:.1f} {yb:.1f} h{20*s:.1f} v{B*.5:.1f} h{-20*s:.1f} Z"
        d2 = f"M{x-10*s:.1f} {yb+B*.5:.1f} h{20*s:.1f} L{x+15*s:.1f} {hip:.1f} L{x-15*s:.1f} {hip:.1f} Z"
        o.append(scribble(d2, (x-15*s, yb+B*.5, x+15*s, hip), c2))
        o.append(scribble(d1, (x-10*s, yb, x+10*s, yb+B*.5), c))
    else:
        d = f"M{x-11*s:.1f} {yb:.1f} h{22*s:.1f} v{B:.1f} h{-22*s:.1f} Z"
        o.append(scribble(d, (x-11*s, yb, x+11*s, hip), c))
        if body == "suit":
            pass
    if tie:
        o.append(solid(f"M{x:.1f} {yb+1:.1f} l-3 4 l3 14 l3 -14 Z", tie))
    if shawl:
        cols = shawl
        for k, cc in enumerate(cols):
            dy = (4 + k*4)*s
            o.append(P(f"M{x-12*s:.1f} {yb+dy-4*s:.1f} Q{x:.1f} {yb+dy+10*s:.1f} {x+12*s:.1f} {yb+dy-4*s:.1f}", cc, 3.4*s))
        o.append(P(f"M{x-2*s:.1f} {yb+18*s:.1f} l-2 6 M{x+2*s:.1f} {yb+18*s:.1f} l2 6", cols[0], 1.8*s))
    # руки
    for side, a, hk, hc in ((-1, arms[0], hands[0], handc[0]), (1, arms[1], hands[1], handc[1])):
        sx, sy = x + side*10*s, yb + 7*s
        if a == "hip":
            o.append(P(f"M{sx:.1f} {sy:.1f} L{sx+side*9*s:.1f} {sy+11*s:.1f} L{sx+side*1*s:.1f} {sy+21*s:.1f}", INK, 3*s)); continue
        if a == "chest":
            ex, ey = x - side*1*s, yb + 14*s
            o.append(P(f"M{sx:.1f} {sy:.1f} Q{sx+side*8*s:.1f} {sy+12*s:.1f} {ex:.1f} {ey:.1f}", INK, 3*s)); o.append(dot(ex, ey, 2.6*s, hc)); continue
        if a == "none": continue
        if isinstance(a, tuple): dx, dy = a
        else: dx, dy = ARM[a]
        ex, ey = sx + side*dx*s, sy + dy*s
        o.append(P(f"M{sx:.1f} {sy:.1f} L{ex:.1f} {ey:.1f}", INK, 3*s))
        k = hk or ("spikes" if a in ("wave", "up", "hi") else "dot")
        o.append(hand(ex, ey, k, hc, s, side))
    if bag:
        o.append(fillrect(x+16*s, yb+22*s, 12*s, 10*s, bag, ow=2.4))
        o.append(P(f"M{x+18*s:.1f} {yb+22*s:.1f} q4 -6 8 0", INK, 2))
    # голова
    hair_t, hair_c = hair if hair else (None, None)
    if hair_t == "long":
        o.append(P(f"M{x-r:.1f} {hy:.1f} Q{x-r-3*s:.1f} {hy+14*s:.1f} {x-r+1:.1f} {hy+20*s:.1f} M{x+r:.1f} {hy:.1f} Q{x+r+3*s:.1f} {hy+14*s:.1f} {x+r-1:.1f} {hy+20*s:.1f}", hair_c, 5*s))
    if hair_t == "pigtails":
        o.append(fillc(x-r-4*s, hy+2*s, 5*s, hair_c, ow=2.4)); o.append(fillc(x+r+4*s, hy+2*s, 5*s, hair_c, ow=2.4))
    o.append(circ(x, hy, r, INK, 3*s, skin))
    if hair_t == "curly":
        for a in range(190, 355, 22):
            aa = math.radians(a)
            o.append(dot(x + math.cos(aa)*r*0.95, hy + math.sin(aa)*r*0.95, 4.6*s, hair_c))
        o.append(dot(x - r*0.98, hy + 3*s, 4*s, hair_c)); o.append(dot(x + r*0.98, hy + 3*s, 4*s, hair_c))
    elif hair_t in ("short", "pigtails", "long", "bun"):
        o.append(solid(f"M{x-r-1:.1f} {hy+1:.1f} Q{x-r:.1f} {hy-r-3*s:.1f} {x:.1f} {hy-r-1*s:.1f} Q{x+r:.1f} {hy-r-3*s:.1f} {x+r+1:.1f} {hy+1:.1f} Q{x+4*s:.1f} {hy-8*s:.1f} {x-r-1:.1f} {hy+1:.1f} Z", hair_c))
        if hair_t == "bun": o.append(fillc(x, hy-r-4*s, 5*s, hair_c, ow=2.4))
    elif hair_t == "spiky":
        o.append(P(f"M{x-r+1:.1f} {hy-r*0.55:.1f} l3 -7 l3 6 l3 -8 l3 8 l3 -7 l3 7 l3 -6", hair_c, 2.8*s))
    elif hair_t == "bald":
        o.append(P(f"M{x-r:.1f} {hy-2*s:.1f} q-2 6 1 9 M{x+r:.1f} {hy-2*s:.1f} q2 6 -1 9", hair_c, 4*s))
    if hat == "top":
        o.append(solid(f"M{x-r-4*s:.1f} {hy-r+2*s:.1f} h{2*r+8*s:.1f} v3 h{-(2*r+8*s):.1f} Z", INK))
        o.append(fillrect(round(x-r+3*s, 1), round(hy-r-16*s, 1), round(2*r-6*s, 1), round(16*s, 1), INK, ow=2.4))
    elif hat and hat[0] == "cap":
        o.append(solid(f"M{x-r:.1f} {hy-4*s:.1f} Q{x:.1f} {hy-r-8*s:.1f} {x+r:.1f} {hy-4*s:.1f} Z", hat[1]))
        o.append(P(f"M{x+r-4*s:.1f} {hy-4*s:.1f} l{12*s:.1f} 0", hat[1], 3.4*s))
    elif hat and hat[0] == "lady":
        o.append(P(f"M{x-r-6*s:.1f} {hy-r+5*s:.1f} Q{x:.1f} {hy-r+1*s:.1f} {x+r+6*s:.1f} {hy-r+5*s:.1f}", hat[1], 3.4*s))
        o.append(solid(f"M{x-r+2*s:.1f} {hy-r+4*s:.1f} Q{x:.1f} {hy-r-14*s:.1f} {x+r-2*s:.1f} {hy-r+4*s:.1f} Z", hat[1]))
        o.append(dot(x+r-3*s, hy-r, 3*s, C["rasp"]))
    if beard:
        o.append(P(f"M{x-r+2:.1f} {hy+5*s:.1f} Q{x:.1f} {hy+r+8*s:.1f} {x+r-2:.1f} {hy+5*s:.1f}", beard, 4*s))
    o.append(face_(x, hy, s, face, eyes))
    if glasses:
        o.append(circ(x-4.6*s, hy-1*s, 3.6*s, INK, 1.4)); o.append(circ(x+4.6*s, hy-1*s, 3.6*s, INK, 1.4))
        o.append(P(f"M{x-1*s:.1f} {hy-1*s:.1f} h{2*s:.1f}", INK, 1.2))
    if blush and face not in ("sad", "frown"):
        o.append(f'<g opacity="0.85">{dot(x-8*s, hy+4*s, 2.2*s, CHEEK)}{dot(x+8*s, hy+4*s, 2.2*s, CHEEK)}</g>')
    return "".join(o)

def face_(x, y, s, face, eyes="open"):
    o = []
    ey = y - 1*s
    if eyes == "closed" or face == "sleep":
        o.append(P(f"M{x-7*s:.1f} {ey:.1f} q2.4 2.4 4.8 0 M{x+2.2*s:.1f} {ey:.1f} q2.4 2.4 4.8 0", INK, 1.8))
    elif eyes == "happy":
        o.append(P(f"M{x-7*s:.1f} {ey+1:.1f} q2.4 -3 4.8 0 M{x+2.2*s:.1f} {ey+1:.1f} q2.4 -3 4.8 0", INK, 1.8))
    elif eyes == "side":
        o.append(dot(x-3*s, ey, 1.8*s)); o.append(dot(x+6*s, ey, 1.8*s))
    else:
        o.append(dot(x-4.6*s, ey, 1.8*s)); o.append(dot(x+4.6*s, ey, 1.8*s))
    my = y + 5*s
    m = {
        "smile": f"M{x-5*s:.1f} {my:.1f} Q{x:.1f} {my+5*s:.1f} {x+5*s:.1f} {my:.1f}",
        "sleep": f"M{x-3*s:.1f} {my+1:.1f} Q{x:.1f} {my+3*s:.1f} {x+3*s:.1f} {my+1:.1f}",
        "sad": f"M{x-5*s:.1f} {my+3*s:.1f} Q{x:.1f} {my-2*s:.1f} {x+5*s:.1f} {my+3*s:.1f}",
        "frown": f"M{x-5*s:.1f} {my+3*s:.1f} Q{x:.1f} {my-2*s:.1f} {x+5*s:.1f} {my+3*s:.1f}",
        "meh": f"M{x-5*s:.1f} {my+1:.1f} q2.5 -2 5 0 q2.5 2 5 0",
        "line": f"M{x-4*s:.1f} {my+1:.1f} h{8*s:.1f}",
    }
    if face in ("big", "laugh"):
        o.append(solid(f"M{x-4.5*s:.1f} {my:.1f} Q{x:.1f} {my+6*s:.1f} {x+4.5*s:.1f} {my:.1f} Z", C["red"]))
    elif face == "open":
        o.append(dot(x, my+1.5*s, 2.8*s, C["red"]))
    elif face == "o":
        o.append(circ(x, my+1.5*s, 2.4*s, INK, 1.6))
    else:
        o.append(P(m.get(face, m["smile"]), INK, 2))
    if face == "frown":
        o.append(P(f"M{x-8*s:.1f} {ey-5*s:.1f} l5 2 M{x+8*s:.1f} {ey-5*s:.1f} l-5 2", INK, 1.8))
    return "".join(o)

# ---------- герои ----------
def rosa(x, y, s=1.15, **kw):
    a = dict(body="topskirt", c=C["sky"], c2=C["night"], hair=("curly", C["copper"]), glasses=True,
             shawl=[C["coral"], C["amber"], C["teal"]])
    a.update(kw); return person(x, y, s, **a)
def amir(x, y, s=1.1, **kw):
    a = dict(body="shirt", c=C["green"], c2=C["blue"], hair=("curly", C["black"]), skin=C["skin2"])
    a.update(kw); return person(x, y, s, **a)

# ---------- предметы ----------
def paper(c):
    return (f'<rect x="0" y="0" width="200" height="200" fill="{c}"/>'
            '<rect x="0" y="0" width="200" height="200" fill="url(#fib)"/>')

def grass(y=180, c=C["green"], x0=0, x1=200):
    d = f"M{x0} {y}"; x = x0; up = True
    while x < x1:
        x += 5; d += f" L{x} {y-6 if up else y}"; up = not up
    return P(d, c, 2.4)

def ground(y, c, top=None):
    return scribble(f"M0 {y} Q100 {y-6} 200 {y} L200 200 L0 200 Z", (0, y-8, 200, 200), c, outline=False, w=3, step=4)

def sun(x, y, r=16, face=True, c=C["orange"], c2=C["yellow"], rays=8):
    o = [fillc(x, y, r, c2, ow=0.01, outline=False), circ(x, y, r, c, 3.2)]
    for k in range(rays):
        a = math.radians(k*360/rays - 90 + 12)
        o.append(P(f"M{x+math.cos(a)*(r+4):.1f} {y+math.sin(a)*(r+4):.1f} L{x+math.cos(a)*(r+12):.1f} {y+math.sin(a)*(r+12):.1f}", c if k % 2 else c2, 3))
    if face:
        o.append(dot(x-r*.35, y-r*.2, 1.9)); o.append(dot(x+r*.35, y-r*.2, 1.9))
        o.append(P(f"M{x-r*.4:.1f} {y+r*.25:.1f} Q{x:.1f} {y+r*.6:.1f} {x+r*.4:.1f} {y+r*.25:.1f}", INK, 2))
    return "".join(o)

def moon(x, y, r=16, c=C["lemon"]):
    return solid(f"M{x:.1f} {y-r:.1f} A{r} {r} 0 1 0 {x+r*0.75:.1f} {y+r*0.8:.1f} A{r*0.75:.1f} {r*0.75:.1f} 0 1 1 {x:.1f} {y-r:.1f} Z", c)

def star(x, y, r=5, c=WHITE):
    pts = []
    for k in range(10):
        a = math.radians(-90 + k*36); rr = r if k % 2 == 0 else r*0.45
        pts.append(f"{x+math.cos(a)*rr:.1f} {y+math.sin(a)*rr:.1f}")
    return solid("M" + " L".join(pts) + " Z", c)

def cloud(x, y, s=1.0, c=WHITE, o=1):
    d = (f"M{x:.1f} {y:.1f} q0 {-10*s:.1f} {10*s:.1f} {-8*s:.1f} q{4*s:.1f} {-8*s:.1f} {12*s:.1f} {-2*s:.1f} "
         f"q{8*s:.1f} {-2*s:.1f} {8*s:.1f} {6*s:.1f} q{2*s:.1f} {4*s:.1f} {-4*s:.1f} {4*s:.1f} Z")
    return f'<g opacity="{o}">{solid(d, c)}</g>'

def bird(x, y, c=INK, s=1):
    return P(f"M{x:.1f} {y:.1f} q{4*s:.1f} {-4*s:.1f} {8*s:.1f} 0 q{4*s:.1f} {-4*s:.1f} {8*s:.1f} 0", c, 2.2)

def heart(x, y, s=1.0, c=C["red"], fill=True):
    d = (f"M{x:.1f} {y+10*s:.1f} C{x-14*s:.1f} {y:.1f} {x-12*s:.1f} {y-12*s:.1f} {x-5*s:.1f} {y-12*s:.1f} "
         f"C{x-2*s:.1f} {y-12*s:.1f} {x:.1f} {y-9*s:.1f} {x:.1f} {y-7*s:.1f} C{x:.1f} {y-9*s:.1f} {x+2*s:.1f} {y-12*s:.1f} {x+5*s:.1f} {y-12*s:.1f} "
         f"C{x+12*s:.1f} {y-12*s:.1f} {x+14*s:.1f} {y:.1f} {x:.1f} {y+10*s:.1f} Z")
    return solid(d, c) if fill else P(d, c, 2.6)

def house(x, y, w=60, h=46, wall=C["ochre"], roof=C["red"], door=C["wood"], win=C["sky"], lit=False, doorw=14):
    o = [fillrect(x, y-h, w, h, wall, ow=0.01, outline=False), P(f"M{x} {y-h} h{w} v{h} h{-w} Z", INK, 3)]
    rd = f"M{x-6} {y-h} L{x+w/2} {y-h-w*0.45} L{x+w+6} {y-h} Z"
    o.append(scribble(rd, (x-6, y-h-w*.45, x+w+6, y-h), roof))
    dx = x + w/2 - doorw/2
    o.append(fillrect(dx, y-24, doorw, 24, door, ow=2.6))
    o.append(dot(dx+doorw-3, y-12, 1.4, INK))
    wc = C["yellow"] if lit else win
    o.append(f'<rect x="{x+6}" y="{y-h+8}" width="10" height="10" fill="{wc}" stroke="{INK}" stroke-width="2"/>')
    o.append(f'<rect x="{x+w-16}" y="{y-h+8}" width="10" height="10" fill="{wc}" stroke="{INK}" stroke-width="2"/>')
    return "".join(o)

def doorway(x, y, w=40, h=74, frame=C["wood"], inside=C["yellow"], open_=True):
    o = [f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="{inside}" stroke="none" opacity="0.55"/>',
         P(f"M{x} {y} V{y-h} H{x+w} V{y}", frame, 5)]
    if open_:
        o.append(scribble(f"M{x+w} {y-h} l14 6 v{h-10} l-14 4 Z", (x+w, y-h, x+w+14, y), frame, ow=2.6))
    return "".join(o)

def bubble(x, y, w, h, tx, ty, inner="", c=WHITE, oc=INK):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(h/2, 14)}" fill="{c}" stroke="{oc}" stroke-width="2.6"/>']
    mx = x + w/2; by = y + h
    if ty > by:
        o.append(f'<path d="M{mx-6:.1f} {by-1:.1f} L{tx:.1f} {ty:.1f} L{mx+6:.1f} {by-1:.1f}" fill="{c}" stroke="{oc}" stroke-width="2.6" stroke-linejoin="round"/>')
        o.append(P(f"M{mx-5:.1f} {by-1.5:.1f} L{mx+5:.1f} {by-1.5:.1f}", c, 3))
    o.append(inner)
    return "".join(o)

def think(x, y, w, h, tx, ty, inner=""):
    o = [f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{WHITE}" stroke="{INK}" stroke-width="2.4"/>']
    for k, rr in ((0.35, 4), (0.7, 2.6)):
        o.append(circ(x+w/2+(tx-x-w/2)*k, y+h+(ty-y-h)*k, rr, INK, 2, WHITE))
    o.append(inner); return "".join(o)

def txt(x, y, t, size=16, c=INK, w=700):
    return f'<text x="{x}" y="{y}" font-family="Comic Sans MS, Chalkboard, Marker Felt, cursive" font-size="{size}" font-weight="{w}" fill="{c}" text-anchor="middle">{t}</text>'

def clock(x, y, r=13, h=3, m=0, c=C["blue"]):
    o = [circ(x, y, r, c, 3, WHITE)]
    for k in range(12):
        a = math.radians(k*30)
        o.append(dot(x+math.cos(a)*(r-3.5), y+math.sin(a)*(r-3.5), 0.9))
    ah = math.radians((h % 12)*30 + m*0.5 - 90); am = math.radians(m*6 - 90)
    o.append(P(f"M{x} {y} l{math.cos(ah)*r*.5:.1f} {math.sin(ah)*r*.5:.1f}", INK, 2.6))
    o.append(P(f"M{x} {y} l{math.cos(am)*r*.75:.1f} {math.sin(am)*r*.75:.1f}", INK, 2))
    return "".join(o)

def calendar(x, y, w=34, h=30, c=C["red"], mark=None, weekend=False):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{WHITE}" stroke="{INK}" stroke-width="2.4"/>',
         fillrect(x, y, w, 8, c, ow=2.4), P(f"M{x+8} {y-3} v6 M{x+w-8} {y-3} v6", INK, 2.4)]
    cw = (w-6)/7; ch = (h-12)/3
    for r_ in range(3):
        for k in range(7):
            cx_ = x + 3 + cw*k + cw/2; cy_ = y + 11 + ch*r_ + ch/2
            col = C["red"] if weekend and k >= 5 else C["grey"]
            o.append(dot(cx_, cy_, 1.3 if not (weekend and k >= 5) else 2, col))
    if mark is not None:
        r_, k = mark
        cx_ = x + 3 + cw*k + cw/2; cy_ = y + 11 + ch*r_ + ch/2
        o.append(circ(cx_, cy_, 4.4, C["red"], 2.2))
    return "".join(o)

def phone(x, y, c=C["red"], s=1):
    d = f"M{x-12*s:.1f} {y:.1f} q0 {-8*s:.1f} {6*s:.1f} {-8*s:.1f} h{12*s:.1f} q{6*s:.1f} 0 {6*s:.1f} {8*s:.1f} l{-6*s:.1f} 0 l-2 -4 h{-8*s:.1f} l-2 4 Z"
    return solid(d, c) + fillrect(round(x-10*s, 1), round(y+1, 1), round(20*s, 1), round(10*s, 1), c, ow=2.4)

def mobile(x, y, c=C["night"], s=1):
    return (f'<rect x="{x-6*s:.1f}" y="{y-10*s:.1f}" width="{12*s:.1f}" height="{20*s:.1f}" rx="2" fill="{c}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{x-4*s:.1f}" y="{y-7*s:.1f}" width="{8*s:.1f}" height="{12*s:.1f}" fill="{C["ice"]}"/>')

def waves(x, y, c=INK, side=1, n=2):
    o = ""
    for k in range(n):
        rr = 6 + k*5
        o += P(f"M{x:.1f} {y-rr:.1f} q{side*rr*.7:.1f} {rr:.1f} 0 {2*rr:.1f}", c, 2.2)
    return o

def motion(x, y, c=INK, side=1, s=1.0):
    return P(f"M{x:.1f} {y:.1f} q{side*6*s:.1f} {6*s:.1f} {side*4*s:.1f} {14*s:.1f} M{x+side*7*s:.1f} {y-4*s:.1f} q{side*8*s:.1f} {8*s:.1f} {side*5*s:.1f} {20*s:.1f}", c, 2.4)

def sparkle(x, y, c=C["amber"], r=5):
    return P(f"M{x} {y-r} v{2*r} M{x-r} {y} h{2*r}", c, 2.4) + P(f"M{x-r*.6:.1f} {y-r*.6:.1f} l{r*1.2:.1f} {r*1.2:.1f} M{x+r*.6:.1f} {y-r*.6:.1f} l{-r*1.2:.1f} {r*1.2:.1f}", c, 1.4)

def zzz(x, y, c=WHITE):
    return P(f"M{x} {y} h8 l-8 9 h8 M{x+12} {y-12} h6 l-6 7 h6", c, 2.2)

def qmark(x, y, c=INK, s=1):
    return P(f"M{x-5*s:.1f} {y-6*s:.1f} q0 {-7*s:.1f} {6*s:.1f} {-7*s:.1f} q{6*s:.1f} 0 {6*s:.1f} {6*s:.1f} q0 {4*s:.1f} {-6*s:.1f} {7*s:.1f} v{4*s:.1f}", c, 2.8*s) + dot(x+1*s, y+9*s, 1.9*s, c)

def excl(x, y, c=C["red"], s=1):
    return P(f"M{x} {y-9*s:.1f} v{12*s:.1f}", c, 3.4*s) + dot(x, y+8*s, 2*s, c)

def smiley(x, y, r=7, c=C["amber"], mood="smile"):
    o = [fillc(x, y, r, c, ow=2.2), dot(x-r*.35, y-r*.2, 1.3), dot(x+r*.35, y-r*.2, 1.3)]
    if mood == "smile": o.append(P(f"M{x-r*.45:.1f} {y+r*.2:.1f} Q{x:.1f} {y+r*.65:.1f} {x+r*.45:.1f} {y+r*.2:.1f}", INK, 1.6))
    elif mood == "sad": o.append(P(f"M{x-r*.45:.1f} {y+r*.55:.1f} Q{x:.1f} {y+r*.1:.1f} {x+r*.45:.1f} {y+r*.55:.1f}", INK, 1.6))
    else: o.append(P(f"M{x-r*.45:.1f} {y+r*.35:.1f} h{r*.9:.1f}", INK, 1.6))
    return "".join(o)

def cup(x, y, c=C["red"], steam=True, s=1):
    d = f"M{x-8*s:.1f} {y-12*s:.1f} h{16*s:.1f} l{-2*s:.1f} {12*s:.1f} h{-12*s:.1f} Z"
    o = [scribble(d, (x-8*s, y-12*s, x+8*s, y), c, ow=2.4), P(f"M{x+8*s:.1f} {y-9*s:.1f} q{6*s:.1f} 1 {1*s:.1f} {6*s:.1f}", c, 2.4)]
    if steam: o.append(P(f"M{x-3*s:.1f} {y-16*s:.1f} q-3 -4 0 -8 M{x+3*s:.1f} {y-16*s:.1f} q-3 -4 0 -8", C["grey"], 1.8))
    return "".join(o)

def table(x, y, w=80, c=C["wood"]):
    return P(f"M{x} {y} h{w} M{x+6} {y} v22 M{x+w-6} {y} v22", c, 4)

def gift(x, y, s=16, c=C["blue"], rib=C["yellow"]):
    return (fillrect(x, y, s, s, c, ow=2.6) + P(f"M{x+s/2} {y} v{s} M{x} {y+s/2} h{s}", rib, 2.4)
            + P(f"M{x+s/2} {y} q-6 -7 -9 -1 M{x+s/2} {y} q6 -7 9 -1", rib, 2.4))

def flower(x, y, c=C["rasp"], stem=C["green"], s=1):
    o = [P(f"M{x} {y} v{-14*s:.1f}", stem, 2.4)]
    for k in range(5):
        a = math.radians(k*72)
        o.append(dot(x+math.cos(a)*4*s, y-16*s+math.sin(a)*4*s, 3*s, c))
    o.append(dot(x, y-16*s, 2.4*s, C["yellow"]))
    return "".join(o)

def bouquet(x, y):
    return flower(x-4, y, C["rasp"]) + flower(x+4, y-2, C["yellow"]) + flower(x, y-4, C["red"])

def tree(x, y, c=C["green"], trunk=C["wood"], s=1):
    return P(f"M{x} {y} v{-24*s:.1f}", trunk, 6*s) + fillc(x, y-34*s, 16*s, c, ow=2.6)

def bed(x, y, w=110, blanket=C["purple"]):
    o = [P(f"M{x} {y} V{y-34} M{x+w} {y} V{y-20} M{x} {y-8} H{x+w}", C["wood"], 4)]
    d = f"M{x+18} {y-24} Q{x+w/2} {y-32} {x+w-4} {y-22} L{x+w-4} {y-8} L{x+18} {y-8} Z"
    o.append(scribble(d, (x+18, y-32, x+w-4, y-8), blanket))
    o.append(f'<ellipse cx="{x+12}" cy="{y-16}" rx="11" ry="5" fill="{WHITE}" stroke="{C["pgrey"]}" stroke-width="1"/>')
    return "".join(o)

def window(x, y, w=40, h=40, frame=C["wood"], inside=C["ice"]):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{inside}" stroke="{frame}" stroke-width="4"/>'
            + P(f"M{x+w/2} {y} v{h} M{x} {y+h/2} h{w}", frame, 3))

def arrow(x1, y1, x2, y2, c=INK, w=2.6, curve=0):
    mx, my = (x1+x2)/2, (y1+y2)/2 - curve
    a = math.atan2(y2-my, x2-mx)
    hx1, hy1 = x2 - 7*math.cos(a-0.5), y2 - 7*math.sin(a-0.5)
    hx2, hy2 = x2 - 7*math.cos(a+0.5), y2 - 7*math.sin(a+0.5)
    return P(f"M{x1} {y1} Q{mx} {my} {x2} {y2} M{hx1:.1f} {hy1:.1f} L{x2} {y2} L{hx2:.1f} {hy2:.1f}", c, w)

def notes(x, y, c=C["violet"]):
    return P(f"M{x} {y} v-12 l8 -3 v12", c, 2.4) + dot(x-2, y, 3, c) + dot(x+6, y-3, 3, c)

def bike(x, y, c=C["red"]):
    return (circ(x-16, y-10, 10, INK, 3) + circ(x+16, y-10, 10, INK, 3)
            + P(f"M{x-16} {y-10} L{x-4} {y-28} L{x+12} {y-28} L{x+16} {y-10} M{x-4} {y-28} L{x+2} {y-10} L{x-16} {y-10} M{x+12} {y-28} l2 -6 h6", c, 3.4))

def sofa(x, y, w=110, c=C["coral"]):
    return (fillrect(x, y-22, w, 22, c, ow=3) + fillrect(x-8, y-34, 12, 34, c, ow=3) + fillrect(x+w-4, y-34, 12, 34, c, ow=3)
            + P(f"M{x} {y} v8 M{x+w} {y} v8", C["wood"], 4))

def suitcase(x, y, c=C["orange"]):
    return fillrect(x, y-20, 26, 20, c, ow=2.6) + P(f"M{x+8} {y-20} v-5 h10 v5", INK, 2.4)

def svg(inner, paper_c):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="520" height="520">'
            '<defs><filter id="cr" x="-5%" y="-5%" width="110%" height="110%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="2" result="t"/>'
            '<feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.4 1.5" result="a"/>'
            '<feComposite in="SourceGraphic" in2="a" operator="in" result="g"/>'
            '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="w"/>'
            '<feDisplacementMap in="g" in2="w" scale="4" xChannelSelector="R" yChannelSelector="G"/></filter>'
            '<pattern id="fib" width="40" height="40" patternUnits="userSpaceOnUse">'
            '<path d="M2 9 Q14 7 24 10 M18 27 Q28 25 38 28 M4 35 Q9 34 14 36" stroke="#000" stroke-opacity="0.06" stroke-width="0.8" fill="none"/></pattern></defs>'
            + paper(paper_c) +
            f'<g filter="url(#cr)" fill="none" stroke-linecap="round" stroke-linejoin="round">{inner}</g></svg>')
