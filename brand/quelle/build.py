"""Erzeugt das flache TarifWerk-Logosystem als SVG (Text in Pfade umgewandelt).

Aufruf aus dem Ordner brand/:
    pip install fonttools uharfbuzz
    python3 quelle/build.py quelle/Manrope.ttf svg

Manrope (SIL Open Font License) gibt es kostenlos bei Google Fonts. Es wird die
variable TTF-Datei gebraucht (Achse wght 200-800).
"""
import math, os, re, sys
import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

blob = hb.Blob.from_file_path(FONT)
face = hb.Face(blob)
UPEM = face.upem

# Markenfarben (aus dem CSS der Live-Seite)
C = dict(ink='#060b16', ink900='#0a1224', electric='#4f8dff', electric_deep='#215ee6',
         silver='#a9b4c4', silver_light='#dfe5ee', steel='#5b687e', white='#ffffff')

THEMES = {
    # dunkler Hintergrund (Header/Footer der Seite)
    'dark':  dict(a=C['electric'], b=C['silver_light'], word1=C['white'], word2=C['electric'], tag=C['silver']),
    # heller Hintergrund (Dokumente, Briefpapier, helle Seiten)
    'light': dict(a=C['electric_deep'], b=C['ink900'], word1=C['ink900'], word2=C['electric_deep'], tag=C['steel']),
}

def text_path(txt, size, wght, x0, y0, tracking=0.0):
    """Liefert (svg_path_d, breite) fuer Text mit Grundlinie bei y0."""
    font = hb.Font(face)
    font.set_variations({'wght': wght})
    buf = hb.Buffer(); buf.add_str(txt); buf.guess_segment_properties()
    hb.shape(font, buf, {'kern': True, 'liga': True})
    s = size / UPEM
    x = 0.0; parts = []
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        pen = SVGPathPen(None)
        tp = TransformPen(pen, (s, 0, 0, -s, x0 + (x + pos.x_offset) * s, y0 - pos.y_offset * s))
        font.draw_glyph_with_pen(info.codepoint, tp)
        d = pen.getCommands()
        d = re.sub(r'-?\d+\.\d+', lambda m: f'{float(m.group()):.2f}'.rstrip('0').rstrip('.'), d)
        if d: parts.append(d)
        x += pos.x_advance + (tracking * UPEM if i < n - 1 else 0)
    return ' '.join(parts), x * s

def cap_height(wght=800):
    font = hb.Font(face); font.set_variations({'wght': wght})
    ext = font.get_glyph_extents(font.get_nominal_glyph(ord('T')))
    return ext.y_bearing / UPEM  # Anteil der Schriftgroesse

# ---------- Bildmarke: zwei gleich grosse, verschraenkte Glieder auf gleicher Hoehe ----------
R, D, SW, GAP = 42.0, 17.0, 12.0, 3.5     # Halbdiagonale, Versatz, Strichstaerke, Luft an Kreuzung
MW = 2 * (D + R) + SW                     # Breite der Marke
MH = 2 * R + SW                           # Hoehe der Marke

def diamond(cx):
    return f'M{cx:.2f} {-R:.2f} L{cx+R:.2f} 0 L{cx:.2f} {R:.2f} L{cx-R:.2f} 0 Z'

def band(cx, cy, ux, uy, L):
    return (cx - ux * L, cy - uy * L, cx + ux * L, cy + uy * L)

def mark_group(theme, uid, tx, ty, scale):
    t = THEMES[theme]
    k = 1 / math.sqrt(2)
    yc = R - D
    # oben: linkes Glied liegt ueber dem rechten (Richtung der oberen rechten Kante des linken Glieds)
    b1 = band(0, -yc, k, k, SW * 1.7)
    # unten: rechtes Glied liegt ueber dem linken (Richtung der unteren linken Kante des rechten Glieds)
    b2 = band(0, yc, k, k, SW * 1.7)
    def mask(mid, b):
        x1, y1, x2, y2 = b
        return (f'<mask id="tw-{mid}" maskUnits="userSpaceOnUse" x="-120" y="-120" width="240" height="240">'
                f'<rect x="-120" y="-120" width="240" height="240" fill="#fff"/>'
                f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#000" '
                f'stroke-width="{SW + 2*GAP:.2f}" stroke-linecap="butt"/></mask>')
    # Kreuzungsrichtungen: linke Kante oben-rechts verlaeuft von (-D,-R) nach (R-D,0) => Richtung (1,1)
    # rechte Kante unten-links verlaeuft von (D-R,0) nach (D,R) => Richtung (1,1)
    defs = mask(f'{uid}mR', b1) + mask(f'{uid}mL', b2)
    common = f'fill="none" stroke-width="{SW}" stroke-linejoin="round"'
    body = (f'<g transform="translate({tx:.2f} {ty:.2f}) scale({scale:.4f})">'
            f'<path d="{diamond(D)}" stroke="{t["b"]}" {common} mask="url(#tw-{uid}mR)"/>'
            f'<path d="{diamond(-D)}" stroke="{t["a"]}" {common} mask="url(#tw-{uid}mL)"/>'
            f'</g>')
    return defs, body

def svg(w, h, defs, body, title, bg=None, rx=0):
    bgr = f'<rect width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.0f}" height="{h:.0f}" '
            f'role="img" aria-label="{title}"><title>{title}</title><defs>{defs}</defs>{bgr}{body}</svg>\n')

def wordmark(theme, x, baseline, size):
    t = THEMES[theme]
    d1, w1 = text_path('Tarif', size, 800, x, baseline, tracking=-0.015)
    d2, w2 = text_path('Werk', size, 800, x + w1 - 0.01 * size, baseline, tracking=-0.015)
    body = f'<path d="{d1}" fill="{t["word1"]}"/><path d="{d2}" fill="{t["word2"]}"/>'
    return body, w1 + w2 - 0.01 * size

