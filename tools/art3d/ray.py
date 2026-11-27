# Маленький 3D-рендер для фигурок семьи: сцена из примитивов (SDF), трассировка лучей (ray marching),
# мягкие тени, затенение углов (AO), «пластилиновая» фактура, текстуры: клетка, горошек, полоски, надпись.
import math
import numpy as np
from numba import njit, prange

# типы примитивов
SPH, CAP, RBOX, ELL, TORZ, TORY, CYLY, HALFY, RBOXZ = 0, 1, 2, 3, 4, 5, 6, 7, 8
# операции: 0 — объединение, 1 — вычесть из предыдущего, 2 — пересечь с предыдущим
NP = 16

class Scene:
    def __init__(self):
        self.prims = []; self.mats = []; self.mat_id = {}; self.texts = []
    def mat(self, name, rgb, tex=0, tp=(0, 0, 0, 0, 0, 0), spec=0.0, col2=(0, 0, 0)):
        if name in self.mat_id: return self.mat_id[name]
        self.mat_id[name] = len(self.mats)
        self.mats.append((tuple(c / 255 for c in rgb), tex, tp, spec, tuple(c / 255 for c in col2)))
        return self.mat_id[name]
    def add(self, typ, mat, params, op=0):
        row = [typ, op, mat] + list(params); row += [0.0] * (NP - len(row)); self.prims.append(row)
    # удобные примитивы
    def sphere(self, m, c, r, op=0): self.add(SPH, m, [*c, r], op)
    def capsule(self, m, a, b, r, op=0): self.add(CAP, m, [*a, *b, r], op)
    def rbox(self, m, c, h, r, op=0): self.add(RBOX, m, [*c, *h, r], op)
    def rboxz(self, m, c, h, r, ang, op=0): self.add(RBOXZ, m, [*c, *h, r, ang], op)  # повёрнутый вокруг оси z
    def ell(self, m, c, rr, op=0): self.add(ELL, m, [*c, *rr], op)
    def torz(self, m, c, R, r, op=0): self.add(TORZ, m, [*c, R, r], op)      # кольцо лицом к зрителю
    def tory(self, m, c, R, r, op=0): self.add(TORY, m, [*c, R, r], op)      # горизонтальное кольцо
    def cyly(self, m, c, r, h, rr, op=0): self.add(CYLY, m, [*c, r, h, rr], op)
    def above(self, m, y, op=2): self.add(HALFY, m, [0, y, 0], op)          # оставить часть выше y
    def text_tex(self, img):  # img: float32 HxW (1 — буква)
        self.texts.append(img); return len(self.texts) - 1
    def arrays(self):
        P = np.array(self.prims, dtype=np.float64)
        A = np.array([m[0] for m in self.mats]); T = np.array([m[1] for m in self.mats], dtype=np.int64)
        TP = np.array([m[2] for m in self.mats], dtype=np.float64); S = np.array([m[3] for m in self.mats]); C2 = np.array([m[4] for m in self.mats])
        TX = np.stack(self.texts).astype(np.float64) if self.texts else np.zeros((1, 2, 2))
        return P, A, T, TP, S, C2, TX

@njit(cache=True)
def sd(P, i, x, y, z):
    t = int(P[i, 0]); q = P[i]
    if t == 0:
        return math.sqrt((x-q[3])**2 + (y-q[4])**2 + (z-q[5])**2) - q[6]
    if t == 1:
        pax, pay, paz = x-q[3], y-q[4], z-q[5]; bax, bay, baz = q[6]-q[3], q[7]-q[4], q[8]-q[5]
        h = (pax*bax + pay*bay + paz*baz) / (bax*bax + bay*bay + baz*baz + 1e-12); h = min(max(h, 0.0), 1.0)
        return math.sqrt((pax-bax*h)**2 + (pay-bay*h)**2 + (paz-baz*h)**2) - q[9]
    if t == 2 or t == 8:
        px, py, pz = x-q[3], y-q[4], z-q[5]
        if t == 8:
            c, s = math.cos(q[10]), math.sin(q[10]); px, py = c*px + s*py, -s*px + c*py
        qx, qy, qz = abs(px)-q[6], abs(py)-q[7], abs(pz)-q[8]
        o = math.sqrt(max(qx, 0.0)**2 + max(qy, 0.0)**2 + max(qz, 0.0)**2)
        return o + min(max(qx, max(qy, qz)), 0.0) - q[9]
    if t == 3:
        px, py, pz = (x-q[3])/q[6], (y-q[4])/q[7], (z-q[5])/q[8]
        k0 = math.sqrt(px*px + py*py + pz*pz)
        k1 = math.sqrt((px/q[6])**2 + (py/q[7])**2 + (pz/q[8])**2) + 1e-9
        return k0*(k0-1.0)/k1
    if t == 4:
        px, py, pz = x-q[3], y-q[4], z-q[5]; d = math.sqrt(px*px + py*py) - q[6]
        return math.sqrt(d*d + pz*pz) - q[7]
    if t == 5:
        px, py, pz = x-q[3], y-q[4], z-q[5]; d = math.sqrt(px*px + pz*pz) - q[6]
        return math.sqrt(d*d + py*py) - q[7]
    if t == 6:
        px, py, pz = x-q[3], y-q[4], z-q[5]
        dx = math.sqrt(px*px + pz*pz) - q[6] + q[8]; dy = abs(py) - q[7] + q[8]
        return min(max(dx, dy), 0.0) + math.sqrt(max(dx, 0.0)**2 + max(dy, 0.0)**2) - q[8]
    if t == 7:
        return q[4] - y
    return 1e9

