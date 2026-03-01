# brand.py — Single source of truth for TheBoringAI brand system
# Import this in every scene file: from brand import *

from manim import *

# ── SERIES IDENTITY ──────────────────────────────────────────────────────────
SERIES_NAME = "TheBoringAI"
SERIES_TAGLINE = "Machine Learning & Deep Learning — Visualized"

# ── PRIMARY PALETTE ──────────────────────────────────────────────────────────
BRAND_MIDNIGHT   = "#0A0E1A"   # Background — deep space black-blue
BRAND_VOID       = "#070B14"   # Deeper background / letter-box bars
BRAND_ELECTRIC   = "#00F5FF"   # Primary accent — electric cyan
BRAND_PLASMA     = "#BF5AF2"   # Secondary accent — plasma purple
BRAND_NOVA       = "#FF6B35"   # Highlight / CTA — nova orange
BRAND_SOLAR      = "#FFD60A"   # Warning / emphasis — solar gold
BRAND_GHOST      = "#E8EAF0"   # Body text — soft white
BRAND_MIST       = "#8892A4"   # Secondary text — muted slate
BRAND_DEEP       = "#1C2333"   # Card / panel background
BRAND_STEEL      = "#2E3A50"   # Dividers / borders

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
LOSS_COLOR        = "#FF073A"         # Loss / error — hot red
GRADIENT_COLOR    = BRAND_SOLAR       # Gradient flow
INPUT_COLOR       = "#39FF14"         # Input layer — neon green
OUTPUT_COLOR      = BRAND_ELECTRIC    # Output layer
HIDDEN_COLOR      = BRAND_PLASMA      # Hidden layers
POSITIVE_COLOR    = BRAND_SOLAR       # Positive values
NEGATIVE_COLOR    = "#FF073A"         # Negative values

# ── DATA-VIZ SEQUENCE (use in order for charts/graphs) ───────────────────────
DATA_COLORS = [
    BRAND_ELECTRIC,  # series 1
    BRAND_PLASMA,    # series 2
    BRAND_NOVA,      # series 3
    BRAND_SOLAR,     # series 4
    "#39FF14",       # series 5 — neon green
    "#FF073A",       # series 6 — hot red
]
