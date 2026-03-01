# animations.py — Reusable animation helpers & UI elements for TheBoringAI

from manim import *
from brand import *
from typography import *
from layout import *

# ── TIMING ───────────────────────────────────────────────────────────────────
FAST   = 0.35
NORMAL = 0.6
SLOW   = 1.0
EPIC   = 1.8

# ── EASING SHORTCUTS ─────────────────────────────────────────────────────────
EASE_OUT  = rate_functions.ease_out_cubic
EASE_IN   = rate_functions.ease_in_cubic
EASE_IO   = rate_functions.ease_in_out_cubic
SPRING    = rate_functions.ease_out_back      # slight overshoot = "springy"
SMOOTH_   = rate_functions.smooth             # manim default smooth


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRANCE ANIMATIONS
# ══════════════════════════════════════════════════════════════════════════════

def fly_in(mob, direction=DOWN, **kwargs):
    """Object slides in from a direction while fading up."""
    start = mob.get_center()
    mob.shift(direction * 2).set_opacity(0)
    return AnimationGroup(
        mob.animate(rate_func=EASE_OUT, run_time=NORMAL).move_to(start),
        mob.animate(rate_func=EASE_OUT, run_time=NORMAL).set_opacity(1),
        **kwargs,
    )


def pop_in(mob, **kwargs):
    """Scale from 0 with a spring overshoot — great for icons and cards."""
    mob.scale(0).set_opacity(0)
    return AnimationGroup(
        mob.animate(rate_func=SPRING, run_time=NORMAL).scale(1),
        mob.animate(rate_func=EASE_OUT, run_time=FAST).set_opacity(1),
        **kwargs,
    )


def type_on(mob, **kwargs):
    """Typewriter effect for Text mobjects."""
    return AddTextLetterByLetter(mob, time_per_char=0.04, **kwargs)


# ══════════════════════════════════════════════════════════════════════════════
#  EMPHASIS ANIMATIONS
# ══════════════════════════════════════════════════════════════════════════════

def pulse(mob, scale=1.12, **kwargs):
    """Scale up and back — draws attention to a specific element."""
    return Succession(
        mob.animate(rate_func=EASE_IO, run_time=FAST).scale(scale),
        mob.animate(rate_func=EASE_IO, run_time=FAST).scale(1 / scale),
        **kwargs,
    )


def glow_stroke(mob, color=BRAND_ELECTRIC, width=6):
    """Returns a glowing copy to layer beneath the original."""
    glow = mob.copy().set_stroke(color=color, width=width, opacity=0.4)
    return glow


# ══════════════════════════════════════════════════════════════════════════════
#  TRANSITIONS
# ══════════════════════════════════════════════════════════════════════════════

def scene_wipe(scene, direction=LEFT):
    """Full-screen bar wipe transition between scene sections."""
    bar = Rectangle(
        width=FRAME_W * 2, height=FRAME_H,
        fill_color=BRAND_VOID, fill_opacity=1,
        stroke_width=0,
    ).move_to(ORIGIN - direction * FRAME_W)
    scene.add(bar)
    scene.play(bar.animate(rate_func=EASE_IO, run_time=SLOW).shift(direction * FRAME_W * 2))
    scene.remove(bar)


# ══════════════════════════════════════════════════════════════════════════════
#  DECORATIVE / BACKGROUND
# ══════════════════════════════════════════════════════════════════════════════

def make_grid(rows=10, cols=18, color=BRAND_STEEL, opacity=0.15):
    """Subtle background grid."""
    lines = VGroup()
    for r in range(rows + 1):
        y = -FRAME_H / 2 + r * (FRAME_H / rows)
        lines.add(
            Line(LEFT * FRAME_W / 2, RIGHT * FRAME_W / 2,
                 color=color, stroke_opacity=opacity, stroke_width=0.5).move_to(UP * y)
        )
    for c in range(cols + 1):
        x = -FRAME_W / 2 + c * (FRAME_W / cols)
        lines.add(
            Line(UP * FRAME_H / 2, DOWN * FRAME_H / 2,
                 color=color, stroke_opacity=opacity, stroke_width=0.5).move_to(RIGHT * x)
        )
    return lines


def make_particles(n=40, color=BRAND_ELECTRIC, radius=0.03, seed=42):
    """Floating dot field — adds depth and energy to backgrounds."""
    import random
    random.seed(seed)
    dots = VGroup(*[
        Dot(
            point=[random.uniform(-6, 6), random.uniform(-3.5, 3.5), 0],
            radius=radius, color=color,
            fill_opacity=random.uniform(0.2, 0.7),
        )
        for _ in range(n)
    ])
    return dots


