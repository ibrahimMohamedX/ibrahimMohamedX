"""Hero banner.

Concept: Flutter, shown the way it is built. A Dart snippet types itself,
and the phone beside it is the screen that code produces: order lines arrive,
the Pay button is pressed, the state flips to Paid. A small Windows app and
three stack chips float around it. One 14 s loop; every element enters on its
own beat and the whole scene leaves together.

The un-animated state is the finished composition, so reduced-motion viewers
and static renderers see the complete banner.
"""
import tokens as T
from svgkit import Doc, pulse_css, status

LOOP = 14.0


def build(compact=False):
    W, H = (600, 840) if compact else (1200, 520)
    d = Doc("bn" + ("s" if compact else ""), W, H,
            "Ibrahim Mohamed, software engineer. Flutter mobile and desktop developer.",
            desc="Animated banner: Dart code types itself and builds a POS phone screen where an order is paid. Floating chips: Flutter, Dart, Cubit/BLoC. Open to remote roles.",
            bg=T.BG, radius=T.R_HERO)
    d.set_loop(LOOP, enter=0.7, exit_=0.7)
    u = d.i
    pulse_css(d)
    P = d._pct

    # ------------------------------------------------------------ atmosphere
    glow_v, glow_c = d.glow("gv", T.VIOLET, 0.34), d.glow("gc", T.CYAN, 0.16)
    if compact:
        d.add(f'<g {d.drift(30, -20, 16)}><circle cx="520" cy="590" r="420" fill="{glow_v}"/></g>')
        d.add(f'<g {d.drift(-20, 30, 13, 4)}><circle cx="20" cy="40" r="300" fill="{glow_c}"/></g>')
    else:
        d.add(f'<g {d.drift(-40, 26, 16)}><circle cx="960" cy="200" r="430" fill="{glow_v}"/></g>')
        d.add(f'<g {d.drift(30, -24, 13, 5)}><circle cx="40" cy="560" r="360" fill="{glow_c}"/></g>')
    d.add_def(f'<pattern id="{u("dots")}" width="28" height="28" patternUnits="userSpaceOnUse">'
              f'<circle cx="2" cy="2" r="1.1" fill="#fff" fill-opacity=".10"/></pattern>')
    d.add_def(f'<radialGradient id="{u("fade")}" cx="{.5 if compact else .72}" cy="{.7 if compact else .4}" r="0.75">'
              f'<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>')
    d.add_def(f'<mask id="{u("m")}"><rect width="{W}" height="{H}" fill="url(#{u("fade")})"/></mask>')
    d.add(f'<rect width="{W}" height="{H}" fill="url(#{u("dots")})" mask="url(#{u("m")})"/>')
    d.shine(0, 0, W, H, delay=3, period=11, op=0.05)

    # ------------------------------------------------------------ identity
    if compact:
        lx, sy, n1, n2, ns, ry, ay, rs, as_ = 36, 66, 160, 240, 80, 300, 344, 28, 20
    else:
        lx, sy, n1, n2, ns, ry, ay, rs, as_ = 64, 104, 214, 310, 92, 372, 420, 31, 22
    with d.rv("fade", 0.1):
        status(d, lx, sy, "Open to remote roles from Egypt", T.GREEN, pulse=True, size=17)
    with d.rv("up", 0.25):
        d.text(lx - 4, n1, "Ibrahim", "sans700", ns, T.INK, ls=-3)
    with d.rv("up", 0.42):
        d.text(lx - 4, n2, "Mohamed", "sans700", ns, T.INK, ls=-3)

    grad = d.gradient("role", lx, 0, lx + 440, 0, units="userSpaceOnUse")
    roles = ["Software engineer", "Flutter mobile & desktop", "Founder of Archai Solutions"]
    d.add_css(
        f".{u('role')}{{animation:{u('role')} 12s ease-in-out infinite}}"
        f"@keyframes {u('role')}{{0%{{opacity:0;transform:translateY(12px)}}4%,29%{{opacity:1;transform:translateY(0)}}"
        f"33%,100%{{opacity:0;transform:translateY(-12px)}}}}")
    with d.rv("fade", 0.8):
        for k, r in enumerate(roles):
            d.text(lx, ry, r, "sans500", rs, grad, cls="role", opacity=1 if k == 0 else 0,
                   extra=f'style="animation-delay:{k * 4}s"' + (f' id="{u("role0")}"' if k == 0 else ""))
    with d.rv("up", 1.0):
        d.text(lx, ay, "مهندس برمجيات · مطوّر تطبيقات الموبايل والديسكتوب", "ar400", as_, T.MUTED)

    # ------------------------------------------------------------ composition
    if compact:
        s = 0.9
        d.add(f'<g transform="translate({(600 - 520 * s) / 2 - 632 * s:.2f} {392 - 34 * s:.2f}) scale({s})">')

    # floating stack chips
    cx = 640
    for k, (label, col) in enumerate([("Flutter", T.CYAN), ("Dart", T.SKY), ("Cubit", T.VIOLET_L)]):
        from svgkit import measure
        w = measure(label, "sans600", 15) + 38
        with d.rv("pop", 0.55 + k * 0.12):
            d.add(f'<g {d.float_(5, 4.5 + k * .8, k * 1.3)}>')
            d.add(f'<rect x="{cx}" y="38" width="{w:g}" height="34" rx="17" fill="{T.RAISED}" stroke="{T.LINE}"/>')
            d.add(f'<circle cx="{cx + 17}" cy="55" r="4.5" fill="{col}"/>')
            d.text(cx + 29, 60, label, "sans600", 15, T.INK)
            d.add("</g>")
        cx += w + 10

    # code card (types itself)
    kx, ky, kw, kh = 640, 92, 332, 184
    with d.rv("left", 0.5):
        d.add(f'<g {d.float_(4, 7, 1.0)}>')
        d.add(f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="18" fill="{T.SURFACE}" stroke="{T.LINE}"/>')
        d.add(f'<path d="M{kx} {ky + 36}H{kx + kw}" stroke="{T.LINE_SOFT}"/>')
        for k in range(3):
            d.add(f'<circle cx="{kx + 20 + k * 15}" cy="{ky + 18}" r="4.3" fill="{T.FAINT}" fill-opacity=".6"/>')
        d.text(kx + kw / 2, ky + 23, "order_list.dart", "mono400", 12.5, T.MUTED, anchor="middle")
        lines = [
            [("BlocBuilder", T.CYAN), ("<", T.BODY), ("OrderCubit", T.CYAN), (", ", T.BODY), ("State", T.CYAN), (">(", T.BODY)],
            [("  builder", T.SKY), (": (", T.BODY), ("context", T.SKY), (", ", T.BODY), ("state", T.SKY), (") {", T.BODY)],
            [("    return ", T.VIOLET_L), ("OrderList", T.CYAN), ("(", T.BODY), ("state", T.SKY), (");", T.BODY)],
            [("  },", T.BODY)],
            [(")", T.BODY)],
        ]
        t = 1.0
        for k, parts in enumerate(lines):
            y = ky + 66 + k * 24
            d.rich(kx + 22, y, parts, "mono400", 13)
            n = sum(len(p) for p, _ in parts)
            d.cover(kx + 18, y - 16, 292, 22, T.SURFACE, t, 0.12 + n * 0.028, max(n // 2, 4))
            t += 0.12 + n * 0.028 + 0.1
        last = ky + 66 + 4 * 24
        d.add(f'<rect x="{kx + 30}" y="{last - 13}" width="7" height="17" rx="1.5" fill="{T.CYAN}" '
              f'style="animation:{u("blink")} 1s steps(1) infinite"/>')
        d.add_css(f"@keyframes {u('blink')}{{0%,50%{{opacity:1}}50.01%,100%{{opacity:0}}}}")
        d.add("</g>")

    # mini Windows app
    mx, my, mw, mh = 650, 336, 256, 150
    with d.rv("up", 1.5):
        d.add(f'<g {d.float_(5, 6.2, 2.2)}>')
        d.add(f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="16" fill="{T.SURFACE}" stroke="{T.LINE}"/>')
        d.add(f'<path d="M{mx} {my + 32}H{mx + mw}" stroke="{T.LINE_SOFT}"/>')
        for k in range(3):
            d.add(f'<circle cx="{mx + 18 + k * 14}" cy="{my + 16}" r="4" fill="{T.FAINT}" fill-opacity=".6"/>')
        d.text(mx + mw / 2, my + 20, "Kitchen", "sans500", 12.5, T.MUTED, anchor="middle")
        for k, (wd, c) in enumerate([(104, T.GREEN), (82, T.AMBER), (120, T.GREEN)]):
            ry_ = my + 48 + k * 30
            with d.rv("right", 1.9 + k * 0.18):
                d.add(f'<rect x="{mx + 16}" y="{ry_}" width="150" height="24" rx="8" fill="{T.RAISED}"/>')
                d.add(f'<circle cx="{mx + 30}" cy="{ry_ + 12}" r="4" fill="{c}"/>')
                d.add(f'<rect x="{mx + 44}" y="{ry_ + 9}" width="{wd * .8:g}" height="6" rx="3" fill="{T.RAISED_2}"/>')
        for k, hh in enumerate([34, 52, 40, 66, 48]):
            with d.rv("growy", 2.2 + k * 0.1):
                d.add(f'<rect x="{mx + 184 + k * 13}" y="{my + 132 - hh}" width="8" height="{hh}" rx="3" fill="{T.CYAN}" fill-opacity="{.35 + k * .1:.2f}"/>')
        d.add("</g>")

    # phone: the screen the code builds
    px, py, pw, ph = 930, 34, 220, 452
    with d.rv("right", 0.45):
        d.add(f'<g {d.float_(6, 6.8, 0)}>')
        g = d.gradient("pg", 0, 0, 1, 1)
        d.add(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="38" fill="#0e0e10" stroke="{g}" stroke-width="1.6"/>')
        d.add(f'<rect x="{px + 8}" y="{py + 8}" width="{pw - 16}" height="{ph - 16}" rx="31" fill="{T.BG}"/>')
        d.add(f'<rect x="{px + 80}" y="{py + 16}" width="60" height="18" rx="9" fill="#050506"/>')
        d.text(px + 24, py + 68, "New order", "sans600", 17, T.INK)
        d.text(px + 198, py + 67, "3 items", "sans500", 13, T.MUTED, anchor="end")
        items = [("Wrap", "EGP 180", T.CYAN), ("Fries", "EGP 95", T.AMBER), ("Cola", "EGP 210", T.VIOLET_L)]
        for k, (nm, pr, col) in enumerate(items):
            y = py + 92 + k * 56
            with d.rv("right", 1.5 + k * 0.5):
                d.add(f'<rect x="{px + 18}" y="{y}" width="184" height="48" rx="14" fill="{T.RAISED}" stroke="{T.LINE_SOFT}"/>')
                d.add(f'<rect x="{px + 26}" y="{y + 8}" width="32" height="32" rx="10" fill="{col}" fill-opacity=".22" stroke="{col}" stroke-opacity=".5"/>')
                d.text(px + 68, y + 21, nm, "sans500", 14, T.INK)
                d.text(px + 68, y + 38, "Qty 1", "sans400", 12, T.MUTED)
                d.text(px + 194, y + 29, pr, "sans600", 13, T.INK, anchor="end")
        d.add(f'<path d="M{px + 20} {py + 268}H{px + 200}" stroke="{T.LINE}" stroke-dasharray="3 4"/>')
        with d.rv("up", 3.0):
            d.text(px + 22, py + 294, "Total", "sans500", 14, T.MUTED)
            d.text(px + 198, py + 300, "EGP 485", "sans700", 24, T.INK, anchor="end", ls=-.5)
        gp = d.gradient("pay", 0, 0, 1, 0)
        # Pay -> pressed -> Paid
        press = u("press")
        d.css.append(f"@keyframes {press}{{0%,{P(3.8):.3f}%{{transform:scale(1)}}{P(3.95):.3f}%{{transform:scale(.93)}}"
                     f"{P(4.2):.3f}%,100%{{transform:scale(1)}}}}")
        with d.rv("pop", 3.3, until=4.2):
            d.add(f'<g class="{u("rv")}" style="transform-box:fill-box;transform-origin:50% 50%;animation:{press} {LOOP:g}s ease-in-out infinite">')
            d.add(f'<rect x="{px + 20}" y="{py + 322}" width="180" height="50" rx="15" fill="{gp}"/>')
            d.text(px + 110, py + 353, "Pay", "sans600", 17, T.BG, anchor="middle")
            d.add("</g>")
        with d.rv("pop", 4.3):
            d.add(f'<rect x="{px + 20}" y="{py + 322}" width="180" height="50" rx="15" fill="{T.GREEN}"/>')
            d.add(f'<path d="M{px + 78} {py + 347}l7 7 13 -14" fill="none" stroke="{T.BG}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
            d.text(px + 112, py + 353, "Paid", "sans600", 17, T.BG)
        with d.rv("up", 5.2):
            d.add(f'<circle cx="{px + 62}" cy="{py + 396}" r="4" fill="{T.GREEN}" class="{u("pulse")}"/>')
            d.text(px + 74, py + 401, "Receipt sent to printer", "sans500", 12, T.MUTED)
        d.add(f'<rect x="{px + 80}" y="{py + ph - 22}" width="60" height="4" rx="2" fill="{T.FAINT}"/>')
        d.add("</g>")

    if compact:
        d.add("</g>")
    return d.render()


if __name__ == "__main__":
    print(len(build()))
