# series/ML/01_neural_network_basics/scene.py
# Episode: What is a Neural Network?
# Render: make render-scene SCENE=series/ML/01_neural_network_basics/scene.py CLASS=NeuralNetworkBasicsScene
#
# This is the canonical location. The scene from scenes/ is re-exported here.

from manim import *
import sys, os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

from brand import *
from typography import *
from layout import *
from animations import *
from components import Opening, Closing, PauseAndPonder, ChapterCard, Watermark
from shared.ml_components import *
from shared.nn_visualizer import *
from shared.math_helpers import *


class NeuralNetworkBasicsScene(Scene):
    """EP 01 — What is a Neural Network? Neurons, layers, weights, forward pass."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        Opening.play(self, episode_number=1, episode_title="What is a Neural Network?")
        Watermark.add(self)

        self._build_bg()

        ChapterCard.play(self, chapter=1, title="The Neuron")
        self._single_neuron()

        ChapterCard.play(self, chapter=2, title="Layers")
        self._layers_explained()

        PauseAndPonder.play(self, "How many layers does a 'deep' network need?")
        PauseAndPonder.reveal(self, "Typically 3+ hidden layers — but it depends on the task!")

        ChapterCard.play(self, chapter=3, title="Full Network")
        self._full_network()

        Closing.with_summary(self, points=[
            "A neuron computes: σ(wᵀx + b)",
            "Layers stack neurons vertically",
            "Connections carry learned weights",
            "Forward pass flows input → output",
        ], next_episode="Gradient Descent")

    def _build_bg(self):
        self.add(make_grid(opacity=0.08), make_particles(n=30))

    def _single_neuron(self):
        neuron = create_neuron(radius=0.6, color=NEURON_COLOR, activated=True)
        neuron.move_to(ORIGIN)

        inputs = VGroup()
        for i, lbl in enumerate(["x₁", "x₂", "x₃"]):
            start = LEFT * 3.5 + UP * (1 - i)
            arrow = Arrow(start, neuron.get_left() + UP * (0.3 - i * 0.3),
                         color=WEIGHT_COLOR, stroke_width=2, buff=0.15)
            label = brand_text(lbl, size=T_BODY, color=INPUT_COLOR).next_to(arrow, LEFT, buff=0.1)
            inputs.add(VGroup(arrow, label))

        out_arrow = Arrow(neuron.get_right(), RIGHT * 3.5, color=OUTPUT_COLOR, stroke_width=2, buff=0.15)
        out_label = brand_text("ŷ", size=T_BODY, color=OUTPUT_COLOR).next_to(out_arrow, RIGHT, buff=0.1)

        eq = MathTex(r"\sigma(\mathbf{w}^T\mathbf{x} + b)", color=TEXT).scale(0.6)
        eq.next_to(neuron, DOWN, buff=0.5)

        self.play(FadeIn(neuron, run_time=NORMAL))
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.3) for i in inputs], lag_ratio=0.2))
        self.play(FadeIn(out_arrow), FadeIn(out_label))
        self.play(Write(eq, run_time=NORMAL))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [neuron, inputs, out_arrow, out_label, eq]])

    def _layers_explained(self):
        input_l = create_layer(3, color=INPUT_COLOR, label="Input")
        hidden_l = create_layer(4, color=HIDDEN_COLOR, label="Hidden")
        output_l = create_layer(2, color=OUTPUT_COLOR, label="Output")
        layers = VGroup(input_l, hidden_l, output_l).arrange(RIGHT, buff=2.0).move_to(DOWN * 0.3)

        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.3) for l in layers], lag_ratio=0.3))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in list(self.mobjects)[:3]])

    def _full_network(self):
        nn = create_neural_network([3, 5, 4, 2], layer_labels=["In", "H1", "H2", "Out"])
        nn.scale(0.7).move_to(DOWN * 0.3)
        self.play(FadeIn(nn, run_time=SLOW))
        animate_forward_pass(self, nn, layer_delay=0.2)
        self.wait(1.0)
