#!/usr/bin/env python3
"""
TheBoringAI — Export System
===========================
Multi-format export with presets for YouTube, Shorts, Facebook, Instagram,
Twitter/X, transparent overlays, and custom profiles.

Usage:
    python tools/export.py --scene series/ML/01_neural_network_basics/scene.py \
                           --class NeuralNetworkBasicsScene \
                           --profile youtube_1080p

    python tools/export.py --scene scene.py --class MyScene --profile all

Profiles:
    youtube_1080p   — 1920×1080  16:9  60fps  H.264     (.mp4)
    youtube_4k      — 3840×2160  16:9  60fps  H.264     (.mp4)
    shorts          — 1080×1920   9:16 60fps  H.264     (.mp4)
    facebook        — 1080×1080   1:1  30fps  H.264     (.mp4)
    instagram       — 1080×1080   1:1  30fps  H.264     (.mp4)
    twitter         — 1280×720   16:9  30fps  H.264     (.mp4)
    transparent     — 1920×1080  16:9  60fps  ProRes    (.mov)
    gif_preview     — 640×360    16:9  15fps  GIF       (.gif)
    all             — Renders ALL profiles above
"""

import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ──────────────────────────────────────────────
# Export Profiles
# ──────────────────────────────────────────────

@dataclass
class ExportProfile:
    name: str
    width: int
    height: int
    fps: int
    codec: str          # h264, prores, gif
    container: str      # mp4, mov, gif
    quality: str        # low_quality, medium_quality, high_quality, production_quality
    bitrate: str = "8M"
    crf: int = 18
    pixel_format: str = "yuv420p"
    audio_codec: str = "aac"
    audio_bitrate: str = "192k"
    description: str = ""
    extra_ffmpeg: list = field(default_factory=list)


PROFILES = {
    "youtube_1080p": ExportProfile(
        name="youtube_1080p",
        width=1920, height=1080, fps=60,
        codec="h264", container="mp4",
        quality="high_quality",
        bitrate="12M", crf=18,
        description="YouTube Full HD — 16:9 @ 60fps",
    ),
    "youtube_4k": ExportProfile(
        name="youtube_4k",
        width=3840, height=2160, fps=60,
        codec="h264", container="mp4",
        quality="production_quality",
        bitrate="40M", crf=15,
        description="YouTube 4K UHD — 16:9 @ 60fps",
    ),
    "shorts": ExportProfile(
        name="shorts",
        width=1080, height=1920, fps=60,
        codec="h264", container="mp4",
        quality="high_quality",
        bitrate="10M", crf=18,
        description="YouTube Shorts / TikTok — 9:16 @ 60fps",
    ),
    "facebook": ExportProfile(
        name="facebook",
        width=1080, height=1080, fps=30,
        codec="h264", container="mp4",
        quality="high_quality",
        bitrate="8M", crf=20,
        description="Facebook / Instagram Square — 1:1 @ 30fps",
    ),
    "instagram": ExportProfile(
        name="instagram",
        width=1080, height=1080, fps=30,
        codec="h264", container="mp4",
        quality="high_quality",
        bitrate="8M", crf=20,
        description="Instagram Square — 1:1 @ 30fps",
    ),
    "twitter": ExportProfile(
        name="twitter",
        width=1280, height=720, fps=30,
        codec="h264", container="mp4",
        quality="medium_quality",
        bitrate="5M", crf=22,
        description="Twitter/X — 16:9 @ 30fps (720p)",
    ),
    "transparent": ExportProfile(
        name="transparent",
        width=1920, height=1080, fps=60,
        codec="prores", container="mov",
        quality="high_quality",
        bitrate="80M", crf=0,
        pixel_format="yuva444p10le",
        description="Transparent overlay — ProRes 4444 with alpha",
        extra_ffmpeg=["-profile:v", "4444"],
    ),
    "gif_preview": ExportProfile(
        name="gif_preview",
        width=640, height=360, fps=15,
        codec="gif", container="gif",
        quality="low_quality",
        bitrate="0", crf=0,
        description="GIF preview — small animated preview",
    ),
}


