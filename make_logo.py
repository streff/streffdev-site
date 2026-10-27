"""Build the streffdev logo as outlined SVG (no font dependency) plus PNG exports."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from pathlib import Path

FONT = Path(__file__).parent / "fontdl/jbm/fonts/ttf/JetBrainsMono-ExtraBold.ttf"
OUT = Path(__file__).parent / "site/brand"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#1B2230"
THISTLE = "#6B47B8"
WHITE = "#FFFFFF"
THISTLE_ON_DARK = "#A88BF0"

font = TTFont(FONT)
gs = font.getGlyphSet()
cmap = font.getBestCmap()
upm = font["head"].unitsPerEm
xh = font["OS/2"].sxHeight
asc = font["OS/2"].sCapHeight


def text_path(text, scale, x0, baseline):
    pen = SVGPathPen(gs)
    x = x0
    for ch in text:
        g = cmap[ord(ch)]
        tp = TransformPen(pen, (scale, 0, 0, -scale, x, baseline))
        gs[g].draw(tp)
        x += gs[g].width * scale
    return pen.getCommands(), x


def wordmark(fg, accent, name):
    scale = 0.1  # 1000 upm -> 100px font size
    pad = 4
    top = asc * scale  # cap height in px; ascender letters ~ cap height
    baseline = pad + top + 6
    d, xend = text_path("streffdev", scale, pad, baseline)
    gap = 10
    cw = 34
    ch = xh * scale
    width = xend + gap + cw + pad
    height = baseline + pad + 2
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.1f} {height:.1f}" role="img" aria-label="streffdev">
  <title>streffdev</title>
  <path fill="{fg}" d="{d}"/>
  <rect fill="{accent}" x="{xend + gap:.1f}" y="{baseline - ch:.1f}" width="{cw}" height="{ch:.1f}" rx="3"/>
</svg>
'''
    (OUT / name).write_text(svg)


def icon(name, bg=INK, fg=WHITE, accent=THISTLE_ON_DARK, size=512):
    # "s" plus block cursor in a rounded square
    scale = 0.38
    gw = gs[cmap[ord("s")]].width * scale
    cw = 124
    gap = 20
    total = gw + gap + cw
    x0 = (size - total) / 2 + 6
    chh = xh * scale
    baseline = size / 2 + chh / 2
    d, xend = text_path("s", scale, x0, baseline)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" role="img" aria-label="streffdev">
  <title>streffdev</title>
  <rect width="{size}" height="{size}" rx="{size*0.22:.0f}" fill="{bg}"/>
  <path fill="{fg}" d="{d}"/>
  <rect fill="{accent}" x="{xend + gap:.1f}" y="{baseline - chh:.1f}" width="{cw}" height="{chh:.1f}" rx="8"/>
</svg>
'''
    (OUT / name).write_text(svg)


wordmark(INK, THISTLE, "streffdev-logo.svg")
wordmark(WHITE, THISTLE_ON_DARK, "streffdev-logo-on-dark.svg")
icon("streffdev-icon.svg")
print("ok", xh, asc, upm)
