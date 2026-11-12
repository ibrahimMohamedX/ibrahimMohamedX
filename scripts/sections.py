"""Stack, experience, contact buttons and the closing card."""
import tokens as T
from svgkit import Doc, measure, pulse_css, tag, wrap

# ------------------------------------------------------------------ stack
STACK = [
    ("Mobile and desktop", ["Flutter", "Dart", "Cubit / BLoC", "Clean Architecture", "MVVM", "GoRouter", "Windows desktop"]),
    ("Networking and data", ["REST APIs", "Dio", "Firebase Auth", "Cloud Firestore", "FCM", "Hive", "Freezed", "build_runner"]),
    ("Web and backend", ["React", "TypeScript", "JavaScript", "HTML", "CSS", "Vite", "Supabase"]),
    ("Business systems", ["POS / ERP", "Payment workflows", "Role-based access", "Bluetooth, USB and network printing"]),
    ("Tools", ["Git", "GitHub", "GitLab", "Figma", "VS Code", "Claude Code"]),
]
CORE = {"Flutter", "Dart"}


def stack():
    W = T.W
    x0, x1 = 284, W - 48
    rows = []
    y = 40
    for label, items in STACK:
        x, ry, placed = x0, y, []
        for it in items:
            w = measure(it, "sans500", 16.5) + 26
            if x + w > x1:
                x, ry = x0, ry + 46
            placed.append((it, x, ry, w))
            x += w + 10
        rows.append((label, y, ry, placed))
        y = ry + 34 + 36
    H = y - 36 + 40
    d = Doc("st", W, H, "Tech stack: Flutter, Dart, Cubit/BLoC, Clean Architecture, Dio, Firebase, Hive, React, TypeScript, Supabase, Git",
            bg=T.SURFACE)
    g = d.gradient("core", 0, 0, 1, 1)
    d.add(f'<circle cx="{W - 120}" cy="0" r="320" fill="{d.glow("gl", T.VIOLET, .16)}"/>')
    for k, (label, ry0, last, placed) in enumerate(rows):
        d.text(48, ry0 + 24, label, "sans600", 22, T.INK, ls=-0.2)
        for it, x, yy, w in placed:
            core = it in CORE
            stroke = g if core else T.LINE
            fill = T.RAISED
            d.add(f'<rect x="{x:g}" y="{yy}" width="{w:g}" height="34" rx="17" fill="{fill}" stroke="{stroke}" stroke-width="{1.6 if core else 1}"/>')
            d.text(x + 13, yy + 23, it, "sans500", 16.5, T.INK if core else T.BODY)
        if k < len(rows) - 1:
            ly = last + 34 + 18
            d.add(f'<path d="M48 {ly}H{W - 48}" stroke="{T.LINE_SOFT}"/>')
    return d.render()


# ------------------------------------------------------------- experience
EXPERIENCE = [
    ("Aug 2026 – present", "Founder and CEO", "Archai Solutions", True,
     "Early-stage company for custom software, mobile and web apps, AI solutions and embedded and IoT work. I lead technical direction and designed Archai HR ERP."),
    ("Mar 2026 – present", "Mobile and desktop app developer", "FutureX", True,
     "Flutter mobile and Windows desktop apps for POS and ERP products: Dio with refresh-token sessions, Cubit/BLoC, GoRouter, payments, role-based permissions and Bluetooth, USB and network printing."),
    ("Jan 2024 – present", "Freelance software developer", "Self-employed", True,
     "Mobile apps and custom software for clients: Figma-to-Flutter UI, REST APIs, Firebase (Auth, Firestore, Cloud Messaging) and offline-first persistence with Hive."),
    ("Graduated 2026", "Bachelor's degree, Technology and Software Development", "Higher Technological Institute, Beni Suef", False, None),
]


