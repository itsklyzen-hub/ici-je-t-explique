"""Mini-vidéos (« saynètes ») : de petites scènes animées qui montrent un exemple.

Une saynète se décrit en JSON : des acteurs (personnages ou icônes) et des actions datées
(tir, impact, téléportation, déplacement, bulle de dialogue...). Elle se joue dans une
« fenêtre » façon écran de jeu. Le format est documenté dans references/saynetes.md.

Coordonnées : x de 0 (gauche) à 100 (droite), y de 0 (haut) à 100 (bas) de la fenêtre.
`taille` d'un acteur : en % de la hauteur de la fenêtre.
"""
import math, random
from PIL import Image, ImageDraw, ImageFilter
import illustrations as ILL
from illustrations import ease_out, ease_out_back, clamp, rgba, SS, _font, FONT, FONT_BOLD

DARK = (20, 10, 40, 255)
WHITE = (255, 255, 255, 255)
RED = (235, 40, 70)
GREEN = (60, 220, 120)


def col(pal, c, default='accent2'):
    if c is None:
        c = default
    if isinstance(c, str) and c in pal:
        return tuple(pal[c][:3])
    if isinstance(c, str) and c.startswith('#'):
        return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
    return {'rouge': RED, 'vert': GREEN, 'blanc': (255, 255, 255), 'gris': (150, 150, 170)}.get(c, tuple(pal['accent2'][:3]))


def ease_io(p):
    p = clamp(p)
    return p * p * (3 - 2 * p)


# ------------------------------------------------------------------ personnage
_perso_cache = {}


def perso_sprite(size, color, expr='normal', regard=1, arme=False, casque=True, pas=-1):
    """Bonhomme bâton épais (tête ronde, membres arrondis, casque gamer). Ancre = milieu bas de l'image.
    pas = phase de marche 0..7 (-1 = immobile)."""
    k = (int(size), color, expr, regard, arme, casque, pas)
    if k in _perso_cache:
        return _perso_cache[k]
    s = size * 2
    Wb, Hb = int(s * 1.5), int(s * 1.1)
    img = Image.new('RGBA', (Wb, Hb), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, 'RGBA')
    cx, fy = Wb / 2, Hb - s * 0.03
    dirn = regard
    lw = s * 0.12                       # épaisseur des membres
    out = s * 0.035                     # contour sombre
    dark_col = tuple(int(v * 0.5) for v in color) + (255,)
    fill = rgba(color)

    def seg(p0, p1, w, c):
        d.line([p0, p1], fill=c, width=int(w))
        for x, y in (p0, p1):
            d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=c)

    sw = math.sin(pas * math.pi / 4) if pas >= 0 else 0.0
    hip = (cx, fy - s * 0.37)
    neck = (cx, fy - s * 0.63)
    sh = (cx, fy - s * 0.58)
    leg_back = (cx - s * 0.14 - sw * s * 0.13, fy - lw / 2 - max(0, sw) * s * 0.05)
    leg_front = (cx + s * 0.14 + sw * s * 0.13, fy - lw / 2 - max(0, -sw) * s * 0.05)
    hand_back = (cx - dirn * s * 0.24 + sw * s * 0.08, fy - s * 0.4)
    if arme:
        hand_front = (cx + dirn * s * 0.32, fy - s * 0.55)
    else:
        hand_front = (cx + dirn * s * 0.24 - sw * s * 0.08, fy - s * 0.4)
    hr = s * 0.19
    hx, hy = cx + dirn * s * 0.02, fy - s + hr + s * 0.01
    limbs = [(sh, hand_back, lw), (hip, leg_back, lw), (hip, leg_front, lw), (neck, hip, lw * 1.45)]
    # 1) silhouette sombre (contour), 2) remplissage couleur : pas de traits qui se chevauchent
    for p0, p1, w in limbs + [(sh, hand_front, lw)]:
        seg(p0, p1, w + out * 2, dark_col)
    d.ellipse((hx - hr - out, hy - hr - out, hx + hr + out, hy + hr + out), fill=dark_col)
    for p0, p1, w in limbs:
        seg(p0, p1, w, fill)
    d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=fill)
    ex, ey = hx + dirn * s * 0.06, hy - s * 0.01
    r = s * 0.055
    sp = s * 0.075
    if expr == 'ko':
        for o in (-1, 1):
            x0 = ex + o * sp
            d.line((x0 - r * 0.8, ey - r * 0.8, x0 + r * 0.8, ey + r * 0.8), fill=WHITE, width=int(s * 0.03))
            d.line((x0 - r * 0.8, ey + r * 0.8, x0 + r * 0.8, ey - r * 0.8), fill=WHITE, width=int(s * 0.03))
        d.line([(ex - s * 0.07 + i * s * 0.035, ey + s * 0.1 + (s * 0.015 if i % 2 else -s * 0.015)) for i in range(5)],
               fill=DARK, width=int(s * 0.02))
    elif expr == 'content':
        for o in (-1, 1):
            x0 = ex + o * sp
            d.arc((x0 - r, ey - r * 0.6, x0 + r, ey + r * 1.2), 200, 340, fill=WHITE, width=int(s * 0.03))
        d.chord((ex - s * 0.07, ey + s * 0.03, ex + s * 0.07, ey + s * 0.14), 0, 180, fill=DARK)
    else:
        big = expr in ('surpris', 'peur')
        rr = r * (1.3 if big else 1)
        for o in (-1, 1):
            x0 = ex + o * sp
            d.ellipse((x0 - rr, ey - rr * 1.1, x0 + rr, ey + rr * 1.1), fill=WHITE)
            pr = rr * (0.38 if big else 0.52)
            px = x0 + dirn * rr * 0.35
            d.ellipse((px - pr, ey - pr, px + pr, ey + pr), fill=DARK)
        if big:
            d.ellipse((ex - s * 0.03, ey + s * 0.08, ex + s * 0.03, ey + s * 0.15), fill=DARK)
        elif expr == 'fache':
            for o in (-1, 1):
                x0 = ex + o * sp
                d.line((x0 - r, ey - r * 1.7 - o * r * 0.4 * dirn, x0 + r, ey - r * 1.7 + o * r * 0.4 * dirn),
                       fill=DARK, width=int(s * 0.025))
            d.arc((ex - s * 0.05, ey + s * 0.09, ex + s * 0.05, ey + s * 0.17), 200, 340, fill=DARK, width=int(s * 0.02))
        else:
            d.arc((ex - s * 0.045, ey + s * 0.04, ex + s * 0.045, ey + s * 0.11), 20, 160, fill=DARK, width=int(s * 0.02))
    if casque:
        d.arc((hx - hr * 1.12, hy - hr * 1.12, hx + hr * 1.12, hy + hr * 1.12), 195, 345, fill=DARK, width=int(s * 0.035))
        cupx = hx - dirn * hr * 0.95
        d.rounded_rectangle((cupx - s * 0.045, hy - s * 0.06, cupx + s * 0.045, hy + s * 0.07), s * 0.03, fill=DARK)
    seg(sh, hand_front, lw, fill)   # bras avant par-dessus la tête et le corps (contour déjà dans la silhouette)
    if arme:
        gx, gy = hand_front
        gx1 = gx + dirn * s * 0.27
        d.rounded_rectangle((min(gx - dirn * s * 0.04, gx1), gy - s * 0.045, max(gx - dirn * s * 0.04, gx1), gy + s * 0.045),
                            s * 0.02, fill=(40, 40, 60, 255))
        d.rounded_rectangle((min(gx, gx + dirn * s * 0.07), gy, max(gx, gx + dirn * s * 0.07), gy + s * 0.12), s * 0.02,
                            fill=(40, 40, 60, 255))
        d.rectangle((min(gx1, gx1 - dirn * s * 0.05), gy - s * 0.045, max(gx1, gx1 - dirn * s * 0.05), gy + s * 0.045), fill=fill)
        d.ellipse((gx - lw * 0.6, gy - lw * 0.6, gx + lw * 0.6, gy + lw * 0.6), fill=fill, outline=dark_col, width=int(out))
    img = img.reduce(2)
    _perso_cache[k] = img
    return img


