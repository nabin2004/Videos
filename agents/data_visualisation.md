# 📊 Data Visualisation

Guides for building brand-consistent charts and graphs.

---

## Color sequence for data series

Always use `DATA_COLORS` from `brand.py` in order:

```python
DATA_COLORS = [
    BRAND_ELECTRIC,  # series 1
    BRAND_PLASMA,    # series 2
    BRAND_NOVA,      # series 3
    BRAND_SOLAR,     # series 4
    "#39FF14",       # series 5
    "#FF073A",       # series 6
]
```

---

## Bar Chart

```python
from manim import BarChart

data   = [42, 78, 55, 91, 63]
labels = ["Q1", "Q2", "Q3", "Q4", "Q5"]

chart = BarChart(
    values=data,
    bar_names=labels,
    y_range=[0, 100, 20],
    y_length=5,
    x_length=9,
    bar_colors=DATA_COLORS[:len(data)],
    bar_stroke_width=0,
    x_axis_config={"font_size": int(T_LABEL*48), "color": TEXT_DIM},
    y_axis_config={"font_size": int(T_LABEL*48), "color": TEXT_DIM},
)
chart.move_to(ORIGIN)

# Animate bars growing from zero
self.play(
    chart.animate.change_bar_values(data),
    run_time=SLOW,
    rate_func=EASE_OUT
)
```

---

## Line Graph

```python
ax = Axes(
    x_range=[0, 10, 1],
    y_range=[0, 100, 20],
    x_length=10, y_length=5,
    axis_config={"color": BRAND_STEEL, "stroke_width": 1},
    tips=False,
)

points = [ax.c2p(x, y) for x, y in zip(range(11), [0,12,30,45,50,60,72,80,85,90,95])]
line = VMobject().set_points_smoothly(points).set_stroke(color=ACCENT, width=3)
dots = VGroup(*[Dot(p, color=ACCENT, radius=0.07) for p in points])

# Glow the line
glow = line.copy().set_stroke(color=ACCENT, width=10, opacity=0.2)

self.play(Create(ax), run_time=FAST)
self.play(Create(glow), Create(line), run_time=EPIC, rate_func=EASE_OUT)
self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08))
```

---

## Pie / Donut Chart

```python
def donut_chart(values, colors=None, inner_radius=0.8, outer_radius=2.0):
    if colors is None:
        colors = DATA_COLORS
    total = sum(values)
    sectors = VGroup()
    angle = PI/2  # start at top
    for val, col in zip(values, colors):
        sweep = (val / total) * TAU
        sector = AnnularSector(
            inner_radius=inner_radius,
            outer_radius=outer_radius,
            angle=sweep,
            start_angle=angle,
            fill_color=col,
            fill_opacity=1,
            stroke_width=0,
        )
        sectors.add(sector)
        angle -= sweep
    return sectors

# Usage
segments = donut_chart([30, 25, 20, 15, 10])
self.play(LaggedStart(*[GrowFromCenter(s) for s in segments], lag_ratio=0.15))
```

---

## Animated Counter (number roll-up)

```python
class CounterText(DecimalNumber):
    """Counts up from 0 to a value with brand styling."""

def animated_counter(target, prefix="", suffix="", color=ACCENT):
    num = DecimalNumber(0, num_decimal_places=0,
                        color=color, font_size=int(T_H1*48))
    num.add_updater(lambda m: m.set_value(m.get_value()))
    return num

# Usage in scene:
counter = animated_counter(4200000, prefix="$")
self.add(counter)
self.play(
    ChangeDecimalToValue(counter, 4200000),
    run_time=EPIC,
    rate_func=EASE_OUT
)
```

---

## Best practices

- Always label axes with `brand_text(..., size=T_LABEL, color=TEXT_DIM)`
- Add a subtle `make_grid()` behind charts for readability
- Animate data entrance — never just `self.add(chart)` without animation
- For before/after comparisons, use `ReplacementTransform` between two charts
