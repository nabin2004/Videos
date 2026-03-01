# scenes/cnn_explained.py — Convolutional Neural Networks
#
# Episode: CNNs — How Computers See
# Render: manim -pqh --fps 60 scenes/cnn_explained.py CNNExplainedScene

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


class CNNExplainedScene(Scene):
    """Visualizes convolution, feature maps, pooling, and the CNN pipeline."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self._build_bg()
        self._intro()
        self._convolution_operation()
        self._feature_maps()
        self._cnn_pipeline()
        self._outro()

    def _build_bg(self):
        self.add(make_grid(opacity=0.08), make_particles(n=25))
        badge = brand_text(SERIES_NAME, size=T_CAPTION, color=ACCENT).to_corner(UL, buff=U4)
        self.add(badge)

    def _intro(self):
        title = brand_title("Convolutional Neural Networks").move_to(POS_TITLE)
        sub = brand_text(
            "Teaching machines to see patterns in images",
            color=TEXT_DIM,
        ).next_to(title, DOWN, buff=U2)

        self.play(FadeIn(title, shift=DOWN * 0.3, run_time=NORMAL, rate_func=EASE_OUT))
        self.play(Write(sub, run_time=SLOW))
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(sub), run_time=FAST)

    def _convolution_operation(self):
        header = brand_text("The Convolution Operation", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # Equation
        eq = ml_equation(EQ_CONV, scale=0.8)
        eq.next_to(header, DOWN, buff=0.4)
        self.play(Write(eq, run_time=NORMAL))

        # Input image grid (5x5)
        np.random.seed(42)
        input_values = np.random.randint(0, 10, (5, 5)).tolist()
        input_grid = create_matrix_grid(5, 5, cell_size=0.5, values=input_values, color=ACCENT)
        input_grid.move_to(LEFT * 3.5 + DOWN * 1.0)
        input_label = brand_text("Input", size=T_CAPTION, color=TEXT_DIM)
        input_label.next_to(input_grid, DOWN, buff=0.2)

        # Kernel (3x3)
        kernel_vals = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=float)
        kernel = create_conv_kernel(size=3, cell_size=0.5, values=kernel_vals, color=BRAND_NOVA)
        kernel.move_to(DOWN * 1.0)
        kernel_label = brand_text("Kernel", size=T_CAPTION, color=TEXT_DIM)
        kernel_label.next_to(kernel, DOWN, buff=0.2)

        # Output feature map (3x3)
        output_grid = create_feature_map(3, 3, cell_size=0.5, color=ACCENT2, label="Output")
        output_grid.move_to(RIGHT * 3.5 + DOWN * 1.0)

        # Multiply symbol
        mult = brand_text("*", size=T_H1, color=TEXT).move_to(LEFT * 1.5 + DOWN * 1.0)
        equals = brand_text("=", size=T_H1, color=TEXT).move_to(RIGHT * 1.5 + DOWN * 1.0)

        self.play(FadeIn(input_grid), FadeIn(input_label))
        self.play(FadeIn(mult), FadeIn(kernel), FadeIn(kernel_label))
        self.play(FadeIn(equals), FadeIn(output_grid))

        # Highlight sliding window
        highlight = Square(
            side_length=1.5, stroke_color=BRAND_NOVA,
            stroke_width=3, fill_opacity=0,
        )
        highlight.move_to(input_grid[0][0:3].get_center())  # top-left 3x3

        self.play(Create(highlight))

        # Slide across a few positions
        positions = [
            input_grid[0][0].get_center(),  # approximate grid positions
            input_grid[0][0].get_center() + RIGHT * 0.5,
            input_grid[0][0].get_center() + RIGHT * 1.0,
        ]
        for pos in positions:
            self.play(
                highlight.animate(rate_func=EASE_IO, run_time=NORMAL).move_to(pos + DOWN * 0.5 + RIGHT * 0.5)
            )

        self.wait(1.0)
        self.play(*[FadeOut(m) for m in [header, eq, input_grid, input_label,
                                          kernel, kernel_label, output_grid,
                                          mult, equals, highlight]])

    def _feature_maps(self):
        header = brand_text("Feature Maps", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        sub = brand_text(
            "Each filter detects a different pattern",
            size=T_BODY, color=TEXT_DIM,
        ).next_to(header, DOWN, buff=U2)
        self.play(FadeIn(sub))

        # Multiple feature maps
        labels = ["Edges", "Corners", "Textures", "Shapes"]
        colors = [ACCENT, ACCENT2, BRAND_NOVA, BRAND_SOLAR]
        maps_group = VGroup()

        for label, color in zip(labels, colors):
            fm = create_feature_map(5, 5, cell_size=0.25, color=color, label=label)
            maps_group.add(fm)

        maps_group.arrange(RIGHT, buff=0.8).move_to(DOWN * 0.5)

        self.play(
            LaggedStart(*[FadeIn(fm, shift=UP * 0.3) for fm in maps_group],
                        lag_ratio=0.2, run_time=SLOW)
        )
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [header, sub, maps_group]])

    def _cnn_pipeline(self):
        header = brand_text("CNN Architecture", size=T_H1, color=ACCENT).move_to(POS_TITLE)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        blocks = [
            {"label": "Input\nImage", "color": INPUT_COLOR, "details": "28×28×1"},
            {"label": "Conv2D", "color": ACCENT, "details": "32 filters"},
            {"label": "ReLU", "color": BRAND_NOVA, "details": "activation"},
            {"label": "MaxPool", "color": ACCENT2, "details": "2×2"},
            {"label": "Conv2D", "color": ACCENT, "details": "64 filters"},
            {"label": "Flatten", "color": BRAND_STEEL, "details": "→ 1D"},
            {"label": "Dense", "color": BRAND_SOLAR, "details": "128 units"},
            {"label": "Output", "color": OUTPUT_COLOR, "details": "10 classes"},
        ]

        pipeline = create_pipeline(blocks, spacing=0.1)
        pipeline.scale(0.55).move_to(DOWN * 0.5)

        self.play(FadeIn(pipeline, run_time=SLOW))
        self.wait(0.5)

        # Animate data flowing through
        signal = Dot(color=ACTIVATION_COLOR, radius=0.1)
        signal.move_to(pipeline[0][0].get_left() + LEFT * 0.3)
        self.add(signal)

        for block in pipeline[0]:
            self.play(
                signal.animate(rate_func=EASE_OUT, run_time=0.25)
                .move_to(block.get_center()),
                block[0].animate(run_time=0.25)
                .set_stroke(ACTIVATION_COLOR, width=2.5),
            )

        self.play(FadeOut(signal))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [header, pipeline]])

    def _outro(self):
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=SLOW)
        self.wait(0.3)
