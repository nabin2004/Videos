# examples/03_ml_components.py
# Demonstrates: create_neural_network, animate_forward_pass, animate_backprop,
#   create_matrix_grid, create_activation_plot, create_loss_curve, ml_block,
#   create_pipeline, data_flow_arrow, create_attention_matrix

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
from shared.math_helpers import sigmoid, relu


class MLComponentsShowcase(Scene):
    """Show every reusable ML/DL visual component."""

    def construct(self):
        self.camera.background_color = BG
        self.add(make_grid(opacity=0.06))

        self._neural_network_section()
        self._matrix_and_tensor_section()
        self._activation_plots_section()
        self._loss_curve_section()
        self._pipeline_section()

    # ─────────────────────────────────────────────────────────────────────────

    def _neural_network_section(self):
        title = neon_text("Neural Network", color=ACCENT, size=T_H1)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        # Build network: 3 → 5 → 4 → 2
        net = create_neural_network(
            [3, 5, 4, 2],
            layer_labels=["Input", "Hidden 1", "Hidden 2", "Output"],
        )
        net.set_height(4.5).move_to(DOWN * 0.3)
        self.play(FadeIn(net, shift=UP * 0.3), run_time=1.0)
        self.wait(0.5)

        # Forward pass
        animate_forward_pass(self, net, layer_delay=0.15)
        self.wait(0.5)

        # Backprop
        animate_backprop(self, net)
        self.wait(0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])

    def _matrix_and_tensor_section(self):
        title = neon_text("Matrix & Tensor", color=ACCENT2, size=T_H1)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        # Matrix grid
        mat = create_matrix_grid(3, 4, values=np.round(np.random.randn(3, 4), 2).tolist())
        mat.move_to(LEFT * 3 + DOWN * 0.3)
        mat_label = brand_text("Weight Matrix (3×4)", size=T_CAPTION, color=TEXT_DIM)
        mat_label.next_to(mat, DOWN, buff=0.3)

        # Tensor
        tensor = create_tensor_3d(shape=(3, 3, 3))
        tensor.move_to(RIGHT * 3 + DOWN * 0.3)
        tensor_label = brand_text("3D Tensor (3×3×3)", size=T_CAPTION, color=TEXT_DIM)
        tensor_label.next_to(tensor, DOWN, buff=0.3)

        self.play(
            FadeIn(mat, shift=UP * 0.2), FadeIn(mat_label),
            FadeIn(tensor, shift=UP * 0.2), FadeIn(tensor_label),
            run_time=1.0,
        )
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def _activation_plots_section(self):
        title = neon_text("Activation Functions", color=BRAND_NOVA, size=T_H1)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        funcs = ["relu", "sigmoid", "tanh", "leaky_relu"]
        colors = [BRAND_ELECTRIC, BRAND_PLASMA, BRAND_NOVA, BRAND_SOLAR]
        plots = VGroup()
        for fname, c in zip(funcs, colors):
            p = create_activation_plot(func_name=fname, width=2.5, height=1.8, color=c)
            plots.add(p)
        plots.arrange_in_grid(rows=1, buff=0.6).move_to(DOWN * 0.3)

        self.play(
            LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in plots], lag_ratio=0.12),
            run_time=1.5,
        )
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def _loss_curve_section(self):
        title = neon_text("Loss Curve", color=LOSS_COLOR, size=T_H1)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        ax_group = create_loss_curve_axes()
        ax_group.move_to(DOWN * 0.3)
        self.play(FadeIn(ax_group))

        # Simulated loss values — (epoch, loss) tuples within axes range
        epochs = 30
        loss_vals = [(i * (100 / epochs), min(0.9 * np.exp(-0.08 * i) + 0.05, 1.0)) for i in range(epochs)]
        ax_obj = ax_group[0]  # extract the Axes from the VGroup
        curve = create_loss_curve(ax_obj, loss_vals)
        self.play(Create(curve), run_time=2.0)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def _pipeline_section(self):
        title = neon_text("ML Pipeline", color=BRAND_SOLAR, size=T_H1)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        pipe = create_pipeline([
            {"label": "Data", "color": BRAND_ELECTRIC},
            {"label": "Preprocess", "color": BRAND_PLASMA},
            {"label": "Model", "color": BRAND_NOVA},
            {"label": "Train", "color": BRAND_SOLAR},
            {"label": "Evaluate", "color": INPUT_COLOR},
        ])
        pipe.set_height(1.2).move_to(DOWN * 0.5)
        self.play(FadeIn(pipe, shift=RIGHT * 0.3), run_time=1.5)
        self.wait(1.5)

        # Also show standalone ml_blocks
        blocks = VGroup(
            ml_block("Conv2D", color=BRAND_ELECTRIC, details="3×3, 64"),
            ml_block("BatchNorm", color=BRAND_PLASMA),
            ml_block("ReLU", color=BRAND_NOVA),
            ml_block("Dense", color=BRAND_SOLAR, details="128 units"),
        ).arrange(RIGHT, buff=0.5).move_to(DOWN * 2.5)

        self.play(
            LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in blocks], lag_ratio=0.08),
            run_time=1.0,
        )
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects])
        fin = neon_text("ML Components ✓", color=ACCENT, size=T_H1)
        self.play(FadeIn(fin, scale=0.8))
        self.wait(1.0)
