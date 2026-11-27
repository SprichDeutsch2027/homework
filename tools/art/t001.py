# Тема 1 · Hallo & Tschüss — сцены к словам
from kid import *

G = 186          # линия земли
S = 1.3          # масштаб героев
def hy(y=G, s=S): return y - 77*s     # центр головы

def klaus(x, y=G, s=S, **kw):
    a = dict(body="shirt", c=C["brown"], c2=C["dgrey"], hair=("bald", C["lgrey"]), beard=C["lgrey"]); a.update(kw); return person(x, y, s, **a)
def brandl(x, y=G, s=S, **kw):
    a = dict(body="dress", c=C["lavender"], hair=("short", C["lgrey"]), hat=("lady", C["violet"]), glasses=True); a.update(kw); return person(x, y, s, **a)
def guenter(x, y=G, s=S, **kw):
    a = dict(body="shirt", c=C["tan"], c2=C["brown"], hair=("bald", C["pgrey"]), glasses=True, tie=C["dred"]); a.update(kw); return person(x, y, s, **a)
def malik(x, y=G, s=S, **kw):
    a = dict(body="shirt", c=C["orange"], c2=C["night"], hair=("spiky", C["black"]), skin=C["skin3"]); a.update(kw); return person(x, y, s, **a)
def clara(x, y=G, s=S, **kw):
    a = dict(body="dress", c=C["rasp"], hair=("long", C["amber"])); a.update(kw); return person(x, y, s, **a)
def petra(x, y=G, s=S, **kw):
    a = dict(body="shirt", c=C["yellow"], c2=C["teal"], hair=("short", C["hbrown"])); a.update(kw); return person(x, y, s, **a)
def lilli(x, y=G, s=1.0, **kw):
    a = dict(body="dress", c=C["pink"], hair=("pigtails", C["amber"])); a.update(kw); return person(x, y, s, **a)
def hannah(x, y=G, s=S, **kw):
    a = dict(body="dress", c=C["red"], hair=("long", C["hbrown"])); a.update(kw); return person(x, y, s, **a)
def tom(x, y=G, s=S, **kw):
    a = dict(body="shirt", c=C["blue"], c2=C["dgrey"], hair=("short", C["amber"])); a.update(kw); return person(x, y, s, **a)
def teen(x, y=G, s=1.15, **kw):
    a = dict(body="shirt", c=C["purple"], c2=C["night"], hair=("short", C["black"]), hat=("cap", C["red"]), skin=C["skin2"]); a.update(kw); return person(x, y, s, **a)

def word(t, x, y, size=15):  # слово в пузыре (только du / Sie)
    return txt(x, y, t, size)

def sunicon(x, y, r=7): return sun(x, y, r, face=False, rays=8)
def hourglass(x, y, c=C["amber"]):
    return P(f"M{x-6} {y-9} h12 l-12 18 h12 Z", INK, 2.2) + solid(f"M{x-3} {y+6} h6 l-3 -5 Z", c) + solid(f"M{x-4} {y-7} h8 l-4 5 Z", c)
def lips(x, y, c=C["red"]):
    return solid(f"M{x-6} {y} q3 -4 6 -1 q3 -3 6 1 q-6 6 -12 0 Z", c)
def thumb(x, y, c=C["amber"]):
    return fillrect(x-6, y-2, 12, 11, c, ow=2.2) + P(f"M{x-4} {y-2} l1 -9 q4 -2 4 3 v6", INK, 2.4)
def tray(x, y):
    return P(f"M{x-16} {y} h32", C["grey"], 4) + cup(x-8, y-2, C["red"], True, .7) + cup(x+8, y-2, C["blue"], True, .7)
def lighthouse(x, y):
    o = ""
    for k in range(4):
        c = C["red"] if k % 2 == 0 else WHITE
        o += scribble(f"M{x-12+k*1.5} {y-k*22} L{x+12-k*1.5} {y-k*22} L{x+10.5-k*1.5} {y-(k+1)*22} L{x-10.5+k*1.5} {y-(k+1)*22} Z", (x-12, y-(k+1)*22, x+12, y-k*22), c, ow=2.4)
    o += P(f"M{x-12} {y} L{x-6} {y-88} L{x+6} {y-88} L{x+12} {y}", INK, 2.6)
    o += fillrect(x-7, y-102, 14, 14, C["yellow"], ow=2.4) + solid(f"M{x-9} {y-102} L{x} {y-112} L{x+9} {y-102} Z", C["red"])
    o += P(f"M{x+10} {y-96} l26 -8 M{x+10} {y-94} l26 6", C["amber"], 2)
    return o
def sea(y):
    return scribble(f"M0 {y} Q50 {y-6} 100 {y} T200 {y} L200 200 L0 200 Z", (0, y-8, 200, 200), C["blue"], outline=False, w=3, step=4, vertical=False) + P(f"M10 {y+8} q6 -5 12 0 q6 5 12 0 M120 {y+14} q6 -5 12 0 q6 5 12 0", WHITE, 2)