def experience():
    W = T.W
    tx, cx = 48, 330
    body_x = 372
    y = 44
    items = []
    for date, role, org, live, desc in EXPERIENCE:
        lines = wrap(desc, "sans400", 18, W - body_x - 48) if desc else []
        h = 34 + 30 + (len(lines) * 28 + 8 if lines else 0)
        items.append((y, date, role, org, live, lines))
        y += h + 22
    H = y - 22 + 40
    d = Doc("ex", W, H, "Experience: Founder at Archai Solutions, Flutter developer at FutureX, freelance developer, Bachelor's degree 2026",
            bg=T.SURFACE)
    pulse_css(d)
    d.add(f'<circle cx="0" cy="{H}" r="300" fill="{d.glow("gl", T.CYAN, .10)}"/>')
    top, bot = items[0][0] + 12, items[-1][0] + 12
    grad = d.gradient("line", 0, top, 0, bot, stops=[(0, T.CYAN), (1, T.VIOLET), ], units="userSpaceOnUse")
    d.add(f'<path d="M{cx} {top}V{bot}" stroke="{T.LINE}" stroke-width="2"/>')
    d.add(f'<path d="M{cx} {top}V{bot - 30}" stroke="{grad}" stroke-width="2" stroke-linecap="round"/>')
    for yy, date, role, org, live, lines in items:
        d.text(tx, yy + 18, date, "sans500", 17, T.MUTED)
        if live:
            d.add(f'<circle cx="{cx}" cy="{yy + 12}" r="13" fill="{T.CYAN}" fill-opacity=".12" class="{d.i("pulse")}"/>')
            d.add(f'<circle cx="{cx}" cy="{yy + 12}" r="6" fill="{T.SURFACE}" stroke="{T.CYAN}" stroke-width="2.2"/>')
            d.add(f'<circle cx="{cx}" cy="{yy + 12}" r="2.6" fill="{T.CYAN}"/>')
        else:
            d.add(f'<circle cx="{cx}" cy="{yy + 12}" r="6" fill="{T.SURFACE}" stroke="{T.FAINT}" stroke-width="2"/>')
        d.text(body_x, yy + 20, role, "sans600", 24, T.INK, ls=-0.3)
        d.text(body_x, yy + 50, org, "sans500", 18, T.VIOLET_L if live else T.MUTED)
        ly = yy + 84
        for ln in lines:
            d.text(body_x, ly, ln, "sans400", 18, T.BODY)
            ly += 28
    d.reduced_motion(f".{d.i('pulse')}{{animation:none!important}}")
    return d.render()


# ---------------------------------------------------------------- buttons
ICONS = {
    "globe": '<circle cx="12" cy="12" r="8.5" fill="none" stroke="{c}" stroke-width="1.7"/><path d="M3.5 12h17M12 3.5c2.6 2.4 3.8 5.3 3.8 8.5s-1.2 6.1-3.8 8.5c-2.6-2.4-3.8-5.3-3.8-8.5S9.4 5.9 12 3.5z" fill="none" stroke="{c}" stroke-width="1.7"/>',
    "mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="3" fill="none" stroke="{c}" stroke-width="1.7"/><path d="M4.5 7.5l7.5 6 7.5-6" fill="none" stroke="{c}" stroke-width="1.7" stroke-linejoin="round"/>',
    "in": '<rect x="3.5" y="3.5" width="17" height="17" rx="4" fill="none" stroke="{c}" stroke-width="1.7"/><path d="M8 10.5v6M8 7.6v.1M11.5 16.5v-6m0 3c0-1.6 1-2.8 2.6-2.8s2.4 1.1 2.4 2.8v3" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round"/>',
    "code": '<path d="M8.5 7.5L4 12l4.5 4.5M15.5 7.5L20 12l-4.5 4.5M13.5 5.5l-3 13" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
}


