# scenes/_template.py — Base template for new TheBoringAI scenes
#
# Copy this file and rename the class when creating a new episode.
# Usage:  cp scenes/_template.py scenes/my_new_scene.py

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *
from shared.ml_components import *
from shared.nn_visualizer import *
from shared.math_helpers import *


class TemplateScene(Scene):
    """[REPLACE] One-sentence description of what this scene communicates."""

    # ── 1. CONFIGURATION ─────────────────────────────────────────────────────
    def setup(self):
        self.camera.background_color = BG

    # ── 2. ENTRY POINT ───────────────────────────────────────────────────────
    def construct(self):
        self._build_bg()
        self._intro()
        self._main_content()
        self._outro()

    # ── 3. BACKGROUND LAYER ──────────────────────────────────────────────────
    def _build_bg(self):
        grid = make_grid()
        particles = make_particles()
        self.add(grid, particles)

    # ── 4. INTRO ─────────────────────────────────────────────────────────────
    def _intro(self):
        # Series badge
        badge = brand_text(
            SERIES_NAME, size=T_CAPTION, color=ACCENT
        ).to_corner(UL, buff=U4)
        self.add(badge)

        title = brand_title("Scene Title Here").move_to(POS_TITLE)
        sub = brand_text(
            "Subtitle / tagline", color=TEXT_DIM
        ).next_to(title, DOWN, buff=U2)

        self.play(FadeIn(title, shift=DOWN * 0.3, run_time=NORMAL, rate_func=EASE_OUT))
        self.play(Write(sub, run_time=SLOW))
        self.wait(0.5)

    # ── 5. MAIN CONTENT ──────────────────────────────────────────────────────
    def _main_content(self):
        # TODO: Replace with your scene logic
        placeholder = brand_text(
            "Content goes here", color=TEXT_DIM
        ).move_to(POS_CENTER)
        self.play(FadeIn(placeholder))
        self.wait(1.5)

    # ── 6. OUTRO ─────────────────────────────────────────────────────────────
    def _outro(self):
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=SLOW)
        self.wait(0.3)
