"""Design tokens for the profile card system.

Single source of truth for every visual value in the generated SVGs:
color ramps, typography scale, spacing, radii and the text-width estimator.
Generators import this module; no raw visual values live in component code.

Legacy names (BG, PANEL, BORDER, TEXT, MUTED, CYAN, VIOLET, GREEN, SANS,
MONO, esc, defs, card_open) are kept working for generate_stats.py.
"""

# ------------------------------------------------- primitives: neutral ramp
N900 = "#07060d"  # page field (banner background)
N800 = "#0d0b18"  # card surface
N700 = "#131022"  # raised surface: chips, tracks, pills
N650 = "#191531"  # inner fills on raised surfaces
BORDER = "#262149"  # hairline strokes
BORDER_SOFT = "#1d1936"  # dividers, secondary strokes

# ---------------------------------------------------------- primitives: ink
TEXT = "#ece9fb"  # primary text  (16.3:1 on N800)
BODY = "#c9c4e4"  # body/secondary text (11.9:1)
MUTED = "#9d97bf"  # captions, labels (7.0:1)
SUBTLE = "#6f6a92"  # decorative glyphs only - never for text under 18px

# -------------------------------------------------------- primitives: brand
CYAN = "#22d3ee"  # accents, overlines, data highlights (10.8:1)
CYAN_DIM = "#1993ab"  # strokes and glow edges
VIOLET = "#8b5cf6"  # gradient end, graphic fills only (4.6:1 - large/graphic)
VIOLET_BRIGHT = "#a78bfa"  # violet as small text (7.2:1)
GREEN = "#34d399"  # availability / shipped status
AMBER = "#fbbf24"  # in-development status

# legacy aliases
BG = N900
PANEL = N800

# ---------------------------------------------------------------- fonts
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
ARABIC = "'Segoe UI', 'Noto Sans Arabic', Tahoma, Arial, sans-serif"
MONO = "SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"

# --------------------------------------------------------- typography scale
# size, weight, letter-spacing(px), line-height(px), family, color-role
T_DISPLAY = dict(size=54, weight=800, ls=0.5, lh=58, family=SANS, fill="gradient")
T_TITLE = dict(size=22, weight=700, ls=-0.2, lh=28, family=SANS, fill=TEXT)
T_ENTRY = dict(size=15, weight=600, ls=0, lh=20, family=SANS, fill=TEXT)
T_BODY = dict(size=13.5, weight=400, ls=0, lh=19.5, family=SANS, fill=BODY)
T_SMALL = dict(size=12.5, weight=400, ls=0, lh=17, family=SANS, fill=BODY)
T_CAPTION = dict(size=11, weight=400, ls=0, lh=15, family=SANS, fill=MUTED)
T_OVERLINE = dict(size=11, weight=400, ls=2.2, lh=15, family=MONO, fill=CYAN)
T_DATA = dict(size=14.5, weight=700, ls=0, lh=20, family=MONO, fill=TEXT)
T_CHIP = dict(size=11.5, weight=400, ls=0, lh=16, family=MONO, fill=BODY)
T_ARABIC = dict(size=17, weight=400, ls=0, lh=26, family=ARABIC, fill=BODY)

# --------------------------------------------------------------- space (4/8)
S1, S2, S3, S4, S5, S6, S7 = 4, 8, 12, 16, 24, 32, 48
PAD_CARD = 26  # inner padding of standard cards
PAD_BANNER_X = 56

# ------------------------------------------------------------------- shape
RADIUS_BANNER = 20
RADIUS_CARD = 14

# ------------------------------------------------------------ status system
# every state pairs a color with a text label - meaning never rides on color
STATUS = {
    "shipped": (GREEN, "shipped"),
    "building": (AMBER, "in development"),
    "live": (CYAN, "live"),
    "info": (MUTED, "info"),
}

# --------------------------------------------- approximate text measurement
_SANS_W = {
    " ": 0.30, "!": 0.30, '"': 0.36, "#": 0.56, "$": 0.55, "%": 0.88, "&": 0.68,
    "'": 0.20, "(": 0.35, ")": 0.35, "*": 0.40, "+": 0.55, ",": 0.27, "-": 0.36,
    ".": 0.27, "/": 0.40, ":": 0.30, ";": 0.30, "<": 0.55, "=": 0.55, ">": 0.55,
    "?": 0.48, "@": 0.80, "[": 0.35, "\\": 0.40, "]": 0.35, "^": 0.50,
    "_": 0.50, "`": 0.33, "{": 0.36, "|": 0.26, "}": 0.36, "~": 0.55,
    "·": 0.30, "—": 1.0, "–": 0.60,
    "a": 0.52, "b": 0.54, "c": 0.47, "d": 0.54, "e": 0.51, "f": 0.34,
    "g": 0.54, "h": 0.54, "i": 0.25, "j": 0.26, "k": 0.50, "l": 0.25,
    "m": 0.84, "n": 0.55, "o": 0.54, "p": 0.54, "q": 0.54, "r": 0.38,
    "s": 0.44, "t": 0.36, "u": 0.55, "v": 0.49, "w": 0.72, "x": 0.47,
    "y": 0.49, "z": 0.44,
    "A": 0.62, "B": 0.58, "C": 0.58, "D": 0.62, "E": 0.52, "F": 0.50,
    "G": 0.66, "H": 0.64, "I": 0.30, "J": 0.44, "K": 0.60, "L": 0.50,
    "M": 0.86, "N": 0.68, "O": 0.68, "P": 0.54, "Q": 0.68, "R": 0.56,
    "S": 0.52, "T": 0.54, "U": 0.64, "V": 0.60, "W": 0.88, "X": 0.58,
    "Y": 0.56, "Z": 0.54,
}
_DIGIT_W = 0.55


