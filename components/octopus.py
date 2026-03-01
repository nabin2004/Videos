# components/octopus.py — OctopusCreature mascot for TheBoringAI
#
# A playful octopus character with 8 tentacles for teaching ML/DL concepts.
# 8 arms = perfect for holding, comparing, counting, and arranging items.
#
# Quick usage:
#   from components.octopus import OctopusCreature, OctopusAnimations, OctopusTeaches
#
#   octo = OctopusCreature(mood="happy")
#   OctopusAnimations.entrance(self, octo)
#   OctopusTeaches.concept(self, "Gradient Descent", ["Follow the slope", ...])

from manim import *
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand import *
from typography import *
from layout import *
from animations import *

# ═══════════════════════════════════════════════════════════════════════════════
#  Constants
# ═══════════════════════════════════════════════════════════════════════════════

NUM_TENTACLES = 8
TENTACLE_RESOLUTION = 20  # points per tentacle curve

# Octopus palette — derived from brand colors
OCTO_EYE_WHITE = "#F0F2F8"
OCTO_PUPIL = "#0E1120"
OCTO_MOUTH = "#0E1120"
OCTO_SUCKER = "#FFFFFF"


# ═══════════════════════════════════════════════════════════════════════════════
#  Color Utilities
# ═══════════════════════════════════════════════════════════════════════════════

def _hex_to_rgb(hex_color):
    """Convert hex string to (r, g, b) floats 0–1."""
    h = str(hex_color).lstrip("#")
    if len(h) < 6:
        h = h * 2  # handle short hex
    return np.array([int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4)])


def _rgb_to_hex(rgb):
    """Convert (r, g, b) floats 0–1 to hex string."""
    r, g, b = np.clip(rgb, 0, 1)
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))


def _shade(hex_color, factor):
    """Darken (factor < 0) or lighten (factor > 0) a color. Range: -1 to 1."""
    rgb = _hex_to_rgb(hex_color)
    if factor > 0:
        rgb = rgb + (1 - rgb) * factor
    else:
        rgb = rgb * (1 + factor)
    return _rgb_to_hex(rgb)


# ═══════════════════════════════════════════════════════════════════════════════
#  OctopusCreature
# ═══════════════════════════════════════════════════════════════════════════════

