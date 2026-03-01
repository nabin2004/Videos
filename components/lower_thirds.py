# components/lower_thirds.py — Broadcast-style lower thirds & labels
#
# Usage:
#   LowerThirds.speaker(self, name="Nabin", title="ML Engineer")
#   LowerThirds.topic(self, "Gradient Descent")

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *


class LowerThirds:
    """Lower-third overlays for broadcaster-style labeling."""

    @staticmethod
    def speaker(scene, name, title="", accent=ACCENT, duration=3.0):
        """Broadcast lower-third for identifying a speaker/presenter."""
        bar = Rectangle(
            width=5.5, height=0.06,
            fill_color=accent, fill_opacity=1, stroke_width=0,
        )
        name_mob = brand_text(name, size=T_H2, color=TEXT)
        name_mob.next_to(bar, UP, buff=0.12, aligned_edge=LEFT)

        group = VGroup(bar, name_mob)

        if title:
            title_mob = brand_text(title, size=T_BODY, color=TEXT_DIM)
            title_mob.next_to(bar, DOWN, buff=0.12, aligned_edge=LEFT)
            group.add(title_mob)

        group.to_corner(DL, buff=U4)

        scene.play(FadeIn(group, shift=UP * 0.3, run_time=NORMAL))
        scene.wait(duration)
        scene.play(FadeOut(group, shift=DOWN * 0.3, run_time=NORMAL))

    @staticmethod
    def topic(scene, topic_text, accent=ACCENT, duration=2.5):
        """Topic label lower-third."""
        bg = RoundedRectangle(
            corner_radius=0.1, width=len(topic_text) * 0.22 + 1.5, height=0.65,
            fill_color=PANEL, fill_opacity=0.9,
            stroke_color=accent, stroke_width=1,
        )
        lbl = brand_text(topic_text, size=T_BODY, color=accent)
        lbl.move_to(bg.get_center())
        group = VGroup(bg, lbl).to_corner(DL, buff=U4)

        scene.play(FadeIn(group, shift=UP * 0.2, run_time=NORMAL))
        scene.wait(duration)
        scene.play(FadeOut(group, shift=DOWN * 0.2, run_time=NORMAL))

    @staticmethod
    def source(scene, source_text, duration=3.0):
        """Source citation lower-third."""
        lbl = brand_text(
            f"Source: {source_text}", size=T_CAPTION, color=TEXT_DIM
        ).to_corner(DL, buff=U4)

        scene.play(FadeIn(lbl, shift=UP * 0.1, run_time=FAST))
        scene.wait(duration)
        scene.play(FadeOut(lbl, run_time=FAST))
