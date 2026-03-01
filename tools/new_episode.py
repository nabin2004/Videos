#!/usr/bin/env python3
"""
TheBoringAI — Project Scaffolding Tool
=======================================
Creates a new episode project with all boilerplate.

Usage:
    python tools/new_episode.py --series ML --num 4 --title "Regularization"
    python tools/new_episode.py --series DL --num 5 --title "GANs Explained"
"""

import argparse
import os
import re
import sys
from pathlib import Path
from textwrap import dedent

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def slugify(text: str) -> str:
    """Convert a title to a directory-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text)
    return text


def create_episode(series: str, num: int, title: str):
    slug = slugify(title)
    dirname = f"{num:02d}_{slug}"
    ep_dir = PROJECT_ROOT / "series" / series / dirname

    if ep_dir.exists():
        print(f"[ERROR] Directory already exists: {ep_dir.relative_to(PROJECT_ROOT)}")
        sys.exit(1)

    ep_dir.mkdir(parents=True, exist_ok=True)

    # Create config.yaml
    config = dedent(f"""\
        # Series video project config
        episode: {num}
        series: {series}
        title: "{title}"
        description: ""
        tags: []
        duration_target: "5-8 min"
        status: "draft"
    """)
    (ep_dir / "config.yaml").write_text(config)

    # Create scene.py from template
    scene_py = dedent(f"""\
        # series/{series}/{dirname}/scene.py
        # Episode: {title}
        # Render: make render-scene SCENE=series/{series}/{dirname}/scene.py CLASS={slug.title().replace('_', '')}Scene
        from manim import *
        import sys, os

        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        sys.path.insert(0, PROJECT_ROOT)

        from brand import *
        from typography import *
        from layout import *
        from animations import *
        from components import Opening, Closing, PauseAndPonder, ChapterCard, Watermark
        from shared.ml_components import *
        from shared.nn_visualizer import *
        from shared.math_helpers import *


        class {slug.title().replace('_', '')}Scene(Scene):
            \\"\\"\\"EP {num:02d} — {title}\\"\\"\\"

            def setup(self):
                self.camera.background_color = BG

            def construct(self):
                Opening.play(self, episode_number={num}, episode_title="{title}",
                             subtitle="{series} Series")
                Watermark.add(self)
                self.add(make_grid(opacity=0.08))

                ChapterCard.play(self, chapter=1, title="Introduction")
                self._intro()

                # TODO: Add your chapters here

                Closing.play(self, next_episode="", social_handle="@TheBoringAI")

            def _intro(self):
                title = brand_title("{title}", size=T_H1)
                self.play(FadeIn(title, run_time=NORMAL))
                self.wait(1.5)
                self.play(FadeOut(title))
    """)
    (ep_dir / "scene.py").write_text(scene_py)

    # Create notes.md
    notes = dedent(f"""\
        # {title}
        ## Episode {num} — {series} Series

        ### Script Notes
        - 

        ### Key Visuals
        - 

        ### References
        - 
    """)
    (ep_dir / "notes.md").write_text(notes)

    # Asset subdirectory
    (ep_dir / "assets").mkdir(exist_ok=True)
    (ep_dir / "assets" / ".gitkeep").touch()

    print(f"✓ Created episode: series/{series}/{dirname}/")
    print(f"  Files: scene.py, config.yaml, notes.md, assets/")
    print(f"  Render: make render-scene SCENE=series/{series}/{dirname}/scene.py")


def main():
    parser = argparse.ArgumentParser(description="Create a new TheBoringAI episode")
    parser.add_argument("--series", "-s", required=True, choices=["ML", "DL"],
                        help="Series name (ML or DL)")
    parser.add_argument("--num", "-n", type=int, required=True, help="Episode number")
    parser.add_argument("--title", "-t", required=True, help="Episode title")
    args = parser.parse_args()
    create_episode(args.series, args.num, args.title)


if __name__ == "__main__":
    main()
