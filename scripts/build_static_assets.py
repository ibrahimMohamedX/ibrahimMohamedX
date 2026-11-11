#!/usr/bin/env python3
"""Build the static SVG assets: banner, tech stack, featured-project cards
and the experience timeline.

The banner uses the original hero design. All other cards use the tokenised
design system from card_style. Run:
    python scripts/build_static_assets.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from card_style import (  # noqa: E402
    BORDER, BORDER_SOFT, BG, CYAN, CYAN_DIM, GREEN, MONO, MUTED, N800, N900,
    PANEL, PAD_CARD, SANS, STATUS, SUBTLE, T_BODY, T_CHIP, T_ENTRY, T_TITLE,
    VIOLET, VIOLET_BRIGHT, card_open, chip, defs, esc, overline,
    pill, text_el, text_w, top_edge,
)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)


def save(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(text)


# ------------------------------------------------------------------ banner (original hero design)
def banner():
    W, H = 1200, 340
    roles = ["Software Engineer", "Flutter Mobile & Desktop Developer", "Founder · Archai Solutions"]
    role_svg = ""
    for i, r in enumerate(roles):
        role_svg += (
            f'<text class="role r{i}" x="70" y="228" font-family="{SANS}" font-size="27" fill="#d7d3ee">{esc(r)}</text>'
        )
    # circuit traces on the right (a nod to the Archai identity)
    traces = [
        "M 905 170 H 840 V 120 H 780", "M 905 190 H 820 V 235 H 760", "M 905 150 V 90 H 960 V 50",
        "M 1015 170 H 1075 V 120 H 1140", "M 1015 190 H 1090 V 245 H 1150", "M 985 105 V 60 H 1040",
    ]
    trace_svg = "".join(f'<path d="{d}" class="trace" fill="none" stroke="url(#bg)" stroke-width="2" stroke-linecap="round"/>' for d in traces)
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="4" fill="{CYAN}"/>'
        for x, y in [(780, 120), (760, 235), (960, 50), (1140, 120), (1150, 245), (1040, 60)]
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">
<title>Ibrahim Mohamed — Software Engineer, Flutter Mobile and Desktop Developer</title>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
  <linearGradient id="bgv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
  <radialGradient id="vg" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0.45"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <radialGradient id="cg" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{CYAN}" stop-opacity="0.28"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 H 0 V 40" fill="none" stroke="#ffffff" stroke-opacity="0.045"/></pattern>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<style>
  .blob1 {{ animation: f1 9s ease-in-out infinite alternate; }}
  .blob2 {{ animation: f2 11s ease-in-out infinite alternate; }}
  @keyframes f1 {{ from {{ transform: translate(0,0); }} to {{ transform: translate(-40px,30px); }} }}
  @keyframes f2 {{ from {{ transform: translate(0,0); }} to {{ transform: translate(50px,-30px); }} }}
  .role {{ opacity: 0; animation: cycle 9s infinite; }}
  .r0 {{ animation-delay: 0s; }} .r1 {{ animation-delay: 3s; }} .r2 {{ animation-delay: 6s; }}
  @keyframes cycle {{ 0% {{ opacity: 0; transform: translateY(8px); }} 6% {{ opacity: 1; transform: translateY(0); }} 30% {{ opacity: 1; }} 36% {{ opacity: 0; transform: translateY(-8px); }} 100% {{ opacity: 0; }} }}
  .trace {{ stroke-dasharray: 6 10; animation: flow 2.4s linear infinite; opacity: .85; }}
  @keyframes flow {{ to {{ stroke-dashoffset: -64; }} }}
  .pulse {{ animation: pulse 2s ease-in-out infinite; transform-origin: center; transform-box: fill-box; }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: .45; transform: scale(1.5); }} }}
  .chip {{ animation: chip 4s ease-in-out infinite alternate; }}
  @keyframes chip {{ from {{ opacity: .75; }} to {{ opacity: 1; }} }}
</style>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <circle class="blob1" cx="1010" cy="60" r="260" fill="url(#vg)"/>
  <circle class="blob2" cx="140" cy="330" r="240" fill="url(#cg)"/>
  {trace_svg}
  {dots}
  <g class="chip">
    <rect x="905" y="125" width="110" height="90" rx="16" fill="{PANEL}" stroke="url(#bgv)" stroke-width="2.5"/>
    <rect x="921" y="141" width="78" height="58" rx="8" fill="none" stroke="{VIOLET}" stroke-opacity="0.5"/>
    <text x="960" y="180" text-anchor="middle" font-family="{MONO}" font-size="30" font-weight="700" fill="url(#bg)">&lt;/&gt;</text>
  </g>
  <text x="70" y="92" font-family="{MONO}" font-size="14" fill="{CYAN}" letter-spacing="3">// HELLO, WORLD — I'M</text>
  <text x="68" y="170" font-family="{SANS}" font-size="68" font-weight="800" fill="url(#bg)" letter-spacing="1">IBRAHIM MOHAMED</text>
  {role_svg}
  <text x="70" y="268" font-family="'Segoe UI', 'Noto Sans Arabic', Tahoma, Arial, sans-serif" font-size="19" fill="{MUTED}">مهندس برمجيات · مطوّر تطبيقات الموبايل والديسكتوب</text>
  <g>
    <rect x="70" y="288" width="214" height="32" rx="16" fill="#0f0d1c" stroke="{GREEN}" stroke-opacity="0.45"/>
    <circle class="pulse" cx="92" cy="304" r="5" fill="{GREEN}"/>
    <text x="106" y="309" font-family="{MONO}" font-size="13" fill="#d7d3ee">Open to remote roles</text>
    <rect x="296" y="288" width="104" height="32" rx="16" fill="#0f0d1c" stroke="{BORDER}"/>
    <text x="348" y="309" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#d7d3ee">Egypt</text>
  </g>
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="{BORDER}"/>
</svg>"""


