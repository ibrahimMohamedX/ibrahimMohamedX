"""Featured-work cards. Each card carries a small illustration of its own
product (peeking up from the card's edge) so the six cards read as six
different things rather than one template repeated.

Motion is tied to content: HR ERP's chart re-grows, the ERP card prints a
slip, the portfolio card flips between English (LTR) and Arabic (RTL).
"""
import tokens as T
from svgkit import Doc, measure, pulse_css, status, tag, wrap

HUES = {"hr": T.VIOLET, "pos": T.CYAN, "erp": T.AMBER, "rasha": T.CORAL, "stylish": T.GREEN, "site": T.SKY}


# ------------------------------------------------------------------ shell
def shell(uid, w, h, title, desc_txt, hue, state, tags, text_w, wide, link_hint, pad_l=0, pad_r=0, text_x=None):
    d = Doc(uid, w, h, title, desc=desc_txt, bg=T.SURFACE, pad_l=pad_l, pad_r=pad_r)
    pulse_css(d)
    g = d.glow("hue", hue, 0.20)
    left = text_x is not None and text_x > w / 2
    if wide and left:
        d.add(f'<circle cx="300" cy="{h * .55:g}" r="360" fill="{g}"/>')
    elif wide:
        d.add(f'<circle cx="{w - 300}" cy="{h * .55:g}" r="360" fill="{g}"/>')
    else:
        d.add(f'<circle cx="{w * .6:g}" cy="{h}" r="330" fill="{g}"/>')
    pad = text_x if text_x is not None else (48 if not wide else 56)
    status(d, pad, 62, state[0], state[1], pulse=state[2])
    size = 34 if wide else 32
    d.text(pad - 2, 62 + 54, title, "sans600", size, T.INK, ls=-0.6)
    y = 62 + 54 + 40
    for ln in wrap(desc_txt, "sans400", 18, text_w):
        d.text(pad, y, ln, "sans400", 18, T.BODY)
        y += 28
    x = pad
    ty = y + 6
    for t in tags:
        x += tag(d, x, ty, t, T.BODY, h=30, size=15) + 8
    return d, ty + 30


def win(d, x, y, w, h, hue=None, r=18, bar=True, fill="#0e0e10"):
    d.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{T.LINE}"/>')
    if bar:
        d.add(f'<path d="M{x} {y + 38}H{x + w}" stroke="{T.LINE_SOFT}"/>')
        for k in range(3):
            d.add(f'<circle cx="{x + 20 + k * 15}" cy="{y + 19}" r="4.2" fill="{T.FAINT}" fill-opacity=".6"/>')


def bar(d, x, y, w, h=8, fill=T.RAISED_2, op=1):
    d.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{h / 2:g}" fill="{fill}" fill-opacity="{op}"/>')


def rail(d, x, y, h, hue, n=5, w=58):
    d.add(f'<path d="M{x + w} {y}V{y + h}" stroke="{T.LINE_SOFT}"/>')
    for k in range(n):
        f = hue if k == 0 else T.RAISED_2
        d.add(f'<rect x="{x + 17}" y="{y + 18 + k * 36}" width="24" height="24" rx="7" fill="{f}" fill-opacity="{.9 if k == 0 else 1}"/>')


def phone(d, x, y, w, hue, body, h=420):
    d.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="#0e0e10" stroke="{T.LINE}" stroke-width="1.5"/>')
    d.add(f'<rect x="{x + w / 2 - 28}" y="{y + 10}" width="56" height="16" rx="8" fill="{T.BG}"/>')
    body(d, x, y)


