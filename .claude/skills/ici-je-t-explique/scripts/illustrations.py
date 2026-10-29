"""Illustrations animées pour render_explication.py.

Deux familles :
- ICONES : pictos fixes dessinés en vectoriel (pc, serveur, manette...), mis en cache.
- ANIMS  : petites scènes animées (aller_retour, chrono, pieces, chat...) dessinées à chaque image.

Toutes les fonctions d'animation ont la signature
    anim(frame, cx, cy, lt, dur, pal, opts, al)
lt = temps écoulé depuis le début de la scène, al = opacité de la scène (0..1).
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
FONT_BOLD = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
DARK = (20, 10, 40, 255)
WHITE = (255, 255, 255, 255)
GOLD = (255, 200, 0, 255)
RED = (235, 40, 70, 255)
GREEN = (40, 210, 110, 255)
_fonts = {}


def _font(path, size):
    k = (path, int(size))
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(path, max(1, int(size)))
    return _fonts[k]


def clamp(p):
    return min(1.0, max(0.0, p))


def ease_out(p):
    p = clamp(p)
    return 1 - (1 - p) ** 3


def ease_out_back(p, k=2.0):
    p = clamp(p) - 1
    return 1 + (k + 1) * p ** 3 + k * p ** 2


def rgba(c, a=255):
    return tuple(c[:3]) + (int(a),)


# ------------------------------------------------------------------ icônes vectorielles (grille 100x100)
class G:
    def __init__(self, d, u):
        self.d, self.u = d, u

    def b(self, box):
        return [v * self.u for v in box]

    def pts(self, pts):
        return [(x * self.u, y * self.u) for x, y in pts]

    def rr(self, box, r, fill=None, outline=None, w=0):
        self.d.rounded_rectangle(self.b(box), r * self.u, fill=fill, outline=outline, width=int(w * self.u))

    def el(self, box, fill=None, outline=None, w=0):
        self.d.ellipse(self.b(box), fill=fill, outline=outline, width=int(w * self.u))

    def poly(self, pts, fill=None):
        self.d.polygon(self.pts(pts), fill=fill)

    def line(self, pts, fill, w):
        p = self.pts(pts)
        self.d.line(p, fill=fill, width=int(w * self.u), joint='curve')
        r = w * self.u / 2
        for x, y in (p[0], p[-1]):
            self.d.ellipse((x - r, y - r, x + r, y + r), fill=fill)

    def arc(self, box, a0, a1, fill, w):
        self.d.arc(self.b(box), a0, a1, fill=fill, width=int(w * self.u))

    def pie(self, box, a0, a1, fill):
        self.d.pieslice(self.b(box), a0, a1, fill=fill)

    def text(self, x, y, txt, size, fill, path=FONT):
        self.d.text((x * self.u, y * self.u), txt, font=_font(path, size * self.u), fill=fill, anchor='mm')


def _pc(g, c):
    g.rr((8, 14, 92, 68), 7, DARK, c, 5); g.rr((16, 22, 84, 60), 3, rgba(c, 80))
    g.rr((43, 67, 57, 80), 0, c); g.rr((28, 79, 72, 87), 3, c)


def _serveur(g, c):
    for y in (8, 38, 68):
        g.rr((16, y, 84, y + 24), 5, DARK, c, 5)
        g.el((25, y + 8, 33, y + 16), GREEN); g.el((37, y + 8, 45, y + 16), GOLD)
        g.line([(56, y + 12), (74, y + 12)], c, 4)


def _manette(g, c):
    g.rr((10, 28, 90, 70), 22, c); g.el((6, 42, 42, 90), c); g.el((58, 42, 94, 90), c)
    g.rr((22, 40, 30, 62), 2, DARK); g.rr((15, 47, 37, 55), 2, DARK)
    for (x, y) in ((70, 41), (78, 50), (62, 50), (70, 59)):
        g.el((x - 4.5, y - 4.5, x + 4.5, y + 4.5), DARK)


def _telephone(g, c):
    g.rr((28, 6, 72, 94), 10, DARK, c, 5); g.rr((34, 15, 66, 79), 3, rgba(c, 80)); g.el((46, 83, 54, 91), c)


def _wifi(g, c):
    for r in (16, 34, 52):
        g.arc((50 - r, 84 - r, 50 + r, 84 + r), 225, 315, c, 9)
    g.el((43, 77, 57, 91), c)


def _cable(g, c):
    g.rr((37, 8, 45, 32), 2, WHITE); g.rr((55, 8, 63, 32), 2, WHITE)
    g.rr((28, 28, 72, 64), 8, c); g.rr((44, 63, 56, 74), 2, c)
    g.line([(50, 72), (50, 84), (38, 96)], c, 8)


def _piece(g, c):
    g.el((6, 6, 94, 94), GOLD, (205, 140, 0, 255), 5); g.el((19, 19, 81, 81), None, (255, 236, 130, 255), 4)
    g.text(50, 53, '€', 46, (160, 95, 0, 255))


def _coeur(g, c):
    g.el((8, 16, 52, 58), c); g.el((48, 16, 92, 58), c); g.poly([(11, 45), (89, 45), (50, 88)], c)


def _trophee(g, c):
    g.arc((8, 14, 36, 44), 90, 270, GOLD, 6); g.arc((64, 14, 92, 44), 270, 90, GOLD, 6)
    g.pie((22, -22, 78, 58), 0, 180, GOLD); g.rr((22, 8, 78, 20), 3, GOLD)
    g.rr((44, 56, 56, 72), 0, GOLD); g.rr((28, 72, 72, 86), 4, GOLD)
    g.text(50, 30, '1', 22, (160, 95, 0, 255))


def _bulle(g, c):
    g.rr((8, 14, 92, 68), 14, c); g.poly([(24, 64), (20, 90), (46, 64)], c)
    for x in (32, 50, 68):
        g.el((x - 5, 36, x + 5, 46), DARK)


def _chrono_base(g, c):
    g.rr((43, 3, 57, 14), 3, c); g.rr((47, 12, 53, 22), 0, c)
    g.el((12, 18, 88, 94), DARK, c, 7)
    for i in range(12):
        a = i * math.pi / 6
        r0, r1 = (26, 32) if i % 3 else (22, 32)
        g.line([(50 + r0 * math.sin(a), 56 - r0 * math.cos(a)), (50 + r1 * math.sin(a), 56 - r1 * math.cos(a))], c, 3)


def _chrono(g, c):
    _chrono_base(g, c)
    g.line([(50, 56), (62, 34)], WHITE, 5); g.el((45, 51, 55, 61), WHITE)


def _cible(g, c):
    g.el((10, 10, 90, 90), None, c, 6); g.el((28, 28, 72, 72), None, c, 6); g.el((43, 43, 57, 57), RED)
    for a, b in (((50, 2), (50, 20)), ((50, 80), (50, 98)), ((2, 50), (20, 50)), ((80, 50), (98, 50))):
        g.line([a, b], c, 6)


def _eclair(g, c):
    g.poly([(60, 2), (16, 56), (46, 56), (34, 98), (84, 40), (54, 40), (68, 2)], GOLD)


def _alerte(g, c):
    g.poly([(50, 4), (97, 90), (3, 90)], GOLD); g.text(50, 62, '!', 52, DARK)


def _check(g, c):
    g.el((6, 6, 94, 94), GREEN); g.line([(28, 52), (44, 68), (74, 34)], WHITE, 10)


def _croix(g, c):
    g.el((6, 6, 94, 94), RED); g.line([(32, 32), (68, 68)], WHITE, 10); g.line([(68, 32), (32, 68)], WHITE, 10)


def _oeil(g, c):
    top = [(x, 50 - 30 * math.sin(math.pi * (x - 4) / 92)) for x in range(4, 97, 4)]
    bot = [(x, 50 + 30 * math.sin(math.pi * (x - 4) / 92)) for x in range(96, 3, -4)]
    g.poly(top + bot, WHITE); g.el((32, 32, 68, 68), c); g.el((43, 43, 57, 57), DARK); g.el((52, 38, 60, 46), WHITE)


def _camera(g, c):
    g.rr((10, 22, 90, 78), 12, DARK, c, 5); g.el((30, 30, 70, 70), c); g.el((39, 39, 61, 61), DARK)
    g.el((76, 28, 84, 36), RED); g.rr((44, 78, 56, 88), 0, c); g.rr((30, 88, 70, 95), 3, c)


def _micro(g, c):
    g.rr((36, 4, 64, 58), 14, c)
    for y in (18, 28, 38):
        g.line([(42, y), (58, y)], DARK, 3)
    g.arc((24, 22, 76, 72), 0, 180, WHITE, 5); g.line([(50, 72), (50, 86)], WHITE, 5); g.line([(36, 90), (64, 90)], WHITE, 6)


def _personne(g, c):
    g.el((33, 6, 67, 40), c); g.pie((14, 46, 86, 118), 180, 360, c)


def _cadenas(g, c):
    g.arc((28, 6, 72, 54), 180, 360, WHITE, 8); g.line([(28.5, 30), (28.5, 46)], WHITE, 8); g.line([(71.5, 30), (71.5, 46)], WHITE, 8)
    g.rr((18, 42, 82, 94), 9, c); g.el((44, 56, 56, 68), DARK); g.rr((47.5, 62, 52.5, 80), 2, DARK)


def _gpu(g, c):
    g.rr((4, 22, 96, 76), 8, DARK, c, 5)
    for x in (14, 54):
        g.el((x, 30, x + 32, 68), None, c, 4); g.el((x + 12, 45, x + 20, 53), c)
    g.rr((14, 76, 62, 84), 1, GOLD)


def _etoile(g, c):
    p = []
    for i in range(10):
        r = 46 if i % 2 == 0 else 19
        a = -math.pi / 2 + i * math.pi / 5
        p.append((50 + r * math.cos(a), 54 + r * math.sin(a)))
    g.poly(p, GOLD)


def _globe(g, c):
    g.el((8, 8, 92, 92), DARK, c, 5); g.el((31, 8, 69, 92), None, c, 4)
    g.line([(10, 50), (90, 50)], c, 4); g.line([(17, 29), (83, 29)], c, 3); g.line([(17, 71), (83, 71)], c, 3)


def _telechargement(g, c):
    g.rr((42, 4, 58, 46), 2, c); g.poly([(24, 42), (76, 42), (50, 70)], c)
    g.line([(12, 64), (12, 88), (88, 88), (88, 64)], WHITE, 7)


def _clavier(g, c):
    g.rr((3, 26, 97, 78), 8, DARK, c, 5)
    for r in range(3):
        for k in range(8):
            x = 11 + k * 10.5 + (r % 2) * 3
            g.rr((x, 34 + r * 11, x + 7, 41 + r * 11), 1.5, c)
    g.rr((28, 67, 72, 72), 2, c)


def _souris(g, c):
    g.rr((26, 6, 74, 94), 24, DARK, c, 5); g.line([(50, 8), (50, 40)], c, 4); g.rr((46, 18, 54, 32), 4, c)


def _casque(g, c):
    g.arc((14, 8, 86, 80), 180, 360, c, 8); g.rr((8, 44, 30, 84), 9, c); g.rr((70, 44, 92, 84), 9, c)


def _live(g, c):
    g.rr((2, 30, 98, 70), 20, RED); g.el((12, 44, 24, 56), WHITE); g.text(60, 50.5, 'LIVE', 25, WHITE)


def _console(g, c):
    g.rr((8, 28, 92, 78), 10, DARK, c, 5); g.line([(20, 44), (60, 44)], c, 4); g.el((68, 56, 80, 68), c)


def _cerveau(g, c):
    for box in ((14, 22, 50, 58), (30, 10, 66, 46), (50, 18, 86, 54), (20, 42, 56, 80), (46, 40, 84, 78)):
        g.el(box, c)
    g.line([(50, 14), (50, 76)], DARK, 3)
    g.rr((44, 74, 58, 92), 4, c)


def _horloge(g, c):
    g.el((8, 8, 92, 92), DARK, c, 7); g.line([(50, 50), (50, 24)], WHITE, 6); g.line([(50, 50), (68, 58)], WHITE, 6)


def _fusee(g, c):
    g.poly([(50, 2), (66, 26), (66, 66), (34, 66), (34, 26)], WHITE); g.el((42, 26, 58, 42), c)
    g.poly([(34, 46), (18, 70), (34, 66)], c); g.poly([(66, 46), (82, 70), (66, 66)], c)
    g.poly([(38, 68), (62, 68), (50, 96)], GOLD)


def _euro(g, c):
    g.rr((6, 22, 94, 78), 10, (60, 190, 110, 255)); g.el((34, 34, 66, 66), None, WHITE, 5); g.text(50, 51, '€', 24, WHITE)


ICONES = {
    'pc': _pc, 'ecran': _pc, 'serveur': _serveur, 'manette': _manette, 'telephone': _telephone, 'wifi': _wifi,
    'cable': _cable, 'piece': _piece, 'coeur': _coeur, 'trophee': _trophee, 'bulle': _bulle, 'chrono': _chrono,
    'chrono_vide': _chrono_base, 'cible': _cible, 'eclair': _eclair, 'alerte': _alerte, 'check': _check,
    'croix': _croix, 'oeil': _oeil, 'camera': _camera, 'micro': _micro, 'personne': _personne, 'cadenas': _cadenas,
    'gpu': _gpu, 'etoile': _etoile, 'globe': _globe, 'telechargement': _telechargement, 'clavier': _clavier,
    'souris': _souris, 'casque': _casque, 'live': _live, 'console': _console, 'cerveau': _cerveau,
    'horloge': _horloge, 'fusee': _fusee, 'billet': _euro,
}
_icon_cache = {}


def icon_sprite(name, size, color):
    """Picto + halo lumineux. Renvoie une image RGBA d'environ 1,4 x size, centrée sur l'icône."""
    k = (name, int(size), tuple(color))
    if k in _icon_cache:
        return _icon_cache[k]
    S = int(size) * 3
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ICONES.get(name, _etoile)(G(ImageDraw.Draw(img, 'RGBA'), S / 100), rgba(color))
    img = img.resize((int(size), int(size)), Image.LANCZOS)
    pad = int(size * 0.2)
    out = Image.new('RGBA', (int(size) + 2 * pad, int(size) + 2 * pad), (0, 0, 0, 0))
    glow = Image.new('L', out.size, 0)
    glow.paste(img.getchannel('A'), (pad, pad))
    glow = glow.filter(ImageFilter.GaussianBlur(size * 0.07)).point(lambda v: int(v * 0.6))
    out.paste(rgba(color), (0, 0), glow)
    out.alpha_composite(img, (pad, pad))
    _icon_cache[k] = out
    return out


def paste_icon(frame, name, cx, cy, size, color, scale=1.0, alpha=1.0, rot=0.0, squish=1.0):
    if scale <= 0.02 or alpha <= 0.01:
        return
    spr = icon_sprite(name, size, color)
    if abs(scale - 1) > 0.01 or abs(squish - 1) > 0.01:
        spr = spr.resize((max(1, int(spr.width * scale * squish)), max(1, int(spr.height * scale))), Image.BILINEAR)
    if abs(rot) > 0.1:
        spr = spr.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 0.99:
        spr = spr.copy(); spr.putalpha(spr.getchannel('A').point(lambda v: int(v * alpha)))
    frame.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))


# ------------------------------------------------------------------ dessin dynamique anti-aliasé
class SS:
    """Zone de dessin suréchantillonnée x2 (coordonnées écran), recollée sur l'image."""

    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y0 = int(x0), int(y0)
        self.w, self.h = int(x1 - x0), int(y1 - y0)
        self.img = Image.new('RGBA', (self.w * 2, self.h * 2), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img, 'RGBA')

    def p(self, x, y):
        return ((x - self.x0) * 2, (y - self.y0) * 2)

    def line(self, pts, fill, w, caps=True):
        q = [self.p(*pt) for pt in pts]
        self.d.line(q, fill=fill, width=int(w * 2), joint='curve')
        if caps:
            for x, y in (q[0], q[-1]):
                self.d.ellipse((x - w, y - w, x + w, y + w), fill=fill)

    def circle(self, x, y, r, fill=None, outline=None, w=0):
        X, Y = self.p(x, y)
        self.d.ellipse((X - r * 2, Y - r * 2, X + r * 2, Y + r * 2), fill=fill, outline=outline, width=int(w * 2))

    def poly(self, pts, fill):
        self.d.polygon([self.p(*pt) for pt in pts], fill=fill)

    def rr(self, box, r, fill=None, outline=None, w=0):
        a, b = self.p(box[0], box[1]); c, d = self.p(box[2], box[3])
        self.d.rounded_rectangle((a, b, c, d), r * 2, fill=fill, outline=outline, width=int(w * 2))

    def arc(self, x, y, r, a0, a1, fill, w):
        X, Y = self.p(x, y)
        self.d.arc((X - r * 2, Y - r * 2, X + r * 2, Y + r * 2), a0, a1, fill=fill, width=int(w * 2))

    def text(self, x, y, txt, size, fill, path=FONT):
        self.d.text(self.p(x, y), txt, font=_font(path, size * 2), fill=fill, anchor='mm',
                    stroke_width=int(size * 0.12), stroke_fill=(10, 6, 25, fill[3] if len(fill) > 3 else 255))

    def done(self, frame, alpha=1.0):
        im = self.img.reduce(2)
        if alpha < 0.99:
            im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
        frame.alpha_composite(im, (self.x0, self.y0))


