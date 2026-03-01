# scenes/backpropagation.py — Backpropagation Explained
#
# Episode: How Backpropagation Works
# Render: manim -pqh --fps 60 scenes/backpropagation.py BackpropagationScene

from manim import *
import numpy as np

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *
from shared.ml_components import *
from shared.nn_visualizer import *
from shared.math_helpers import *


class BackpropagationScene(Scene):
    """Visualizes backpropagation: the chain rule flowing gradients backwards."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self._build_bg()
        self._intro()
        self._chain_rule()
        self._network_with_backprop()
        self._gradient_flow()
        self._summary()
        self._outro()

    def _build_bg(self):
        self.add(make_grid(opacity=0.08), make_particles(n=25))
        badge = brand_text(SERIES_NAME, size=T_CAPTION, color=ACCENT).to_corner(UL, buff=U4)
        self.add(badge)

    def _intro(self):
        title = brand_title("Backpropagation").move_to(POS_TITLE)
        sub = brand_text(
            "Teaching networks to learn from their mistakes",
            color=TEXT_DIM,
        ).next_to(title, DOWN, buff=U2)

        self.play(FadeIn(title, shift=DOWN * 0.3, run_time=NORMAL, rate_func=EASE_OUT))
        self.play(Write(sub, run_time=SLOW))
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(sub), run_time=FAST)

    def _chain_rule(self):
        header = brand_text("The Chain Rule", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Chain rule equation
        eq_box = ml_equation_box(EQ_CHAIN_RULE, label="Chain Rule", color=ACCENT, scale=0.9)
        eq_box.move_to(UP * 0.5)
        self.play(FadeIn(eq_box, shift=UP * 0.3, run_time=SLOW))
        self.wait(0.5)

        # Simple computation graph
        comp_graph_label = brand_text(
            "Computation Graph", size=T_H2, color=ACCENT2
        )
        comp_graph_label.next_to(eq_box, DOWN, buff=0.8)

        # x → multiply → add bias → activation → loss
        blocks = [
            {"label": "Input x", "color": INPUT_COLOR},
            {"label": "× w", "color": WEIGHT_COLOR},
            {"label": "+ b", "color": WEIGHT_COLOR},
            {"label": "σ(z)", "color": ACTIVATION_COLOR},
            {"label": "Loss", "color": LOSS_COLOR},
        ]
        pipeline = create_pipeline(blocks, spacing=0.2)
        pipeline.scale(0.65).next_to(comp_graph_label, DOWN, buff=0.4)

        self.play(FadeIn(comp_graph_label))
        self.play(FadeIn(pipeline, run_time=SLOW))
        self.wait(1.5)

        # Show backward arrows
        backward_label = brand_text("← Gradients flow backward", size=T_BODY, color=GRADIENT_COLOR)
        backward_label.next_to(pipeline, DOWN, buff=0.4)

        back_arrow = Arrow(
            pipeline.get_right() + RIGHT * 0.3,
            pipeline.get_left() + LEFT * 0.3,
            color=GRADIENT_COLOR, stroke_width=3,
        )
        back_arrow.next_to(backward_label, DOWN, buff=0.2)

        self.play(FadeIn(backward_label), GrowArrow(back_arrow, run_time=SLOW))
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in [header, eq_box, comp_graph_label, pipeline,
                                          backward_label, back_arrow]])

    def _network_with_backprop(self):
        header = brand_text("Backprop in Action", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Build network
        nn = create_neural_network(
            [2, 4, 3, 1],
            layer_labels=["Input", "Hidden 1", "Hidden 2", "Output"],
        )
        nn.scale(0.7).move_to(DOWN * 0.3)
        self.play(FadeIn(nn, run_time=SLOW))
        self.wait(0.3)

        # Forward pass
        fwd_label = brand_text("1. Forward Pass →", size=T_BODY, color=ACTIVATION_COLOR)
        fwd_label.to_corner(UR, buff=U4)
        self.play(FadeIn(fwd_label))
        animate_forward_pass(self, nn, layer_delay=0.15)

        # Compute loss
        loss_card = metric_card("Loss", "2.34", accent=LOSS_COLOR)
        loss_card.scale(0.6).to_corner(DR, buff=U4)
        self.play(FadeIn(loss_card, shift=UP * 0.2))
        self.wait(0.5)

        # Backward pass
        bwd_label = brand_text("2. ← Backward Pass", size=T_BODY, color=GRADIENT_COLOR)
        bwd_label.next_to(fwd_label, DOWN, buff=0.3)
        self.play(FadeIn(bwd_label))
        animate_backprop(self, nn)
        self.wait(1.0)

        self.nn = nn
        self.play(*[FadeOut(m) for m in [header, fwd_label, bwd_label, loss_card, nn]])

    def _gradient_flow(self):
        header = brand_text("Gradient Flow", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        eqs = equation_sequence(
            [EQ_FORWARD, EQ_CHAIN_RULE, EQ_GD_UPDATE],
            labels=["Forward:", "Chain Rule:", "Update:"],
            spacing=0.9,
        )
        eqs.scale(0.8).move_to(DOWN * 0.3)

        self.play(
            LaggedStart(
                *[FadeIn(eq, shift=RIGHT * 0.3) for eq in eqs],
                lag_ratio=0.5, run_time=EPIC,
            )
        )
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in [header, eqs]])

    def _summary(self):
        header = brand_text("Summary", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        points = bullet_list([
            "Forward pass: compute predictions",
            "Compute loss (how wrong we are)",
            "Backward pass: compute gradients via chain rule",
            "Update: adjust weights to reduce loss",
            "Repeat until convergence",
        ], accent=ACCENT)
        points.scale(0.85).move_to(DOWN * 0.3)

        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in points],
                        lag_ratio=0.2, run_time=SLOW)
        )
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in [header, points]])

    def _outro(self):
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=SLOW)
        self.wait(0.3)