# ------------------------------------------------------------ illustrations
def ill_hr(d, ox, oy, hue):
    u = d.i
    d.add_css(
        f".{u('b')}{{transform-box:fill-box;transform-origin:50% 100%;animation:{u('grow')} 9s cubic-bezier(.2,.8,.2,1) infinite}}"
        f"@keyframes {u('grow')}{{0%{{transform:scaleY(.05)}}14%,86%{{transform:scaleY(1)}}100%{{transform:scaleY(1)}}}}")
    d.reduced_motion(f".{u('b')}{{animation:none!important}}")
    W_, H_ = 532, 420
    win(d, ox, oy, W_, H_, hue)
    d.add(f'<rect x="{ox + W_ - 134}" y="{oy + 10}" width="116" height="20" rx="10" fill="{T.RAISED}" stroke="{T.LINE}"/>')
    d.add(f'<circle cx="{ox + W_ - 122}" cy="{oy + 20}" r="6" fill="{hue}"/>')
    bar(d, ox + W_ - 108, oy + 17, 60, 6, T.RAISED_2)
    rail(d, ox, oy + 38, H_ - 38, hue)
    for k, name in enumerate(["Employees", "Attendance", "Leave", "Payroll"]):
        x = ox + 76 + k * 108
        d.add(f'<rect x="{x}" y="{oy + 60}" width="98" height="80" rx="12" fill="{T.RAISED}" stroke="{T.LINE_SOFT}"/>')
        d.text(x + 12, oy + 82, name, "sans500", 12.5, T.MUTED)
        bar(d, x + 12, oy + 96, 46, 16, T.RAISED_2)
        d.add(f'<path d="M{x + 12} {oy + 130}l14 -8 12 4 14 -10 14 3 18 -9" fill="none" stroke="{hue}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    # chart
    d.add(f'<rect x="{ox + 76}" y="{oy + 156}" width="262" height="190" rx="12" fill="{T.RAISED}" stroke="{T.LINE_SOFT}"/>')
    bar(d, ox + 92, oy + 172, 80, 8, T.RAISED_2)
    base = oy + 328
    for k, hh in enumerate([54, 82, 66, 104, 90, 120, 74, 98]):
        d.add(f'<rect class="{u("b")}" style="animation-delay:{k * 0.06:.2f}s" x="{ox + 94 + k * 29}" y="{base - hh}" width="16" height="{hh}" rx="5" fill="{hue}" fill-opacity="{.35 + .08 * (k % 4)}"/>')
    d.add(f'<path d="M{ox + 90} {base + 1}H{ox + 324}" stroke="{T.LINE}"/>')
    # attendance list
    d.add(f'<rect x="{ox + 352}" y="{oy + 156}" width="164" height="190" rx="12" fill="{T.RAISED}" stroke="{T.LINE_SOFT}"/>')
    for k, c in enumerate([T.GREEN, T.GREEN, T.AMBER, T.GREEN]):
        ry = oy + 180 + k * 38
        d.add(f'<circle cx="{ox + 376}" cy="{ry}" r="11" fill="{T.RAISED_2}"/>')
        bar(d, ox + 396, ry - 7, 60, 7, T.RAISED_2)
        bar(d, ox + 396, ry + 5, 36, 5, T.LINE)
        d.add(f'<circle cx="{ox + 500}" cy="{ry}" r="4" fill="{c}"/>')


def ill_pos(d, ox, oy, hue):
    W_ = 492
    win(d, ox, oy, W_, 300, hue)
    d.add(f'<path d="M{ox + 300} {oy + 38}V{oy + 300}" stroke="{T.LINE_SOFT}"/>')
    for k, (a, b) in enumerate([(130, 48), (96, 56), (150, 44), (110, 52)]):
        ry = oy + 58 + k * 44
        d.add(f'<rect x="{ox + 20}" y="{ry}" width="32" height="32" rx="9" fill="{T.RAISED_2}"/>')
        bar(d, ox + 64, ry + 5, a, 8)
        bar(d, ox + 64, ry + 21, a * .5, 5, T.RAISED)
        bar(d, ox + 276 - b, ry + 11, b, 8)
    for k in range(6):
        cx = ox + 320 + (k % 3) * 52
        cy = oy + 58 + (k // 3) * 46
        d.add(f'<rect x="{cx}" y="{cy}" width="44" height="38" rx="10" fill="{T.RAISED}" stroke="{T.LINE_SOFT}"/>')
    g = d.gradient("pay", 0, 0, 1, 0, stops=[(0, T.CYAN), (1, "#6ee7f9")])
    d.add(f'<rect x="{ox + 320}" y="{oy + 158}" width="148" height="44" rx="12" fill="{g}"/>')
    d.text(ox + 394, oy + 186, "Pay", "sans600", 16, T.BG, anchor="middle")
    for k, (lab, c) in enumerate([("Cashier", hue), ("Kitchen", T.AMBER)]):
        d.add(f'<circle cx="{ox + 322 + k * 80}" cy="{oy + 228}" r="4" fill="{c}"/>')
        d.text(ox + 333 + k * 80, oy + 233, lab, "sans500", 13, T.MUTED)


def ill_erp(d, ox, oy, hue):
    u = d.i
    d.add_css(
        f".{u('slip')}{{animation:{u('slip')} 7s linear infinite}}"
        f"@keyframes {u('slip')}{{0%,8%{{transform:translateY(-46px)}}40%,88%{{transform:translateY(0);animation-timing-function:steps(7,end)}}100%{{transform:translateY(0);opacity:0}}}}")
    d.add_def(f'<clipPath id="{u("slipclip")}"><rect x="{ox + 330}" y="{oy + 120}" width="140" height="200"/></clipPath>')
    d.reduced_motion(f".{u('slip')}{{animation:none!important}}")
    W_ = 492
    win(d, ox, oy, W_, 300, hue)
    rail(d, ox, oy + 38, 262, hue, n=4, w=50)
    for k, c in enumerate(["Present", "Present", "Late", "Present"]):
        ry = oy + 58 + k * 40
        d.add(f'<rect x="{ox + 66}" y="{ry - 6}" width="248" height="34" rx="10" fill="{T.RAISED}" stroke="{T.LINE_SOFT}"/>')
        d.add(f'<circle cx="{ox + 88}" cy="{ry + 11}" r="9" fill="{T.RAISED_2}"/>')
        bar(d, ox + 106, ry + 6, 74, 7)
        col = T.AMBER if c == "Late" else T.GREEN
        d.add(f'<circle cx="{ox + 226}" cy="{ry + 11}" r="3.5" fill="{col}"/>')
        d.text(ox + 237, ry + 16, c, "sans500", 12.5, T.MUTED)
    # printer + slip
    d.add(f'<rect x="{ox + 336}" y="{oy + 70}" width="128" height="40" rx="12" fill="{T.RAISED}" stroke="{T.LINE}"/>')
    d.add(f'<rect x="{ox + 348}" y="{oy + 92}" width="104" height="5" rx="2.5" fill="{T.BG}"/>')
    d.add(f'<g clip-path="url(#{u("slipclip")})"><g class="{u("slip")}">')
    d.add(f'<rect x="{ox + 354}" y="{oy + 97}" width="92" height="120" fill="{T.PAPER}"/>')
    for k, wd in enumerate([60, 48, 56, 40, 52]):
        d.add(f'<rect x="{ox + 364}" y="{oy + 110 + k * 14}" width="{wd}" height="4" rx="2" fill="{T.PAPER_MUTED}" fill-opacity=".6"/>')
    d.add("</g></g>")
    d.text(ox + 400, oy + 250, "USB  Bluetooth  Network", "sans500", 12.5, T.MUTED, anchor="middle")


def ill_rasha(d, ox, oy, hue):
    def a(d, x, y):
        bar(d, x + 18, y + 40, 92, 8, T.RAISED_2)
        d.add(f'<rect x="{x + 18}" y="{y + 60}" width="{164}" height="30" rx="15" fill="{T.RAISED}" stroke="{T.LINE_SOFT}"/>')
        for k in range(2):
            gy = y + 108 + k * 118
            g = d.gradient(f"r{k}", 0, 0, 1, 1, stops=[(0, hue), (1, T.VIOLET if k == 0 else T.AMBER)])
            d.add(f'<rect x="{x + 18}" y="{gy}" width="164" height="104" rx="16" fill="{g}" fill-opacity=".85"/>')
            d.add(f'<rect x="{x + 18}" y="{gy + 70}" width="164" height="34" rx="0" fill="#000" fill-opacity=".28"/>')
            bar(d, x + 30, gy + 82, 70, 8, "#fff", .85)
            d.add(f'<circle cx="{x + 164}" cy="{gy + 20}" r="11" fill="#000" fill-opacity=".3"/>')
    def b(d, x, y):
        g = d.gradient("rd", 0, 0, 0, 1, stops=[(0, hue), (1, T.VIOLET)])
        d.add(f'<rect x="{x + 10}" y="{y + 36}" width="180" height="112" rx="22" fill="{g}" fill-opacity=".85"/>')
        bar(d, x + 18, y + 164, 110, 10, T.RAISED_2)
        bar(d, x + 18, y + 184, 150, 6, T.RAISED)
        for k in range(3):
            d.add(f'<rect x="{x + 18 + k * 60}" y="{y + 206}" width="52" height="34" rx="10" fill="{T.RAISED}" stroke="{T.LINE_SOFT}"/>')
    phone(d, ox, oy, 200, hue, a)
    phone(d, ox + 224, oy + 34, 200, hue, b)


def ill_stylish(d, ox, oy, hue):
    def a(d, x, y):
        bar(d, x + 18, y + 40, 70, 8, T.RAISED_2)
        d.add(f'<circle cx="{x + 172}" cy="{y + 44}" r="10" fill="{T.RAISED}" stroke="{T.LINE_SOFT}"/>')
        d.add(f'<circle cx="{x + 178}" cy="{y + 38}" r="4" fill="{hue}"/>')
        for k in range(4):
            cx = x + 18 + (k % 2) * 86
            cy = y + 66 + (k // 2) * 124
            tone = [hue, T.SKY, T.CORAL, T.AMBER][k]
            d.add(f'<rect x="{cx}" y="{cy}" width="78" height="92" rx="14" fill="{tone}" fill-opacity=".22" stroke="{tone}" stroke-opacity=".35"/>')
            bar(d, cx + 4, cy + 100, 50, 6, T.RAISED_2)
            bar(d, cx + 4, cy + 112, 28, 6, T.RAISED)
    def b(d, x, y):
        d.add(f'<rect x="{x + 10}" y="{y + 36}" width="180" height="150" rx="22" fill="{hue}" fill-opacity=".20" stroke="{hue}" stroke-opacity=".4"/>')
        bar(d, x + 18, y + 204, 120, 12, T.RAISED_2)
        bar(d, x + 18, y + 226, 70, 8, T.RAISED)
        d.add(f'<rect x="{x + 18}" y="{y + 250}" width="164" height="40" rx="14" fill="{hue}"/>')
        d.text(x + 100, y + 276, "Add to cart", "sans600", 14, T.BG, anchor="middle")
    phone(d, ox, oy, 200, hue, a)
    phone(d, ox + 224, oy + 34, 200, hue, b)


def ill_site(d, ox, oy, hue):
    u = d.i
    d.add_css(
        f".{u('en')}{{animation:{u('en')} 8s ease-in-out infinite}}.{u('ar')}{{animation:{u('ar')} 8s ease-in-out infinite}}"
        f".{u('thumb')}{{animation:{u('thumb')} 8s ease-in-out infinite}}"
        f"@keyframes {u('en')}{{0%,44%{{opacity:1}}50%,94%{{opacity:0}}100%{{opacity:1}}}}"
        f"@keyframes {u('ar')}{{0%,44%{{opacity:0}}50%,94%{{opacity:1}}100%{{opacity:0}}}}"
        f"@keyframes {u('thumb')}{{0%,44%{{transform:translateX(0)}}50%,94%{{transform:translateX(26px)}}100%{{transform:translateX(0)}}}}")
    d.reduced_motion(f".{u('en')},.{u('ar')},.{u('thumb')}{{animation:none!important}}.{u('ar')}{{opacity:0}}")
    W_ = 532
    win(d, ox, oy, W_, 260, hue)
    d.add(f'<rect x="{ox + 150}" y="{oy + 10}" width="260" height="20" rx="10" fill="{T.RAISED}"/>')
    bar(d, ox + 166, oy + 17, 90, 6, T.FAINT, .5)
    # language toggle
    tx, ty = ox + W_ - 96, oy + 8
    d.add(f'<rect x="{tx}" y="{ty}" width="62" height="24" rx="12" fill="{T.RAISED}" stroke="{T.LINE}"/>')
    d.add(f'<circle class="{u("thumb")}" cx="{tx + 14}" cy="{ty + 12}" r="9" fill="{hue}"/>')
    d.text(tx + 27, ty + 16.5, "EN", "sans600", 11, T.MUTED, anchor="middle", opacity=.0)
    # LTR content
    d.add(f'<g class="{u("en")}">')
    d.add(f'<rect x="{ox + 40}" y="{oy + 74}" width="250" height="26" rx="8" fill="{T.INK}" fill-opacity=".92"/>')
    d.add(f'<rect x="{ox + 40}" y="{oy + 110}" width="190" height="26" rx="8" fill="{T.INK}" fill-opacity=".92"/>')
    bar(d, ox + 40, oy + 156, 300, 8); bar(d, ox + 40, oy + 172, 240, 8)
    d.add(f'<rect x="{ox + 40}" y="{oy + 200}" width="110" height="34" rx="17" fill="{hue}"/>')
    for k in range(3):
        d.add(f'<rect x="{ox + 352}" y="{oy + 74 + k * 56}" width="140" height="44" rx="12" fill="{T.RAISED}" stroke="{T.LINE_SOFT}"/>')
    d.add("</g>")
    # RTL content (mirrored)
    d.add(f'<g class="{u("ar")}" opacity="0">')
    r = ox + W_ - 40
    d.add(f'<rect x="{r - 250}" y="{oy + 74}" width="250" height="26" rx="8" fill="{T.INK}" fill-opacity=".92"/>')
    d.add(f'<rect x="{r - 190}" y="{oy + 110}" width="190" height="26" rx="8" fill="{T.INK}" fill-opacity=".92"/>')
    bar(d, r - 300, oy + 156, 300, 8); bar(d, r - 240, oy + 172, 240, 8)
    d.add(f'<rect x="{r - 110}" y="{oy + 200}" width="110" height="34" rx="17" fill="{hue}"/>')
    for k in range(3):
        d.add(f'<rect x="{ox + 40}" y="{oy + 74 + k * 56}" width="140" height="44" rx="12" fill="{T.RAISED}" stroke="{T.LINE_SOFT}"/>')
    d.add("</g>")


# ------------------------------------------------------------------ cards
ILL_W = {"ill_hr": 532, "ill_pos": 492, "ill_erp": 492, "ill_rasha": 424, "ill_stylish": 424, "ill_site": 532}


def wide(uid, title, desc, hue, state, tags, ill, ill_y, h=340, tw=470, side="R"):
    left = side == "L"
    d, _ = shell(uid, T.W, h, title, desc, hue, state, tags, tw, True, None, text_x=640 if left else None)
    iw = ILL_W[ill.__name__]
    base = 56 if left else 620
    ill(d, base + (532 - iw) // 2, ill_y, hue)
    return d.render()


ILL_W = {"ill_hr": 532, "ill_pos": 492, "ill_erp": 492, "ill_rasha": 424, "ill_stylish": 424, "ill_site": 532}


def wide(uid, title, desc, hue, state, tags, ill, ill_y, h=340, tw=470, side="R"):
    left = side == "L"
    d, _ = shell(uid, T.W, h, title, desc, hue, state, tags, tw, True, None, text_x=640 if left else None)
    iw = ILL_W[ill.__name__]
    base = 56 if left else 620
    ill(d, base + (532 - iw) // 2, ill_y, hue)
    return d.render()


def half(uid, title, desc, hue, state, tags, ill, ill_y=282, h=470, side="L"):
    # 24-unit gutter baked into the canvas: left card gets it on the right, right card on the left
    d, _ = shell(uid, T.W_HALF, h, title, desc, hue, state, tags, T.W_HALF - 96, False, None,
                 pad_l=T.GAP if side == "R" else 0, pad_r=T.GAP if side == "L" else 0)
    ill(d, 48 if ill not in (ill_rasha, ill_stylish) else 70, ill_y, hue)
    return d.render()


CARDS = [
    ("work-hr-erp.svg", lambda: wide(
        "wh", "Archai HR ERP",
        "Multi-company HR platform. One central project manages companies and subscriptions; every customer gets its own Supabase project. Employees, attendance, leave and payroll are complete.",
        HUES["hr"], ("Completed", T.GREEN, False), ["React", "TypeScript", "Supabase", "Vite"], ill_hr, 46, h=360, tw=480)),
    ("work-futurex-pos.svg", lambda: wide(
        "wp", "FutureX POS",
        "Cashier and kitchen flows, orders and checks, mixed payment methods, role-based permissions and receipt printing.",
        HUES["pos"], ("Completed, private company code", T.GREEN, False), ["Flutter", "Cubit", "Dio"], ill_pos, 50, h=340, tw=470, side="L")),
    ("work-futurex-erp.svg", lambda: wide(
        "we", "FutureX ERP",
        "Business ERP with a ShellRoute app shell, attendance-based access and a layered thermal-printing module over USB, Bluetooth and network.",
        HUES["erp"], ("In development, private company code", T.AMBER, True), ["Flutter", "GoRouter", "Cubit"], ill_erp, 50, h=340, tw=470)),
    ("work-rasha7ly.svg", lambda: wide(
        "wr", "Rasha7ly",
        "Travel recommendation app with personalized destination suggestions, image browsing and an animated interface.",
        HUES["rasha"], ("Public repository", T.MUTED, False), ["Flutter", "MVVM", "Firebase"], ill_rasha, 46, h=340, tw=470, side="L")),
    ("work-stylish.svg", lambda: wide(
        "ws", "Stylish",
        "E-commerce app with 20+ screens built from Figma designs and structured with Clean Architecture.",
        HUES["stylish"], ("Public repository", T.MUTED, False), ["Flutter", "Cubit", "Clean Architecture"], ill_stylish, 46, h=340, tw=470)),
    ("work-portfolio.svg", lambda: wide(
        "wo", "Portfolio",
        "Bilingual personal website in English and Arabic, built with React and Vite.",
        HUES["site"], ("Live at himego.vercel.app", T.CYAN, True), ["React", "Vite", "Supabase"], ill_site, 44, h=300, tw=440, side="L")),
]


# ------------------------------------------------- compact (phone) cards
SM_ILL = {  # illustration -> (x, y, scale)
    ill_hr: (48, 0, 504 / 532), ill_site: (48, 0, 504 / 532),
    ill_pos: (54, 292, 1.0), ill_erp: (54, 292, 1.0),
    ill_rasha: (88, 292, 1.0), ill_stylish: (88, 292, 1.0),
}


def compact(uid, title, desc, hue, state, tags, ill, peek=190):
    """Phone variant: text on top, the illustration starts below the tag row
    (so long copy can never collide with it) and peeks up from the bottom edge."""
    from svgkit import wrap as _wrap
    lines = len(_wrap(desc, "sans400", 18, T.W_SM - 96))
    bottom = 62 + 54 + 40 + lines * 28 + 6 + 30
    y = bottom + 30
    h = y + peek
    d, _ = shell(uid, T.W_SM, h, title, desc, hue, state, tags, T.W_SM - 96, False, None)
    x, _y, s = SM_ILL[ill]
    d.add(f'<g transform="translate({x} {y}) scale({s:.4f}) translate({-x} {-y})">')
    ill(d, x, y, hue)
    d.add("</g>")
    return d.render()


SM_SPECS = [
    ("work-hr-erp.svg", "sh", "Archai HR ERP",
     "Multi-company HR platform. One central project manages companies and subscriptions; every customer gets its own Supabase project. Employees, attendance, leave and payroll are complete.",
     HUES["hr"], ("Completed", T.GREEN, False), ["React", "TypeScript", "Supabase", "Vite"], ill_hr, 230),
    ("work-futurex-pos.svg", "sp", "FutureX POS",
     "Cashier and kitchen flows, orders and checks, mixed payment methods, role-based permissions and receipt printing.",
     HUES["pos"], ("Completed, private company code", T.GREEN, False), ["Flutter", "Cubit", "Dio"], ill_pos, 190),
    ("work-futurex-erp.svg", "se", "FutureX ERP",
     "Business ERP with a ShellRoute app shell, attendance-based access and a layered thermal-printing module over USB, Bluetooth and network.",
     HUES["erp"], ("In development, private company code", T.AMBER, True), ["Flutter", "GoRouter", "Cubit"], ill_erp, 190),
    ("work-rasha7ly.svg", "sr", "Rasha7ly",
     "Travel recommendation app with personalized destination suggestions, image browsing and an animated interface.",
     HUES["rasha"], ("Public repository", T.MUTED, False), ["Flutter", "MVVM", "Firebase"], ill_rasha, 190),
    ("work-stylish.svg", "ss", "Stylish",
     "E-commerce app with 20+ screens built from Figma designs and structured with Clean Architecture.",
     HUES["stylish"], ("Public repository", T.MUTED, False), ["Flutter", "Cubit", "Clean Architecture"], ill_stylish, 190),
    ("work-portfolio.svg", "so", "Portfolio",
     "Bilingual personal website in English and Arabic, built with React and Vite.",
     HUES["site"], ("Live at himego.vercel.app", T.CYAN, True), ["React", "Vite", "Supabase"], ill_site, 190),
]


def sm_cards():
    return {fn: compact(uid, title, desc, hue, st, tags, ill, peek=h)
            for fn, uid, title, desc, hue, st, tags, ill, h in SM_SPECS}
