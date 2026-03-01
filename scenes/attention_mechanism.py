# scenes/attention_mechanism.py — Attention Is All You Need
#
# Episode: The Attention Mechanism — How Transformers Think
# Render: manim -pqh --fps 60 scenes/attention_mechanism.py AttentionMechanismScene

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


class AttentionMechanismScene(Scene):
    """Visualizes self-attention: Q, K, V matrices, attention weights, and the transformer block."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self._build_bg()
        self._intro()
        self._intuition()
        self._qkv_explanation()
        self._attention_matrix()
        self._transformer_block()
        self._outro()

    def _build_bg(self):
        self.add(make_grid(opacity=0.08), make_particles(n=25))
        badge = brand_text(SERIES_NAME, size=T_CAPTION, color=ACCENT).to_corner(UL, buff=U4)
        self.add(badge)

    def _intro(self):
        title = brand_title("Attention Mechanism").move_to(POS_TITLE)
        sub = brand_text(
            '"Attention Is All You Need" — Vaswani et al., 2017',
            color=TEXT_DIM,
        ).next_to(title, DOWN, buff=U2)

        self.play(FadeIn(title, shift=DOWN * 0.3, run_time=NORMAL, rate_func=EASE_OUT))
        self.play(Write(sub, run_time=SLOW))
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(sub), run_time=FAST)

    def _intuition(self):
        header = brand_text("The Intuition", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Show a sentence with attention weights
        sentence = "The cat sat on the mat"
        words = sentence.split()

        word_mobs = VGroup()
        for word in words:
            w = brand_text(word, size=T_H2, color=TEXT)
            word_mobs.add(w)
        word_mobs.arrange(RIGHT, buff=0.4).move_to(UP * 0.5)

        self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.2) for w in word_mobs],
                              lag_ratio=0.1, run_time=SLOW))
        self.wait(0.3)

        # Highlight "cat" and show attention to "sat" and "mat"
        self.play(word_mobs[1].animate(run_time=FAST).set_color(ACCENT))  # "cat"

        # Draw attention arcs
        arcs = VGroup()
        attention_to = [(2, 0.8), (5, 0.6), (0, 0.3)]  # (word_index, weight)
        for idx, weight in attention_to:
            arc = CurvedArrow(
                word_mobs[1].get_bottom() + DOWN * 0.1,
                word_mobs[idx].get_bottom() + DOWN * 0.1,
                color=ACCENT,
                stroke_width=weight * 4,
                stroke_opacity=weight,
                angle=-0.5 if idx > 1 else 0.5,
            )
            arcs.add(arc)

        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.2, run_time=SLOW))

        explanation = brand_text(
            '"cat" attends most to "sat" — learning which words matter',
            size=T_BODY, color=TEXT_DIM,
        ).move_to(DOWN * 1.5)
        self.play(FadeIn(explanation))

        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [header, word_mobs, arcs, explanation]])

    def _qkv_explanation(self):
        header = brand_text("Query, Key, Value", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Three labeled blocks
        q_block = ml_block("Query (Q)", width=2.5, height=1.0, color=ACCENT, details="What am I looking for?")
        k_block = ml_block("Key (K)", width=2.5, height=1.0, color=ACCENT2, details="What do I contain?")
        v_block = ml_block("Value (V)", width=2.5, height=1.0, color=BRAND_NOVA, details="What do I provide?")

        blocks = VGroup(q_block, k_block, v_block).arrange(RIGHT, buff=0.8).move_to(UP * 0.5)

        self.play(
            LaggedStart(*[FadeIn(b, shift=UP * 0.3) for b in blocks],
                        lag_ratio=0.2, run_time=SLOW)
        )
        self.wait(0.5)

        # Attention formula
        eq_box = ml_equation_box(EQ_ATTENTION, label="Scaled Dot-Product Attention", color=ACCENT, scale=0.75)
        eq_box.move_to(DOWN * 1.5)
        self.play(FadeIn(eq_box, shift=UP * 0.3, run_time=SLOW))
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in [header, blocks, eq_box]])

    def _attention_matrix(self):
        header = brand_text("Attention Weights", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        tokens = ["The", "cat", "sat", "on", "mat"]
        attn = create_attention_matrix(tokens, size=0.6)
        attn.move_to(DOWN * 0.3)

        self.play(FadeIn(attn, run_time=SLOW))
        self.wait(0.5)

        explanation = brand_text(
            "Brighter = higher attention weight",
            size=T_BODY, color=TEXT_DIM,
        ).next_to(attn, DOWN, buff=0.5)
        self.play(FadeIn(explanation))

        self.wait(2.0)
        self.play(*[FadeOut(m) for m in [header, attn, explanation]])

    def _transformer_block(self):
        header = brand_text("Transformer Block", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        blocks = [
            {"label": "Input\nEmbedding", "color": INPUT_COLOR},
            {"label": "Multi-Head\nAttention", "color": ACCENT},
            {"label": "Add &\nNorm", "color": BRAND_STEEL},
            {"label": "Feed\nForward", "color": ACCENT2},
            {"label": "Add &\nNorm", "color": BRAND_STEEL},
            {"label": "Output", "color": OUTPUT_COLOR},
        ]
        pipeline = create_pipeline(blocks, spacing=0.2)
        pipeline.scale(0.6).move_to(DOWN * 0.5)

        self.play(FadeIn(pipeline, run_time=SLOW))
        self.wait(0.5)

        # Animate signal
        signal = Dot(color=ACTIVATION_COLOR, radius=0.1)
        signal.move_to(pipeline[0][0].get_left() + LEFT * 0.3)
        self.add(signal)

        for block in pipeline[0]:
            self.play(
                signal.animate(rate_func=EASE_OUT, run_time=0.3)
                .move_to(block.get_center())
            )

        self.play(FadeOut(signal))

        note = brand_text(
            "Stack 6-96 of these blocks → GPT, BERT, etc.",
            size=T_BODY, color=TEXT_DIM,
        ).next_to(pipeline, DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in [header, pipeline, note]])

    def _outro(self):
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=SLOW)
        self.wait(0.3)
