# series/DL/02_activation_functions/scene.py
from manim import *
import sys, os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

from brand import *
from typography import *
from layout import *
from animations import *
from components import Opening, Closing, PauseAndPonder, ChapterCard, Watermark
from shared.ml_components import *
from shared.math_helpers import *


class ActivationFunctionsScene(Scene):
    """DL-02 — Why non-linearity matters."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        Opening.play(self, episode_number=2, episode_title="Activation Functions",
                     subtitle="Deep Learning Series")
        Watermark.add(self)
        self.add(make_grid(opacity=0.08))

        ChapterCard.play(self, chapter=1, title="Sigmoid")
        self._show_activation("Sigmoid", EQ_SIGMOID, sigmoid, BRAND_ELECTRIC)

        ChapterCard.play(self, chapter=2, title="ReLU")
        self._show_activation("ReLU", EQ_RELU, relu, BRAND_NOVA)

        PauseAndPonder.with_choices(self,
            question="Which activation is most popular today?",
            choices=["Sigmoid", "Tanh", "ReLU", "Softmax"])
        PauseAndPonder.reveal(self, "ReLU! It's simple, fast, and avoids vanishing gradients.")

        ChapterCard.play(self, chapter=3, title="Tanh")
        self._show_activation("Tanh", EQ_TANH, tanh, BRAND_PLASMA)

        Closing.with_summary(self, points=[
            "Activations add non-linearity",
            "Sigmoid: (0,1), good for probabilities",
            "ReLU: simple & efficient, most popular",
            "Tanh: (-1,1), zero-centred",
        ], next_episode="CNN Explained")

    def _show_activation(self, name, equation, func, color):
        eq = ml_equation_box(equation, label=name)
        eq.move_to(UP * 1.5)
        self.play(FadeIn(eq))

        plot = create_activation_plot(func, x_range=[-4, 4], color=color)
        plot.move_to(DOWN * 1)
        self.play(Create(plot, run_time=SLOW))
        self.wait(1)
        self.play(FadeOut(eq), FadeOut(plot))
