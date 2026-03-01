# components/pause_ponder.py — "Pause & Ponder" break segments
#
# Drop between sections:
#   PauseAndPonder.play(self, "What happens if we increase the learning rate?")

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *


class PauseAndPonder:
    """