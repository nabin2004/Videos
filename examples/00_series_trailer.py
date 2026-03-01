# examples/00_series_trailer.py
# ═══════════════════════════════════════════════════════════════════════════════
#  TheBoringAI — Series Trailer
#  "From Lines to Losses: The ML Journey"
#
#  A fast-paced, cinematic montage that gives a GLIMPSE of every major ML
#  concept — not a lecture, just enough to ignite curiosity.
#
#  Render:
#    manim -qh examples/00_series_trailer.py SeriesTrailer
# ═══════════════════════════════════════════════════════════════════════════════

from manim import *
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *
from shared.ml_components import (
    ml_block,
    create_activation_plot,
    create_neural_network,
    data_flow_arrow,
)
from shared.math_helpers import (
    sigmoid, relu, tanh, leaky_relu,
    ml_equation, ml_equation_box,
    EQ_LINEAR, EQ_SIGMOID, EQ_MSE, EQ_BCE,
    EQ_RELU, EQ_TANH, EQ_GD_UPDATE, EQ_CROSS_ENTROPY,
)
from shared.nn_visualizer import create_2d_scatter, create_decision_boundary
from components.octopus import (
    OctopusCreature,
    ProfessorOctopus,
    NeuralOctopus,
    OctopusAnimations,
)
from components.opening import Opening
from components.bumper import Bumper
from components.watermark import Watermark


# ─── Timing constants for a trailer feel ────────────────────────────────────
T_FLASH  = 0.30     # very fast flash animation
T_QUICK  = 0.45     # quick show
T_BEAT   = 0.60     # normal beat
T_HOLD   = 1.00     # hold for reading
T_PAUSE  = 0.40     # pause between sections

# ─── Colors for specific models ─────────────────────────────────────────────
C_LINEAR   = BRAND_ELECTRIC
C_LOGISTIC = BRAND_PLASMA
C_RIDGE    = BRAND_SOLAR
C_LASSO    = BRAND_NOVA
C_ELASTIC  = "#39FF14"    # neon green
C_SVM      = "#FF073A"    # hot red
C_TREE     = BRAND_SOLAR
C_FOREST   = "#39FF14"
C_KNN      = BRAND_PLASMA


