"""Stack, experience, contact, buttons (desktop + compact variants).

Same choreography as the cards: staggered entrance on a shared 12 s loop,
ambient motion (light sweep, drifting glow, travelling pulse on the timeline),
synchronized exit, replay.
"""
import tokens as T
from svgkit import Doc, measure, pulse_css, tag, wrap

LOOP = 12.0

# ------------------------------------------------------------------ stack
STACK = [
    ("Mobile and desktop", ["Flutter", "Dart", "Cubit / BLoC", "Clean Architecture", "MVVM", "GoRouter", "Windows desktop"]),
    ("Networking and data", ["REST APIs", "Dio", "Firebase Auth", "Cloud Firestore", "FCM", "Hive", "Freezed", "build_runner"]),
    ("Web and backend", ["React", "TypeScript", "JavaScript", "HTML", "CSS", "Vite", "Supabase"]),
    ("Business systems", ["POS / ERP", "Payment workflows", "Role-based access", "Bluetooth, USB and network printing"]),
    ("Tools", ["Git", "GitHub", "GitLab", "Figma", "VS Code", "Claude Code"]),
]
CORE = {"Flutter", "Dart"}


def _stack(compact):
    W = T.W_SM if compact else T.W
    x0, x1 = (32, W - 32) if compact else (284, W - 48)
    fs, padw, gap = (16, 26, 8) if compact else (16.5, 26, 10)
    rows, y = [], 36 if compact else 40
    for label, items in STACK:
        ly = y
        x, ry, placed = x0, (y + 40 if compact else y), []
        for it in items:
            w = measure(it, "sans500", fs) + padw
            if x + w > x1:
                x, ry = x0, ry + 42 if compact else ry + 46
            placed.append((it, x, ry, w))
            x += w + gap
        y = ry + 34 + (22 if compact else 36)
        rows.append((label, ly, placed, y - (11 if compact else 18)))
    H = (y - 22 + 36) if compact else (y - 36 + 40)
    d = Doc("sts" if compact else "st", W, H,
            "Tech stack: Flutter, Dart, Cubit/BLoC, Clean Architecture, Dio, Firebase, Hive, React, TypeScript, Supabase, Git", bg=T.SURFACE)
    d.set_loop(LOOP)
    g = d.gradient("core", 0, 0, 1, 1)
    d.add(f'<g {d.drift(-30, 20, 15)}><circle cx="{W - 80}" cy="0" r="320" fill="{d.glow("gl", T.VIOLET, .16)}"/></g>')
    d.shine(0, 0, W, H, delay=2, period=10)
    n = 0
    for k, (label, ly, placed, div) in enumerate(rows):
        with d.rv("left", 0.15 + k * 0.16):
            if compact:
                d.text(x0, ly + 22, label, "sans600", 20, T.INK, ls=-0.2)
            else:
                d.text(48, ly + 24, label, "sans600", 22, T.INK, ls=-0.2)
        for it, x, yy, w in placed:
            core = it in CORE
            with d.rv("pop", 0.35 + k * 0.16 + (n % 8) * 0.045):
                if core:
                    d.add(f'<g {d.idle("core", "0%{transform:scale(1)}100%{transform:scale(1.06)}", 1.8)}>')
                d.add(f'<rect x="{x:g}" y="{yy}" width="{w:g}" height="34" rx="17" fill="{T.RAISED}" '
                      f'stroke="{g if core else T.LINE}" stroke-width="{1.6 if core else 1}"/>')
                d.text(x + 13, yy + 23, it, "sans500", fs, T.INK if core else T.BODY)
                if core:
                    d.add("</g>")
            n += 1
        if k < len(rows) - 1:
            with d.rv("growx", 0.3 + k * 0.16):
                d.add(f'<path d="M{x0 if compact else 48} {div:g}H{W - (32 if compact else 48)}" stroke="{T.LINE_SOFT}"/>')
    return d.render()


def stack():
    return _stack(False)


def stack_sm():
    return _stack(True)


