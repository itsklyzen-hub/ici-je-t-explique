#!/usr/bin/env python3
"""Vidéo explicative gaming/streaming : texte animé + sous-titres + voix off + musique.

Usage :
  python3 render_explication.py scenes.json --out video.mp4 [--voix voix.mp3]
  python3 render_explication.py scenes.json --still 3.2 --out apercu.png [--voix voix.mp3]
  python3 render_explication.py scenes.json --timing [--voix voix.mp3]

Format 1080x1920, 30 fps. Le format de scenes.json est décrit dans references/format_scenes.md.
"""
import argparse, json, math, os, re, subprocess, sys, tempfile, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import illustrations as ILL  # noqa: E402
import saynetes as SAY  # noqa: E402

W, H, FPS = 1080, 1920, 30
SR = 44100
VO = 0.35            # la voix démarre à 0,35 s
TAIL = 1.2           # temps après la fin de la voix
FONT_DIR = '/usr/share/fonts/opentype/inter'
FONT_BLACK = f'{FONT_DIR}/Inter-Black.otf'
FONT_BOLD = f'{FONT_DIR}/Inter-Bold.otf'
MAXW = 880           # largeur utile du texte (zones sûres TikTok/Reels)
CY = 820             # centre vertical de la zone de contenu
SUB_Y = 1390         # sous-titres (au-dessus de l'interface TikTok)
ILL_CY = 565         # centre des illustrations animées

PALETTE = dict(
    fond1=(14, 8, 38), fond2=(48, 10, 72), grille=(120, 70, 255),
    texte=(255, 255, 255), accent=(255, 214, 10), accent2=(0, 229, 255), accent3=(255, 46, 136),
)


