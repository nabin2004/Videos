# 🎨 Using Brand Colors

All colors live in **`brand.py`** — never hard-code hex values in scene files.

---

## Quick reference

| Token | Hex | Usage |
|-------|-----|-------|
| `BG` | `#0A0E1A` | Scene background |
| `ACCENT` | `#00F5FF` | Primary accent, titles, key data |
| `ACCENT2` | `#BF5AF2` | Secondary accent, sub-headings |
| `HILIGHT` | `#FF6B35` | CTA elements, warnings, hot data |
| `TEXT` | `#E8EAF0` | Body copy |
| `TEXT_DIM` | `#8892A4` | Captions, labels, secondary info |
| `PANEL` | `#1C2333` | Card / box backgrounds |
| `BRAND_SOLAR` | `#FFD60A` | Charts: positive / growth |
| `BRAND_STEEL` | `#2E3A50` | Borders, dividers, track fills |

---

## Importing

```python
from brand import *        # recommended — brings in everything
# or selectively:
from brand import ACCENT, TEXT, PANEL
```

---

## Applying colors

### Text
```python
# Body
label = Text("Hello", color=TEXT)

# Accent headline
title = Text("BIG TITLE", color=ACCENT, weight=BOLD)

# Dimmed caption
caption = Text("Source: ...", color=TEXT_DIM, font_size=14)
```

### Shapes
```python
box = RoundedRectangle(
    fill_color=PANEL, fill_opacity=1,
    stroke_color=ACCENT, stroke_width=1.5
)
```

### Gradients (via color_gradient)
```python
line = Line(LEFT*3, RIGHT*3)
line.set_color_by_gradient(*GRAD_ELECTRIC_PLASMA)
```

### Data series (charts / bars)
```python
for i, bar in enumerate(bars):
    bar.set_fill(DATA_COLORS[i % len(DATA_COLORS)])
```

---

## Do's and Don'ts

✅ **Do** — use semantic aliases (`ACCENT`, `TEXT`, `PANEL`)  
✅ **Do** — use `DATA_COLORS[n]` for sequential data series  
✅ **Do** — use `BRAND_SOLAR` for positive metrics, `HILIGHT` for negative  

❌ **Don't** — write `color="#00F5FF"` directly in scene files  
❌ **Don't** — invent new one-off colors; extend `brand.py` instead  
❌ **Don't** — use white (`WHITE`) — use `TEXT` (`#E8EAF0`) for softer contrast  

---

## Extending the palette

If you need a new color, add it to `brand.py` with a descriptive name and a comment explaining its purpose:

```python
BRAND_AURORA = "#00FF87"   # Special: bio / health data series
```
