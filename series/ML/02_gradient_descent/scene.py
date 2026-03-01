# series/ML/02_gradient_descent/scene.py
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


class GradientDescentScene(Scene):
    """EP 02 — How neural networks learn by following the slope."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        Opening.play(self, episode_number=2, episode_title="Gradient Descent")
        Watermark.add(self)
        self.add(make_grid(opacity=0.08))

        ChapterCard.play(self, chapter=1, title="The Loss Landscape")
        self._loss_landscape()

        ChapterCard.play(self, chapter=2, title="Taking Steps")
        self._gradient_step()

        PauseAndPonder.with_choices(self,
            question="What happens if the learning rate is too large?",
            choices=["Converges faster", "Overshoots the minimum", "Network gets smarter"])
        PauseAndPonder.reveal(self, "It overshoots! The loss can diverge instead of converging.")

        ChapterCard.play(self, chapter=3, title="Learning Rate")
        self._learning_rate_comparison()

        Closing.with_summary(self, points=[
            "Gradient descent follows the negative gradient",
            "Learning rate controls step size",
            "Too large → diverges, too small → slow",
            "SGD adds stochastic sampling",
        ], next_episode="Loss Functions")

    def _loss_landscape(self):
        axes = Axes(x_range=[-3, 3, 1], y_range=[0, 10, 2],
                    x_length=8, y_length=5, axis_config={"color": TEXT})
        axes.move_to(DOWN * 0.3)
        labels = axes.get_axis_labels(x_label="w", y_label="L(w)")
        curve = axes.plot(lambda x: x**2 + 0.5 * np.sin(3*x) + 2, color=LOSS_COLOR)
        self.play(Create(axes), Write(labels))
        self.play(Create(curve, run_time=SLOW))
        self.wait(1)
        self.play(*[FadeOut(m) for m in [axes, labels, curve]])

    def _gradient_step(self):
        eq = ml_equation(EQ_GD_UPDATE)
        eq.move_to(UP * 1)
        self.play(Write(eq))
        self.wait(1.5)
        self.play(FadeOut(eq))

    def _learning_rate_comparison(self):
        title = brand_text("Learning Rate Effect", size=T_H2, color=PRIMARY)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        for lr, label_text, color in [(0.01, "α = 0.01 (slow)", BRAND_GHOST),
                                       (0.1, "α = 0.1 (good)", BRAND_ELECTRIC),
                                       (1.0, "α = 1.0 (unstable)", BRAND_NOVA)]:
            label = brand_text(label_text, size=T_BODY, color=color)
            label.move_to(ORIGIN)
            self.play(FadeIn(label))
            self.wait(0.8)
            self.play(FadeOut(label))

        self.play(FadeOut(title))
