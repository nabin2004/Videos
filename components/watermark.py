# components/watermark.py — Persistent watermark / series badge
#
# Usage:
#   wm = Watermark.add(self)          — adds badge to corner, returns mob
#   Watermark.add(self, corner=UR)    — change corner

from manim import *

import sys, os