def tagline(theme, x, baseline, size, tracking=0.16):
    d, w = text_path('BERATUNG AUF AUGENHÖHE', size, 600, x, baseline, tracking=tracking)
    return f'<path d="{d}" fill="{THEMES[theme]["tag"]}"/>', w

def write(name, content):
    with open(os.path.join(OUT, name), 'w') as f: f.write(content)
    print('  ', name)

CAP = cap_height()

for th in THEMES:
    # 1) Nur Zeichen
    pad = 2
    defs, body = mark_group(th, 'z', MW / 2 + pad, MH / 2 + pad, 1)
    write(f'tarifwerk-zeichen-{th}.svg', svg(MW + 2*pad, MH + 2*pad, defs, body, 'TarifWerk'))

    # 2) Horizontal ohne Unterzeile (Header): Markenhoehe = 1.35 x Versalhoehe
    size = 100.0
    capH = CAP * size
    mscale = (capH * 1.55) / MH
    mw, mh = MW * mscale, MH * mscale
    gap = 0.30 * size
    H = mh + 4
    base = H / 2 + capH / 2
    defs, mbody = mark_group(th, 'h', 2 + mw / 2, H / 2, mscale)
    wbody, ww = wordmark(th, 2 + mw + gap, base, size)
    W = 2 + mw + gap + ww + 4
    write(f'tarifwerk-logo-horizontal-{th}.svg', svg(W, H, defs, mbody + wbody, 'TarifWerk'))

    # 3) Horizontal mit Unterzeile (Footer, Briefkopf)
    wbody, ww = wordmark(th, 0, 0, size)  # nur zur Breitenmessung
    # Unterzeile auf Breite der Wortmarke ausrichten
    tsize = 20.0
    _, tw = tagline(th, 0, 0, tsize)
    tsize = tsize * ww / tw
    tcap = CAP * tsize
    block_h = capH + 0.42 * size + tcap
    mscale2 = (block_h * 1.0) / MH
    mw2, mh2 = MW * mscale2, MH * mscale2
    H2 = max(mh2, block_h) + 8
    top = (H2 - block_h) / 2
    x_text = 4 + mw2 + 0.32 * size
    defs, mbody = mark_group(th, 't', 4 + mw2 / 2, H2 / 2, mscale2)
    wbody, ww = wordmark(th, x_text, top + capH, size)
    tbody, _ = tagline(th, x_text, top + capH + 0.42 * size + tcap, tsize)
    W2 = x_text + ww + 6
    write(f'tarifwerk-logo-{th}.svg', svg(W2, H2, defs, mbody + wbody + tbody, 'TarifWerk – Beratung auf Augenhöhe'))

    # 4) Gestapelt (Social, OG-Bild, Profilbild)
    mscale3 = (capH * 2.6) / MH
    mw3, mh3 = MW * mscale3, MH * mscale3
    _, ww = wordmark(th, 0, 0, size)
    tsize3 = 20.0; _, tw = tagline(th, 0, 0, tsize3); tsize3 *= ww / tw
    W3 = max(mw3, ww) + 20
    y = 10
    defs, mbody = mark_group(th, 's', W3 / 2, y + mh3 / 2, mscale3)
    y += mh3 + 0.42 * size + capH
    wbody, _ = wordmark(th, (W3 - ww) / 2, y, size)
    y += 0.45 * size + CAP * tsize3
    tbody, _ = tagline(th, (W3 - ww) / 2, y, tsize3)
    H3 = y + 12
    write(f'tarifwerk-logo-gestapelt-{th}.svg', svg(W3, H3, defs, mbody + wbody + tbody, 'TarifWerk – Beratung auf Augenhöhe'))

    # 5) Nur Wortmarke (ohne Zeichen), mit und ohne Unterzeile
    wbody, ww = wordmark(th, 4, 4 + capH, size)
    write(f'tarifwerk-wortmarke-{th}.svg', svg(ww + 8, capH + 8 + 0.22 * size, '', wbody, 'TarifWerk'))
    tsz = 20.0; _, tw = tagline(th, 0, 0, tsz); tsz *= ww / tw
    tbody, _ = tagline(th, 4, 4 + capH + 0.42 * size + CAP * tsz, tsz)
    write(f'tarifwerk-wortmarke-unterzeile-{th}.svg', svg(ww + 8, capH + 0.42 * size + CAP * tsz + 10, '', wbody + tbody, 'TarifWerk – Beratung auf Augenhöhe'))

# 6) App-Icon / Favicon: Zeichen auf dunklem, abgerundetem Quadrat
S = 512
sc = (S * 0.72) / MW
defs, body = mark_group('dark', 'i', S / 2, S / 2, sc)
write('tarifwerk-icon.svg', svg(S, S, defs, body, 'TarifWerk', bg=C['ink'], rx=112))
# Favicon: etwas dickere Wirkung durch groesseres Zeichen
sc = (S * 0.84) / MW
defs, body = mark_group('dark', 'f', S / 2, S / 2, sc)
write('favicon.svg', svg(S, S, defs, body, 'TarifWerk', bg=C['ink'], rx=110))

# Quadratisch ohne Rundung (Apple Touch Icon / maskable): Apple rundet selbst
sc = (S * 0.66) / MW
defs, body = mark_group('dark', 'q', S / 2, S / 2, sc)
write('tarifwerk-icon-quadrat.svg', svg(S, S, defs, body, 'TarifWerk', bg=C['ink'], rx=0))
