# components/bumper.py — Short transition bumpers between content blocks
#
# Usage:
#   Bumper.play(self)                        — default brand flash
#   Bumper.text(self, "Up Next: Training")   — text bumper

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *


class Bumper:
    """Quick 1-2 second transition bumpers."""

    @staticmethod
    def play(scene, flash_color=ACCENT):
        """Brand flash bumper — quick pulse of color then back to content."""
        flash = Rectangle(
            width=FRAME_W, height=FRAME_H,
            fill_color=flash_color, fill_opacity=0,
            stroke_width=0,
        )
        scene.play(
            flash.animate(rate_func=rate_functions.there_and_back, run_time=0.6)
            .set_fill(opacity=0.15)
        )
        scene.remove(flash)

    @staticmethod
    def text(scene, text, color=ACCENT):
        """Text bumper — shows a short message then fades."""
        msg = brand_text(text, size=T_H2, color=color).move_to(ORIGIN)
        scene.play(FadeIn(msg, shift=UP * 0.15, run_time=FAST))
        scene.wait(0.8)
        scene.play(FadeOut(msg, run_time=FAST))

    @staticmethod
    def wipe(scene, direction=LEFT):
        """Full-screen wipe (re-exported from animations for convenience)."""
        scene_wipe(scene, direction)

    @staticmethod
    def logo_flash(scene):
        """Quick logo flash bumper."""
        logo = brand_text(SERIES_NAME, size=T_H1, color=ACCENT)
        logo.move_to(ORIGIN).set_opacity(0)
        scene.play(
            logo.animate(rate_func=rate_functions.there_and_back_with_pause, run_time=1.2)
            .set_opacity(0.6)
        )
        scene.remove(logo)
