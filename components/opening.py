# components/opening.py — Branded series opening / cold open
#
# Drop into any scene's construct():
#   Opening.play(self, episode_number=1, episode_title="Neural Networks 101")

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *


class Opening:
    """
    Modular opening sequence. Call Opening.play(scene, ...) at the top of construct().

    Variants:
        Opening.play(scene)                     — default series intro
        Opening.play(scene, episode_number=3,
                     episode_title="Backprop")  — episode-specific opener
        Opening.cold_open(scene, hook_text)     — quick hook before title card
    """

    @staticmethod
    def play(scene, episode_number=None, episode_title="", duration=4.0):
        """Full branded opening: grid bg → neon logo → episode card → wipe out."""

        # ── Background layer ──────────────────────────────────────────────
        grid = make_grid(opacity=0.08)
        particles = make_particles(n=50, color=ACCENT, radius=0.02)
        scene.add(grid, particles)

        # ── Neon series logo ──────────────────────────────────────────────
        logo = neon_text(SERIES_NAME, color=ACCENT, size=T_HERO)
        logo.move_to(UP * 0.8)
        logo.scale(0).set_opacity(0)

        scene.play(
            logo.animate(rate_func=SPRING, run_time=EPIC).scale(1).set_opacity(1)
        )
        scene.play(pulse(logo, scale=1.06))

        # ── Tagline ──────────────────────────────────────────────────────
        tagline = brand_text(SERIES_TAGLINE, size=T_BODY, color=TEXT_DIM)
        tagline.next_to(logo, DOWN, buff=U2)
        scene.play(FadeIn(tagline, shift=UP * 0.15, run_time=NORMAL))

        # ── Episode card (optional) ──────────────────────────────────────
        if episode_number is not None:
            ep_badge = brand_text(
                f"Episode {episode_number}", size=T_CAPTION, color=ACCENT2
            )
            ep_title = brand_text(episode_title, size=T_H2, color=TEXT)
            ep_group = VGroup(ep_badge, ep_title).arrange(DOWN, buff=0.15)
            ep_group.next_to(tagline, DOWN, buff=U4)

            rule = divider(color=ACCENT, width=6, opacity=0.4)
            rule.next_to(tagline, DOWN, buff=U2)

            scene.play(GrowFromCenter(rule, run_time=NORMAL))
            scene.play(
                FadeIn(ep_badge, shift=DOWN * 0.1, run_time=FAST),
                FadeIn(ep_title, shift=DOWN * 0.15, run_time=NORMAL),
            )

        scene.wait(max(duration - 3.5, 0.5))

        # ── Wipe out ─────────────────────────────────────────────────────
        scene.play(
            *[FadeOut(m, shift=UP * 0.4) for m in scene.mobjects],
            run_time=SLOW, rate_func=EASE_IN,
        )

    @staticmethod
    def cold_open(scene, hook_text, duration=2.5):
        """Quick text hook before the main title card."""
        hook = brand_text(hook_text, size=T_H2, color=TEXT)
        hook.move_to(ORIGIN)

        scene.play(FadeIn(hook, shift=UP * 0.2, run_time=NORMAL))
        scene.wait(duration)
        scene.play(FadeOut(hook, shift=UP * 0.3, run_time=FAST))

    @staticmethod
    def minimal(scene, episode_title=""):
        """Minimal 2-second opener: just the badge + title."""
        badge = brand_text(SERIES_NAME, size=T_CAPTION, color=ACCENT)
        badge.to_corner(UL, buff=U4)

        title = brand_title(episode_title).move_to(POS_TITLE)
        rule = divider(color=ACCENT, width=8).next_to(title, DOWN, buff=U2)

        scene.play(
            FadeIn(badge, run_time=FAST),
            FadeIn(title, shift=DOWN * 0.2, run_time=NORMAL),
            GrowFromCenter(rule, run_time=NORMAL),
        )
        scene.wait(0.5)
        scene.play(FadeOut(title), FadeOut(rule), run_time=FAST)
        # Badge stays on screen