# ──────────────────────────────────────────────
# Utility helpers
# ──────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXPORT_DIR = PROJECT_ROOT / "exports"


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def get_manim_quality_flag(quality: str) -> str:
    return {
        "low_quality": "-ql",
        "medium_quality": "-qm",
        "high_quality": "-qh",
        "production_quality": "-qp",
    }.get(quality, "-qh")


def render_scene(scene_path: str, class_name: str, profile: ExportProfile,
                 dry_run: bool = False) -> Optional[Path]:
    """Render a scene with Manim at the given quality, then transcode with ffmpeg."""

    # Step 1: Render with Manim at max quality
    quality_flag = get_manim_quality_flag(profile.quality)
    manim_cmd = [
        "manim", quality_flag,
        "--fps", str(profile.fps),
        "--disable_caching",
        "-o", f"{class_name}_{profile.name}",
        str(scene_path), class_name,
    ]

    # For transparent renders, pass --transparent
    if profile.codec == "prores":
        manim_cmd.insert(1, "--transparent")

    print(f"\n{'='*60}")
    print(f"  EXPORT: {profile.description}")
    print(f"  Resolution: {profile.width}×{profile.height} @ {profile.fps}fps")
    print(f"  Codec: {profile.codec} / .{profile.container}")
    print(f"{'='*60}")
    print(f"  CMD: {' '.join(manim_cmd)}\n")

    if dry_run:
        print("  [DRY RUN] Skipping render.")
        return None

    result = subprocess.run(manim_cmd, cwd=str(PROJECT_ROOT))
    if result.returncode != 0:
        print(f"  [ERROR] Manim render failed (exit {result.returncode})")
        return None

    # Step 2: Find the rendered file
    media_dir = PROJECT_ROOT / "output" / "videos" / Path(scene_path).stem
    rendered = _find_latest_video(media_dir)
    if not rendered:
        # Also check media/videos path
        media_dir = PROJECT_ROOT / "media" / "videos" / Path(scene_path).stem
        rendered = _find_latest_video(media_dir)

    if not rendered:
        print("  [ERROR] Could not locate rendered output.")
        return None

    # Step 3: Transcode / resize with ffmpeg
    profile_dir = EXPORT_DIR / profile.name
    ensure_dir(profile_dir)
    out_file = profile_dir / f"{class_name}.{profile.container}"

    if profile.codec == "gif":
        ffmpeg_cmd = _build_gif_cmd(rendered, out_file, profile)
    elif profile.codec == "prores":
        ffmpeg_cmd = _build_prores_cmd(rendered, out_file, profile)
    else:
        ffmpeg_cmd = _build_h264_cmd(rendered, out_file, profile)

    print(f"  Transcoding → {out_file.relative_to(PROJECT_ROOT)}")
    result = subprocess.run(ffmpeg_cmd, cwd=str(PROJECT_ROOT))

    if result.returncode != 0:
        print(f"  [ERROR] ffmpeg failed (exit {result.returncode})")
        return None

    size_mb = out_file.stat().st_size / (1024 * 1024)
    print(f"  ✓ Exported: {out_file.relative_to(PROJECT_ROOT)} ({size_mb:.1f} MB)")
    return out_file


