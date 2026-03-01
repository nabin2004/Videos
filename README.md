# TheBoringAI

**Machine Learning & Deep Learning — Visualized**

A production-grade Manim animation series that makes the boring parts of AI... not so boring. Every episode is a self-contained, broadcast-quality animation explaining core ML/DL concepts with consistent branding and motion design.

---

## Episodes

| # | Scene | File | Topic |
|---|-------|------|-------|
| 0 | `IntroScene` | `scenes/intro.py` | Series intro & title card |
| 1 | `NeuralNetworkBasicsScene` | `scenes/neural_network_basics.py` | Neurons, layers, forward pass |
| 2 | `GradientDescentScene` | `scenes/gradient_descent.py` | Loss landscape, learning rate |
| 3 | `BackpropagationScene` | `scenes/backpropagation.py` | Chain rule, gradient flow |
| 4 | `ActivationFunctionsScene` | `scenes/activation_functions.py` | ReLU, Sigmoid, Tanh |
| 5 | `LossFunctionsScene` | `scenes/loss_functions.py` | MSE, Cross-Entropy, training curves |
| 6 | `CNNExplainedScene` | `scenes/cnn_explained.py` | Convolution, feature maps, pooling |
| 7 | `AttentionMechanismScene` | `scenes/attention_mechanism.py` | Self-attention, Q/K/V, Transformer |
| 8 | `OutroScene` | `scenes/outro.py` | End card & CTA |

---

## Project Structure

```
TheBoringAI/
├── agents/              # AI prompts for generating new scenes
│   ├── MASTER_PROMPT.md # Main prompt — paste into Claude/GPT
│   └── *.md             # Feature-specific reference docs
├── brand.py             # Color palette & brand constants
├── typography.py        # Font helpers & type scale
├── layout.py            # Grid, positions, safe areas
├── animations.py        # Reusable animation functions & UI elements
├── manim.cfg            # Default render config (1080p 60fps)
├── shared/              # ML/DL-specific building blocks
│   ├── ml_components.py # Neurons, layers, matrices, tensors
│   ├── nn_visualizer.py # Forward pass, backprop, attention, CNN
│   └── math_helpers.py  # Common equations & activation functions
├── scenes/              # One .py file per episode
│   ├── _template.py     # Copy this to start a new scene
│   ├── intro.py
│   ├── neural_network_basics.py
│   ├── gradient_descent.py
│   ├── backpropagation.py
│   ├── activation_functions.py
│   ├── loss_functions.py
│   ├── cnn_explained.py
│   ├── attention_mechanism.py
│   └── outro.py
├── assets/              # Fonts, images, audio
├── output/              # Rendered videos (git-ignored)
├── render_all.sh        # Batch render script
└── pyproject.toml       # Python project config
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install manim numpy
```

### 2. Install fonts (recommended)

- [Inter](https://fonts.google.com/specimen/Inter) — UI text
- [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) — Display titles
- [JetBrains Mono](https://www.jetbrains.com/lp/mono/) — Code snippets

### 3. Preview a scene

```bash
# Fast draft (480p)
manim -pql scenes/intro.py IntroScene

# Production (1080p 60fps)
manim -pqh --fps 60 scenes/intro.py IntroScene
```

### 4. Render all episodes

```bash
chmod +x render_all.sh
./render_all.sh        # 1080p
./render_all.sh ql     # draft
./render_all.sh qk     # 4K
```

---

## Creating New Episodes

1. Copy the template:
   ```bash
   cp scenes/_template.py scenes/my_new_topic.py
   ```

2. Rename the class and fill in content using the shared utilities:
   ```python
   from shared.ml_components import *
   from shared.nn_visualizer import *
   from shared.math_helpers import *
   ```

3. Preview:
   ```bash
   manim -pql scenes/my_new_topic.py MyNewTopicScene
   ```

Alternatively, paste `agents/MASTER_PROMPT.md` into an LLM and ask it to generate a complete scene.

---

## Brand System

| Token | Hex | Usage |
|-------|-----|-------|
| `BG` | `#0A0E1A` | Scene background |
| `ACCENT` | `#00F5FF` | Primary accent (electric cyan) |
| `ACCENT2` | `#BF5AF2` | Secondary accent (plasma purple) |
| `HILIGHT` | `#FF6B35` | Highlights (nova orange) |
| `TEXT` | `#E8EAF0` | Body text |
| `TEXT_DIM` | `#8892A4` | Captions, labels |
| `PANEL` | `#1C2333` | Card backgrounds |

ML-specific semantic colors:
- `NEURON_COLOR` — neuron nodes
- `WEIGHT_COLOR` — connections
- `ACTIVATION_COLOR` — activated neurons
- `LOSS_COLOR` — loss/error
- `GRADIENT_COLOR` — gradient flow

---

## Shared ML/DL Components

### Neural Networks
```python
nn = create_neural_network([3, 5, 5, 2], layer_labels=["In", "H1", "H2", "Out"])
animate_forward_pass(self, nn)
animate_backprop(self, nn)
```

### Equations
```python
eq = ml_equation_box(EQ_ATTENTION, label="Attention", color=ACCENT)
```

### Architecture Diagrams
```python
pipeline = create_pipeline([
    {"label": "Conv2D", "color": ACCENT},
    {"label": "ReLU", "color": BRAND_NOVA},
    {"label": "Dense", "color": ACCENT2},
])
```

### Data Visualization
```python
attn = create_attention_matrix(["The", "cat", "sat"])
fm = create_feature_map(5, 5, color=ACCENT, label="Feature Map")
```

---

## License

MIT

---

*Built with [Manim Community](https://www.manim.community/) v0.18+ · Python 3.9+*
