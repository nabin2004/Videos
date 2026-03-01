# scenes/loss_functions.py — Loss Functions Explained
#
# Episode: Loss Functions — Measuring How Wrong You Are
# Render: manim -pqh --fps 60 scenes/loss_functions.py LossFunctionsScene

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


class LossFunctionsScene(Scene):
    """Visualizes MSE, Cross-Entropy, and how loss guides learning."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self._build_bg()
        self._intro()
        self._what_is_loss()
        self._mse_visualization()
        self._cross_entropy_visualization()
        self._loss_curve_training()
        self._outro()

    def _build_bg(self):
        self.add(make_grid(opacity=0.08), make_particles(n=25))
        badge = brand_text(SERIES_NAME, size=T_CAPTION, color=ACCENT).to_corner(UL, buff=U4)
        self.add(badge)

    def _intro(self):
        title = brand_title("Loss Functions").move_to(POS_TITLE)
        sub = brand_text(
            "Measuring how wrong your model is",
            color=TEXT_DIM,
        ).next_to(title, DOWN, buff=U2)

        self.play(FadeIn(title, shift=DOWN * 0.3, run_time=NORMAL, rate_func=EASE_OUT))
        self.play(Write(sub, run_time=SLOW))
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(sub), run_time=FAST)

    def _what_is_loss(self):
        header = brand_text("What is Loss?", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Simple analogy
        items = bullet_list([
            "Loss = a number measuring prediction error",
            "High loss → bad predictions",
            "Low loss → good predictions",
            "Goal: minimize the loss!",
        ])
        items.scale(0.85).move_to(DOWN * 0.3)

        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in items],
                        lag_ratio=0.25, run_time=SLOW)
        )
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [header, items]])

    def _mse_visualization(self):
        header = brand_text("Mean Squared Error (MSE)", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Equation
        eq_box = ml_equation_box(EQ_MSE, label="Regression Loss", color=LOSS_COLOR, scale=0.8)
        eq_box.move_to(UP * 1.5)
        self.play(FadeIn(eq_box, shift=UP * 0.2, run_time=SLOW))

        # Scatter plot with prediction line
        ax = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=5, y_length=3.5,
            axis_config={"color": BRAND_STEEL, "stroke_width": 1},
            tips=False,
        ).move_to(DOWN * 1.2)

        # Data points
        np.random.seed(42)
        xs = np.linspace(1, 9, 8)
        ys = 0.8 * xs + 1 + np.random.randn(8) * 0.8

        dots = VGroup(*[
            Dot(ax.c2p(x, y), color=ACCENT, radius=0.08) for x, y in zip(xs, ys)
        ])

        # Prediction line
        pred_line = ax.plot(lambda x: 0.8 * x + 1, x_range=[0, 10], color=BRAND_NOVA, stroke_width=2)

        self.play(Create(ax, run_time=FAST))
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08, run_time=NORMAL))
        self.play(Create(pred_line, run_time=NORMAL))

        # Show error lines
        error_lines = VGroup()
        for x, y in zip(xs, ys):
            pred_y = 0.8 * x + 1
            line = DashedLine(
                ax.c2p(x, y), ax.c2p(x, pred_y),
                color=LOSS_COLOR, stroke_width=1.5, dash_length=0.05,
            )
            error_lines.add(line)

        error_label = brand_text("← errors (squared)", size=T_CAPTION, color=LOSS_COLOR)
        error_label.next_to(ax, RIGHT, buff=0.3)

        self.play(Create(error_lines, run_time=NORMAL), FadeIn(error_label))
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in [header, eq_box, ax, dots, pred_line,
                                          error_lines, error_label]])

    def _cross_entropy_visualization(self):
        header = brand_text("Cross-Entropy Loss", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        eq_box = ml_equation_box(EQ_CROSS_ENTROPY, label="Classification Loss", color=ACCENT2, scale=0.8)
        eq_box.move_to(UP * 1.2)
        self.play(FadeIn(eq_box, shift=UP * 0.2, run_time=SLOW))

        # Plot: -log(p) curve
        ax = Axes(
            x_range=[0.01, 1, 0.2], y_range=[0, 5, 1],
            x_length=5, y_length=3,
            axis_config={"color": BRAND_STEEL, "stroke_width": 1},
            tips=False,
        ).move_to(DOWN * 1.2)

        neg_log = ax.plot(lambda p: -np.log(p), x_range=[0.02, 1, 0.01],
                         color=LOSS_COLOR, stroke_width=2.5)
        neg_log_glow = neg_log.copy().set_stroke(color=LOSS_COLOR, width=10, opacity=0.15)

        x_lbl = brand_text("Predicted probability p", size=T_LABEL, color=TEXT_DIM)
        x_lbl.next_to(ax.x_axis, DOWN, buff=0.2)
        y_lbl = brand_text("-log(p)", size=T_LABEL, color=TEXT_DIM)
        y_lbl.next_to(ax.y_axis, LEFT, buff=0.2)

        self.play(Create(ax, run_time=FAST), FadeIn(x_lbl), FadeIn(y_lbl))
        self.play(Create(neg_log_glow), Create(neg_log, run_time=SLOW))

        # Annotations
        anno_high = brand_text("p ≈ 0 → huge loss!", size=T_CAPTION, color=LOSS_COLOR)
        anno_high.next_to(ax, RIGHT, buff=0.4).shift(UP * 0.5)
        anno_low = brand_text("p ≈ 1 → tiny loss ✓", size=T_CAPTION, color=BRAND_SOLAR)
        anno_low.next_to(anno_high, DOWN, buff=0.4)

        self.play(FadeIn(anno_high), FadeIn(anno_low))
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in [header, eq_box, ax, neg_log, neg_log_glow,
                                          x_lbl, y_lbl, anno_high, anno_low]])

    def _loss_curve_training(self):
        header = brand_text("Training Progress", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Loss curve over training
        ax_group = create_loss_curve_axes()
        ax_group.move_to(DOWN * 0.3)
        ax = ax_group[0]

        # Generate decreasing loss values
        epochs = np.linspace(0, 100, 50)
        loss_values = 0.85 * np.exp(-0.03 * epochs) + 0.05 + 0.02 * np.random.randn(50)
        loss_values = np.clip(loss_values, 0.03, 1.0)
        data_points = list(zip(epochs, loss_values))

        loss_curve = create_loss_curve(ax, data_points, color=LOSS_COLOR)

        self.play(Create(ax_group, run_time=NORMAL))
        self.play(Create(loss_curve, run_time=EPIC, rate_func=EASE_OUT))

        # Annotations
        start_label = brand_text("High loss\n(untrained)", size=T_CAPTION, color=LOSS_COLOR)
        start_label.next_to(ax.c2p(5, 0.85), UP, buff=0.2)

        end_label = brand_text("Low loss\n(trained!)", size=T_CAPTION, color=BRAND_SOLAR)
        end_label.next_to(ax.c2p(90, 0.08), UP, buff=0.2)

        self.play(FadeIn(start_label), FadeIn(end_label))
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in [header, ax_group, loss_curve, start_label, end_label]])

    def _outro(self):
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=SLOW)
        self.wait(0.3)