def _find_latest_video(media_dir: Path) -> Optional[Path]:
    """Find the most recently modified video file in a directory tree."""
    if not media_dir.exists():
        return None
    candidates = []
    for ext in ("*.mp4", "*.mov", "*.webm"):
        candidates.extend(media_dir.rglob(ext))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _build_h264_cmd(src: Path, dst: Path, p: ExportProfile) -> list:
    return [
        "ffmpeg", "-y", "-i", str(src),
        "-vf", f"scale={p.width}:{p.height}:force_original_aspect_ratio=decrease,"
               f"pad={p.width}:{p.height}:(ow-iw)/2:(oh-ih)/2:color=0x0A0E1A",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", str(p.crf),
        "-maxrate", p.bitrate,
        "-bufsize", str(int(p.bitrate.replace("M", "")) * 2) + "M" if "M" in p.bitrate else p.bitrate,
        "-pix_fmt", p.pixel_format,
        "-movflags", "+faststart",
        "-r", str(p.fps),
        str(dst),
    ]


def _build_prores_cmd(src: Path, dst: Path, p: ExportProfile) -> list:
    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-vf", f"scale={p.width}:{p.height}:force_original_aspect_ratio=decrease,"
               f"pad={p.width}:{p.height}:(ow-iw)/2:(oh-ih)/2:color=0x0A0E1A@0",
        "-c:v", "prores_ks",
        "-pix_fmt", p.pixel_format,
        "-r", str(p.fps),
    ]
    cmd.extend(p.extra_ffmpeg)
    cmd.append(str(dst))
    return cmd


def _build_gif_cmd(src: Path, dst: Path, p: ExportProfile) -> list:
    palette = str(dst.with_suffix(".palette.png"))
    # Two-pass GIF for better quality
    # We run palette generation first, then combine
    subprocess.run([
        "ffmpeg", "-y", "-i", str(src),
        "-vf", f"fps={p.fps},scale={p.width}:-1:flags=lanczos,palettegen=max_colors=128",
        palette,
    ])
    return [
        "ffmpeg", "-y", "-i", str(src), "-i", palette,
        "-lavfi", f"fps={p.fps},scale={p.width}:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer",
        str(dst),
    ]


# ──────────────────────────────────────────────
# Batch export helpers
# ──────────────────────────────────────────────

def export_all_profiles(scene_path: str, class_name: str, dry_run: bool = False):
    """Render a scene in ALL export profiles."""
    results = {}
    for name, profile in PROFILES.items():
        out = render_scene(scene_path, class_name, profile, dry_run=dry_run)
        results[name] = str(out) if out else "FAILED"

    print(f"\n{'='*60}")
    print("  EXPORT SUMMARY")
    print(f"{'='*60}")
    for name, path in results.items():
        status = "✓" if path != "FAILED" else "✗"
        print(f"  {status}  {name:20s}  →  {path}")
    return results


def list_profiles():
    """Print all available export profiles."""
    print(f"\n{'='*60}")
    print("  AVAILABLE EXPORT PROFILES")
    print(f"{'='*60}")
    for name, p in PROFILES.items():
        ratio = f"{p.width}×{p.height}"
        print(f"  {name:20s}  {ratio:>12s}  {p.fps:>3d}fps  {p.codec:>6s}  .{p.container}  — {p.description}")


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="TheBoringAI — Multi-format Export System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--scene", "-s", help="Path to the scene .py file")
    parser.add_argument("--class", "-c", dest="class_name", help="Scene class name")
    parser.add_argument("--profile", "-p", default="youtube_1080p",
                        help="Export profile name or 'all' (default: youtube_1080p)")
    parser.add_argument("--list", "-l", action="store_true", help="List available profiles")
    parser.add_argument("--dry-run", action="store_true", help="Show commands without executing")
    args = parser.parse_args()

    if args.list:
        list_profiles()
        return

    if not args.scene or not args.class_name:
        parser.error("--scene and --class are required for export.")

    if args.profile == "all":
        export_all_profiles(args.scene, args.class_name, dry_run=args.dry_run)
    elif args.profile in PROFILES:
        render_scene(args.scene, args.class_name, PROFILES[args.profile], dry_run=args.dry_run)
    else:
        print(f"Unknown profile: {args.profile}")
        list_profiles()
        sys.exit(1)


if __name__ == "__main__":
    main()
