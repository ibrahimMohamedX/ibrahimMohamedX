"""Design tokens for the profile asset system.

Every colour, size and radius used by the generated SVGs lives here.
To re-skin the whole profile, change this file and run `python scripts/build_assets.py`.

Identity notes
- Field colour #0b0b0c is the theme-color published by himego.vercel.app.
- Cyan -> violet is the brand gradient already used across the previous profile.
- Type: IBM Plex Sans (Latin) + IBM Plex Sans Arabic, both open-licensed (OFL).
  IBM Plex Mono is used only where the content is literally a printed receipt.
"""

# ---------------------------------------------------------------- surfaces
BG = "#0b0b0c"        # field (matches the portfolio's theme-color)
SURFACE = "#111113"   # cards
RAISED = "#18181b"    # elements sitting on a card
RAISED_2 = "#202024"  # hover-level fills, tracks
LINE = "#26262b"      # strokes
LINE_SOFT = "#1b1b1f" # dividers

# --------------------------------------------------------------------- ink
INK = "#f4f4f6"       # primary text   (17.7:1 on SURFACE)
BODY = "#b8b8c4"      # secondary text (10.2:1)
MUTED = "#8a8a98"     # captions       (5.5:1)
FAINT = "#5c5c68"     # decoration only, never text

# ------------------------------------------------------------------- brand
CYAN = "#22d3ee"
VIOLET = "#8b5cf6"
VIOLET_L = "#a78bfa"
GREEN = "#34d399"
AMBER = "#fbbf24"
CORAL = "#fb7185"
SKY = "#60a5fa"

# paper (receipt) colours
PAPER = "#f3f1ea"
PAPER_INK = "#1c1b1f"
PAPER_MUTED = "#6d6a74"

# ------------------------------------------------------------------- fonts
FONT_DIR = "fonts"

# key -> (css family, weight, file)
FONTS = {
    "sans400": ("Plex Sans", 400, "ibm-plex-sans-latin-400-normal.woff2"),
    "sans500": ("Plex Sans", 500, "ibm-plex-sans-latin-500-normal.woff2"),
    "sans600": ("Plex Sans", 600, "ibm-plex-sans-latin-600-normal.woff2"),
    "sans700": ("Plex Sans", 700, "ibm-plex-sans-latin-700-normal.woff2"),
    "mono400": ("Plex Mono", 400, "ibm-plex-mono-latin-400-normal.woff2"),
    "mono500": ("Plex Mono", 500, "ibm-plex-mono-latin-500-normal.woff2"),
    "ar400": ("Plex Arabic", 400, "ibm-plex-sans-arabic-arabic-400-normal.woff2"),
    "ar500": ("Plex Arabic", 500, "ibm-plex-sans-arabic-arabic-500-normal.woff2"),
    "ar600": ("Plex Arabic", 600, "ibm-plex-sans-arabic-arabic-600-normal.woff2"),
}

FALLBACK = {
    "Plex Sans": "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif",
    "Plex Mono": "SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace",
    "Plex Arabic": "'Segoe UI', 'Noto Sans Arabic', Tahoma, Arial, sans-serif",
}

# ------------------------------------------------------------------- shape
R_HERO = 28
R_CARD = 24
R_INNER = 12
R_TAG = 999

W = 1200  # every asset is authored at 1200 units wide; halves are 588
W_HALF = 588
W_SM = 600   # compact (phone) variants are authored at 600 wide
GAP = 24
