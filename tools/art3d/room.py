# Вечер в комнате: семья сидит вокруг низкого стола, Малыш рисует. Ролик-петля + положение листа на столе для сайта.
#   cd tools/art3d && python3 room.py ../../words/img/fam      → <lang>/room.webp, room_still.webp и ../../words/data/room.json
import json, math, os, sys
import numpy as np
from PIL import Image
from ray import Scene, draw
import toys
from toys import Toy, WHO, SCALE, NICK, body, HC, HR, lerp

W, H = 640, 420
CAM = dict(center=(0, 0.8, -0.5), half=1.92, yaw=0.0, pitch=0.68)
SHEET = dict(x=(-0.36, 0.36), z=(-0.36, 0.2), y=0.515)          # лист на столе (мировые координаты)
SEATS = {   # кто: (x, z, поворот к столу, масштаб)
    "irina": (-0.58, -1.72, 0.0), "igor": (0.58, -1.72, 0.0), "vitya": (-2.2, -1.0, 0.65), "lyuda": (2.2, -1.0, -0.65),
    "danya": (-1.5, 0.85, 1.0), "nika": (1.5, 0.85, -1.0)}

def idle(who, t):
    w = math.sin(2*math.pi*t); w2 = 0.5 - 0.5*math.cos(2*math.pi*t)
    if who == "danya": return dict(pose=("down", lerp((0.58, 0.98, 0.26), (0.2, 1.2, 0.42), w2)), face="big" if w2 > 0.6 else "smile", eyes="happy" if w2 > 0.6 else "open", head=(0, -0.02*w2))
    if who == "nika": return dict(pose=("down", (0.5 - 0.15*w2, 1.5 + 0.05*w, 0.25)), eyes="happy", head=(0.02*w, 0))
    if who == "irina": return dict(pose=((0.36, 0.8, 0.2), (0.45 - 0.1*w2, 1.0 + 0.04*w, 0.34)), eyes="side" if w2 > 0.5 else "open", head=(0.02*w, 0))
    if who == "igor": return dict(pose=("down", "hold"), tape=0.04 + 0.22*w2, eyes="side" if w2 > 0.5 else "open", head=(0.02*w, 0))
    if who == "lyuda": return dict(pose=((0.24, 0.9 + 0.03*w, 0.38), (0.24, 0.9 + 0.03*w, 0.38)), eyes="happy" if w2 > 0.5 else "open", head=(0.02*w, 0.01*w2))
    if who == "vitya": return dict(pose=("down", (0.45, 1.02 + 0.06*w, 0.34)), face="o" if w2 > 0.8 else "smile", head=(0, -0.02*w2))

def room(sc):
    m = sc.mat
    sc.rbox(m("floor", (196, 150, 104)), (0, -0.05, -0.6), (4.2, 0.05, 3.2), 0.02)
    sc.cyly(m("rug", (200, 90, 70)), (0, 0.006, -0.35), 2.25, 0.006, 0.004)
    sc.cyly(m("rug2", (236, 190, 110)), (0, 0.012, -0.35), 1.7, 0.006, 0.004)
    sc.rbox(m("wall", (238, 214, 180)), (0, 2.0, -2.75), (4.2, 2.0, 0.06), 0.02)
    sc.rbox(m("frame", (138, 90, 43)), (-1.5, 2.2, -2.68), (0.5, 0.36, 0.03), 0.02); sc.rbox(m("pic", (150, 200, 220)), (-1.5, 2.2, -2.65), (0.42, 0.28, 0.02), 0.01)
    sc.sphere(m("sunpic", (245, 166, 35)), (-1.62, 2.28, -2.63), 0.09)
    sofa = m("sofa", (120, 170, 205))
    sc.rbox(sofa, (0, 0.3, -1.82), (1.25, 0.2, 0.38), 0.08); sc.rbox(sofa, (0, 0.78, -2.18), (1.3, 0.42, 0.13), 0.1)
    for sx in (-1, 1): sc.rbox(sofa, (sx*1.38, 0.5, -1.85), (0.13, 0.32, 0.42), 0.08)
    arm = m("armchair", (110, 140, 70))
    for sx in (-1, 1):
        sc.rbox(arm, (sx*2.27, 0.3, -1.03), (0.42, 0.2, 0.42), 0.08); sc.rbox(arm, (sx*2.65, 0.78, -1.03), (0.1, 0.42, 0.44), 0.08)
    pf = m("pouf", (232, 120, 100))
    for sx in (-1, 1): sc.cyly(pf, (sx*1.55, 0.26, 0.78), 0.32, 0.25, 0.08)
    tb = m("table", (150, 100, 58))
    sc.cyly(tb, (0, 0.48, -0.1), 0.85, 0.035, 0.02); sc.cyly(tb, (0, 0.24, -0.1), 0.1, 0.24, 0.02); sc.cyly(tb, (0, 0.02, -0.1), 0.35, 0.02, 0.01)
    sc.rbox(m("sheet", (251, 248, 242)), (0, SHEET["y"] - 0.004, sum(SHEET["z"])/2), ((SHEET["x"][1] - SHEET["x"][0])/2, 0.004, (SHEET["z"][1] - SHEET["z"][0])/2), 0.003)
    for k, col in enumerate(((229, 57, 53), (30, 136, 229), (67, 160, 71), (253, 216, 53))):
        sc.capsule(m(f"cr{k}", col), (0.45 + k*0.06, 0.53, -0.3), (0.48 + k*0.06, 0.53, -0.1), 0.022)
    sc.capsule(m("lamp", (90, 70, 50)), (2.75, 0.0, -1.95), (2.75, 1.9, -1.95), 0.03)
    sc.cyly(m("shade", (255, 226, 150), spec=1.0), (2.75, 2.0, -1.95), 0.32, 0.2, 0.05)
    sc.rbox(m("shelf", (120, 80, 45)), (-3.1, 1.0, -2.3), (0.45, 1.0, 0.25), 0.03)
    for k, col in enumerate(((229, 57, 53), (30, 136, 229), (245, 166, 35), (67, 160, 71), (142, 36, 77))):
        sc.rbox(m(f"book{k}", col), (-3.4 + k*0.13, 1.42, -2.15), (0.05, 0.22, 0.17), 0.01)

