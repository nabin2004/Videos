# scenes/neural_network_basics.py — What is a Neural Network?
#
# Episode: Neural Network Basics
# Render: manim -pqh --fps 60 scenes/neural_network_basics.py NeuralNetworkBasicsScene

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


class NeuralNetworkBasicsScene(Scene):
    """Explains the building blocks of a neural network: neurons, layers, weights."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self._build_bg()
        self._intro()
        self._single_neuron()
        self._layers_explained()
        self._full_network()
        self._forward_pass_demo()
        self._key_equations()
        self._outro()

    # ── Background ────────────────────────────────────────────────────────────
    def _build_bg(self):
        self.add(make_grid(opacity=0.08), make_particles(n=30))
        badge = brand_text(SERIES_NAME, size=T_CAPTION, color=ACCENT).to_corner(UL, buff=U4)
        self.add(badge)

    # ── Intro ─────────────────────────────────────────────────────────────────
    def _intro(self):
        title = brand_title("What is a Neural Network?").move_to(POS_TITLE)
        sub = brand_text(
            "The fundamental building block of deep learning",
            color=TEXT_DIM,
        ).next_to(title, DOWN, buff=U2)

        self.play(FadeIn(title, shift=DOWN * 0.3, run_time=NORMAL, rate_func=EASE_OUT))
        self.play(Write(sub, run_time=SLOW))
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(sub), run_time=FAST)

    # ── Single Neuron ─────────────────────────────────────────────────────────
    def _single_neuron(self):
        header = brand_text("The Neuron", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Create a big neuron
        neuron = create_neuron(radius=0.6, color=NEURON_COLOR, activated=True)
        neuron.move_to(ORIGIN)

        # Input arrows
        inputs = VGroup()
        input_labels = ["x₁", "x₂", "x₃"]
        for i, label_text in enumerate(input_labels):
            start = LEFT * 3.5 + UP * (1 - i)
            arrow = Arrow(start, neuron.get_left() + UP * (0.3 - i * 0.3),
                         color=WEIGHT_COLOR, stroke_width=2, buff=0.15)
            lbl = brand_text(label_text, size=T_BODY, color=INPUT_COLOR)
            lbl.next_to(arrow, LEFT, buff=0.1)
            inputs.add(VGroup(arrow, lbl))

        # Output arrow
        out_arrow = Arrow(
            neuron.get_right(), RIGHT * 3.5,
            color=OUTPUT_COLOR, stroke_width=2, buff=0.15,
        )
        out_label = brand_text("ŷ", size=T_BODY, color=OUTPUT_COLOR)
        out_label.next_to(out_arrow, RIGHT, buff=0.1)

        # Equation inside neuron area
        eq = MathTex(r"\sigma(\mathbf{w}^T\mathbf{x} + b)", color=TEXT).scale(0.6)
        eq.next_to(neuron, DOWN, buff=0.5)

        self.play(FadeIn(neuron, run_time=NORMAL))
        self.play(
            LaggedStart(*[FadeIn(inp, shift=RIGHT * 0.3) for inp in inputs],
                        lag_ratio=0.2, run_time=SLOW)
        )
        self.play(FadeIn(out_arrow), FadeIn(out_label))
        self.play(Write(eq, run_time=NORMAL))
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in [header, neuron, inputs, out_arrow, out_label, eq]])

    # ── Layers Explained ──────────────────────────────────────────────────────
    def _layers_explained(self):
        header = brand_text("Layers", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Show three types of layers side by side
        input_layer = create_layer(3, color=INPUT_COLOR, label="Input Layer")
        hidden_layer = create_layer(4, color=HIDDEN_COLOR, label="Hidden Layer")
        output_layer = create_layer(2, color=OUTPUT_COLOR, label="Output Layer")

        layers_group = VGroup(input_layer, hidden_layer, output_layer).arrange(RIGHT, buff=2.0)
        layers_group.move_to(DOWN * 0.3)

        self.play(
            LaggedStart(
                FadeIn(input_layer, shift=UP * 0.3),
                FadeIn(hidden_layer, shift=UP * 0.3),
                FadeIn(output_layer, shift=UP * 0.3),
                lag_ratio=0.3, run_time=SLOW,
            )
        )

        # Descriptions
        descriptions = [
            "Raw features\n(pixels, numbers...)",
            "Learned\nrepresentations",
            "Final\nprediction",
        ]
        for layer, desc in zip([input_layer, hidden_layer, output_layer], descriptions):
            d = brand_text(desc, size=T_CAPTION, color=TEXT_DIM)
            d.next_to(layer, DOWN, buff=0.5)
            self.play(FadeIn(d, run_time=FAST))

        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in [self.mobjects[0], self.mobjects[1], self.mobjects[2]]])

    # ── Full Network ──────────────────────────────────────────────────────────
    def _full_network(self):
        header = brand_text("Putting It Together", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        nn = create_neural_network(
            [3, 5, 4, 2],
            layer_labels=["Input", "Hidden 1", "Hidden 2", "Output"],
        )
        nn.scale(0.7).move_to(DOWN * 0.3)

        self.play(FadeIn(nn, run_time=SLOW))
        self.wait(1.0)

        self.nn = nn
        self.nn_header = header

    # ── Forward Pass Demo ─────────────────────────────────────────────────────
    def _forward_pass_demo(self):
        fp_label = brand_text("Forward Pass", size=T_H2, color=ACCENT2)
        fp_label.next_to(self.nn, UP, buff=0.8)
        self.play(
            FadeOut(self.nn_header),
            FadeIn(fp_label, shift=DOWN * 0.2),
        )

        animate_forward_pass(self, self.nn, layer_delay=0.2)
        self.wait(0.5)

        self.play(*[FadeOut(m) for m in self.mobjects if m not in [self.mobjects[0], self.mobjects[1], self.mobjects[2]]])

    # ── Key Equations ─────────────────────────────────────────────────────────
    def _key_equations(self):
        header = brand_text("Key Equations", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        eqs = equation_sequence(
            [EQ_FORWARD, EQ_ACTIVATION, EQ_RELU],
            labels=["Forward:", "Activation:", "ReLU:"],
            spacing=0.9,
        )
        eqs.scale(0.85).move_to(DOWN * 0.3)

        self.play(
            LaggedStart(
                *[FadeIn(eq, shift=RIGHT * 0.3) for eq in eqs],
                lag_ratio=0.4, run_time=EPIC,
            )
        )
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in [header, eqs]])

    # ── Outro ─────────────────────────────────────────────────────────────────
    def _outro(self):
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=SLOW)
        self.wait(0.3)
