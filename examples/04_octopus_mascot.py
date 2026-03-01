# examples/04_octopus_mascot.py
# Demonstrates: OctopusCreature, moods, ProfessorOctopus, BabyOctopus,
#   NeuralOctopus, DataOctopus, OctopusAnimations, OctopusTeaches,
#   holding/presenting items, thought/speech bubbles, teaching helpers

from manim import *
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *
from shared.ml_components import ml_block
from components.octopus import (
    OctopusCreature,
    ProfessorOctopus,
    BabyOctopus,
    NeuralOctopus,
    DataOctopus,
    OctopusAnimations,
    OctopusTeaches,
)


class OctopusMascotShowcase(Scene):
    """Full showcase of the OctopusCreature mascot system."""

    def construct(self):
        self.camera.background_color = BG
        self.add(make_grid(opacity=0.05))

        self._intro()
        self._moods()
        self._variations()
        self._holding_items()
        self._teaching_concept()
        self._teaching_quiz()

    # ─────────────────────────────────────────────────────────────────────────

    def _intro(self):
        """Basic octopus entrance + wave + speech bubble."""
        title = neon_text("Meet the Octopus!", color=ACCENT, size=T_H1)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        octo = OctopusCreature(mood="happy", height=2.5)
        octo.move_to(ORIGIN)
        OctopusAnimations.entrance(self, octo)
        OctopusAnimations.wave_hello(self, octo)
        OctopusAnimations.say(self, octo, "Hi! I'm your ML guide!", mood="excited", hold=2.0)

        OctopusAnimations.idle(self, octo, duration=1.5)
        self.play(FadeOut(title), FadeOut(octo))

    def _moods(self):
        """Cycle through all moods side by side."""
        title = neon_text("Moods", color=ACCENT2, size=T_H1)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        moods = ["happy", "thinking", "confused", "excited", "surprised",
                 "teaching", "sleepy", "sad", "neutral"]

        mood_row = VGroup()
        for m in moods:
            o = OctopusCreature(mood=m, height=1.2)
            lbl = brand_text(m, size=T_LABEL, color=TEXT_DIM)
            lbl.next_to(o, DOWN, buff=0.1)
            mood_row.add(VGroup(o, lbl))
        mood_row.arrange(RIGHT, buff=0.3).set_width(13).move_to(DOWN * 0.3)

        self.play(
            LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in mood_row], lag_ratio=0.06),
            run_time=2.0,
        )
        self.wait(2.0)
        self.play(FadeOut(mood_row), FadeOut(title))

    def _variations(self):
        """Show all four variations."""
        title = neon_text("Variations", color=BRAND_NOVA, size=T_H1)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        prof = ProfessorOctopus(height=2.0)
        prof_lbl = brand_text("Professor", size=T_CAPTION, color=BRAND_PLASMA)

        baby = BabyOctopus(height=1.5)
        baby_lbl = brand_text("Baby", size=T_CAPTION, color=BRAND_NOVA)

        neural = NeuralOctopus(height=2.0)
        neural_lbl = brand_text("Neural", size=T_CAPTION, color=BRAND_ELECTRIC)

        data = DataOctopus(labels=["lr", "epochs", "batch", "drop", "decay", "mom", "β₁", "β₂"], height=2.0)
        data_lbl = brand_text("Data", size=T_CAPTION, color=BRAND_PLASMA)

        variants = VGroup()
        for octo, lbl in [(prof, prof_lbl), (baby, baby_lbl), (neural, neural_lbl), (data, data_lbl)]:
            lbl.next_to(octo, DOWN, buff=0.15)
            variants.add(VGroup(octo, lbl))
        variants.arrange(RIGHT, buff=1.0).move_to(DOWN * 0.3)

        for v in variants:
            self.play(FadeIn(v, shift=UP * 0.2), run_time=0.6)
            self.wait(0.3)

        # Fire a pulse on neural octopus
        neural.pulse_tentacle(self, 2, color=BRAND_SOLAR)
        neural.pulse_tentacle(self, 6, color=BRAND_NOVA)

        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def _holding_items(self):
        """Octopus holds and presents ML blocks."""
        title = neon_text("Tentacle Interactions", color=BRAND_SOLAR, size=T_H1)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        octo = OctopusCreature(mood="teaching", height=2.2)
        octo.move_to(UP * 0.5)
        OctopusAnimations.entrance(self, octo)

        # Present activation functions
        items = [
            ml_block("ReLU", width=1.5, height=0.6, color=BRAND_ELECTRIC),
            ml_block("Sigmoid", width=1.5, height=0.6, color=BRAND_PLASMA),
            ml_block("Tanh", width=1.5, height=0.6, color=BRAND_NOVA),
            ml_block("Softmax", width=1.5, height=0.6, color=BRAND_SOLAR),
        ]
        group = OctopusAnimations.present(self, octo, items, title="Activation Functions")
        self.wait(1.5)

        # Juggle some tensors
        self.play(FadeOut(group))
        tensors = [
            ml_block(f"x{i}", width=0.8, height=0.5, color=DATA_COLORS[i])
            for i in range(4)
        ]
        juggled = OctopusAnimations.juggle(self, octo, tensors, cycles=2)
        self.wait(0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

    def _teaching_concept(self):
        """OctopusTeaches.concept — bullet point lesson."""
        OctopusTeaches.concept(
            self,
            "Gradient Descent",
            [
                "Initialize weights randomly",
                "Compute loss on training batch",
                "Calculate gradients via backprop",
                "Update weights: w ← w − α∇L",
                "Repeat until convergence",
            ],
        )
        self.wait(0.3)

    def _teaching_quiz(self):
        """OctopusTeaches.quiz — interactive question."""
        OctopusTeaches.quiz(
            self,
            "Which avoids vanishing gradients?",
            ["Sigmoid", "ReLU", "Tanh", "Step"],
            answer_index=1,
        )

        # Finale
        fin = neon_text("Octopus Mascot ✓", color=ACCENT, size=T_H1)
        self.play(FadeIn(fin, scale=0.8))
        self.wait(1.0)
