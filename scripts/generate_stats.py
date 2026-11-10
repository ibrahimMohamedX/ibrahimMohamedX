#!/usr/bin/env python3
"""Generate assets/stats.svg and assets/languages.svg from the GitHub REST API.

Standard library only. Uses GITHUB_TOKEN / GH_TOKEN when present (recommended in Actions).
Usage: python scripts/generate_stats.py <github-username> [--placeholder]
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from card_style import *  # noqa: E402,F401,F403

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
API = "https://api.github.com"
W, H = 490, 230

LANG_COLORS = {
    "Dart": "#00B4AB", "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "HTML": "#e34c26",
    "CSS": "#8b5cf6", "Kotlin": "#A97BFF", "Swift": "#F05138", "Python": "#3572A5",
    "C++": "#f34b7d", "C": "#8a8a8a", "Java": "#b07219", "Shell": "#89e051", "PHP": "#4F5D95",
    "C#": "#178600", "Ruby": "#701516", "SCSS": "#c6538c", "Vue": "#41b883",
}


def get(path, params=None):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"}
    )
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
    stars = sum(r["stargazers_count"] for r in own)
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
        "stars": stars,
        "followers": profile.get("followers", 0),
        "commits": commits,
        "since": datetime.strptime(profile["created_at"], "%Y-%m-%dT%H:%M:%SZ").year,
        "langs": langs,
    }


def fmt(n):
    return "—" if n is None else f"{n:,}"


def stats_svg(d):
    rows = [
        ("Public repositories", fmt(d["repos"]) if d else "…"),
        ("Stars earned", fmt(d["stars"]) if d else "…"),
        ("Public commits", fmt(d["commits"]) if d else "…"),
        ("Followers", fmt(d["followers"]) if d else "…"),
        ("On GitHub since", str(d["since"]) if d else "…"),
    ]
    out = [
        card_open(W, H, "st", "GitHub overview"),
        f'<text x="28" y="44" font-family="{MONO}" font-size="12" fill="{CYAN}" letter-spacing="1.5">// GITHUB OVERVIEW</text>',
    ]
    y = 78
    for label, val in rows:
        out.append(f'<text x="28" y="{y}" font-family="{SANS}" font-size="14" fill="{MUTED}">{esc(label)}</text>')
        out.append(
            f'<text x="{W-28}" y="{y}" text-anchor="end" font-family="{SANS}" font-size="15" '
            f'font-weight="700" fill="{TEXT}">{esc(val)}</text>'
        )
        out.append(f'<line x1="28" y1="{y+10}" x2="{W-28}" y2="{y+10}" stroke="{BORDER}"/>')
        y += 28
    note = "Public repositories and public activity only" if d else "Syncing live stats. Updates automatically after the first push."
    out.append(f'<text x="28" y="{H-12}" font-family="{SANS}" font-size="11" fill="{MUTED}" opacity="0.8">{esc(note)}</text>')
    out.append("</svg>")
    return "".join(out)


def languages_svg(d):
    out = [
        card_open(W, H, "lg", "Top languages"),
        f'<text x="28" y="44" font-family="{MONO}" font-size="12" fill="{CYAN}" letter-spacing="1.5">// TOP LANGUAGES</text>',
    ]
    if not d or not d["langs"]:
        msg = "Syncing live stats. Updates automatically after the first push." if not d else "No language data yet"
        out.append(f'<text x="28" y="100" font-family="{SANS}" font-size="13" fill="{MUTED}">{esc(msg)}</text>')
    else:
        total = sum(d["langs"].values())
        top = sorted(d["langs"].items(), key=lambda kv: -kv[1])[:6]
        y = 76
        bar_x, bar_w = 130, W - 130 - 76
        for name, size in top:
            pct = size / total * 100
            color = LANG_COLORS.get(name, "#6b7280")
            out.append(f'<text x="28" y="{y+4}" font-family="{SANS}" font-size="13" fill="{TEXT}">{esc(name)}</text>')
            out.append(f'<rect x="{bar_x}" y="{y-6}" width="{bar_w}" height="10" rx="5" fill="#15122a"/>')
            out.append(f'<rect x="{bar_x}" y="{y-6}" width="{max(bar_w*pct/100, 6):.1f}" height="10" rx="5" fill="{color}"/>')
            out.append(
                f'<text x="{W-28}" y="{y+4}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">{pct:.1f}%</text>'
            )
            y += 26
    out.append(
        f'<text x="28" y="{H-16}" font-family="{SANS}" font-size="11" fill="{MUTED}" opacity="0.8">'
        f"By code size across public, non-fork repositories</text>"
    )
    out.append("</svg>")
    return "".join(out)


def write(name, content, out_dir=OUT):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: generate_stats.py <github-username> [--placeholder]")
    data = None if "--placeholder" in sys.argv else collect(sys.argv[1])
    write("stats.svg", stats_svg(data))
    write("languages.svg", languages_svg(data))
    print("stats written", "(placeholder)" if data is None else data)
