# examples/06_full_mini_episode.py
# A complete mini-episode combining EVERY module:
#   Opening, Watermark, ChapterCard, OctopusCreature, Neural Network,
#   Activation Plots, ML Blocks, PauseAndPonder, OctopusTeaches,
#   Bumper, LowerThirds, SubscribeCTA, Closing

from manim import *
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *
from shared.ml_components import (
    create_neural_network,
    create_activation_plot,
    ml_block,
)
from shared.nn_visualizer import animate_forward_pass
from components.octopus import (
    OctopusCreature,
    ProfessorOctopus,
    NeuralOctopus,
    OctopusAnimations,
    OctopusTeaches,
)
from components.opening import Opening
from components.closing import Closing
from components.chapter_card import ChapterCard
from components.pause_ponder import PauseAndPonder
from components.bumper import Bumper
from components.watermark import Watermark
from components.subscribe_cta import SubscribeCTA
from components.lower_thirds import LowerThirds


class MiniEpisode(Scene):
    """
    Full mini-episode: 'What Is a Neural Network?'

    Demonstrates every single module in the project working together.
    """

    def construct(self):
        self.camera.background_color = BG

        # ═══════════════════════════════════════════════════════════════════
        #  ACT 1 — Opening
        # ═══════════════════════════════════════════════════════════════════

        Opening.play(self, episode_number=1, episode_title="What Is a Neural Network?")
        wm = Watermark.add_with_episode(self, episode_number=1)

        # ═══════════════════════════════════════════════════════════════════
        #  ACT 2 — Octopus introduces the concept
        # ═══════════════════════════════════════════════════════════════════

        ChapterCard.play(self, chapter=1, title="The Big Picture")
        self.add(make_grid(opacity=0.05))
        wm = Watermark.add_with_episode(self, episode_number=1)

        # Professor octopus enters
        prof = ProfessorOctopus(height=2.0)
        prof.move_to(LEFT * 5 + DOWN * 0.5)
        OctopusAnimations.entrance(self, prof)
        prof.look(RIGHT)

        OctopusAnimations.say(
            self, prof,
            "A neural network is a function\nthat learns from data!",
            mood="teaching", hold=2.5,
        )

        LowerThirds.speaker(self, name="Prof. Octopus", title="ML Instructor", duration=2.0)

        # ═══════════════════════════════════════════════════════════════════
        #  ACT 3 — Show a neural network
        # ═══════════════════════════════════════════════════════════════════

        net = create_neural_network(
            [3, 4, 4, 2],
            layer_labels=["Input", "Hidden 1", "Hidden 2", "Output"],
        )
        net.set_height(3.5).move_to(RIGHT * 1.5)
        self.play(FadeIn(net, shift=UP * 0.3), run_time=1.0)
        self.wait(0.5)

        # Forward pass
        OctopusAnimations.say(self, prof, "Watch the signal flow!", mood="excited", hold=0.5)
        animate_forward_pass(self, net, layer_delay=0.1)
        self.wait(0.5)

        # Clean network
        self.play(FadeOut(net))

        # ═══════════════════════════════════════════════════════════════════
        #  ACT 4 — Present activation functions with tentacles
        # ═══════════════════════════════════════════════════════════════════

        Bumper.text(self, "Activation Functions")
        self.add(make_grid(opacity=0.05))
        wm = Watermark.add_with_episode(self, episode_number=1)

        # Move professor to top
        self.play(prof.animate.move_to(UP * 2.0).scale(0.8), run_time=0.5)

        # Present activation function blocks
        act_items = [
            ml_block("ReLU", width=1.4, height=0.6, color=BRAND_ELECTRIC),
            ml_block("Sigmoid", width=1.4, height=0.6, color=BRAND_PLASMA),
            ml_block("Tanh", width=1.4, height=0.6, color=BRAND_NOVA),
        ]
        presented = OctopusAnimations.present(self, prof, act_items, title="Activations")
        self.wait(1.5)
        self.play(FadeOut(presented))

        # Show actual plots
        plots = VGroup(
            create_activation_plot("relu", width=3.0, height=2.0, color=BRAND_ELECTRIC),
            create_activation_plot("sigmoid", width=3.0, height=2.0, color=BRAND_PLASMA),
            create_activation_plot("tanh", width=3.0, height=2.0, color=BRAND_NOVA),
        ).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.5)

        self.play(
            LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in plots], lag_ratio=0.15),
            run_time=1.5,
        )
        self.wait(2.0)
        self.play(FadeOut(plots), FadeOut(prof))

        # ═══════════════════════════════════════════════════════════════════
        #  ACT 5 — Pause & Ponder
        # ═══════════════════════════════════════════════════════════════════

        PauseAndPonder.play(
            self,
            "Why does ReLU work better than Sigmoid\nin deep networks?",
            duration=4.0,
        )
        PauseAndPonder.reveal(
            self,
            "ReLU avoids the vanishing gradient problem\nbecause its derivative is 1 for positive inputs.",
        )

        # ═══════════════════════════════════════════════════════════════════
        #  ACT 6 — Neural octopus demonstrates signal flow
        # ═══════════════════════════════════════════════════════════════════

        ChapterCard.play(self, chapter=2, title="Inside the Neurons")
        self.add(make_grid(opacity=0.05))
        wm = Watermark.add_with_episode(self, episode_number=1)

        neural_octo = NeuralOctopus(height=2.8)
        neural_octo.move_to(ORIGIN)
        OctopusAnimations.entrance(self, neural_octo)

        OctopusAnimations.say(
            self, neural_octo,
            "Each of my tentacles is like\na neural connection!",
            mood="teaching", hold=2.0,
        )

        # Pulse several tentacles to show signal firing
        for i in [0, 2, 5, 7]:
            neural_octo.pulse_tentacle(self, i, run_time=0.4)

        self.wait(0.5)

        # ═══════════════════════════════════════════════════════════════════
        #  ACT 7 — Training pipeline
        # ═══════════════════════════════════════════════════════════════════

        self.play(FadeOut(neural_octo))

        OctopusTeaches.pipeline(self, [
            ("Data", BRAND_ELECTRIC),
            ("Forward Pass", BRAND_PLASMA),
            ("Loss", LOSS_COLOR),
            ("Backprop", GRADIENT_COLOR),
            ("Update", BRAND_SOLAR),
        ])

        # ═══════════════════════════════════════════════════════════════════
        #  ACT 8 — Quiz time
        # ═══════════════════════════════════════════════════════════════════

        Bumper.text(self, "Quiz Time! 🧠")
        self.add(make_grid(opacity=0.05))

        OctopusTeaches.quiz(
            self,
            "What does backpropagation compute?",
            ["Predictions", "Gradients", "Features", "Weights"],
            answer_index=1,
        )

        # ═══════════════════════════════════════════════════════════════════
        #  ACT 9 — Subscribe & Close
        # ═══════════════════════════════════════════════════════════════════

        SubscribeCTA.popup(self, text="Like & Subscribe for more!", duration=2.5)
        Closing.play(self, next_episode="Gradient Descent", social_handle="@TheBoringAI")