# ------------------------------------------------------------------ fond de fenêtre
_bg_cache = {}


def window_bg(w, h, sol, border):
    k = (w, h, sol, border)
    if k in _bg_cache:
        return _bg_cache[k]
    img = Image.new('RGBA', (w, h), (12, 6, 30, 255))
    d = ImageDraw.Draw(img, 'RGBA')
    for y in range(h):
        a = int(40 * (y / h))
        d.line((0, y, w, y), fill=(60, 30, 120, a))
    gy = int(h * sol / 100)
    d.rectangle((0, gy, w, h), fill=(30, 16, 70, 255))
    for k2 in range(-12, 13):
        d.line((w / 2 + k2 * 60, gy, w / 2 + k2 * 160, h), fill=border + (50,), width=2)
    for j in range(1, 5):
        y = gy + (h - gy) * (j / 5) ** 1.6
        d.line((0, y, w, y), fill=border + (40,), width=2)
    d.line((0, gy, w, gy), fill=border + (170,), width=3)
    _bg_cache[k] = img
    return img


# ------------------------------------------------------------------ moteur
class Saynete:
    def __init__(self, spec, pal, w, h):
        self.spec, self.pal, self.w, self.h = spec, pal, w, h
        self.duree = float(spec.get('duree', 3.0))
        self.sol = float(spec.get('sol', 88))
        self.acteurs = spec.get('acteurs', {})
        self.actions = sorted(spec.get('actions', []), key=lambda a: a.get('t', 0))

    def px(self, x, y):
        return x / 100 * self.w, y / 100 * self.h

    def size_px(self, a):
        return float(a.get('taille', 40)) / 100 * self.h

    def state(self, name, t):
        a = self.acteurs[name]
        st = dict(x=float(a.get('x', 50)), y=float(a.get('y', self.sol)), alpha=1.0 if a.get('visible', True) else 0.0,
                  expr=a.get('expression', 'normal'), regard=1 if a.get('regard', 'droite') == 'droite' else -1,
                  dy=0.0, shake=0.0, glitch=-1.0, pas=-1, ghost=None, flash=0.0, scale=1.0, rot=0.0)
        for ac in self.actions:
            qui = ac.get('qui') or ac.get('sur')
            if qui != name:
                continue
            t0 = float(ac.get('t', 0))
            if t < t0:
                break
            dt = t - t0
            act = ac.get('action')
            du = float(ac.get('duree', 0.6))
            if act == 'deplace':
                p = ease_io(dt / du)
                if dt < du:
                    st['pas'] = int(dt * 14) % 8
                if 'x' in ac:
                    st['x'] = st['x'] + (float(ac['x']) - st['x']) * p
                if 'y' in ac:
                    st['y'] = st['y'] + (float(ac['y']) - st['y']) * p
            elif act == 'teleporte':
                ox, oy = st['x'], st['y']
                st['x'], st['y'] = float(ac.get('x', st['x'])), float(ac.get('y', st['y']))
                if ac.get('glitch', True):
                    st['glitch'] = dt
                    st['ghost'] = (ox, oy, dt)
            elif act == 'expression':
                st['expr'] = ac.get('expression', 'normal')
            elif act == 'regarde':
                st['regard'] = 1 if ac.get('vers', 'droite') == 'droite' else -1
            elif act == 'saute':
                if dt < du:
                    st['dy'] = -math.sin(math.pi * dt / du) * float(ac.get('hauteur', 25))
            elif act == 'tremble':
                if dt < du:
                    st['shake'] = (1 - dt / du)
            elif act == 'impact':
                if dt < 0.4:
                    st['shake'] = max(st['shake'], 1 - dt / 0.4)
                    st['flash'] = max(0, 1 - dt / 0.15)
            elif act == 'apparait':
                st['alpha'] = ease_out(dt / 0.25)
                st['scale'] = ease_out_back(dt / 0.35)
            elif act == 'disparait':
                st['alpha'] = 1 - ease_out(dt / 0.25)
            elif act == 'tombe':
                st['expr'] = 'ko'
                st['rot'] = -st['regard'] * 90 * ease_out_back(dt / 0.35, 1.2)
            elif act == 'grandit':
                st['scale'] = 1 + (float(ac.get('echelle', 1.5)) - 1) * ease_out_back(dt / du)
        return st

    def actor_sprite(self, name, st):
        a = self.acteurs[name]
        size = self.size_px(a)
        forme = a.get('forme', 'perso')
        c = col(self.pal, a.get('couleur'))
        if forme == 'perso':
            spr = perso_sprite(size, c, st['expr'], st['regard'], a.get('arme', False), a.get('casque', True), st['pas'])
            anchor = 'bas'
        else:
            spr = ILL.icon_sprite(forme, size, c)
            anchor = 'centre'
        return spr, anchor, size

    def hand(self, name, t):
        st = self.state(name, t)
        a = self.acteurs[name]
        size = self.size_px(a)
        x, y = self.px(st['x'], st['y'])
        if a.get('forme', 'perso') == 'perso':
            return x + st['regard'] * size * 0.62, y - size * 0.55
        return x, y

    def center(self, name, t):
        st = self.state(name, t)
        a = self.acteurs[name]
        size = self.size_px(a)
        x, y = self.px(st['x'], st['y'])
        if a.get('forme', 'perso') == 'perso':
            return x, y - size * 0.5
        return x, y

    def render(self, t, alpha=1.0, border=(0, 229, 255)):
        w, h = self.w, self.h
        win = window_bg(w, h, self.sol, border).copy()
        ss = SS(0, 0, w, h)
        # fantômes + acteurs
        for name, a in self.acteurs.items():
            st = self.state(name, t)
            if st['alpha'] <= 0.01:
                continue
            spr, anchor, size = self.actor_sprite(name, st)
            bob = math.sin(t * 4 + sum(map(ord, name)) % 7) * size * 0.02 if a.get('forme', 'perso') == 'perso' and st['expr'] != 'ko' else 0
            if st['ghost'] and st['ghost'][2] < 0.6:
                gx, gy = self.px(st['ghost'][0], st['ghost'][1])
                ga = 0.55 * (1 - st['ghost'][2] / 0.6)
                self._paste(win, spr, anchor, gx, gy, ga, tint=(255, 255, 255))
            x, y = self.px(st['x'], st['y'])
            y += st['dy'] / 100 * h + bob
            if st['shake'] > 0:
                x += math.sin(t * 90) * 10 * st['shake']
            g = st['glitch']
            if 0 <= g < 0.35:
                self._glitch(win, spr, anchor, x, y, st['alpha'], t)
            else:
                self._paste(win, spr, anchor, x, y, st['alpha'], scale=st['scale'], rot=st['rot'],
                            flash=st['flash'])
        # effets
        for ac in self.actions:
            t0 = float(ac.get('t', 0))
            if t < t0:
                continue
            dt = t - t0
            act = ac.get('action')
            if act == 'tir':
                self._tir(ss, ac, t0, dt)
            elif act == 'impact':
                x, y = self.center(ac['sur'], t0)
                ILL.burst(ss, x, y, dt, self.pal['accent'], n=10, r0=h * 0.1, r1=h * 0.28, dur=0.4, w=6)
                ILL.ring(ss, x, y, dt, (255, 255, 255), h * 0.05, h * 0.3, 0.45, 6)
            elif act == 'texte':
                self._texte(ss, ac, t0, dt)
            elif act == 'bulle':
                self._bulle(ss, ac, t0, dt)
            elif act == 'compteur':
                du = float(ac.get('duree', 1.0))
                v = float(ac.get('de', 0)) + (float(ac.get('a', 100)) - float(ac.get('de', 0))) * ease_out(dt / du)
                x, y = self.px(float(ac.get('x', 50)), float(ac.get('y', 15)))
                ss.text(x, y, f"{ac.get('prefixe', '')}{int(round(v))}{ac.get('suffixe', '')}", float(ac.get('taille', 9)) / 100 * h,
                        rgba(col(self.pal, ac.get('couleur'), 'accent')))
            elif act == 'lag':
                # écran figé / chargement : petit rond qui tourne au centre
                du = float(ac.get('duree', 0.6))
                if dt < du:
                    x, y = self.px(float(ac.get('x', 50)), float(ac.get('y', 40)))
                    a0 = (dt * 600) % 360
                    ss.arc(x, y, h * 0.07, a0, a0 + 270, rgba((255, 255, 255), 220), h * 0.018)
        ss.done(win)
        for ac in self.actions:
            if ac.get('action') == 'flash' and 0 <= t - float(ac.get('t', 0)) < 0.25:
                a = 1 - (t - float(ac['t'])) / 0.25
                win.alpha_composite(Image.new('RGBA', (w, h), (255, 255, 255, int(180 * a))))
        return win

    def _paste(self, win, spr, anchor, x, y, alpha, scale=1.0, rot=0.0, flash=0.0, tint=None):
        if scale != 1.0 and scale > 0.02:
            spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.BILINEAR)
        if abs(rot) > 0.5:
            spr = spr.rotate(rot, Image.BICUBIC, expand=True)
            bb = spr.getbbox()
            if bb:
                spr = spr.crop(bb)   # pour que le perso allongé touche bien le sol
        if tint or flash > 0.02:
            c = tint or (255, 255, 255)
            k = 0.85 if tint else flash
            over = Image.new('RGBA', spr.size, c + (0,))
            over.putalpha(spr.getchannel('A').point(lambda v: int(v * k)))
            spr = spr.copy(); spr.alpha_composite(over)
        if alpha < 0.99:
            spr = spr.copy(); spr.putalpha(spr.getchannel('A').point(lambda v: int(v * alpha)))
        if anchor == 'bas':
            pos = (int(x - spr.width / 2), int(y - spr.height))
        else:
            pos = (int(x - spr.width / 2), int(y - spr.height / 2))
        win.alpha_composite(spr, pos)

    def _glitch(self, win, spr, anchor, x, y, alpha, t):
        rnd = random.Random(int(t * 30))
        for c, dx in (((0, 229, 255), -10), ((255, 46, 136), 10)):
            self._paste(win, spr, anchor, x + dx, y, 0.6 * alpha, tint=c)
        n = 6
        hgt = spr.height
        out = Image.new('RGBA', (spr.width + 80, hgt), (0, 0, 0, 0))
        for k in range(n):
            y0, y1 = int(k * hgt / n), int((k + 1) * hgt / n)
            band = spr.crop((0, y0, spr.width, y1))
            out.alpha_composite(band, (40 + rnd.randint(-30, 30), y0))
        if rnd.random() > 0.25:
            self._paste(win, out, anchor, x, y, alpha)

    def _tir(self, ss, ac, t0, dt):
        du = float(ac.get('duree', 0.2))
        x0, y0 = self.hand(ac['de'], t0)
        if 'vers' in ac and ac['vers'] in self.acteurs:
            x1, y1 = self.center(ac['vers'], t0)
        else:
            x1, y1 = self.px(float(ac.get('x', 100)), float(ac.get('y', 50)))
        c = col(self.pal, ac.get('couleur'), 'accent')
        ILL.burst(ss, x0, y0, dt, c, n=6, r0=8, r1=40, dur=0.18, w=5)
        if ac.get('rate'):
            # la balle continue sa route jusqu'au bord
            L = math.hypot(x1 - x0, y1 - y0) or 1
            ux, uy = (x1 - x0) / L, (y1 - y0) / L
            far = (self.w + 100 - x0) / ux if abs(ux) > 0.01 else 2000
            if ux < 0:
                far = (x0 + 100) / -ux
            x2, y2 = x0 + ux * far, y0 + uy * far
            du2 = du * far / L
        else:
            x2, y2, du2 = x1, y1, du
        if dt > du2:
            return
        p = dt / du2
        bx, by = x0 + (x2 - x0) * p, y0 + (y2 - y0) * p
        tx, ty = x0 + (x2 - x0) * max(0, p - 0.25 * du / du2), y0 + (y2 - y0) * max(0, p - 0.25 * du / du2)
        ss.line([(tx, ty), (bx, by)], rgba(c, 160), self.h * 0.02)
        ILL.glow_dot(ss, bx, by, self.h * 0.018, c)

    def _texte(self, ss, ac, t0, dt):
        du = float(ac.get('duree', 1.0))
        if dt > du:
            return
        if 'sur' in ac and ac['sur'] in self.acteurs:
            x, y = self.center(ac['sur'], t0)
            y -= self.size_px(self.acteurs[ac['sur']]) * 0.75
        else:
            x, y = self.px(float(ac.get('x', 50)), float(ac.get('y', 20)))
        sc = ease_out_back(dt / 0.25)
        a = clamp((du - dt) / 0.25)
        y -= dt * self.h * 0.06
        ss.text(x, y, ac.get('texte', ''), float(ac.get('taille', 11)) / 100 * self.h * max(0.05, sc),
                rgba(col(self.pal, ac.get('couleur'), 'accent'), 255 * a))

    def _bulle(self, ss, ac, t0, dt):
        du = float(ac.get('duree', 1.2))
        if dt > du:
            return
        name = ac['qui']
        a_ = self.acteurs[name]
        x, y = self.center(name, t0 + dt)
        size = self.size_px(a_)
        txt = ac.get('texte', '...')
        fs = float(ac.get('taille', 8)) / 100 * self.h
        f = _font(FONT_BOLD, fs)
        tw = f.getlength(txt)
        sc = ease_out_back(dt / 0.25)
        al = clamp((du - dt) / 0.2)
        bx = x + (size * 0.2)
        by = y - size * 0.75
        wbox, hbox = (tw + fs * 1.2) * sc, fs * 1.7 * sc
        bx = min(max(bx, wbox / 2 + 8), self.w - wbox / 2 - 8)
        ss.poly([(x + size * 0.05, by + hbox / 2 - 2), (x + size * 0.25, by + hbox / 2 - 2), (x + size * 0.1, by + hbox / 2 + fs * 0.6 * sc)],
                (255, 255, 255, int(255 * al)))
        ss.rr((bx - wbox / 2, by - hbox / 2, bx + wbox / 2, by + hbox / 2), hbox * 0.45, (255, 255, 255, int(255 * al)))
        if sc > 0.3:
            ss.d.text(ss.p(bx, by), txt, font=_font(FONT_BOLD, fs * 2 * sc), fill=(20, 10, 40, int(255 * al)), anchor='mm')