def text_w(s, size, mono=False, bold=False):
    """Estimated rendered width of *s* in px. Mono fonts are fixed-advance."""
    if mono:
        w = len(str(s)) * 0.55 * size
    else:
        w = sum(
            _DIGIT_W if c.isdigit() else _SANS_W.get(c, 0.54)
            for c in str(s)
        ) * size
    return w * (1.045 if bold else 1.0)


# ------------------------------------------------------------------ helpers
def esc(s):
    return (
        str(s)
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
    )


def defs(uid):
    """Shared gradients: linear cyan-violet (identity) + soft violet glow."""
    return (
        "<defs>"
        f'<linearGradient id="{uid}g" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
        f'<radialGradient id="{uid}glow" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{VIOLET}" stop-opacity="0.30"/>'
        f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
        "</defs>"
    )


def top_edge(w, uid, x=16):
    """The signature gradient hairline along a card's top edge."""
    return f'<rect x="{x}" y="0.5" width="{w - 2 * x}" height="2.5" rx="1.25" fill="url(#{uid}g)"/>'


def text_el(x, y, s, t, fill=None, anchor=None, opacity=None):
    """A <text> element fully driven by a type token."""
    attrs = f'x="{x}" y="{y}" font-family="{t["family"]}" font-size="{t["size"]}"'
    if t.get("weight"):
        attrs += f' font-weight="{t["weight"]}"'
    if t.get("ls"):
        attrs += f' letter-spacing="{t["ls"]}"'
    if anchor:
        attrs += f' text-anchor="{anchor}"'
    if opacity is not None:
        attrs += f' opacity="{opacity}"'
    fill = fill if fill is not None else t["fill"]
    if fill != "gradient":
        attrs += f' fill="{fill}"'
    return f"<text {attrs}>{esc(s)}</text>"


def card_open(w, h, uid, title=None, rx=RADIUS_CARD):
    """Standard card shell: surface, hairline, glow, gradient top edge."""
    t = f"<title>{esc(title)}</title>" if title else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">{t}'
        f"{defs(uid)}"
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="{N800}" stroke="{BORDER}"/>'
        f'<circle cx="{w - 20}" cy="14" r="110" fill="url(#{uid}glow)"/>'
        f"{top_edge(w, uid)}"
    )


def overline(x, y, s, uid=None, fill=None):
    """Mono section label, e.g. '// TECH STACK'."""
    return text_el(x, y, s, T_OVERLINE, fill=fill or CYAN)


def pill(x, y, label, color, h=22, mono=True):
    """Status pill: colored dot + text label. Returns (svg, total_width)."""
    t = T_CHIP if mono else T_SMALL
    dot_r = 3
    text_x = x + 14 + 2 * dot_r + 1
    w = (text_x - x) + text_w(label, t["size"], mono) + 12
    svg = (
        f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{N700}" stroke="{BORDER}"/>'
        f'<circle cx="{x + 12 + dot_r:.1f}" cy="{y + h / 2}" r="{dot_r}" fill="{color}"/>'
        + text_el(text_x, y + h / 2 + t["size"] * 0.35, label, t)
    )
    return svg, w


def chip(x, y, label, h=26, size=12.5, mono=False, dot=True, uid=None):
    """Tech chip with measured width. Returns (svg, total_width)."""
    pad_x = 11 if dot else 12
    dot_w = (2 * 3 + 7) if dot else 0
    w = pad_x + dot_w + text_w(label, size, mono) + pad_x
    svg = f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{N700}" stroke="{BORDER}"/>'
    if dot:
        fill = f"url(#{uid}g)" if uid else CYAN
        svg += f'<circle cx="{x + pad_x + 3:.1f}" cy="{y + h / 2}" r="3" fill="{fill}"/>'
    tx = x + pad_x + dot_w
    svg += text_el(tx, y + h / 2 + size * 0.35, label, dict(T_SMALL, size=size, family=MONO if mono else SANS))
    return svg, w
