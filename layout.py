# layout.py — Grid, positions & safe areas for TheBoringAI

from manim import *

# ── BASE UNIT ────────────────────────────────────────────────────────────────
# Manim default frame is 8 units tall × 14.2 wide
U  = 0.25          # 1 grid unit
U2 = U * 2         # 2 units
U4 = U * 4         # 4 units  (standard margin)
U8 = U * 8         # 8 units  (section gap)

FRAME_W = 14.2
FRAME_H = 8.0

# ── SAFE AREA (keep content inside) ─────────────────────────────────────────
SAFE_LEFT   = -FRAME_W / 2 + U4
SAFE_RIGHT  =  FRAME_W / 2 - U4
SAFE_TOP    =  FRAME_H / 2 - U2
SAFE_BOTTOM = -FRAME_H / 2 + U2

# ── COMMON ANCHOR POSITIONS ─────────────────────────────────────────────────
POS_TITLE     = UP    * 3.2
POS_SUBTITLE  = UP    * 2.5
POS_CENTER    = ORIGIN
POS_LOWER     = DOWN  * 2.8
POS_FOOTER    = DOWN  * 3.6
POS_LEFT_COL  = LEFT  * 3.5
POS_RIGHT_COL = RIGHT * 3.5

# ── ML/DL SPECIFIC LAYOUT POSITIONS ─────────────────────────────────────────
POS_NETWORK_CENTER  = ORIGIN + DOWN * 0.3   # Neural net slightly below center
POS_EQUATION_CENTER = UP * 0.5              # Equations slightly above center
POS_DIAGRAM_LEFT    = LEFT * 3.0            # Left diagram in split view
POS_DIAGRAM_RIGHT   = RIGHT * 3.0           # Right diagram in split view
