# components/watermark.py — Persistent watermark / series badge
#
# Usage:
#   wm = Watermark.add(self)          — adds badge to corner, returns mob
#   Watermark.add(self, corner=UR)    — change corner

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *


class Watermark:
    """Persistent on-screen badge / watermark."""

    @staticmethod
    def add(scene, corner=UL, opacity=0.7):
        """Add the TheBoringAI badge to a corner. Returns the mobject."""
        badge = brand_text(SERIES_NAME, size=T_CAPTION, color=ACCENT)
        badge.set_opacity(opacity).to_corner(corner, buff=U4)
        scene.add(badge)
        return badge

    @staticmethod
    def add_with_episode(scene, episode_number, corner=UL, opacity=0.7):
        """Badge + episode number."""
        badge = brand_text(SERIES_NAME, size=T_CAPTION, color=ACCENT)
        ep = brand_text(f"EP {episode_number}", size=T_LABEL, color=ACCENT2)
        group = VGroup(badge, ep).arrange(RIGHT, buff=0.2)
        group.set_opacity(opacity).to_corner(corner, buff=U4)
        scene.add(group)
        return group

    @staticmethod
    def progress_bar(scene, progress=0.0, color=ACCENT):
        """Thin progress bar at the very bottom of the frame."""
        track = Line(
            LEFT * FRAME_W / 2, RIGHT * FRAME_W / 2,
            color=BRAND_STEEL, stroke_width=2, stroke_opacity=0.3,
        ).move_to(DOWN * (FRAME_H / 2 - 0.05))

        fill = Line(
            LEFT * FRAME_W / 2,
            LEFT * FRAME_W / 2 + RIGHT * FRAME_W * progress,
            color=color, stroke_width=2,
        ).move_to(track.get_center()).align_to(track, LEFT)

        scene.add(track, fill)
        return VGroup(track, fill)