@njit(cache=True)
def scene(P, x, y, z):
    n = P.shape[0]; dm = 1e9; mm = -1; best = 1e9; i = 0; k = 0.012
    while i < n:
        d = sd(P, i, x, y, z); m = int(P[i, 2]); j = i + 1
        while j < n and P[j, 1] != 0:
            e = sd(P, j, x, y, z)
            d = max(d, -e) if P[j, 1] == 1 else max(d, e)
            j += 1
        if d < best: best = d; mm = m
        h = min(max(0.5 + 0.5*(dm - d)/k, 0.0), 1.0)
        dm = dm*(1.0-h) + d*h - k*h*(1.0-h)
        i = j
    return dm, mm

@njit(cache=True)
def hash3(x, y, z):
    v = math.sin(x*127.1 + y*311.7 + z*74.7)*43758.5453
    return v - math.floor(v)

@njit(cache=True)
def vnoise(x, y, z):
    ix, iy, iz = math.floor(x), math.floor(y), math.floor(z); fx, fy, fz = x-ix, y-iy, z-iz
    fx, fy, fz = fx*fx*(3-2*fx), fy*fy*(3-2*fy), fz*fz*(3-2*fz); s = 0.0
    for a in range(2):
        for b in range(2):
            for c in range(2):
                w = (fx if a else 1-fx)*(fy if b else 1-fy)*(fz if c else 1-fz)
                s += w*hash3(ix+a, iy+b, iz+c)
    return s

