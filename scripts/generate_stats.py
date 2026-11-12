#!/usr/bin/env python3
"""Generate assets/github.svg (numbers + language mix) from the GitHub REST API.

Standard library + the local SVG kit only. Uses GITHUB_TOKEN / GH_TOKEN when present.

    python scripts/generate_stats.py <github-username>
    python scripts/generate_stats.py --snapshot      # offline, uses the last known numbers
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime

import tokens as T
from svgkit import Doc, measure, save

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
API = "https://api.github.com"

# last numbers published in the previous profile; used for --snapshot / API failures
SNAPSHOT = {
    "repos": 31, "stars": 0, "commits": 193, "followers": 1, "since": 2022,
    "langs": {"TypeScript": 523, "JavaScript": 204, "Dart": 100, "CSS": 74, "C++": 46, "CMake": 37},
}

LANG_COLORS = {
    "Dart": "#2dd4bf", "TypeScript": "#60a5fa", "JavaScript": "#fbbf24", "CSS": "#a78bfa",
    "HTML": "#fb7185", "Kotlin": "#c084fc", "Swift": "#fb923c", "Python": "#38bdf8",
    "C++": "#f472b6", "C": "#94a3b8", "CMake": "#64748b", "Java": "#f59e0b", "Shell": "#86efac",
    "PHP": "#818cf8", "C#": "#4ade80",
}
EXTRA = ["#22d3ee", "#34d399", "#e879f9", "#facc15"]


def get(path, params=None):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"})
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect(user):
    profile = get(f"/users/{user}")
    repos, page = [], 1
    while True:
        batch = get(f"/users/{user}/repos", {"per_page": 100, "type": "owner", "page": page})
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"]]
    langs = {}
    for r in own[:100]:
        try:
            for k, v in get(f"/repos/{user}/{r['name']}/languages").items():
                langs[k] = langs.get(k, 0) + v
        except Exception:
            pass
    try:
        commits = get("/search/commits", {"q": f"author:{user}", "per_page": 1}).get("total_count")
    except Exception:
        commits = None
    return {
        "repos": profile.get("public_repos", len(own)),
        "stars": sum(r["stargazers_count"] for r in own),
        "followers": profile.get("followers", 0),
        "commits": commits if commits is not None else SNAPSHOT["commits"],
        "since": datetime.strptime(profile["created_at"], "%Y-%m-%dT%H:%M:%SZ").year,
        "langs": langs or SNAPSHOT["langs"],
    }


def fmt(n):
    return f"{n:,}"


def _langs(data):
    langs = {k: v for k, v in data["langs"].items() if k.lower() != "html"}
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    return top, total


def github_svg(data, compact=False):
    W, H = (T.W_SM, 470) if compact else (T.W, 330)
    m = 32 if compact else 48
    d = Doc("ghs" if compact else "gh", W, H,
            "GitHub in numbers: public repositories, commits, stars, followers and top languages", bg=T.SURFACE)
    d.set_loop(12.0)
    d.add(f'<g {d.drift(-30, 20, 15)}><circle cx="{W - 80}" cy="0" r="320" fill="{d.glow("gl", T.VIOLET, .16)}"/></g>')
    d.shine(0, 0, W, H, delay=2, period=10)

    cells = [("Public repositories", data["repos"]), ("Public commits", data["commits"]),
             ("Stars earned", data["stars"]), ("Followers", data["followers"])]
    colw = (W - 96) / 4
    for k, (label, val) in enumerate(cells):
        if compact:
            x, y = 32 + (k % 2) * 270, 76 + (k // 2) * 100
            size, ly = 56, y + 28
        else:
            x, y = 48 + k * colw, 92
            size, ly = 64, 128
        with d.rv("up", 0.2 + k * 0.13):
            d.text(x, y, fmt(val), "sans700", size, T.INK, ls=-2 if not compact else -1.5)
            d.text(x + 2, ly, label, "sans500", 17 if compact else 18, T.MUTED)
        if k and not compact:
            with d.rv("growy", 0.3 + k * 0.13):
                d.add(f'<path d="M{x - 20:g} 50V134" stroke="{T.LINE_SOFT}"/>')
    ry = 258 if compact else 168
    with d.rv("growx", 0.7):
        d.add(f'<path d="M{m} {ry}H{W - m}" stroke="{T.LINE_SOFT}"/>')

    top, total = _langs(data)
    ty, by, bh = (296, 312, 14) if compact else (208, 228, 16)
    with d.rv("up", 0.9):
        d.text(m, ty, "Languages by code size", "sans600", 19 if compact else 20, T.INK)
        d.text(W - m, ty, f"Since {data['since']}" if compact else f"On GitHub since {data['since']}",
               "sans400", 15 if compact else 16, T.MUTED, anchor="end")
    bw = W - 2 * m
    d.add(f'<rect x="{m}" y="{by}" width="{bw}" height="{bh}" rx="{bh / 2}" fill="{T.RAISED_2}"/>')
    clip = d.i("barclip")
    d.add_def(f'<clipPath id="{clip}"><rect x="{m}" y="{by}" width="{bw}" height="{bh}" rx="{bh / 2}"/></clipPath>')
    d.add(f'<g clip-path="url(#{clip})">')
    x, cols = m, []
    for i, (name, v) in enumerate(top):
        c = LANG_COLORS.get(name, EXTRA[i % len(EXTRA)])
        cols.append(c)
        wd = bw * v / total
        with d.rv("growx", 1.0 + i * 0.12):
            d.add(f'<rect x="{x:.1f}" y="{by}" width="{max(wd - 3, 2):.1f}" height="{bh}" fill="{c}"/>')
        x += wd
    d.add("</g>")
    for i, (name, v) in enumerate(top):
        if compact:
            px, py = 32 + (i % 2) * 270, 372 + (i // 2) * 32
        else:
            px, py = 48 + i * (W - 96) / max(len(top), 1), 284
        with d.rv("pop", 1.3 + i * 0.1):
            d.add(f'<circle cx="{px + 6:g}" cy="{py - 5 if compact else py - 6}" r="6" fill="{cols[i]}"/>')
            d.text(px + 20, py, name, "sans500", 17 if compact else 18, T.INK)
            pct = f"{v / total * 100:.1f}%"
            if compact:
                d.text(px + 20 + measure(name, "sans500", 17) + 8, py, pct, "sans400", 15, T.MUTED)
            else:
                d.text(px + 20, py + 24, pct, "sans400", 16, T.MUTED)
    return d.render()


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--snapshot" in sys.argv or not args:
        data = SNAPSHOT
    else:
        try:
            data = collect(args[0])
        except Exception as e:  # keep the previous asset rather than fail the workflow
            sys.exit(f"stats collection failed, keeping existing asset: {e}")
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "sm"), exist_ok=True)
    n = save(os.path.join(OUT, "github.svg"), github_svg(data))
    n2 = save(os.path.join(OUT, "sm", "github.svg"), github_svg(data, compact=True))
    print("github.svg", n, "bytes; sm/github.svg", n2, "bytes")