class SeriesTrailer(Scene):
    """
    TheBoringAI Series Trailer — a cinematic ML montage.

    Flow:
      Opening → Linear Regression → Multivariate → Sigmoid → Logistic
      → Ridge → Lasso → Elastic Net → SVM → Decision Tree → Random Forest
      → KNN → Clustering → Neural Net glimpse → Loss Functions barrage
      → Activation Functions barrage → Octopus finale → End card
    """

    def construct(self):
        self.camera.background_color = BG

        self._cold_open()
        self._act1_linear_world()
        self._act2_regularization()
        self._act3_classifiers()
        self._act4_trees_and_neighbors()
        self._act5_loss_functions()
        self._act6_activation_functions()
        self._finale()

    # ═════════════════════════════════════════════════════════════════════════
    #  COLD OPEN — "What if a straight line could learn?"
    # ═════════════════════════════════════════════════════════════════════════

    def _cold_open(self):
        grid = make_grid(opacity=0.06)
        particles = make_particles(n=50, color=ACCENT, radius=0.015)
        self.add(grid, particles)

        # Series logo
        logo = neon_text(SERIES_NAME, color=ACCENT, size=T_HERO)
        logo.move_to(UP * 0.5)
        logo.scale(0).set_opacity(0)
        self.play(
            logo.animate(rate_func=SPRING, run_time=1.2).scale(1).set_opacity(1)
        )

        tagline = brand_text(
            "Machine Learning — Visualized", size=T_H2, color=TEXT_DIM
        )
        tagline.next_to(logo, DOWN, buff=0.35)
        self.play(FadeIn(tagline, shift=UP * 0.12), run_time=T_BEAT)
        self.wait(0.8)

        # Hook line
        hook = brand_text(
            "What if a straight line could learn?", size=T_BODY, color=BRAND_SOLAR
        )
        hook.next_to(tagline, DOWN, buff=0.5)
        self.play(FadeIn(hook, shift=UP * 0.1), run_time=T_QUICK)
        self.wait(0.6)

        self.play(
            *[FadeOut(m, shift=DOWN * 0.3) for m in [logo, tagline, hook]],
            run_time=T_BEAT,
        )
        self.remove(grid, particles)

    # ═════════════════════════════════════════════════════════════════════════
    #  ACT 1 — The Linear World
    # ═════════════════════════════════════════════════════════════════════════

    def _act1_linear_world(self):
        self.add(make_grid(opacity=0.04))

        # ── 1a. Simple Linear Regression ─────────────────────────────────
        label = neon_text("Linear Regression", color=C_LINEAR, size=T_H2)
        label.to_edge(UP, buff=0.4)
        self.play(FadeIn(label, shift=DOWN * 0.15), run_time=T_FLASH)

        # Scatter + best-fit line
        ax = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=6, y_length=4,
            axis_config={"color": BRAND_STEEL, "stroke_width": 1},
            tips=False,
        ).move_to(DOWN * 0.4)

        np.random.seed(42)
        xs = np.linspace(1, 9, 20)
        ys = 0.8 * xs + 1.0 + np.random.randn(20) * 0.8
        dots = VGroup(*[
            Dot(ax.c2p(x, y), radius=0.06, color=C_LINEAR, fill_opacity=0.8)
            for x, y in zip(xs, ys)
        ])
        self.play(FadeIn(ax), run_time=T_QUICK)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.02),
            run_time=T_BEAT,
        )

        line = ax.plot(lambda x: 0.8 * x + 1.0, color=C_LINEAR, stroke_width=3)
        self.play(Create(line), run_time=T_BEAT)

        # Equation flash
        eq = ml_equation(EQ_LINEAR, color=C_LINEAR).scale(0.9)
        eq.to_edge(RIGHT, buff=0.8).shift(UP * 0.5)
        self.play(FadeIn(eq, shift=LEFT * 0.2), run_time=T_FLASH)
        self.wait(T_PAUSE)

        # ── 1b. Multi-variable — add more dimensions ────────────────────
        multi_label = brand_text("→ Multiple Features", size=T_BODY, color=BRAND_SOLAR)
        multi_label.next_to(label, DOWN, buff=0.15)
        self.play(FadeIn(multi_label, shift=RIGHT * 0.15), run_time=T_FLASH)

        # Morph equation to multivariate
        eq2 = ml_equation(
            r"y = w_1 x_1 + w_2 x_2 + \cdots + w_n x_n + b", color=C_LINEAR
        ).scale(0.85)
        eq2.move_to(eq)
        self.play(Transform(eq, eq2), run_time=T_BEAT)

        # Extra feature lines burst from the original
        lines_extra = VGroup(*[
            ax.plot(
                lambda x, s=s: (0.8 + s * 0.15) * x + 1.0 + s * 0.4,
                color=C_LINEAR, stroke_width=1.5, stroke_opacity=0.35,
            )
            for s in range(-3, 4) if s != 0
        ])
        self.play(FadeIn(lines_extra, shift=UP * 0.08), run_time=T_FLASH)
        self.wait(T_PAUSE)

        # ── 1c. Pass through sigmoid → Logistic Regression ──────────────
        self.play(FadeOut(multi_label), run_time=T_FLASH)
        trans_label = brand_text("+ Sigmoid →", size=T_H2, color=C_LOGISTIC)
        trans_label.next_to(label, RIGHT, buff=0.3)
        self.play(FadeIn(trans_label, shift=RIGHT * 0.2), run_time=T_FLASH)

        # Re-label
        new_label = neon_text("Logistic Regression", color=C_LOGISTIC, size=T_H2)
        new_label.to_edge(UP, buff=0.4)

        # Sigmoid curve overlaid
        sig_curve = ax.plot(
            lambda x: 10 * sigmoid(0.8 * x - 4),
            color=C_LOGISTIC, stroke_width=3,
        )
        self.play(
            FadeOut(lines_extra),
            Transform(label, new_label),
            FadeOut(trans_label),
            Transform(line, sig_curve),
            run_time=T_BEAT,
        )

        # Sigmoid equation
        eq_sig = ml_equation(EQ_SIGMOID, color=C_LOGISTIC).scale(0.85)
        eq_sig.move_to(eq)
        self.play(Transform(eq, eq_sig), run_time=T_QUICK)

        # Recolor dots to two classes
        for i, d in enumerate(dots):
            new_color = C_LINEAR if ys[i] < 5 else C_LOGISTIC
            d.set_fill(new_color)
        self.play(
            *[d.animate.set_fill(opacity=1.0) for d in dots],
            run_time=T_FLASH,
        )
        self.wait(T_PAUSE)

        # Clean exit
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_QUICK)

    # ═════════════════════════════════════════════════════════════════════════
    #  ACT 2 — Regularization Family
    # ═════════════════════════════════════════════════════════════════════════

    def _act2_regularization(self):
        self.add(make_grid(opacity=0.04))

        # ── Base linear regression equation ──────────────────────────────
        base_eq = ml_equation(
            r"\mathcal{L} = \text{MSE}(y, \hat{y})", color=TEXT
        ).scale(0.9).move_to(UP * 2.5)
        self.play(FadeIn(base_eq, shift=DOWN * 0.15), run_time=T_FLASH)
        self.wait(T_PAUSE)

        # ── Ridge Regression: add L2 ────────────────────────────────────
        ridge_label = neon_text("Ridge Regression", color=C_RIDGE, size=T_H2)
        ridge_label.move_to(UP * 1.3)

        ridge_eq = ml_equation(
            r"\mathcal{L} = \text{MSE} + \lambda \sum w_i^2", color=C_RIDGE
        ).scale(0.85).next_to(ridge_label, DOWN, buff=0.3)

        l2_badge = brand_text("+ L2 penalty", size=T_CAPTION, color=C_RIDGE)
        l2_badge.next_to(ridge_eq, RIGHT, buff=0.3)

        self.play(
            FadeIn(ridge_label, shift=DOWN * 0.15),
            FadeIn(ridge_eq, shift=UP * 0.1),
            FadeIn(l2_badge),
            run_time=T_BEAT,
        )

        # Highlight the added term
        highlight_box = SurroundingRectangle(
            ridge_eq[-4:] if len(ridge_eq) > 4 else ridge_eq,
            color=C_RIDGE, buff=0.1, stroke_width=2,
        )
        self.play(Create(highlight_box), run_time=T_FLASH)
        self.wait(T_PAUSE)

        # ── Lasso Regression: add L1 ────────────────────────────────────
        self.play(FadeOut(highlight_box))

        lasso_label = neon_text("Lasso Regression", color=C_LASSO, size=T_H2)
        lasso_label.move_to(DOWN * 0.3)

        lasso_eq = ml_equation(
            r"\mathcal{L} = \text{MSE} + \lambda \sum |w_i|", color=C_LASSO
        ).scale(0.85).next_to(lasso_label, DOWN, buff=0.3)

        l1_badge = brand_text("+ L1 penalty", size=T_CAPTION, color=C_LASSO)
        l1_badge.next_to(lasso_eq, RIGHT, buff=0.3)

        self.play(
            FadeIn(lasso_label, shift=DOWN * 0.15),
            FadeIn(lasso_eq, shift=UP * 0.1),
            FadeIn(l1_badge),
            run_time=T_BEAT,
        )
        self.wait(T_PAUSE)

        # ── Elastic Net: combine both ───────────────────────────────────
        en_label = neon_text("Elastic Net", color=C_ELASTIC, size=T_H2)
        en_label.move_to(DOWN * 2.0)

        en_eq = ml_equation(
            r"\mathcal{L} = \text{MSE} + \lambda_1 \sum |w_i| + \lambda_2 \sum w_i^2",
            color=C_ELASTIC,
        ).scale(0.8).next_to(en_label, DOWN, buff=0.3)

        both_badge = brand_text("L1 + L2", size=T_CAPTION, color=C_ELASTIC)
        both_badge.next_to(en_eq, RIGHT, buff=0.3)

        self.play(
            FadeIn(en_label, shift=DOWN * 0.15),
            FadeIn(en_eq, shift=UP * 0.1),
            FadeIn(both_badge),
            run_time=T_BEAT,
        )

        # Flash: connect Ridge + Lasso → Elastic Net
        arrow_r = Arrow(
            ridge_label.get_bottom(), en_label.get_top() + LEFT * 0.5,
            color=C_RIDGE, stroke_width=2, buff=0.15,
        )
        arrow_l = Arrow(
            lasso_label.get_bottom(), en_label.get_top() + RIGHT * 0.5,
            color=C_LASSO, stroke_width=2, buff=0.15,
        )
        self.play(GrowArrow(arrow_r), GrowArrow(arrow_l), run_time=T_QUICK)
        self.wait(T_HOLD)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_QUICK)

    # ═════════════════════════════════════════════════════════════════════════
    #  ACT 3 — SVM & Classification
    # ═════════════════════════════════════════════════════════════════════════

    def _act3_classifiers(self):
        self.add(make_grid(opacity=0.04))

        title = neon_text("Support Vector Machine", color=C_SVM, size=T_H2)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=T_FLASH)

        # 2D scatter with two classes
        ax = Axes(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1],
            x_length=6, y_length=5,
            axis_config={"color": BRAND_STEEL, "stroke_width": 0.8},
            tips=False,
        ).move_to(DOWN * 0.3)
        self.play(FadeIn(ax), run_time=T_FLASH)

        np.random.seed(99)
        pts_a = [(np.random.randn() - 1.5, np.random.randn() - 1.2) for _ in range(18)]
        pts_b = [(np.random.randn() + 1.5, np.random.randn() + 1.2) for _ in range(18)]
        scatter = create_2d_scatter(pts_a, pts_b, ax, color_a=C_LINEAR, color_b=C_LOGISTIC)
        self.play(FadeIn(scatter), run_time=T_QUICK)

        # Decision boundary
        boundary = create_decision_boundary(ax, slope=-1, intercept=0, color=C_SVM, width=3)
        self.play(Create(boundary), run_time=T_BEAT)

        # Margin lines
        margin_hi = create_decision_boundary(ax, slope=-1, intercept=1.2, color=C_SVM, width=1.5)
        margin_lo = create_decision_boundary(ax, slope=-1, intercept=-1.2, color=C_SVM, width=1.5)
        margin_hi.set_stroke(opacity=0.4)
        margin_lo.set_stroke(opacity=0.4)

        margin_label = brand_text("Maximum Margin", size=T_CAPTION, color=C_SVM)
        margin_label.next_to(ax, RIGHT, buff=0.3).shift(UP * 0.5)

        self.play(
            Create(margin_hi), Create(margin_lo),
            FadeIn(margin_label),
            run_time=T_QUICK,
        )

        # Flash: "Classification AND Regression"
        dual_label = brand_text(
            "Classification  •  Regression", size=T_BODY, color=TEXT
        )
        dual_label.next_to(ax, DOWN, buff=0.3)
        self.play(FadeIn(dual_label, shift=UP * 0.1), run_time=T_FLASH)
        self.wait(T_HOLD)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_QUICK)

    # ═════════════════════════════════════════════════════════════════════════
    #  ACT 4 — Trees, Forests, Neighbors & Friends
    # ═════════════════════════════════════════════════════════════════════════

    def _act4_trees_and_neighbors(self):
        self.add(make_grid(opacity=0.04))

        # ── Decision Tree ────────────────────────────────────────────────
        dt_label = neon_text("Decision Tree", color=C_TREE, size=T_H2)
        dt_label.to_edge(UP, buff=0.4)
        self.play(FadeIn(dt_label, shift=DOWN * 0.15), run_time=T_FLASH)

        tree = self._build_tree(depth=3, color=C_TREE)
        tree.set_height(3.5).move_to(LEFT * 3.0 + DOWN * 0.5)
        self.play(FadeIn(tree, shift=UP * 0.2), run_time=T_BEAT)
        self.wait(T_PAUSE)

        # ── Random Forest: multiply the tree ─────────────────────────────
        rf_label = neon_text("Random Forest", color=C_FOREST, size=T_H2)
        rf_label.to_edge(UP, buff=0.4)
        self.play(Transform(dt_label, rf_label), run_time=T_QUICK)

        # Spawn more trees
        trees = VGroup()
        for i in range(4):
            t = self._build_tree(depth=2, color=[C_TREE, C_FOREST, C_LINEAR, C_LOGISTIC][i])
            t.set_height(2.2)
            trees.add(t)
        trees.arrange(RIGHT, buff=0.5).move_to(RIGHT * 1.5 + DOWN * 0.5)

        self.play(
            tree.animate.set_height(2.2).move_to(LEFT * 4.5 + DOWN * 0.5),
            LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in trees], lag_ratio=0.08),
            run_time=T_BEAT,
        )

        # "Ensemble" bracket
        brace = Brace(VGroup(tree, trees), DOWN, color=BRAND_GHOST)
        brace_text = brand_text("Ensemble of Trees", size=T_CAPTION, color=TEXT_DIM)
        brace_text.next_to(brace, DOWN, buff=0.1)
        self.play(FadeIn(brace), FadeIn(brace_text), run_time=T_QUICK)
        self.wait(T_PAUSE)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_QUICK)
        self.add(make_grid(opacity=0.04))

        # ── KNN ──────────────────────────────────────────────────────────
        knn_label = neon_text("K-Nearest Neighbors", color=C_KNN, size=T_H2)
        knn_label.to_edge(UP, buff=0.4)
        self.play(FadeIn(knn_label, shift=DOWN * 0.15), run_time=T_FLASH)

        # Scatter with query point
        ax2 = Axes(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1],
            x_length=5, y_length=4,
            axis_config={"color": BRAND_STEEL, "stroke_width": 0.8},
            tips=False,
        ).move_to(DOWN * 0.4)
        self.play(FadeIn(ax2), run_time=T_FLASH)

        np.random.seed(77)
        knn_pts_a = [(np.random.randn() * 1.2 - 1.5, np.random.randn() * 1.2) for _ in range(12)]
        knn_pts_b = [(np.random.randn() * 1.2 + 1.5, np.random.randn() * 1.2) for _ in range(12)]
        knn_scatter = create_2d_scatter(knn_pts_a, knn_pts_b, ax2, color_a=C_LINEAR, color_b=C_LOGISTIC)
        self.play(FadeIn(knn_scatter), run_time=T_QUICK)

        # Query point
        query = Dot(ax2.c2p(0.3, 0.5), radius=0.1, color=BRAND_SOLAR, fill_opacity=1)
        query_label = brand_text("?", size=T_H2, color=BRAND_SOLAR)
        query_label.move_to(query).shift(UP * 0.3)
        self.play(FadeIn(query, scale=2), FadeIn(query_label), run_time=T_FLASH)

        # K=3 circle
        k_circle = Circle(radius=1.0, color=C_KNN, stroke_width=2, stroke_opacity=0.6)
        k_circle.move_to(query)
        k_label = brand_text("K = 3", size=T_CAPTION, color=C_KNN)
        k_label.next_to(k_circle, UR, buff=0.1)
        self.play(Create(k_circle), FadeIn(k_label), run_time=T_BEAT)
        self.wait(T_PAUSE)

        # ── Quick flash: other models ────────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_QUICK)
        self.add(make_grid(opacity=0.04))

        models = [
            ("Naïve Bayes", BRAND_ELECTRIC),
            ("PCA", BRAND_PLASMA),
            ("K-Means", BRAND_NOVA),
            ("Gradient Boosting", BRAND_SOLAR),
        ]
        cards = VGroup()
        for name, color in models:
            cards.add(ml_block(name, width=2.8, height=0.8, color=color))
        cards.arrange_in_grid(rows=2, cols=2, buff=0.4).move_to(ORIGIN)

        coming = neon_text("And so much more...", color=TEXT_DIM, size=T_H2)
        coming.to_edge(UP, buff=0.4)

        self.play(FadeIn(coming, shift=DOWN * 0.1), run_time=T_FLASH)
        self.play(
            LaggedStart(*[FadeIn(c, scale=0.8) for c in cards], lag_ratio=0.08),
            run_time=T_BEAT,
        )
        self.wait(T_HOLD)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_QUICK)

    # ═════════════════════════════════════════════════════════════════════════
    #  ACT 5 — Loss Functions Barrage
    # ═════════════════════════════════════════════════════════════════════════

    def _act5_loss_functions(self):
        self.add(make_grid(opacity=0.04))

        title = neon_text("Loss Functions", color=LOSS_COLOR, size=T_H1)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title, shift=DOWN * 0.2, scale=0.9), run_time=T_QUICK)

        # Rapid-fire loss function showcase
        losses = [
            ("MSE",
             r"\frac{1}{n}\sum(y - \hat{y})^2",
             BRAND_ELECTRIC,
             lambda x: x**2),
            ("MAE",
             r"\frac{1}{n}\sum|y - \hat{y}|",
             BRAND_PLASMA,
             lambda x: abs(x)),
            ("Huber",
             r"\begin{cases} \frac{1}{2}x^2 & |x| \le \delta \\ \delta(|x|-\frac{\delta}{2}) \end{cases}",
             BRAND_NOVA,
             lambda x: 0.5 * x**2 if abs(x) <= 1 else abs(x) - 0.5),
            ("Cross-Entropy",
             r"-\sum y \log(\hat{y})",
             BRAND_SOLAR,
             lambda x: -np.log(max(sigmoid(x), 1e-8))),
            ("Hinge",
             r"\max(0, 1 - y \cdot \hat{y})",
             C_SVM,
             lambda x: max(0, 1 - x)),
            ("Log-Cosh",
             r"\sum \log(\cosh(\hat{y} - y))",
             C_ELASTIC,
             lambda x: np.log(np.cosh(x))),
        ]

        # Display losses in a rapid cascade
        ax = Axes(
            x_range=[-3, 3, 1], y_range=[-0.5, 4, 1],
            x_length=4, y_length=3,
            axis_config={"color": BRAND_STEEL, "stroke_width": 0.8},
            tips=False,
        )

        current_group = VGroup()

        for i, (name, tex, color, func) in enumerate(losses):
            # Position: alternate left / right
            side = LEFT if i % 2 == 0 else RIGHT
            x_offset = side * 3.5

            eq_box = ml_equation_box(tex, label=name, color=color, scale=0.65)
            eq_box.move_to(x_offset + DOWN * 0.8)
            eq_box.set_height(min(eq_box.get_height(), 2.2))  # cap height

            # Small plot on the opposite side
            plot_ax = ax.copy().set_height(2.2).move_to(-x_offset + DOWN * 0.8)
            graph = plot_ax.plot(func, x_range=[-3, 3, 0.05], color=color, stroke_width=2.5)

            entry = VGroup(eq_box, plot_ax, graph)

            if current_group.submobjects:
                self.play(FadeOut(current_group, shift=UP * 0.2), run_time=T_FLASH)

            current_group = entry
            self.play(FadeIn(entry, shift=DOWN * 0.15), run_time=T_QUICK)
            self.wait(T_PAUSE)

        self.play(FadeOut(current_group, shift=UP * 0.2), run_time=T_FLASH)

        # Grand flash — ALL loss names at once
        all_names = VGroup()
        for name, _, color, _ in losses:
            t = brand_text(name, size=T_H2, color=color)
            all_names.add(t)
        all_names.arrange_in_grid(rows=2, cols=3, buff=0.5).move_to(DOWN * 0.5)
        self.play(
            LaggedStart(*[FadeIn(n, scale=0.7) for n in all_names], lag_ratio=0.04),
            run_time=T_BEAT,
        )
        self.wait(T_HOLD)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_QUICK)

    # ═════════════════════════════════════════════════════════════════════════
    #  ACT 6 — Activation Functions Barrage
    # ═════════════════════════════════════════════════════════════════════════

    def _act6_activation_functions(self):
        self.add(make_grid(opacity=0.04))

        title = neon_text("Activation Functions", color=ACTIVATION_COLOR, size=T_H1)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title, shift=DOWN * 0.2, scale=0.9), run_time=T_QUICK)

        activations = [
            ("ReLU",        relu,                             BRAND_ELECTRIC),
            ("Sigmoid",     sigmoid,                          BRAND_PLASMA),
            ("Tanh",        tanh,                             BRAND_NOVA),
            ("Leaky ReLU",  lambda x: leaky_relu(x, 0.1),    BRAND_SOLAR),
            ("Swish",       lambda x: x * sigmoid(x),         C_ELASTIC),
            ("GELU",        lambda x: 0.5*x*(1+np.tanh(np.sqrt(2/np.pi)*(x+0.044715*x**3))), C_SVM),
            ("Softplus",    lambda x: np.log(1 + np.exp(x)),  C_KNN),
            ("ELU",         lambda x: x if x >= 0 else np.exp(x)-1, C_LASSO),
        ]

        # Display in a grid — all at once for dramatic effect
        act_ax = Axes(
            x_range=[-4, 4, 1], y_range=[-2, 4, 1],
            x_length=2.8, y_length=2.0,
            axis_config={"color": BRAND_STEEL, "stroke_width": 0.6},
            tips=False,
        )

        plots = VGroup()
        for name, func, color in activations:
            ax_copy = act_ax.copy()
            graph = ax_copy.plot(func, x_range=[-4, 4, 0.05], color=color, stroke_width=2)
            lbl = brand_text(name, size=T_LABEL, color=color)
            lbl.next_to(ax_copy, DOWN, buff=0.08)
            plots.add(VGroup(ax_copy, graph, lbl))

        plots.arrange_in_grid(rows=2, cols=4, buff=0.35).set_height(5.0).move_to(DOWN * 0.3)

        # Dramatic: appear one-by-one FAST then pulse
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.8) for p in plots], lag_ratio=0.06),
            run_time=1.5,
        )
        self.wait(0.5)

        # Pulse each one rapidly
        for p in plots:
            self.play(
                p.animate.scale(1.08),
                run_time=0.08,
                rate_func=there_and_back,
            )

        self.wait(T_HOLD)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_QUICK)

    # ═════════════════════════════════════════════════════════════════════════
    #  FINALE — Octopus + Call to Action
    # ═════════════════════════════════════════════════════════════════════════

    def _finale(self):
        self.add(make_grid(opacity=0.05))
        particles = make_particles(n=60, color=ACCENT, radius=0.02, seed=99)
        self.add(particles)

        # Professor octopus enters
        prof = ProfessorOctopus(height=2.8)
        prof.move_to(ORIGIN + DOWN * 0.3)
        OctopusAnimations.entrance(self, prof)

        OctopusAnimations.say(
            self, prof,
            "This is just the beginning.",
            mood="excited", hold=1.5,
        )

        # Neural octopus pulse
        prof.change_mood("teaching")

        # Grand title
        series_title = neon_text("TheBoringAI", color=ACCENT, size=T_HERO)
        series_title.move_to(UP * 2.8)
        self.play(
            FadeIn(series_title, shift=DOWN * 0.2, scale=0.9),
            run_time=T_BEAT,
        )

        subtitle = brand_text(
            "Every Algorithm. Every Equation. Visualized.",
            size=T_BODY, color=TEXT,
        )
        subtitle.next_to(series_title, DOWN, buff=0.25)
        self.play(FadeIn(subtitle, shift=UP * 0.1), run_time=T_QUICK)

        # CTA
        cta = brand_text("Subscribe → Don't miss Episode 1", size=T_H2, color=BRAND_SOLAR)
        cta.next_to(prof, DOWN, buff=0.8)
        self.play(FadeIn(cta, shift=UP * 0.15), run_time=T_BEAT)

        OctopusAnimations.wave_hello(self, prof, cycles=2)

        self.wait(2.0)

        # Final fade
        self.play(
            *[FadeOut(m, shift=DOWN * 0.2) for m in self.mobjects],
            run_time=1.0,
        )
        self.wait(0.5)

    # ═════════════════════════════════════════════════════════════════════════
    #  Helpers
    # ═════════════════════════════════════════════════════════════════════════

    def _build_tree(self, depth=3, color=BRAND_SOLAR):
        """Build a simple binary tree diagram."""
        nodes = VGroup()
        edges = VGroup()
        positions = {}

        def _add_node(level, index, x, y):
            node = Circle(
                radius=0.15,
                fill_color=color if level == depth else PANEL,
                fill_opacity=0.8 if level == depth else 0.5,
                stroke_color=color, stroke_width=1.5,
            )
            node.move_to(np.array([x, y, 0]))
            nodes.add(node)
            positions[(level, index)] = node

            if level < depth:
                gap = 2.0 / (2 ** level)
                _add_node(level + 1, index * 2, x - gap / 2, y - 1.0)
                _add_node(level + 1, index * 2 + 1, x + gap / 2, y - 1.0)

                child_l = positions[(level + 1, index * 2)]
                child_r = positions[(level + 1, index * 2 + 1)]
                edges.add(Line(node.get_bottom(), child_l.get_top(), color=color, stroke_width=1.5))
                edges.add(Line(node.get_bottom(), child_r.get_top(), color=color, stroke_width=1.5))

        _add_node(0, 0, 0, 0)
        return VGroup(edges, nodes)
