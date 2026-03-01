# 🧩 Standard UI Elements

All elements below are defined in `animations.py`. Import with `from animations import *`.

---

## Callout Box

A branded info box with an icon and text body.

```python
box = callout("This is an important note", icon="💡", accent=ACCENT)
box.move_to(POS_CENTER)
self.play(FadeIn(box, shift=UP*0.3))
```

**Parameters**

| Param | Default | Description |
|-------|---------|-------------|
| `text` | — | Body text string |
| `icon` | `"→"` | Left icon character or emoji |
| `accent` | `ACCENT` | Border and icon color |
| `width` | `6` | Box width in Manim units |

---

## Metric Card

A KPI card showing a large value with label.

```python
card = metric_card("Monthly Revenue", "$4.2M", unit="USD", accent=BRAND_SOLAR)
self.play(pop_in(card))
```

**Layout** (auto-arranged inside the card):
```
┌──────────────────┐
│   $4.2M  USD     │
│  Monthly Revenue │
└──────────────────┘
```

---

## Progress Bar

Animated fill bar — animate the fill width after creation:

```python
bar = progress_bar(0, width=8, label="Progress", accent=ACCENT)
self.add(bar)
# Animate to 75%
fill = bar[1]  # index 1 = the fill rectangle
self.play(fill.animate.set_width(8 * 0.75).align_to(bar[0], LEFT),
          run_time=SLOW, rate_func=EASE_OUT)
```

---

## Divider Line

Subtle horizontal rule between content sections.

```python
rule = divider(color=ACCENT, width=10)
rule.move_to(DOWN * 1.5)
self.play(GrowFromCenter(rule))
```

---

## Neon Glow Text

Layered glow effect — good for hero titles and logo treatments.

```python
glowing = neon_text("MANIM STUDIO", color=ACCENT, size=T_HERO)
glowing.move_to(POS_CENTER)
self.play(FadeIn(glowing))
```

The returned `VGroup` has 3 layers: `[glow_wide, glow_tight, text]`.  
Animate them separately for flicker effects:

```python
self.play(glowing[0].animate.set_opacity(0.05),
          glowing[1].animate.set_opacity(0.15),
          run_time=FAST)
```

---

## Bullet List

```python
def bullet_list(items, accent=ACCENT, gap=0.55):
    rows = VGroup()
    for item in items:
        dot  = Dot(radius=0.06, color=accent)
        text = brand_text(item, size=T_BODY)
        row  = VGroup(dot, text).arrange(RIGHT, buff=0.2)
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=gap)
    return rows

# Usage
bullets = bullet_list(["Fast rendering", "Brand-consistent", "Reusable"])
self.play(LaggedStart(*[FadeIn(r, shift=RIGHT*0.2) for r in bullets],
                       lag_ratio=0.2))
```

---

## Section Header

```python
def section_header(title, subtitle=""):
    t = brand_title(title, color=ACCENT).move_to(POS_TITLE)
    s = brand_text(subtitle, color=TEXT_DIM).next_to(t, DOWN, buff=U2)
    rule = divider().next_to(s, DOWN, buff=U)
    return VGroup(t, s, rule)

# Usage
header = section_header("Chapter 2", "The Architecture")
self.play(fly_in(header[0]), Write(header[1]), GrowFromCenter(header[2]),
          lag_ratio=0.3)
```

---

## Lower Third (broadcast-style)

```python
def lower_third(name, title, accent=ACCENT):
    bar   = Rectangle(width=5.5, height=0.06,
                      fill_color=accent, fill_opacity=1, stroke_width=0)
    name_ = brand_text(name,  size=T_H2,    color=TEXT).next_to(bar, UP, buff=0.12, aligned_edge=LEFT)
    title_= brand_text(title, size=T_BODY,  color=TEXT_DIM).next_to(bar, DOWN, buff=0.12, aligned_edge=LEFT)
    group = VGroup(bar, name_, title_)
    group.to_corner(DL, buff=U4)
    return group

# Usage
lt = lower_third("Jane Smith", "Head of Engineering")
self.play(FadeIn(lt, shift=UP*0.3))
self.wait(3)
self.play(FadeOut(lt, shift=DOWN*0.3))
```
