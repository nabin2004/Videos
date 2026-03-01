# scenes/gradient_descent.py — Gradient Descent Visualized
#
# Episode: How Gradient Descent Works
# Render: manim -pqh --fps 60 scenes/gradient_descent.py GradientDescentScene

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


class GradientDescentScene(Scene):
    """Visualizes gradient descent on a loss surface — the ball rolling downhill analogy."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self._build_bg()
        self._intro()
        self._loss_landscape()
        self._gradient_steps()
        self._learning_rate_comparison()
        self._update_rule()
        self._outro()

    def _build_bg(self):
        self.add(make_grid(opacity=0.08), make_particles(n=25))
        badge = brand_text(SERIES_NAME, size=T_CAPTION, color=ACCENT).to_corner(UL, buff=U4)
        self.add(badge)

    def _intro(self):
        title = brand_title("Gradient Descent").move_to(POS_TITLE)
        sub = brand_text(
            "How neural networks learn by following the slope",
            color=TEXT_DIM,
        ).next_to(title, DOWN, buff=U2)

        self.play(FadeIn(title, shift=DOWN * 0.3, run_time=NORMAL, rate_func=EASE_OUT))
        self.play(Write(sub, run_time=SLOW))
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(sub), run_time=FAST)

    def _loss_landscape(self):
        header = brand_text("The Loss Landscape", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Create axes
        ax = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 2],
            x_length=8,
            y_length=4.5,
            axis_config={"color": BRAND_STEEL, "stroke_width": 1},
            tips=False,
        ).move_to(DOWN * 0.3)

        x_label = brand_text("Parameter θ", size=T_LABEL, color=TEXT_DIM)
        x_label.next_to(ax.x_axis, DOWN, buff=0.25)
        y_label = brand_text("Loss L(θ)", size=T_LABEL, color=TEXT_DIM)
        y_label.next_to(ax.y_axis, LEFT, buff=0.25)

        # Loss function: simple quadratic
        loss_func = lambda x: 0.5 * x ** 2 + 0.3 * np.sin(2 * x) + 1
        loss_curve = ax.plot(loss_func, x_range=[-3.8, 3.8, 0.05], color=LOSS_COLOR, stroke_width=2.5)
        loss_glow = loss_curve.copy().set_stroke(color=LOSS_COLOR, width=10, opacity=0.15)

        self.play(Create(ax, run_time=NORMAL), FadeIn(x_label), FadeIn(y_label))
        self.play(Create(loss_glow), Create(loss_curve, run_time=SLOW))
        self.wait(0.5)

        self.ax = ax
        self.loss_func = loss_func
        self.loss_curve = loss_curve
        self.loss_glow = loss_glow
        self.header = header
        self.ax_labels = VGroup(x_label, y_label)

    def _gradient_steps(self):
        self.play(FadeOut(self.header))
        step_label = brand_text("Following the gradient downhill...", size=T_H2, color=ACCENT2)
        step_label.move_to(POS_TITLE)
        self.play(FadeIn(step_label, shift=DOWN * 0.2))

        ax = self.ax
        loss_func = self.loss_func

        # Starting point
        theta = 3.0
        lr = 0.3
        ball = Dot(ax.c2p(theta, loss_func(theta)), color=ACCENT, radius=0.12)
        ball_glow = Dot(ax.c2p(theta, loss_func(theta)), color=ACCENT, radius=0.2, fill_opacity=0.3)

        self.play(FadeIn(ball_glow), FadeIn(ball))

        # Gradient descent steps
        for step in range(8):
            gradient = theta + 0.3 * np.cos(2 * theta)  # derivative of loss
            theta_new = theta - lr * gradient
            theta_new = np.clip(theta_new, -3.8, 3.8)

            new_pos = ax.c2p(theta_new, loss_func(theta_new))

            # Draw gradient arrow
            grad_arrow = Arrow(
                ball.get_center(),
                new_pos,
                color=GRADIENT_COLOR,
                stroke_width=2,
                buff=0,
                max_tip_length_to_length_ratio=0.25,
            )
            self.play(Create(grad_arrow, run_time=FAST))
            self.play(
                ball.animate(rate_func=EASE_OUT, run_time=NORMAL).move_to(new_pos),
                ball_glow.animate(rate_func=EASE_OUT, run_time=NORMAL).move_to(new_pos),
            )
            self.play(FadeOut(grad_arrow, run_time=FAST * 0.5))

            theta = theta_new

        # Converged indicator
        star = brand_text("★ Minimum found!", size=T_BODY, color=BRAND_SOLAR)
        star.next_to(ball, UP, buff=0.3)
        self.play(FadeIn(star, shift=DOWN * 0.1))
        self.wait(1.0)

        self.play(*[FadeOut(m) for m in [step_label, ball, ball_glow, star]])

    def _learning_rate_comparison(self):
        header = brand_text("Learning Rate Matters", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Show three cards
        cards = VGroup(
            callout("α too small → slow convergence", icon="🐢", accent=ACCENT, width=5),
            callout("α just right → smooth descent", icon="✓", accent=BRAND_SOLAR, width=5),
            callout("α too large → diverges!", icon="💥", accent=LOSS_COLOR, width=5),
        ).arrange(DOWN, buff=0.5).move_to(DOWN * 0.5)

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=RIGHT * 0.3) for c in cards],
                lag_ratio=0.3, run_time=SLOW,
            )
        )
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in [header, cards, self.ax, self.loss_curve,
                                          self.loss_glow, self.ax_labels]])

    def _update_rule(self):
        header = brand_text("The Update Rule", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        eq_box = ml_equation_box(EQ_GD_UPDATE, label="Gradient Descent", color=ACCENT, scale=1.1)
        eq_box.move_to(UP * 0.3)
        self.play(FadeIn(eq_box, shift=UP * 0.2, run_time=SLOW))
        self.wait(0.5)

        # Annotate parts
        annotations = bullet_list([
            "θ = model parameters (weights & biases)",
            "α = learning rate (step size)",
            "∇L = gradient of the loss function",
        ], accent=ACCENT2)
        annotations.scale(0.8).next_to(eq_box, DOWN, buff=0.6)

        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in annotations],
                        lag_ratio=0.2, run_time=SLOW)
        )
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in [header, eq_box, annotations]])

    def _outro(self):
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=SLOW)
        self.wait(0.3)
