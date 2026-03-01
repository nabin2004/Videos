# 🎬 Manim Studio — Documentation Index

A production-grade animation system built on the [Manim Community](https://www.manim.community/) library, with consistent branding, reusable components, and media-quality render settings.

---

## 📁 Project structure

```
manim-studio/
├── MASTER_PROMPT.md     ← 🔑 Start here — copy into Claude to generate scenes
├── brand.py             ← Color palette & brand constants
├── typography.py        ← Font helpers & type scale
├── layout.py            ← Grid, positions, safe areas
├── animations.py        ← Reusable animation functions & UI elements
├── manim.cfg            ← Default render config
├── scenes/              ← One .py file per scene
└── docs/                ← You are here
    ├── README.md                 (this file)
    ├── create_new_project.md     ← How to scaffold a project
    ├── add_a_scene.md            ← How to add a new scene
    ├── using_brand_colors.md     ← Color system reference
    ├── typography.md             ← Font & text helpers
    ├── animation_presets.md      ← Timing, easing & animation helpers
    ├── standard_elements.md      ← UI components (cards, bars, callouts...)
    ├── data_visualisation.md     ← Charts, graphs, counters
    └── render_and_export.md      ← Quality flags, codecs, batch rendering
```

---

## 🚀 Quick start

```bash
# 1. Install Manim
pip install manim

# 2. Copy brand/typography/layout/animations .py files to project root

# 3. Create your first scene
cp scenes/_template.py scenes/my_scene.py

# 4. Preview
manim -pql scenes/my_scene.py MyScene
```

---

## 📖 Doc quick-links

| I want to… | Go to |
|-----------|-------|
| Start a brand new project | [`create_new_project.md`](create_new_project.md) |
| Add a new scene | [`add_a_scene.md`](add_a_scene.md) |
| Use or extend colors | [`using_brand_colors.md`](using_brand_colors.md) |
| Style text | [`typography.md`](typography.md) |
| Add animations & effects | [`animation_presets.md`](animation_presets.md) |
| Build UI elements | [`standard_elements.md`](standard_elements.md) |
| Make charts & graphs | [`data_visualisation.md`](data_visualisation.md) |
| Render for delivery | [`render_and_export.md`](render_and_export.md) |
| Generate scenes with AI | [`../MASTER_PROMPT.md`](../MASTER_PROMPT.md) |

---

## 🎨 Brand at a glance

| Token | Color | Hex |
|-------|-------|-----|
| Background | ![](https://via.placeholder.com/12/0A0E1A/0A0E1A) Midnight | `#0A0E1A` |
| Primary Accent | ![](https://via.placeholder.com/12/00F5FF/00F5FF) Electric Cyan | `#00F5FF` |
| Secondary Accent | ![](https://via.placeholder.com/12/BF5AF2/BF5AF2) Plasma Purple | `#BF5AF2` |
| Highlight | ![](https://via.placeholder.com/12/FF6B35/FF6B35) Nova Orange | `#FF6B35` |
| Text | ![](https://via.placeholder.com/12/E8EAF0/E8EAF0) Ghost White | `#E8EAF0` |

---

## 🧠 Using the Master Prompt

1. Open `MASTER_PROMPT.md`
2. Copy the **entire** contents
3. Paste as a system prompt into Claude (or any capable LLM)
4. Ask it to create any scene — e.g.:  
   *"Create a data reveal scene showing our Q3 revenue growing from $2M to $4.2M"*
5. The output will be complete, runnable Manim code using the full brand system

---

## ✅ Versioning

| Version | Date | Notes |
|---------|------|-------|
| 1.0 | 2025 | Initial release |

---

*Built for Manim Community v0.18+. Python 3.9+.*
