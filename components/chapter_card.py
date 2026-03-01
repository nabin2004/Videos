# components/chapter_card.py — Chapter title cards between sections
#
# Usage:
#   ChapterCard.play(self, chapter=1, title="What is a Neuron?")

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *


class ChapterCard:
    """
    Full-screen chapter title between content sections.

    Variants:
        ChapterCard.play(scene, chapter=1, title="...")
        ChapterCard.mini(scene, title="...")             — inline, no wipe
    """

    @staticmethod
    def play(scene, chapter, title, subtitle="", duration=2.5):
        """Full-screen chapter card with number + title + wipe."""

        # Fade existing content
        if scene.mobjects:
            scene.play(
                *[FadeOut(m, shift=LEFT * 0.3) for m in scene.mobjects],
                run_time=FAST,
            )

        # Background
        bg = Rectangle(
            width=FRAME_W, height=FRAME_H,
            fill_color=BG, fill_opacity=1, stroke_width=0,
        )
        scene.add(bg)
        scene.add(make_grid(opacity=0.06))

        # Chapter number
        ch_num = brand_text(
            f"Chapter {chapter}", size=T_CAPTION, color=ACCENT2
        ).move_to(UP * 0.8)

        # Title
        ch_title = brand_title(title, color=ACCENT)
        ch_title.next_to(ch_num, DOWN, buff=0.3)
        if ch_title.width > FRAME_W - 4:
            ch_title.scale_to_fit_width(FRAME_W - 4)

        # Subtitle
        sub_mob = None
        if subtitle:
            sub_mob = brand_text(subtitle, size=T_BODY, color=TEXT_DIM)
            sub_mob.next_to(ch_title, DOWN, buff=0.3)

        # Decorative lines
        line_l = Line(LEFT * 3, LEFT * 0.5, color=ACCENT, stroke_opacity=0.3, stroke_width=1)
        line_r = Line(RIGHT * 0.5, RIGHT * 3, color=ACCENT, stroke_opacity=0.3, stroke_width=1)
        lines = VGroup(line_l, line_r).move_to(ch_num.get_center() + UP * 0.4)

        # Animate
        scene.play(
            GrowFromCenter(line_l, run_time=NORMAL),
            GrowFromCenter(line_r, run_time=NORMAL),
            FadeIn(ch_num, shift=DOWN * 0.1, run_time=NORMAL),
        )
        scene.play(FadeIn(ch_title, shift=DOWN * 0.15, run_time=NORMAL))
        if sub_mob:
            scene.play(FadeIn(sub_mob, run_time=FAST))

        scene.wait(duration)

        all_mobs = [bg, ch_num, ch_title, line_l, line_r]
        if sub_mob:
            all_mobs.append(sub_mob)
        scene.play(
            *[FadeOut(m) for m in scene.mobjects],
            run_time=FAST,
        )

    @staticmethod
    def mini(scene, title, color=ACCENT):
        """Inline section break — no full wipe, just a header slide."""
        header = brand_text(title, size=T_H1, color=color).move_to(POS_TITLE)
        rule = divider(color=color, width=8).next_to(header, DOWN, buff=U)

        scene.play(
            FadeIn(header, shift=DOWN * 0.15, run_time=NORMAL),
            GrowFromCenter(rule, run_time=NORMAL),
        )
        scene.wait(0.8)
        scene.play(FadeOut(rule, run_time=FAST))
        # header stays — caller removes it when the section is done
        return header
