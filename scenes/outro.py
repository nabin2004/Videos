# scenes/outro.py — TheBoringAI Series Outro / End Card
#
# Render: manim -pqh --fps 60 scenes/outro.py OutroScene

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *


class OutroScene(Scene):
    """Series outro: logo, call-to-action, social links."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self._build_bg()
        self._logo()
        self._cta()
        self._fade_out()

    def _build_bg(self):
        grid = make_grid(opacity=0.06)
        particles = make_particles(n=50, color=ACCENT2, radius=0.02)
        self.add(grid, particles)

    def _logo(self):
        logo = neon_text(SERIES_NAME, color=ACCENT, size=T_HERO)
        logo.move_to(UP * 1.0)
        logo.scale(0).set_opacity(0)

        self.play(
            logo.animate(rate_func=SPRING, run_time=EPIC).scale(1).set_opacity(1)
        )
        self.play(pulse(logo, scale=1.06))

        tagline = brand_text(
            SERIES_TAGLINE,
            size=T_BODY, color=TEXT_DIM,
        ).next_to(logo, DOWN, buff=U2)

        rule = divider(color=ACCENT, width=8, opacity=0.4)
        rule.next_to(tagline, DOWN, buff=U2)

        self.play(Write(tagline, run_time=SLOW))
        self.play(GrowFromCenter(rule, run_time=NORMAL))

        self.wait(0.5)
        self.logo = logo
        self.tagline = tagline
        self.rule = rule

    def _cta(self):
        cta_items = VGroup(
            brand_text("Like & Subscribe for more episodes", size=T_BODY, color=TEXT),
            brand_text("Next Episode: Coming Soon", size=T_BODY, color=ACCENT2),
        ).arrange(DOWN, buff=0.4).next_to(self.rule, DOWN, buff=0.6)

        self.play(
            LaggedStart(*[FadeIn(item, shift=UP * 0.2) for item in cta_items],
                        lag_ratio=0.3, run_time=SLOW)
        )
        self.wait(3.0)

    def _fade_out(self):
        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=SLOW,
            rate_func=EASE_IN,
        )
        self.wait(0.5)
