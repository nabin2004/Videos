# components/closing.py — Branded series closing / end card
#
# Drop into any scene's construct():
#   Closing.play(self, next_episode="Backpropagation")

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *


class Closing:
    """
    Modular end card. Call Closing.play(scene, ...) at the end of construct().

    Variants:
        Closing.play(scene)                              — standard outro
        Closing.play(scene, next_episode="Backprop")     — teases next ep
        Closing.with_summary(scene, points=[...])        — recap + outro
    """

    @staticmethod
    def play(scene, next_episode="", social_handle="@TheBoringAI", duration=5.0):
        """Full branded end card: logo, CTA, next episode teaser."""

        # ── Wipe in ──────────────────────────────────────────────────────
        scene.play(
            *[FadeOut(m, shift=DOWN * 0.3) for m in scene.mobjects],
            run_time=SLOW,
        )

        # ── Background ───────────────────────────────────────────────────
        grid = make_grid(opacity=0.06)
        particles = make_particles(n=40, color=ACCENT2, radius=0.02)
        scene.add(grid, particles)

        # ── Logo ─────────────────────────────────────────────────────────
        logo = neon_text(SERIES_NAME, color=ACCENT, size=T_H1)
        logo.move_to(UP * 1.5)
        logo.scale(0).set_opacity(0)
        scene.play(
            logo.animate(rate_func=SPRING, run_time=SLOW).scale(1).set_opacity(1)
        )

        # ── Divider ──────────────────────────────────────────────────────
        rule = divider(color=ACCENT, width=8, opacity=0.4)
        rule.next_to(logo, DOWN, buff=U2)
        scene.play(GrowFromCenter(rule, run_time=FAST))

        # ── CTA ──────────────────────────────────────────────────────────
        cta_like = brand_text("👍  Like & Subscribe", size=T_BODY, color=TEXT)
        cta_bell = brand_text("🔔  Turn on notifications", size=T_BODY, color=TEXT)
        cta_share = brand_text("📤  Share with a friend", size=T_BODY, color=TEXT_DIM)
        cta_group = VGroup(cta_like, cta_bell, cta_share).arrange(DOWN, buff=0.35)
        cta_group.next_to(rule, DOWN, buff=0.5)

        scene.play(
            LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cta_group],
                        lag_ratio=0.2, run_time=SLOW)
        )

        # ── Next episode teaser ──────────────────────────────────────────
        if next_episode:
            next_label = brand_text(
                f"Next →  {next_episode}", size=T_BODY, color=ACCENT2
            )
            next_label.next_to(cta_group, DOWN, buff=0.6)
            scene.play(FadeIn(next_label, shift=UP * 0.15, run_time=NORMAL))

        # ── Social handle ────────────────────────────────────────────────
        handle = brand_text(social_handle, size=T_CAPTION, color=TEXT_DIM)
        handle.to_corner(DR, buff=U4)
        scene.play(FadeIn(handle, run_time=FAST))

        scene.wait(duration)

        # ── Fade all ─────────────────────────────────────────────────────
        scene.play(
            *[FadeOut(m, shift=DOWN * 0.3) for m in scene.mobjects],
            run_time=SLOW, rate_func=EASE_IN,
        )
        scene.wait(0.3)

    @staticmethod
    def with_summary(scene, points, next_episode="", duration=6.0):
        """Recap key points, then play the standard outro."""
        # ── Summary section ──────────────────────────────────────────────
        header = brand_text("Recap", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        scene.play(FadeIn(header, shift=DOWN * 0.2))

        bullets = bullet_list(points, accent=ACCENT)
        bullets.scale(0.85).move_to(DOWN * 0.3)
        scene.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in bullets],
                        lag_ratio=0.2, run_time=SLOW)
        )
        scene.wait(2.0)

        # Then play the standard closing
        Closing.play(scene, next_episode=next_episode, duration=duration - 2.0)

    @staticmethod
    def quick(scene, message="Thanks for watching!"):
        """Minimal 2-second outro — just a message and fade."""
        msg = brand_text(message, size=T_H2, color=TEXT).move_to(ORIGIN)
        scene.play(
            *[FadeOut(m) for m in scene.mobjects], run_time=FAST,
        )
        scene.play(FadeIn(msg, shift=UP * 0.2, run_time=NORMAL))
        scene.wait(1.5)
        scene.play(FadeOut(msg, run_time=SLOW))
