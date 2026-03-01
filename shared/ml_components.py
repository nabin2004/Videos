# shared/ml_components.py — Reusable ML/DL visual components for TheBoringAI
#
# Provides building-block mobjects for neural networks, matrices, tensors,
# data flow diagrams, and common ML iconography.

from manim import *
import numpy as np

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from brand import *
from typography import *
from layout import *


# ══════════════════════════════════════════════════════════════════════════════
#  NEURON & LAYER PRIMITIVES
# ══════════════════════════════════════════════════════════════════════════════

def create_neuron(radius=0.25, color=NEURON_COLOR, activated=False):
    """Single neuron circle with optional activation glow."""
    neuron = Circle(
        radius=radius,
        fill_color=color if activated else PANEL,
        fill_opacity=0.9 if activated else 0.6,
        stroke_color=color,
        stroke_width=2,
    )
    if activated:
        glow = Circle(
            radius=radius * 1.4,
            fill_opacity=0,
            stroke_color=color,
            stroke_width=4,
            stroke_opacity=0.3,
        ).move_to(neuron.get_center())
        return VGroup(glow, neuron)
    return neuron


def create_layer(n_neurons, spacing=0.7, color=NEURON_COLOR, label=None, activated_indices=None):
    """Vertical column of neurons representing one layer."""
    if activated_indices is None:
        activated_indices = []
    neurons = VGroup(*[
        create_neuron(color=color, activated=(i in activated_indices))
        for i in range(n_neurons)
    ]).arrange(DOWN, buff=spacing - 0.5)

    layer_group = VGroup(neurons)

    if label:
        lbl = brand_text(label, size=T_CAPTION, color=TEXT_DIM)
        lbl.next_to(neurons, DOWN, buff=0.3)
        layer_group.add(lbl)

    return layer_group


def create_connections(layer_a, layer_b, color=WEIGHT_COLOR, opacity=0.3, width=1):
    """Lines connecting every neuron in layer_a to every neuron in layer_b."""
    connections = VGroup()
    neurons_a = layer_a[0] if isinstance(layer_a[0], VGroup) else [layer_a[0]]
    neurons_b = layer_b[0] if isinstance(layer_b[0], VGroup) else [layer_b[0]]

    for na in neurons_a:
        center_a = na[-1].get_center() if isinstance(na, VGroup) else na.get_center()
        for nb in neurons_b:
            center_b = nb[-1].get_center() if isinstance(nb, VGroup) else nb.get_center()
            line = Line(
                center_a, center_b,
                color=color,
                stroke_width=width,
                stroke_opacity=opacity,
            )
            connections.add(line)
    return connections


def create_neural_network(layer_sizes, layer_colors=None, layer_labels=None, spacing=1.8):
    """
    Full neural network diagram.

    Args:
        layer_sizes: list of int, e.g. [3, 5, 5, 2]
        layer_colors: list of colors per layer (defaults to brand palette)
        layer_labels: list of str labels per layer
        spacing: horizontal distance between layers
    """
    if layer_colors is None:
        default_colors = [INPUT_COLOR] + [HIDDEN_COLOR] * (len(layer_sizes) - 2) + [OUTPUT_COLOR]
        layer_colors = default_colors[:len(layer_sizes)]

    if layer_labels is None:
        layer_labels = [None] * len(layer_sizes)

    layers = VGroup()
    all_connections = VGroup()

    for i, (size, color, label) in enumerate(zip(layer_sizes, layer_colors, layer_labels)):
        layer = create_layer(size, color=color, label=label)
        layers.add(layer)

    layers.arrange(RIGHT, buff=spacing)

    for i in range(len(layers) - 1):
        conns = create_connections(layers[i], layers[i + 1])
        all_connections.add(conns)

    return VGroup(all_connections, layers)


# ══════════════════════════════════════════════════════════════════════════════
#  DATA / TENSOR VISUALIZATION
# ══════════════════════════════════════════════════════════════════════════════

def create_matrix_grid(rows, cols, cell_size=0.45, values=None, color=ACCENT):
    """Grid representation of a matrix with optional numeric values."""
    grid = VGroup()
    texts = VGroup()

    for r in range(rows):
        for c in range(cols):
            cell = Square(
                side_length=cell_size,
                fill_color=PANEL,
                fill_opacity=0.8,
                stroke_color=color,
                stroke_width=1,
            )
            cell.move_to(np.array([c * cell_size, -r * cell_size, 0]))
            grid.add(cell)

            if values is not None and r < len(values) and c < len(values[r]):
                val_text = brand_text(
                    f"{values[r][c]:.1f}",
                    size=T_LABEL,
                    color=TEXT,
                ).move_to(cell.get_center())
                texts.add(val_text)

    result = VGroup(grid, texts)
    result.move_to(ORIGIN)
    return result