class OctopusCreature(VGroup):
    """
    A charming octopus mascot for TheBoringAI animations.

    The creature has a dome-shaped head with expressive eyes, a mood-dependent
    mouth, and **8 curvy tentacles** that can hold, point at, and fan out
    items — perfect for teaching ML/DL concepts.

    Parameters
    ----------
    color : str
        Body color.  Defaults to ``BRAND_ELECTRIC`` (cyan).
    mood : str
        Facial expression.  One of:
        ``happy`` | ``thinking`` | ``confused`` | ``excited`` |
        ``surprised`` | ``teaching`` | ``sleepy`` | ``sad`` | ``neutral``
    height : float
        Overall height in Manim units (default 2.5).
    show_suckers : bool
        If *True*, draws tiny sucker circles along the inner side of each
        tentacle (False by default — cleaner look).
    tentacle_curl : float
        Wave amplitude multiplier for tentacles (default 1.0).  Set to 0 for
        straight tentacles, >1 for extra wavy.

    Examples
    --------
    >>> octo = OctopusCreature(mood="teaching")
    >>> self.play(FadeIn(octo))
    >>> octo.look_at(some_mobject)

    >>> # Hold items with tentacles
    >>> items = [ml_block(f"w{i}") for i in range(4)]
    >>> octo.hold_items(items)

    See Also
    --------
    ProfessorOctopus : teacher variant with glasses and cap
    BabyOctopus      : smaller cute variant with big eyes
    NeuralOctopus    : tentacles colored per data class
    DataOctopus      : tentacles labeled with concepts
    """

    def __init__(
        self,
        color=None,
        mood="happy",
        height=2.5,
        show_suckers=False,
        tentacle_curl=1.0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.creature_color = color or BRAND_ELECTRIC
        self.mood = mood
        self.creature_height = height
        self._show_suckers = show_suckers
        self.tentacle_curl = tentacle_curl
        self.held_items = {}  # tentacle_index → Mobject

        self._build()
        self.set_height(height)

    # ─── Construction ───────────────────────────────────────────────────────

    def _build(self):
        """Assemble head → eyes → mouth → spots → tentacles (back-to-front)."""
        self.head = self._build_head()
        self.left_eye, self.right_eye = self._build_eyes()
        self.eyes = VGroup(self.left_eye, self.right_eye)
        self.mouth = self._build_mouth(self.mood)
        self.spots = self._build_spots()
        self.tentacles = self._build_tentacles()
        # Suckers (optional)
        self.suckers = self._build_suckers() if self._show_suckers else VGroup()

        # Layering: tentacles behind, head on top, then face details
        self.add(
            self.tentacles,
            self.suckers,
            self.head,
            self.spots,
            self.eyes,
            self.mouth,
        )

    # ── Head ────────────────────────────────────────────────────────────────

    def _build_head(self):
        """Dome-shaped head/mantle with a highlight to suggest 3D form."""
        body = Ellipse(
            width=1.8,
            height=1.5,
            color=self.creature_color,
            fill_opacity=1.0,
            stroke_width=2,
            stroke_color=_shade(self.creature_color, -0.25),
        )

        # Glossy highlight
        highlight = Ellipse(
            width=0.8,
            height=0.35,
            color=WHITE,
            fill_opacity=0.15,
            stroke_width=0,
        )
        highlight.move_to(body.get_center() + UP * 0.30 + LEFT * 0.10)

        return VGroup(body, highlight)

    # ── Eyes ────────────────────────────────────────────────────────────────

    def _build_eyes(self):
        """Two expressive eyes with iris → pupil → highlight dot."""

        def _eye(offset):
            iris = Ellipse(
                width=0.48,
                height=0.52,
                color=OCTO_EYE_WHITE,
                fill_opacity=1.0,
                stroke_width=1.5,
                stroke_color="#C8C8D0",
            )
            pupil = Circle(
                radius=0.14,
                color=OCTO_PUPIL,
                fill_opacity=1.0,
                stroke_width=0,
            )
            dot = Circle(
                radius=0.04,
                color=WHITE,
                fill_opacity=1.0,
                stroke_width=0,
            )
            dot.move_to(pupil.get_center() + UP * 0.045 + LEFT * 0.035)

            pupil_group = VGroup(pupil, dot)
            pupil_group.move_to(iris.get_center())

            eye = VGroup(iris, pupil_group)
            eye.iris = iris
            eye.pupil = pupil_group
            eye.move_to(offset)
            return eye

        return _eye(LEFT * 0.38 + UP * 0.12), _eye(RIGHT * 0.38 + UP * 0.12)

    # ── Mouth ───────────────────────────────────────────────────────────────

    _MOUTH_BUILDERS = {}  # populated by _register_mood

    @classmethod
    def _register_mood(cls, name):
        """Decorator that registers a mouth-builder function."""
        def decorator(fn):
            cls._MOUTH_BUILDERS[name] = fn
            return fn
        return decorator

    def _build_mouth(self, mood):
        builder = self._MOUTH_BUILDERS.get(mood, self._MOUTH_BUILDERS.get("happy"))
        return builder(self)

    # ── Spots / texture ─────────────────────────────────────────────────────

    def _build_spots(self):
        """Semi-transparent dots on the head for organic texture."""
        positions = [
            UP * 0.38 + LEFT * 0.30,
            UP * 0.42 + RIGHT * 0.15,
            UP * 0.10 + LEFT * 0.58,
            UP * 0.18 + RIGHT * 0.52,
            UP * 0.55,
        ]
        spots = VGroup()
        rng = np.random.RandomState(42)  # deterministic
        for pos in positions:
            spot = Circle(
                radius=rng.uniform(0.035, 0.065),
                color=_shade(self.creature_color, 0.25),
                fill_opacity=0.25,
                stroke_width=0,
            )
            spot.move_to(pos)
            spots.add(spot)
        return spots

    # ── Tentacles ───────────────────────────────────────────────────────────

    def _build_tentacles(self):
        """Eight wavy tentacles fanning out from the bottom of the head."""
        tentacles = VGroup()
        angles = np.linspace(-1.15, 1.15, NUM_TENTACLES)
        # Alternate lengths for visual variety
        rng = np.random.RandomState(7)
        lengths = [0.95 + rng.uniform(0, 0.25) for _ in range(NUM_TENTACLES)]

        for i in range(NUM_TENTACLES):
            t_frac = i / (NUM_TENTACLES - 1)  # 0 → 1 across base
            start_x = -0.72 + t_frac * 1.44
            start_y = -0.58 + 0.12 * np.cos(np.pi * t_frac)
            start = np.array([start_x, start_y, 0.0])
            tentacle = self._make_tentacle(start, angles[i], lengths[i], i)
            tentacles.add(tentacle)
        return tentacles

    def _make_tentacle(self, start, angle, length, index):
        """Build one wavy VMobject tentacle with tapered stroke.

        Taper is simulated by splitting the curve into short segments
        with decreasing stroke widths — compatible with the Cairo renderer
        which only supports scalar stroke widths per VMobject.
        """
        curl = self.tentacle_curl
        pts = []
        for j in range(TENTACLE_RESOLUTION):
            t = j / (TENTACLE_RESOLUTION - 1)
            x = start[0] + length * t * np.sin(angle)
            y = start[1] - length * t * np.cos(angle) * 0.85
            # Increasing-amplitude wave
            amp = 0.10 * curl * t * (1 + 0.4 * t)
            wave = amp * np.sin(4 * np.pi * t + index * 0.75)
            x += wave * np.cos(angle)
            y -= wave * np.sin(angle)
            pts.append(np.array([x, y, 0.0]))

        # Build tapered tentacle as VGroup of short segments
        n_segs = len(pts) - 1
        base_w, tip_w = 4.5, 1.0
        segments = VGroup()
        for k in range(n_segs):
            frac = k / max(n_segs - 1, 1)
            w = base_w + (tip_w - base_w) * frac
            seg = Line(pts[k], pts[k + 1], stroke_width=w, stroke_color=self.creature_color)
            segments.add(seg)

        # Store as a VGroup but keep the metadata helpers expect
        segments.tip_point = np.array(pts[-1])
        segments.base_point = np.array(pts[0])
        segments.index = index
        segments._all_pts = pts  # kept for point_from_proportion fallback
        return segments

    # ── Suckers (optional) ──────────────────────────────────────────────────

    def _build_suckers(self):
        """Small circles along the inner side of each tentacle."""
        all_suckers = VGroup()
        for tentacle in self.tentacles:
            pts = getattr(tentacle, '_all_pts', None)
            if pts is None or len(pts) < 2:
                continue
            n = 5
            for k in range(1, n + 1):
                alpha = k / (n + 1)
                idx = int(alpha * (len(pts) - 1))
                pos = pts[min(idx, len(pts) - 1)]
                sucker = Circle(
                    radius=0.025 * (1 - 0.4 * alpha),
                    color=_shade(self.creature_color, 0.35),
                    fill_opacity=0.5,
                    stroke_width=0,
                )
                sucker.move_to(pos)
                all_suckers.add(sucker)
        return all_suckers

    # ═══════════════════════════════════════════════════════════════════════════
    #  Eye Control
    # ═══════════════════════════════════════════════════════════════════════════

    def look_at(self, point_or_mobject):
        """Move both pupils toward *point_or_mobject*."""
        target = (
            point_or_mobject.get_center()
            if isinstance(point_or_mobject, Mobject)
            else np.array(point_or_mobject, dtype=float)
        )
        for eye in (self.left_eye, self.right_eye):
            center = eye.iris.get_center()
            direction = target - center
            norm = np.linalg.norm(direction)
            if norm < 1e-8:
                continue
            direction /= norm
            max_shift = eye.iris.get_width() * 0.18
            eye.pupil.move_to(center + direction * max_shift)
        return self

    def look(self, direction):
        """Look in a unit-direction vector (e.g. ``UP + RIGHT``)."""
        return self.look_at(self.get_center() + np.array(direction, dtype=float) * 5)

    def reset_eyes(self):
        """Centre both pupils."""
        for eye in (self.left_eye, self.right_eye):
            eye.pupil.move_to(eye.iris.get_center())
        return self

    def blink(self):
        """Flatten eyes to bottom-y (instant, non-animated). Use with `.copy()``."""
        for eye in (self.left_eye, self.right_eye):
            bottom_y = eye.iris.get_bottom()[1]
            for part in eye.family_members_with_points():
                pts = part.get_points().copy()
                pts[:, 1] = bottom_y
                part.set_points(pts)
        return self

    # ═══════════════════════════════════════════════════════════════════════════
    #  Mood
    # ═══════════════════════════════════════════════════════════════════════════

    def change_mood(self, mood):
        """Swap mouth shape for a new expression (instant)."""
        new_mouth = self._build_mouth(mood)
        # Scale & position new mouth to match current one
        new_mouth.set_height(max(self.mouth.get_height(), 0.05))
        new_mouth.move_to(self.mouth.get_center())
        self.remove(self.mouth)
        self.mouth = new_mouth
        self.add(self.mouth)
        self.mood = mood
        return self

    def get_mood(self):
        return self.mood

    # ═══════════════════════════════════════════════════════════════════════════
    #  Tentacle Interaction
    # ═══════════════════════════════════════════════════════════════════════════

    def get_tentacle(self, index):
        """Return tentacle by *index* (0–7, wraps)."""
        return self.tentacles[index % NUM_TENTACLES]

    def get_tentacle_tip(self, index):
        """World-space position of tentacle *index* tip."""
        tentacle = self.get_tentacle(index)
        # The last segment's endpoint is the tip
        return tentacle[-1].get_end()

    def get_all_tips(self):
        """List of all 8 tentacle tip positions."""
        return [self.get_tentacle_tip(i) for i in range(NUM_TENTACLES)]

    def hold_item(self, item, tentacle_index=0, buff=0.05):
        """Snap *item* to the tip of *tentacle_index*."""
        tip = self.get_tentacle_tip(tentacle_index)
        item.next_to(tip, DOWN, buff=buff)
        self.held_items[tentacle_index] = item
        return self

    def hold_items(self, items, start_index=0):
        """
        Distribute *items* evenly across tentacles.

        Fewer items → spread further apart.  Excess items are ignored.
        """
        n = min(len(items), NUM_TENTACLES)
        if n == 0:
            return self
        step = max(1, NUM_TENTACLES // n)
        for i, item in enumerate(items[:n]):
            idx = (start_index + i * step) % NUM_TENTACLES
            self.hold_item(item, idx)
        return self

    def release_items(self):
        """Forget all held items (does **not** remove them from scene)."""
        self.held_items.clear()
        return self

    def nearest_tentacle_to(self, target):
        """Return the index of the tentacle whose tip is closest to *target*."""
        if isinstance(target, Mobject):
            target = target.get_center()
        tips = self.get_all_tips()
        dists = [np.linalg.norm(np.array(tip) - np.array(target)) for tip in tips]
        return int(np.argmin(dists))

    # ═══════════════════════════════════════════════════════════════════════════
    #  Bubbles (thought / speech)
    # ═══════════════════════════════════════════════════════════════════════════

    def get_thought_bubble(self, text, width=None, **kwargs):
        """Return a *VGroup* thought bubble positioned above-right."""
        content = brand_text(str(text), size=T_BODY, color=TEXT)
        content.next_to(self, UR, buff=0.5)

        bg = RoundedRectangle(
            corner_radius=0.2,
            width=width or content.get_width() + 0.6,
            height=content.get_height() + 0.5,
            color=PANEL,
            fill_opacity=0.92,
            stroke_width=1.5,
            stroke_color=self.creature_color,
        )
        bg.move_to(content)
        content.set_z_index(1)

        # Thought-trail dots
        trail = VGroup()
        base = self.head.get_center() + UR * 0.55
        for i, r in enumerate([0.06, 0.04, 0.03]):
            dot = Circle(
                radius=r,
                color=self.creature_color,
                fill_opacity=0.55,
                stroke_width=0,
            )
            dot.move_to(base + UR * (i * 0.22 + 0.1))
            trail.add(dot)

        return VGroup(trail, bg, content)

    def get_speech_bubble(self, text, width=None, **kwargs):
        """Return a *VGroup* speech bubble with a tail pointing at the octopus."""
        content = brand_text(str(text), size=T_BODY, color=TEXT)
        content.next_to(self, UR, buff=0.55)

        bg = RoundedRectangle(
            corner_radius=0.15,
            width=width or content.get_width() + 0.6,
            height=content.get_height() + 0.5,
            color=PANEL,
            fill_opacity=0.92,
            stroke_width=1.5,
            stroke_color=self.creature_color,
        )
        bg.move_to(content)
        content.set_z_index(1)

        # Tail triangle
        tail = Triangle(
            color=PANEL,
            fill_opacity=0.92,
            stroke_width=1.5,
            stroke_color=self.creature_color,
        )
        tail.set_height(0.22).set_width(0.16)
        tail.next_to(bg, DL, buff=-0.06)

        return VGroup(tail, bg, content)

    # ═══════════════════════════════════════════════════════════════════════════
    #  Layout / Arrangement Helpers
    # ═══════════════════════════════════════════════════════════════════════════

    def fan_positions(self, n, radius=2.0, spread=PI * 0.75):
        """
        Return *n* positions arranged in a downward arc below the octopus.

        Useful for ``present_items``, ``count_off``, etc.
        """
        center = self.get_center() + DOWN * 0.6
        angles = np.linspace(-spread / 2, spread / 2, max(n, 1))
        return [
            center + radius * np.array([np.sin(a), -np.cos(a), 0])
            for a in angles
        ]

    def present_items(self, items, radius=2.0, spread=PI * 0.75):
        """Position *items* in a fan below the octopus.  Returns the items VGroup."""
        positions = self.fan_positions(len(items), radius, spread)
        group = VGroup()
        for item, pos in zip(items, positions):
            item.move_to(pos)
            group.add(item)
        return group

    def arrange_comparison(self, left_item, right_item, gap=3.5):
        """Place two items on either side of the octopus for VS comparison."""
        center = self.get_center()
        left_item.move_to(center + LEFT * gap / 2 + DOWN * 1.0)
        right_item.move_to(center + RIGHT * gap / 2 + DOWN * 1.0)
        return VGroup(left_item, right_item)

    def grid_positions(self, n, cols=4, spacing=1.4):
        """Return *n* positions in a grid below the octopus."""
        center = self.get_center() + DOWN * 1.8
        rows = (n + cols - 1) // cols
        positions = []
        for i in range(n):
            r, c = divmod(i, cols)
            x = (c - (cols - 1) / 2) * spacing
            y = -(r - (rows - 1) / 2) * spacing
            positions.append(center + np.array([x, y, 0]))
        return positions

    def line_positions(self, n, total_width=8.0):
        """Return *n* evenly-spaced positions in a horizontal line below."""
        center = self.get_center() + DOWN * 1.8
        xs = np.linspace(-total_width / 2, total_width / 2, max(n, 1))
        return [center + RIGHT * x for x in xs]


# ───────────────────────────────────────────────────────────────────────────────
#  Mood mouth-shape registrations
# ───────────────────────────────────────────────────────────────────────────────

@OctopusCreature._register_mood("happy")
def _mouth_happy(self):
    m = Arc(radius=0.22, start_angle=-PI * 0.78, angle=PI * 0.56,
            color=OCTO_MOUTH, stroke_width=2.5)
    m.move_to(DOWN * 0.22)
    return m

@OctopusCreature._register_mood("thinking")
def _mouth_thinking(self):
    m = Line(LEFT * 0.12, RIGHT * 0.12, color=OCTO_MOUTH, stroke_width=2.5)
    m.move_to(DOWN * 0.23 + RIGHT * 0.06)
    return m

@OctopusCreature._register_mood("confused")
def _mouth_confused(self):
    pts = [
        np.array([-0.14, -0.04, 0]),
        np.array([-0.04,  0.04, 0]),
        np.array([ 0.04, -0.04, 0]),
        np.array([ 0.14,  0.02, 0]),
    ]
    m = VMobject(color=OCTO_MOUTH, stroke_width=2.5)
    m.set_points_smoothly(pts)
    m.move_to(DOWN * 0.23)
    return m

@OctopusCreature._register_mood("excited")
def _mouth_excited(self):
    m = Ellipse(width=0.26, height=0.22, color=OCTO_MOUTH,
                fill_opacity=0.8, stroke_width=2)
    m.move_to(DOWN * 0.22)
    return m

@OctopusCreature._register_mood("surprised")
def _mouth_surprised(self):
    m = Circle(radius=0.10, color=OCTO_MOUTH,
               fill_opacity=0.8, stroke_width=2)
    m.move_to(DOWN * 0.22)
    return m

@OctopusCreature._register_mood("teaching")
def _mouth_teaching(self):
    m = Arc(radius=0.24, start_angle=-PI * 0.72, angle=PI * 0.44,
            color=OCTO_MOUTH, stroke_width=3)
    m.move_to(DOWN * 0.20)
    return m

@OctopusCreature._register_mood("sleepy")
def _mouth_sleepy(self):
    m = Line(LEFT * 0.10, RIGHT * 0.10, color=OCTO_MOUTH, stroke_width=2)
    m.move_to(DOWN * 0.24)
    return m

@OctopusCreature._register_mood("sad")
def _mouth_sad(self):
    m = Arc(radius=0.20, start_angle=PI * 0.22, angle=PI * 0.56,
            color=OCTO_MOUTH, stroke_width=2.5)
    m.move_to(DOWN * 0.28)
    return m

@OctopusCreature._register_mood("neutral")
def _mouth_neutral(self):
    return _mouth_thinking(self)


# ═══════════════════════════════════════════════════════════════════════════════
#  Variations
# ═══════════════════════════════════════════════════════════════════════════════

class ProfessorOctopus(OctopusCreature):
    """
    Teacher octopus — wears round glasses and a mortarboard cap.

    Perfect for "here's the theory" segments and formal explanations.

    Example
    -------
    >>> prof = ProfessorOctopus()
    >>> OctopusAnimations.entrance(self, prof)
    >>> OctopusAnimations.say(self, prof, "Let's talk about calculus!")
    """

    def __init__(self, color=None, mood="teaching", **kwargs):
        super().__init__(color=color or BRAND_PLASMA, mood=mood, **kwargs)
        self._add_glasses()
        self._add_cap()

    def _add_glasses(self):
        left_lens = Circle(
            radius=0.19, color=BRAND_GHOST,
            fill_opacity=0.06, stroke_width=2.0, stroke_color=BRAND_GHOST,
        )
        right_lens = left_lens.copy()
        left_lens.move_to(self.left_eye.get_center())
        right_lens.move_to(self.right_eye.get_center())

        bridge = Line(
            left_lens.get_right(), right_lens.get_left(),
            color=BRAND_GHOST, stroke_width=2.0,
        )
        left_arm = Line(
            left_lens.get_left(),
            left_lens.get_left() + LEFT * 0.18 + UP * 0.04,
            color=BRAND_GHOST, stroke_width=2.0,
        )
        right_arm = Line(
            right_lens.get_right(),
            right_lens.get_right() + RIGHT * 0.18 + UP * 0.04,
            color=BRAND_GHOST, stroke_width=2.0,
        )
        self.glasses = VGroup(left_lens, right_lens, bridge, left_arm, right_arm)
        self.add(self.glasses)

    def _add_cap(self):
        top = self.head.get_top()
        board = Square(
            side_length=0.55, color="#1A1A2E",
            fill_opacity=1.0, stroke_width=1, stroke_color=BRAND_GHOST,
        )
        board.rotate(PI / 14).move_to(top + UP * 0.14)

        base = RoundedRectangle(
            corner_radius=0.04, width=0.38, height=0.14,
            color="#28284A", fill_opacity=1.0,
            stroke_width=1, stroke_color=BRAND_GHOST,
        )
        base.next_to(board, DOWN, buff=-0.02)

        tassel_end = board.get_center() + RIGHT * 0.32 + DOWN * 0.22
        tassel_line = Line(
            board.get_center(), tassel_end,
            color=BRAND_SOLAR, stroke_width=2,
        )
        tassel_dot = Circle(
            radius=0.04, color=BRAND_SOLAR,
            fill_opacity=1, stroke_width=0,
        )
        tassel_dot.move_to(tassel_end)

        self.cap = VGroup(base, board, tassel_line, tassel_dot)
        self.add(self.cap)


class BabyOctopus(OctopusCreature):
    """
    Smaller, cuter octopus with oversized eyes and a rounder head.

    Great for introducing simple concepts, showing "beginner" perspective,
    or as an audience surrogate asking questions.

    Example
    -------
    >>> baby = BabyOctopus()
    >>> OctopusAnimations.entrance(self, baby)
    >>> OctopusAnimations.think(self, baby, "What even is a gradient?")
    """

    def __init__(self, color=None, mood="happy", height=1.3, **kwargs):
        super().__init__(
            color=color or BRAND_NOVA, mood=mood, height=height,
            tentacle_curl=0.7, **kwargs,
        )
        # Enlarge eyes relative to head for cute effect
        eyes_center = self.eyes.get_center()
        self.eyes.scale(1.35)
        self.eyes.move_to(eyes_center + UP * 0.03)


class NeuralOctopus(OctopusCreature):
    """
    Each tentacle is a different ``DATA_COLORS`` shade — like neural connections
    carrying different signals.  Comes with ``pulse_tentacle()`` to
    visually fire a signal down a tentacle.

    Example
    -------
    >>> noc = NeuralOctopus()
    >>> self.play(FadeIn(noc))
    >>> noc.pulse_tentacle(self, 3)  # fire signal on tentacle #3
    """

    def __init__(self, color=None, mood="teaching", **kwargs):
        super().__init__(color=color or BRAND_ELECTRIC, mood=mood, **kwargs)
        self._colorize_tentacles()

    def _colorize_tentacles(self):
        palette = DATA_COLORS * ((NUM_TENTACLES // len(DATA_COLORS)) + 1)
        for i, tentacle in enumerate(self.tentacles):
            for seg in tentacle:
                seg.set_stroke(color=palette[i])

    def pulse_tentacle(self, scene, index, color=BRAND_SOLAR, run_time=0.6):
        """Animate a glow pulse along tentacle *index*."""
        t = self.get_tentacle(index)
        # Save original colors per-segment
        orig_colors = [seg.get_stroke_color() for seg in t]
        orig_widths = [seg.get_stroke_width() for seg in t]
        scene.play(
            *[seg.animate.set_stroke(color=color, width=8) for seg in t],
            run_time=run_time / 2,
        )
        scene.play(
            *[
                seg.animate.set_stroke(color=oc, width=ow)
                for seg, oc, ow in zip(t, orig_colors, orig_widths)
            ],
            run_time=run_time / 2,
        )


class DataOctopus(OctopusCreature):
    """
    Each tentacle tip is labelled with a concept — ideal for showing
    data pipelines, feature names, or hyperparameters.

    Example
    -------
    >>> doc = DataOctopus(labels=["lr", "epochs", "batch", "dropout",
    ...                           "decay", "momentum", "β₁", "β₂"])
    """

    def __init__(self, labels=None, color=None, **kwargs):
        super().__init__(color=color or BRAND_PLASMA, mood="teaching", **kwargs)
        self.tip_labels = VGroup()
        if labels:
            self.label_tentacles(labels)

    def label_tentacles(self, labels):
        """Place a text label at each tentacle tip."""
        self.tip_labels = VGroup()
        for i, txt in enumerate(labels[:NUM_TENTACLES]):
            tip = self.get_tentacle_tip(i)
            lbl = brand_text(str(txt), size=T_LABEL, color=TEXT)
            lbl.next_to(tip, DOWN, buff=0.06)
            self.tip_labels.add(lbl)
        self.add(self.tip_labels)
        return self


# ═══════════════════════════════════════════════════════════════════════════════
#  OctopusAnimations — drop-in animation helpers (all static)
# ═══════════════════════════════════════════════════════════════════════════════

class OctopusAnimations:
    """
    Ready-made animation sequences — call on any scene.

    Every method is ``@staticmethod`` so usage is simple::

        OctopusAnimations.entrance(self, octo)
        OctopusAnimations.wave_hello(self, octo)
        OctopusAnimations.think(self, octo, "Hmm...")
    """

    # ── Entrance / Exit ─────────────────────────────────────────────────────

    @staticmethod
    def entrance(scene, octo, direction=DOWN, run_time=1.0):
        """Playful entrance — scale up + slide in with spring easing."""
        scene.play(
            FadeIn(octo, shift=direction * 1.5, scale=0.5),
            run_time=run_time,
            rate_func=smooth,
        )

    @staticmethod
    def exit(scene, octo, direction=DOWN, run_time=0.8):
        """Exit — shrink + fade out."""
        scene.play(
            FadeOut(octo, shift=direction * 1.5, scale=0.5),
            run_time=run_time,
        )

    # ── Expressions ─────────────────────────────────────────────────────────

    @staticmethod
    def wave_hello(scene, octo, tentacle_indices=None, cycles=1, run_time=0.8):
        """
        Wave outer tentacles back and forth.

        Parameters
        ----------
        tentacle_indices : list[int] | None
            Which tentacles wave. Defaults to the two outermost ``[0, 7]``.
        """
        if tentacle_indices is None:
            tentacle_indices = [0, NUM_TENTACLES - 1]
        for _ in range(cycles):
            anims = []
            for idx in tentacle_indices:
                t = octo.get_tentacle(idx)
                anims.append(
                    Rotate(t, angle=0.35 * (-1 if idx < 4 else 1),
                           about_point=t[0].get_start())
                )
            scene.play(*anims, run_time=run_time / 2, rate_func=there_and_back)

    @staticmethod
    def blink_anim(scene, octo, run_time=0.25):
        """Quick blink — closes eyes and reopens."""
        saved = octo.eyes.copy()
        octo.blink()
        scene.wait(run_time)
        octo.eyes.become(saved)

    @staticmethod
    def look_around(scene, octo, run_time=1.5):
        """Glance left → right → centre."""
        octo.look(LEFT)
        scene.wait(run_time / 3)
        octo.look(RIGHT)
        scene.wait(run_time / 3)
        octo.reset_eyes()
        scene.wait(run_time / 3)

    # ── Speech / Thought ────────────────────────────────────────────────────

    @staticmethod
    def think(scene, octo, text, hold=1.5, run_time=0.8):
        """Show thought bubble, pause, then dismiss."""
        octo.change_mood("thinking")
        bubble = octo.get_thought_bubble(text)
        scene.play(FadeIn(bubble, shift=UP * 0.2), run_time=run_time)
        scene.wait(hold)
        scene.play(FadeOut(bubble), run_time=run_time * 0.5)
        octo.change_mood("happy")
        return bubble

    @staticmethod
    def say(scene, octo, text, mood="happy", hold=1.5, run_time=0.8):
        """Show speech bubble, pause, then dismiss."""
        octo.change_mood(mood)
        bubble = octo.get_speech_bubble(text)
        scene.play(FadeIn(bubble, shift=UP * 0.15), run_time=run_time)
        scene.wait(hold)
        scene.play(FadeOut(bubble), run_time=run_time * 0.5)
        return bubble

    # ── Presenting / Teaching ───────────────────────────────────────────────

    @staticmethod
    def present(scene, octo, items, title=None, run_time=1.5):
        """
        Fan *items* out below the octopus, optionally with a title above.

        Returns the positioned VGroup so you can later ``FadeOut`` it.

        Example
        -------
        >>> cards = [ml_block("ReLU"), ml_block("Sigmoid"), ml_block("Tanh")]
        >>> group = OctopusAnimations.present(self, octo, cards, "Activations")
        """
        positioned = octo.present_items(items)
        anims = [FadeIn(item, shift=DOWN * 0.3) for item in positioned]
        if title:
            title_mob = brand_text(title, size=T_H2, color=ACCENT)
            title_mob.next_to(octo, UP, buff=0.3)
            anims.insert(0, FadeIn(title_mob, shift=UP * 0.2))
            positioned.add(title_mob)
        scene.play(LaggedStart(*anims, lag_ratio=0.12), run_time=run_time)
        return positioned

    @staticmethod
    def compare(scene, octo, left_item, right_item,
                left_label="A", right_label="B", run_time=1.0):
        """
        Hold two items for side-by-side **VS** comparison.

        Example
        -------
        >>> OctopusAnimations.compare(self, octo, sigmoid_plot, relu_plot,
        ...                           "Sigmoid", "ReLU")
        """
        octo.arrange_comparison(left_item, right_item)
        l_lbl = brand_text(left_label, size=T_CAPTION, color=BRAND_ELECTRIC)
        r_lbl = brand_text(right_label, size=T_CAPTION, color=BRAND_NOVA)
        l_lbl.next_to(left_item, UP, buff=0.12)
        r_lbl.next_to(right_item, UP, buff=0.12)

        vs = brand_text("VS", size=T_H2, color=BRAND_NOVA)
        vs.move_to((left_item.get_center() + right_item.get_center()) / 2 + UP * 0.2)

        scene.play(
            FadeIn(left_item, shift=LEFT * 0.3),
            FadeIn(right_item, shift=RIGHT * 0.3),
            FadeIn(l_lbl), FadeIn(r_lbl),
            FadeIn(vs, scale=1.4),
            run_time=run_time,
        )
        return VGroup(left_item, right_item, l_lbl, r_lbl, vs)

    @staticmethod
    def count_off(scene, octo, items, layout="arc", run_time=2.0):
        """
        Enumerate *items* (strings or Mobjects) one by one in a fan / grid / line.

        Example
        -------
        >>> OctopusAnimations.count_off(self, octo, [
        ...     "Load data", "Preprocess", "Train", "Evaluate", "Deploy"
        ... ])
        """
        if layout == "arc":
            positions = octo.fan_positions(len(items))
        elif layout == "grid":
            positions = octo.grid_positions(len(items))
        else:
            positions = octo.line_positions(len(items))

        cards = VGroup()
        for i, (content, pos) in enumerate(zip(items, positions)):
            if isinstance(content, str):
                num = brand_text(f"{i + 1}.", size=T_BODY, color=BRAND_SOLAR)
                txt = brand_text(content, size=T_CAPTION, color=TEXT)
                card = VGroup(num, txt).arrange(RIGHT, buff=0.12)
            elif isinstance(content, Mobject):
                card = content
            else:
                continue
            card.move_to(pos)
            cards.add(card)

        per_item = run_time / max(len(cards), 1)
        for card in cards:
            scene.play(FadeIn(card, shift=DOWN * 0.2), run_time=per_item)
        return cards

    @staticmethod
    def juggle(scene, octo, items, cycles=2, run_time=2.0):
        """
        Playful juggling animation — items orbit above the octopus.

        Example
        -------
        >>> tensors = [ml_block(f"x{i}", width=0.8, height=0.5) for i in range(3)]
        >>> OctopusAnimations.juggle(self, octo, tensors)
        """
        n = len(items)
        center = octo.get_center() + UP * 1.4
        for i, item in enumerate(items):
            a = -PI / 4 + (i / max(n - 1, 1)) * PI / 2
            item.move_to(center + 0.8 * np.array([np.sin(a), np.cos(a) * 0.3, 0]))
        scene.play(*[FadeIn(item) for item in items], run_time=0.3)

        group = VGroup(*items)
        angle_per = PI / max(n, 1)
        for _ in range(cycles):
            scene.play(
                Rotate(group, angle_per, about_point=center),
                run_time=run_time / (2 * cycles),
                rate_func=smooth,
            )
        return group

    @staticmethod
    def idle(scene, octo, duration=2.0):
        """Subtle idle animation — slight hover + blink."""
        scene.play(
            octo.animate.shift(UP * 0.06),
            run_time=duration / 4,
            rate_func=there_and_back,
        )
        OctopusAnimations.blink_anim(scene, octo)
        scene.play(
            octo.animate.shift(UP * 0.04),
            run_time=duration / 4,
            rate_func=there_and_back,
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  OctopusTeaches — high-level pedagogical sequences
# ═══════════════════════════════════════════════════════════════════════════════

class OctopusTeaches:
    """
    Complete teaching sequences combining octopus + content.

    Each method manages its own entrance/exit — just call and go::

        OctopusTeaches.concept(self, "Backpropagation", [
            "Compute loss at output",
            "Apply chain rule backwards",
            "Update each weight",
        ])
    """

    @staticmethod
    def concept(scene, title, bullet_points, octo=None, side=LEFT):
        """
        Octopus introduces a concept: title + animated bullet points.

        Parameters
        ----------
        scene : Scene
        title : str
        bullet_points : list[str]
        octo : OctopusCreature | None
            Pass an existing octopus or let the method create one.
        side : np.ndarray
            Which side the octopus stands on (``LEFT`` or ``RIGHT``).

        Returns
        -------
        OctopusCreature — the octopus (useful for follow-up animations).
        """
        if octo is None:
            octo = OctopusCreature(mood="teaching", height=2.0)
        octo.move_to(side * 4.5 + DOWN * 0.5)
        OctopusAnimations.entrance(scene, octo)
        octo.look(-side)  # face inward

        content_x = -side[0] * 1.5  # opposite side

        title_mob = brand_text(title, size=T_H2, color=ACCENT)
        title_mob.move_to(RIGHT * content_x + UP * 2.5)
        scene.play(FadeIn(title_mob, shift=DOWN * 0.2))

        bullets = VGroup()
        for i, point in enumerate(bullet_points):
            b = brand_text(f"•  {point}", size=T_BODY, color=TEXT)
            b.move_to(RIGHT * content_x + UP * (1.5 - i * 0.7))
            b.align_to(title_mob, LEFT)
            bullets.add(b)

        for b in bullets:
            scene.play(FadeIn(b, shift=RIGHT * (-side[0]) * 0.2), run_time=0.45)
            scene.wait(0.25)

        scene.wait(1.0)
        scene.play(FadeOut(title_mob), FadeOut(bullets), run_time=0.5)
        OctopusAnimations.exit(scene, octo)
        return octo

    @staticmethod
    def step_by_step(scene, steps, octo=None, layout="arc"):
        """
        Walk through *steps* one-at-a-time with the octopus counting off.

        Example
        -------
        >>> OctopusTeaches.step_by_step(self, [
        ...     "Load data", "Forward pass", "Compute loss",
        ...     "Backpropagate", "Update weights",
        ... ])
        """
        if octo is None:
            octo = OctopusCreature(mood="teaching", height=2.0)
        octo.move_to(UP * 1.8)
        OctopusAnimations.entrance(scene, octo)

        cards = OctopusAnimations.count_off(scene, octo, steps, layout=layout)

        scene.wait(1.5)
        scene.play(FadeOut(cards), run_time=0.5)
        OctopusAnimations.exit(scene, octo)
        return octo

    @staticmethod
    def vs(scene, item_a, item_b, label_a="A", label_b="B", octo=None):
        """
        Side-by-side comparison with a VS badge.

        Example
        -------
        >>> OctopusTeaches.vs(self, sigmoid_plot, relu_plot, "Sigmoid", "ReLU")
        """
        if octo is None:
            octo = OctopusCreature(mood="thinking", height=1.8)
        octo.move_to(UP * 2.2)
        OctopusAnimations.entrance(scene, octo)

        group = OctopusAnimations.compare(
            scene, octo, item_a, item_b, label_a, label_b,
        )
        scene.wait(2.0)
        scene.play(FadeOut(group), run_time=0.5)
        OctopusAnimations.exit(scene, octo)
        return octo

    @staticmethod
    def quiz(scene, question, choices, answer_index=0, octo=None):
        """
        Interactive quiz moment:  question → choices → reveal answer.

        Parameters
        ----------
        question : str
        choices : list[str]
            Up to 8 answers (one per tentacle!).
        answer_index : int
            Index of the correct choice.

        Example
        -------
        >>> OctopusTeaches.quiz(self,
        ...     "Which activation avoids vanishing gradients?",
        ...     ["Sigmoid", "ReLU", "Tanh", "Step"],
        ...     answer_index=1)
        """
        if octo is None:
            octo = OctopusCreature(mood="teaching", height=2.0)
        octo.move_to(UP * 2.0)
        OctopusAnimations.entrance(scene, octo)

        q_mob = brand_text(question, size=T_H2, color=ACCENT)
        q_mob.next_to(octo, DOWN, buff=0.4)
        scene.play(FadeIn(q_mob, shift=DOWN * 0.2))
        scene.wait(0.5)

        # Fan choices below
        positions = octo.fan_positions(len(choices), radius=2.2, spread=PI * 0.7)
        letters = "ABCDEFGH"
        choice_cards = VGroup()
        for i, (txt, pos) in enumerate(zip(choices, positions)):
            letter = brand_text(f"{letters[i]}.", size=T_BODY, color=BRAND_SOLAR)
            label = brand_text(txt, size=T_CAPTION, color=TEXT)
            card = VGroup(letter, label).arrange(RIGHT, buff=0.1)

            bg = RoundedRectangle(
                corner_radius=0.1,
                width=card.get_width() + 0.3,
                height=card.get_height() + 0.2,
                color=PANEL, fill_opacity=0.85, stroke_width=1,
                stroke_color=BRAND_STEEL,
            )
            bg.move_to(card)
            group = VGroup(bg, card)
            group.move_to(pos)
            choice_cards.add(group)

        scene.play(
            LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in choice_cards],
                        lag_ratio=0.1),
            run_time=1.0,
        )
        scene.wait(2.0)

        # Highlight correct answer
        correct = choice_cards[answer_index]
        scene.play(
            correct[0].animate.set_stroke(color=BRAND_ELECTRIC, width=3),
            correct[0].animate.set_fill(color=_shade(BRAND_ELECTRIC, -0.7), opacity=0.4),
            run_time=0.6,
        )
        octo.change_mood("excited")
        scene.wait(1.5)

        scene.play(FadeOut(q_mob), FadeOut(choice_cards), run_time=0.5)
        OctopusAnimations.exit(scene, octo)
        return octo

    @staticmethod
    def pipeline(scene, stages, octo=None):
        """
        Show a left-to-right pipeline where each stage is labeled.

        The octopus stands to the side and points. Each stage appears
        sequentially with arrows between them.

        Parameters
        ----------
        stages : list[tuple[str, str]]
            Each element is ``(label, hex_color)`` or  just a ``str``
            (which will use ``BRAND_ELECTRIC``).

        Example
        -------
        >>> OctopusTeaches.pipeline(self, [
        ...     ("Data", BRAND_ELECTRIC),
        ...     ("Feature Eng.", BRAND_PLASMA),
        ...     ("Model", BRAND_NOVA),
        ...     ("Evaluate", BRAND_SOLAR),
        ... ])
        """
        if octo is None:
            octo = OctopusCreature(mood="teaching", height=1.8)
        octo.move_to(LEFT * 5.5 + DOWN * 0.5)
        OctopusAnimations.entrance(scene, octo)
        octo.look(RIGHT)

        normalized = []
        for s in stages:
            if isinstance(s, str):
                normalized.append((s, BRAND_ELECTRIC))
            else:
                normalized.append(s)

        n = len(normalized)
        total_w = 10.0
        box_w = min(1.8, total_w / n - 0.4)
        start_x = -total_w / 2 + 2.0  # offset for octopus
        pipeline_mobs = VGroup()

        for i, (label, color) in enumerate(normalized):
            x = start_x + i * (total_w / n)
            box = RoundedRectangle(
                corner_radius=0.1, width=box_w, height=0.7,
                color=color, fill_opacity=0.2,
                stroke_width=2, stroke_color=color,
            )
            txt = brand_text(label, size=T_CAPTION, color=color)
            txt.move_to(box)
            stage = VGroup(box, txt).move_to(RIGHT * x)
            pipeline_mobs.add(stage)

        arrows = VGroup()
        for i in range(n - 1):
            a = Arrow(
                pipeline_mobs[i].get_right(),
                pipeline_mobs[i + 1].get_left(),
                color=BRAND_GHOST, stroke_width=2, buff=0.08,
                max_tip_length_to_length_ratio=0.15,
            )
            arrows.add(a)

        for i, stage in enumerate(pipeline_mobs):
            anims = [FadeIn(stage, shift=RIGHT * 0.3)]
            if i > 0:
                anims.append(GrowArrow(arrows[i - 1]))
            scene.play(*anims, run_time=0.5)

        scene.wait(2.0)
        scene.play(FadeOut(pipeline_mobs), FadeOut(arrows), run_time=0.5)
        OctopusAnimations.exit(scene, octo)
        return octo