def malysh(sc, lang, t):
    s = 0.72; T = Toy(sc, 0, -0.95, s)
    w = math.sin(2*math.pi*t*2); w2 = math.sin(2*math.pi*t*3)
    pose = ((0.34, 0.9, 0.3), (0.15 + 0.16*w, 0.95 + 0.02*w2, 0.82 + 0.08*w2)); T.hx, T.hy = 0.01*w*s, -0.03*s
    hands = body(T, "m", (253, 216, 53), (108, 180, 224), (229, 57, 53), pose, "smile", "side")
    T.inhead = True; hair = T.m("mhair", (196, 110, 52))
    T.sphere(hair, (0, HC + 0.03, -0.02), HR + 0.012); T.above(1.62)
    T.cap(hair, (0, 1.76, 0.05), (0.06, 1.86, 0.08), 0.045); T.cap(hair, (0.06, 1.86, 0.08), (0.0, 1.9, 0.12), 0.035); T.inhead = False
    T.patch("mpatch", NICK[lang]["malysh"], (0, 0.93, 0.256), 0.17, 0.065)
    h = hands[1]; T.cap(T.m("cr0", (229, 57, 53)), (h[0], h[1] - 0.02, h[2] + 0.02), (h[0] + 0.03, h[1] - 0.12, h[2] + 0.1), 0.026)

def frame(lang, t, w=W, h=H):
    sc = Scene(); room(sc)
    for who, (x, z, yaw) in SEATS.items():
        kw = idle(who, (t + 0.17*list(SEATS).index(who)) % 1.0)
        T = Toy(sc, x, z, SCALE[who], head=kw.pop("head", (0, 0)), yaw=yaw, sit=True); T.tape = kw.pop("tape", 0.14)
        WHO[who](T, NICK[lang][who], **kw)
    malysh(sc, lang, t)
    img = draw(sc, w, h, CAM["center"], CAM["half"], yaw=CAM["yaw"], pitch=CAM["pitch"], bg=((60, 45, 35), (40, 30, 25)), light=(-0.35, 0.8, 0.55))
    return Image.fromarray((img*255).clip(0, 255).astype(np.uint8))

def project(p, w=W, h=H):
    yaw, pitch, half, c = CAM["yaw"], CAM["pitch"], CAM["half"], CAM["center"]
    cp, sp = math.cos(pitch), math.sin(pitch)
    d = (-math.sin(yaw)*cp, -sp, -math.cos(yaw)*cp); r = (math.cos(yaw), 0.0, -math.sin(yaw))
    u = (r[1]*d[2] - r[2]*d[1], r[2]*d[0] - r[0]*d[2], r[0]*d[1] - r[1]*d[0])
    q = [p[i] - c[i] for i in range(3)]
    uu = sum(q[i]*r[i] for i in range(3)); vv = sum(q[i]*u[i] for i in range(3))
    return (w/2 + uu/half*(h/2), h/2 - vv/half*(h/2))

def homography(dst):
    """Квадрат 200×200 → четырёхугольник dst (по часовой от левого верхнего) → CSS matrix3d."""
    src = [(0, 0), (200, 0), (200, 200), (0, 200)]; A = []; b = []
    for (x, y), (X, Y) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -X*x, -X*y]); b.append(X)
        A.append([0, 0, 0, x, y, 1, -Y*x, -Y*y]); b.append(Y)
    h = list(np.linalg.solve(np.array(A, float), np.array(b, float))) + [1.0]
    m = [h[0], h[3], 0, h[6], h[1], h[4], 0, h[7], 0, 0, 1, 0, h[2], h[5], 0, h[8]]
    return "matrix3d(" + ",".join(f"{v:.6f}" for v in m) + ")"

if __name__ == "__main__":
    out_root = sys.argv[1]; n = 12
    for lang in ("ru", "uk"):
        frames = [frame(lang, i/n) for i in range(n)]
        frames[0].save(os.path.join(out_root, lang, "room.webp"), save_all=True, append_images=frames[1:], duration=[140]*n, loop=0, quality=72, method=4)
        frames[0].save(os.path.join(out_root, lang, "room_still.webp"), quality=78); print(lang, flush=True)
    y = SHEET["y"]; x0, x1 = SHEET["x"]; z0, z1 = SHEET["z"]
    quad = [project((x0, y, z0)), project((x1, y, z0)), project((x1, y, z1)), project((x0, y, z1))]
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "words", "data", "room.json")
    json.dump({"w": W, "h": H, "quad": quad, "m": homography(quad)}, open(root, "w")); print("ok", quad)
