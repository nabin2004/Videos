# 🎬 Render & Export

---

## Render quality flags

| Flag | Resolution | FPS | Use for |
|------|-----------|-----|---------|
| `-ql` | 480p | 15 | Fast preview during development |
| `-qm` | 720p | 30 | Review / client preview |
| `-qh` | 1080p | 60 | Final delivery (web / social) |
| `-qk` | 2160p (4K) | 60 | Broadcast / cinema |

```bash
# Syntax
manim -p<quality> [options] <file.py> <ClassName>

# Examples
manim -pql scenes/intro.py IntroScene          # draft
manim -pqh --fps 60 scenes/intro.py IntroScene # 1080p production
manim -pqk --fps 60 scenes/intro.py IntroScene # 4K broadcast
```

---

## Transparent background (alpha channel)

Use when compositing over video footage or motion backgrounds:

```bash
manim -pqh --fps 60 --transparent scenes/logo_sting.py LogoStingScene
```

Output will be a `.mov` (ProRes 4444 with alpha) or `.webm`.

---

## Render a single frame (poster)

```bash
manim -s scenes/intro.py IntroScene
# Saves a PNG of the last frame
```

---

## Batch render all scenes

```bash
# render_all.sh
#!/usr/bin/env bash
set -e
QUALITY=${1:-qh}
for file in scenes/*.py; do
    # Extract class names ending in "Scene"
    classes=$(grep -E "^class \w+Scene" "$file" | sed 's/class //' | sed 's/(.*//')
    for cls in $classes; do
        echo "▶ Rendering $cls from $file"
        manim -p$QUALITY --fps 60 "$file" "$cls"
    done
done
echo "✅ All scenes rendered."
```

```bash
chmod +x render_all.sh
./render_all.sh          # 1080p
./render_all.sh qk       # 4K
```

---

## Output locations

Manim writes files to `./output/` (or `./media/` by default):

```
output/
└── videos/
    └── scenes/
        └── 1080p60/
            ├── IntroScene.mp4
            └── DataRevealScene.mp4
```

Override with `media_dir` in `manim.cfg`:
```ini
[CLI]
media_dir = ./output
```

---

## Codec recommendations

| Platform | Container | Codec | Settings |
|----------|-----------|-------|----------|
| Web / YouTube | MP4 | H.264 | `-qh` default |
| Social (Instagram / TikTok) | MP4 | H.264 | `-qh`, 9:16 aspect |
| Broadcast / NLE import | MOV | ProRes 422 | re-encode via ffmpeg |
| Compositing (After Effects) | MOV | ProRes 4444 | `--transparent` |

### Quick ffmpeg re-encode to ProRes
```bash
ffmpeg -i IntroScene.mp4 -c:v prores_ks -profile:v 3 -c:a pcm_s16le IntroScene_prores.mov
```

---

## Performance tips

- Use `-n` flag to render only specific frame ranges during debugging:  
  `manim -pql -n 0,120 scenes/intro.py IntroScene`
- Avoid `always_update_mobjects` — it re-renders every frame
- Cache heavy `SVGMobject` / `ImageMobject` loads in `setup()`
- Use `self.renderer.skip_animations = True` to skip to a point during dev
