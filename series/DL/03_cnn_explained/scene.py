# series/DL/03_cnn_explained/scene.py
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


class CNNExplainedScene(Scene):
    """DL-03 — Teaching machines to see patterns in images."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        Opening.play(self, episode_number=3, episode_title="CNN Explained",
                     subtitle="Deep Learning Series")
        Watermark.add(self)
        self.add(make_grid(opacity=0.08))

        ChapterCard.play(self, chapter=1, title="Convolution")
        self._convolution()

        ChapterCard.play(self, chapter=2, title="Feature Maps")
        self._feature_maps()

        PauseAndPonder.play(self, "Why does a CNN use filters instead of fully connected layers?")
        PauseAndPonder.reveal(self, "Parameter sharing! A 3×3 filter has 9 params\nvs millions in a fully-connected approach.")

        ChapterCard.play(self, chapter=3, title="Architecture")
        self._architecture()

        Closing.with_summary(self, points=[
            "Convolution slides a filter across input",
            "Feature maps detect edges, textures, objects",
            "Pooling reduces spatial dimensions",
            "Conv → Pool → Flatten → Dense → Output",
        ], next_episode="Attention Mechanism")

    def _convolution(self):
        eq = ml_equation_box(EQ_CONV, label="Convolution")
        self.play(FadeIn(eq))
        self.wait(1.5)
        self.play(FadeOut(eq))

    def _feature_maps(self):
        fmaps = VGroup()
        colors = [BRAND_ELECTRIC, BRAND_NOVA, BRAND_PLASMA]
        for i, c in enumerate(colors):
            fm = create_feature_map(size=5, color=c, cell_size=0.35)
            fmaps.add(fm)
        fmaps.arrange(RIGHT, buff=1.0).move_to(ORIGIN)
        self.play(LaggedStart(*[FadeIn(fm, shift=UP * 0.3) for fm in fmaps], lag_ratio=0.3))
        self.wait(1.5)
        self.play(FadeOut(fmaps))

    def _architecture(self):
        pipeline = create_pipeline(
            ["Input\n28×28", "Conv\n3×3", "Pool\n2×2", "Conv\n3×3", "Flatten", "Dense", "Output\n10"],
            colors=[INPUT_COLOR, BRAND_ELECTRIC, BRAND_PLASMA,
                    BRAND_ELECTRIC, WEIGHT_COLOR, HIDDEN_COLOR, OUTPUT_COLOR])
        pipeline.scale(0.65).move_to(ORIGIN)
        self.play(FadeIn(pipeline, run_time=SLOW))
        self.wait(2)
        self.play(FadeOut(pipeline))