def rgb(c):
    if isinstance(c, (list, tuple)):
        return tuple(c)
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- audio utils
def decode_audio(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    st = (x * 32767).astype(np.int16)
    with wave.open(path, 'wb') as f:
        f.setnchannels(2 if st.ndim == 2 else 1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(st.tobytes())


# ---------------------------------------------------------------- timing
def plain(s):
    return re.sub(r'[*]', '', s or '')


def compute_timing(cfg, voice_dur):
    scenes = cfg['scenes']
    if all('debut' in s and 'fin' in s for s in scenes):
        total = max(s['fin'] for s in scenes) + (0 if voice_dur is None else 0.3)
        return total
    lens = [max(8, len(plain(s.get('voix', '')))) + 6 for s in scenes]  # +6 ~ petite pause entre scènes
    if voice_dur is not None:
        speech = voice_dur
    else:
        speech = sum(lens) / 14.5   # débit moyen d'une voix française ~14,5 caractères/s
    t = VO
    for s, n in zip(scenes, lens):
        d = speech * n / sum(lens)
        s['debut'], s['fin'] = round(t, 3), round(t + d, 3)
        t += d
    scenes[0]['debut'] = 0.0
    scenes[-1]['fin'] = round(t + TAIL, 3)
    return scenes[-1]['fin']


def build_subtitles(cfg):
    subs = []
    for s in cfg['scenes']:
        words = plain(s.get('voix', '')).split()
        if not words:
            continue
        chunks, cur = [], []
        for w in words:
            cur.append(w)
            if len(' '.join(cur)) >= 20 or w[-1] in '.?!,:' or len(cur) >= 5:
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
        a = s['debut'] + (VO if s is cfg['scenes'][0] else 0.05)
        b = s['fin'] - (TAIL if s is cfg['scenes'][-1] else 0.05)
        tot = sum(len(' '.join(c)) + 2 for c in chunks)
        t = a
        for c in chunks:
            d = (b - a) * (len(' '.join(c)) + 2) / tot
            subs.append(dict(debut=t, fin=t + d, mots=c))
            t += d
    return subs


# ---------------------------------------------------------------- drawing helpers
_font_cache, _sprite_cache = {}, {}


def font(path, size):
    k = (path, size)
    if k not in _font_cache:
        _font_cache[k] = ImageFont.truetype(path, size)
    return _font_cache[k]


def word_sprite(word, size, color, path=FONT_BLACK, stroke=None):
    k = (word, size, color, path)
    if k in _sprite_cache:
        return _sprite_cache[k]
    f = font(path, size)
    stroke = max(4, size // 11) if stroke is None else stroke
    bb = f.getbbox(word, stroke_width=stroke)
    pad = 24
    w, h = bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad + 14
    org = (pad - bb[0], pad - bb[1])
    shadow = Image.new('L', (w, h), 0)
    ImageDraw.Draw(shadow).text((org[0], org[1] + 12), word, font=f, fill=170, stroke_width=stroke, stroke_fill=170)
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    img.paste((0, 0, 0, 255), (0, 0), shadow)
    d = ImageDraw.Draw(img)
    d.text(org, word, font=f, fill=color + (255,), stroke_width=stroke, stroke_fill=(10, 6, 25, 255))
    # ancre = position de la ligne de base gauche du texte
    spr = (img, org, f.getlength(word))
    _sprite_cache[k] = spr
    return spr


def parse_rich(text):
    """'Le *ping* c'est...' -> [(mot, accentué)]"""
    out = []
    for tok in re.findall(r'\*[^*]+\*|\S+', text or ''):
        if tok.startswith('*') and tok.endswith('*'):
            out += [(w, True) for w in tok[1:-1].split()]
        elif out and re.fullmatch(r'[?!:;»%]+', tok):
            out[-1] = (out[-1][0] + '\u202f' + tok, out[-1][1])   # « ? » jamais seul en début de ligne
        else:
            out.append((tok, False))
    return out


def layout(text, size, maxw, max_lines, path=FONT_BLACK, min_size=60):
    words = parse_rich(text)
    while True:
        f = font(path, size)
        sp = f.getlength(' ')
        lines, cur, cw = [], [], 0
        for w, acc in words:
            ww = f.getlength(w)
            if cur and cw + sp + ww > maxw:
                lines.append(cur); cur, cw = [], 0
            cur.append((w, acc, ww)); cw += (sp if len(cur) > 1 else 0) + ww
        if cur:
            lines.append(cur)
        widest = max((sum(x[2] for x in l) + sp * (len(l) - 1)) for l in lines) if lines else 0
        if (len(lines) <= max_lines and widest <= maxw) or size <= min_size:
            break
        size -= 6
    lh = int(size * 1.12)
    placed = []
    for li, l in enumerate(lines):
        lw = sum(x[2] for x in l) + sp * (len(l) - 1)
        x = -lw / 2
        y = (li - (len(lines) - 1) / 2) * lh
        for w, acc, ww in l:
            placed.append(dict(mot=w, acc=acc, x=x, y=y, w=ww))
            x += ww + sp
    return placed, size, len(lines) * lh


def ease_out_back(p, k=2.0):
    p = min(1, max(0, p)) - 1
    return 1 + (k + 1) * p ** 3 + k * p ** 2


def ease_out(p):
    p = min(1, max(0, p))
    return 1 - (1 - p) ** 3


def paste(frame, spr, cx, base_y, scale=1.0, alpha=1.0, left=None):
    """Colle un mot : cx = centre horizontal (ou left), base_y = haut du texte."""
    img, org, adv = spr
    if scale <= 0.02 or alpha <= 0.01:
        return
    if abs(scale - 1) > 0.01:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.BILINEAR)
    if alpha < 0.99:
        a = img.getchannel('A').point(lambda v: int(v * alpha))
        img = img.copy(); img.putalpha(a)
    ox, oy = org[0] * scale, org[1] * scale
    if left is not None:
        x = left - ox + adv * (1 - scale) / 2
    else:
        x = cx - img.width / 2
    frame.alpha_composite(img, (int(round(x)), int(round(base_y - oy))))


def draw_words(frame, placed, size, cx, cy, t0, t, colors, stagger=0.09, pop=0.28, alpha=1.0, wave_amp=0.0):
    for i, p in enumerate(placed):
        ts = t0 + i * stagger
        if t < ts:
            continue
        pr = (t - ts) / pop
        sc = ease_out_back(pr) if pr < 1 else 1.0
        col = colors['accent'] if p['acc'] else colors['texte']
        spr = word_sprite(p['mot'], size, col)
        dy = 0
        if p['acc'] and pr >= 1:
            dy = math.sin((t - ts) * 6) * wave_amp
        paste(frame, spr, None, cy + p['y'] - size * 0.5 + dy, sc, alpha, left=cx + p['x'])
        if p['acc'] and t - ts < 0.45 and size >= 70:
            wx, wy = cx + p['x'] + p['w'] / 2, cy + p['y']
            rx = p['w'] / 2 + 90
            ss = ILL.SS(wx - rx - 40, wy - size - 60, wx + rx + 40, wy + size + 60)
            for sgn in (-1, 1):   # petits traits qui jaillissent des deux côtés du mot
                for k in (-1, 0, 1):
                    ang = (0 if sgn > 0 else math.pi) + k * 0.5
                    ox = wx + sgn * (p['w'] / 2 + 10)
                    pr2 = ease_out((t - ts) / 0.45)
                    r0, r1 = 20 + 50 * pr2, 50 + 70 * pr2
                    ss.line([(ox + r0 * math.cos(ang), wy + r0 * math.sin(ang)), (ox + r1 * math.cos(ang), wy + r1 * math.sin(ang))],
                            colors['accent'] + (int(255 * (1 - (t - ts) / 0.45) * alpha),), 7)
            ss.done(frame)


def rounded_rect(frame, box, r, fill, outline=None, width=0):
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    if x1 - x0 < 2 or y1 - y0 < 2:
        return
    patch = Image.new('RGBA', (x1 - x0 + 1, y1 - y0 + 1), (0, 0, 0, 0))
    ImageDraw.Draw(patch).rounded_rectangle((0, 0, x1 - x0, y1 - y0), max(0, int(r)), fill=fill, outline=outline, width=width)
    frame.alpha_composite(patch, (x0, y0))


# ---------------------------------------------------------------- background
class Background:
    def __init__(self, pal):
        y = np.linspace(0, 1, H)[:, None, None]
        x = np.linspace(-1, 1, W)[None, :, None]
        c1, c2 = np.array(pal['fond1'], float), np.array(pal['fond2'], float)
        g = c1 * (1 - y) + c2 * y
        glow = np.exp(-((x * 0.9) ** 2 + ((y - 0.42) * 1.6) ** 2) * 2.2)
        g = g + glow * np.array(pal['grille'], float) * 0.22
        vign = 1 - 0.45 * (x ** 2) * 0.6 - 0.35 * ((y - 0.5) * 2) ** 4
        self.base = np.clip(g * vign, 0, 255).astype(np.float32)
        # grille en perspective (style "synthwave") : lignes verticales fixes précalculées,
        # lignes horizontales qui défilent ajoutées à chaque image
        self.grid_col = np.array(pal['grille'], np.float32)
        self.hz = hz = int(H * 0.70)
        depth = (np.arange(hz, H) - hz + 1) / (H - hz)
        self.depth = depth
        a = self.base
        xs = np.arange(W)[None, :]
        dep = depth[:, None]
        for k in range(-9, 10):
            xk = W / 2 + k * 260 * dep
            d = np.clip(1 - np.abs(xs - xk) / (2.2 * dep + 0.6), 0, 1) * 0.5 * dep ** 0.5
            a[hz:] += d[:, :, None] * self.grid_col
        a[hz - 3:hz + 3] += self.grid_col * 0.8
        self.static = np.clip(a, 0, 255).astype(np.uint8)
        self.static_f = np.clip(a, 0, 255)
        rng = np.random.default_rng(3)
        self.stars = [(rng.uniform(0, W), rng.uniform(0, hz), rng.uniform(0.5, 2.2), rng.uniform(0, 6.28)) for _ in range(70)]

    def frame(self, t, flash=0.0, pulse=0.0):
        hz = self.hz
        phase = (1 / self.depth + t * 1.6) % 1.0
        line = np.clip(1 - np.abs(phase - 0.5) * 2 * 14, 0, 1) * self.depth ** 0.6 * (0.45 + 0.25 * pulse)
        rows = np.nonzero(line > 0.01)[0]
        if flash > 0.005:
            img = np.clip(self.static_f + flash * 255, 0, 255).astype(np.uint8)
        else:
            img = self.static.copy()
        if len(rows):
            sub = self.static_f[hz + rows] + line[rows, None, None] * self.grid_col + flash * 255
            img[hz + rows] = np.clip(sub, 0, 255).astype(np.uint8)
        fr = Image.fromarray(img, 'RGB').convert('RGBA')
        d = ImageDraw.Draw(fr)
        for (sx, sy, r, ph) in self.stars:
            yy = (sy + t * 18 * r) % hz
            b = int(140 + 110 * math.sin(t * 2 + ph))
            d.ellipse((sx - r, yy - r, sx + r, yy + r), fill=(b, b, 255, 255))
        return fr


# ---------------------------------------------------------------- scenes
def scene_alpha(s, t):
    a = ease_out((t - s['debut']) / 0.18)
    b = ease_out((s['fin'] - t) / 0.18) if s.get('_has_next') else 1
    return min(a, b)


def draw_scene(frame, s, t, cfg, pal):
    typ = s.get('type', 'texte')
    t0 = s['debut']
    al = scene_alpha(s, t)
    lt = t - t0
    ill = s.get('_ill')
    if ill and typ not in ('versus', 'liste'):
        ILL.draw(frame, ill, W / 2, ILL_CY - (40 if typ == 'chiffre' else 0), lt, s['fin'] - t0, pal, al)
    if typ in ('accroche', 'texte'):
        big = 150 if typ == 'accroche' else 120
        placed, size, bh = layout(s.get('texte', ''), big if not ill else 124, MAXW, 3 if ill else 4)
        shake = math.sin(lt * 70) * max(0, 1 - lt / 0.35) * 14 if typ == 'accroche' else 0
        draw_words(frame, placed, size, W / 2 + shake, 1040 if ill else CY, t0 + 0.05, t, pal,
                   stagger=0.12, pop=0.3, alpha=al, wave_amp=6)
    elif typ == 'point':
        n = str(s.get('numero', ''))
        top, r0 = (850, 48) if ill else (CY - 250, 95)
        if n:
            sc = ease_out_back((lt) / 0.35)
            r = r0 * sc
            if r > 2:
                rounded_rect(frame, (W / 2 - r, top - r, W / 2 + r, top + r), int(r * 0.32), pal['accent3'] + (int(255 * al),))
                paste(frame, word_sprite(n, int(r0 * 1.26), pal['texte']), W / 2, top - r0 * 0.76, sc, al)
        placed, size, bh = layout(s.get('texte', ''), 104 if ill else 116, MAXW, 2 if ill else 3)
        y0 = 1020 if ill else CY + 20
        draw_words(frame, placed, size, W / 2, y0, t0 + 0.2, t, pal, alpha=al)
        if s.get('detail'):
            dp, dsz, _ = layout(s['detail'], 56 if ill else 60, MAXW, 2, path=FONT_BOLD, min_size=40)
            dcol = dict(pal, texte=(215, 210, 255))
            draw_words(frame, dp, dsz, W / 2, y0 + bh / 2 + (80 if ill else 110), t0 + 0.6, t, dcol, stagger=0.04, alpha=al)
    elif typ == 'chiffre':
        val = float(s.get('valeur', 0))
        p = ease_out(lt / 1.0)
        dec = int(s.get('decimales', 0))
        cur = val * p
        txt = f"{cur:,.{dec}f}".replace(',', ' ').replace('.', ',') if dec else f"{int(round(cur)):,}".replace(',', ' ')
        size_n = 210 if ill else 250
        num = word_sprite(txt, size_n, pal['accent'])
        unit = s.get('unite', '')
        sc = ease_out_back(lt / 0.3) * (1 + 0.08 * math.exp(-((lt - 1.05) / 0.08) ** 2))
        y = 790 if ill else CY - 260
        if unit:
            us = word_sprite(unit, int(size_n * 0.48), pal['accent2'])
            total = num[2] + 24 + us[2]
            paste(frame, num, None, y, sc, al, left=W / 2 - total / 2)
            paste(frame, us, None, y + size_n * 0.46, sc, al, left=W / 2 - total / 2 + num[2] + 24)
        else:
            paste(frame, num, W / 2, y, sc, al)
        ss = ILL.SS(0, y - 150, W, y + size_n + 150)
        ILL.burst(ss, W / 2, y + size_n * 0.5, lt - 1.0, pal['accent'], n=14, r0=size_n * 0.9, r1=size_n * 1.5, dur=0.45, w=9)
        ss.done(frame, al)
        placed, size, bh = layout(s.get('texte', ''), 88 if ill else 96, MAXW, 2 if ill else 3)
        draw_words(frame, placed, size, W / 2, 1180 if ill else CY + 150, t0 + 0.5, t, pal, alpha=al)
    elif typ == 'exemple':
        fen = (s.get('fenetres') or [])[:2]
        dur = s['fin'] - t0
        if len(fen) == 2:
            boxes, ty = [(90, 330, 900, 390), (90, 755, 900, 390)], 1255
        else:
            boxes, ty = [(90, 340, 900, 620)], 1110
        for i, (fw, box) in enumerate(zip(fen, boxes)):
            delai = float(fw.get('delai', i * dur * 0.42))
            SAY.draw_window(frame, *box, fw.get('saynete', {}), lt, pal, al, fw.get('titre'),
                            fw.get('couleur', ('accent2', 'accent3')[i % 2]), delai)
        if s.get('texte'):
            placed, size, _ = layout(s['texte'], 80, MAXW, 2)
            draw_words(frame, placed, size, W / 2, ty, t0 + 0.6, t, pal, alpha=al)
    elif typ == 'versus':
        for side, key, col, d in ((-1, 'gauche', pal['accent2'], 0.0), (1, 'droite', pal['accent3'], 0.2)):
            p = ease_out((lt - d) / 0.4)
            if p <= 0:
                continue
            cy = CY - 130 + side * 175
            cx = W / 2 + side * (1 - p) * 260
            box = (cx - 420, cy - 135, cx + 420, cy + 135)
            rounded_rect(frame, box, 40, (20, 12, 50, int(220 * al * p)), outline=col + (int(255 * al * p),), width=8)
            icon = s.get(key + '_icone')
            tx, tw = (cx + 75, 600) if icon else (cx, 760)
            if icon:
                bob = math.sin(lt * 3 + side) * 6
                ILL.paste_icon(frame, icon, cx - 300, cy + bob, 150, col, ease_out_back((lt - d - 0.1) / 0.4), al * p)
            sub = s.get(key + '_detail')
            placed, size, _ = layout(s.get(key, ''), 100, tw, 1, min_size=50)
            cc = dict(pal, texte=col)
            draw_words(frame, placed, size, tx, cy - (40 if sub else 0), t0 + d + 0.15, t, cc, stagger=0.05, alpha=al * p)
            if sub:
                sp, ssz, _ = layout(sub, 54 if not icon else 46, tw, 1, path=FONT_BOLD, min_size=32)
                draw_words(frame, sp, ssz, tx, cy + 60, t0 + d + 0.4, t, pal, stagger=0.03, alpha=al * p)
        sc = ease_out_back((lt - 0.45) / 0.3)
        if sc > 0:
            rounded_rect(frame, (W / 2 - 85 * sc, CY - 130 - 62 * sc, W / 2 + 85 * sc, CY - 130 + 62 * sc), int(40 * sc), pal['accent'] + (255,))
            paste(frame, word_sprite('VS', 90, (20, 10, 40), stroke=0), W / 2, CY - 130 - 52 * sc, sc, al)
            ss = ILL.SS(W / 2 - 260, CY - 390, W / 2 + 260, CY + 130)
            ILL.burst(ss, W / 2, CY - 130, lt - 0.5, pal['accent'], n=10, r0=110, r1=220, dur=0.4, w=8)
            ss.done(frame, al)
        if s.get('texte'):
            placed, size, _ = layout(s['texte'], 84, MAXW, 2)
            draw_words(frame, placed, size, W / 2, CY + 270, t0 + 0.8, t, pal, alpha=al)
    elif typ == 'liste':
        items = s.get('items', [])[:5]
        icones = s.get('icones') or []
        if s.get('texte'):
            placed, size, bh = layout(s['texte'], 92, MAXW, 2)
            draw_words(frame, placed, size, W / 2, CY - 250 - bh / 2, t0, t, pal, alpha=al)
        span = max(0.5, (s['fin'] - t0 - 0.6)) / max(1, len(items))
        for i, it in enumerate(items):
            ts = t0 + 0.35 + i * span
            p = ease_out((t - ts) / 0.3)
            if p <= 0:
                continue
            y = CY - 110 + i * 145
            x0 = 120 + (1 - p) * -80
            rounded_rect(frame, (x0, y - 58, W - 120, y + 58), 30, (25, 14, 60, int(200 * al * p)))
            if i < len(icones) and icones[i]:
                cols = (pal['accent2'], pal['accent3'], pal['accent'])
                ILL.paste_icon(frame, icones[i], x0 + 58, y, 84, cols[i % 3], ease_out_back((t - ts) / 0.4), al * p)
            else:
                rounded_rect(frame, (x0 + 18, y - 40, x0 + 98, y + 40), 22, pal['accent3'] + (int(255 * al * p),))
                paste(frame, word_sprite(str(i + 1), 64, pal['texte']), x0 + 58, y - 38, 1.0, al * p)
            ip, isz, _ = layout(it, 62, W - 380, 1, min_size=36)
            draw_words(frame, ip, isz, (x0 + 130 + W - 120) / 2, y, -1, t, pal, stagger=0.0, pop=0.01, alpha=al * p)
            ss = ILL.SS(x0 - 60, y - 120, x0 + 180, y + 120)
            ILL.burst(ss, x0 + 58, y, t - ts - 0.1, pal['accent'], n=8, r0=55, r1=100, dur=0.35, w=5)
            ss.done(frame, al)
    elif typ == 'fin':
        ty = 1000 if ill else CY - 120
        placed, size, bh = layout(s.get('texte', ''), 110 if ill else 120, MAXW, 2 if ill else 3)
        draw_words(frame, placed, size, W / 2, ty, t0, t, pal, alpha=al, wave_amp=5)
        py = ty + bh / 2 + (85 if ill else 110)
        pseudo = s.get('pseudo') or cfg.get('pseudo')
        if pseudo:
            sc = ease_out_back((lt - 0.5) / 0.35)
            if sc > 0:
                spr = word_sprite(pseudo, 76, (20, 10, 40), stroke=0)
                w = (spr[2] + 90) * sc
                rounded_rect(frame, (W / 2 - w / 2, py - 60 * sc, W / 2 + w / 2, py + 60 * sc), int(60 * sc), pal['accent'] + (255,))
                paste(frame, spr, W / 2, py - 52 * sc, sc, 1.0)


def draw_header(frame, cfg, t, total, pal):
    # barre de progression
    rounded_rect(frame, (60, 70, W - 60, 82), 6, (255, 255, 255, 50))
    rounded_rect(frame, (60, 70, 60 + max(12, (W - 120) * t / total), 82), 6, pal['accent'] + (255,))
    serie = cfg.get('serie')
    if serie:
        spr = word_sprite(serie.upper(), 40, (20, 10, 40), path=FONT_BLACK, stroke=0)
        w = spr[2] + 56
        rounded_rect(frame, (W / 2 - w / 2, 120, W / 2 + w / 2, 186), 33, pal['accent2'] + (255,))
        paste(frame, spr, W / 2, 128)
    titre = cfg.get('titre')
    if titre:
        placed, size, _ = layout(titre, 58, MAXW, 2, path=FONT_BLACK, min_size=40)
        cols = dict(pal, accent=pal['accent'])
        draw_words(frame, placed, size, W / 2, 262, -1, t, cols, stagger=0, pop=0.01)


def draw_subtitle(frame, subs, t, pal):
    for sb in subs:
        if sb['debut'] <= t < sb['fin']:
            words = sb['mots']
            f = font(FONT_BOLD, 60)
            text = ' '.join(words)
            tw = f.getlength(text)
            x0 = W / 2 - tw / 2
            rounded_rect(frame, (x0 - 30, SUB_Y - 18, x0 + tw + 30, SUB_Y + 82), 24, (8, 4, 20, 190))
            prog = (t - sb['debut']) / (sb['fin'] - sb['debut'])
            tot = sum(len(w) + 1 for w in words)
            acc = 0
            x = x0
            for w in words:
                active = acc / tot <= prog
                acc += len(w) + 1
                col = pal['accent'] if active else (255, 255, 255)
                spr = word_sprite(w, 60, col, path=FONT_BOLD, stroke=0)
                paste(frame, spr, None, SUB_Y, 1.0, 1.0, left=x)
                x += f.getlength(w + ' ')
            break


# ---------------------------------------------------------------- music
def make_music(total, cuts):
    """Fond musical original 110 BPM (synthèse numpy), léger, pour passer sous une voix."""
    n = int(total * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2), np.float32)
    beat = 60 / 110
    rng = np.random.default_rng(11)
    prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]  # Am F C G

    def mt(m):
        return 440 * 2 ** ((m - 69) / 12)

    def add(sig, at, g=1.0, pan=0.0):
        i = int(at * SR)
        if i >= n:
            return
        s = sig[:n - i] * g
        out[i:i + len(s), 0] += s * (1 - pan) * 0.5 * 2 ** 0.5
        out[i:i + len(s), 1] += s * (1 + pan) * 0.5 * 2 ** 0.5

    tk = np.arange(int(0.35 * SR)) / SR
    kick = np.sin(2 * np.pi * (45 * tk + 120 * (1 - np.exp(-tk * 30)) / 30)) * np.exp(-tk * 9)
    th = np.arange(int(0.05 * SR)) / SR
    hat = rng.standard_normal(len(th)) * np.exp(-th * 90)
    hat = np.diff(hat, prepend=0)
    nbeats = int(total / beat) + 1
    for b in range(nbeats):
        at = b * beat
        bar = (b // 4) % 4
        root, chord = prog[bar]
        if b % 4 == 0:
            tt = np.arange(int(beat * 4 * SR)) / SR
            env = np.minimum(1, tt / 0.4) * np.exp(-tt * 0.4)
            pad = sum(np.sign(np.sin(2 * np.pi * mt(m) * tt * (1 + dd))) * 0.3 + np.sin(2 * np.pi * mt(m) * tt)
                      for m in chord for dd in (-0.003, 0.003))
            add(pad * env * 0.025, at, pan=0)
        add(kick * 0.5, at)
        add(hat * 0.12, at + beat / 2, pan=0.3)
        # basse
        tb = np.arange(int(beat * 0.9 * SR)) / SR
        bass = np.sin(2 * np.pi * mt(root - 12) * tb) * np.exp(-tb * 3)
        add(bass * 0.22, at + beat / 2)
        # arpège "chiptune"
        for k in range(2):
            m = chord[(b * 2 + k) % 3] + 12
            ta = np.arange(int(beat / 2 * 0.8 * SR)) / SR
            sq = np.sign(np.sin(2 * np.pi * mt(m) * ta)) * np.exp(-ta * 10)
            add(sq * 0.035, at + k * beat / 2, pan=-0.3 if k else 0.3)
    # whoosh à chaque changement de scène
    tw = np.arange(int(0.5 * SR)) / SR
    nz = rng.standard_normal(len(tw))
    wh = np.convolve(nz, np.ones(30) / 30, 'same') * np.sin(np.pi * tw / tw[-1]) ** 2
    for c in cuts:
        add(wh * 0.35, max(0, c - 0.25))
    fade = np.minimum(1, (total - t) / 0.8)[:, None]
    return out * np.clip(fade, 0, 1)


def build_audio(total, cuts, voice, path):
    music = make_music(total, cuts)
    n = len(music)
    mix = music.copy()
    if voice is not None:
        v = np.zeros(n, np.float32)
        i = int(VO * SR)
        v[i:i + len(voice)] = voice[:n - i]
        # ducking : la musique baisse quand la voix parle
        env = np.sqrt(np.convolve(v ** 2, np.ones(4410) / 4410, 'same'))
        duck = 1 - 0.55 * np.clip(env / (env.max() + 1e-9) * 4, 0, 1)
        mix = music * duck[:, None] * 0.6
        peak = np.abs(v).max() + 1e-9
        mix += (v / peak * 0.8)[:, None]
    write_wav(path + '.raw.wav', mix * 0.9)
    j = subprocess.run(['ffmpeg', '-hide_banner', '-i', path + '.raw.wav', '-af',
                        'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    m = json.loads(j[j.rindex('{'):j.rindex('}') + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', path + '.raw.wav', '-af', af, '-ar', str(SR), path], check=True)
    os.remove(path + '.raw.wav')


# ---------------------------------------------------------------- main
def frame_at(t, cfg, subs, total, bg, pal):
    cuts = [s['debut'] for s in cfg['scenes'][1:]]
    flash = sum(max(0, 0.10 - abs(t - c) * 0.8) for c in cuts)
    pulse = math.exp(-((t % (60 / 110)) * 12))
    fr = bg.frame(t, flash, pulse)
    draw_header(fr, cfg, t, total, pal)
    for s in cfg['scenes']:
        if s['debut'] - 0.01 <= t < s['fin'] + (0.18 if s.get('_has_next') else 0):
            if t < s['fin']:
                draw_scene(fr, s, t, cfg, pal)
    if cfg.get('sous_titres', True):
        draw_subtitle(fr, subs, t, pal)
    return fr.convert('RGB')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('scenes')
    ap.add_argument('--voix')
    ap.add_argument('--out', default='video.mp4')
    ap.add_argument('--still', type=float, nargs='*')
    ap.add_argument('--timing', action='store_true')
    a = ap.parse_args()
    cfg = json.load(open(a.scenes, encoding='utf-8'))
    pal = dict(PALETTE)
    for k, v in (cfg.get('couleurs') or {}).items():
        pal[k] = rgb(v)
    voice = decode_audio(a.voix) if a.voix else None
    vdur = None if voice is None else len(voice) / SR
    total = compute_timing(cfg, vdur)
    for i, s in enumerate(cfg['scenes']):
        s['_has_next'] = i < len(cfg['scenes']) - 1
        s['_ill'] = ILL.normalize(s.get('illustration'))
    subs = build_subtitles(cfg)
    if a.timing or not (45 <= total <= 62):
        for s in cfg['scenes']:
            print(f"{s['debut']:6.2f} -> {s['fin']:6.2f}  {s.get('type', 'texte'):9s} {plain(s.get('texte', ''))[:50]}")
        print(f'Durée totale : {total:.1f} s' + ('' if 45 <= total <= 62 else '  (ATTENTION : hors de la cible 45-60 s)'))
        if a.timing:
            return
    bg = Background(pal)
    if a.still is not None:
        for k, ts in enumerate(a.still):
            out = a.out if len(a.still) == 1 else re.sub(r'(\.png)?$', f'_{k:02d}.png', a.out, count=1)
            frame_at(ts, cfg, subs, total, bg, pal).save(out)
            print(out)
        return
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, 'mix.wav')
    build_audio(total, [s['debut'] for s in cfg['scenes'][1:]], voice, wav)
    nf = int(total * FPS)
    p = subprocess.Popen(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', a.out],
                         stdin=subprocess.PIPE)
    for i in range(nf):
        p.stdin.write(frame_at(i / FPS, cfg, subs, total, bg, pal).tobytes())
        if i % 150 == 0:
            print(f'  image {i}/{nf}', file=sys.stderr)
    p.stdin.close()
    p.wait()
    mb = os.path.getsize(a.out) / 1e6
    print(f'OK {a.out}  {total:.1f} s  {mb:.1f} Mo' + ('  (ATTENTION > 20 Mo)' if mb > 20 else ''))


if __name__ == '__main__':
    main()