# ---------------------------------------------------------------- tech stack
STACK = [
    ("MOBILE & DESKTOP", ["Flutter", "Dart", "Cubit / BLoC", "Clean Architecture", "MVVM", "GoRouter", "Windows Desktop"]),
    ("NETWORKING & DATA", ["REST APIs", "Dio", "Firebase Auth", "Cloud Firestore", "FCM", "Hive", "Freezed", "build_runner"]),
    ("WEB & BACKEND", ["React", "TypeScript", "JavaScript", "HTML", "CSS", "Vite", "Supabase"]),
    ("BUSINESS SYSTEMS", ["POS / ERP", "Payment workflows", "Role-based access", "Bluetooth · USB · Network printing"]),
    ("TOOLS", ["Git", "GitHub", "GitLab", "Figma", "VS Code", "Claude Code"]),
]

W_ST = 1012


def stack():
    uid = "st"
    pad = 32
    label_w = 186
    x0, right = pad, W_ST - pad
    chip_x0 = pad + label_w
    n_items = sum(len(items) for _, items in STACK)

    parts = []
    y = 76
    last = len(STACK) - 1
    for i, (label, items) in enumerate(STACK):
        parts.append(overline(x0, y + 17, label))
        x, row_y = chip_x0, y
        for it in items:
            s, w = chip(x, row_y, it, h=26, size=12.5, uid=uid)
            if x + w > right:
                x, row_y = chip_x0, row_y + 36
                s, w = chip(x, row_y, it, h=26, size=12.5, uid=uid)
            parts.append(s)
            x += w + 8
        bottom = row_y + 26
        if i < last:
            div = bottom + 16
            parts.append(f'<line x1="{x0}" y1="{div}" x2="{right}" y2="{div}" stroke="{BORDER_SOFT}"/>')
            y = div + 24
        else:
            y = bottom
    H = y + 24
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_ST}" height="{H}" viewBox="0 0 {W_ST} {H}" role="img">'
        f"<title>Tech stack</title>{defs(uid)}"
        f'<rect x="0.5" y="0.5" width="{W_ST - 1}" height="{H - 1}" rx="14" fill="{N800}" stroke="{BORDER}"/>'
        f"{top_edge(W_ST, uid)}"
        f"{overline(pad, 40, '// TECH STACK')}"
        f'<text x="{right}" y="40" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">{n_items} tools</text>'
    )
    return head + "".join(parts) + "</svg>"


# ------------------------------------------------------------- project cards
def wrap_px(text, max_w, size, bold=False):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        cand = (cur + " " + w_).strip()
        if text_w(cand, size, bold=bold) > max_w and cur:
            lines.append(cur)
            cur = w_
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def project(uid, title, status_label, state, desc, chips_):
    W, H = 492, 220
    color, _ = STATUS[state]
    out = [card_open(W, H, uid, title)]
    s, _pw = pill(PAD_CARD, 24, status_label, color, h=22)
    out.append(s)
    out.append(text_el(PAD_CARD, 88, title, T_TITLE))
    y = 112
    for ln in wrap_px(desc, W - 2 * PAD_CARD, T_BODY["size"])[:3]:
        out.append(text_el(PAD_CARD, y, ln, T_BODY))
        y += T_BODY["lh"]
    x = PAD_CARD
    for c in chips_:
        s, w = chip(x, H - 26 - 24, c, h=24, size=11.5, mono=True, dot=False)
        out.append(s)
        x += w + 8
    out.append("</svg>")
    return "".join(out)


