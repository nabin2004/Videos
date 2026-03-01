#!/usr/bin/env bash
# render_all.sh — Batch render all TheBoringAI scenes
#
# Usage:
#   ./render_all.sh          # 1080p 60fps (default)
#   ./render_all.sh ql       # 480p draft
#   ./render_all.sh qk       # 4K broadcast

set -e

QUALITY=${1:-qh}
FPS=60
SCENES_DIR="scenes"

echo "═══════════════════════════════════════════════════════"
echo "  TheBoringAI — Batch Renderer"
echo "  Quality: -${QUALITY}  FPS: ${FPS}"
echo "═══════════════════════════════════════════════════════"
echo ""

count=0
errors=0

for file in ${SCENES_DIR}/*.py; do
    # Skip __init__.py and _template.py
    base=$(basename "$file")
    if [[ "$base" == "__init__.py" || "$base" == "_template.py" ]]; then
        continue
    fi

    # Extract class names ending in "Scene"
    classes=$(grep -E "^class \w+Scene" "$file" | sed 's/class //' | sed 's/(.*//') || true

    for cls in $classes; do
        echo "▶ Rendering ${cls} from ${file}..."
        if manim -p${QUALITY} --fps ${FPS} "$file" "$cls"; then
            echo "  ✅ ${cls} done."
            ((count++))
        else
            echo "  ❌ ${cls} FAILED."
            ((errors++))
        fi
        echo ""
    done
done

echo "═══════════════════════════════════════════════════════"
echo "  Done! ${count} scenes rendered, ${errors} errors."
echo "═══════════════════════════════════════════════════════"
