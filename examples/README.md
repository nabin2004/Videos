# Examples

Runnable example scenes demonstrating every module in the **TheBoringAI** Manim toolkit.

## Quick Start

```bash
# From project root
source .venv/bin/activate

# Render a single example (low quality for speed)
manim -ql examples/01_brand_and_typography.py BrandShowcase

# Render all examples
make render-examples      # or manually:
for f in examples/*.py; do manim -ql "$f"; done
```

## Example Index

| # | File | Scene Class | What It Demonstrates |
|---|------|-------------|----------------------|
| 01 | `01_brand_and_typography.py` | `BrandShowcase` | Brand palette, typography helpers, math, code blocks |
| 02 | `02_animations_and_layout.py` | `AnimationsShowcase` | fly_in, pop_in, pulse, neon_text, grid, particles, callout, metric cards |
| 03 | `03_ml_components.py` | `MLComponentsShowcase` | Neural networks, matrices, tensors, activation plots, loss curves, ml_block, pipelines |
| 04 | `04_octopus_mascot.py` | `OctopusMascotShowcase` | OctopusCreature, moods, variations, holding items, teaching sequences |
| 05 | `05_video_components.py` | `VideoComponentsShowcase` | Opening, ChapterCard, PauseAndPonder, LowerThirds, Bumper, Watermark, SubscribeCTA, Closing |
| 06 | `06_full_mini_episode.py` | `MiniEpisode` | End-to-end mini episode combining everything: opening, octopus teaching, neural net, quiz, closing |

## Rendered Output

Videos land in `output/videos/` (configured in `manim.cfg`).

## Tips

- Use `-ql` for fast 480p preview, `-qh` for 1080p, `-qk` for 4K.
- Add `--format gif` for short loops.
- All examples are self-contained — each imports only from the project root modules.