def glow_dot(ss, x, y, r, col, a=1.0):
    for k, al in ((2.6, 0.12), (1.8, 0.25), (1.25, 0.5)):
        ss.circle(x, y, r * k, fill=rgba(col, 255 * al * a))
    ss.circle(x, y, r, fill=rgba((255, 255, 255), 255 * a))


def burst(ss, x, y, since, col, n=10, r0=50, r1=140, dur=0.45, w=7, rot=0.0):
    """Éclat de traits qui partent en étoile (impact, apparition)."""
    if since < 0 or since > dur:
        return
    p = ease_out(since / dur)
    a = 1 - since / dur
    for i in range(n):
        ang = rot + i * 2 * math.pi / n
        ra, rb = r0 + (r1 - r0) * p * 0.6, r0 + (r1 - r0) * p
        ss.line([(x + ra * math.cos(ang), y + ra * math.sin(ang)), (x + rb * math.cos(ang), y + rb * math.sin(ang))],
                rgba(col, 255 * a), w * (0.4 + 0.6 * a))


def ring(ss, x, y, since, col, r0=60, r1=220, dur=0.7, w=8):
    if since < 0 or since > dur:
        return
    p = ease_out(since / dur)
    ss.circle(x, y, r0 + (r1 - r0) * p, outline=rgba(col, 255 * (1 - since / dur)), w=w * (1 - 0.6 * p))