def button(uid, label, icon, hue, primary=False):
    size = 19
    w = int(measure(label, "sans600", size) + 84)
    h = 56
    d = Doc(uid, w, h, label, radius=h / 2, bg=(hue if primary else T.SURFACE), border=not primary)
    ink = T.BG if primary else T.INK
    d.add(f'<g transform="translate(24 16) scale(1)">{ICONS[icon].format(c=ink if primary else hue)}</g>')
    d.text(58, 35.5, label, "sans600", size, ink)
    return d.render()


BUTTONS = [
    ("btn-portfolio.svg", "Portfolio", "globe", T.CYAN, True),
    ("btn-email.svg", "Email me", "mail", T.VIOLET_L, False),
    ("btn-linkedin.svg", "LinkedIn", "in", T.CYAN, False),
    ("btn-archai.svg", "Archai Solutions", "code", T.VIOLET_L, False),
]


def buttons():
    return {fn: button(fn[:-4].replace("btn-", "b")[:4], lbl, ic, hue, pr) for fn, lbl, ic, hue, pr in BUTTONS}


# ---------------------------------------------------------------- closing
def contact():
    W, H = T.W, 300
    d = Doc("ct", W, H, "Get in touch: open to remote Flutter, mobile and software engineering roles", bg=T.SURFACE)
    g = d.gradient("g", 0, 0, 1, 0)
    d.add(f'<circle cx="{W - 160}" cy="40" r="380" fill="{d.glow("gl", T.VIOLET, .30)}"/>')
    d.add(f'<circle cx="120" cy="320" r="260" fill="{d.glow("gc", T.CYAN, .12)}"/>')
    pulse_css(d)
    d.add(f'<circle cx="64" cy="70" r="5" fill="{T.GREEN}" class="{d.i("pulse")}"/>')
    d.text(80, 76, "Available for remote work", "sans500", 18, T.BODY)
    d.text(54, 150, "Need a Flutter engineer?", "sans700", 54, T.INK, ls=-1.5)
    d.text(56, 206, "I'm looking for a remote role on a team that ships mobile, desktop and SaaS products.", "sans400", 22, T.BODY)
    d.text(56, 252, "ibrahimmohamed09854@gmail.com", "sans600", 22, T.VIOLET_L)
    d.reduced_motion(f".{d.i('pulse')}{{animation:none!important}}")
    return d.render()


# =============================================================== compact
def stack_sm():
    W = T.W_SM
    x0, x1 = 32, W - 32
    y = 36
    placed_rows = []
    for label, items in STACK:
        ly = y
        x, ry, placed = x0, y + 40, []
        for it in items:
            w = measure(it, "sans500", 16) + 26
            if x + w > x1:
                x, ry = x0, ry + 42
            placed.append((it, x, ry, w))
            x += w + 8
        placed_rows.append((label, ly, placed))
        y = ry + 34 + 22
        placed_rows[-1] = (label, ly, placed, y - 11)
    H = y - 22 + 36
    d = Doc("sts", W, H, "Tech stack: Flutter, Dart, Cubit/BLoC, Clean Architecture, Dio, Firebase, Hive, React, TypeScript, Supabase, Git",
            bg=T.SURFACE)
    g = d.gradient("core", 0, 0, 1, 1)
    d.add(f'<circle cx="{W}" cy="0" r="260" fill="{d.glow("gl", T.VIOLET, .16)}"/>')
    for k, (label, ly, placed, div) in enumerate(placed_rows):
        d.text(x0, ly + 22, label, "sans600", 20, T.INK, ls=-0.2)
        for it, x, yy, w in placed:
            core = it in CORE
            d.add(f'<rect x="{x:g}" y="{yy}" width="{w:g}" height="34" rx="17" fill="{T.RAISED}" stroke="{g if core else T.LINE}" stroke-width="{1.6 if core else 1}"/>')
            d.text(x + 13, yy + 23, it, "sans500", 16, T.INK if core else T.BODY)
        if k < len(placed_rows) - 1:
            d.add(f'<path d="M{x0} {div:g}H{W - 32}" stroke="{T.LINE_SOFT}"/>')
    return d.render()


