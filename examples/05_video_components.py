# examples/05_video_components.py
# Demonstrates: Opening, ChapterCard, PauseAndPonder, LowerThirds,
#   Bumper, Watermark, SubscribeCTA, Closing

from manim import *
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *
from components.opening import Opening
from components.closing import Closing
from components.chapter_card import ChapterCard
from components.pause_ponder import PauseAndPonder
from components.bumper import Bumper
from components.watermark import Watermark
from components.subscribe_cta import SubscribeCTA
from components.lower_thirds import LowerThirds


class VideoComponentsShowcase(Scene):
    """Walk through every production video component."""

    def construct(self):
        self.camera.background_color = BG

        # ── 1. Opening ──────────────────────────────────────────────────
        Opening.play(self, episode_number=1, episode_title="Components Demo")

        # ── 2. Watermark (persistent) ───────────────────────────────────
        wm = Watermark.add_with_episode(self, episode_number=1)

        # ── 3. Chapter Card ─────────────────────────────────────────────
        ChapterCard.play(self, chapter=1, title="Brand System", subtitle="Colors, fonts, and helpers")

        # ── 4. Some content ─────────────────────────────────────────────
        self.add(make_grid(opacity=0.06))
        wm2 = Watermark.add_with_episode(self, episode_number=1)

        content = brand_text("Imagine a beautiful neural network here...", size=T_BODY, color=TEXT)
        content.move_to(ORIGIN)
        self.play(FadeIn(content))
        self.wait(1.0)

        # ── 5. Lower Third ──────────────────────────────────────────────
        LowerThirds.speaker(self, name="Nabin", title="ML Engineer @ TheBoringAI", duration=2.0)

        # ── 6. Topic lower third ────────────────────────────────────────
        LowerThirds.topic(self, "Gradient Descent", duration=2.0)

        # ── 7. Bumper transition ────────────────────────────────────────
        Bumper.play(self)
        Bumper.text(self, "Up Next: The Quiz")

        # ── 8. Pause & Ponder ───────────────────────────────────────────
        PauseAndPonder.play(self, "What is the derivative of ReLU at x = 0?", duration=3.0)

        # ── 9. Answer reveal ────────────────────────────────────────────
        PauseAndPonder.reveal(self, "Undefined! But we typically set it to 0.")

        # ── 10. Progress bar ────────────────────────────────────────────
        Watermark.progress_bar(self, progress=0.75)
        self.wait(1.0)

        # ── 11. Subscribe CTA ───────────────────────────────────────────
        SubscribeCTA.popup(self, text="Like & Subscribe!", duration=2.0)

        # ── 12. Closing ─────────────────────────────────────────────────
        Closing.play(self, next_episode="Backpropagation", social_handle="@TheBoringAI")