def bezier(p0, c, p1, s):
    return ((1 - s) ** 2 * p0[0] + 2 * (1 - s) * s * c[0] + s * s * p1[0],
            (1 - s) ** 2 * p0[1] + 2 * (1 - s) * s * c[1] + s * s * p1[1])


def arrow_head(ss, x, y, ang, size, col):
    ss.poly([(x + size * math.cos(ang), y + size * math.sin(ang)),
             (x + size * 0.8 * math.cos(ang + 2.5), y + size * 0.8 * math.sin(ang + 2.5)),
             (x + size * 0.8 * math.cos(ang - 2.5), y + size * 0.8 * math.sin(ang - 2.5))], col)


def dashed_curve(ss, p0, c, p1, frac, col, w=8, n=34):
    m = int(n * clamp(frac))
    for i in range(0, m, 2):
        ss.line([bezier(p0, c, p1, i / n), bezier(p0, c, p1, min(i + 1, m) / n)], col, w)


def label(ss, x, y, txt, size=40, col=WHITE):
    if txt:
        ss.text(x, y, txt, size, col, FONT_BOLD)


# ------------------------------------------------------------------ animations
def anim_aller_retour(frame, cx, cy, lt, dur, pal, o, al):
    L, R = (cx - 300, cy), (cx + 300, cy)
    period = float(o.get('periode', 1.6))
    t_loop = 1.3
    ph = ((lt - t_loop) / period) % 1 if lt > t_loop else -1
    bumpR = math.exp(-((ph - 0.5) / 0.05) ** 2) * 0.15 if ph >= 0 else 0
    bumpL = (math.exp(-(ph / 0.05) ** 2) + math.exp(-((ph - 1) / 0.05) ** 2)) * 0.15 if ph >= 0 else 0
    paste_icon(frame, o.get('gauche', 'pc'), L[0], L[1], 170, pal['accent2'], ease_out_back(lt / 0.4) + bumpL, al)
    paste_icon(frame, o.get('droite', 'serveur'), R[0], R[1], 170, pal['accent3'], ease_out_back((lt - 0.15) / 0.4) + bumpR, al)
    ss = SS(cx - 520, cy - 230, cx + 520, cy + 230)
    a0, c0, b0 = (L[0] + 110, cy - 40), (cx, cy - 190), (R[0] - 110, cy - 40)
    a1, c1, b1 = (R[0] - 110, cy + 40), (cx, cy + 190), (L[0] + 110, cy + 40)
    f0, f1 = (lt - 0.35) / 0.45, (lt - 0.8) / 0.45
    dashed_curve(ss, a0, c0, b0, f0, rgba(pal['accent2']))
    dashed_curve(ss, a1, c1, b1, f1, rgba(pal['accent3']))
    for f, (p0, c, p1), col in ((f0, (a0, c0, b0), pal['accent2']), (f1, (a1, c1, b1), pal['accent3'])):
        if f >= 1:
            e = bezier(p0, c, p1, 1); q = bezier(p0, c, p1, 0.94)
            arrow_head(ss, e[0], e[1], math.atan2(e[1] - q[1], e[0] - q[0]), 30 * ease_out_back((f - 1) * 3), rgba(col))
    if ph >= 0:
        for k in range(7, -1, -1):
            pk = ph - k * 0.012
            if pk < 0:
                continue
            if pk < 0.5:
                x, y = bezier(a0, c0, b0, pk * 2)
            else:
                x, y = bezier(a1, c1, b1, (pk - 0.5) * 2)
            if k:
                ss.circle(x, y, 14 * (1 - k / 9), fill=rgba(pal['accent'], 200 * (1 - k / 8)))
            else:
                glow_dot(ss, x, y, 13, pal['accent'])
        if ph >= 0:
            burst(ss, R[0], R[1], (ph - 0.5) * period, pal['accent'], n=8, r0=95, r1=150, dur=0.3, w=6)
    label(ss, L[0], cy + 140, o.get('label_gauche', 'Toi'))
    label(ss, R[0], cy + 140, o.get('label_droite', 'Serveur'))
    if o.get('centre') and lt > 1.0:
        ss.text(cx, cy, o['centre'], 52, rgba(pal['accent'], 255 * ease_out((lt - 1.0) / 0.3)))
    ss.done(frame, al)


