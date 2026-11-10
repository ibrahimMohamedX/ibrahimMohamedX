"""Shared visual language for the profile cards (dark, cyan-to-violet, matching the portfolio theme color)."""

BG = "#07060d"
PANEL = "#0d0b18"
BORDER = "#221e3a"
TEXT = "#ece9fb"
MUTED = "#8f8aab"
CYAN = "#22d3ee"
VIOLET = "#8b5cf6"
GREEN = "#34d399"
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def defs(uid):
    return (
        f'<defs>'
        f'<linearGradient id="{uid}g" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
        f'<radialGradient id="{uid}glow" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{VIOLET}" stop-opacity="0.35"/>'
        f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
        f'</defs>'
    )


def card_open(w, h, uid, title=None):
    t = f"<title>{esc(title)}</title>" if title else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">{t}'
        f"{defs(uid)}"
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="16" fill="{PANEL}" stroke="{BORDER}"/>'
        f'<circle cx="{w-30}" cy="30" r="90" fill="url(#{uid}glow)"/>'
        f'<rect x="16" y="0.5" width="{w-32}" height="3" rx="1.5" fill="url(#{uid}g)"/>'
    )