def experience_sm():
    W = T.W_SM
    cx, bx = 38, 72
    y = 38
    items = []
    for date, role, org, live, desc in EXPERIENCE:
        rl = wrap(role, "sans600", 22, W - bx - 28)
        dl = wrap(desc, "sans400", 17, W - bx - 28) if desc else []
        h = 26 + len(rl) * 28 + 26 + (len(dl) * 25 + 10 if dl else 0)
        items.append((y, date, rl, org, live, dl))
        y += h + 26
    H = y - 26 + 34
    d = Doc("exs", W, H, "Experience: Founder at Archai Solutions, Flutter developer at FutureX, freelance developer, Bachelor's degree 2026",
            bg=T.SURFACE)
    pulse_css(d)
    top, bot = items[0][0] + 8, items[-1][0] + 8
    grad = d.gradient("line", 0, top, 0, bot, stops=[(0, T.CYAN), (1, T.VIOLET)], units="userSpaceOnUse")
    d.add(f'<path d="M{cx} {top}V{bot}" stroke="{T.LINE}" stroke-width="2"/>')
    d.add(f'<path d="M{cx} {top}V{bot - 24}" stroke="{grad}" stroke-width="2" stroke-linecap="round"/>')
    for yy, date, rl, org, live, dl in items:
        if live:
            d.add(f'<circle cx="{cx}" cy="{yy + 8}" r="12" fill="{T.CYAN}" fill-opacity=".12" class="{d.i("pulse")}"/>')
            d.add(f'<circle cx="{cx}" cy="{yy + 8}" r="6" fill="{T.SURFACE}" stroke="{T.CYAN}" stroke-width="2.2"/>')
            d.add(f'<circle cx="{cx}" cy="{yy + 8}" r="2.6" fill="{T.CYAN}"/>')
        else:
            d.add(f'<circle cx="{cx}" cy="{yy + 8}" r="6" fill="{T.SURFACE}" stroke="{T.FAINT}" stroke-width="2"/>')
        d.text(bx, yy + 13, date, "sans500", 15, T.MUTED)
        ty = yy + 44
        for ln in rl:
            d.text(bx, ty, ln, "sans600", 22, T.INK, ls=-0.3)
            ty += 28
        d.text(bx, ty - 2, org, "sans500", 17, T.VIOLET_L if live else T.MUTED)
        ty += 28
        for ln in dl:
            d.text(bx, ty, ln, "sans400", 17, T.BODY)
            ty += 25
    d.reduced_motion(f".{d.i('pulse')}{{animation:none!important}}")
    return d.render()


def contact_sm():
    W, H = T.W_SM, 360
    d = Doc("cts", W, H, "Get in touch: open to remote Flutter, mobile and software engineering roles", bg=T.SURFACE)
    d.add(f'<circle cx="{W - 60}" cy="20" r="300" fill="{d.glow("gl", T.VIOLET, .30)}"/>')
    d.add(f'<circle cx="40" cy="380" r="240" fill="{d.glow("gc", T.CYAN, .12)}"/>')
    pulse_css(d)
    d.add(f'<circle cx="44" cy="58" r="5" fill="{T.GREEN}" class="{d.i("pulse")}"/>')
    d.text(60, 64, "Available for remote work", "sans500", 17, T.BODY)
    d.text(34, 134, "Need a Flutter", "sans700", 46, T.INK, ls=-1.2)
    d.text(34, 186, "engineer?", "sans700", 46, T.INK, ls=-1.2)
    for i, ln in enumerate(wrap("I'm looking for a remote role on a team that ships mobile, desktop and SaaS products.", "sans400", 20, W - 68)):
        d.text(36, 232 + i * 28, ln, "sans400", 20, T.BODY)
    d.text(36, 316, "ibrahimmohamed09854@gmail.com", "sans600", 19, T.VIOLET_L)
    d.reduced_motion(f".{d.i('pulse')}{{animation:none!important}}")
    return d.render()
