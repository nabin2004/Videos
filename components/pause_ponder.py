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
    Mid-video interactive pause that asks the viewer a question.

    Variants:
        PauseAndPonder.play(scene, question)              — standard pause
        PauseAndPonder.with_choices(scene, q, choices)    — multiple choice
        PauseAndPonder.countdown(scene, question, secs=5) — with timer
        PauseAndPonder.reveal(scene, answer)              — answer reveal
    """

    @staticmethod
    def play(scene, question, duration=4.0, icon="🤔"):
        """Standard pause break: dims screen, shows question, waits."""

        # ── Dim overlay ──────────────────────────────────────────────────
        overlay = Rectangle(
            width=FRAME_W, height=FRAME_H,
            fill_color=BRAND_VOID, fill_opacity=0.75,
            stroke_width=0,
        )
        scene.play(FadeIn(overlay, run_time=FAST))

        # ── Badge ────────────────────────────────────────────────────────
        badge_bg = RoundedRectangle(
            corner_radius=0.15, width=4.5, height=0.65,
            fill_color=ACCENT2, fill_opacity=0.15,
            stroke_color=ACCENT2, stroke_width=1.5,
        ).move_to(UP * 2.0)

        badge_text = brand_text(
            f"{icon}  Pause & Ponder", size=T_BODY, color=ACCENT2
        ).move_to(badge_bg.get_center())

        scene.play(FadeIn(badge_bg), FadeIn(badge_text), run_time=NORMAL)

        # ── Question ─────────────────────────────────────────────────────
        q = brand_text(question, size=T_H2, color=TEXT)
        # Wrap long text
        if q.width > FRAME_W - 3:
            q.scale_to_fit_width(FRAME_W - 3)
        q.move_to(ORIGIN)

        scene.play(FadeIn(q, shift=UP * 0.2, run_time=NORMAL))

        # ── Hint to pause ────────────────────────────────────────────────
        hint = brand_text(
            "⏸  Pause the video and think about it!", size=T_CAPTION, color=TEXT_DIM
        ).move_to(DOWN * 2.0)
        scene.play(FadeIn(hint, run_time=FAST))

        scene.wait(duration)

        # ── Clean up ─────────────────────────────────────────────────────
        scene.play(
            *[FadeOut(m) for m in [overlay, badge_bg, badge_text, q, hint]],
            run_time=FAST,
        )

    @staticmethod
    def with_choices(scene, question, choices, duration=5.0):
        """Pause with multiple-choice options (A, B, C, D)."""

        overlay = Rectangle(
            width=FRAME_W, height=FRAME_H,
            fill_color=BRAND_VOID, fill_opacity=0.75,
            stroke_width=0,
        )
        scene.play(FadeIn(overlay, run_time=FAST))

        # Badge
        badge = brand_text(
            "🤔  Pause & Ponder", size=T_BODY, color=ACCENT2
        ).move_to(UP * 2.8)
        scene.play(FadeIn(badge, run_time=FAST))

        # Question
        q = brand_text(question, size=T_H2, color=TEXT)
        if q.width > FRAME_W - 3:
            q.scale_to_fit_width(FRAME_W - 3)
        q.move_to(UP * 1.5)
        scene.play(FadeIn(q, shift=UP * 0.2, run_time=NORMAL))

        # Choices
        letters = "ABCDEF"
        choice_mobs = VGroup()
        for i, choice in enumerate(choices[:6]):
            letter = brand_text(
                f"{letters[i]}.", size=T_BODY, color=ACCENT
            )
            text = brand_text(choice, size=T_BODY, color=TEXT)
            row = VGroup(letter, text).arrange(RIGHT, buff=0.3)
            choice_mobs.add(row)

        choice_mobs.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        choice_mobs.move_to(DOWN * 0.5)

        scene.play(
            LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in choice_mobs],
                        lag_ratio=0.15, run_time=SLOW)
        )

        hint = brand_text("⏸  Pause and pick your answer!", size=T_CAPTION, color=TEXT_DIM)
        hint.move_to(DOWN * 3.0)
        scene.play(FadeIn(hint, run_time=FAST))

        scene.wait(duration)

        scene.play(
            *[FadeOut(m) for m in [overlay, badge, q, choice_mobs, hint]],
            run_time=FAST,
        )

    @staticmethod
    def countdown(scene, question, seconds=5):
        """Pause with a visible countdown timer."""

        overlay = Rectangle(
            width=FRAME_W, height=FRAME_H,
            fill_color=BRAND_VOID, fill_opacity=0.75,
            stroke_width=0,
        )
        scene.play(FadeIn(overlay, run_time=FAST))

        badge = brand_text("🤔  Pause & Ponder", size=T_BODY, color=ACCENT2)
        badge.move_to(UP * 2.5)
        scene.play(FadeIn(badge, run_time=FAST))

        q = brand_text(question, size=T_H2, color=TEXT)
        if q.width > FRAME_W - 3:
            q.scale_to_fit_width(FRAME_W - 3)
        q.move_to(UP * 0.5)
        scene.play(FadeIn(q, shift=UP * 0.2, run_time=NORMAL))

        # Countdown
        timer = brand_text(str(seconds), size=T_HERO, color=ACCENT)
        timer.move_to(DOWN * 1.5)
        scene.play(FadeIn(timer, run_time=FAST))

        for s in range(seconds - 1, -1, -1):
            new_timer = brand_text(str(s), size=T_HERO, color=ACCENT)
            new_timer.move_to(DOWN * 1.5)
            scene.play(
                ReplacementTransform(timer, new_timer, run_time=0.8),
                rate_func=rate_functions.ease_in_out_cubic,
            )
            timer = new_timer

        scene.play(
            *[FadeOut(m) for m in [overlay, badge, q, timer]],
            run_time=FAST,
        )

    @staticmethod
    def reveal(scene, answer, color=BRAND_SOLAR, duration=2.0):
        """Quick answer reveal after a pause break."""
        overlay = Rectangle(
            width=FRAME_W, height=FRAME_H,
            fill_color=BRAND_VOID, fill_opacity=0.5,
            stroke_width=0,
        )
        scene.play(FadeIn(overlay, run_time=FAST))

        badge = brand_text("✅  Answer", size=T_BODY, color=color).move_to(UP * 1.5)
        ans = brand_text(answer, size=T_H2, color=TEXT)
        if ans.width > FRAME_W - 3:
            ans.scale_to_fit_width(FRAME_W - 3)
        ans.move_to(ORIGIN)

        scene.play(FadeIn(badge, run_time=FAST))
        scene.play(FadeIn(ans, shift=UP * 0.2, run_time=NORMAL))
        scene.wait(duration)
        scene.play(*[FadeOut(m) for m in [overlay, badge, ans]], run_time=FAST)
