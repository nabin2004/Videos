# ➕ Add a Scene

A **scene** is a single, self-contained animation unit — think of it like one chapter or one video segment.

---

## 1. Create the file

```bash
touch scenes/my_new_scene.py
```

Name the file after what the scene *does* — `data_reveal.py`, `logo_sting.py`, `chart_walkthrough.py`.

---

## 2. Paste the base template

```python
# scenes/my_new_scene.py

from manim import *
from brand import *
from typography import *
from layout import *
from animations import *


class MyNewScene(Scene):
    """One-sentence description of what this scene communicates."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self._build_bg()
        self._intro()
        self._main_content()
        self._outro()

    # ── Background layer ──────────────────────────────────────────────────────
    def _build_bg(self):
        self.add(make_grid(), make_particles())

    # ── Intro beat ────────────────────────────────────────────────────────────
    def _intro(self):
        title = brand_title("Scene Title").move_to(POS_TITLE)
        self.play(fly_in(title))
        self.wait(0.4)

    # ── Main content ──────────────────────────────────────────────────────────
    def _main_content(self):
        # TODO: replace with your scene logic
        placeholder = brand_text("Content goes here", color=TEXT_DIM).move_to(POS_CENTER)
        self.play(FadeIn(placeholder))
        self.wait(1.5)

    # ── Outro beat ────────────────────────────────────────────────────────────
    def _outro(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=SLOW)
        self.wait(0.2)
```

---

## 3. Register the scene (optional but recommended)

Add an entry to your project's `scenes/__init__.py` so you can reference it centrally:

```python
# scenes/__init__.py
from .my_new_scene import MyNewScene
```

---

## 4. Preview it

```bash
manim -pql scenes/my_new_scene.py MyNewScene
```

---

## Scene naming conventions

| Type | Class name | File name |
|------|-----------|-----------|
| Intro / title card | `IntroScene` | `intro.py` |
| Data / chart reveal | `DataRevealScene` | `data_reveal.py` |
| Logo sting | `LogoStingScene` | `logo_sting.py` |
| Transition bumper | `BumperScene` | `bumper.py` |
| Outro / end card | `OutroScene` | `outro.py` |

---

## Tips

- **One class per file** keeps renders fast and diffs clean.
- If two scenes share objects, extract those into a `shared/` module — never duplicate.
- Keep `construct()` as a high-level orchestrator; push detail into private methods (`_`-prefixed).
- Always end with a `self.wait()` so the last frame holds before the video cuts.
