# components/closing.py — Branded series closing / end card
#
# Drop into any scene's construct():
#   Closing.play(self, next_episode="Backpropagation")

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *


class Closing:
    """
    Modular end card. Call Closing.play(scene, ...) at the end of construct().

    Variants: