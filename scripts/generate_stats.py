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


def github_svg(data, compact=False):
    if compact:
        return github_svg_sm(data)
    W, H = T.W, 330
    d = Doc("gh", W, H, "GitHub in numbers: public repositories, commits, stars, followers and top languages", bg=T.SURFACE)
    d.add(f'<circle cx="{W - 80}" cy="0" r="340" fill="{d.glow("gl", T.VIOLET, .16)}"/>')

    cells = [("Public repositories", data["repos"]), ("Public commits", data["commits"]),
             ("Stars earned", data["stars"]), ("Followers", data["followers"])]
    colw = (W - 96) / 4
    for k, (label, val) in enumerate(cells):
        x = 48 + k * colw
        d.text(x, 92, fmt(val), "sans700", 64, T.INK, ls=-2)
        d.text(x + 2, 128, label, "sans500", 18, T.MUTED)
        if k:
            d.add(f'<path d="M{x - 20:g} 50V134" stroke="{T.LINE_SOFT}"/>')
    d.add(f'<path d="M48 168H{W - 48}" stroke="{T.LINE_SOFT}"/>')

    langs = {k: v for k, v in data["langs"].items() if k.lower() != "html"}
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    shown = sum(v for _, v in top)
    d.text(48, 208, "Languages by code size", "sans600", 20, T.INK)
    bx, bw, by = 48, W - 96, 228
    clip = d.i("barclip")
    d.add_def(f'<clipPath id="{clip}"><rect x="{bx}" y="{by}" width="{bw}" height="16" rx="8"/></clipPath>')
    d.add(f'<rect x="{bx}" y="{by}" width="{bw}" height="16" rx="8" fill="{T.RAISED_2}"/>')
    d.add(f'<g clip-path="url(#{clip})">')
    x, cols = bx, []
    for i, (name, v) in enumerate(top):
        c = LANG_COLORS.get(name, EXTRA[i % len(EXTRA)])
        cols.append(c)
        w = bw * v / total
        d.add(f'<rect x="{x:.1f}" y="{by}" width="{max(w - 3, 2):.1f}" height="16" fill="{c}"/>')
        x += w
    d.add("</g>")
    lx, ly = 48, 284
    slot = (W - 96) / max(len(top), 1)
    for i, (name, v) in enumerate(top):
        px = 48 + i * slot
        d.add(f'<circle cx="{px + 6:g}" cy="{ly - 6}" r="6" fill="{cols[i]}"/>')
        d.text(px + 20, ly, name, "sans500", 18, T.INK)
        d.text(px + 20, ly + 24, f"{v / total * 100:.1f}%", "sans400", 16, T.MUTED)
    d.text(W - 48, 208, f"On GitHub since {data['since']}", "sans400", 16, T.MUTED, anchor="end")
    return d.render()


def github_svg_sm(data):
    W, H = T.W_SM, 470
    d = Doc("ghs", W, H, "GitHub in numbers: public repositories, commits, stars, followers and top languages", bg=T.SURFACE)
    d.add(f'<circle cx="{W}" cy="0" r="260" fill="{d.glow("gl", T.VIOLET, .16)}"/>')
    cells = [("Public repositories", data["repos"]), ("Public commits", data["commits"]),
             ("Stars earned", data["stars"]), ("Followers", data["followers"])]
    for k, (label, val) in enumerate(cells):
        x = 32 + (k % 2) * 270
        y = 76 + (k // 2) * 100
        d.text(x, y, fmt(val), "sans700", 56, T.INK, ls=-1.5)
        d.text(x + 2, y + 28, label, "sans500", 17, T.MUTED)
    d.add(f'<path d="M32 258H{W - 32}" stroke="{T.LINE_SOFT}"/>')
    langs = {k: v for k, v in data["langs"].items() if k.lower() != "html"}
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    d.text(32, 296, "Languages by code size", "sans600", 19, T.INK)
    bx, bw, by = 32, W - 64, 312
    clip = d.i("barclip")
    d.add_def(f'<clipPath id="{clip}"><rect x="{bx}" y="{by}" width="{bw}" height="14" rx="7"/></clipPath>')
    d.add(f'<rect x="{bx}" y="{by}" width="{bw}" height="14" rx="7" fill="{T.RAISED_2}"/>')
    d.add(f'<g clip-path="url(#{clip})">')
    x, cols = bx, []
    for i, (name, v) in enumerate(top):
        c = LANG_COLORS.get(name, EXTRA[i % len(EXTRA)])
        cols.append(c)
        wd = bw * v / total
        d.add(f'<rect x="{x:.1f}" y="{by}" width="{max(wd - 3, 2):.1f}" height="14" fill="{c}"/>')
        x += wd
    d.add("</g>")
    for i, (name, v) in enumerate(top):
        px = 32 + (i % 2) * 270
        py = 372 + (i // 2) * 32
        d.add(f'<circle cx="{px + 6}" cy="{py - 5}" r="6" fill="{cols[i]}"/>')
        d.text(px + 20, py, f"{name}", "sans500", 17, T.INK)
        d.text(px + 20 + measure(name, "sans500", 17) + 8, py, f"{v / total * 100:.1f}%", "sans400", 15, T.MUTED)
    d.text(W - 32, 296, f"Since {data['since']}", "sans400", 15, T.MUTED, anchor="end")
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
