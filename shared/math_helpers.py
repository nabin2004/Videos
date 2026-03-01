# shared/math_helpers.py — Math & equation helpers for ML/DL animations
#
# Common equations, loss functions, and mathematical notation used
# throughout TheBoringAI series.

from manim import *
import numpy as np

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from brand import *
from typography import *
from layout import *


# ══════════════════════════════════════════════════════════════════════════════
#  COMMON ML/DL EQUATIONS (LaTeX strings)
# ══════════════════════════════════════════════════════════════════════════════

# Linear Regression
EQ_LINEAR        = r"y = \mathbf{w}^T \mathbf{x} + b"
EQ_MSE           = r"\mathcal{L} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2"

# Logistic Regression / Sigmoid
EQ_SIGMOID       = r"\sigma(z) = \frac{1}{1 + e^{-z}}"
EQ_BCE           = r"\mathcal{L} = -\frac{1}{n}\sum_{i=1}^{n}\left[y_i\log(\hat{y}_i) + (1-y_i)\log(1-\hat{y}_i)\right]"

# Softmax
EQ_SOFTMAX       = r"\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}"
EQ_CROSS_ENTROPY = r"\mathcal{L} = -\sum_{c=1}^{C} y_c \log(\hat{y}_c)"

# Gradient Descent
EQ_GD_UPDATE     = r"\theta \leftarrow \theta - \alpha \nabla_\theta \mathcal{L}"
EQ_SGD           = r"\theta_{t+1} = \theta_t - \alpha \nabla_\theta \mathcal{L}(\theta_t; x^{(i)}, y^{(i)})"

# Adam Optimizer
EQ_ADAM_M        = r"m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t"
EQ_ADAM_V        = r"v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2"
EQ_ADAM_UPDATE   = r"\theta_{t+1} = \theta_t - \frac{\alpha \hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}"

# Neural Network
EQ_FORWARD       = r"z^{[l]} = W^{[l]} a^{[l-1]} + b^{[l]}"
EQ_ACTIVATION    = r"a^{[l]} = g(z^{[l]})"
EQ_RELU          = r"\text{ReLU}(z) = \max(0, z)"
EQ_TANH          = r"\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}"

# Backpropagation
EQ_CHAIN_RULE    = r"\frac{\partial \mathcal{L}}{\partial w} = \frac{\partial \mathcal{L}}{\partial a} \cdot \frac{\partial a}{\partial z} \cdot \frac{\partial z}{\partial w}"

# Attention
EQ_ATTENTION     = r"\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V"

# Batch Normalization
EQ_BATCHNORM     = r"\hat{x}_i = \frac{x_i - \mu_\mathcal{B}}{\sqrt{\sigma_\mathcal{B}^2 + \epsilon}}"

# Dropout
EQ_DROPOUT       = r"h' = h \odot m, \quad m_i \sim \text{Bernoulli}(p)"

# Convolution
EQ_CONV          = r"(f * g)(t) = \sum_{\tau} f(\tau) \cdot g(t - \tau)"


# ══════════════════════════════════════════════════════════════════════════════
#  EQUATION DISPLAY HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def ml_equation(tex_string, color=TEXT, scale=1.0):
    """Create a nicely-formatted ML equation."""
    eq = MathTex(tex_string, color=color)
    eq.scale(scale)
    return eq


def ml_equation_box(tex_string, label="", color=ACCENT, scale=0.9):
    """Equation inside a branded panel with optional label."""
    eq = MathTex(tex_string, color=TEXT).scale(scale)

    bg = RoundedRectangle(
        corner_radius=0.15,
        width=eq.width + 1.0,
        height=eq.height + 0.8,
        fill_color=PANEL,
        fill_opacity=0.9,
        stroke_color=color,
        stroke_width=1.5,
    )
    eq.move_to(bg.get_center())

    group = VGroup(bg, eq)

    if label:
        lbl = brand_text(label, size=T_CAPTION, color=color)
        lbl.next_to(bg, UP, buff=0.15, aligned_edge=LEFT)
        group = VGroup(lbl, bg, eq)

    return group


def equation_sequence(equations, labels=None, spacing=0.8):
    """
    Vertically stacked sequence of equations (e.g., derivation steps).

    Args:
        equations: list of LaTeX strings
        labels: optional list of step labels
        spacing: vertical gap
    """
    items = VGroup()
    for i, eq_str in enumerate(equations):
        eq = ml_equation(eq_str, scale=0.85)
        row = VGroup()

        if labels and i < len(labels):
            lbl = brand_text(labels[i], size=T_CAPTION, color=ACCENT2)
            lbl.next_to(eq, LEFT, buff=0.4)
            row.add(lbl)

        row.add(eq)
        items.add(row)

    items.arrange(DOWN, buff=spacing, aligned_edge=LEFT)
    return items


# ══════════════════════════════════════════════════════════════════════════════
#  FUNCTION PLOTTING HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def plot_function(ax, func, x_range=None, color=ACCENT, width=2.5, add_glow=True):
    """
    Plot a function on axes with optional glow effect.

    Args:
        ax: Manim Axes object
        func: callable f(x) -> y
        x_range: [min, max, step] (defaults to ax range)
        color: line color
        width: stroke width
        add_glow: whether to add a glow underneath
    """
    if x_range is None:
        x_range = [ax.x_range[0], ax.x_range[1], 0.05]

    graph = ax.plot(func, x_range=x_range, color=color, stroke_width=width)

    if add_glow:
        glow = graph.copy().set_stroke(color=color, width=width * 4, opacity=0.15)
        return VGroup(glow, graph)

    return graph


def sigmoid(x):
    """Sigmoid activation function."""
    return 1.0 / (1.0 + np.exp(-x))


def relu(x):
    """ReLU activation function."""
    return np.maximum(0, x)


def tanh(x):
    """Tanh activation function."""
    return np.tanh(x)


def leaky_relu(x, alpha=0.01):
    """Leaky ReLU activation function."""
    return np.where(x >= 0, x, alpha * x)


def softmax(x):
    """Softmax function for a 1-D array."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()