# ------------------------------------------------------------- experience
EXPERIENCE = [
    ("Aug 2026 – present", "Founder and CEO", "Archai Solutions", "live",
     "Early-stage company for custom software, mobile and web apps, AI solutions and embedded and IoT work. I lead technical direction and designed Archai HR ERP."),
    ("Mar 2026 – present", "Mobile and desktop app developer", "FutureX", "live",
     "Flutter mobile and Windows desktop apps for POS and ERP products: Dio with refresh-token sessions, Cubit/BLoC, GoRouter, payments, role-based permissions and Bluetooth, USB and network printing."),
    ("Jan 2024 – present", "Freelance software developer", "Self-employed", "live",
     "Mobile apps and custom software for clients: Figma-to-Flutter UI, REST APIs, Firebase (Auth, Firestore, Cloud Messaging) and offline-first persistence with Hive."),
    ("Graduated 2026", "Bachelor's degree, Technology and Software Development", "Higher Technological Institute, Beni Suef", "done", None),
]


def _node(d, cx, cy, state, t):
    """live = pulsing cyan ring (ongoing). done = solid green with a check (achieved)."""
    with d.rv("pop", t):
        if state == "live":
            d.add(f'<circle cx="{cx}" cy="{cy}" r="13" fill="{T.CYAN}" fill-opacity=".12" class="{d.i("pulse")}"/>')
            d.add(f'<circle cx="{cx}" cy="{cy}" r="6" fill="{T.SURFACE}" stroke="{T.CYAN}" stroke-width="2.2"/>')
            d.add(f'<circle cx="{cx}" cy="{cy}" r="2.6" fill="{T.CYAN}"/>')
        else:
            d.add(f'<circle cx="{cx}" cy="{cy}" r="14" fill="{T.GREEN}" fill-opacity=".14"/>')
            d.add(f'<circle cx="{cx}" cy="{cy}" r="10.5" fill="{T.GREEN}"/>')
            d.add(f'<path d="M{cx - 4.6} {cy + .4}l3.2 3.2 6 -6.4" fill="none" stroke="{T.BG}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')


def _experience(compact):
    W = T.W_SM if compact else T.W
    cx = 38 if compact else 330
    bx = 72 if compact else 372
    y = 38 if compact else 44
    items = []
    for date, role, org, state, desc in EXPERIENCE:
        if compact:
            rl = wrap(role, "sans600", 22, W - bx - 28)
            dl = wrap(desc, "sans400", 17, W - bx - 28) if desc else []
            h = 26 + len(rl) * 28 + 26 + (len(dl) * 25 + 10 if dl else 0)
            items.append((y, date, rl, org, state, dl))
            y += h + 26
        else:
            dl = wrap(desc, "sans400", 18, W - bx - 48) if desc else []
            h = 34 + 30 + (len(dl) * 28 + 8 if dl else 0)
            items.append((y, date, [role], org, state, dl))
            y += h + 22
    H = (y - 26 + 34) if compact else (y - 22 + 40)
    d = Doc("exs" if compact else "ex", W, H,
            "Experience: Founder at Archai Solutions, Flutter developer at FutureX, freelance developer, Bachelor's degree completed in 2026", bg=T.SURFACE)
    d.set_loop(LOOP)
    pulse_css(d)
    d.add(f'<g {d.drift(30, -20, 15)}><circle cx="0" cy="{H}" r="300" fill="{d.glow("gl", T.CYAN, .10)}"/></g>')
    d.shine(0, 0, W, H, delay=3, period=10)
    off = 8 if compact else 12
    top, bot = items[0][0] + off, items[-1][0] + off
    grad = d.gradient("line", 0, top, 0, bot, stops=[(0, T.CYAN), (0.8, T.VIOLET), (1, T.GREEN)], units="userSpaceOnUse")
    d.add(f'<path d="M{cx} {top}V{bot}" stroke="{T.LINE}" stroke-width="2"/>')
    d.draw(f"M{cx} {top}V{bot}", grad, 2, 0.2)
    # light travelling down the timeline
    trav = d.idle("trav", f"0%{{transform:translateY(0);opacity:0}}12%{{opacity:1}}88%{{opacity:1}}100%{{transform:translateY({bot - top}px);opacity:0}}",
                  3.6, 0, alt=False, ease="linear")
    d.add(f'<g {trav}><circle cx="{cx}" cy="{top}" r="4" fill="{T.CYAN}"/></g>')
    for k, (yy, date, rl, org, state, dl) in enumerate(items):
        t = 0.45 + k * 0.32
        _node(d, cx, yy + off, state, t)
        done = state == "done"
        if compact:
            with d.rv("up", t + 0.1):
                d.text(bx, yy + 13, date, "sans500", 15, T.GREEN if done else T.MUTED)
                ty = yy + 44
                for ln in rl:
                    d.text(bx, ty, ln, "sans600", 22, T.INK, ls=-0.3)
                    ty += 28
                d.text(bx, ty - 2, org, "sans500", 17, T.GREEN if done else T.VIOLET_L)
                ty += 28
                for ln in dl:
                    d.text(bx, ty, ln, "sans400", 17, T.BODY)
                    ty += 25
        else:
            with d.rv("left", t + 0.05):
                d.text(48, yy + 18, date, "sans500", 17, T.GREEN if done else T.MUTED)
            with d.rv("up", t + 0.12):
                d.text(bx, yy + 20, rl[0], "sans600", 24, T.INK, ls=-0.3)
                d.text(bx, yy + 50, org, "sans500", 18, T.GREEN if done else T.VIOLET_L)
                ly = yy + 84
                for ln in dl:
                    d.text(bx, ly, ln, "sans400", 18, T.BODY)
                    ly += 28
    return d.render()


