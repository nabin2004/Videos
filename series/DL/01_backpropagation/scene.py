# series/DL/01_backpropagation/scene.py
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
from shared.nn_visualizer import *
from shared.math_helpers import *


class BackpropagationScene(Scene):
    """DL-01 — Teaching networks to learn from their mistakes."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        Opening.play(self, episode_number=1, episode_title="Backpropagation",
                     subtitle="Deep Learning Series")
        Watermark.add(self)
        self.add(make_grid(opacity=0.08))

        ChapterCard.play(self, chapter=1, title="Chain Rule")
        self._chain_rule()

        ChapterCard.play(self, chapter=2, title="Gradient Flow")
        self._gradient_flow()

        PauseAndPonder.play(self, "Why do we go backwards instead of forwards?")
        PauseAndPonder.reveal(self,
            "Going backwards lets us compute ALL gradients\nin a single pass — much more efficient!")

        Closing.with_summary(self, points=[
            "Backprop applies the chain rule layer by layer",
            "Gradients flow backwards from loss → input",
            "Each weight gets updated proportionally",
            "Vanishing gradients can stall deep networks",
        ], next_episode="Activation Functions")

    def _chain_rule(self):
        eq = ml_equation_box(EQ_CHAIN_RULE, label="The Chain Rule")
        self.play(FadeIn(eq))
        self.wait(2)
        self.play(FadeOut(eq))

    def _gradient_flow(self):
        nn = create_neural_network([3, 4, 3, 2])
        nn.scale(0.7).move_to(DOWN * 0.3)
        self.play(FadeIn(nn))
        animate_forward_pass(self, nn, layer_delay=0.15)
        self.wait(0.5)
        animate_backprop(self, nn, layer_delay=0.15)
        self.wait(1)
        self.play(FadeOut(nn))
