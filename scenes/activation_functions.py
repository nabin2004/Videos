# scenes/activation_functions.py — Activation Functions Compared
#
# Episode: Activation Functions — Why Non-Linearity Matters
# Render: manim -pqh --fps 60 scenes/activation_functions.py ActivationFunctionsScene

from manim import *
import numpy as np

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *
from shared.ml_components import *
from shared.math_helpers import *


class ActivationFunctionsScene(Scene):
    """Compares ReLU, Sigmoid, and Tanh activation functions side by side."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self._build_bg()
        self._intro()
        self._why_nonlinearity()
        self._sigmoid_deep_dive()
        self._relu_deep_dive()
        self._tanh_deep_dive()
        self._comparison_grid()
        self._outro()

    def _build_bg(self):
        self.add(make_grid(opacity=0.08), make_particles(n=25))
        badge = brand_text(SERIES_NAME, size=T_CAPTION, color=ACCENT).to_corner(UL, buff=U4)
        self.add(badge)

    def _intro(self):
        title = brand_title("Activation Functions").move_to(POS_TITLE)
        sub = brand_text(
            "The magic that gives neural networks their power",
            color=TEXT_DIM,
        ).next_to(title, DOWN, buff=U2)

        self.play(FadeIn(title, shift=DOWN * 0.3, run_time=NORMAL, rate_func=EASE_OUT))
        self.play(Write(sub, run_time=SLOW))
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(sub), run_time=FAST)

    def _why_nonlinearity(self):
        header = brand_text("Why Non-Linearity?", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Without activation: just a linear function
        without_box = callout(
            "Without activation: network = single linear function",
            icon="✗", accent=LOSS_COLOR, width=10,
        )
        with_box = callout(
            "With activation: network can learn ANY function",
            icon="✓", accent=BRAND_SOLAR, width=10,
        )

        boxes = VGroup(without_box, with_box).arrange(DOWN, buff=0.6).move_to(DOWN * 0.3)
        self.play(FadeIn(without_box, shift=RIGHT * 0.3, run_time=NORMAL))
        self.wait(0.5)
        self.play(FadeIn(with_box, shift=RIGHT * 0.3, run_time=NORMAL))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [header, boxes]])

    def _sigmoid_deep_dive(self):
        header = brand_text("Sigmoid", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Plot
        ax = Axes(
            x_range=[-6, 6, 1], y_range=[-0.2, 1.2, 0.2],
            x_length=7, y_length=3.5,
            axis_config={"color": BRAND_STEEL, "stroke_width": 1},
            tips=False,
        ).move_to(LEFT * 1.5 + DOWN * 0.5)

        graph = ax.plot(sigmoid, x_range=[-6, 6, 0.05], color=ACCENT, stroke_width=2.5)
        glow = graph.copy().set_stroke(color=ACCENT, width=10, opacity=0.15)

        self.play(Create(ax, run_time=FAST))
        self.play(Create(glow), Create(graph, run_time=SLOW))

        # Equation
        eq = ml_equation(EQ_SIGMOID, scale=0.85)
        eq.next_to(ax, RIGHT, buff=0.8)

        info = bullet_list([
            "Output: (0, 1)",
            "Smooth gradient",
            "Vanishing gradient problem",
        ], accent=ACCENT2)
        info.scale(0.7).next_to(eq, DOWN, buff=0.5)

        self.play(Write(eq, run_time=NORMAL))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in info],
                              lag_ratio=0.2, run_time=SLOW))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [header, ax, graph, glow, eq, info]])

    def _relu_deep_dive(self):
        header = brand_text("ReLU", size=T_H1, color=BRAND_NOVA).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        ax = Axes(
            x_range=[-4, 4, 1], y_range=[-1, 4, 1],
            x_length=7, y_length=3.5,
            axis_config={"color": BRAND_STEEL, "stroke_width": 1},
            tips=False,
        ).move_to(LEFT * 1.5 + DOWN * 0.5)

        graph = ax.plot(relu, x_range=[-4, 4, 0.05], color=BRAND_NOVA, stroke_width=2.5)
        glow = graph.copy().set_stroke(color=BRAND_NOVA, width=10, opacity=0.15)

        self.play(Create(ax, run_time=FAST))
        self.play(Create(glow), Create(graph, run_time=SLOW))

        eq = ml_equation(EQ_RELU, scale=0.85)
        eq.next_to(ax, RIGHT, buff=0.8)

        info = bullet_list([
            "Output: [0, ∞)",
            "No vanishing gradient",
            "Dead neurons if z < 0",
            "Most popular choice!",
        ], accent=BRAND_NOVA)
        info.scale(0.7).next_to(eq, DOWN, buff=0.5)

        self.play(Write(eq, run_time=NORMAL))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in info],
                              lag_ratio=0.2, run_time=SLOW))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [header, ax, graph, glow, eq, info]])

    def _tanh_deep_dive(self):
        header = brand_text("Tanh", size=T_H1, color=ACCENT2).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        ax = Axes(
            x_range=[-4, 4, 1], y_range=[-1.5, 1.5, 0.5],
            x_length=7, y_length=3.5,
            axis_config={"color": BRAND_STEEL, "stroke_width": 1},
            tips=False,
        ).move_to(LEFT * 1.5 + DOWN * 0.5)

        graph = ax.plot(tanh, x_range=[-4, 4, 0.05], color=ACCENT2, stroke_width=2.5)
        glow = graph.copy().set_stroke(color=ACCENT2, width=10, opacity=0.15)

        self.play(Create(ax, run_time=FAST))
        self.play(Create(glow), Create(graph, run_time=SLOW))

        eq = ml_equation(EQ_TANH, scale=0.85)
        eq.next_to(ax, RIGHT, buff=0.8)

        info = bullet_list([
            "Output: (-1, 1)",
            "Zero-centered",
            "Better than sigmoid",
            "Still has vanishing gradient",
        ], accent=ACCENT2)
        info.scale(0.7).next_to(eq, DOWN, buff=0.5)

        self.play(Write(eq, run_time=NORMAL))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in info],
                              lag_ratio=0.2, run_time=SLOW))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [header, ax, graph, glow, eq, info]])

    def _comparison_grid(self):
        header = brand_text("Side by Side", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        plots = VGroup(
            create_activation_plot("relu", color=BRAND_NOVA),
            create_activation_plot("sigmoid", color=ACCENT),
            create_activation_plot("tanh", color=ACCENT2),
            create_activation_plot("leaky_relu", color=BRAND_SOLAR),
        ).arrange_in_grid(rows=2, cols=2, buff=0.8).move_to(DOWN * 0.3)

        self.play(
            LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in plots],
                        lag_ratio=0.2, run_time=SLOW)
        )
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in [header, plots]])

    def _outro(self):
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=SLOW)
        self.wait(0.3)
