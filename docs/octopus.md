# OctopusCreature — Mascot & Teaching Character

> An 8-armed octopus mascot that holds, compares, counts, and presents
> ML/DL concepts — built entirely from Manim primitives.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Anatomy](#anatomy)
- [Moods](#moods)
- [Variations](#variations)
- [OctopusAnimations](#octopusanimations)
- [OctopusTeaches](#octopusteaches)
- [Cookbook](#cookbook)
- [API Reference](#api-reference)

---

## Quick Start

```python
from components.octopus import OctopusCreature, OctopusAnimations, OctopusTeaches

class MyScene(Scene):
    def construct(self):
        octo = OctopusCreature(mood="happy")
        OctopusAnimations.entrance(self, octo)

        OctopusAnimations.say(self, octo, "Welcome to TheBoringAI!")
        OctopusAnimations.wave_hello(self, octo)

        OctopusAnimations.exit(self, octo)
```

---

## Anatomy

The octopus is a `VGroup` assembled in back-to-front layers:

```
 Layer 6  mouth         — mood-dependent shape
 Layer 5  eyes          — iris + pupil with look_at()
 Layer 4  spots         — organic texture dots
 Layer 3  head          — dome ellipse + glossy highlight
 Layer 2  suckers       — (optional) circles along tentacles
 Layer 1  tentacles     — 8 tapered wavy VMobjects
```

Access any part directly:

```python
octo.head           # VGroup(body_ellipse, highlight)
octo.eyes           # VGroup(left_eye, right_eye)
octo.left_eye       # VGroup(iris, pupil_group)
octo.right_eye
octo.mouth          # VMobject — replaced on mood change
octo.tentacles      # VGroup of 8 tentacles
octo.spots          # VGroup of texture dots
```

---

## Moods

Change the octopus's expression with `octo.change_mood("name")`:

| Mood | Mouth Shape | When to Use |
|------|-------------|-------------|
| `happy` | Upward arc smile | Default, intros, celebrations |
| `teaching` | Open-mouth smile | Explaining concepts |
| `thinking` | Flat line, offset right | Pondering a question |
| `confused` | Wavy squiggle | "This is tricky…" moments |
| `excited` | Open oval | "Eureka!" reveals |
| `surprised` | Open circle | Plot twists, unexpected results |
| `sad` | Downward arc frown | Showing failure cases |
| `sleepy` | Flat line, centered | Boring parts, overfitting jokes |
| `neutral` | Same as thinking | Default fallback |

```python
octo.change_mood("excited")   # instant swap
octo.change_mood("thinking")  # instant swap
```

---

## Variations

### ProfessorOctopus

Adds round glasses and a mortarboard cap. Default color: plasma purple.

```python
prof = ProfessorOctopus()
OctopusAnimations.entrance(self, prof)
OctopusAnimations.say(self, prof, "Let's derive the chain rule!")
```

### BabyOctopus

Smaller (height=1.3), cuter, with oversized eyes. Default color: nova orange.

```python
baby = BabyOctopus()
OctopusAnimations.entrance(self, baby)
OctopusAnimations.think(self, baby, "What even is a gradient?")
```

### NeuralOctopus

Each tentacle uses a different `DATA_COLORS` shade — like neural signals.
Has a `pulse_tentacle()` method to animate firing.

```python
noc = NeuralOctopus()
self.play(FadeIn(noc))
noc.pulse_tentacle(self, 0)  # fire signal on tentacle 0
noc.pulse_tentacle(self, 3)  # fire signal on tentacle 3
```

### DataOctopus

Each tentacle tip is labelled. Perfect for hyperparameters, features, etc.

```python
doc = DataOctopus(labels=[
    "lr", "epochs", "batch", "dropout",
    "decay", "momentum", "β₁", "β₂",
])
self.play(FadeIn(doc))
```

---

## OctopusAnimations

Static helper methods — just pass `(scene, octo, ...)`.

### Entrance / Exit

```python
OctopusAnimations.entrance(self, octo)              # scale-up fade in
OctopusAnimations.entrance(self, octo, direction=LEFT)  # slide from left
OctopusAnimations.exit(self, octo)                   # shrink fade out
```

### Expressions

```python
OctopusAnimations.wave_hello(self, octo)              # wave outer tentacles
OctopusAnimations.wave_hello(self, octo, [2, 5])      # wave specific tentacles
OctopusAnimations.blink_anim(self, octo)              # quick blink
OctopusAnimations.look_around(self, octo)             # glance left → right → center
OctopusAnimations.idle(self, octo, duration=3.0)      # subtle hover + blink
```

### Speech

```python
OctopusAnimations.say(self, octo, "Hello world!")
OctopusAnimations.think(self, octo, "Hmm, what if...?")
```

### Teaching

```python
# Fan items below the octopus
cards = [ml_block("ReLU"), ml_block("Sigmoid"), ml_block("Tanh")]
group = OctopusAnimations.present(self, octo, cards, title="Activations")

# Side-by-side comparison
OctopusAnimations.compare(self, octo, left_plot, right_plot, "SGD", "Adam")

# Count off steps
OctopusAnimations.count_off(self, octo, [
    "Load data", "Preprocess", "Train", "Evaluate"
], layout="arc")

# Playful juggling
OctopusAnimations.juggle(self, octo, [block1, block2, block3])
```

---

## OctopusTeaches

High-level sequences that manage their own entrance / content / exit.

### concept — Title + Bullet Points

```python
OctopusTeaches.concept(self, "Gradient Descent", [
    "Follow the negative gradient",
    "Learning rate controls step size",
    "Converges to local minimum",
])
```

### step_by_step — Enumerated Walk-Through

```python
OctopusTeaches.step_by_step(self, [
    "Load training data",
    "Forward pass",
    "Compute loss",
    "Backpropagate",
    "Update weights",
])
```

### vs — Side-by-Side Comparison

```python
OctopusTeaches.vs(self, sigmoid_plot, relu_plot, "Sigmoid", "ReLU")
```

### quiz — Interactive Multiple Choice

```python
OctopusTeaches.quiz(self,
    "Which activation avoids vanishing gradients?",
    ["Sigmoid", "ReLU", "Tanh", "Step"],
    answer_index=1,
)
```

### pipeline — Left-to-Right Data Flow

```python
OctopusTeaches.pipeline(self, [
    ("Data", BRAND_ELECTRIC),
    ("Feature Eng.", BRAND_PLASMA),
    ("Model", BRAND_NOVA),
    ("Evaluate", BRAND_SOLAR),
])
```

---

## Cookbook

### Hold weights with tentacles

```python
octo = OctopusCreature(mood="teaching", height=2.5)
self.play(FadeIn(octo))

weights = VGroup()
for i in range(8):
    w = brand_text(f"w{i}", size=T_LABEL, color=WEIGHT_COLOR)
    weights.add(w)
octo.hold_items(list(weights))
self.play(*[FadeIn(w) for w in weights])
```

### Professor explains then quizzes

```python
prof = ProfessorOctopus()
OctopusTeaches.concept(self, "Activation Functions", [
    "Add non-linearity to the network",
    "Applied after the linear transformation",
    "Determine which neurons 'fire'",
], octo=prof)

OctopusTeaches.quiz(self,
    "Which is most popular today?",
    ["Sigmoid", "ReLU", "Tanh", "Softmax"],
    answer_index=1, octo=prof,
)
```

### Baby octopus asks a question

```python
baby = BabyOctopus()
OctopusAnimations.entrance(self, baby)
OctopusAnimations.think(self, baby, "Why does loss go down?")
baby.change_mood("excited")
OctopusAnimations.say(self, baby, "Oh! Gradient descent!")
OctopusAnimations.exit(self, baby)
```

### Neural octopus fires signals

```python
noc = NeuralOctopus()
self.play(FadeIn(noc))
for i in range(8):
    noc.pulse_tentacle(self, i, run_time=0.3)
```

### Pipeline with octopus guide

```python
OctopusTeaches.pipeline(self, [
    "Data Collection",
    "Cleaning",
    "Feature Engineering",
    "Training",
    "Validation",
    "Deployment",
])
```

---

## API Reference

### OctopusCreature

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `color` | str | `BRAND_ELECTRIC` | Body color |
| `mood` | str | `"happy"` | Initial expression |
| `height` | float | `2.5` | Height in Manim units |
| `show_suckers` | bool | `False` | Draw sucker circles on tentacles |
| `tentacle_curl` | float | `1.0` | Wave amplitude (0=straight, >1=extra wavy) |

**Instance methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `look_at(target)` | self | Move pupils toward target |
| `look(direction)` | self | Look in unit-direction vector |
| `reset_eyes()` | self | Centre both pupils |
| `blink()` | self | Flatten eyes (instant) |
| `change_mood(mood)` | self | Swap mouth shape |
| `get_tentacle(i)` | VMobject | Tentacle by index (0–7) |
| `get_tentacle_tip(i)` | ndarray | World position of tip |
| `get_all_tips()` | list | All 8 tip positions |
| `hold_item(item, i)` | self | Attach item to tentacle tip |
| `hold_items(items)` | self | Distribute items across tentacles |
| `release_items()` | self | Forget held items |
| `nearest_tentacle_to(target)` | int | Closest tentacle index |
| `get_thought_bubble(text)` | VGroup | Create thought bubble |
| `get_speech_bubble(text)` | VGroup | Create speech bubble |
| `present_items(items)` | VGroup | Position items in fan arc |
| `arrange_comparison(a, b)` | VGroup | Position items for VS |
| `fan_positions(n)` | list | n arc positions |
| `grid_positions(n)` | list | n grid positions |
| `line_positions(n)` | list | n line positions |
