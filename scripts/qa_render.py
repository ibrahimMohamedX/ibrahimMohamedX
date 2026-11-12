#!/usr/bin/env python3
"""QA: render SVG assets in headless Chromium at chosen animation times.

    python scripts/qa_render.py out_dir file.svg[@t1,t2,...] ...

Each SVG is inlined in a page (so its CSS animations can be paused and
seeked via the Web Animations API) and screenshotted at 2x.
Requires: pip install playwright && playwright install chromium
"""
import os
import sys

from playwright.sync_api import sync_playwright


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    jobs = []
    for a in sys.argv[2:]:
        path, _, ts = a.partition("@")
        jobs.append((path, [float(t) for t in ts.split(",")] if ts else [None]))
    with sync_playwright() as p:
        b = p.chromium.launch()
        for path, times in jobs:
            svg = open(path, encoding="utf-8").read()
            import re
            w, h = map(float, re.search(r'width="([\d.]+)" height="([\d.]+)"', svg).groups())
            pg = b.new_page(viewport={"width": int(w), "height": int(h)}, device_scale_factor=1)
            pg.set_content(f'<body style="margin:0;background:#2b2b30">{svg}</body>')
            pg.wait_for_timeout(400)
            for t in times:
                if t is not None:
                    pg.evaluate("""t => { document.getAnimations().forEach(a => {a.pause(); a.currentTime = t*1000;});
                        document.querySelectorAll('svg').forEach(s => { s.pauseAnimations(); s.setCurrentTime(t); }); }""", t)
                    pg.wait_for_timeout(120)
                name = os.path.splitext(os.path.basename(path))[0] + ("" if t is None else f"_t{t:g}") + ".png"
                pg.screenshot(path=os.path.join(out, name))
                print("shot", name)
            pg.close()
        b.close()


if __name__ == "__main__":
    main()