# ══════════════════════════════════════════════════════════════════════════════
#  STANDARD UI ELEMENTS
# ══════════════════════════════════════════════════════════════════════════════

def callout(text, icon="→", accent=ACCENT, width=6):
    """Branded info box with icon and text body."""
    bg   = RoundedRectangle(
        corner_radius=0.15, width=width, height=1.1,
        fill_color=PANEL, fill_opacity=1,
        stroke_color=accent, stroke_width=1.5,
    )
    ico  = brand_text(icon, color=accent, size=T_H2)
    body = brand_text(text, size=T_BODY).next_to(ico, RIGHT, buff=U)
    group = VGroup(ico, body).move_to(bg.get_center())
    return VGroup(bg, group)


def metric_card(label, value, unit="", accent=ACCENT):
    """KPI card showing a large value with label."""
    bg    = RoundedRectangle(
        corner_radius=0.2, width=3, height=2,
        fill_color=PANEL, fill_opacity=1,
        stroke_color=accent, stroke_width=1,
    )
    val   = brand_text(value, size=T_H1, color=accent)
    unt   = brand_text(unit,  size=T_BODY, color=TEXT_DIM).next_to(val, RIGHT, aligned_edge=DOWN)
    lbl   = brand_text(label, size=T_CAPTION, color=TEXT_DIM).next_to(val, DOWN, buff=U)
    inner = VGroup(val, unt, lbl).move_to(bg.get_center())
    return VGroup(bg, inner)


def progress_bar(pct, width=8, label="", accent=ACCENT):
    """Animated fill bar."""
    track = RoundedRectangle(
        corner_radius=0.12, width=width, height=0.28,
        fill_color=BRAND_STEEL, fill_opacity=1, stroke_width=0,
    )
    fill  = RoundedRectangle(
        corner_radius=0.12, width=max(width * pct, 0.01), height=0.28,
        fill_color=accent, fill_opacity=1, stroke_width=0,
    ).align_to(track, LEFT)
    lbl   = brand_text(label, size=T_CAPTION, color=TEXT_DIM).next_to(track, UP, buff=U)
    pct_t = brand_text(f"{int(pct * 100)}%", size=T_CAPTION, color=accent).next_to(track, RIGHT, buff=U)
    return VGroup(track, fill, lbl, pct_t)


def divider(color=ACCENT, width=10, opacity=0.4):
    """Subtle horizontal rule between content sections."""
    return Line(LEFT * width / 2, RIGHT * width / 2,
                color=color, stroke_opacity=opacity, stroke_width=1)


def neon_text(content, color=ACCENT, size=T_H1):
    """Layered glow effect — good for hero titles."""
    main  = brand_text(content, color=color, size=size)
    glow1 = main.copy().set_stroke(color=color, width=12, opacity=0.15)
    glow2 = main.copy().set_stroke(color=color, width=6,  opacity=0.30)
    return VGroup(glow1, glow2, main)


def bullet_list(items, accent=ACCENT, gap=0.55):
    """Bulleted list of text items."""
    rows = VGroup()
    for item in items:
        dot  = Dot(radius=0.06, color=accent)
        text = brand_text(item, size=T_BODY)
        row  = VGroup(dot, text).arrange(RIGHT, buff=0.2)
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=gap)
    return rows


def section_header(title, subtitle=""):
    """Section header with title, subtitle, and divider."""
    t = brand_title(title, color=ACCENT).move_to(POS_TITLE)
    s = brand_text(subtitle, color=TEXT_DIM).next_to(t, DOWN, buff=U2)
    rule = divider().next_to(s, DOWN, buff=U)
    return VGroup(t, s, rule)


def lower_third(name, title, accent=ACCENT):
    """Broadcast-style lower third."""
    bar   = Rectangle(
        width=5.5, height=0.06,
        fill_color=accent, fill_opacity=1, stroke_width=0,
    )
    name_ = brand_text(name,  size=T_H2,   color=TEXT).next_to(bar, UP, buff=0.12, aligned_edge=LEFT)
    title_= brand_text(title, size=T_BODY, color=TEXT_DIM).next_to(bar, DOWN, buff=0.12, aligned_edge=LEFT)
    group = VGroup(bar, name_, title_)
    group.to_corner(DL, buff=U4)
    return group
