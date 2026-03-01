# series/common/outro/scene.py
# Reusable series outro — can be rendered standalone or imported.
from manim import *
import sys, os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

from brand import *
from typography import *
from layout import *
from animations import *
from components import Closing, SubscribeCTA


class SeriesOutroScene(Scene):
    """Generic series outro with CTA."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        SubscribeCTA.end_screen(self, handle="@TheBoringAI")
        Closing.play(self, next_episode="", social_handle="@TheBoringAI")
