"""Generate a 1200x628 premium sneaker banner as SVG with all text converted to outlines."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont

FONTS = sys.argv[1]
OUT = sys.argv[2]
W, H = 1200, 628

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
SHOE = """
<g id="shoe">
  <!-- upper -->
  <path d="M42 162 C30 124 42 86 66 60 C78 46 88 24 104 13 C117 5 131 9 136 22 C141 36 152 45 176 50
           C226 58 290 80 340 106 C400 132 470 136 530 146 C576 153 600 172 600 196
           C540 205 300 190 60 190 Z" fill="url(#upper)"/>
  <!-- knit texture -->
  <g clip-path="url(#upperClip)" opacity="0.18" stroke="#8a7d6d" stroke-width="1.1" fill="none">
    <path d="M40 40 H600 M40 52 H600 M40 64 H600 M40 76 H600 M40 88 H600 M40 100 H600 M40 112 H600 M40 124 H600 M40 136 H600 M40 148 H600 M40 160 H600 M40 172 H600 M40 184 H600" stroke-dasharray="3 3"/>
  </g>
  <!-- sock collar opening -->
  <path d="M104 14 C115 8 128 11 133 22 C126 30 112 32 101 26 C99 21 100 17 104 14 Z" fill="#3a332c"/>
  <!-- heel counter -->
  <path d="M42 162 C31 126 42 92 62 68 C74 84 86 112 92 150 Z" fill="url(#counter)"/>
  <path d="M60 104 C66 112 70 124 72 138" stroke="#f6efe6" stroke-width="2" fill="none" opacity="0.5"/>
  <!-- heel pull tab -->
  <path d="M66 60 C60 50 62 36 72 26 L80 30 C74 40 74 50 78 58 Z" fill="#c9bcab"/>
  <!-- toe cap -->
  <path d="M488 140 C548 146 600 166 600 196 C562 192 524 188 492 184 C480 172 478 152 488 140 Z" fill="url(#toe)"/>
  <g clip-path="url(#upperClip)">
  <!-- brand waves (original mark) -->
  <path d="M150 156 C222 146 284 116 334 88 L350 99 C302 128 244 156 186 166 Z" fill="#f7f1e8"/>
  <path d="M196 166 C262 158 326 132 372 104 L384 113 C340 140 282 164 230 172 Z" fill="#e3d8ca"/>
  <path d="M150 156 C222 146 284 116 334 88" stroke="#ffffff" stroke-width="1.5" fill="none" opacity="0.7"/>
  <!-- eyestay + laces -->
  <path d="M178 52 C222 62 262 80 296 104 C312 116 330 124 352 130" stroke="#d6cab9" stroke-width="10" fill="none" stroke-linecap="round"/>
  <g stroke="#fbf7f1" stroke-width="5" stroke-linecap="round">
    <path d="M190 48 L206 66"/><path d="M212 54 L226 74"/><path d="M234 63 L246 84"/>
    <path d="M256 75 L266 96"/><path d="M278 89 L286 110"/><path d="M300 104 L306 122"/>
  </g>
  </g>
  <!-- top highlight -->
  <path d="M138 26 C150 42 168 48 190 52 C230 60 262 78 290 100" stroke="#ffffff" stroke-width="2.5" fill="none" opacity="0.55"/>
  <!-- midsole -->
  <path d="M24 182 C22 160 60 154 110 158 L470 178 C540 182 592 188 600 206 C603 218 590 228 565 229
           L62 231 C32 231 21 218 24 182 Z" fill="url(#mid)"/>
  <path d="M32 174 C60 160 100 160 140 162 L470 182 C530 186 575 192 594 204" stroke="#ffffff" stroke-width="2" fill="none" opacity="0.6"/>
  <!-- air windows -->
  <rect x="66" y="192" width="112" height="24" rx="12" fill="url(#iri)"/>
  <rect x="210" y="196" width="66" height="21" rx="10.5" fill="url(#iri)" opacity="0.9"/>
  <rect x="304" y="198" width="96" height="21" rx="10.5" fill="url(#iri)"/>
  <rect x="430" y="200" width="76" height="20" rx="10" fill="url(#iri)" opacity="0.95"/>
  <g fill="#ffffff" opacity="0.75">
    <rect x="76" y="196" width="56" height="5" rx="2.5"/><rect x="314" y="202" width="44" height="4" rx="2"/>
    <rect x="440" y="204" width="34" height="4" rx="2"/><rect x="218" y="200" width="30" height="4" rx="2"/>
  </g>
  <!-- outsole -->
  <path d="M30 224 L570 226 C590 226 598 233 591 241 C581 249 560 251 540 251 L72 251 C42 251 26 241 30 224 Z" fill="url(#outsole)"/>
</g>"""

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
  <clipPath id="upperClip">
    <path d="M42 162 C30 124 42 86 66 60 C78 46 88 24 104 13 C117 5 131 9 136 22 C141 36 152 45 176 50
             C226 58 290 80 340 106 C400 132 470 136 530 146 C576 153 600 172 600 196 C540 205 300 190 60 190 Z"/>
  </clipPath>
  <filter id="dark" x="-20%" y="-30%" width="140%" height="160%"><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.75 0"/><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/></filter>
  {SHOE}
</defs>"""

parts = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']

# blurred corner shoes
parts.append('<use xlink:href="#shoe" transform="translate(-150 -40) rotate(-18) scale(0.55)" filter="url(#blur)" opacity="0.55"/>')
parts.append('<use xlink:href="#shoe" transform="translate(1010 520) rotate(16) scale(0.5)" filter="url(#blur)" opacity="0.5"/>')

# logo mark (original): two nested arcs
parts.append('<g transform="translate(600 40)" fill="none" stroke="#e9e0d4" stroke-linecap="round">'
             '<path d="M-14 8 C-10 -6 6 -12 16 -4" stroke-width="4"/>'
             '<path d="M-6 12 C-2 4 8 2 12 6" stroke-width="3"/></g>')

# tagline
p, _ = place(MONT_MD, "THE ART OF EVERY STEP", 13, cx=W / 2, y=82, tracking=0.55, fill="#d9cfc2")
parts.append(p)

# giant word
word_size = 300
cap = 0.7 * word_size
sy = (470 - 108) / cap
p, ww = place(BEBAS, "ARDENT", word_size, cx=W / 2, y=470, tracking=0.02, sy=round(sy, 3), fill="url(#word)")
parts.append(p)

# glow + shadow + hero shoe
parts.append('<ellipse cx="600" cy="400" rx="380" ry="170" fill="url(#glow)"/>')
parts.append('<ellipse cx="600" cy="545" rx="330" ry="26" fill="url(#shadow)"/>')
parts.append('<use xlink:href="#shoe" transform="translate(290 282) scale(1.04)" filter="url(#dark)"/>')
parts.append('<use xlink:href="#shoe" transform="translate(290 282) scale(1.04)"/>')

# callout chips
def chip(x, y, lines, dot):
    w, h = 190, 22 + 20 * len(lines)
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#141210" fill-opacity="0.6" stroke="#6e655b" stroke-width="1"/>']
    for i, ln in enumerate(lines):
        t, _ = place(MONT_SB, ln, 13, cx=x + w / 2, y=y + 27 + 20 * i, tracking=0.06, fill="#efe7dc")
        g.append(t)
    dx, dy = dot
    g.append(f'<circle cx="{dx}" cy="{dy}" r="8" fill="none" stroke="#efe7dc" stroke-width="1.2" opacity="0.8"/>')
    g.append(f'<circle cx="{dx}" cy="{dy}" r="3.2" fill="#efe7dc"/>')
    return "".join(g)

parts.append(chip(960, 300, ["PREMIUM AND", "SLEEK DESIGN"], (944, 378)))
parts.append(chip(52, 458, ["EXTREME", "COMFORT"], (262, 444)))

# CTA pill
parts.append('<rect x="526" y="568" width="148" height="40" rx="20" fill="#efe7dc"/>')
p, _ = place(MONT_SB, "SHOP NOW", 14, cx=600, y=593, tracking=0.12, fill="#141210")
parts.append(p)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
       f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n<title>ARDENT premium sneaker banner</title>\n'
       + DEFS + "\n" + "\n".join(parts) + "\n</svg>\n")
open(OUT, "w").write(svg)
print("wrote", OUT, len(svg), "bytes")