def anim_transfert(frame, cx, cy, lt, dur, pal, o, al):
    L, R = (cx - 300, cy), (cx + 300, cy)
    sens = 1 if o.get('sens', 'droite') == 'droite' else -1
    paste_icon(frame, o.get('gauche', 'serveur'), L[0], L[1], 170, pal['accent2'], ease_out_back(lt / 0.4), al)
    paste_icon(frame, o.get('droite', 'pc'), R[0], R[1], 170, pal['accent3'], ease_out_back((lt - 0.15) / 0.4), al)
    ss = SS(cx - 520, cy - 230, cx + 520, cy + 230)
    x0, x1 = L[0] + 115, R[0] - 115
    f = ease_out((lt - 0.3) / 0.4)
    for i in range(0, 14, 2):
        a, b = i / 14, (i + 1) / 14
        if a < f:
            ss.line([(x0 + (x1 - x0) * a, cy), (x0 + (x1 - x0) * min(b, f), cy)], rgba((255, 255, 255), 90), 6)
    if lt > 0.6:
        for k in range(5):
            s = ((lt - 0.6) * 0.8 + k / 5) % 1
            s = s if sens > 0 else 1 - s
            x = x0 + (x1 - x0) * s
            fade = math.sin(math.pi * s)
            glow_dot(ss, x, cy, 12, pal['accent'], fade)
        head = x1 + 22 if sens > 0 else x0 - 22
        arrow_head(ss, head, cy, 0 if sens > 0 else math.pi, 30, rgba(pal['accent']))
    label(ss, L[0], cy + 140, o.get('label_gauche', ''))
    label(ss, R[0], cy + 140, o.get('label_droite', ''))
    if o.get('centre'):
        ss.text(cx, cy - 70, o['centre'], 50, rgba(pal['accent'], 255 * ease_out((lt - 0.6) / 0.3)))
    ss.done(frame, al)