@njit(parallel=True, cache=True)
def render(P, A, T, TP, S, C2, TX, W, H, cx, half, yaw, pitch, bg_top, bg_bot, light):
    img = np.zeros((H, W, 3))
    cyw, syw, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
    # направление взгляда (камера спереди, чуть сверху)
    dx, dy, dz = -syw*cp, -sp, -cyw*cp
    rx, ry, rz = cyw, 0.0, -syw
    ux, uy, uz = ry*dz - rz*dy, rz*dx - rx*dz, rx*dy - ry*dx
    lx, ly, lz = light[0], light[1], light[2]
    for py in prange(H):
        for px in range(W):
            u = (px + 0.5 - W/2) / (H/2) * half; v = -(py + 0.5 - H/2) / (H/2) * half
            ox = cx[0] + rx*u + ux*v - dx*8; oy = cx[1] + ry*u + uy*v - dy*8; oz = cx[2] + rz*u + uz*v - dz*8
            tb = py / H; bgr = bg_top*(1-tb) + bg_bot*tb
            t = 0.0; hit = False; mat = -1
            for it in range(160):
                x, y, z = ox+dx*t, oy+dy*t, oz+dz*t
                d, mat = scene(P, x, y, z)
                if d < 0.0015: hit = True; break
                t += d*0.9
                if t > 16: break
            if not hit:
                img[py, px, 0], img[py, px, 1], img[py, px, 2] = bgr[0], bgr[1], bgr[2]; continue
            x, y, z = ox+dx*t, oy+dy*t, oz+dz*t
            e = 0.0015
            n1, _ = scene(P, x+e, y-e, z-e); n2, _ = scene(P, x-e, y-e, z+e); n3, _ = scene(P, x-e, y+e, z-e); n4, _ = scene(P, x+e, y+e, z+e)
            nx = n1 - n2 - n3 + n4; ny = -n1 - n2 + n3 + n4; nz = -n1 + n2 - n3 + n4
            nl = math.sqrt(nx*nx + ny*ny + nz*nz) + 1e-9; nx, ny, nz = nx/nl, ny/nl, nz/nl
            # цвет материала
            ar, ag, ab = A[mat, 0], A[mat, 1], A[mat, 2]; tex = T[mat]; tp = TP[mat]
            if tex == 1:   # клетка
                fxx = (x*tp[0]) - math.floor(x*tp[0]); fyy = (y*tp[0]) - math.floor(y*tp[0])
                s1 = fxx < tp[1]; s2 = fyy < tp[1]
                if s1 or s2:
                    f = 0.75 if (s1 and s2) else 1.0
                    ar, ag, ab = C2[mat, 0]*f, C2[mat, 1]*f, C2[mat, 2]*f
            elif tex == 2:  # горошек
                gx = x*tp[0] - math.floor(x*tp[0]) - 0.5; gy = y*tp[0] - math.floor(y*tp[0]) - 0.5
                if gx*gx + gy*gy < tp[1]*tp[1]: ar, ag, ab = C2[mat, 0], C2[mat, 1], C2[mat, 2]
            elif tex == 3:  # надпись: прямоугольник x0,y0,w,h, номер текстуры
                uu = (x - tp[0]) / tp[2]; vv = 1.0 - (y - tp[1]) / tp[3]
                if uu >= 0 and uu < 1 and vv >= 0 and vv < 1:
                    k = int(tp[4]); th, tw = TX.shape[1], TX.shape[2]
                    a = TX[k, min(th-1, int(vv*th)), min(tw-1, int(uu*tw))]
                    ar, ag, ab = ar*(1-a) + C2[mat, 0]*a, ag*(1-a) + C2[mat, 1]*a, ab*(1-a) + C2[mat, 2]*a
            elif tex == 4:  # полоски шарфа по углу вокруг шеи
                ang = math.atan2(z - tp[1], x - tp[0]) + y*tp[3]
                if (int(math.floor(ang*tp[2]/3.14159)) % 2) == 0: ar, ag, ab = C2[mat, 0], C2[mat, 1], C2[mat, 2]
            elif tex == 5:  # поперечные полоски
                if (int(math.floor((y - tp[0])*tp[1])) % 2) == 0: ar, ag, ab = C2[mat, 0], C2[mat, 1], C2[mat, 2]
            # пластилиновая фактура
            g = 0.93 + 0.1*vnoise(x*38, y*38, z*38) + 0.04*hash3(x*900, y*900, z*900)
            ar, ag, ab = ar*g, ag*g, ab*g
            # свет: ключевой, заполняющий, небо, контровой, мягкая тень и AO
            dif = max(nx*lx + ny*ly + nz*lz, 0.0)
            sh = 1.0; st = 0.01
            for k in range(40):
                h, _ = scene(P, x+lx*st+nx*0.003, y+ly*st+ny*0.003, z+lz*st+nz*0.003)
                sh = min(sh, 10.0*h/st)
                st += max(h, 0.008)
                if sh < 0.02 or st > 3: break
            sh = max(sh, 0.0)
            ao = 1.0
            for k in range(1, 6):
                hh = 0.025*k; dd, _ = scene(P, x+nx*hh, y+ny*hh, z+nz*hh)
                ao -= (hh - dd)*(2.2/k)
            ao = min(max(ao, 0.25), 1.0)
            fill = max(-nx*0.6 + ny*0.15 + nz*0.6, 0.0)*0.22
            sky = (0.45 + 0.35*ny)*ao
            rim = (1.0 - max(-(nx*dx + ny*dy + nz*dz), 0.0))**3*0.25
            lit = dif*sh*0.82 + fill + sky*0.5
            # блик
            hx, hy, hz = lx - dx, ly - dy, lz - dz; hl = math.sqrt(hx*hx + hy*hy + hz*hz); hx, hy, hz = hx/hl, hy/hl, hz/hl
            spc = (max(nx*hx + ny*hy + nz*hz, 0.0)**(40 if S[mat] > 0.5 else 12))*(0.9 if S[mat] > 0.5 else 0.12)*sh
            cr = ar*lit + rim*0.9 + spc; cg = ag*lit + rim*0.88 + spc; cb = ab*lit + rim*0.85 + spc
            img[py, px, 0] = min(cr, 1.0); img[py, px, 1] = min(cg, 1.0); img[py, px, 2] = min(cb, 1.0)
    return img

def draw(sc, W, H, center, half, yaw=0.25, pitch=0.18, bg=((246, 240, 228), (236, 226, 208)), light=(-0.5, 0.72, 0.5)):
    P, A, T, TP, S, C2, TX = sc.arrays()
    l = np.array(light, dtype=np.float64); l /= np.linalg.norm(l)
    return render(P, A, T, TP, S, C2, TX, W, H, np.array(center, dtype=np.float64), half, yaw, pitch,
                  np.array(bg[0], dtype=np.float64)/255, np.array(bg[1], dtype=np.float64)/255, l)
