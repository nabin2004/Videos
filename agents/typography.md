# 🔤 Typography

All typography helpers live in `typography.py`.

---

## Font families

| Role | Font | Install |
|------|------|---------|
| UI / labels | **Inter** | [fonts.google.com/specimen/Inter](https://fonts.google.com/specimen/Inter) |
| Display / hero | **Space Grotesk** | [fonts.google.com/specimen/Space+Grotesk](https://fonts.google.com/specimen/Space+Grotesk) |
| Code / data | **JetBrains Mono** | [jetbrains.com/lp/mono](https://www.jetbrains.com/lp/mono/) |

Install fonts system-wide so Manim can find them, or use absolute paths:

```python
Text("Hello", font="/path/to/Inter-Regular.ttf")
```

---

## Type scale

| Token | Manim size | px equiv | Use |
|-------|-----------|----------|-----|
| `T_HERO` | 1.10 | ~53px | Main scene title |
| `T_H1` | 0.80 | ~38px | Section heading |
| `T_H2` | 0.60 | ~29px | Sub-heading |
| `T_BODY` | 0.42 | ~20px | Body copy, bullets |
| `T_CAPTION` | 0.32 | ~15px | Captions, footnotes |
| `T_LABEL` | 0.28 | ~13px | Axis labels, tiny UI |

---

## Helper functions

### `brand_text(content, size, color, font)`

General-purpose text — defaults to Inter, body size, ghost white.

```python
p = brand_text("Supporting copy here")
h = brand_text("Sub-heading", size=T_H2, color=ACCENT)
c = brand_text("Source: Internal data, 2024", size=T_CAPTION, color=TEXT_DIM)
```

### `brand_title(content, color)`

Hero display title — uses Space Grotesk Bold.

```python
t = brand_title("MANIM STUDIO")
t_colored = brand_title("Data Insights", color=ACCENT2)
```

### `brand_code(content)`

Code block with branded window background.

```python
snippet = brand_code("def hello():\n    return 'world'")
```

---

## Text alignment

```python
# Centered (default)
t = brand_text("Center").move_to(ORIGIN)

# Left-aligned block
block = VGroup(
    brand_title("Heading"),
    brand_text("Paragraph one"),
    brand_text("Paragraph two"),
).arrange(DOWN, aligned_edge=LEFT, buff=U2)
block.to_edge(LEFT, buff=U4)
```

---

## Inline color emphasis

Use `MarkupText` for mixed-color runs:

```python
mixed = MarkupText(
    f'Launch in <span fgcolor="{ACCENT}">Q3 2025</span>',
    font="Inter"
)
```

---

## Math / LaTeX

```python
formula = MathTex(r"\sum_{i=0}^{n} x_i", color=TEXT)
formula.set_color_by_tex("x_i", ACCENT)
```

For display equations, bump to `T_H1`:

```python
formula.scale(T_H1 / 0.5)  # Manim default MathTex is ~0.5 units
```
