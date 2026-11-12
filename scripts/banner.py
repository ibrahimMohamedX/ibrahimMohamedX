"""Hero banner.

One orchestrated moment: a POS window, the Print button is pressed, and a
thermal receipt feeds out of the printer in discrete steps (the way a real
printer advances paper). The receipt carries the facts. Everything else is
quiet. The default (un-animated) state is the finished composition, so
reduced-motion viewers and static renderers see the full banner.
"""
import tokens as T
from svgkit import Doc, measure, pulse_css, status

W, H = 1200, 520
LOOP = 18  # seconds


def zigzag(x, y, w, depth=7, step=10):
    pts, n = [f"M{x} {y}"], int(w // step)
    for k in range(n):
        pts.append(f"L{x + k * step + step / 2:g} {y + depth}")
        pts.append(f"L{x + (k + 1) * step:g} {y}")
    return " ".join(pts)


def barcode(x, y, w, h):
    # deterministic pseudo-barcode
    seq = [2, 1, 3, 1, 1, 2, 4, 1, 2, 2, 1, 3, 1, 2, 1, 1, 4, 2, 1, 3, 2, 1, 1, 2, 3, 1, 2, 4, 1, 1, 2, 1, 3, 2, 1]
    out, cx, on = [], x, True
    for s in seq:
        bw = s * 1.6
        if on and cx + bw <= x + w:
            out.append(f'<rect x="{cx:.1f}" y="{y}" width="{bw:.1f}" height="{h}" fill="{T.PAPER_INK}"/>')
        cx += bw + 1.4
        on = not on
        if cx > x + w:
            break
    return "".join(out)


def build(compact=False):
    W, H = (600, 840) if compact else (1200, 520)
    d = Doc("bn" + ("s" if compact else ""), W, H, "Ibrahim Mohamed, software engineer. Flutter mobile and desktop developer.",
            desc="Animated banner: a POS window prints a receipt listing Flutter, Windows desktop, Cubit/BLoC, Dio and Bluetooth, USB and network printing. Open to remote roles.",
            bg=T.BG, radius=T.R_HERO)
    u = d.i
    pulse_css(d)

    # ---- atmosphere
    glow_v = d.glow("gv", T.VIOLET, 0.34)
    glow_c = d.glow("gc", T.CYAN, 0.16)
    if compact:
        d.add(f'<circle cx="520" cy="560" r="420" fill="{glow_v}"/>')
        d.add(f'<circle cx="20" cy="40" r="300" fill="{glow_c}"/>')
    else:
        d.add(f'<circle cx="930" cy="150" r="420" fill="{glow_v}"/>')
        d.add(f'<circle cx="40" cy="560" r="360" fill="{glow_c}"/>')
    d.add_def(f'<pattern id="{u("dots")}" width="28" height="28" patternUnits="userSpaceOnUse">'
              f'<circle cx="2" cy="2" r="1.1" fill="#fff" fill-opacity=".10"/></pattern>')
    d.add_def(f'<radialGradient id="{u("fade")}" cx="0.72" cy="0.4" r="0.75">'
              f'<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>')
    d.add_def(f'<mask id="{u("m")}"><rect width="{W}" height="{H}" fill="url(#{u("fade")})"/></mask>')
    d.add(f'<rect width="{W}" height="{H}" fill="url(#{u("dots")})" mask="url(#{u("m")})"/>')

    # ---- left: identity
    if compact:
        lx, sy, n1, n2, ns, ry, ay, rs, as_ = 36, 66, 160, 240, 80, 300, 344, 28, 20
    else:
        lx, sy, n1, n2, ns, ry, ay, rs, as_ = 64, 104, 214, 310, 92, 372, 420, 31, 22
    status(d, lx, sy, "Open to remote roles from Egypt", T.GREEN, pulse=True, size=17)
    d.text(lx - 4, n1, "Ibrahim", "sans700", ns, T.INK, ls=-3)
    d.text(lx - 4, n2, "Mohamed", "sans700", ns, T.INK, ls=-3)

    grad = d.gradient("role", lx, 0, lx + 440, 0, units="userSpaceOnUse")
    roles = ["Software engineer", "Flutter mobile & desktop", "Founder of Archai Solutions"]
    for k, r in enumerate(roles):
        extra = f'style="animation-delay:{k * 4}s"' if k else 'style="animation-delay:0s"'
        d.text(lx, ry, r, "sans500", rs, grad, cls="role", opacity=1 if k == 0 else 0,
               extra=extra + (f' id="{d.i("role0")}"' if k == 0 else ""))
    d.text(lx, ay, "مهندس برمجيات · مطوّر تطبيقات الموبايل والديسكتوب", "ar400", as_, T.MUTED)

    # ---- right: POS window (compact: the whole composition moves below the text)
    if compact:
        d.add('<g transform="translate(51 388) scale(0.9) translate(-650 -44)">')
    wx, wy, ww, wh = 650, 44, 484, 206
    d.add(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="16" fill="{T.SURFACE}" stroke="{T.LINE}"/>')
    d.add(f'<path d="M{wx} {wy + 36}H{wx + ww}" stroke="{T.LINE_SOFT}"/>')
    for k, c in enumerate([T.FAINT] * 3):
        d.add(f'<circle cx="{wx + 20 + k * 16}" cy="{wy + 18}" r="4.5" fill="{c}" fill-opacity=".7"/>')
    d.text(wx + ww / 2, wy + 23, "Orders", "sans500", 14, T.MUTED, anchor="middle")
    # rail
    d.add(f'<path d="M{wx + 56} {wy + 36}V{wy + wh}" stroke="{T.LINE_SOFT}"/>')
    for k in range(4):
        fill = T.VIOLET if k == 0 else T.RAISED_2
        op = ".9" if k == 0 else "1"
        d.add(f'<rect x="{wx + 16}" y="{wy + 52 + k * 36}" width="24" height="24" rx="7" fill="{fill}" fill-opacity="{op}"/>')
    # order rows
    for k, (a, b) in enumerate([(140, 44), (112, 52), (132, 40)]):
        ry = wy + 54 + k * 46
        d.add(f'<rect x="{wx + 76}" y="{ry}" width="34" height="34" rx="9" fill="{T.RAISED_2}"/>')
        d.add(f'<rect x="{wx + 124}" y="{ry + 6}" width="{a}" height="8" rx="4" fill="{T.RAISED_2}"/>')
        d.add(f'<rect x="{wx + 124}" y="{ry + 22}" width="{a * .55:g}" height="6" rx="3" fill="{T.RAISED}"/>')
        d.add(f'<rect x="{wx + 316 - b}" y="{ry + 12}" width="{b}" height="8" rx="4" fill="{T.RAISED_2}"/>')
    # summary column
    sx = wx + 342
    d.add(f'<path d="M{sx - 10} {wy + 36}V{wy + wh}" stroke="{T.LINE_SOFT}"/>')
    d.add(f'<rect x="{sx + 6}" y="{wy + 54}" width="60" height="8" rx="4" fill="{T.RAISED_2}"/>')
    d.add(f'<rect x="{sx + 6}" y="{wy + 72}" width="104" height="14" rx="5" fill="{T.RAISED_2}"/>')
    g = d.gradient("btn", 0, 0, 1, 0)
    d.add(f'<g class="{u("press")}"><rect x="{sx + 6}" y="{wy + 124}" width="124" height="46" rx="13" fill="{g}"/>')
    d.text(sx + 68, wy + 153, "Print receipt", "sans600", 15, T.BG, anchor="middle")
    d.add("</g>")

    # ---- printer
    py = wy + wh - 10
    d.add(f'<rect x="742" y="{py}" width="300" height="34" rx="12" fill="{T.RAISED}" stroke="{T.LINE}"/>')
    sy = py + 20
    d.add(f'<rect x="760" y="{sy}" width="264" height="6" rx="3" fill="{T.BG}"/>')
    d.add(f'<rect class="{u("slot")}" x="760" y="{sy}" width="264" height="6" rx="3" fill="{T.CYAN}" opacity="0"/>')
    d.add(f'<circle cx="1018" cy="{py + 10}" r="3" fill="{T.GREEN}"/>')

    # ---- receipt (clipped below the slot, fed downward)
    rx, rw = 772, 240
    top = sy + 6
    rh = 226
    full = rh + 12
    # The clip grows in discrete steps (CSS), like paper advancing in a thermal printer.
    # Default state = fully revealed, so static renderers and reduced-motion viewers see everything.
    d.add_def(
        f'<clipPath id="{u("feed")}"><rect class="{u("feedclip")}" x="700" y="{top}" width="400" height="{full}"/></clipPath>')
    d.add(f'<g clip-path="url(#{u("feed")})"><g class="{u("receipt")}">')
    # paper body + torn edge (drawn right-to-left)
    n = int(rw // 10)
    edge = " ".join(f"L{rx + rw - k * 10 - 5:g} {top + rh + 7} L{rx + rw - (k + 1) * 10:g} {top + rh}" for k in range(n))
    d.add(f'<path d="M{rx} {top}H{rx + rw}V{top + rh} {edge} Z" fill="{T.PAPER}"/>')
    d.add(f'<rect x="{rx}" y="{top}" width="{rw}" height="14" fill="#000" fill-opacity=".12"/>')  # slot shadow
    cx = rx + rw / 2
    d.text(cx, top + 36, "IBRAHIM MOHAMED", "mono500", 15, T.PAPER_INK, anchor="middle", ls=0.6)
    d.text(cx, top + 54, "software engineer", "mono400", 12.5, T.PAPER_MUTED, anchor="middle")
    d.add(f'<path d="M{rx + 16} {top + 68}H{rx + rw - 16}" stroke="{T.PAPER_MUTED}" stroke-dasharray="3 4"/>')
    rows = [("Mobile", "Flutter"), ("Desktop", "Windows"), ("State", "Cubit/BLoC"),
            ("Network", "Dio"), ("Printing", "USB/BT/LAN")]
    for k, (a, b) in enumerate(rows):
        y = top + 90 + k * 19
        d.text(rx + 16, y, a, "mono400", 13, T.PAPER_INK)
        d.text(rx + rw - 16, y, b, "mono500", 13, T.PAPER_INK, anchor="end")
        lw = measure(a, "mono400", 13)
        rw_ = measure(b, "mono500", 13)
        x1, x2 = rx + 16 + lw + 6, rx + rw - 16 - rw_ - 6
        d.add(f'<path d="M{x1:g} {y - 3}H{x2:g}" stroke="{T.PAPER_MUTED}" stroke-opacity=".55" stroke-dasharray="1 4" stroke-linecap="round"/>')
    d.add(f'<path d="M{rx + 16} {top + 172}H{rx + rw - 16}" stroke="{T.PAPER_MUTED}" stroke-dasharray="3 4"/>')
    d.text(rx + 16, top + 192, "OPEN TO REMOTE", "mono500", 13, T.PAPER_INK, ls=0.4)
    ck = rx + rw - 32
    d.add(f'<path d="M{ck} {top + 187}l5 5 10 -11" fill="none" stroke="{T.PAPER_INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    d.add(barcode(rx + 16, top + 202, rw - 32, 14))
    d.add("</g></g>")

    if compact:
        d.add("</g>")

    # ---- motion
    L = LOOP
    d.add_css(
        f".{u('role')}{{animation:{u('role')} 12s ease-in-out infinite}}"
        f"@keyframes {u('role')}{{0%{{opacity:0;transform:translateY(12px)}}4%,29%{{opacity:1;transform:translateY(0)}}"
        f"33%,100%{{opacity:0;transform:translateY(-12px)}}}}"
        f".{u('press')}{{transform-box:fill-box;transform-origin:center;animation:{u('press')} {L}s ease-in-out infinite}}"
        f"@keyframes {u('press')}{{0%,2%{{transform:scale(1);filter:none}}3.2%{{transform:scale(.94)}}5%,100%{{transform:scale(1)}}}}"
        f".{u('receipt')}{{animation:{u('fade')} {L}s linear infinite}}"
        f"@keyframes {u('fade')}{{0%,92%{{opacity:1}}96%,100%{{opacity:0}}}}"
        f".{u('feedclip')}{{animation:{u('feedclip')} {L}s linear infinite}}"
        f"@keyframes {u('feedclip')}{{0%,5%{{height:0;animation-timing-function:steps(19,end)}}29%,95.9%{{height:{full}px}}96%,100%{{height:0}}}}"
        f".{u('slot')}{{animation:{u('slot')} {L}s linear infinite}}"
        f"@keyframes {u('slot')}{{0%,5%{{opacity:0}}6%,28%{{opacity:.9}}30%,100%{{opacity:0}}}}"
    )
    d.reduced_motion(
        f".{u('role')},.{u('press')},.{u('receipt')},.{u('slot')},.{u('feedclip')},.{u('pulse')}{{animation:none!important}}"
        f".{u('role')}{{opacity:0}}#{u('role0')}{{opacity:1}}")
    return d.render()


if __name__ == "__main__":
    print(len(build()))