PROJECTS = [
    ("project-hr-erp.svg", "Archai HR ERP", "SaaS · Completed", "shipped",
     "Multi-tenant HR platform: a central platform project plus one Supabase project per company. Employees, attendance, leave and payroll.",
     ["React", "TypeScript", "Supabase"]),
    ("project-futurex-pos.svg", "FutureX POS", "Company project · Completed", "shipped",
     "Cashier and kitchen workflows, order and check management, mixed payment methods, role-based access and receipt printing.",
     ["Flutter", "Cubit", "Dio"]),
    ("project-futurex-erp.svg", "FutureX ERP", "Company project · In development", "building",
     "ShellRoute app shell, attendance-based access and a layered thermal-printing module over USB, Bluetooth and network.",
     ["Flutter", "GoRouter", "Cubit"]),
    ("project-rasha7ly.svg", "Rasha7ly", "EDPI program project", "info",
     "Travel recommendation app with personalized destination suggestions, image browsing and animated UI.",
     ["Flutter", "MVVM", "Firebase"]),
    ("project-stylish.svg", "Stylish", "E-commerce app", "info",
     "E-commerce app with 20+ screens implemented from Figma designs, structured with Clean Architecture.",
     ["Flutter", "Cubit", "Clean Arch."]),
    ("project-portfolio.svg", "Portfolio", "Live · himego.vercel.app", "live",
     "Bilingual (Arabic / English) personal portfolio built with React and Vite.",
     ["React", "Vite"]),
]


# ----------------------------------------------------------- experience card
EXPERIENCE = [
    ("Mobile & Desktop App Developer (Flutter)", "FutureX", "Mar 2026 – Present"),
    ("Founder & CEO", "Archai Solutions", "Jun 2026 – Present"),
    ("Freelance Mobile & Software Developer", "Self-employed", "Jan 2024 – Present"),
    ("Bachelor's Degree, Higher Technological Institute, Beni Suef", "", "2026"),
]

W_EX = 1012


def experience():
    uid = "ex"
    pad = 32
    y0, pitch = 74, 44
    H = y0 + (len(EXPERIENCE) - 1) * pitch + 30
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_EX}" height="{H}" viewBox="0 0 {W_EX} {H}" role="img">'
        f"<title>Experience</title>{defs(uid)}"
        f'<rect x="0.5" y="0.5" width="{W_EX - 1}" height="{H - 1}" rx="14" fill="{N800}" stroke="{BORDER}"/>'
        f"{top_edge(W_EX, uid)}"
        f"{overline(pad, 40, '// EXPERIENCE')}",
    ]
    line_x = pad + 15
    last = y0 + (len(EXPERIENCE) - 1) * pitch
    out.append(f'<line x1="{line_x}" y1="{y0 - 4}" x2="{line_x}" y2="{last + 2}" stroke="{BORDER_SOFT}" stroke-width="2"/>')
    y = y0
    for role, org, period in EXPERIENCE:
        cy = y - 5
        if org:
            out.append(f'<circle cx="{line_x}" cy="{cy}" r="4.5" fill="url(#{uid}g)"/>')
            out.append(f'<circle cx="{line_x}" cy="{cy}" r="8" fill="none" stroke="{VIOLET}" stroke-opacity="0.25"/>')
        else:
            out.append(f'<circle cx="{line_x}" cy="{cy}" r="4" fill="{SUBTLE}"/>')
        out.append(text_el(pad + 34, y, role, T_ENTRY))
        tx = pad + 34 + text_w(role, T_ENTRY["size"], bold=True) + 18
        if org:
            out.append(text_el(tx, y, org, dict(T_CHIP, fill=MUTED)))
        out.append(text_el(W_EX - pad, y, period, dict(T_CHIP, fill=MUTED), anchor="end"))
        y += pitch
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    save("banner.svg", banner())
    save("stack.svg", stack())
    for i, (fn, t, s, st, d, c) in enumerate(PROJECTS):
        save(fn, project(f"p{i}", t, s, st, d, c))
    save("experience.svg", experience())
    print("static assets written to", OUT)
