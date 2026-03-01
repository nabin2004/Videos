# 🆕 Create a New Manim Studio Project

This guide walks you from zero to a running project in under 5 minutes.

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | ≥ 3.9 | [python.org](https://python.org) |
| Manim Community | ≥ 0.18 | `pip install manim` |
| LaTeX (optional) | any | `sudo apt install texlive-full` |
| Fonts | Inter, Space Grotesk, JetBrains Mono | Google Fonts / system |

---

## Step 1 — Scaffold the project

```bash
# Create and enter directory
mkdir my-manim-project && cd my-manim-project

# Recommended layout
my-manim-project/
├── brand.py            # Color / brand constants  ← copy from MASTER_PROMPT
├── typography.py       # Font helpers             ← copy from MASTER_PROMPT
├── layout.py           # Grid / positions         ← copy from MASTER_PROMPT
├── animations.py       # Reusable animation fns   ← copy from MASTER_PROMPT
├── scenes/             # One file per scene
│   └── intro.py
├── assets/
│   ├── fonts/
│   ├── images/
│   └── audio/
├── output/             # Rendered videos (git-ignored)
├── manim.cfg           # Render config
└── README.md
```

---

## Step 2 — Copy the brand files

Copy `brand.py`, `typography.py`, `layout.py`, and `animations.py` exactly from the **MASTER_PROMPT.md** into your project root.

---

## Step 3 — Create `manim.cfg`

```ini
[CLI]
quality         = high_quality
fps             = 60
background_color= #0A0E1A
preview         = True
media_dir       = ./output
```

---

## Step 4 — Create your first scene

```bash
# Copy the Scene Architecture template into scenes/intro.py
# (see MASTER_PROMPT.md → Scene Architecture Pattern)
touch scenes/intro.py
```

Paste the template and rename the class to `IntroScene`.

---

## Step 5 — Render & preview

```bash
# Fast draft preview
manim -pql scenes/intro.py IntroScene

# Full HD production render
manim -pqh --fps 60 scenes/intro.py IntroScene
```

Your rendered video appears in `./output/videos/`.

---

## Step 6 — Add to `.gitignore`

```
output/
__pycache__/
*.pyc
.DS_Store
media/
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: brand` | Run manim from the project root, not from `scenes/` |
| Font not found | Install fonts system-wide or pass absolute path |
| LaTeX errors | Use `MathTex` fallback or install `texlive-full` |
| Black background instead of brand color | Check `manim.cfg` or add `self.camera.background_color = BG` in `setup()` |
