"""Generate a 1080x1080 (usage: make_banner.py FONTS_DIR OUT.svg SHOE.png) premium sneaker banner as SVG with all text converted to outlines."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont

FONTS = sys.argv[1]
OUT = sys.argv[2]
W, H = 1080, 1080

def load(name, wght=None):
    f = TTFont(f"{FONTS}/{name}")
    if wght and "fvar" in f:
        f = instantiateVariableFont(f, {"wght": wght})
    return f

BEBAS = load("Bebas.ttf")
MONT_SB = load("Montserrat.ttf", 600)
MONT_MD = load("Montserrat.ttf", 500)


def text_path(font, text, size, tracking=0.0, sx=1.0):
    """Return (path_d, width) for text at origin baseline; tracking in em."""
    upm = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]
    scale = size / upm
    pen = SVGPathPen(gs)
    x = 0.0
    for i, ch in enumerate(text):
        g = cmap.get(ord(ch))
        if g is None:
            continue
        tp = TransformPen(pen, (scale * sx, 0, 0, -scale, x, 0))
        gs[g].draw(tp)
        x += hmtx[g][0] * scale * sx
        if i < len(text) - 1:
            x += tracking * size
    return pen.getCommands(), x


def place(font, text, size, cx=None, x=None, y=0, tracking=0.0, sx=1.0, sy=1.0, **attrs):
    d, w = text_path(font, text, size, tracking, sx)
    left = cx - w / 2 if cx is not None else x
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<path transform="translate({left:.2f} {y:.2f}) scale(1 {sy})" d="{d}" {a}/>', w


# ---------------------------------------------------------------- shoe (local 600x260 box, toe right)
import base64
SHOE_PNG = sys.argv[3]
_b64 = base64.b64encode(open(SHOE_PNG, "rb").read()).decode()
SW, SH = 840, 485  # cropped photo is 864x499
SHOE = f'<image id="shoe" width="{SW}" height="{SH}" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,{_b64}"/>'

DEFS = f"""
<defs>
  <radialGradient id="bg" cx="50%" cy="48%" r="70%">
    <stop offset="0" stop-color="#26221f"/><stop offset="0.55" stop-color="#0f0e0d"/><stop offset="1" stop-color="#050505"/>
  </radialGradient>
  <linearGradient id="word" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ece3d7"/><stop offset="0.42" stop-color="#cbbdab"/><stop offset="0.82" stop-color="#3b342e"/><stop offset="1" stop-color="#1b1816"/>
  </linearGradient>
  <linearGradient id="upper" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f1e9de"/><stop offset="1" stop-color="#cdbfad"/>
  </linearGradient>
  <linearGradient id="counter" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#bfb09c"/><stop offset="1" stop-color="#e6dccf"/>
  </linearGradient>
  <linearGradient id="toe" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#e9dfd2"/><stop offset="1" stop-color="#c8baa7"/>
  </linearGradient>
  <linearGradient id="mid" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f6f0e7"/><stop offset="1" stop-color="#d3c6b4"/>
  </linearGradient>
  <linearGradient id="outsole" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#b6a794"/><stop offset="1" stop-color="#8d7f6e"/>
  </linearGradient>
  <linearGradient id="iri" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#9fd6ff"/><stop offset="0.35" stop-color="#5c7dd8"/>
    <stop offset="0.65" stop-color="#c7a3ff"/><stop offset="1" stop-color="#eaf6ff"/>
  </linearGradient>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#f3e7d6" stop-opacity="0.22"/><stop offset="1" stop-color="#f3e7d6" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="shadow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#000" stop-opacity="0.85"/><stop offset="1" stop-color="#000" stop-opacity="0"/>
  </radialGradient>
  <filter id="dark" x="-20%" y="-30%" width="140%" height="160%"><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.75 0"/><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/></filter>
  {SHOE}
</defs>"""

parts = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']

# blurred corner shoes
parts.append('<use xlink:href="#shoe" transform="translate(-170 -40) rotate(-20) scale(0.5)" filter="url(#blur)" opacity="0.5"/>')
parts.append('<use xlink:href="#shoe" transform="translate(860 860) rotate(18) scale(0.45)" filter="url(#blur)" opacity="0.5"/>')

# logo mark (original): two nested arcs
parts.append('<g transform="translate(540 70) scale(1.6)" fill="none" stroke="#e9e0d4" stroke-linecap="round">'
             '<path d="M-14 8 C-10 -6 6 -12 16 -4" stroke-width="4"/>'
             '<path d="M-6 12 C-2 4 8 2 12 6" stroke-width="3"/></g>')

# tagline
p, _ = place(MONT_MD, "THE ART OF EVERY STEP", 17, cx=W / 2, y=138, tracking=0.55, fill="#d9cfc2")
parts.append(p)

# giant word: cap height stretched to span 190..660
word_size = 330
cap = 0.7 * word_size
sy = (660 - 190) / cap
p, ww = place(BEBAS, "ARDENT", word_size, cx=W / 2, y=660, tracking=0.02, sy=round(sy, 3), fill="url(#word)")
parts.append(p)

# glow + shadow + hero shoe
SX, SY = (W - SW) / 2, 418
parts.append('<ellipse cx="540" cy="640" rx="470" ry="260" fill="url(#glow)"/>')
parts.append('<ellipse cx="540" cy="892" rx="390" ry="30" fill="url(#shadow)"/>')
parts.append(f'<use xlink:href="#shoe" transform="translate({SX} {SY})" filter="url(#dark)"/>')
parts.append(f'<use xlink:href="#shoe" transform="translate({SX} {SY})"/>')

# callout chips
def chip(x, y, lines, dot):
    w, h = 220, 28 + 24 * len(lines)
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#141210" fill-opacity="0.6" stroke="#6e655b" stroke-width="1.2"/>']
    for i, ln in enumerate(lines):
        t, _ = place(MONT_SB, ln, 16, cx=x + w / 2, y=y + 33 + 24 * i, tracking=0.06, fill="#efe7dc")
        g.append(t)
    dx, dy = dot
    g.append(f'<circle cx="{dx}" cy="{dy}" r="10" fill="none" stroke="#efe7dc" stroke-width="1.4" opacity="0.8"/>')
    g.append(f'<circle cx="{dx}" cy="{dy}" r="4" fill="#efe7dc"/>')
    return "".join(g)

parts.append(chip(820, 560, ["PREMIUM AND", "SLEEK DESIGN"], (800, 668)))
parts.append(chip(44, 860, ["EXTREME", "COMFORT"], (250, 830)))

# CTA pill
parts.append('<rect x="452" y="968" width="176" height="50" rx="25" fill="#efe7dc"/>')
p, _ = place(MONT_SB, "SHOP NOW", 18, cx=540, y=999.5, tracking=0.12, fill="#141210")
parts.append(p)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
       f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n<title>ARDENT premium sneaker banner</title>\n'
       + DEFS + "\n" + "\n".join(parts) + "\n</svg>\n")
open(OUT, "w").write(svg)
print("wrote", OUT, len(svg), "bytes")
