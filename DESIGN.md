# Design notes

## Rebuild
```bash
pip install fonttools brotli
python scripts/build_assets.py              # banner, work cards, stack, experience, contact, buttons (+ assets/sm/)
python scripts/generate_stats.py <user>     # assets/github.svg (+ sm/); add --snapshot to run offline
pip install markdown && python scripts/build_preview.py dark   # local preview
python scripts/qa_render.py out/ assets/banner.svg@0.5,3,9     # screenshots at animation times (needs playwright)
```
The GitHub Action (`.github/workflows/update-stats.yml`) runs both build scripts daily.

## System
- All colours, fonts and radii live in `scripts/tokens.py`. Re-skinning = edit that file and rebuild.
- Field `#0b0b0c` is the theme-color published by himego.vercel.app. Cyan to violet is the brand gradient carried over from the previous profile.
- Type: IBM Plex Sans + IBM Plex Sans Arabic (OFL, see `scripts/fonts/OFL.txt`). Plex Mono appears only inside the printed receipt.
- Fonts are subset per SVG and embedded as base64 woff2, so each asset is self-contained (GitHub renders README SVGs through `<img>`, where external fonts cannot load).
- No scripts, no external requests, no `foreignObject`. Verified by the build checks in the PR notes.

## Responsive
Every asset has a desktop version (1200 wide) and a compact one in `assets/sm/` (600 wide, single column,
larger relative type). The README swaps them with `<picture><source media="(max-width: 640px)">`.
If a viewer strips `<source>`, the desktop asset is shown, which still works, just smaller.

## Motion
- Hero: a POS window, the Print button is pressed, a receipt feeds out in 19 discrete steps (like a thermal printer). 18s loop.
- Hero roles rotate every 4s. Status dots pulse. HR ERP chart re-grows. ERP card prints a slip. Portfolio card flips EN (LTR) / AR (RTL).
- The un-animated state of every asset is the finished composition. `prefers-reduced-motion` turns every animation off.
