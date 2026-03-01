# components/bumper.py — Short transition bumpers between content blocks
#
# Usage:
#   Bumper.play(self)                        — default brand flash
#   Bumper.text(self, "Up Next: Training")   — text bumper

from manim import *

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *