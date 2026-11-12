"""Small SVG authoring kit: font embedding, real text measurement, helpers.

Fonts are subset per SVG (only the glyphs that SVG uses) and embedded as
base64 woff2, so every asset is fully self-contained. GitHub renders README
SVGs through <img>, where external fonts/CSS cannot load; data: URIs can.
"""
import base64
import io
import os
from collections import defaultdict
from functools import lru_cache

from fontTools import subset
from fontTools.ttLib import TTFont

import tokens as T

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(HERE, T.FONT_DIR)


# ------------------------------------------------------------------ fonts
@lru_cache(maxsize=None)
def _font(key):
    return TTFont(os.path.join(FONT_PATH, T.FONTS[key][2]))


@lru_cache(maxsize=None)
def _metrics(key):
    f = _font(key)
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upm = f["head"].unitsPerEm
    return cmap, hmtx, upm


def measure(s, key, size, ls=0.0):
    """Advance width of *s* in px (no kerning; good to ~1-2%)."""
    cmap, hmtx, upm = _metrics(key)
    w = 0
    for ch in s:
        g = cmap.get(ord(ch))
        w += hmtx[g][0] if g else upm * 0.5
    return w / upm * size + ls * len(s)


def wrap(s, key, size, max_w, ls=0.0):
    lines, cur = [], ""
    for word in s.split():
        cand = (cur + " " + word).strip()
        if measure(cand, key, size, ls) > max_w and cur:
            lines.append(cur)
            cur = word
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def _subset_b64(key, chars):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.notdef_outline = True
    opts.name_IDs = [1, 2]
    opts.hinting = False
    font = TTFont(os.path.join(FONT_PATH, T.FONTS[key][2]))
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(chars)))
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def fam(key):
    name = T.FONTS[key][0]
    return f"'{name}', {T.FALLBACK[name]}"


# -------------------------------------------------------------------- doc
class Doc:
    """One SVG document. All class/keyframe/id names are prefixed with uid so
    several docs can be inlined in one HTML page without CSS collisions."""

    def __init__(self, uid, w, h, title, desc=None, bg=None, radius=None, border=True, pad_l=0, pad_r=0):
        self.uid, self.w, self.h = uid, w, h
        self.title, self.desc = title, desc
        self.defs, self.css, self.body = [], [], []
        self.used = defaultdict(set)
        self.bg, self.radius, self.border = bg, radius, border
        self.pad_l, self.pad_r = pad_l, pad_r

    # ids / classes
    def i(self, name):
        return f"{self.uid}-{name}"

    def add(self, s):
        self.body.append(s)

    def add_def(self, s):
        self.defs.append(s)

    def add_css(self, s):
        self.css.append(s)

    def text(self, x, y, s, font="sans400", size=18, fill=T.INK, anchor=None,
             ls=None, cls=None, opacity=None, rtl=False, extra=""):
        self.used[font].update(s)
        name, weight, _ = T.FONTS[font]
        a = f'x="{x:g}" y="{y:g}" font-family="{fam(font)}" font-size="{size:g}" font-weight="{weight}" fill="{fill}"'
        if anchor:
            a += f' text-anchor="{anchor}"'
        if ls:
            a += f' letter-spacing="{ls:g}"'
        if opacity is not None:
            a += f' opacity="{opacity:g}"'
        if rtl:
            a += ' direction="rtl" unicode-bidi="embed"'
        if cls:
            a += f' class="{self.i(cls)}"'
        return self.add(f"<text {a} {extra}>{esc(s)}</text>")

    def gradient(self, name, x1=0, y1=0, x2=1, y2=0, stops=None, units=None):
        stops = stops or [(0, T.CYAN), (1, T.VIOLET)]
        u = f' gradientUnits="{units}"' if units else ""
        s = "".join(f'<stop offset="{o:g}" stop-color="{c}"/>' for o, c in stops)
        self.add_def(f'<linearGradient id="{self.i(name)}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{u}>{s}</linearGradient>')
        return f"url(#{self.i(name)})"

    def glow(self, name, color, op=0.35):
        self.add_def(
            f'<radialGradient id="{self.i(name)}" cx="0.5" cy="0.5" r="0.5">'
            f'<stop offset="0" stop-color="{color}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')
        return f"url(#{self.i(name)})"

    def reduced_motion(self, css):
        """CSS that applies when the viewer prefers reduced motion."""
        self.css.append(f"@media (prefers-reduced-motion: reduce){{{css}}}")

    def render(self):
        faces = []
        for key, chars in self.used.items():
            name, weight, _ = T.FONTS[key]
            b64 = _subset_b64(key, chars | set(" "))
            faces.append(
                f"@font-face{{font-family:'{name}';font-weight:{weight};font-style:normal;"
                f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
        r = self.radius if self.radius is not None else T.R_CARD
        clip = f'<clipPath id="{self.i("clip")}"><rect width="{self.w}" height="{self.h}" rx="{r}"/></clipPath>'
        bg = ""
        if self.bg:
            bg = f'<rect width="{self.w}" height="{self.h}" rx="{r}" fill="{self.bg}"/>'
        border = ""
        if self.border:
            border = (f'<rect x="0.5" y="0.5" width="{self.w - 1}" height="{self.h - 1}" rx="{r}" '
                      f'fill="none" stroke="{T.LINE}"/>')
        desc = f"<desc>{esc(self.desc)}</desc>" if self.desc else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w + self.pad_l + self.pad_r}" height="{self.h}" '
            f'viewBox="{-self.pad_l} 0 {self.w + self.pad_l + self.pad_r} {self.h}" role="img" aria-label="{esc(self.title)}">'
            f"<title>{esc(self.title)}</title>{desc}"
            f"<defs>{clip}{''.join(self.defs)}</defs>"
            f"<style>{''.join(faces)}{''.join(self.css)}</style>"
            f'<g clip-path="url(#{self.i("clip")})">{bg}{"".join(self.body)}</g>{border}</svg>'
        )


# ---------------------------------------------------------------- helpers
def tag(doc, x, y, label, color=None, h=30, size=15, font="sans500", filled=True):
    """Rounded tag. Returns its width."""
    w = measure(label, font, size) + 24
    color = color or T.BODY
    fill = f'fill="{T.RAISED}"' if filled else 'fill="none"'
    doc.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h}" rx="{h / 2}" {fill} stroke="{T.LINE}"/>')
    doc.text(x + 12, y + h / 2 + size * 0.35, label, font, size, color)
    return w


def status(doc, x, y, label, color, pulse=False, size=16):
    """Dot + word. Meaning never rides on colour alone."""
    cls = f' class="{doc.i("pulse")}"' if pulse else ""
    doc.add(f'<circle cx="{x + 5:g}" cy="{y - 5:g}" r="4.5" fill="{color}"{cls}/>')
    doc.text(x + 18, y, label, "sans500", size, T.BODY)
    return 18 + measure(label, "sans500", size)


def pulse_css(doc):
    doc.add_css(
        f".{doc.i('pulse')}{{transform-box:fill-box;transform-origin:center;animation:{doc.i('pulse')} 2.2s ease-in-out infinite}}"
        f"@keyframes {doc.i('pulse')}{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.4;transform:scale(1.7)}}}}")


def save(path, svg):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    return len(svg.encode())
