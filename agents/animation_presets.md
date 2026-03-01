# 🎞️ Animation Presets

`animations.py` provides a library of reusable, brand-consistent animations. Import everything with:

```python
from animations import *
```

---

## Timing constants

| Constant | Duration | Use when |
|----------|----------|----------|
| `FAST`   | 0.35 s | Micro-interactions, button presses |
| `NORMAL` | 0.60 s | Standard transitions |
| `SLOW`   | 1.00 s | Scene-level transitions, emphasis |
| `EPIC`   | 1.80 s | Hero reveals, logo stings |

---

## Easing curves

| Constant | Feel | Use for |
|----------|------|---------|
| `EASE_OUT` | Decelerates | Entrances — objects landing |
| `EASE_IN` | Accelerates | Exits — objects leaving |
| `EASE_IO` | S-curve | Pans, camera moves |
| `SPRING` | Slight overshoot | Poppy, energetic reveals |
| `SMOOTH_` | Manim default | Generic fallback |

```python
# Always pass rate_func explicitly
self.play(mob.animate(rate_func=EASE_OUT, run_time=NORMAL).shift(UP))
```

---

## Entrance animations

### `fly_in(mob, direction=DOWN)`
Object slides in from a direction while fading up from transparent.

```python
title = brand_title("Hello World")
self.play(fly_in(title, direction=LEFT))
```

### `pop_in(mob)`
Object scales from 0 with a spring overshoot — great for icons and metric cards.

```python
card = metric_card("Revenue", "$4.2M")
self.play(pop_in(card))
```

### `type_on(mob)`
Typewriter letter-by-letter reveal — use on `Text` objects only.

```python
headline = brand_text("Loading data...")
self.play(type_on(headline))
```

---

## Emphasis animations

### `pulse(mob, scale=1.12)`
Scale up and back — draws attention to a specific element.

```python
self.play(pulse(kpi_number, scale=1.15))
```

### `glow_stroke(mob, color, width)`
Returns a glowing copy to layer beneath the original.

```python
glow = glow_stroke(title, color=ACCENT, width=10)
self.add(glow)
self.add(title)
```

---

## Transition

### `scene_wipe(scene, direction=LEFT)`
Full-screen bar wipe — use between major scene sections.

```python
scene_wipe(self, direction=UP)
# then build the next content section
```

---

## Decorative helpers

### `make_grid(rows, cols, color, opacity)`
Subtle background grid — always add in `_build_bg()`.

```python
self.add(make_grid(opacity=0.12))
```

### `make_particles(n, color, radius, seed)`
Floating dot field — adds depth and energy to backgrounds.

```python
self.add(make_particles(n=60, color=ACCENT, radius=0.025))
```

---

## Staggered group reveals

Use Manim's built-in `LaggedStart` with brand timings:

```python
items = VGroup(card1, card2, card3)
self.play(
    LaggedStart(
        *[fly_in(c, direction=DOWN) for c in items],
        lag_ratio=0.25,
        run_time=SLOW
    )
)
```
