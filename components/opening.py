# components/opening.py — Branded series opening / cold open
#
# Drop into any scene's construct():
#   Opening.play(self, episode_number=1, episode_title="Neural Networks 101")

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *


class Opening:
    """
    Modular opening sequence. Call Opening.play(scene, ...) at the top of construct().

    Variants:
        Opening.play(scene)                     — default series intro
        Opening.play(scene, episode_number=3,
                     episode_title="Backprop")  — episode-specific opener