def anim_chrono(frame, cx, cy, lt, dur, pal, o, al):
    sc = ease_out_back(lt / 0.4)
    size = 300
    paste_icon(frame, 'chrono_vide', cx, cy, size, pal['accent2'], sc, al)
    if sc < 0.95:
        return
    ccx, ccy = cx, cy - size / 2 + size * 0.56
    r = size * 0.27
    rev = float(o.get('tours_par_seconde', 0.7))
    ang = (lt - 0.4) * rev * 360
    ss = SS(cx - 200, cy - 200, cx + 200, cy + 200)
    ss.arc(ccx, ccy, r * 0.75, -90, -90 + (ang % 360), rgba(pal['accent'], 200), 10)
    a = math.radians(ang - 90)
    ss.line([(ccx, ccy), (ccx + r * 1.05 * math.cos(a), ccy + r * 1.05 * math.sin(a))], WHITE, 7)
    ss.circle(ccx, ccy, 9, fill=rgba(pal['accent3']))
    if o.get('texte'):
        ss.text(cx, cy + 180, o['texte'], 46, rgba(pal['accent']))
    ss.done(frame, al)


def anim_graphique(frame, cx, cy, lt, dur, pal, o, al):
    vals = o.get('valeurs') or [0.3, 0.45, 0.62, 0.9]
    if o.get('sens') == 'baisse' and not o.get('valeurs'):
        vals = vals[::-1]
    n = len(vals)
    ss = SS(cx - 380, cy - 220, cx + 380, cy + 220)
    base, hmax, wbar = cy + 150, 300, min(110, 520 / n)
    gap = (600 - n * wbar) / max(1, n - 1)
    ss.line([(cx - 330, base), (cx + 330, base)], rgba((255, 255, 255), 160), 6)
    tops = []
    for i, v in enumerate(vals):
        p = ease_out_back((lt - 0.2 - i * 0.15) / 0.45, 1.4)
        x = cx - 300 + i * (wbar + gap)
        h = hmax * v * max(0, p)
        col = pal['accent2'] if i < n - 1 else pal['accent']
        if h > 4:
            ss.rr((x, base - h, x + wbar, base), 12, rgba(col))
        tops.append((x + wbar / 2, base - hmax * v - 30))
        etqs = o.get('etiquettes') or []
        etq = etqs[i] if i < len(etqs) else None
        if etq:
            label(ss, x + wbar / 2, base + 40, etq, 34)
    f = (lt - 0.3 - n * 0.15) / 0.6
    if f > 0:
        m = 40
        pts = []
        for j in range(int(m * clamp(f)) + 1):
            s = j / m * (n - 1)
            i = min(int(s), n - 2)
            u = s - i
            pts.append((tops[i][0] + (tops[i + 1][0] - tops[i][0]) * u, tops[i][1] + (tops[i + 1][1] - tops[i][1]) * u))
        if len(pts) > 1:
            col = rgba(pal['accent3'])
            ss.line(pts, col, 9)
            if f >= 1:
                e, q = pts[-1], pts[-2]
                arrow_head(ss, e[0], e[1], math.atan2(e[1] - q[1], e[0] - q[0]), 38, col)
    ss.done(frame, al)


