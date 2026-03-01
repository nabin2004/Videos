# examples/01_brand_and_typography.py
# Demonstrates: brand palette, typography helpers, math/code blocks, gradients

from manim import *
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *


class BrandShowcase(Scene):
    """Show off the TheBoringAI brand system — palette, fonts, and helpers."""

    def construct(self):
        self.camera.background_color = BG

        # ── 1. Title ─────────────────────────────────────────────────────
        title = brand_title("TheBoringAI Brand System")
        title.move_to(POS_TITLE)
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(0.5)

        # ── 2. Color Palette ─────────────────────────────────────────────
        palette_colors = [
            ("ELECTRIC", BRAND_ELECTRIC),
            ("PLASMA", BRAND_PLASMA),
            ("NOVA", BRAND_NOVA),
            ("SOLAR", BRAND_SOLAR),
            ("GHOST", BRAND_GHOST),
            ("MIDNIGHT", BRAND_MIDNIGHT),
        ]

        swatches = VGroup()
        for name, color in palette_colors:
            rect = RoundedRectangle(
                corner_radius=0.08, width=1.6, height=0.9,
                fill_color=color, fill_opacity=1.0,
                stroke_color=WHITE, stroke_width=1,
            )
            lbl = brand_text(name, size=T_LABEL, color=BG if color == BRAND_GHOST else TEXT)
            lbl.move_to(rect.get_center())
            swatches.add(VGroup(rect, lbl))

        swatches.arrange(RIGHT, buff=0.25)
        swatches.move_to(UP * 1.0)
        self.play(
            LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in swatches], lag_ratio=0.08),
            run_time=1.2,
        )
        self.wait(1.0)

        # ── 3. Typography Scale ──────────────────────────────────────────
        self.play(FadeOut(swatches, shift=UP * 0.3))

        type_samples = VGroup(
            brand_text("T_HERO  — Space Grotesk Bold", size=T_HERO, color=ACCENT, font=FONT_DISPLAY),
            brand_text("T_H1  — Inter Regular", size=T_H1, color=TEXT),
            brand_text("T_H2  — Sub-heading", size=T_H2, color=TEXT),
            brand_text("T_BODY — Body text for explanations", size=T_BODY, color=TEXT),
            brand_text("T_CAPTION — Captions & footnotes", size=T_CAPTION, color=TEXT_DIM),
            brand_text("T_LABEL — Tiny labels", size=T_LABEL, color=TEXT_DIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        type_samples.move_to(DOWN * 0.3)

        self.play(
            LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in type_samples], lag_ratio=0.08),
            run_time=1.5,
        )
        self.wait(1.5)

        # ── 4. Math & Code ───────────────────────────────────────────────
        self.play(FadeOut(type_samples, shift=LEFT * 0.3))

        eq = brand_math(r"L = -\sum_{i} y_i \log(\hat{y}_i)", color=ACCENT)
        eq.scale(1.4).move_to(UP * 0.5)
        eq_label = brand_text("Cross-Entropy Loss", size=T_CAPTION, color=TEXT_DIM)
        eq_label.next_to(eq, DOWN, buff=0.3)

        self.play(FadeIn(eq, shift=UP * 0.15), FadeIn(eq_label))
        self.wait(1.5)

        # ── 5. Data Colors ───────────────────────────────────────────────
        self.play(FadeOut(eq), FadeOut(eq_label))

        data_label = brand_text("DATA_COLORS sequence:", size=T_BODY, color=TEXT)
        data_label.move_to(UP * 1.0)

        dots = VGroup()
        for i, c in enumerate(DATA_COLORS):
            d = Circle(radius=0.3, fill_color=c, fill_opacity=1, stroke_width=0)
            num = brand_text(str(i + 1), size=T_LABEL, color=BG)
            num.move_to(d)
            dots.add(VGroup(d, num))
        dots.arrange(RIGHT, buff=0.4).move_to(DOWN * 0.3)

        self.play(FadeIn(data_label), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.1))
        self.wait(1.0)

        # ── Cleanup ──────────────────────────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        thanks = neon_text("Brand System ✓", color=ACCENT, size=T_H1)
        self.play(FadeIn(thanks, scale=0.8))
        self.wait(1.0)
