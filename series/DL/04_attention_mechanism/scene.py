# series/DL/04_attention_mechanism/scene.py
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


class AttentionMechanismScene(Scene):
    """DL-04 — How transformers think."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        Opening.play(self, episode_number=4, episode_title="Attention Mechanism",
                     subtitle="Deep Learning Series")
        Watermark.add(self)
        self.add(make_grid(opacity=0.08))

        ChapterCard.play(self, chapter=1, title="Query, Key, Value")
        self._qkv()

        ChapterCard.play(self, chapter=2, title="Attention Scores")
        self._attention_matrix()

        PauseAndPonder.play(self, "Why is attention called 'All You Need'?")
        PauseAndPonder.reveal(self,
            "Attention replaces recurrence + convolution,\nprocessing all tokens in parallel!")

        ChapterCard.play(self, chapter=3, title="Multi-Head")
        self._multi_head()

        Closing.with_summary(self, points=[
            "Q, K, V are linear projections of input",
            "Attention = softmax(QKᵀ/√d) · V",
            "Multiple heads capture different relationships",
            "Foundation of all modern LLMs",
        ])

    def _qkv(self):
        eq = ml_equation_box(EQ_ATTENTION, label="Scaled Dot-Product Attention")
        self.play(FadeIn(eq))
        self.wait(2)
        self.play(FadeOut(eq))

    def _attention_matrix(self):
        tokens = ["The", "cat", "sat", "on", "mat"]
        matrix = create_attention_matrix(tokens, token_color=PRIMARY)
        matrix.scale(0.8).move_to(ORIGIN)
        self.play(FadeIn(matrix, run_time=SLOW))
        self.wait(2)
        self.play(FadeOut(matrix))

    def _multi_head(self):
        heads = VGroup()
        colors = DATA_COLORS[:4]
        for i, c in enumerate(colors):
            head = ml_block(f"Head {i+1}", color=c, width=1.5, height=0.8)
            heads.add(head)
        heads.arrange(RIGHT, buff=0.5).move_to(UP * 0.5)

        concat = ml_block("Concat", color=WEIGHT_COLOR, width=2.0, height=0.8)
        concat.next_to(heads, DOWN, buff=0.8)

        out = ml_block("Linear", color=OUTPUT_COLOR, width=2.0, height=0.8)
        out.next_to(concat, DOWN, buff=0.6)

        arrows1 = VGroup(*[Arrow(h.get_bottom(), concat.get_top(),
                                  color=BRAND_GHOST, stroke_width=1.5, buff=0.1) for h in heads])
        arrow2 = Arrow(concat.get_bottom(), out.get_top(),
                       color=BRAND_GHOST, stroke_width=1.5, buff=0.1)

        group = VGroup(heads, arrows1, concat, arrow2, out)
        self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.2) for h in heads], lag_ratio=0.15))
        self.play(Create(arrows1), FadeIn(concat))
        self.play(Create(arrow2), FadeIn(out))
        self.wait(1.5)
        self.play(FadeOut(group))
