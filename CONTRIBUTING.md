# Contributing to TheBoringAI

## Quick Workflow

```bash
# 1. Create a new episode
make new-episode SERIES=ML NUM=4 TITLE="Your Topic"

# 2. Edit the generated scene.py
code series/ML/04_your_topic/scene.py

# 3. Preview while editing
make preview S=series/ML/04_your_topic/scene.py C=YourTopicScene

# 4. Or use interactive mode for live editing
make interactive S=series/ML/04_your_topic/scene.py C=YourTopicScene

# 5. Render final version
make render S=series/ML/04_your_topic/scene.py C=YourTopicScene

# 6. Export for platforms
make export-youtube S=series/ML/04_your_topic/scene.py C=YourTopicScene
make export-shorts S=series/ML/04_your_topic/scene.py C=YourTopicScene
```

## Code Style

- Use `black` for formatting (line length 100)
- Use `isort` for import ordering
- Use `ruff` for linting
- Run `make format` before committing

## Scene Conventions

1. Always set `self.camera.background_color = BG` in `setup()`
2. Start with `Opening.play(...)` and end with `Closing.play(...)`
3. Use `ChapterCard.play(...)` between sections
4. Add `Watermark.add(self)` after opening
5. Use brand colors from `brand.py` — never hardcode hex values
6. Use typography helpers from `typography.py` — never use raw `Text()`
7. Use timing constants (`FAST`, `NORMAL`, `SLOW`, `EPIC`) — never hardcode durations

## Commit Messages

```
feat: add episode on regularization
fix: correct gradient arrow direction in backprop
style: reformat scenes with black
docs: update README with new shortcuts
```