_sayn_cache = {}


def draw_window(frame, x0, y0, w, h, spec, lt, pal, al, titre=None, couleur='accent2', delai=0.0):
    """Dessine une fenêtre de saynète sur l'image. lt = temps local de la scène."""
    k = (id(spec), w, h)
    if k not in _sayn_cache:
        _sayn_cache[k] = Saynete(spec, pal, w, h)
    sy = _sayn_cache[k]
    border = col(pal, couleur)
    started = lt >= delai
    if started:
        tt = lt - delai
        t = tt % sy.duree if spec.get('boucle', True) else min(tt, sy.duree)
    else:
        t = 0.0
    p = ease_out_back((lt - min(delai, 0.1)) / 0.4, 1.2) if lt < delai + 0.4 else 1
    p = max(0.0, min(p, 1.08))
    if p <= 0.02:
        return
    win = sy.render(t, border=border)
    if not started:
        dim = Image.new('RGBA', win.size, (10, 5, 25, 140))
        win.alpha_composite(dim)
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), 34, fill=int(255 * al))
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out.paste(win, (0, 0), mask)
    ImageDraw.Draw(out).rounded_rectangle((0, 0, w - 1, h - 1), 34, outline=border + (int(255 * al),), width=7)
    if titre:
        f = _font(FONT, 46)
        tw = f.getlength(titre)
        ImageDraw.Draw(out).rounded_rectangle((22, 20, 22 + tw + 44, 86), 30, fill=border + (int(235 * al),))
        ImageDraw.Draw(out).text((44, 53), titre, font=f, fill=(20, 10, 40, int(255 * al)), anchor='lm')
    if p != 1:
        out = out.resize((max(1, int(w * p)), max(1, int(h * p))), Image.BILINEAR)
    frame.alpha_composite(out, (int(x0 + (w - out.width) / 2), int(y0 + (h - out.height) / 2)))
