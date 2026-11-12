#!/usr/bin/env python3
"""Render README.md the way GitHub lays it out (dark or light) for visual QA.

    pip install markdown
    python scripts/build_preview.py [dark|light] [out.html]

Images are referenced as files, exactly like <img> on GitHub, so embedded
fonts and CSS animations are tested through the same code path.
"""
import os
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES = {
    "dark": dict(bg="#0d1117", fg="#e6edf3", mut="#9198a1", line="#3d444d", link="#4493f8"),
    "light": dict(bg="#ffffff", fg="#1f2328", mut="#59636e", line="#d1d9e0", link="#0969da"),
}


def main():
    theme = sys.argv[1] if len(sys.argv) > 1 else "dark"
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, ".preview", f"{theme}.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    t = THEMES[theme]
    md = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    body = markdown.markdown(md, extensions=["md_in_html"])
    css = f"""
    body{{margin:0;background:{t['bg']};color:{t['fg']};font:16px/1.5 -apple-system,'Segoe UI',Helvetica,Arial,sans-serif}}
    .wrap{{max-width:888px;margin:0 auto;padding:32px 16px 64px;box-sizing:border-box}}
    h2{{font-size:24px;font-weight:600;padding-bottom:.3em;border-bottom:1px solid {t['line']};margin:24px 0 16px}}
    a{{color:{t['link']};text-decoration:none}} img{{max-width:100%;vertical-align:middle}}
    sub{{color:{t['mut']};font-size:12px}} summary{{cursor:pointer}}
    """
    html = (f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Profile preview ({theme})</title><style>{css}</style><div class="wrap">{body}</div>')
    # make asset paths absolute so the preview works from .preview/
    html = html.replace('src="assets/', f'src="file://{ROOT}/assets/').replace('srcset="assets/', f'srcset="file://{ROOT}/assets/')
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(out)


if __name__ == "__main__":
    main()
