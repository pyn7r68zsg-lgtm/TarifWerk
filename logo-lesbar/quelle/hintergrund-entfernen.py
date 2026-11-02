"""Farbe-zu-Transparenz (wie GIMP 'Color to Alpha'): entfernt einen einfarbigen Hintergrund,
ohne das Logo selbst zu veraendern. Auf dem Original-Hintergrund ergibt sich exakt das Original."""
import sys, numpy as np
from PIL import Image
src, dst, r, g, b = sys.argv[1], sys.argv[2], *map(float, sys.argv[3:6])
thr = float(sys.argv[6]) if len(sys.argv) > 6 else 0.04
c = np.asarray(Image.open(src).convert('RGB')).astype(np.float64)
bg = np.array([r, g, b])
up = np.where(c > bg, (c - bg) / np.maximum(255 - bg, 1e-6), 0)
dn = np.where(c < bg, (bg - c) / np.maximum(bg, 1e-6), 0)
a = np.max(np.maximum(up, dn), axis=2)
# JPEG-Rauschen im Hintergrund entfernen, Uebergang weich halten
a = np.clip((a - thr) / (1 - thr), 0, 1)
safe = np.maximum(a, 1e-6)[..., None]
col = np.clip((c - bg) / safe + bg, 0, 255)
out = np.dstack([col, a * 255]).round().astype(np.uint8)
im = Image.fromarray(out, 'RGBA')
bb = im.split()[3].point(lambda v: 255 if v > 6 else 0).getbbox()
pad = 6
im = im.crop((max(bb[0]-pad, 0), max(bb[1]-pad, 0), min(bb[2]+pad, im.width), min(bb[3]+pad, im.height)))
im.save(dst, optimize=True)
print(dst, im.size)
