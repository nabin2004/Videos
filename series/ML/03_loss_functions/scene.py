# series/ML/03_loss_functions/scene.py
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


class LossFunctionsScene(Scene):
    """EP 03 — Measuring how wrong your model is."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        Opening.play(self, episode_number=3, episode_title="Loss Functions")
        Watermark.add(self)
        self.add(make_grid(opacity=0.08))

        ChapterCard.play(self, chapter=1, title="Mean Squared Error")
        self._mse()

        ChapterCard.play(self, chapter=2, title="Cross-Entropy Loss")
        self._cross_entropy()

        PauseAndPonder.play(self, "When would you use MSE vs Cross-Entropy?")
        PauseAndPonder.reveal(self, "MSE for regression, Cross-Entropy for classification!")

        ChapterCard.play(self, chapter=3, title="Watching Loss Drop")
        self._training_curve()

        Closing.with_summary(self, points=[
            "MSE: average squared differences",
            "Cross-Entropy: penalises wrong confidence",
            "Loss guides gradient descent",
            "Training curves show convergence",
        ], next_episode="Backpropagation (DL Series)")

    def _mse(self):
        eq = ml_equation_box(EQ_MSE, label="Mean Squared Error")
        self.play(FadeIn(eq))
        self.wait(1.5)
        self.play(FadeOut(eq))

    def _cross_entropy(self):
        eq = ml_equation_box(EQ_CROSS_ENTROPY, label="Cross-Entropy Loss")
        self.play(FadeIn(eq))
        self.wait(1.5)
        self.play(FadeOut(eq))

    def _training_curve(self):
        axes = create_loss_curve_axes()
        curve = create_loss_curve(axes, color=LOSS_COLOR)
        self.play(Create(axes))
        self.play(Create(curve, run_time=SLOW))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [axes, curve]])
