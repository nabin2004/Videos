# shared/nn_visualizer.py — High-level neural network visualization helpers
#
# Composable building blocks for animating forward pass, backpropagation,
# attention mechanisms, and common DL architectures.

from manim import *
import numpy as np

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from brand import *
from typography import *
from layout import *
from shared.ml_components import *


# ══════════════════════════════════════════════════════════════════════════════
#  FORWARD PASS ANIMATION
# ══════════════════════════════════════════════════════════════════════════════

def animate_forward_pass(scene, network, layer_delay=0.3, signal_color=ACTIVATION_COLOR):
    """
    Animate a signal flowing left-to-right through a neural network.

    Args:
        scene: the Manim Scene instance
        network: VGroup from create_neural_network (connections, layers)
        layer_delay: seconds between layer activations
        signal_color: color of the activation pulse
    """
    connections, layers = network[0], network[1]

    for i, layer in enumerate(layers):
        neurons = layer[0]  # VGroup of neuron mobjects
        anims = []
        for neuron in neurons:
            target = neuron[-1] if isinstance(neuron, VGroup) else neuron
            anims.append(
                target.animate(rate_func=rate_functions.ease_out_cubic, run_time=0.4)
                .set_fill(signal_color, opacity=0.9)
            )
        scene.play(*anims)

        # Highlight connections to next layer
        if i < len(connections):
            conn_group = connections[i]
            scene.play(
                conn_group.animate(run_time=0.3).set_stroke(
                    color=signal_color, opacity=0.6, width=2
                )
            )
        scene.wait(layer_delay)

    # Reset
    scene.wait(0.5)


def animate_backprop(scene, network, gradient_color=GRADIENT_COLOR):
    """
    Animate gradient signals flowing right-to-left (backpropagation).
    """
    connections, layers = network[0], network[1]

    for i in range(len(layers) - 1, -1, -1):
        neurons = layers[i][0]
        anims = []
        for neuron in neurons:
            target = neuron[-1] if isinstance(neuron, VGroup) else neuron
            anims.append(
                target.animate(rate_func=rate_functions.ease_out_cubic, run_time=0.3)
                .set_stroke(gradient_color, width=3)
            )
        scene.play(*anims)

        if i > 0:
            conn_group = connections[i - 1]
            scene.play(
                conn_group.animate(run_time=0.25).set_stroke(
                    color=gradient_color, opacity=0.5, width=1.5
                )
            )


# ══════════════════════════════════════════════════════════════════════════════
#  ATTENTION PATTERN
# ══════════════════════════════════════════════════════════════════════════════

def create_attention_matrix(tokens, weights=None, size=0.5):
    """
    Visualize a self-attention weight matrix.

    Args:
        tokens: list of token strings, e.g. ["The", "cat", "sat"]
        weights: 2D numpy array of attention weights (auto-generated if None)
        size: cell size
    """
    n = len(tokens)
    if weights is None:
        # Generate a plausible-looking attention pattern
        weights = np.random.dirichlet(np.ones(n), size=n)

    grid = VGroup()
    for r in range(n):
        for c in range(n):
            w = float(weights[r][c])
            cell = Square(
                side_length=size,
                fill_color=ACCENT,
                fill_opacity=w,
                stroke_color=BRAND_STEEL,
                stroke_width=0.5,
            )
            cell.move_to(np.array([c * size, -r * size, 0]))
            grid.add(cell)

    # Row labels (query tokens)
    row_labels = VGroup()
    for r, tok in enumerate(tokens):
        lbl = brand_text(tok, size=T_LABEL, color=TEXT_DIM)
        lbl.next_to(grid[r * n], LEFT, buff=0.15)
        row_labels.add(lbl)

    # Column labels (key tokens)
    col_labels = VGroup()
    for c, tok in enumerate(tokens):
        lbl = brand_text(tok, size=T_LABEL, color=TEXT_DIM)
        lbl.next_to(grid[c], UP, buff=0.15)
        col_labels.add(lbl)

    result = VGroup(grid, row_labels, col_labels)
    result.move_to(ORIGIN)
    return result