def wheel(x, y, r=46):
    o = circ(x, y, r, C["red"], 3.4) + circ(x, y, 6, INK, 3)
    for k in range(12):
        a = math.radians(k*30)
        o += P(f"M{x} {y} L{x+math.cos(a)*r:.1f} {y+math.sin(a)*r:.1f}", C["grey"], 1.8)
        if k % 2 == 0:
            gx, gy = x+math.cos(a)*r, y+math.sin(a)*r
            o += fillrect(round(gx-5, 1), round(gy, 1), 10, 9, [C["yellow"], C["blue"], C["green"]][k//2 % 3], ow=2)
    o += P(f"M{x} {y} L{x-26} {y+r+40} M{x} {y} L{x+26} {y+r+40}", INK, 3)
    return o
def mountains(y):
    return (scribble(f"M-10 {y} L40 {y-70} L80 {y-30} L120 {y-86} L170 {y-24} L210 {y-60} L210 {y} Z", (-10, y-86, 210, y), C["lgrey"], ow=2.6)
            + solid(f"M30 {y-58} L40 {y-70} L50 {y-58} L44 {y-62} L38 {y-56} Z", WHITE)
            + solid(f"M108 {y-71} L120 {y-86} L132 {y-71} L125 {y-75} L118 {y-68} Z", WHITE))
def pretzel(x, y, c=C["wood"]):
    return P(f"M{x-12} {y+8} Q{x-20} {y-12} {x} {y-6} Q{x+20} {y-12} {x+12} {y+8} Q{x} {y+16} {x-6} {y-2} M{x+6} {y-2} Q{x} {y+16} {x-12} {y+8}", c, 4)
def board(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#2f4f3f" stroke="{C["wood"]}" stroke-width="5"/>'
def chandelier(x, y):
    o = P(f"M{x} 0 v{y-8}", INK, 2) + P(f"M{x-26} {y} Q{x} {y+16} {x+26} {y}", C["amber"], 3)
    for dx in (-26, -9, 9, 26):
        o += P(f"M{x+dx} {y+ (6 if abs(dx) < 10 else 0)} v-8", C["amber"], 2.4) + solid(f"M{x+dx-2} {y-8+(6 if abs(dx) < 10 else 0)} q2 -7 4 0 Z", C["orange"])
    return o
def garland(x0, x1, y):
    o = P(f"M{x0} {y} Q{(x0+x1)/2} {y+14} {x1} {y}", INK, 1.6); cols = [C["red"], C["yellow"], C["blue"], C["green"], C["rasp"]]
    n = 6
    for k in range(n):
        t = (k+0.5)/n; px = x0 + (x1-x0)*t; py = y + 14*4*t*(1-t)*0.98
        o += solid(f"M{px-5:.1f} {py:.1f} h10 l-5 10 Z", cols[k % 5])
    return o
def envelope(x, y, w=110, h=72):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>'
            + P(f"M{x} {y} L{x+w/2} {y+h*0.55} L{x+w} {y}", INK, 2.6)
            + fillc(x+w/2, y+h*0.55, 11, C["dred"], ow=2.4) + star(x+w/2, y+h*0.55, 5, C["amber"]))
def rathaus(x, y, w=64):
    o = scribble(f"M{x} {y} h{w} v-34 h{-w} Z", (x, y-34, x+w, y), C["pgrey"], ow=2.6)
    o += solid(f"M{x-4} {y-34} L{x+w/2} {y-52} L{x+w+4} {y-34} Z", C["lgrey"]) + P(f"M{x-4} {y-34} L{x+w/2} {y-52} L{x+w+4} {y-34} Z", INK, 2.4)
    for k in range(5):
        o += P(f"M{x+6+k*13} {y-30} v28", C["grey"], 3)
    o += P(f"M{x+w/2} {y-52} v-12", INK, 2) + solid(f"M{x+w/2} {y-64} h12 v6 h-12 Z", C["red"])
    return o
def counter(x, y, w=70):
    return fillrect(x, y-34, w, 34, C["sky"], ow=3) + P(f"M{x-4} {y-34} h{w+8}", C["wood"], 4)
def skate(x, y):
    return P(f"M{x-16} {y} h32", C["orange"], 4) + dot(x-10, y+4, 3) + dot(x+10, y+4, 3)
def cat(x, y, c=C["dgrey"]):
    return (fillc(x, y-10, 9, c, ow=2.4) + fillc(x+12, y-20, 7, c, ow=2.4)
            + solid(f"M{x+6} {y-25} l2 -8 l4 5 Z", c) + solid(f"M{x+14} {y-26} l4 -7 l2 7 Z", c)
            + P(f"M{x-8} {y-12} q-10 -4 -6 -16", c, 3) + dot(x+10, y-21, 1.2, WHITE) + dot(x+15, y-21, 1.2, WHITE))
def owl(x, y):
    return (fillc(x, y, 10, C["wood"], ow=2.4) + circ(x-4, y-3, 3.4, INK, 1.6, WHITE) + circ(x+4, y-3, 3.4, INK, 1.6, WHITE)
            + dot(x-4, y-3, 1.4) + dot(x+4, y-3, 1.4) + solid(f"M{x-1.5} {y+1} h3 l-1.5 3 Z", C["amber"]))
def rooster(x, y):
    return (fillc(x, y-12, 11, C["ochre"], ow=2.6) + fillc(x+10, y-26, 6, C["ochre"], ow=2.4)
            + solid(f"M{x+6} {y-32} q2 -6 4 0 q2 -6 4 0 Z", C["red"]) + solid(f"M{x+16} {y-27} l6 2 l-6 2 Z", C["amber"])
            + P(f"M{x-10} {y-16} q-8 -12 -2 -20 M{x-10} {y-12} q-12 -6 -10 -16", C["green"], 3) + P(f"M{x-2} {y-1} v6 M{x+4} {y-1} v6", C["amber"], 2.4)
            + dot(x+11, y-27, 1.2))
def fence(x0, x1, y, c=C["wood"]):
    o = P(f"M{x0} {y-12} H{x1} M{x0} {y-22} H{x1}", c, 3)
    x = x0
    while x <= x1:
        o += P(f"M{x} {y} v-30", c, 3.4); x += 12
    return o
def sky(c, y1=120, c2=None):
    o = scribble(f"M0 0 H200 V{y1} H0 Z", (0, 0, 200, y1), c, outline=False, w=4, step=5, vertical=False)
    return o
def lamp(x, y):
    return P(f"M{x} {y} v-80", INK, 3.4) + solid(f"M{x-8} {y-80} h16 l-3 -10 h-10 Z", C["yellow"]) + f'<circle cx="{x}" cy="{y-82}" r="16" fill="{C["lemon"]}" opacity="0.35"/>'

def sleephead(x, y, s=.75):
    r = 13*s
    return (fillc(x-r-3, y+2, 4, C["amber"], ow=2) + fillc(x+r+3, y+2, 4, C["amber"], ow=2) + circ(x, y, r, INK, 2.4, SKIN)
            + solid(f"M{x-r-1:.1f} {y+1:.1f} Q{x-r:.1f} {y-r-3:.1f} {x:.1f} {y-r-1:.1f} Q{x+r:.1f} {y-r-3:.1f} {x+r+1:.1f} {y+1:.1f} Q{x+3:.1f} {y-6:.1f} {x-r-1:.1f} {y+1:.1f} Z", C["amber"])
            + P(f"M{x-6} {y} q2 2 4 0 M{x+2} {y} q2 2 4 0 M{x-2} {y+5} q2 2 4 0", INK, 1.6) + dot(x-7, y+4, 1.8, CHEEK) + dot(x+7, y+4, 1.8, CHEEK))
def bike2(x, y, c, k=1.4):
    r = 10*k
    return (circ(x-16*k, y-r, r, INK, 3) + circ(x+16*k, y-r, r, INK, 3)
            + P(f"M{x-16*k} {y-r} L{x-4*k} {y-r-18*k} L{x+12*k} {y-r-18*k} L{x+16*k} {y-r} M{x-4*k} {y-r-18*k} L{x+2*k} {y-r} L{x-16*k} {y-r} M{x+12*k} {y-r-18*k} l2 -8 h7 M{x-6*k} {y-r-18*k} l-2 -6 h-8", c, 3.6))
def clover(x, y):
    return "".join(heart(x+dx, y+dy, .32, C["green"]) for dx, dy in ((-4, -4), (4, -4), (-4, 4), (4, 4))) + P(f"M{x} {y+4} q2 8 6 10", C["dgreen"], 2)
def chalkman(x, y, arm=(10, -4), c=WHITE):
    return circ(x, y-26, 5, c, 2) + P(f"M{x} {y-21} v12 M{x} {y-9} l-5 9 M{x} {y-9} l5 9 M{x} {y-17} l{arm[0]} {arm[1]} M{x} {y-17} l-7 6", c, 2)
SC = {}
def sc(k, paper):
    def d(f): SC[k] = (paper, f); return f
    return d

@sc("hallo", "cream")
def _():
    return (doorway(10, G, 44, 96) + grass(G+2, C["green"]) + rosa(76, G, arms=("down", "wave"), handc=(INK, C["amber"]), face="big")
            + motion(112, 52, C["orange"]) + amir(152, G, s=1.25, arms=("wave", "down"), handc=(C["orange"], INK)) + motion(124, 66, C["orange"], -1, .8))

@sc("tschuess", "blue")
def _():
    return (house(10, 160, 62, 48, C["ochre"], C["red"]) + P("M48 162 Q100 172 150 170", C["violet"], 2.6, extra='stroke-dasharray="5 6"')
            + amir(156, G, s=1.1, arms=("wave", "down"), handc=(C["orange"], INK)) + motion(130, 70, C["orange"], -1, .8)
            + grass(G+2, C["green"], 80, 200))

@sc("guten-morgen", "peach")
def _():
    return (sun(104, 128, 22, True) + ground(140, C["lgreen"]) + bird(150, 30, C["navy"]) + bird(174, 44, C["navy"], .8)
            + rosa(46, G, arms=("down", "hi"))
            + amir(162, G, s=1.2, arms=("hi", "down"))
            + bubble(14, 22, 52, 34, 50, 74, sun(40, 39, 8, False, rays=8)))

@sc("guten-tag", "blue")
def _():
    return (sun(100, 26, 15, True) + cloud(22, 44, 1.1) + cloud(160, 50, .9) + grass(G+2, C["green"])
            + amir(60, G, arms=("down", "hi")) + brandl(146, G, cane=True, arms=("down", "low"), face="smile")
            + bubble(4, 66, 40, 28, 48, 100, sun(24, 80, 6, False)))

@sc("guten-abend", "dusk")
def _():
    return (sky(C["lavender"], 70) + P("M0 72 H200", C["amber"], 3) + sun(188, 84, 14, False, C["dorange"], C["amber"], 0)
            + star(30, 24, 5, C["yellow"]) + star(120, 14, 4, C["yellow"]) + doorway(4, G, 40, 92, inside=C["yellow"])
            + rosa(58, G, arms=("down", "hi")) + klaus(154, G, arms=("hi", "down"))
            + bubble(86, 30, 44, 30, 78, 66, P("M95 52 h26", INK, 2) + sun(108, 52, 7, False, C["dorange"], C["amber"], 5)))

@sc("auf-wiedersehen", "lav")
def _():
    return (doorway(10, G, 46, 100) + grass(G+2, C["green"]) + amir(66, G, arms=("down", "chest"), face="smile")
            + guenter(146, G, hat="top", arms=("wave", "down"), cane=False) + motion(116, 60, C["violet"], -1, .8))

@sc("mir-gehts-gut", "yellow")
def _():
    return (sun(160, 40, 16) + grass(G+2, C["green"]) + amir(96, G-14, s=1.35, arms=("up", "up"), face="big")
            + P("M80 186 h12 M104 186 h12", C["grey"], 2.6) + sparkle(36, 60, C["blue"], 6) + sparkle(150, 100, C["rasp"], 5) + sparkle(40, 130, C["amber"], 5))

@sc("gruessen", "mint")
def _():
    return (grass(G+2, C["green"]) + amir(46, G, arms=("down", "hi")) + motion(74, 62, C["orange"], 1, .7)
            + brandl(108, G-6, s=.95, arms=("hi", "down"), cane=True) + klaus(146, G-10, s=.9, arms=("down", "hi"))
            + lilli(182, G-14, s=.75, arms=("hi", "down")))

@sc("bis-morgen", "dusk")
def _():
    return (sky(C["lavender"], 60) + moon(170, 26, 12) + doorway(4, G, 42, 96, inside=C["yellow"])
            + rosa(66, G, arms=("down", "wave"), handc=(INK, C["amber"])) + amir(156, G, s=1.15, arms=("wave", "down"), bag=None)
            + bubble(84, 6, 62, 44, 80, 70, calendar(90, 14, 30, 26, C["orange"], (1, 3)) + sun(132, 30, 6, False)))

@sc("bis-spaeter", "cream")
def _():
    return (grass(G+2, C["green"]) + amir(110, G, arms=("wave", "low"), handc=(C["orange"], INK)) + P("M150 130 h18 M146 146 h24 M152 162 h16", C["grey"], 2.6)
            + rosa(30, G, s=1.0, arms=("down", "hi"))
            + bubble(118, 14, 50, 44, 112, 70, clock(143, 36, 15, 5, 0, C["blue"])))

@sc("bis-bald", "pink")
def _():
    return (grass(G+2, C["green"]) + rosa(64, G, arms=("down", "wave"), handc=(INK, C["rasp"])) + motion(98, 50, C["rasp"], 1, .8)
            + malik(160, G, s=1.1, arms=("wave", "down"))
            + bubble(10, 8, 64, 40, 54, 72, hourglass(28, 28) + heart(54, 30, .7, C["red"])))

@sc("gute-nacht", "night")
def _():
    return (window(130, 20, 52, 46, C["tan"], "#33496f") + moon(156, 42, 11) + star(140, 30, 3) + star(172, 58, 2.6)
            + bed(30, 178, 120, C["purple"]) + sleephead(44, 152, 1.0) + zzz(66, 118)
            + rosa(170, G, s=1.1, arms=("low", "down"), face="smile"))

@sc("schoenes-wochenende", "yellow")
def _():
    return (sun(30, 30, 13) + grass(G+2, C["green"]) + rosa(52, G, arms=("down", "wave"), handc=(INK, C["amber"]))
            + amir(150, G-24, s=.85, arms=("wave", "fwd"), handc=(C["orange"], INK)) + bike2(150, G, C["teal"])
            + bubble(84, 8, 64, 46, 76, 76, calendar(91, 16, 36, 30, C["red"], None, True) + sun(136, 30, 6, False)))

@sc("anrede", "cream")
def _():
    return (grass(G+2, C["green"]) + lilli(30, G, s=.85, arms=("down", "down")) + amir(100, G, arms=("low", "low"))
            + brandl(166, G, cane=True, arms=("down", "low"))
            + bubble(28, 16, 46, 30, 86, 70, word("du", 51, 37, 17)) + bubble(116, 16, 50, 30, 114, 70, word("Sie", 141, 37, 17)))

@sc("hand-geben", "lav")
def _():
    return (grass(G+2, C["green"]) + rosa(62, G, arms=("down", (30, 14))) + amir(140, G, arms=((30, 14), "down"))
            + dot(101, 113, 6.5, C["red"]) + P("M92 98 l-4 -7 M101 96 v-9 M110 98 l4 -7", C["orange"], 2.4))

@sc("es-geht-so", "grey")
def _():
    return (cloud(70, 44, 1.6, C["lgrey"]) + sun(118, 32, 12, False) + cloud(96, 52, 1.5, C["lgrey"])
            + grass(G+2, C["olive"]) + klaus(96, G, arms=("down", "hi"), face="meh")
            + P("M128 92 q6 -8 12 0 q6 8 12 0", C["orange"], 2.6) + P("M124 104 l6 -3 M162 88 l-6 3", C["orange"], 2))

@sc("hallo-zusammen", "mint")
def _():
    o = amir(40, G, arms=("down", "up"), handc=(INK, C["orange"]), face="big") + motion(70, 48, C["orange"], 1, .8)
    o += person(110, 150, .75, body="dress", c=C["rasp"], hair=("long", C["amber"]), arms=("hi", "down"))
    o += person(140, 150, .75, body="shirt", c=C["blue"], hair=("spiky", C["hbrown"]), arms=("down", "hi"))
    o += person(170, 150, .75, body="dress", c=C["purple"], hair=("curly", C["black"]), arms=("hi", "down"))
    o += fillrect(92, 140, 100, 12, C["wood"], ow=3) + P("M100 152 v32 M184 152 v32", C["wood"], 4)
    o += cup(118, 140, C["red"], False, .6) + cup(160, 140, C["blue"], False, .6)
    return o

@sc("bis-dann", "blue")
def _():
    return (grass(G+2, C["green"]) + amir(56, G, arms=("down", "wave"), handc=(INK, C["orange"])) + malik(150, G, arms=("wave", "down"))
            + bubble(66, 8, 70, 44, 66, 66, calendar(72, 16, 30, 28, C["teal"], (1, 2)) + clock(120, 30, 11, 3, 0)))

@sc("morgen", "peach")
def _():
    return (sun(118, 120, 26, True) + ground(126, C["lgreen"]) + P("M0 130 Q60 112 120 132 T200 120", C["green"], 3)
            + fence(10, 70, 176) + rooster(40, 146) + bird(150, 40, C["navy"]) + bird(170, 54, C["navy"], .8)
            + flower(150, 180, C["rasp"]) + flower(176, 184, C["yellow"]))

@sc("tag", "blue")
def _():
    return (sun(100, 34, 18) + cloud(20, 60, 1.2) + cloud(156, 64, 1) + ground(150, C["lgreen"])
            + tree(160, 170, C["green"]) + house(16, 172, 60, 44, C["ochre"], C["coral"]) + flower(100, 186, C["rasp"]) + flower(120, 182, C["yellow"])
            + bird(110, 80, C["navy"]))

@sc("abend", "dusk")
def _():
    return (sky(C["lilac"], 90) + P("M0 92 H200", C["amber"], 3) + sun(100, 108, 22, False, C["dorange"], C["orange"], 0)
            + ground(118, C["olive"]) + house(116, 176, 62, 46, C["tan"], C["plum"], lit=True) + star(30, 24, 5, C["yellow"]) + star(160, 16, 4, C["yellow"])
            + bird(30, 60, C["night"]) + tree(40, 180, C["dgreen"]))

@sc("nacht", "night")
def _():
    return (moon(150, 40, 18) + star(30, 30, 5) + star(70, 16, 3.4) + star(100, 54, 4) + star(186, 92, 3) + star(20, 90, 3)
            + house(16, 184, 62, 50, "#33496f", C["violet"], C["brown"], "#1c2741") + tree(156, 186, "#2f5d3a", C["brown"]) + owl(148, 146)
            + P("M0 186 H200", "#33496f", 4))

@sc("danke", "mint")
def _():
    return (grass(G+2, C["green"]) + rosa(52, G, arms=("down", (26, 10))) + gift(96, 104, 22, C["blue"], C["yellow"])
            + amir(150, G, arms=((28, 10), "chest"), face="big") + heart(112, 40, 1.2, C["red"]) + sparkle(84, 50, C["amber"]) + sparkle(144, 30, C["amber"]))

@sc("bitte", "peach")
def _():
    return (table(10, 150, 70) + cup(30, 150, C["blue"], False, .8) + rosa(66, G, arms=("down", (32, 4))) + cup(120, 116, C["red"], True, 1.2)
            + amir(166, G, s=1.15, arms=((14, 2), "down"), face="smile"))

@sc("hand", "white")
def _():
    hand_d = "M88 196 L86 150 L72 122 L74 110 L84 112 L94 136 L92 92 L100 88 L104 130 L106 80 L114 80 L114 130 L120 90 L128 92 L124 138 L134 106 L142 110 L134 158 L124 196 Z"
    i = uid("h")
    cols = [C["red"], C["orange"], C["yellow"], C["green"], C["blue"]]
    o = f'<g transform="translate(-32,-52) scale(1.25)"><clipPath id="{i}"><path d="{hand_d}"/></clipPath><g clip-path="url(#{i})">'
    bands = [(56, 98), (98, 112), (112, 125), (125, 138), (138, 170)]
    for (a, b), c in zip(bands, cols):
        x = a; z = f"M{x} 220"; up = True
        while x < b:
            x += 3; z += f" L{x} {60 if up else 220}"; up = not up
        o += P(z, c, 3.2)
    o += "</g>" + f'{P(hand_d, INK, 3)}{dot(100, 160, 2.2)}{dot(116, 160, 2.2)}{P("M98 168 Q108 176 118 168", INK, 2)}</g>'
    return o + sparkle(36, 40, C["purple"], 6) + sparkle(170, 60, C["rasp"], 5) + sparkle(160, 160, C["amber"], 5)

@sc("herzlich", "pink")
def _():
    return (grass(G+2, C["green"]) + rosa(100, G, s=1.4, arms=("up", "up"), face="big", eyes="happy")
            + heart(100, 118, .9, C["red"]) + heart(40, 50, .8, C["rasp"]) + heart(160, 44, 1, C["red"]) + heart(30, 120, .6, C["red"]) + heart(172, 116, .7, C["rasp"]))

@sc("machs-gut", "mint")
def _():
    return (grass(G+2, C["green"]) + rosa(54, G, arms=("down", "wave"), handc=(INK, C["amber"]))
            + amir(154, G, s=1.15, arms=("wave", "down"), bag=C["orange"]) + suitcase(166, G)
            + bubble(80, 10, 60, 38, 70, 70, heart(98, 30, .7, C["red"]) + clover(122, 28)))

@sc("freundlich", "yellow")
def _():
    return (doorway(116, G, 44, 104, inside=C["lemon"]) + grass(G+2, C["green"]) + amir(84, G, s=1.35, arms=("out", (26, 0)), face="big", eyes="happy")
            + sparkle(30, 50, C["orange"], 6) + sparkle(140, 40, C["rasp"], 5) + sparkle(30, 140, C["blue"], 5) + sun(176, 24, 10))

@sc("nett", "pink")
def _():
    return (grass(G+2, C["green"]) + amir(60, G, arms=("down", (28, 0))) + flower(104, 118, C["rasp"], C["green"], 1.3)
            + rosa(150, G, arms=((14, 4), "down"), face="smile")
            + think(108, 6, 60, 40, 140, 66, heart(126, 28, .7, C["red"]) + smiley(152, 26, 7)))

@sc("sich-bedanken", "peach")
def _():
    return (rosa(56, G, arms=("down", "down"), face="smile") + amir(140, G, arms=((18, 6), "chest"), face="smile")
            + cup(116, 120, C["red"], True, 1) + bubble(110, 6, 50, 40, 132, 70, heart(135, 28, .9, C["red"])) + grass(G+2, C["green"]))

@sc("auf-wiederhoeren", "blue")
def _():
    o = fillrect(130, 150, 56, 36, C["wood"], ow=3) + phone(158, 142, C["red"], 1.1) + P("M150 146 q-30 30 -60 -20", C["red"], 2)
    o += rosa(84, G, s=1.35, arms=("wave", (6, -30)), handc=(C["amber"], INK), face="smile")
    o += solid("M98 70 l10 -4 l2 8 l-10 2 Z", C["red"]) + waves(114, 72, C["blue"]) + motion(46, 64, C["orange"], -1, .8)
    return o

@sc("lange-nicht-gesehen", "peach")
def _():
    o = grass(G+2, C["green"]) + rosa(52, G, arms=("up", "up"), face="open") + clara(148, G, arms=("out", "out"), face="big") + suitcase(174, G)
    for k, (x, y, a) in enumerate(((84, 40, -12), (104, 20, 8), (124, 48, -6), (96, 70, 14))):
        o += f'<g transform="rotate({a} {x} {y})">' + calendar(x-10, y-8, 20, 18, C["red"]) + "</g>"
    return o

@sc("sympathisch", "mint")
def _():
    return (grass(G+2, C["green"]) + malik(100, G, s=1.35, arms=("hi", "down"), face="big")
            + petra(28, G, s=.9, arms=("down", "down")) + klaus(174, G, s=.9, arms=("down", "down"))
            + think(2, 40, 40, 28, 26, 96, heart(22, 56, .55, C["red"])) + think(156, 40, 40, 28, 172, 96, heart(176, 56, .55, C["red"]))
            + sparkle(140, 50, C["amber"]))

@sc("besuch", "cream")
def _():
    return (doorway(8, G, 44, 100) + grass(G+2, C["green"]) + rosa(70, G, s=1.2, arms=("down", "out"), face="big")
            + clara(116, G, s=1, arms=((16, 4), "down")) + bouquet(132, 118)
            + klaus(150, G, s=.95, arms=("down", "down")) + lilli(186, G, s=.7, arms=("hi", "down"))
            + garland(4, 60, 76))

@sc("nachbar", "blue")
def _():
    return (house(118, 176, 72, 70, C["tan"], C["teal"]) + f'<rect x="128" y="112" width="26" height="24" fill="{C["ice"]}" stroke="{INK}" stroke-width="2.4"/>'
            + person(141, 140, .45, body="shirt", c=C["orange"], hair=("short", C["hbrown"]), arms=("down", "wave"), handc=(INK, C["orange"]))
            + fence(94, 110, G) + grass(G+2, C["green"]) + rosa(54, G, arms=("down", "wave"), handc=(INK, C["amber"])) + motion(88, 54, C["orange"], 1, .7))

@sc("formell", "grey")
def _():
    return (grass(G+2, C["olive"]) + person(96, G, 1.4, body="shirt", c=C["night"], c2=C["night"], hair=("short", C["dgrey"]), tie=C["red"],
            arms=("down", "down"), face="line", bag=C["brown"], blush=False)
            + bubble(118, 16, 56, 34, 112, 70, word("Sie", 146, 40, 19)))

@sc("moin", "blue")
def _():
    return ('<g transform="translate(-20,-56) scale(1.35)">' + lighthouse(48, 160) + "</g>" + sea(158) + scribble("M92 162 Q150 150 200 156 L200 200 L92 200 Z", (92, 150, 200, 200), C["sand"], outline=False, w=3, step=4) + bird(120, 30, C["dgrey"]) + bird(150, 46, C["dgrey"], .8)
            + person(140, G-6, 1.15, body="shirt", c=C["navy"], c2=C["dgrey"], hair=("short", C["amber"]), hat=("cap", C["navy"]), arms=("down", "wave"), handc=(INK, C["amber"]), beard=C["amber"]))

@sc("servus", "lav")
def _():
    return (wheel(70, 72, 48) + grass(G+2, C["green"]) + hannah(150, G, arms=("down", "wave"), handc=(INK, C["rasp"]), face="big") + motion(184, 58, C["rasp"], 1, .6))

@sc("duzen", "yellow")
def _():
    return (grass(G+2, C["green"]) + amir(66, G, arms=("down", (14, -30)), handc=(INK, C["orange"]), face="big") + malik(136, G, arms=((14, -30), "down"), handc=(C["orange"], INK), face="big")
            + sparkle(101, 50, C["orange"], 6) + bubble(4, 18, 44, 30, 50, 70, word("du", 26, 39, 17)) + bubble(150, 18, 44, 30, 150, 70, word("du", 172, 39, 17)))

@sc("siezen", "cream")
def _():
    return (grass(G+2, C["green"]) + f'<g transform="rotate(8 60 186)">' + amir(60, G, arms=("down", (16, 14)), face="smile") + "</g>"
            + brandl(148, G, cane=True, arms=("down", "low"))
            + bubble(76, 12, 52, 34, 80, 70, word("Sie", 102, 36, 19)))

@sc("schoenen-tag-noch", "blue")
def _():
    return (sun(178, 22, 12) + amir(50, 182, s=1.1, arms=("down", "wave"), handc=(INK, C["orange"])) + counter(10, G, 84)
            + fillrect(20, 140, 14, 12, C["yellow"], ow=2.2) + grass(G+2, C["green"], 100, 200)
            + brandl(150, G, arms=("hi", "down"), bag=None) + fillrect(122, 152, 16, 16, C["rasp"], ow=2.4))

@sc("schoenen-feierabend", "dusk")
def _():
    o = sky(C["amber"], 60) + sun(40, 62, 14, False, C["dorange"], C["orange"], 0)
    o += fillrect(100, 30, 90, 156, C["lgrey"], ow=3)
    for r_ in range(4):
        for k in range(3):
            o += f'<rect x="{110+k*26}" y="{40+r_*26}" width="16" height="14" fill="{C["yellow"] if (r_+k) % 2 else C["ice"]}" stroke="{INK}" stroke-width="2"/>'
    o += clock(145, 18, 12, 6, 0, C["blue"]) + grass(G+2, C["green"], 0, 100)
    o += rosa(70, G, s=1.2, arms=("down", "wave"), handc=(INK, C["amber"])) + petra(160, G, s=.95, arms=("hi", "down"), bag=C["brown"])
    return o

@sc("sich-verabschieden", "dusk")
def _():
    return (sky(C["lavender"], 56) + moon(176, 20, 10) + doorway(4, G, 40, 98, inside=C["yellow"]) + grass(G+2, C["green"])
            + amir(66, G, arms=("down", (26, 8))) + klaus(118, G, s=1.1, arms=((24, 10), "down")) + brandl(170, G, s=1, arms=("down", "wave"), handc=(INK, C["violet"])))

@sc("ansprechen", "mint")
def _():
    return (grass(G+2, C["green"]) + person(150, G, 1.2, body="dress", c=C["coral"], hair=("long", C["black"]), arms=((12, 2), (12, 2)), face="o")
            + fillrect(134, 112, 32, 20, C["blue"], ow=2.4) + P("M150 112 v20", INK, 2)
            + amir(64, G, arms=("down", "hi"), face="smile") + bubble(80, 18, 48, 30, 76, 70, dot(94, 33, 2.4) + dot(104, 33, 2.4) + dot(114, 33, 2.4)))

@sc("hoeflich", "lav")
def _():
    return (doorway(120, G, 46, 108, inside=C["lemon"]) + grass(G+2, C["green"])
            + f'<g transform="rotate(10 100 186)">' + amir(100, G, arms=((28, 2), "chest"), face="smile") + "</g>"
            + brandl(44, G, cane=False, arms=("down", "low"), face="smile") + P("M18 186 L22 120 q4 -6 8 0", C["wood"], 3.2) + sparkle(150, 40, C["amber"]))

@sc("unhoeflich", "grey")
def _():
    return (doorway(6, G, 40, 96) + grass(G+2, C["olive"]) + rosa(64, G, s=1.2, arms=("down", "hi"), face="sad")
            + person(150, G, 1.25, body="shirt", c=C["dgrey"], c2=C["night"], hair=("short", C["black"]), arms=("chest", "chest"), face="frown", eyes="side", blush=False)
            + excl(110, 50, C["red"], 1.3) + P("M178 112 h16 M180 128 h14", C["grey"], 2.6))

@sc("locker", "yellow")
def _():
    return (amir(70, 178, s=1, arms=("hi", "down"), face="big") + petra(124, 178, s=1, arms=("down", "up"), face="big", eyes="happy") + sofa(30, 176, 130, C["coral"])
            + notes(40, 60) + notes(150, 50, C["blue"]) + cup(180, 120, C["teal"], True, .8) + P("M0 186 H200", C["wood"], 3))

@sc("winken", "blue")
def _():
    return (house(20, 186, 112, 120, C["ochre"], C["red"], C["wood"], C["ice"], doorw=0.01).replace('width="10" height="10"', 'width="0" height="0"')
            + f'<rect x="34" y="90" width="58" height="52" fill="{C["ice"]}" stroke="{INK}" stroke-width="3"/>'
            + lilli(62, 152, .62, arms=("down", "wave"), handc=(INK, C["rasp"]), face="big") + f'<rect x="34" y="142" width="58" height="6" fill="{C["wood"]}"/>'
            + motion(84, 98, C["rasp"], 1, .6) + amir(164, G, s=1.1, arms=("wave", "down"), handc=(C["orange"], INK)))

@sc("abschied", "dusk")
def _():
    o = sky(C["lilac"], 50) + star(20, 20, 4, C["yellow"]) + grass(G+2, C["green"])
    o += clara(52, G, arms=("wave", "down"), handc=(C["rasp"], INK), face="sad") + suitcase(70, G)
    o += rosa(124, G, s=1.1, arms=("down", "wave"), handc=(INK, C["amber"]), face="sad") + petra(176, G, s=1, arms=("down", "wave"))
    o += solid("M132 106 q-3 5 0 8 q3 -3 0 -8 Z", C["blue"])
    return o

@sc("umarmen", "pink")
def _():
    return (grass(G+2, C["green"]) + petra(118, G, arms=((-14, 6), "down"), face="smile", eyes="closed") + rosa(84, G, arms=("down", (26, 2)), face="big", eyes="happy")
            + heart(100, 40, 1, C["red"]) + heart(60, 30, .6, C["rasp"]) + heart(146, 28, .7, C["rasp"]))

@sc("sich-melden", "peach")
def _():
    return (grass(G+2, C["green"]) + rosa(54, G, arms=("down", (8, -26)), face="smile")
            + amir(152, G, s=1.15, arms=("wave", (14, 6)), handc=(C["orange"], INK)) + mobile(178, 122, C["night"], 1)
            + bubble(68, 6, 56, 42, 64, 62, mobile(86, 27, C["red"]) + P("M96 20 q5 7 0 14 M102 16 q8 11 0 22", C["blue"], 2)))

@sc("haendedruck", "cream")
def _():
    o = scribble("M0 120 L62 106 L70 130 L0 148 Z", (0, 100, 70, 150), C["blue"], ow=3)
    o += scribble("M200 118 L138 104 L130 128 L200 146 Z", (130, 100, 200, 150), C["red"], ow=3)
    o += f'<path d="M66 106 Q84 92 102 96 L134 104 Q140 118 132 132 L104 136 Q84 138 70 130 Z" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'
    o += P("M96 100 q12 -2 20 6 M92 112 q14 -2 24 6 M92 122 q14 -2 22 6", INK, 2.2) + P("M100 96 q-8 -10 4 -12 q10 0 6 10", INK, 2.6)
    o += P("M84 76 l-6 -10 M100 70 v-12 M116 76 l6 -10", C["orange"], 2.6) + P("M70 160 q30 14 60 0", C["grey"], 2.2)
    return o

@sc("begruessen", "mint")
def _():
    return (doorway(6, G, 44, 104) + grass(G+2, C["green"]) + rosa(74, G, s=1.3, arms=("out", "out"), face="big")
            + brandl(160, G, arms=("hi", "down"), cane=True) + sparkle(120, 40, C["amber"]))

@sc("begruessung", "peach")
def _():
    return (doorway(6, G, 48, 106) + garland(2, 62, 80) + grass(G+2, C["green"]) + rosa(82, G, arms=("down", (26, 4)))
            + tray(124, 122) + amir(166, G, s=1.15, arms=("hi", "down"), bag=None))

@sc("herzlich-begruessen", "pink")
def _():
    return (doorway(6, G, 44, 104) + grass(G+2, C["green"]) + amir(120, G, s=1.2, arms=((-16, 6), "down"), face="big", eyes="happy", bag=C["orange"])
            + rosa(90, G, arms=("down", (26, 0)), face="big", eyes="happy") + heart(106, 36, 1, C["red"]) + heart(150, 50, .6, C["rasp"]) + heart(66, 46, .6, C["rasp"]))

@sc("vertraut", "cream")
def _():
    return (house(110, 180, 80, 64, C["ochre"], C["teal"], C["wood"]) + heart(150, 86, .8, C["red"]) + grass(G+2, C["green"])
            + amir(66, G, arms=("down", "fwd"), face="big", eyes="happy") + P("M100 128 l6 4 M104 128 v8", C["amber"], 3) + dot(99, 126, 3.4, C["amber"])
            + cat(30, G))

@sc("gruess-gott", "blue")
def _():
    return (mountains(130) + ground(130, C["lgreen"]) + person(128, G, 1.05, body="topskirt", c=WHITE, c2=C["green"], hair=("pigtails", C["amber"]), arms=("hi", "down"), face="big")
            + counter(96, G, 100) + pretzel(176, 140)
            + amir(48, G, s=1.15, arms=("down", "hi")))

@sc("zunicken", "mint")
def _():
    return (grass(G+2, C["green"]) + amir(60, G, arms=("down", "hi")) + guenter(144, G, arms=("down", "down"), face="smile")
            + P("M120 56 q-6 12 0 24 M168 56 q6 12 0 24", C["orange"], 2.6) + arrow(144, 34, 144, 50, C["orange"]))

@sc("smalltalk", "yellow")
def _():
    return (grass(G+2, C["green"]) + amir(50, G, arms=("down", (20, 2))) + cup(80, 120, C["red"], True, .8)
            + klaus(150, G, arms=((20, 2), "down")) + cup(120, 120, C["blue"], True, .8)
            + bubble(10, 8, 54, 36, 46, 66, sun(28, 26, 6, False) + cloud(36, 32, .7, C["lgrey"]))
            + bubble(138, 8, 54, 36, 150, 66, cloud(150, 30, .7, C["lgrey"]) + P("M156 34 l-2 6 M164 34 l-2 6 M172 34 l-2 6", C["blue"], 2)))

@sc("du-anbieten", "pink")
def _():
    return (grass(G+2, C["green"]) + rosa(60, G, arms=("down", (30, 10)), face="big") + amir(146, G, arms=("down", "down"), face="o")
            + bubble(4, 10, 50, 34, 50, 68, word("du", 29, 33, 18)) + excl(146, 40, C["orange"]) + sparkle(104, 108, C["amber"]) + heart(104, 92, .5, C["red"]))

@sc("tschau", "lav")
def _():
    return (doorway(10, G, 44, 100) + grass(G+2, C["green"]) + teen(110, G-8, arms=("wave", "down"), handc=(C["red"], INK), face="big") + skate(110, G-4)
            + P("M150 110 h22 M146 126 h28 M152 142 h20", C["grey"], 2.6))

@sc("per-du-sein", "peach")
def _():
    return (grass(G+2, C["green"]) + rosa(76, G, arms=("down", (18, -6)), face="big") + petra(124, G, arms=((18, -6), "down"), face="big")
            + bubble(6, 10, 48, 32, 60, 66, word("du", 30, 32, 17)) + bubble(146, 10, 48, 32, 140, 66, word("du", 170, 32, 17)) + heart(100, 40, .9, C["red"]))

@sc("distanziert", "grey")
def _():
    return (grass(G+2, C["olive"]) + person(30, G, 1, body="dress", c=C["rasp"], hair=("long", C["amber"]), arms=("down", "hi"), face="big")
            + person(62, G, 1, body="shirt", c=C["teal"], hair=("spiky", C["hbrown"]), arms=("hi", "down"), face="big") + notes(46, 60)
            + P("M96 100 V180", C["grey"], 2.6, extra='stroke-dasharray="5 7"')
            + person(156, G, 1.25, body="shirt", c=C["navy"], c2=C["dgrey"], hair=("short", C["black"]), arms=("chest", "chest"), face="line", eyes="side", blush=False))

@sc("foermlich", "cream")
def _():
    o = rathaus(120, 80, 66) + envelope(22, 100, 120, 78)
    for k in range(3):
        o += P(f"M{34+k*0} {192+k*0} h0", INK, 1)
    return o + bubble(10, 14, 58, 34, 40, 100, word("Sie", 39, 38, 19))

@sc("fluechtig-kennen", "blue")
def _():
    return (grass(G+2, C["green"]) + amir(50, G, arms=("down", "hi"), face="smile", eyes="side") + P("M18 100 h-14 M22 116 h-18", C["grey"], 2.6)
            + malik(150, G, arms=("hi", "down"), face="smile", eyes="side") + P("M184 100 h14 M180 116 h18", C["grey"], 2.6)
            + think(78, 12, 44, 34, 66, 64, qmark(100, 30, C["blue"])))

@sc("ins-gespraech-kommen", "peach")
def _():
    o = fillrect(70, 140, 60, 10, C["wood"], ow=3) + P("M80 150 v34 M120 150 v34", C["wood"], 4)
    o += amir(40, G, arms=("down", (22, 2)), face="big") + guenter(160, G, arms=((22, 2), "down"), face="big")
    o += cup(86, 140, C["red"], True, .7) + cup(114, 140, C["blue"], True, .7)
    o += bubble(18, 8, 44, 24, 40, 60, dot(32, 20, 2) + dot(40, 20, 2) + dot(48, 20, 2))
    o += bubble(138, 8, 44, 24, 160, 60, dot(152, 20, 2) + dot(160, 20, 2) + dot(168, 20, 2))
    o += bubble(74, 36, 52, 26, 100, 90, smiley(92, 49, 6) + heart(110, 50, .45, C["red"]))
    return o

@sc("sich-blicken-lassen", "yellow")
def _():
    o = f'<rect x="120" y="50" width="70" height="136" fill="{C["lemon"]}" opacity="0.6"/>' + P("M120 186 V50 H190 V186", C["wood"], 5)
    o += scribble("M146 52 L190 52 L190 186 L146 186 Z", (146, 52, 190, 186), C["tan"], ow=3)
    o += f'<g>{person(132, 186, 1.1, body="shirt", c=C["brown"], c2=C["dgrey"], hair=("bald", C["lgrey"]), beard=C["lgrey"], arms=("none", "none"), face="smile", eyes="side")}</g>'
    o += scribble("M146 52 L190 52 L190 186 L146 186 Z", (146, 52, 190, 186), C["tan"], ow=3) + dot(152, 120, 2.2)
    o += rosa(56, G, arms=("down", "up"), face="open", handc=(INK, C["amber"])) + excl(96, 50, C["red"]) + grass(G+2, C["green"], 0, 118)
    return o

@sc("kurz-angebunden", "grey")
def _():
    return (person(130, G, 1.2, body="shirt", c=C["navy"], c2=C["night"], hair=("short", C["dgrey"]), tie=C["dred"], arms=((6, -26), "down"), face="frown", blush=False)
            + solid("M136 74 l8 -6 l4 4 l-8 6 Z", C["dgrey"])
            + fillrect(90, 140, 100, 12, C["wood"], ow=3) + P("M100 152 v34 M180 152 v34", C["wood"], 4) + phone(166, 132, C["dgrey"], 1)
            + bubble(152, 22, 36, 26, 150, 66, P("M162 35 h14", INK, 3)) + excl(40, 70, C["red"], 1.5) + P("M30 120 q20 -10 40 0", C["grey"], 2))

@sc("zuwinken", "mint")
def _():
    return (grass(G+2, C["green"]) + petra(132, G-24, s=.85, arms=("wave", "fwd"), handc=(C["amber"], INK), face="big") + bike2(132, G, C["red"])
            + motion(102, 70, C["amber"], -1, .7) + P("M176 130 h18 M172 146 h22", C["grey"], 2.6)
            + rosa(40, G, s=1.1, arms=("down", "wave"), handc=(INK, C["amber"])))

@sc("umgangsform", "cream")
def _():
    o = board(14, 14, 172, 92)
    o += chalkman(40, 92, (12, -2)) + chalkman(64, 92, (-12, -2)) + P("M112 52 l8 10 l14 -22", C["lgreen"], 4)
    o += chalkman(150, 92, (8, -14)) + P("M164 48 q6 6 4 14", WHITE, 1.8) + P("M96 30 v60", WHITE, 1.2, extra='stroke-dasharray="3 4"')
    o += grass(G+2, C["green"]) + rosa(150, G, s=1.05, arms=((-24, -26), "down"), face="smile")
    o += person(50, G, .8, body="shirt", c=C["blue"], hair=("spiky", C["black"]), arms=("down", "hi")) + person(90, G, .8, body="dress", c=C["rasp"], hair=("pigtails", C["hbrown"]), arms=("down", "down"))
    return o

@sc("floskel", "blue")
def _():
    return (grass(G+2, C["green"]) + amir(140, G, arms=("hi", "down"), face="smile", eyes="side") + P("M176 100 h16 M178 116 h14 M174 132 h18", C["grey"], 2.6)
            + bubble(120, 10, 44, 34, 132, 66, qmark(136, 26, C["blue"], .9) + smiley(152, 28, 5))
            + klaus(50, G, arms=("down", "hi"), face="o") + think(6, 12, 60, 36, 40, 66, dot(22, 30, 2) + dot(32, 30, 2) + dot(42, 30, 2) + dot(52, 30, 2)))

@sc("etikette", "lav")
def _():
    o = '<g transform="translate(-50,-6) scale(1.5)">' + chandelier(100, 30) + "</g>" + P("M0 186 H200", C["dred"], 3) + scribble("M60 186 L140 186 L150 200 L50 200 Z", (50, 186, 150, 200), C["red"], outline=False)
    o += f'<g transform="rotate(-8 56 186)">' + person(56, G, 1.25, body="shirt", c=C["black"], c2=C["black"], hair=("short", C["hbrown"]), tie=C["dred"], arms=("down", "chest"), face="smile") + "</g>"
    o += f'<g transform="rotate(8 146 186)">' + person(146, G, 1.25, body="dress", c=C["purple"], hair=("bun", C["black"]), arms=("chest", "down"), face="smile") + "</g>"
    o += sparkle(100, 100, C["amber"], 6)
    return o

@sc("ueberschwaenglich", "pink")
def _():
    return (grass(G+2, C["green"]) + tom(132, G, arms=("out", "out"), face="o") + hannah(86, G, arms=("up", (32, -2)), face="big", eyes="happy")
            + lips(150, 70) + lips(168, 92) + lips(150, 112) + heart(40, 40, .8, C["red"]) + heart(110, 26, .6, C["rasp"])
            + sparkle(30, 100, C["amber"], 6) + sparkle(180, 40, C["orange"], 6) + sparkle(20, 150, C["purple"], 5))

@sc("wie-gehts", "cream")
def _():
    return (grass(G+2, C["green"]) + rosa(60, G, arms=("down", (24, 2)), face="smile") + amir(150, G, arms=("down", "down"), face="smile")
            + bubble(60, 6, 80, 42, 72, 70, qmark(78, 26, C["blue"], 1) + smiley(102, 27, 8, C["amber"], "smile") + smiley(124, 27, 8, C["lgrey"], "sad")))

@sc("und-dir", "mint")
def _():
    return (grass(G+2, C["green"]) + amir(56, G, arms=("down", "point"), face="big", handc=(INK, INK)) + malik(150, G, arms=("down", "down"), face="smile", s=1.2)
            + bubble(14, 6, 76, 40, 52, 70, smiley(32, 26, 8) + qmark(70, 25, C["blue"], 1)))

@sc("und-ihnen", "lav")
def _():
    return (grass(G+2, C["green"]) + amir(52, G, arms=("down", (30, 4)), face="smile")
            + guenter(150, G, arms=("down", "down"), face="smile", cane=True, hat="top")
            + bubble(8, 6, 76, 40, 48, 70, smiley(26, 26, 8) + qmark(64, 25, C["violet"], 1)))

# слово → ключ сцены
KEYS = {
 "hallo": "hallo", "tschüss": "tschuess", "Guten Morgen": "guten-morgen", "Guten Tag": "guten-tag", "Guten Abend": "guten-abend",
 "Auf Wiedersehen": "auf-wiedersehen", "Mir geht's gut": "mir-gehts-gut", "grüßen": "gruessen", "Bis morgen": "bis-morgen",
 "bis später": "bis-spaeter", "Bis bald": "bis-bald", "Gute Nacht": "gute-nacht", "Schönes Wochenende": "schoenes-wochenende",
 "die Anrede": "anrede", "die Hand geben": "hand-geben", "Es geht so": "es-geht-so", "Hallo zusammen": "hallo-zusammen",
 "Bis dann": "bis-dann", "der Morgen": "morgen", "der Tag": "tag", "der Abend": "abend", "die Nacht": "nacht", "danke": "danke",
 "bitte": "bitte", "die Hand": "hand", "herzlich": "herzlich", "Mach's gut": "machs-gut", "freundlich": "freundlich", "nett": "nett",
 "sich bedanken": "sich-bedanken", "auf Wiederhören": "auf-wiederhoeren", "lange nicht gesehen": "lange-nicht-gesehen",
 "sympathisch": "sympathisch", "der Besuch": "besuch", "der Nachbar": "nachbar", "formell": "formell", "Moin": "moin", "Servus": "servus",
 "duzen": "duzen", "siezen": "siezen", "Schönen Tag noch": "schoenen-tag-noch", "Schönen Feierabend": "schoenen-feierabend",
 "sich verabschieden": "sich-verabschieden", "ansprechen": "ansprechen", "höflich": "hoeflich", "unhöflich": "unhoeflich", "locker": "locker",
 "winken": "winken", "der Abschied": "abschied", "umarmen": "umarmen", "sich melden": "sich-melden", "der Händedruck": "haendedruck",
 "begrüßen": "begruessen", "die Begrüßung": "begruessung", "jemanden herzlich begrüßen": "herzlich-begruessen", "vertraut": "vertraut",
 "Grüß Gott": "gruess-gott", "zunicken": "zunicken", "der Smalltalk": "smalltalk", "das Du anbieten": "du-anbieten", "Tschau": "tschau",
 "per Du sein": "per-du-sein", "distanziert": "distanziert", "förmlich": "foermlich", "sich flüchtig kennen": "fluechtig-kennen",
 "ins Gespräch kommen": "ins-gespraech-kommen", "sich blicken lassen": "sich-blicken-lassen", "kurz angebunden": "kurz-angebunden",
 "zuwinken": "zuwinken", "die Umgangsform": "umgangsform", "die Floskel": "floskel", "die Etikette": "etikette",
 "überschwänglich": "ueberschwaenglich", "Wie geht's?": "wie-gehts", "Und dir?": "und-dir", "Und Ihnen?": "und-ihnen",
}
