#!/usr/bin/env python3
"""Build the static SVG assets: banner, tech stack and featured-project cards.
Run: python scripts/build_static_assets.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from card_style import *  # noqa: E402,F401,F403

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)


def save(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(text)


# ------------------------------------------------------------------ banner
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
    <rect x="905" y="125" width="110" height="90" rx="16" fill="#0d0b18" stroke="url(#bgv)" stroke-width="2.5"/>
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


# ------------------------------------------------------------------ tech stack
STACK = [
    ("MOBILE & DESKTOP", ["Flutter", "Dart", "Cubit / BLoC", "Clean Architecture", "MVVM", "GoRouter", "Windows Desktop"]),
    ("NETWORKING & DATA", ["REST APIs", "Dio", "Firebase Auth", "Cloud Firestore", "FCM", "Hive", "Freezed", "build_runner"]),
    ("WEB & BACKEND", ["React", "TypeScript", "JavaScript", "HTML", "CSS", "Vite", "Supabase"]),
    ("BUSINESS SYSTEMS", ["POS / ERP", "Payment workflows", "Role-based access", "Bluetooth · USB · Network printing"]),
    ("TOOLS", ["Git", "GitHub", "GitLab", "Figma", "VS Code", "Claude Code"]),
]


def stack():
    W = 1000
    label_w, x0, right = 190, 28, W - 28
    y = 62
    parts = []
    idx = 0
    for label, items in STACK:
        parts.append(f'<text x="{x0}" y="{y+20}" font-family="{MONO}" font-size="11.5" fill="{CYAN}" letter-spacing="1.5">{esc(label)}</text>')
        x = x0 + label_w
        row_y = y
        for it in items:
            w = int(len(it) * 7.9 + 32)
            if x + w > right:
                x = x0 + label_w
                row_y += 40
            parts.append(
                f'<g class="c" style="animation-delay:{idx*0.06:.2f}s">'
                f'<rect x="{x}" y="{row_y}" width="{w}" height="30" rx="15" fill="#120f22" stroke="{BORDER}"/>'
                f'<circle cx="{x+14}" cy="{row_y+15}" r="3" fill="url(#sg)"/>'
                f'<text x="{x+24}" y="{row_y+20}" font-family="{SANS}" font-size="13" fill="{TEXT}">{esc(it)}</text></g>'
            )
            x += w + 10
            idx += 1
        y = row_y + 52
        parts.append(f'<line x1="{x0}" y1="{y-12}" x2="{right}" y2="{y-12}" stroke="{BORDER}" stroke-opacity="0.6"/>')
    H = y + 6
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">'
        f"<title>Tech stack</title>{defs('s')}"
        f'<linearGradient id="sg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
        f"<style>.c{{opacity:0;animation:in .5s ease forwards}}@keyframes in{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}</style>"
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="{PANEL}" stroke="{BORDER}"/>'
        f'<rect x="16" y="0.5" width="{W-32}" height="3" rx="1.5" fill="url(#sg)"/>'
        f'<text x="{x0}" y="40" font-family="{MONO}" font-size="12" fill="{MUTED}" letter-spacing="2">// TECH STACK</text>'
    )
    return head + "".join(parts) + "</svg>"


# ------------------------------------------------------------------ project cards
def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def project(uid, title, status, desc, chips, accent=CYAN):
    W, H = 490, 214
    out = [card_open(W, H, uid, title)]
    sw = int(len(status) * 6.9 + 28)
    out.append(f'<rect x="28" y="26" width="{sw}" height="24" rx="12" fill="#120f22" stroke="{accent}" stroke-opacity="0.5"/>')
    out.append(f'<circle cx="42" cy="38" r="3.5" fill="{accent}"/>')
    out.append(f'<text x="52" y="42.5" font-family="{MONO}" font-size="11.5" fill="#d7d3ee">{esc(status)}</text>')
    out.append(f'<text x="28" y="86" font-family="{SANS}" font-size="23" font-weight="700" fill="{TEXT}">{esc(title)}</text>')
    y = 112
    for ln in wrap(desc, 62)[:3]:
        out.append(f'<text x="28" y="{y}" font-family="{SANS}" font-size="13" fill="{MUTED}">{esc(ln)}</text>')
        y += 19
    x = 28
    for c in chips:
        w = int(len(c) * 7 + 22)
        out.append(f'<rect x="{x}" y="{H-44}" width="{w}" height="24" rx="12" fill="#120f22" stroke="{BORDER}"/>')
        out.append(f'<text x="{x+w/2}" y="{H-27.5}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="#d7d3ee">{esc(c)}</text>')
        x += w + 8
    out.append("</svg>")
    return "".join(out)


PROJECTS = [
    ("project-hr-erp.svg", "Archai HR ERP", "SaaS · Completed",
     "Multi-tenant HR platform: a central platform project plus one Supabase project per company. Employees, attendance, leave and payroll.",
     ["React", "TypeScript", "Supabase"], CYAN),
    ("project-futurex-pos.svg", "FutureX POS", "Company project · Completed",
     "Cashier and kitchen workflows, order and check management, mixed payment methods, role-based access and receipt printing.",
     ["Flutter", "Cubit", "Dio"], VIOLET),
    ("project-futurex-erp.svg", "FutureX ERP", "Company project · In development",
     "ShellRoute app shell, attendance-based access and a layered thermal-printing module over USB, Bluetooth and network.",
     ["Flutter", "GoRouter", "Cubit"], VIOLET),
    ("project-rasha7ly.svg", "Rasha7ly", "EDPI program project",
     "Travel recommendation app with personalized destination suggestions, image browsing and animated UI.",
     ["Flutter", "MVVM", "Firebase"], CYAN),
    ("project-stylish.svg", "Stylish", "E-commerce app",
     "E-commerce app with 20+ screens implemented from Figma designs, structured with Clean Architecture.",
     ["Flutter", "Cubit", "Clean Arch."], CYAN),
    ("project-portfolio.svg", "Portfolio", "Live · himego.vercel.app",
     "Bilingual (Arabic / English) personal portfolio built with React and Vite.",
     ["React", "Vite"], VIOLET),
]

if __name__ == "__main__":
    save("banner.svg", banner())
    save("stack.svg", stack())
    for i, (fn, t, s, d, c, a) in enumerate(PROJECTS):
        save(fn, project(f"p{i}", t, s, d, c, a))
    print("static assets written to", OUT)
