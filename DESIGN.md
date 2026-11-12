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
README SVGs are shown through `<img>`, so scroll-triggered animation (IntersectionObserver) is not possible on GitHub.
Instead every asset runs a shared timeline (12 s; hero 14 s): elements enter one after another, hold, leave together, and replay.
Ambient motion runs continuously, so something is always alive when a section scrolls into view.

- Hero: Dart code types itself, the phone beside it builds the screen (order lines arrive, Pay is pressed, state flips to Paid), a Windows "Kitchen" app and Flutter/Dart/Cubit chips float.
- Cards: status, title, copy and tags arrive in order; the illustration slides in and builds itself (bars grow, sparklines draw, rows slide, tiles pop); light sweep; drifting glow.
- Stack: labels slide in, chips pop in sequence, Flutter and Dart pulse. Experience: line draws, nodes pop, a light travels down the timeline; ongoing roles pulse, the completed degree is a solid green check.
- GitHub numbers: figures rise in turn, language bar segments grow. Contact: headline rises, email underline draws. Buttons: pop in, icons float, sheen sweep.
- The un-animated state of every asset is the finished composition. `prefers-reduced-motion` turns all animation off.
- Motion API lives in `scripts/svgkit.py` (`Doc.rv`, `Doc.draw`, `Doc.idle`, `Doc.shine`, `Doc.cover`).