# ══════════════════════════════════════════════════════════════════════════════
#  CNN FEATURE MAP VISUALIZATION
# ══════════════════════════════════════════════════════════════════════════════

def create_feature_map(rows=5, cols=5, cell_size=0.3, color=ACCENT, label="Feature Map"):
    """Grid of squares representing a convolutional feature map."""
    import random
    grid = VGroup()
    for r in range(rows):
        for c in range(cols):
            opacity = random.uniform(0.1, 0.9)
            cell = Square(
                side_length=cell_size,
                fill_color=color,
                fill_opacity=opacity,
                stroke_color=color,
                stroke_width=0.5,
                stroke_opacity=0.3,
            )
            cell.move_to(np.array([c * cell_size, -r * cell_size, 0]))
            grid.add(cell)

    lbl = brand_text(label, size=T_LABEL, color=TEXT_DIM)
    grid_group = VGroup(grid)
    grid_group.move_to(ORIGIN)
    lbl.next_to(grid_group, DOWN, buff=0.2)

    return VGroup(grid_group, lbl)


def create_conv_kernel(size=3, cell_size=0.3, values=None, color=BRAND_NOVA):
    """Small grid representing a convolution kernel/filter."""
    if values is None:
        values = np.random.randn(size, size)

    grid = VGroup()
    for r in range(size):
        for c in range(size):
            val = values[r][c]
            cell_color = POSITIVE_COLOR if val >= 0 else NEGATIVE_COLOR
            cell = Square(
                side_length=cell_size,
                fill_color=cell_color,
                fill_opacity=abs(val) / (abs(values).max() + 1e-8) * 0.8,
                stroke_color=color,
                stroke_width=1,
            )
            cell.move_to(np.array([c * cell_size, -r * cell_size, 0]))

            val_text = brand_text(
                f"{val:.1f}", size=T_LABEL * 0.7, color=TEXT
            ).move_to(cell.get_center())

            grid.add(VGroup(cell, val_text))

    grid.move_to(ORIGIN)
    return grid


# ══════════════════════════════════════════════════════════════════════════════
#  DECISION BOUNDARY (2D CLASSIFICATION)
# ══════════════════════════════════════════════════════════════════════════════

def create_2d_scatter(points_a, points_b, ax, color_a=ACCENT, color_b=ACCENT2, radius=0.06):
    """
    Scatter plot for binary classification data.

    Args:
        points_a, points_b: lists of (x, y) tuples
        ax: Manim Axes object
    """
    dots = VGroup()
    for x, y in points_a:
        dots.add(Dot(ax.c2p(x, y), color=color_a, radius=radius))
    for x, y in points_b:
        dots.add(Dot(ax.c2p(x, y), color=color_b, radius=radius))
    return dots


def create_decision_boundary(ax, slope, intercept, color=BRAND_NOVA, width=2):
    """Linear decision boundary line on axes."""
    x_min, x_max = ax.x_range[0], ax.x_range[1]
    y1 = slope * x_min + intercept
    y2 = slope * x_max + intercept
    line = Line(
        ax.c2p(x_min, y1),
        ax.c2p(x_max, y2),
        color=color,
        stroke_width=width,
    )
    return line


# ══════════════════════════════════════════════════════════════════════════════
#  PIPELINE / ARCHITECTURE DIAGRAM
# ══════════════════════════════════════════════════════════════════════════════

def create_pipeline(blocks, spacing=0.5, arrow_color=ACCENT):
    """
    Horizontal pipeline of ml_block items connected by arrows.

    Args:
        blocks: list of dicts {"label": str, "color": color, "details": str}
        spacing: gap between blocks
    """
    mobjects = VGroup()
    for b in blocks:
        block = ml_block(
            label=b.get("label", "Block"),
            color=b.get("color", ACCENT),
            details=b.get("details", ""),
        )
        mobjects.add(block)

    mobjects.arrange(RIGHT, buff=spacing + 0.8)

    arrows = VGroup()
    for i in range(len(mobjects) - 1):
        arrow = Arrow(
            mobjects[i].get_right(),
            mobjects[i + 1].get_left(),
            color=arrow_color,
            stroke_width=2,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )
        arrows.add(arrow)

    return VGroup(mobjects, arrows)
