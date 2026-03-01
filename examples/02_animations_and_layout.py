# examples/02_animations_and_layout.py
# Demonstrates: fly_in, pop_in, pulse, type_on, neon_text, glow_stroke,
#   scene_wipe, make_grid, make_particles, callout, metric_card, progress_bar,
#   divider, bullet_list, section_header

from manim import *
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *


class AnimationsShowcase(Scene):
    """Demonstrate every helper from animations.py."""

    def construct(self):
        self.camera.background_color = BG

        # ── Background setup ─────────────────────────────────────────────
        grid = make_grid(opacity=0.08)
        particles = make_particles(n=30, color=ACCENT, radius=0.02)
        self.add(grid, particles)

        # ── 1. Neon text entrance ────────────────────────────────────────
        hero = neon_text("Animation Toolkit", color=ACCENT, size=T_HERO)
        hero.move_to(UP * 2.5)
        self.play(FadeIn(hero, shift=DOWN * 0.3))
        self.wait(0.5)

        # ── 2. fly_in ───────────────────────────────────────────────────
        box1 = ml_block_card("fly_in", BRAND_ELECTRIC)
        box1.move_to(LEFT * 3.5)
        self.play(fly_in(box1, direction=LEFT))
        self.wait(0.3)

        # ── 3. pop_in ───────────────────────────────────────────────────
        box2 = ml_block_card("pop_in", BRAND_PLASMA)
        box2.move_to(ORIGIN)
        self.play(pop_in(box2))
        self.wait(0.3)

        # ── 4. pulse ────────────────────────────────────────────────────
        box3 = ml_block_card("pulse", BRAND_NOVA)
        box3.move_to(RIGHT * 3.5)
        self.play(FadeIn(box3))
        self.play(pulse(box3, scale=1.2))
        self.wait(0.5)

        # ── 5. glow_stroke ──────────────────────────────────────────────
        glow = glow_stroke(box2, color=BRAND_SOLAR, width=8)
        self.play(FadeIn(glow), run_time=0.4)
        self.wait(0.5)
        self.play(FadeOut(glow), run_time=0.3)

        # Clear the cards
        self.play(FadeOut(box1), FadeOut(box2), FadeOut(box3), FadeOut(hero))

        # ── 6. scene_wipe transition ─────────────────────────────────────
        scene_wipe(self, direction=LEFT)

        # ── 7. Section header ────────────────────────────────────────────
        header = section_header("UI Elements", "Callouts, metrics & more")
        header.move_to(UP * 3.0)
        self.play(FadeIn(header, shift=DOWN * 0.2))

        # ── 8. Callout ──────────────────────────────────────────────────
        co = callout("This is a branded callout box", icon="💡", accent=ACCENT)
        co.move_to(UP * 1.2)
        self.play(FadeIn(co, shift=UP * 0.15))
        self.wait(0.5)

        # ── 9. Metric cards ─────────────────────────────────────────────
        m1 = metric_card("Accuracy", "97.3", unit="%", accent=BRAND_ELECTRIC)
        m2 = metric_card("Loss", "0.041", accent=BRAND_NOVA)
        m3 = metric_card("F1 Score", "0.95", accent=BRAND_PLASMA)
        metrics = VGroup(m1, m2, m3).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.5)
        self.play(
            LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in metrics], lag_ratio=0.1),
            run_time=1.0,
        )
        self.wait(0.5)

        # ── 10. Progress bar ────────────────────────────────────────────
        pb = progress_bar(0.73, label="Training Progress", accent=BRAND_SOLAR)
        pb.move_to(DOWN * 2.2)
        self.play(FadeIn(pb, shift=UP * 0.1))
        self.wait(0.5)

        # ── 11. Divider ─────────────────────────────────────────────────
        div = divider(color=ACCENT2, width=10)
        div.move_to(DOWN * 3.0)
        self.play(FadeIn(div))
        self.wait(0.5)

        # ── 12. Bullet list ─────────────────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects])
        grid2 = make_grid(opacity=0.06)
        self.add(grid2)

        bl = bullet_list(["Load dataset", "Preprocess features", "Train model", "Evaluate"], accent=ACCENT)
        bl.move_to(UP * 0.5)
        self.play(FadeIn(bl, shift=RIGHT * 0.2), run_time=1.0)
        self.wait(1.5)

        # ── Finale ──────────────────────────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        fin = neon_text("Animations ✓", color=ACCENT, size=T_H1)
        self.play(FadeIn(fin, scale=0.8))
        self.wait(1.0)


# ── Helper ──────────────────────────────────────────────────────────────────

def ml_block_card(label, color):
    """Quick labeled card for the demo."""
    bg = RoundedRectangle(
        corner_radius=0.12, width=2.4, height=1.0,
        fill_color=PANEL, fill_opacity=0.9,
        stroke_color=color, stroke_width=2,
    )
    txt = brand_text(label, size=T_BODY, color=color)
    txt.move_to(bg)
    return VGroup(bg, txt)
