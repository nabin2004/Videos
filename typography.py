# typography.py — Font helpers & type scale for TheBoringAI

from manim import *
from brand import *

# ── FONT FAMILIES ────────────────────────────────────────────────────────────
FONT_PRIMARY   = "Inter"          # UI / labels
FONT_DISPLAY   = "Space Grotesk"  # Hero titles
FONT_MONO      = "JetBrains Mono" # Code / data

# ── SIZE SCALE (in Manim units — multiply by 0.7 for compact layouts) ────────
T_HERO    = 1.10   # Main title
T_H1      = 0.80   # Section heading
T_H2      = 0.60   # Sub-heading
T_BODY    = 0.42   # Body copy
T_CAPTION = 0.32   # Captions / footnotes
T_LABEL   = 0.28   # Axis labels, tiny UI

# ── HELPER FACTORIES ─────────────────────────────────────────────────────────

def brand_text(content, size=T_BODY, color=TEXT, font=FONT_PRIMARY, **kwargs):
    """General-purpose branded text — defaults to Inter, body size, ghost white."""
    return Text(content, font_size=size * 48, color=color, font=font, **kwargs)


def brand_title(content, color=ACCENT, **kwargs):
    """Hero display title — Space Grotesk Bold."""
    return Text(
        content,
        font_size=T_HERO * 48,
        color=color,
        font=FONT_DISPLAY,
        weight=BOLD,
        **kwargs,
    )


def brand_code(content, **kwargs):
    """Code block with branded window background."""
    return Code(
        code=content,
        font=FONT_MONO,
        background="window",
        background_color=PANEL,
        insert_line_no=False,
        style="monokai",
        **kwargs,
    )


def brand_math(tex_string, color=TEXT, **kwargs):
    """MathTex with brand color defaults."""
    return MathTex(tex_string, color=color, **kwargs)


def brand_equation(tex_string, color=TEXT, size=T_H2, **kwargs):
    """Scaled MathTex for display equations."""
    eq = MathTex(tex_string, color=color, **kwargs)
    eq.scale(size / 0.5)  # Manim default MathTex is ~0.5 units
    return eq