def experience():
    return _experience(False)


def experience_sm():
    return _experience(True)


# ---------------------------------------------------------------- buttons
ICONS = {
    "globe": '<circle cx="12" cy="12" r="8.5" fill="none" stroke="{c}" stroke-width="1.7"/><path d="M3.5 12h17M12 3.5c2.6 2.4 3.8 5.3 3.8 8.5s-1.2 6.1-3.8 8.5c-2.6-2.4-3.8-5.3-3.8-8.5S9.4 5.9 12 3.5z" fill="none" stroke="{c}" stroke-width="1.7"/>',
    "mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="3" fill="none" stroke="{c}" stroke-width="1.7"/><path d="M4.5 7.5l7.5 6 7.5-6" fill="none" stroke="{c}" stroke-width="1.7" stroke-linejoin="round"/>',
    "in": '<rect x="3.5" y="3.5" width="17" height="17" rx="4" fill="none" stroke="{c}" stroke-width="1.7"/><path d="M8 10.5v6M8 7.6v.1M11.5 16.5v-6m0 3c0-1.6 1-2.8 2.6-2.8s2.4 1.1 2.4 2.8v3" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round"/>',
    "code": '<path d="M8.5 7.5L4 12l4.5 4.5M15.5 7.5L20 12l-4.5 4.5M13.5 5.5l-3 13" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
}


def button(uid, label, icon, hue, primary=False, idx=0):
    size = 19
    w = int(measure(label, "sans600", size) + 84)
    h = 56
    d = Doc(uid, w, h, label, radius=h / 2, bg=(hue if primary else T.SURFACE), border=not primary)
    d.set_loop(LOOP)
    ink = T.BG if primary else T.INK
    with d.rv("pop", 0.1 + idx * 0.14):
        d.add(f'<g {d.float_(2, 3 + idx * .4, idx * .7)}><g transform="translate(24 16)">{ICONS[icon].format(c=ink if primary else hue)}</g></g>')
        d.text(58, 35.5, label, "sans600", size, ink)
    d.shine(0, 0, w, h, delay=idx * 1.2, period=6, op=0.16 if primary else 0.08)
    return d.render()


