#!/usr/bin/env python3
"""Build every static SVG in assets/. Run from the repo root:

    pip install fonttools brotli
    python scripts/build_assets.py
"""
import os

import banner
import sections
import work
from svgkit import save

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")


def main():
    os.makedirs(OUT, exist_ok=True)
    files = {"banner.svg": banner.build(), "stack.svg": sections.stack(),
             "experience.svg": sections.experience(), "contact.svg": sections.contact()}
    files.update({fn: f() for fn, f in work.CARDS})
    files.update(sections.buttons())
    sm = {"banner.svg": banner.build(compact=True), "stack.svg": sections.stack_sm(),
          "experience.svg": sections.experience_sm(), "contact.svg": sections.contact_sm()}
    sm.update(work.sm_cards())
    os.makedirs(os.path.join(OUT, "sm"), exist_ok=True)
    for name, svg in sm.items():
        files["sm/" + name] = svg
    total = 0
    for name, svg in sorted(files.items()):
        n = save(os.path.join(OUT, name), svg)
        total += n
        print(f"{name:26s}{n / 1024:7.1f} KB")
    print(f"{'total':26s}{total / 1024:7.1f} KB")


if __name__ == "__main__":
    main()