def create_tensor_3d(shape=(3, 3, 3), cell_size=0.35, colors=None):
    """
    Pseudo-3D stacked matrix for tensor visualization.
    shape = (depth, rows, cols)
    """
    if colors is None:
        colors = DATA_COLORS
    depth, rows, cols = shape
    layers = VGroup()

    for d in range(depth):
        layer = VGroup()
        for r in range(rows):
            for c in range(cols):
                cell = Square(
                    side_length=cell_size,
                    fill_color=colors[d % len(colors)],
                    fill_opacity=0.4,
                    stroke_color=colors[d % len(colors)],
                    stroke_width=1,
                )
                cell.move_to(np.array([
                    c * cell_size + d * 0.15,
                    -r * cell_size + d * 0.15,
                    0,
                ]))
                layer.add(cell)
        layers.add(layer)

    return layers


# ══════════════════════════════════════════════════════════════════════════════
#  LOSS / TRAINING CURVE
# ══════════════════════════════════════════════════════════════════════════════

def create_loss_curve_axes(x_label="Epoch", y_label="Loss"):
    """Axes configured for a standard training loss plot."""
    ax = Axes(
        x_range=[0, 100, 20],
        y_range=[0, 1, 0.2],
        x_length=8,
        y_length=4,
        axis_config={
            "color": BRAND_STEEL,
            "stroke_width": 1,
            "include_ticks": True,
            "tick_size": 0.05,
        },
        tips=False,
    )
    x_lbl = brand_text(x_label, size=T_LABEL, color=TEXT_DIM)
    x_lbl.next_to(ax.x_axis, DOWN, buff=0.3)
    y_lbl = brand_text(y_label, size=T_LABEL, color=TEXT_DIM)
    y_lbl.next_to(ax.y_axis, LEFT, buff=0.3).rotate(PI / 2)

    return VGroup(ax, x_lbl, y_lbl)


def create_loss_curve(ax, values, color=LOSS_COLOR, add_glow=True):
    """
    Plot a loss curve on given axes.
    values: list of (epoch, loss) tuples
    """
    points = [ax.c2p(x, y) for x, y in values]
    curve = VMobject().set_points_smoothly(points)
    curve.set_stroke(color=color, width=2.5)

    result = VGroup(curve)
    if add_glow:
        glow = curve.copy().set_stroke(color=color, width=10, opacity=0.2)
        result = VGroup(glow, curve)

    return result


# ══════════════════════════════════════════════════════════════════════════════
#  ACTIVATION FUNCTION ICONS
# ══════════════════════════════════════════════════════════════════════════════

def create_activation_plot(func_name="relu", width=2.0, height=1.5, color=ACTIVATION_COLOR):
    """Small activation function plot (ReLU, Sigmoid, Tanh)."""
    ax = Axes(
        x_range=[-3, 3, 1],
        y_range=[-1.5, 1.5, 0.5],
        x_length=width,
        y_length=height,
        axis_config={"color": BRAND_STEEL, "stroke_width": 0.8},
        tips=False,
    )

    funcs = {
        "relu":    lambda x: max(0, x),
        "sigmoid": lambda x: 1 / (1 + np.exp(-x)),
        "tanh":    lambda x: np.tanh(x),
        "leaky_relu": lambda x: x if x >= 0 else 0.01 * x,
    }

    fn = funcs.get(func_name, funcs["relu"])
    graph = ax.plot(fn, color=color, x_range=[-3, 3, 0.05])

    label = brand_text(func_name.upper(), size=T_LABEL, color=color)
    label.next_to(ax, DOWN, buff=0.15)

    return VGroup(ax, graph, label)


# ══════════════════════════════════════════════════════════════════════════════
#  DATA FLOW ARROW
# ══════════════════════════════════════════════════════════════════════════════

def data_flow_arrow(start, end, label="", color=ACCENT):
    """Arrow with optional label for data flow diagrams."""
    arrow = Arrow(
        start, end,
        color=color,
        stroke_width=2,
        max_tip_length_to_length_ratio=0.15,
    )
    group = VGroup(arrow)
    if label:
        lbl = brand_text(label, size=T_LABEL, color=TEXT_DIM)
        lbl.next_to(arrow, UP, buff=0.1)
        group.add(lbl)
    return group


# ══════════════════════════════════════════════════════════════════════════════
#  BRANDED ML BOX (e.g., "Conv2D", "Dense", "LSTM")
# ══════════════════════════════════════════════════════════════════════════════

def ml_block(label, width=2.0, height=0.8, color=ACCENT, details=""):
    """Labeled rectangle representing an ML layer/operation."""
    bg = RoundedRectangle(
        corner_radius=0.1,
        width=width,
        height=height,
        fill_color=PANEL,
        fill_opacity=0.9,
        stroke_color=color,
        stroke_width=1.5,
    )
    lbl = brand_text(label, size=T_BODY, color=color)
    lbl.move_to(bg.get_center())

    group = VGroup(bg, lbl)

    if details:
        det = brand_text(details, size=T_LABEL, color=TEXT_DIM)
        det.next_to(bg, DOWN, buff=0.08)
        group.add(det)

    return group
