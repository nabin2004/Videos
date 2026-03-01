# scenes/intro.py — TheBoringAI Series Intro / Title Card
#
# Render: manim -pqh --fps 60 scenes/intro.py IntroScene

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *
from shared.ml_components import *


class IntroScene(Scene):
    """Series intro: animated logo, title reveal, and neural network backdrop."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self._build_bg()
        self._logo_reveal()
        self._series_title()
        self._neural_net_backdrop()
        self._tagline()
        self._outro()

    # ── Background ────────────────────────────────────────────────────────────
    def _build_bg(self):
        grid = make_grid(opacity=0.08)
        particles = make_particles(n=60, color=ACCENT, radius=0.02)
        self.add(grid, particles)

    # ── Logo Reveal ───────────────────────────────────────────────────────────
    def _logo_reveal(self):
        # Neon glow series name
        logo = neon_text(SERIES_NAME, color=ACCENT, size=T_HERO)
        logo.move_to(UP * 0.5)

        # Scale in with spring
        logo.scale(0).set_opacity(0)
        self.play(
            logo.animate(rate_func=SPRING, run_time=EPIC).scale(1).set_opacity(1)
        )
        self.wait(0.3)

        # Pulse emphasis
        self.play(pulse(logo, scale=1.08))
        self.wait(0.5)

        # Move to top
        self.play(
            logo.animate(rate_func=EASE_IO, run_time=SLOW)
            .move_to(POS_TITLE)
            .scale(0.65)
        )
        self.logo = logo

    # ── Series Title ──────────────────────────────────────────────────────────
    def _series_title(self):
        subtitle = brand_text(
            "Machine Learning & Deep Learning — Visualized",
            size=T_H2,
            color=TEXT_DIM,
        ).next_to(self.logo, DOWN, buff=U2)

        self.play(Write(subtitle, run_time=SLOW, rate_func=EASE_OUT))
        self.wait(0.3)

        rule = divider(color=ACCENT, width=8, opacity=0.5)
        rule.next_to(subtitle, DOWN, buff=U2)
        self.play(GrowFromCenter(rule, run_time=NORMAL))
        self.subtitle = subtitle
        self.rule = rule

    # ── Neural Network Backdrop ───────────────────────────────────────────────
    def _neural_net_backdrop(self):
        nn = create_neural_network(
            [3, 5, 5, 3],
            layer_labels=["Input", "Hidden 1", "Hidden 2", "Output"],
        )
        nn.scale(0.55).move_to(DOWN * 0.8)
        nn.set_opacity(0.5)

        self.play(FadeIn(nn, run_time=SLOW))
        self.wait(0.5)

        # Brief activation pulse through the network
        connections, layers = nn[0], nn[1]
        for i, layer in enumerate(layers):
            neurons = layer[0]
            self.play(
                *[
                    (n[-1] if isinstance(n, VGroup) else n)
                    .animate(run_time=0.25)
                    .set_fill(ACTIVATION_COLOR, opacity=0.7)
                    for n in neurons
                ],
                rate_func=EASE_OUT,
            )
            if i < len(connections):
                self.play(
                    connections[i].animate(run_time=0.2).set_stroke(
                        ACTIVATION_COLOR, opacity=0.4
                    )
                )

        self.wait(0.5)
        self.nn = nn

    # ── Tagline ───────────────────────────────────────────────────────────────
    def _tagline(self):
        tagline = brand_text(
            "Making the boring parts of AI... not so boring.",
            size=T_BODY,
            color=TEXT,
        ).move_to(POS_FOOTER)

        self.play(FadeIn(tagline, shift=UP * 0.2, run_time=NORMAL))
        self.wait(2.0)

    # ── Outro ─────────────────────────────────────────────────────────────────
    def _outro(self):
        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=SLOW,
            rate_func=EASE_IN,
        )
        self.wait(0.3)
