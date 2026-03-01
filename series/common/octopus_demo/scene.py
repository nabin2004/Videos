# series/common/octopus_demo/scene.py
# Demo scene showcasing the OctopusCreature and all its variations.
# Render: make preview S=series/common/octopus_demo/scene.py C=OctopusDemoScene

from manim import *
import sys, os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

from brand import *
from typography import *
from layout import *
from animations import *
from components.octopus import (
    OctopusCreature,
    ProfessorOctopus,
    BabyOctopus,
    NeuralOctopus,
    DataOctopus,
    OctopusAnimations,
    OctopusTeaches,
)
from shared.ml_components import ml_block


class OctopusDemoScene(Scene):
    """
    Showcase every OctopusCreature feature:
      1. Basic octopus + moods
      2. Variations parade
      3. Teaching sequences (concept, step-by-step, quiz, pipeline)
      4. Holding & presenting items
      5. Comparison & juggling
    """

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self.add(make_grid(opacity=0.06))
        self._intro()
        self._mood_showcase()
        self._variations_parade()
        self._teaching_demos()
        self._tentacle_interactions()
        self._finale()

    # ── 1. Intro ────────────────────────────────────────────────────────────

    def _intro(self):
        title = brand_title("Meet the Octopus!", size=T_H1)
        title.to_edge(UP, buff=0.8)
        self.play(FadeIn(title, shift=DOWN * 0.3))

        octo = OctopusCreature(mood="happy", height=3.0, color=BRAND_ELECTRIC)
        octo.move_to(DOWN * 0.3)
        OctopusAnimations.entrance(self, octo)
        OctopusAnimations.wave_hello(self, octo)

        OctopusAnimations.say(
            self, octo,
            "Hi! I'm your ML/DL guide.\n8 arms, infinite concepts!",
            mood="excited", hold=2.0,
        )

        self.play(FadeOut(title), run_time=0.4)
        OctopusAnimations.exit(self, octo)

    # ── 2. Mood showcase ───────────────────────────────────────────────────

    def _mood_showcase(self):
        section = brand_title("Moods", size=T_H2)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section))

        octo = OctopusCreature(mood="happy", height=2.2)
        octo.move_to(DOWN * 0.5)
        OctopusAnimations.entrance(self, octo)

        moods = ["happy", "teaching", "thinking", "confused",
                 "excited", "surprised", "sad", "sleepy"]

        for mood in moods:
            label = brand_text(mood, size=T_BODY, color=BRAND_SOLAR)
            label.next_to(octo, UP, buff=0.4)
            octo.change_mood(mood)
            self.play(FadeIn(label, shift=DOWN * 0.1), run_time=0.3)
            self.wait(0.6)
            self.play(FadeOut(label), run_time=0.2)

        OctopusAnimations.exit(self, octo)
        self.play(FadeOut(section))

    # ── 3. Variations parade ───────────────────────────────────────────────

    def _variations_parade(self):
        section = brand_title("Variations", size=T_H2)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section))

        variants = [
            ("Professor", ProfessorOctopus(height=2.0)),
            ("Baby", BabyOctopus(height=1.8)),
            ("Neural", NeuralOctopus(height=2.0)),
            ("Data", DataOctopus(
                labels=["lr", "epoch", "batch", "drop", "wd", "mom", "β₁", "β₂"],
                height=2.0,
            )),
        ]

        for name, variant in variants:
            label = brand_text(name, size=T_H2, color=variant.creature_color)
            label.next_to(variant, UP, buff=0.4)
            variant.move_to(DOWN * 0.3)

            OctopusAnimations.entrance(self, variant)
            self.play(FadeIn(label, shift=DOWN * 0.1))
            self.wait(1.2)
            self.play(FadeOut(label))
            OctopusAnimations.exit(self, variant)

        self.play(FadeOut(section))

    # ── 4. Teaching demos ──────────────────────────────────────────────────

    def _teaching_demos(self):
        # Concept
        OctopusTeaches.concept(self, "Gradient Descent", [
            "Follow the negative gradient",
            "Learning rate controls step size",
            "Converges to local minimum",
        ])

        # Step by step
        OctopusTeaches.step_by_step(self, [
            "Forward pass",
            "Compute loss",
            "Backward pass",
            "Update weights",
        ])

        # Quiz
        OctopusTeaches.quiz(
            self,
            "Most popular activation?",
            ["Sigmoid", "ReLU", "Tanh", "Softmax"],
            answer_index=1,
        )

        # Pipeline
        OctopusTeaches.pipeline(self, [
            ("Data", BRAND_ELECTRIC),
            ("Clean", BRAND_PLASMA),
            ("Train", BRAND_NOVA),
            ("Eval", BRAND_SOLAR),
        ])

    # ── 5. Tentacle interactions ───────────────────────────────────────────

    def _tentacle_interactions(self):
        section = brand_title("Tentacle Power!", size=T_H2)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section))

        octo = OctopusCreature(mood="teaching", height=2.5)
        octo.move_to(UP * 1.5)
        OctopusAnimations.entrance(self, octo)

        # Present activation function cards
        cards = VGroup(*[
            ml_block(name, width=1.4, height=0.6, color=color)
            for name, color in [
                ("ReLU", BRAND_ELECTRIC),
                ("Sigmoid", BRAND_PLASMA),
                ("Tanh", BRAND_NOVA),
                ("Softmax", BRAND_SOLAR),
                ("GELU", INPUT_COLOR),
            ]
        ])
        group = OctopusAnimations.present(self, octo, list(cards))
        self.wait(1.5)
        self.play(FadeOut(group))

        # Juggle some data blocks
        data = VGroup(*[
            ml_block(f"x{i}", width=0.7, height=0.5, color=DATA_COLORS[i % len(DATA_COLORS)])
            for i in range(4)
        ])
        jgroup = OctopusAnimations.juggle(self, octo, list(data))
        self.wait(0.5)
        self.play(FadeOut(jgroup))

        OctopusAnimations.exit(self, octo)
        self.play(FadeOut(section))

    # ── 6. Finale ──────────────────────────────────────────────────────────

    def _finale(self):
        octo = OctopusCreature(mood="excited", height=3.0, color=BRAND_ELECTRIC)
        octo.move_to(ORIGIN)
        OctopusAnimations.entrance(self, octo)
        OctopusAnimations.say(
            self, octo,
            "That's the OctopusCreature!\nUse me in your scenes!",
            mood="excited", hold=2.5,
        )
        OctopusAnimations.wave_hello(self, octo, cycles=2)
        OctopusAnimations.exit(self, octo)
