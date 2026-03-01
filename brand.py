# brand.py — Single source of truth for TheBoringAI brand system
# Import this in every scene file: from brand import *

from manim import *

# ── SERIES IDENTITY ──────────────────────────────────────────────────────────
SERIES_NAME = "TheBoringAI"
SERIES_TAGLINE = "Machine Learning & Deep Learning — Visualized"

# ── PRIMARY PALETTE ──────────────────────────────────────────────────────────
BRAND_MIDNIGHT   = "#191919"   # Background — warm charcoal
BRAND_VOID       = "#111111"   # Deeper background / letter-box bars
BRAND_ELECTRIC   = "#D4A27F"   # Primary accent — warm sand
BRAND_PLASMA     = "#CC785C"   # Secondary accent — terracotta
BRAND_NOVA       = "#E8B888"   # Highlight / CTA — golden tan
BRAND_SOLAR      = "#F5D0A9"   # Warning / emphasis — pale peach
BRAND_GHOST      = "#F0EDE8"   # Body text — warm cream
BRAND_MIST       = "#A89F95"   # Secondary text — muted stone
BRAND_DEEP       = "#242220"   # Card / panel background
BRAND_STEEL      = "#3A3530"   # Dividers / borders

# ── GRADIENT PAIRS ───────────────────────────────────────────────────────────
GRAD_ELECTRIC_PLASMA = [BRAND_ELECTRIC, BRAND_PLASMA]  # Hero gradient
GRAD_NOVA_SOLAR      = [BRAND_NOVA,     BRAND_SOLAR]   # Warm highlight
GRAD_DEEP_MIDNIGHT   = [BRAND_DEEP,     BRAND_MIDNIGHT]# Subtle depth

# ── SEMANTIC ALIASES ─────────────────────────────────────────────────────────
BG       = BRAND_MIDNIGHT
ACCENT   = BRAND_ELECTRIC
ACCENT2  = BRAND_PLASMA
HILIGHT  = BRAND_NOVA
TEXT     = BRAND_GHOST
TEXT_DIM = BRAND_MIST
PANEL    = BRAND_DEEP

# ── ML/DL SPECIFIC SEMANTIC COLORS ──────────────────────────────────────────
NEURON_COLOR      = BRAND_ELECTRIC    # Neuron nodes
WEIGHT_COLOR      = BRAND_PLASMA      # Connection weights
ACTIVATION_COLOR  = BRAND_NOVA        # Activated neurons
LOSS_COLOR        = "#C05040"         # Loss / error — warm red
GRADIENT_COLOR    = BRAND_SOLAR       # Gradient flow
INPUT_COLOR       = "#B8C9A3"         # Input layer — sage green
OUTPUT_COLOR      = BRAND_ELECTRIC    # Output layer
HIDDEN_COLOR      = BRAND_PLASMA      # Hidden layers
POSITIVE_COLOR    = BRAND_SOLAR       # Positive values
NEGATIVE_COLOR    = "#C05040"         # Negative values

# ── DATA-VIZ SEQUENCE (use in order for charts/graphs) ───────────────────────
DATA_COLORS = [
    BRAND_ELECTRIC,  # series 1 — warm sand
    BRAND_PLASMA,    # series 2 — terracotta
    BRAND_NOVA,      # series 3 — golden tan
    BRAND_SOLAR,     # series 4 — pale peach
    "#B8C9A3",       # series 5 — sage green
    "#C05040",       # series 6 — warm red
]
