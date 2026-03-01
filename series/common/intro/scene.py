# series/common/intro/scene.py
# Reusable series intro — can be rendered standalone or imported.
from manim import *
import sys, os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

from brand import *
from typography import *
from layout import *
from animations import *
from components import Opening


class SeriesIntroScene(Scene):
    """Generic series intro. Override episode_number/title for per-episode use."""
    episode_number = 0
    episode_title = "TheBoringAI"
    subtitle = ""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        Opening.play(self,
                     episode_number=self.episode_number,
                     episode_title=self.episode_title,
                     subtitle=self.subtitle)