BUTTONS = [
    ("btn-portfolio.svg", "Portfolio", "globe", T.CYAN, True),
    ("btn-email.svg", "Email me", "mail", T.VIOLET_L, False),
    ("btn-linkedin.svg", "LinkedIn", "in", T.CYAN, False),
    ("btn-archai.svg", "Archai Solutions", "code", T.VIOLET_L, False),
]


def buttons():
    return {fn: button("b" + str(i), lbl, ic, hue, pr, i) for i, (fn, lbl, ic, hue, pr) in enumerate(BUTTONS)}


# ---------------------------------------------------------------- closing
def contact():
    W, H = T.W, 300
    d = Doc("ct", W, H, "Get in touch: open to remote Flutter, mobile and software engineering roles", bg=T.SURFACE)
    d.set_loop(LOOP)
    pulse_css(d)
    d.add(f'<g {d.drift(-40, 20, 15)}><circle cx="{W - 160}" cy="40" r="380" fill="{d.glow("gl", T.VIOLET, .30)}"/></g>')
    d.add(f'<g {d.drift(30, -20, 12, 3)}><circle cx="120" cy="320" r="260" fill="{d.glow("gc", T.CYAN, .12)}"/></g>')
    d.shine(0, 0, W, H, delay=2, period=9)
    with d.rv("fade", 0.1):
        d.add(f'<circle cx="64" cy="70" r="5" fill="{T.GREEN}" class="{d.i("pulse")}"/>')
        d.text(80, 76, "Available for remote work", "sans500", 18, T.BODY)
    with d.rv("up", 0.25):
        d.text(54, 150, "Need a Flutter engineer?", "sans700", 54, T.INK, ls=-1.5)
    with d.rv("up", 0.5):
        d.text(56, 206, "I'm looking for a remote role on a team that ships mobile, desktop and SaaS products.", "sans400", 22, T.BODY)
    with d.rv("up", 0.75):
        d.text(56, 252, "ibrahimmohamed09854@gmail.com", "sans600", 22, T.VIOLET_L)
    g = d.gradient("ul", 0, 0, 1, 0)
    d.draw(f"M56 264H{56 + measure('ibrahimmohamed09854@gmail.com', 'sans600', 22):.0f}", g, 2.5, 1.1)
    return d.render()


def contact_sm():
    W, H = T.W_SM, 360
    d = Doc("cts", W, H, "Get in touch: open to remote Flutter, mobile and software engineering roles", bg=T.SURFACE)
    d.set_loop(LOOP)
    pulse_css(d)
    d.add(f'<g {d.drift(-30, 20, 15)}><circle cx="{W - 60}" cy="20" r="300" fill="{d.glow("gl", T.VIOLET, .30)}"/></g>')
    d.add(f'<g {d.drift(24, -20, 12, 3)}><circle cx="40" cy="380" r="240" fill="{d.glow("gc", T.CYAN, .12)}"/></g>')
    d.shine(0, 0, W, H, delay=2, period=9)
    with d.rv("fade", 0.1):
        d.add(f'<circle cx="44" cy="58" r="5" fill="{T.GREEN}" class="{d.i("pulse")}"/>')
        d.text(60, 64, "Available for remote work", "sans500", 17, T.BODY)
    with d.rv("up", 0.25):
        d.text(34, 134, "Need a Flutter", "sans700", 46, T.INK, ls=-1.2)
    with d.rv("up", 0.4):
        d.text(34, 186, "engineer?", "sans700", 46, T.INK, ls=-1.2)
    with d.rv("up", 0.6):
        for i, ln in enumerate(wrap("I'm looking for a remote role on a team that ships mobile, desktop and SaaS products.", "sans400", 20, W - 68)):
            d.text(36, 232 + i * 28, ln, "sans400", 20, T.BODY)
    with d.rv("up", 0.85):
        d.text(36, 316, "ibrahimmohamed09854@gmail.com", "sans600", 19, T.VIOLET_L)
    g = d.gradient("ul", 0, 0, 1, 0)
    d.draw(f"M36 326H{36 + measure('ibrahimmohamed09854@gmail.com', 'sans600', 19):.0f}", g, 2.5, 1.2)
    return d.render()
