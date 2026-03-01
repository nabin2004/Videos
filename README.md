# TheBoringAI — ML/DL Animation Series

> Beautiful, branded Manim animations for Machine Learning & Deep Learning education.

```
  ╔══════════════════════════════════════════════╗
  ║          T h e B o r i n g A I               ║
  ║     ML / DL  Video Animation Pipeline        ║
  ╚══════════════════════════════════════════════╝
```

---

## Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Series Episodes](#series-episodes)
- [Components](#components)
- [Make Commands](#make-commands)
- [Exporting](#exporting)
- [Interactive Mode (OpenGL)](#interactive-mode-opengl)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Creating New Episodes](#creating-new-episodes)
- [Brand System](#brand-system)
- [Asset Management](#asset-management)
- [Development](#development)

---

## Quick Start

### 1. Install

```bash
cd Videos
make install
# — or —
pip install -e ".[dev]"
```

### 2. Preview a scene

```bash
make preview S=series/ML/01_neural_network_basics/scene.py C=NeuralNetworkBasicsScene
```

### 3. Render in high quality

```bash
make render S=series/ML/01_neural_network_basics/scene.py C=NeuralNetworkBasicsScene
```

### 4. Export for YouTube

```bash
make export-youtube S=series/ML/01_neural_network_basics/scene.py C=NeuralNetworkBasicsScene
```

That's it! Read on for the full guide.

---

## Project Structure

```
Videos/
├── brand.py                  # Colors, fonts, brand constants
├── typography.py             # Text factories (brand_text, brand_title, ...)
├── layout.py                 # Grid system, positions, safe areas
├── animations.py             # Animation presets (fly_in, pop_in, scene_wipe, ...)
├── manim.cfg                 # Default Manim configuration
├── Makefile                  # Build system (see Make Commands)
├── pyproject.toml            # Python project config
│
├── components/               # Reusable video components
│   ├── opening.py            #   Opening titles & intros
│   ├── closing.py            #   Outros & CTAs
│   ├── pause_ponder.py       #   "Pause & Ponder" interactive breaks
│   ├── chapter_card.py       #   Chapter/section cards
│   ├── bumper.py             #   Brand bumpers & transitions
│   ├── watermark.py          #   Corner watermarks & progress bars
│   ├── subscribe_cta.py      #   Subscribe popups & end screens
│   └── lower_thirds.py       #   Speaker/topic/source lower thirds
│
├── shared/                   # Shared ML/DL visualization utilities
│   ├── ml_components.py      #   Neurons, layers, networks, tensors
│   ├── nn_visualizer.py      #   Forward pass, backprop, attention animations
│   └── math_helpers.py       #   LaTeX equations, activation functions, plots
│
├── series/                   # Video episodes organized by series
│   ├── ML/                   #   Machine Learning series
│   │   ├── 01_neural_network_basics/
│   │   │   ├── scene.py      #     Episode scene file
│   │   │   └── config.yaml   #     Episode metadata
│   │   ├── 02_gradient_descent/
│   │   └── 03_loss_functions/
│   ├── DL/                   #   Deep Learning series
│   │   ├── 01_backpropagation/
│   │   ├── 02_activation_functions/
│   │   ├── 03_cnn_explained/
│   │   └── 04_attention_mechanism/
│   └── common/               #   Shared intro/outro scenes
│       ├── intro/
│       └── outro/
│
├── scenes/                   # Legacy/standalone scenes
│
├── tools/                    # CLI tools
│   ├── export.py             #   Multi-format export system
│   ├── interactive.py        #   OpenGL live editing launcher
│   ├── new_episode.py        #   Episode scaffolding
│   └── assets.py             #   Asset manager
│
├── assets/                   # Media assets
│   ├── audio/sfx/            #   Sound effects
│   ├── audio/music/          #   Background music
│   ├── images/thumbnails/    #   YouTube thumbnails
│   ├── images/overlays/      #   Overlay graphics
│   └── logos/                #   Logo files
│
├── exports/                  # Exported videos (by profile)
│
├── .vscode/                  # VS Code configuration
│   ├── settings.json         #   Editor settings
│   ├── tasks.json            #   Build tasks
│   └── keybindings.json      #   Keyboard shortcuts
│
└── agents/                   # AI agent prompts (reference)
```

---

## Series Episodes

### ML Series (Machine Learning)

| # | Episode | Directory |
|---|---------|-----------|
| 01 | What is a Neural Network? | `series/ML/01_neural_network_basics/` |
| 02 | Gradient Descent | `series/ML/02_gradient_descent/` |
| 03 | Loss Functions | `series/ML/03_loss_functions/` |

### DL Series (Deep Learning)

| # | Episode | Directory |
|---|---------|-----------|
| 01 | Backpropagation | `series/DL/01_backpropagation/` |
| 02 | Activation Functions | `series/DL/02_activation_functions/` |
| 03 | CNN Explained | `series/DL/03_cnn_explained/` |
| 04 | Attention Mechanism | `series/DL/04_attention_mechanism/` |

Each episode directory contains:
- **`scene.py`** — The Manim scene (render this)
- **`config.yaml`** — Episode metadata (title, tags, status)
- **`notes.md`** — Script notes (optional)
- **`assets/`** — Episode-specific assets (optional)

---

## Components

Drop-in video building blocks. Import and call in any scene:

```python
from components import Opening, Closing, PauseAndPonder, ChapterCard

class MyScene(Scene):
    def construct(self):
        # 1. Opening title sequence
        Opening.play(self, episode_number=1, episode_title="My Episode")

        # 2. Chapter card
        ChapterCard.play(self, chapter=1, title="Introduction")

        # ... your content ...

        # 3. Pause & Ponder break
        PauseAndPonder.play(self, "What do you think happens next?")
        PauseAndPonder.reveal(self, "The answer!")

        # 4. Closing with summary
        Closing.with_summary(self, points=[
            "Point one",
            "Point two",
        ], next_episode="Next Episode Title")
```

### Available Components

| Component | Methods | Description |
|-----------|---------|-------------|
| **Opening** | `.play()`, `.cold_open()`, `.minimal()` | Episode intro sequences |
| **Closing** | `.play()`, `.with_summary()`, `.quick()` | Outro & next episode tease |
| **PauseAndPonder** | `.play()`, `.with_choices()`, `.countdown()`, `.reveal()` | Interactive thinking breaks |
| **ChapterCard** | `.play()`, `.mini()` | Section dividers |
| **Bumper** | `.play()`, `.text()`, `.wipe()`, `.logo_flash()` | Brand transitions |
| **Watermark** | `.add()`, `.add_with_episode()`, `.progress_bar()` | Corner watermarks |
| **SubscribeCTA** | `.popup()`, `.end_screen()` | Subscribe call-to-action |
| **LowerThirds** | `.speaker()`, `.topic()`, `.source()` | Broadcaster-style info bars |
| **OctopusCreature** | `.look_at()`, `.hold_items()`, `.change_mood()` | Playful 8-armed mascot for teaching |
| **ProfessorOctopus** | *inherits* + glasses & mortarboard | Teacher / explainer variant |
| **BabyOctopus** | *inherits* + oversized eyes | Curious / question-asker variant |
| **NeuralOctopus** | `.pulse_tentacle()` | Tentacles as neural connections |
| **DataOctopus** | `.label_tentacles()` | Labeled tentacles for data pipelines |
| **OctopusAnimations** | `.entrance()`, `.wave_hello()`, `.present()`, `.juggle()` | Pre-built animation sequences |
| **OctopusTeaches** | `.concept()`, `.step_by_step()`, `.vs()`, `.quiz()`, `.pipeline()` | High-level teaching helpers |

> **Full octopus docs →** [docs/octopus.md](docs/octopus.md)

---

## Make Commands

```bash
make help                    # Show all commands
```

### Rendering

```bash
make preview S=<scene> C=<class>       # Quick preview (low quality)
make render S=<scene> C=<class>        # High quality render
make render-4k S=<scene> C=<class>     # 4K production render
make render-all                        # Render ALL episodes
make render-ml                         # Render all ML episodes
make render-dl                         # Render all DL episodes
```

### Exporting

```bash
make export-youtube S=<scene> C=<class>       # YouTube 1080p
make export-4k S=<scene> C=<class>            # YouTube 4K
make export-shorts S=<scene> C=<class>        # Shorts / TikTok (9:16)
make export-facebook S=<scene> C=<class>      # Facebook (1:1)
make export-instagram S=<scene> C=<class>     # Instagram (1:1)
make export-twitter S=<scene> C=<class>       # Twitter/X (720p)
make export-transparent S=<scene> C=<class>   # ProRes 4444 (alpha)
make export-gif S=<scene> C=<class>           # Animated GIF
make export-all S=<scene> C=<class>           # ALL profiles
make list-profiles                            # Show all profiles
```

### Interactive

```bash
make interactive S=<scene> C=<class>          # OpenGL live editing
make presenter S=<scene> C=<class>            # Presenter step-through
make interactive-record S=<scene> C=<class>   # Interactive + record
```

### Project

```bash
make new-episode SERIES=ML NUM=4 TITLE="Regularization"  # Create episode
make status                                                # Project overview
make assets-scan                                           # Catalog assets
make assets-validate                                       # Check directories
```

### Development

```bash
make install          # Install dependencies
make lint             # Check code style
make format           # Auto-format code
make clean            # Remove outputs & caches
make clean-exports    # Clear exported files
make clean-all        # Full clean
```

---

## Exporting

### Export Profiles

| Profile | Resolution | Aspect | FPS | Codec | Format | Use Case |
|---------|-----------|--------|-----|-------|--------|----------|
| `youtube_1080p` | 1920×1080 | 16:9 | 60 | H.264 | .mp4 | YouTube Full HD |
| `youtube_4k` | 3840×2160 | 16:9 | 60 | H.264 | .mp4 | YouTube 4K UHD |
| `shorts` | 1080×1920 | 9:16 | 60 | H.264 | .mp4 | Shorts / TikTok |
| `facebook` | 1080×1080 | 1:1 | 30 | H.264 | .mp4 | Facebook Posts |
| `instagram` | 1080×1080 | 1:1 | 30 | H.264 | .mp4 | Instagram Posts |
| `twitter` | 1280×720 | 16:9 | 30 | H.264 | .mp4 | Twitter/X |
| `transparent` | 1920×1080 | 16:9 | 60 | ProRes | .mov | Compositing |
| `gif_preview` | 640×360 | 16:9 | 15 | GIF | .gif | Social previews |

### Direct Python usage

```python
from tools.export import PROFILES, render_scene

render_scene("series/ML/01_.../scene.py", "NeuralNetworkBasicsScene",
             PROFILES["shorts"])
```

Exports land in `exports/<profile_name>/`.

---

## Interactive Mode (OpenGL)

Manim's OpenGL renderer enables **live, interactive editing** with real-time preview:

```bash
# Launch interactive mode
make interactive S=series/ML/01_neural_network_basics/scene.py C=NeuralNetworkBasicsScene

# With recording
make interactive-record S=series/ML/01_neural_network_basics/scene.py C=NeuralNetworkBasicsScene

# Presenter mode (step through animations)
make presenter S=series/ML/01_neural_network_basics/scene.py C=NeuralNetworkBasicsScene
```

### Window Controls

| Key | Action |
|-----|--------|
| `r` | Reset / Replay scene |
| `q` / `Esc` | Quit |
| `Space` | Pause / Resume |
| `Scroll` | Zoom in/out |
| `Drag` | Pan camera |

### Checkpoints

Insert checkpoints in your `construct()` method to create replay points:

```python
def construct(self):
    # ... some animations ...

    self.interactive_embed()  # ▶ Manim pauses here in interactive mode
                              #   You can inspect/modify objects in the REPL

    # ... more animations ...
```

---

## Keyboard Shortcuts

### VS Code (copy to your keybindings.json)

| Shortcut | Action |
|----------|--------|
| `Shift+Super+R` | Run current scene in interactive mode |
| `Super+R` | Insert checkpoint (replay point) |
| `Super+Alt+R` | Insert recorded checkpoint |
| `Super+Ctrl+R` | Insert skipped checkpoint |
| `Super+E` | Exit interactive Manim (Ctrl+C) |
| `Super+Alt+/` | Fold all block comments |

### VS Code Tasks (Ctrl+Shift+B)

Pre-configured build tasks:
- **Manim: Preview Scene** — Quick low-quality preview
- **Manim: Render HD** — High quality render
- **Manim: Render 4K** — Production quality
- **Manim: Interactive (OpenGL)** — Live editing
- **Export: YouTube 1080p / Shorts / All Profiles**

---

## Creating New Episodes

### Using the scaffold tool

```bash
make new-episode SERIES=ML NUM=4 TITLE="Regularization"
make new-episode SERIES=DL NUM=5 TITLE="GANs Explained"
```

This creates:
```
series/ML/04_regularization/
├── scene.py          # Pre-filled template with all imports
├── config.yaml       # Episode metadata
├── notes.md          # Script notes
└── assets/           # Episode-specific assets
```

---

## Brand System

### Colors

| Name | Hex | Usage |
|------|-----|-------|
| `BG` / `BRAND_MIDNIGHT` | `#0A0E1A` | Background |
| `PRIMARY` / `BRAND_ELECTRIC` | `#00F5FF` | Primary accent (cyan) |
| `SECONDARY` / `BRAND_PLASMA` | `#BF5AF2` | Secondary (purple) |
| `HIGHLIGHT` / `BRAND_NOVA` | `#FF6B35` | Highlights (orange) |
| `EMPHASIS` / `BRAND_SOLAR` | `#FFD60A` | Emphasis (yellow) |
| `TEXT` / `BRAND_GHOST` | `#E8EAF0` | Body text |

### ML-Specific Colors

| Name | Hex | Usage |
|------|-----|-------|
| `NEURON_COLOR` | `#00F5FF` | Neuron nodes |
| `WEIGHT_COLOR` | `#BF5AF2` | Connection weights |
| `ACTIVATION_COLOR` | `#FF6B35` | Activation highlights |
| `LOSS_COLOR` | `#FF3B5C` | Loss/error curves |
| `GRADIENT_COLOR` | `#FFD60A` | Gradient arrows |

### Typography

| Scale | Size | Usage |
|-------|------|-------|
| `T_HERO` | 1.10 | Hero/splash titles |
| `T_H1` | 0.80 | Section headings |
| `T_H2` | 0.60 | Sub-headings |
| `T_BODY` | 0.42 | Body text |
| `T_CAPTION` | 0.32 | Captions |
| `T_LABEL` | 0.28 | Small labels |

### Fonts

| Font | Usage |
|------|-------|
| **Space Grotesk** | Hero titles, display text |
| **Inter** | UI text, body copy |
| **JetBrains Mono** | Code blocks |

---

## Asset Management

```bash
make assets-scan       # Scan & catalog all assets → assets/catalog.json
make assets-validate   # Check all directories exist
make assets-tree       # Print asset directory tree
```

---

## Development

### Requirements

- **Python** >= 3.9
- **Manim Community** >= 0.18.0
- **ffmpeg** (for exports)
- **NumPy** >= 1.21.0
- **LaTeX** (optional, for math equations)
- **OpenGL** support (for interactive mode)

### Code Style

```bash
make lint      # Check with ruff + black
make format    # Auto-format with black + isort
```

---

## License

MIT

---

*Built with [Manim Community](https://www.manim.community/) v0.18+ · Python 3.9+*
