# components/subscribe_cta.py — Subscribe / engagement call-to-action overlays
#
# Usage:
#   SubscribeCTA.popup(self)            — popup in bottom-right
#   SubscribeCTA.end_screen(self)       — full end-screen overlay

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *


class SubscribeCTA:
    """Subscribe / engagement popups and overlays."""

    @staticmethod
    def popup(scene, text="Subscribe for more!", duration=3.0, corner=DR):
        """Small popup CTA in a corner — appears and disappears."""
        bg = RoundedRectangle(
            corner_radius=0.15, width=4.5, height=0.9,
            fill_color=PANEL, fill_opacity=0.95,
            stroke_color=ACCENT, stroke_width=1.5,
        )
        icon = brand_text("🔔", size=T_H2)
        msg = brand_text(text, size=T_BODY, color=TEXT)
        content = VGroup(icon, msg).arrange(RIGHT, buff=0.2)
        content.move_to(bg.get_center())
        card = VGroup(bg, content)
        card.to_corner(corner, buff=U2)

        scene.play(FadeIn(card, shift=UP * 0.3, run_time=NORMAL))
        scene.wait(duration)
        scene.play(FadeOut(card, shift=DOWN * 0.3, run_time=NORMAL))

    @staticmethod
    def end_screen(scene, duration=5.0):
        """Full end-screen overlay for the last 20 seconds of a YouTube video."""
        overlay = Rectangle(
            width=FRAME_W, height=FRAME_H,
            fill_color=BG, fill_opacity=0.9, stroke_width=0,
        )
        scene.play(FadeIn(overlay, run_time=FAST))

        logo = neon_text(SERIES_NAME, color=ACCENT, size=T_H1)
        logo.move_to(UP * 2.0)

        # Two placeholder boxes for YouTube end screen elements
        box_l = RoundedRectangle(
            corner_radius=0.2, width=4.5, height=2.8,
            fill_color=PANEL, fill_opacity=0.5,
            stroke_color=ACCENT, stroke_width=1,
        ).move_to(LEFT * 2.8 + DOWN * 0.5)

        box_r = RoundedRectangle(
            corner_radius=0.2, width=4.5, height=2.8,
            fill_color=PANEL, fill_opacity=0.5,
            stroke_color=ACCENT2, stroke_width=1,
        ).move_to(RIGHT * 2.8 + DOWN * 0.5)

        lbl_l = brand_text("▶ Watch Next", size=T_BODY, color=TEXT_DIM).move_to(box_l)
        lbl_r = brand_text("📋 Playlist", size=T_BODY, color=TEXT_DIM).move_to(box_r)

        sub_btn = RoundedRectangle(
            corner_radius=0.1, width=3, height=0.65,
            fill_color="#FF0000", fill_opacity=0.9,
            stroke_width=0,
        ).move_to(DOWN * 3.0)
        sub_text = brand_text("SUBSCRIBE", size=T_BODY, color="#FFFFFF")
        sub_text.move_to(sub_btn.get_center())

        scene.play(
            FadeIn(logo, run_time=NORMAL),
            FadeIn(box_l, shift=UP * 0.2, run_time=NORMAL),
            FadeIn(box_r, shift=UP * 0.2, run_time=NORMAL),
            FadeIn(lbl_l, run_time=NORMAL),
            FadeIn(lbl_r, run_time=NORMAL),
        )
        scene.play(FadeIn(sub_btn), FadeIn(sub_text))

        scene.wait(duration)
