#!/usr/bin/env python3
"""
TheBoringAI — Interactive Manim (OpenGL Live Preview)
=====================================================
Launches Manim with the OpenGL renderer for live, interactive editing.
Supports checkpointing, live code reload, and camera control.

Usage:
    python tools/interactive.py series/ML/01_neural_network_basics/scene.py NeuralNetworkBasicsScene
    python tools/interactive.py --presenter scene.py MyScene

Keys (in OpenGL window):
    r           — Reset scene
    q / Esc     — Quit
    scroll      — Zoom in/out
    drag        — Pan camera
    space       — Pause / Resume

For VS Code checkpoint integration see: .vscode/keybindings.json
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def launch_interactive(scene_path: str, class_name: str,
                       presenter: bool = False, write: bool = False):
    """Launch Manim with OpenGL renderer for interactive editing."""

    cmd = [
        "manim",
        "--renderer=opengl",
        "--enable_gui",
    ]

    if write:
        cmd.append("--write_to_movie")

    if presenter:
        cmd.append("--presenter_mode")

    # Quality (use medium for interactive speed)
    cmd.extend(["-qm", "--fps", "30"])

    cmd.extend([scene_path, class_name])

    print(f"\n{'='*60}")
    print("  INTERACTIVE MODE — OpenGL Renderer")
    print(f"{'='*60}")
    print(f"  Scene:  {scene_path}")
    print(f"  Class:  {class_name}")
    print(f"  Mode:   {'Presenter' if presenter else 'Interactive'}")
    print(f"  Record: {'Yes' if write else 'No'}")
    print()
    print("  Controls:")
    print("    r         → Reset scene")
    print("    q / Esc   → Quit")
    print("    scroll    → Zoom")
    print("    drag      → Pan camera")
    print("    space     → Pause / Resume")
    print()
    print("  Checkpoint shortcuts (VS Code):")
    print("    ⌘+R            → Checkpoint paste (replay to here)")
    print("    ⌘+Alt+R        → Recorded checkpoint")
    print("    ⌘+Ctrl+R       → Skipped checkpoint")
    print("    Shift+⌘+R      → Run scene")
    print("    ⌘+E            → Exit interactive")
    print(f"{'='*60}\n")
    print(f"  CMD: {' '.join(cmd)}\n")

    os.chdir(str(PROJECT_ROOT))
    os.execvp(cmd[0], cmd)


# ──────────────────────────────────────────────
# Checkpoint helpers (for programmatic use)
# ──────────────────────────────────────────────

CHECKPOINT_PASTE = """
# === CHECKPOINT ===
# Paste this in your scene's construct() to create a replay point.
# When running interactively, Manim jumps to the latest checkpoint.
import manim
if hasattr(manim, 'config') and manim.config.renderer == "opengl":
    self.interactive_embed()
"""

RECORDED_CHECKPOINT = """
# === RECORDED CHECKPOINT ===
# Like checkpoint, but records the segment leading up to it.
self.wait_until_bookmark("__recorded_checkpoint__")
"""

SKIPPED_CHECKPOINT = """
# === SKIPPED CHECKPOINT ===
# Skips all animation before this point (fast-forward).
self.skip_animations = False  # Re-enable from here
"""


def main():
    parser = argparse.ArgumentParser(description="TheBoringAI — Interactive Manim")
    parser.add_argument("scene", help="Path to scene file")
    parser.add_argument("class_name", help="Scene class name")
    parser.add_argument("--presenter", action="store_true",
                        help="Presenter mode (step-through)")
    parser.add_argument("--write", "-w", action="store_true",
                        help="Also write to movie file")
    args = parser.parse_args()
    launch_interactive(args.scene, args.class_name,
                       presenter=args.presenter, write=args.write)


if __name__ == "__main__":
    main()
