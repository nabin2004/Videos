#!/usr/bin/env python3
"""
TheBoringAI — Asset Manager
============================
Organize, validate, and catalog project assets.

Usage:
    python tools/assets.py scan              # Scan & catalog all assets
    python tools/assets.py validate          # Check for missing/broken refs
    python tools/assets.py tree              # Print asset directory tree
"""

import argparse
import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ASSET_DIRS = {
    "audio/sfx": [".wav", ".mp3", ".ogg", ".flac"],
    "audio/music": [".wav", ".mp3", ".ogg", ".flac"],
    "images/thumbnails": [".png", ".jpg", ".jpeg", ".webp"],
    "images/overlays": [".png", ".svg"],
    "logos": [".png", ".svg", ".pdf"],
}

EXPORT_DIRS = {
    "youtube_1080p": "exports/youtube_1080p",
    "youtube_4k": "exports/youtube_4k",
    "shorts": "exports/shorts",
    "facebook": "exports/facebook",
    "instagram": "exports/instagram",
    "twitter": "exports/twitter",
    "transparent": "exports/transparent",
    "gif_preview": "exports/gif_preview",
}


def scan_assets():
    """Scan all asset directories and return a catalog."""
    catalog = {}
    assets_root = PROJECT_ROOT / "assets"
    total = 0

    for subdir, extensions in ASSET_DIRS.items():
        dir_path = assets_root / subdir
        files = []
        if dir_path.exists():
            for f in dir_path.iterdir():
                if f.suffix.lower() in extensions:
                    files.append({
                        "name": f.name,
                        "size": f.stat().st_size,
                        "path": str(f.relative_to(PROJECT_ROOT)),
                    })
        catalog[subdir] = files
        total += len(files)

    print(f"\n  Asset Catalog — {total} files found")
    print(f"  {'='*50}")
    for subdir, files in catalog.items():
        print(f"  {subdir}/ ({len(files)} files)")
        for f in files:
            size_kb = f["size"] / 1024
            print(f"    {f['name']:30s}  {size_kb:>8.1f} KB")

    # Save catalog
    catalog_path = PROJECT_ROOT / "assets" / "catalog.json"
    with open(catalog_path, "w") as fp:
        json.dump(catalog, fp, indent=2)
    print(f"\n  Catalog saved → assets/catalog.json")
    return catalog


def validate_assets():
    """Check that all expected asset directories exist."""
    print(f"\n  Asset Validation")
    print(f"  {'='*50}")
    ok = True
    assets_root = PROJECT_ROOT / "assets"

    for subdir in ASSET_DIRS:
        dir_path = assets_root / subdir
        exists = dir_path.exists()
        status = "✓" if exists else "✗ MISSING"
        print(f"  {status:12s}  assets/{subdir}/")
        if not exists:
            ok = False

    for name, path in EXPORT_DIRS.items():
        dir_path = PROJECT_ROOT / path
        exists = dir_path.exists()
        status = "✓" if exists else "—"
        print(f"  {status:12s}  {path}/")

    print()
    if ok:
        print("  All asset directories present.")
    else:
        print("  Some directories missing. Run: make setup-dirs")
    return ok


def print_tree():
    """Print asset directory structure."""
    print(f"\n  Asset Tree")
    print(f"  {'='*50}")
    for root, dirs, files in os.walk(PROJECT_ROOT / "assets"):
        depth = Path(root).relative_to(PROJECT_ROOT / "assets").parts
        indent = "  " + "│  " * len(depth)
        dirname = Path(root).name
        print(f"{indent}📁 {dirname}/")
        for f in sorted(files):
            if f == ".gitkeep":
                continue
            print(f"{indent}│  📄 {f}")


def main():
    parser = argparse.ArgumentParser(description="TheBoringAI — Asset Manager")
    parser.add_argument("action", choices=["scan", "validate", "tree"],
                        help="Action to perform")
    args = parser.parse_args()

    if args.action == "scan":
        scan_assets()
    elif args.action == "validate":
        validate_assets()
    elif args.action == "tree":
        print_tree()


if __name__ == "__main__":
    main()