def anim_pieces(frame, cx, cy, lt, dur, pal, o, al):
    nom = o.get('nom', 'piece')
    n = int(o.get('nombre', 8))
    for i in range(n):
        t0 = 0.12 * i
        if lt < t0:
            continue
        col, lvl = i % 3, i // 3
        x = cx + (col - 1) * 170 + (8 if lvl % 2 else -8)
        y_land = cy + 120 - lvl * 42
        y_start = cy - 280
        tf = 0.45
        s = (lt - t0) / tf
        if s < 1:
            y = y_start + (y_land - y_start) * s * s
            squish = abs(math.cos((lt - t0) * 9 + i))
        else:
            k = s - 1
            y = y_land - 40 * abs(math.sin(k * 6)) * math.exp(-k * 7)
            squish = 1
        paste_icon(frame, nom, x, y, 120, pal['accent'], 1, al, squish=max(0.15, squish))
    ss = SS(cx - 400, cy - 300, cx + 400, cy + 260)
    for i in range(n):
        land = 0.12 * i + 0.45
        burst(ss, cx + (i % 3 - 1) * 170, cy + 120 - (i // 3) * 42, lt - land, pal['accent'], n=8, r0=60, r1=110, dur=0.3, w=5)
    ss.done(frame, al)


def anim_chat(frame, cx, cy, lt, dur, pal, o, al):
    msgs = o.get('messages') or ['GG !', 'Trop fort', "Let's go !", 'Clip ça !', 'Incroyable', 'ahah', 'LETS GOOO']
    cols = [pal['accent2'], pal['accent3'], pal['accent'], (130, 255, 140), (190, 140, 255)]
    every = float(o.get('rythme', 0.45))
    ss = SS(cx - 460, cy - 260, cx + 460, cy + 230)
    shown = int(max(0, lt) / every) + 1
    f = _font(FONT_BOLD, 44)
    for j in range(shown):
        k = shown - 1 - j          # 0 = le plus récent
        e = ease_out((lt - (shown - 1) * every) / 0.25)
        rise = k - 1 + e           # le nouveau message pousse les autres vers le haut
        y = cy + 150 - rise * 92
        if y < cy - 190:
            continue
        a = clamp((y - (cy - 190)) / 80)
        txt = msgs[j % len(msgs)]
        tw = f.getlength(txt)
        x0 = cx - 380
        ss.rr((x0, y - 38, x0 + tw + 120, y + 38), 30, (25, 14, 60, int(220 * a)))
        ss.circle(x0 + 40, y, 20, fill=rgba(cols[j % len(cols)], 255 * a))
        ss.d.text(ss.p(x0 + 78, y), txt, font=_font(FONT_BOLD, 88), fill=(255, 255, 255, int(255 * a)), anchor='lm')
    ss.done(frame, al)
    for h in range(int(lt / 0.35)):
        th = lt - h * 0.35
        if th > 1.6:
            continue
        x = cx + 320 + 40 * math.sin(h * 2.1 + th * 3)
        y = cy + 160 - th * 230
        paste_icon(frame, 'coeur', x, y, 60 + 20 * (h % 2), pal['accent3'], 1, al * clamp(1.6 - th))


def anim_cible(frame, cx, cy, lt, dur, pal, o, al):
    cycle = 1.8
    ph = lt % cycle
    hit = 0.9
    since = ph - hit
    shake = math.sin(lt * 80) * 10 * math.exp(-since * 10) if since > 0 else 0
    paste_icon(frame, o.get('cible', 'personne'), cx + shake, cy + 10, 220,
               pal['accent3'] if not (0 < since < 0.15) else (255, 255, 255), ease_out_back(lt / 0.4), al)
    ss = SS(cx - 400, cy - 260, cx + 400, cy + 260)
    r = 260 * (1 - ease_out(min(1, ph / hit)))
    ang = lt * 2.3
    x, y = cx + r * math.cos(ang), cy - 30 + r * math.sin(ang) * 0.6
    col = rgba(pal['accent'])
    ss.circle(x, y, 70, outline=col, w=7)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ss.line([(x + dx * 40, y + dy * 40), (x + dx * 95, y + dy * 95)], col, 7)
    if since > 0:
        a = clamp(1 - since / 0.5)
        for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            ss.line([(x + dx * 25, y + dy * 25), (x + dx * 55, y + dy * 55)], rgba((255, 255, 255), 255 * a), 8)
        burst(ss, x, y, since, pal['accent'], n=12, r0=80, r1=200, dur=0.4)
    ss.done(frame, al)


def anim_wifi(frame, cx, cy, lt, dur, pal, o, al):
    force = int(o.get('force', 3))
    ss = SS(cx - 260, cy - 240, cx + 260, cy + 200)
    sc = ease_out_back(lt / 0.4)
    bx, by = cx, cy + 120
    ph = (lt % 1.4) / 1.4
    for i, r in enumerate((80, 160, 240)):
        on = i < force and ph > i * 0.22
        if i >= force:
            col = rgba((255, 255, 255), 50)
        else:
            col = rgba(pal['accent2'], 255 if on else 90)
        ss.arc(bx, by, r * sc, 225, 315, col, 36 * sc)
    ss.circle(bx, by, 26 * sc, fill=rgba(pal['accent2']))
    if force < 3 and lt > 0.5:
        a = 0.5 + 0.5 * math.sin(lt * 9)
        ss.circle(cx + 170, cy - 140, 46, fill=rgba(RED, 255 * a))
        ss.text(cx + 170, cy - 140, '!', 60, rgba((255, 255, 255), 255 * a))
    ss.done(frame, al)


def anim_chargement(frame, cx, cy, lt, dur, pal, o, al):
    target = float(o.get('jusqua', 1.0))
    p = target * ease_out((lt - 0.2) / max(0.6, float(o.get('duree', 1.8))))
    ss = SS(cx - 380, cy - 200, cx + 380, cy + 160)
    x0, x1, y0, y1 = cx - 330, cx + 330, cy + 20, cy + 90
    ss.rr((x0, y0, x1, y1), 35, (255, 255, 255, 40), rgba(pal['accent2']), 5)
    xf = x0 + (x1 - x0) * p
    if xf > x0 + 30:
        ss.rr((x0 + 8, y0 + 8, xf - 8, y1 - 8), 27, rgba(pal['accent']))
        for k in range(-1, 20):
            sx = x0 + 8 + k * 50 + (lt * 120) % 50
            if x0 + 20 < sx < xf - 40:
                ss.line([(sx, y1 - 14), (sx + 26, y0 + 14)], (255, 255, 255, 90), 12, caps=False)
    ss.text(cx, cy - 70, o.get('texte') or f'{int(round(p * 100))} %', 90, WHITE)
    ss.done(frame, al)


def anim_alerte(frame, cx, cy, lt, dur, pal, o, al):
    ss = SS(cx - 320, cy - 300, cx + 320, cy + 300)
    for k in range(4):
        ring(ss, cx, cy + 10, (lt - 0.3 - k * 0.8) % 3.2, RED if k % 2 else pal['accent'], 110, 300, 0.8, 9)
    ss.done(frame, al)
    sc = ease_out_back(lt / 0.4) * (1 + 0.06 * math.sin(lt * 8))
    shake = math.sin(lt * 60) * 12 * max(0, 1 - lt / 0.5)
    paste_icon(frame, o.get('nom', 'alerte'), cx + shake, cy, 250, pal['accent'], sc, al)


def anim_icone(frame, cx, cy, lt, dur, pal, o, al):
    nom = o.get('nom', 'etoile')
    size = float(o.get('taille', 270))
    col = pal.get(o.get('couleur', 'accent2'), pal['accent2'])
    ss = SS(cx - 330, cy - 300, cx + 330, cy + 300)
    ring(ss, cx, cy, lt - 0.1, col, size * 0.4, size * 1.0, 0.7, 9)
    burst(ss, cx, cy, lt - 0.15, pal['accent'], n=12, r0=size * 0.55, r1=size * 0.95, dur=0.5, w=8, rot=0.26)
    for k in range(3):   # petites étincelles qui tournent
        a = lt * 1.5 + k * 2.1
        sx, sy = cx + size * 0.62 * math.cos(a), cy + size * 0.5 * math.sin(a)
        s = 10 + 5 * math.sin(lt * 5 + k)
        if lt > 0.5:
            ss.poly([(sx, sy - s * 2), (sx + s * 0.5, sy), (sx, sy + s * 2), (sx - s * 0.5, sy)], rgba((255, 255, 255), 200))
            ss.poly([(sx - s * 2, sy), (sx, sy + s * 0.5), (sx + s * 2, sy), (sx, sy - s * 0.5)], rgba((255, 255, 255), 200))
    ss.done(frame, al)
    bob = math.sin(lt * 3) * 12
    paste_icon(frame, nom, cx, cy + bob, size, col, ease_out_back(lt / 0.45), al, rot=math.sin(lt * 2) * 4)


def anim_icones(frame, cx, cy, lt, dur, pal, o, al):
    noms = (o.get('noms') or ['manette', 'pc', 'telephone'])[:4]
    n = len(noms)
    size = {1: 260, 2: 230, 3: 200, 4: 165}[n]
    step = min(330, 900 / n)
    cols = [pal['accent2'], pal['accent3'], pal['accent'], (130, 255, 140)]
    lien = o.get('liens')
    ss = SS(cx - 520, cy - 220, cx + 520, cy + 220)
    for i in range(n - 1):
        if not lien:
            break
        xm = cx + (i + 0.5 - (n - 1) / 2) * step
        p = ease_out_back((lt - 0.25 - (i + 1) * 0.2) / 0.3)
        if p <= 0:
            continue
        if lien == 'plus':
            ss.line([(xm - 26 * p, cy), (xm + 26 * p, cy)], WHITE, 10); ss.line([(xm, cy - 26 * p), (xm, cy + 26 * p)], WHITE, 10)
        else:
            dx = 8 * math.sin(lt * 6)
            ss.line([(xm - 34 * p + dx, cy), (xm + 14 * p + dx, cy)], rgba(pal['accent']), 10)
            arrow_head(ss, xm + 30 * p + dx, cy, 0, 30 * p, rgba(pal['accent']))
    for i, nm in enumerate(noms):
        labs = o.get('labels') or []
        lab = labs[i] if i < len(labs) else None
        if lab:
            label(ss, cx + (i - (n - 1) / 2) * step, cy + size * 0.5 + 60, lab, 36)
    ss.done(frame, al)
    for i, nm in enumerate(noms):
        x = cx + (i - (n - 1) / 2) * step
        sc = ease_out_back((lt - i * 0.2) / 0.4)
        bob = math.sin(lt * 3 + i * 1.3) * 10
        paste_icon(frame, nm, x, cy + bob, size, cols[i % len(cols)], sc, al)


def anim_fleche(frame, cx, cy, lt, dur, pal, o, al):
    ang = {'droite': 0, 'bas': 90, 'gauche': 180, 'haut': -90}.get(o.get('sens', 'haut'), -90)
    a = math.radians(ang)
    col = rgba(pal.get(o.get('couleur', 'accent'), pal['accent']))
    ss = SS(cx - 320, cy - 300, cx + 320, cy + 300)
    p = ease_out_back(lt / 0.45, 1.6)
    move = 18 * math.sin(lt * 5) if lt > 0.5 else 0
    L = 360 * p
    ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    bx, by = cx - ux * (180 - move), cy - uy * (180 - move)
    tip = (bx + ux * L, by + uy * L)
    shaft = 40
    neck = L - 130 * p
    pts = [(bx + vx * shaft, by + vy * shaft), (bx + ux * neck + vx * shaft, by + uy * neck + vy * shaft),
           (bx + ux * neck + vx * 105 * p, by + uy * neck + vy * 105 * p), tip,
           (bx + ux * neck - vx * 105 * p, by + uy * neck - vy * 105 * p), (bx + ux * neck - vx * shaft, by + uy * neck - vy * shaft),
           (bx - vx * shaft, by - vy * shaft)]
    if L > 20:
        ss.poly([(x + 8, y + 12) for x, y in pts], (0, 0, 0, 120))
        ss.poly(pts, col)
        for k in (-1, 0, 1):   # traits de vitesse
            off = 110 * k
            sx, sy = bx - ux * 40 + vx * off, by - uy * 40 + vy * off
            ln = 80 + 40 * math.sin(lt * 7 + k)
            ss.line([(sx, sy), (sx - ux * ln, sy - uy * ln)], rgba((255, 255, 255), 150), 8)
    ss.done(frame, al)


def anim_saynete(frame, cx, cy, lt, dur, pal, o, al):
    import saynetes
    saynetes.draw_window(frame, int(cx - 450), int(cy - 215), 900, 430, o.get('saynete', o), lt, pal, al,
                         o.get('titre'), o.get('couleur', 'accent2'), float(o.get('delai', 0)))


ANIMS = {
    'aller_retour': anim_aller_retour, 'transfert': anim_transfert, 'chrono': anim_chrono, 'graphique': anim_graphique,
    'pieces': anim_pieces, 'chat': anim_chat, 'cible': anim_cible, 'wifi': anim_wifi, 'chargement': anim_chargement,
    'alerte': anim_alerte, 'saynete': anim_saynete, 'icone': anim_icone, 'icones': anim_icones, 'fleche': anim_fleche,
}


def normalize(ill):
    """'aller_retour' | 'manette' | {'type': ...} -> dict d'options avec 'type'."""
    if not ill:
        return None
    if isinstance(ill, str):
        ill = {'type': ill}
    ill = dict(ill)
    if ill.get('type') not in ANIMS:
        if ill.get('type') in ICONES:
            ill = dict(ill, nom=ill['type'], type='icone')
        else:
            print(f"Illustration inconnue : {ill.get('type')} (ignorée)")
            return None
    return ill


def draw(frame, ill, cx, cy, lt, dur, pal, al):
    if ill:
        ANIMS[ill['type']](frame, cx, cy, lt, dur, pal, ill, al)
