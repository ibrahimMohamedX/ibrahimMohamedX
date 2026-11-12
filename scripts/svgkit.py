"""Small SVG authoring kit: font embedding, real text measurement, helpers.

Fonts are subset per SVG (only the glyphs that SVG uses) and embedded as
base64 woff2, so every asset is fully self-contained. GitHub renders README
SVGs through <img>, where external fonts/CSS cannot load; data: URIs can.
"""
import base64
import io
import os
from contextlib import contextmanager
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
        self.loop, self.enter, self.exit_ = 12.0, 0.7, 0.6
        self._kfs = {}

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


    # ------------------------------------------------------------ motion
    # Every reveal shares one absolute timeline (self.loop seconds): an element
    # enters at `delay`, holds, and ALL elements leave together at loop-exit.
    # Keyframes are generated per (kind, delay, until) with absolute percentages,
    # so staggering survives every iteration. The un-animated state is "visible".
    KINDS = {
        "up":    ("opacity:0;transform:translateY(18px)", "opacity:0;transform:translateY(-8px)", "50% 50%"),
        "down":  ("opacity:0;transform:translateY(-18px)", "opacity:0;transform:translateY(8px)", "50% 50%"),
        "left":  ("opacity:0;transform:translateX(-30px)", "opacity:0;transform:translateX(-8px)", "50% 50%"),
        "right": ("opacity:0;transform:translateX(30px)", "opacity:0;transform:translateX(8px)", "50% 50%"),
        "pop":   ("opacity:0;transform:scale(.82)", "opacity:0;transform:scale(.94)", "50% 50%"),
        "fade":  ("opacity:0", "opacity:0", "50% 50%"),
        "growx": ("opacity:0;transform:scaleX(0)", "opacity:0;transform:scaleX(1)", "0% 50%"),
        "growy": ("opacity:0;transform:scaleY(0)", "opacity:0;transform:scaleY(1)", "50% 100%"),
        "draw":  ("opacity:1;stroke-dashoffset:1", "opacity:0;stroke-dashoffset:0", "50% 50%"),
    }

    def set_loop(self, loop, enter=0.7, exit_=0.6):
        self.loop, self.enter, self.exit_ = float(loop), enter, exit_

    def _pct(self, t):
        return max(0.0, min(100.0, t / self.loop * 100))

    def _kf(self, kind, delay, until):
        key = (kind, round(delay, 3), None if until is None else round(until, 3))
        if key in self._kfs:
            return self._kfs[key]
        name = f"{self.uid}-{kind}-{len(self._kfs)}"
        a, z, _ = self.KINDS[kind]
        vis = "opacity:1;stroke-dashoffset:0" if kind == "draw" else "opacity:1;transform:none"
        L, e = self.loop, self.enter
        t0 = delay
        t1 = delay + (e * 2.6 if kind == "draw" else e)
        t2 = until if until is not None else L - self.exit_
        t3 = (t2 + self.exit_) if until is not None else L
        ease = "cubic-bezier(.22,.9,.24,1)"
        p0, p1, p2, p3 = (self._pct(t) for t in (t0, t1, t2, t3))
        head = f"0%{{{a};animation-timing-function:{ease}}}" if p0 == 0 else \
               f"0%,{p0:.3f}%{{{a};animation-timing-function:{ease}}}"
        body = (f"{p1:.3f}%{{{vis}}}" if p1 >= p2 else
                f"{p1:.3f}%{{{vis}}}{p2:.3f}%{{{vis};animation-timing-function:ease-in}}")
        tail = f"{p3:.3f}%,100%{{{z}}}" if p3 < 100 else f"100%{{{z}}}"
        self.css.append(f"@keyframes {name}{{{head}{body}{tail}}}")
        self._kfs[key] = name
        return name

    def rv_attrs(self, kind="up", delay=0.0, until=None):
        name = self._kf(kind, delay, until)
        origin = self.KINDS[kind][2]
        extra = f";stroke-dasharray:1" if kind == "draw" else ""
        return (f'class="{self.i("rv")}" style="transform-box:fill-box;transform-origin:{origin}'
                f'{extra};animation:{name} {self.loop:g}s linear infinite"')

    @contextmanager
    def rv(self, kind="up", delay=0.0, until=None):
        self.add(f"<g {self.rv_attrs(kind, delay, until)}>")
        yield
        self.add("</g>")

    def draw(self, d_attr, stroke, width=2, delay=0.0, extra=""):
        self.add(f'<path d="{d_attr}" pathLength="1" fill="none" stroke="{stroke}" stroke-width="{width}" '
                 f'stroke-linecap="round" stroke-linejoin="round" {self.rv_attrs("draw", delay)} {extra}/>')

    def idle(self, name, css_body, dur, delay=0.0, alt=True, ease="ease-in-out", origin=None):
        """Continuous ambient motion. Returns attrs for the element to animate."""
        nm = f"{self.uid}-{name}"
        if not any(c.startswith(f"@keyframes {nm}{{") for c in self.css):
            self.css.append(f"@keyframes {nm}{{{css_body}}}")
        o = f";transform-box:fill-box;transform-origin:{origin or '50% 50%'}"
        return (f'class="{self.i("idle")}" style="animation:{nm} {dur:g}s {ease} {-delay:g}s infinite'
                f'{" alternate" if alt else ""}{o}"')

    def float_(self, dy=7, dur=5.5, delay=0.0):
        return self.idle(f"fl{int(dy)}", f"0%{{transform:translateY(0)}}100%{{transform:translateY({-dy}px)}}", dur, delay)

    def drift(self, dx=26, dy=16, dur=14, delay=0.0):
        return self.idle(f"dr{int(dx)}", f"0%{{transform:translate(0,0)}}100%{{transform:translate({dx}px,{dy}px)}}", dur, delay)

    def shine(self, x, y, w, h, delay=0.0, period=9.0, op=0.075):
        """Soft diagonal light sweep across a surface (clipped by the doc)."""
        gid = self.i("shg")
        if not any(f'id="{gid}"' in x_ for x_ in self.defs):
            self.add_def(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
                         f'<stop offset=".5" stop-color="#fff" stop-opacity="{op}"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
        nm = self.i("shine")
        if not any(c.startswith(f"@keyframes {nm}{{") for c in self.css):
            self.css.append(f"@keyframes {nm}{{0%{{transform:translateX(0)}}36%,100%{{transform:translateX({w + 420:g}px)}}}}")
        self.add(f'<g transform="skewX(-18)" class="{self.i("idle")}"><rect x="{x - 300:g}" y="{y - 10:g}" width="220" height="{h + 20:g}" '
                 f'fill="url(#{gid})" style="animation:{nm} {period:g}s ease-in-out {-delay:g}s infinite"/></g>')

    def cover(self, x, y, w, h, fill, start, dur, steps):
        """Opaque rect that un-covers text left to right in discrete steps (typing)."""
        name = self.i(f"cv{len(self._kfs)}")
        self._kfs[("cv", name)] = name
        p0, p1 = self._pct(start), self._pct(start + dur)
        self.css.append(f"@keyframes {name}{{0%,{p0:.3f}%{{transform:scaleX(1);animation-timing-function:steps({steps},end)}}"
                        f"{p1:.3f}%,99.99%{{transform:scaleX(0)}}100%{{transform:scaleX(1)}}}}")
        self.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}" class="{self.i("rv")}" '
                 f'style="transform-box:fill-box;transform-origin:100% 50%;animation:{name} {self.loop:g}s linear infinite"/>')

    def rich(self, x, y, parts, font="mono400", size=14, extra=""):
        """Single-line text made of coloured runs [(text, fill), ...]."""
        name, weight, _ = T.FONTS[font]
        for t_, _f in parts:
            self.used[font].update(t_)
        spans = "".join(f'<tspan fill="{f}">{esc(t_)}</tspan>' for t_, f in parts)
        self.add(f'<text x="{x:g}" y="{y:g}" font-family="{fam(font)}" font-size="{size:g}" font-weight="{weight}" '
                 f'xml:space="preserve" style="white-space:pre" {extra}>{spans}</text>')

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
        self.css.append(f"@media (prefers-reduced-motion: reduce){{.{self.i('rv')},.{self.i('idle')},.{self.i('idle')} *{{animation:none!important}}}}")
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
