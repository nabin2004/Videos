# =============================================================================
#  TheBoringAI — Makefile
#  Manim Animation Pipeline for ML/DL Video Series
# =============================================================================
#
#  Quick Reference:
#    make help               Show all available targets
#    make preview S=...      Preview a scene (low quality, fast)
#    make render S=...       Render a scene (high quality)
#    make render-all         Render ALL series episodes
#    make export S=... P=... Export for a platform
#    make interactive S=...  OpenGL live editing
#    make new-episode        Scaffold a new episode
#    make clean              Remove output artifacts
#
# =============================================================================

# ─── Configuration ──────────────────────────────────────────────────────────

PYTHON        := python3
MANIM         := manim
PROJECT_ROOT  := $(shell pwd)
EXPORT_TOOL   := $(PROJECT_ROOT)/tools/export.py
INTERACTIVE   := $(PROJECT_ROOT)/tools/interactive.py
NEW_EP_TOOL   := $(PROJECT_ROOT)/tools/new_episode.py
ASSET_TOOL    := $(PROJECT_ROOT)/tools/assets.py

# User variables (pass on command line)
S             ?=                    # Scene file path
C             ?=                    # Scene class name
P             ?= youtube_1080p      # Export profile
SERIES        ?= ML                 # Series (ML or DL)
NUM           ?= 1                  # Episode number
TITLE         ?= Untitled           # Episode title
Q             ?= h                  # Quality: l, m, h, p

# Quality mapping
QUALITY_l := -ql
QUALITY_m := -qm
QUALITY_h := -qh
QUALITY_p := -qp
QUALITY   := $(QUALITY_$(Q))

.DEFAULT_GOAL := help

# ─── Core Targets ───────────────────────────────────────────────────────────

.PHONY: help
help: ## Show this help message
	@echo ""
	@echo "  ╔══════════════════════════════════════════════════════╗"
	@echo "  ║       TheBoringAI — Manim Animation Pipeline        ║"
	@echo "  ╚══════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  Usage: make <target> [VAR=value ...]"
	@echo ""
	@echo "  ─── Rendering ───────────────────────────────────────"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "  ─── Variables ───────────────────────────────────────"
	@echo "  S=<path>     Scene file     (e.g., series/ML/01_.../scene.py)"
	@echo "  C=<class>    Scene class    (e.g., NeuralNetworkBasicsScene)"
	@echo "  P=<profile>  Export profile (youtube_1080p, shorts, facebook, ...)"
	@echo "  Q=<quality>  Quality        (l=low, m=med, h=high, p=production)"
	@echo "  SERIES=ML|DL Series name"
	@echo "  NUM=<int>    Episode number"
	@echo "  TITLE=<str>  Episode title"
	@echo ""

# ─── Rendering ──────────────────────────────────────────────────────────────

.PHONY: preview
preview: _check-scene ## Preview a scene (low quality, fast)
	$(MANIM) -ql --preview $(S) $(C)

.PHONY: render
render: _check-scene ## Render a scene (high quality)
	$(MANIM) $(QUALITY) $(S) $(C)

.PHONY: render-4k
render-4k: _check-scene ## Render a scene in 4K
	$(MANIM) -qp --fps 60 $(S) $(C)

.PHONY: render-scene
render-scene: render ## Alias for 'render'

.PHONY: render-all
render-all: ## Render ALL series episodes (high quality)
	@echo "  Rendering all ML episodes..."
	@for dir in series/ML/*/; do \
		if [ -f "$$dir/scene.py" ]; then \
			echo "  → $$dir"; \
			CLASS=$$(grep -oP 'class \K\w+Scene' "$$dir/scene.py" | head -1); \
			$(MANIM) $(QUALITY) "$$dir/scene.py" $$CLASS || true; \
		fi; \
	done
	@echo "  Rendering all DL episodes..."
	@for dir in series/DL/*/; do \
		if [ -f "$$dir/scene.py" ]; then \
			echo "  → $$dir"; \
			CLASS=$$(grep -oP 'class \K\w+Scene' "$$dir/scene.py" | head -1); \
			$(MANIM) $(QUALITY) "$$dir/scene.py" $$CLASS || true; \
		fi; \
	done
	@echo "  ✓ All episodes rendered."

.PHONY: render-ml
render-ml: ## Render all ML series episodes
	@for dir in series/ML/*/; do \
		if [ -f "$$dir/scene.py" ]; then \
			echo "  → $$dir"; \
			CLASS=$$(grep -oP 'class \K\w+Scene' "$$dir/scene.py" | head -1); \
			$(MANIM) $(QUALITY) "$$dir/scene.py" $$CLASS || true; \
		fi; \
	done

.PHONY: render-dl
render-dl: ## Render all DL series episodes
	@for dir in series/DL/*/; do \
		if [ -f "$$dir/scene.py" ]; then \
			echo "  → $$dir"; \
			CLASS=$$(grep -oP 'class \K\w+Scene' "$$dir/scene.py" | head -1); \
			$(MANIM) $(QUALITY) "$$dir/scene.py" $$CLASS || true; \
		fi; \
	done

.PHONY: render-examples
render-examples: ## Render all example scenes (low quality)
	@echo "  Rendering examples..."
	@for f in examples/*.py; do \
		echo "  → $$f"; \
		CLASS=$$(grep -oP 'class \K\w+' "$$f" | head -1); \
		$(MANIM) -ql "$$f" $$CLASS || true; \
	done
	@echo "  ✓ All examples rendered."

# ─── Exporting ──────────────────────────────────────────────────────────────

.PHONY: export
export: _check-scene ## Export scene for a platform (P=youtube_1080p)
	$(PYTHON) $(EXPORT_TOOL) --scene $(S) --class $(C) --profile $(P)

.PHONY: export-youtube
export-youtube: _check-scene ## Export for YouTube 1080p
	$(PYTHON) $(EXPORT_TOOL) --scene $(S) --class $(C) --profile youtube_1080p

.PHONY: export-4k
export-4k: _check-scene ## Export for YouTube 4K
	$(PYTHON) $(EXPORT_TOOL) --scene $(S) --class $(C) --profile youtube_4k

.PHONY: export-shorts
export-shorts: _check-scene ## Export for YouTube Shorts / TikTok (9:16)
	$(PYTHON) $(EXPORT_TOOL) --scene $(S) --class $(C) --profile shorts

.PHONY: export-facebook
export-facebook: _check-scene ## Export for Facebook (1:1)
	$(PYTHON) $(EXPORT_TOOL) --scene $(S) --class $(C) --profile facebook

.PHONY: export-instagram
export-instagram: _check-scene ## Export for Instagram (1:1)
	$(PYTHON) $(EXPORT_TOOL) --scene $(S) --class $(C) --profile instagram

.PHONY: export-twitter
export-twitter: _check-scene ## Export for Twitter/X (720p)
	$(PYTHON) $(EXPORT_TOOL) --scene $(S) --class $(C) --profile twitter

.PHONY: export-transparent
export-transparent: _check-scene ## Export transparent ProRes 4444 (.mov)
	$(PYTHON) $(EXPORT_TOOL) --scene $(S) --class $(C) --profile transparent

.PHONY: export-gif
export-gif: _check-scene ## Export animated GIF preview
	$(PYTHON) $(EXPORT_TOOL) --scene $(S) --class $(C) --profile gif_preview

.PHONY: export-all
export-all: _check-scene ## Export scene in ALL profiles
	$(PYTHON) $(EXPORT_TOOL) --scene $(S) --class $(C) --profile all

.PHONY: list-profiles
list-profiles: ## List all export profiles
	$(PYTHON) $(EXPORT_TOOL) --list

# ─── Interactive / OpenGL ───────────────────────────────────────────────────

.PHONY: interactive
interactive: _check-scene ## Launch OpenGL interactive mode
	$(PYTHON) $(INTERACTIVE) $(S) $(C)

.PHONY: presenter
presenter: _check-scene ## Launch presenter mode (step-through)
	$(PYTHON) $(INTERACTIVE) --presenter $(S) $(C)

.PHONY: interactive-record
interactive-record: _check-scene ## Interactive mode + record to file
	$(PYTHON) $(INTERACTIVE) --write $(S) $(C)

# ─── Project Management ────────────────────────────────────────────────────

.PHONY: new-episode
new-episode: ## Create a new episode (SERIES=ML NUM=4 TITLE="...")
	$(PYTHON) $(NEW_EP_TOOL) --series $(SERIES) --num $(NUM) --title "$(TITLE)"

.PHONY: assets-scan
assets-scan: ## Scan and catalog all assets
	$(PYTHON) $(ASSET_TOOL) scan

.PHONY: assets-validate
assets-validate: ## Validate asset directories
	$(PYTHON) $(ASSET_TOOL) validate

.PHONY: assets-tree
assets-tree: ## Show asset directory tree
	$(PYTHON) $(ASSET_TOOL) tree

# ─── Development ────────────────────────────────────────────────────────────

.PHONY: install
install: ## Install dependencies
	pip install -e ".[dev]"

.PHONY: lint
lint: ## Run linters (ruff + black check)
	ruff check .
	black --check .

.PHONY: format
format: ## Auto-format code
	black .
	isort .

.PHONY: typecheck
typecheck: ## Run type checking
	mypy --ignore-missing-imports brand.py typography.py layout.py animations.py

.PHONY: test
test: ## Run tests (if any)
	$(PYTHON) -m pytest tests/ -v 2>/dev/null || echo "  No tests found yet."

# ─── Setup ──────────────────────────────────────────────────────────────────

.PHONY: setup
setup: setup-dirs install ## Full project setup
	@echo "  ✓ Project setup complete!"

.PHONY: setup-dirs
setup-dirs: ## Create all required directories
	@mkdir -p series/ML series/DL series/common/intro series/common/outro
	@mkdir -p exports assets/audio/sfx assets/audio/music
	@mkdir -p assets/images/thumbnails assets/images/overlays assets/logos
	@mkdir -p tools output
	@echo "  ✓ Directories created."

# ─── Cleanup ────────────────────────────────────────────────────────────────

.PHONY: clean
clean: ## Remove rendered output & caches
	rm -rf output/ media/ __pycache__/ .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "  ✓ Cleaned output and caches."

.PHONY: clean-exports
clean-exports: ## Remove exported files
	rm -rf exports/*/
	@echo "  ✓ Cleaned exports."

.PHONY: clean-all
clean-all: clean clean-exports ## Remove everything (output + exports)
	@echo "  ✓ Full clean complete."

# ─── Status / Info ──────────────────────────────────────────────────────────

.PHONY: status
status: ## Show project status overview
	@echo ""
	@echo "  ╔══════════════════════════════════════════════════════╗"
	@echo "  ║            TheBoringAI — Project Status             ║"
	@echo "  ╚══════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  ML Episodes:"
	@for dir in series/ML/*/; do \
		if [ -f "$$dir/config.yaml" ]; then \
			title=$$(grep "title:" "$$dir/config.yaml" | head -1 | sed 's/.*: *"\(.*\)"/\1/'); \
			status=$$(grep "status:" "$$dir/config.yaml" | head -1 | sed 's/.*: *"\(.*\)"/\1/'); \
			echo "    [$$(basename $$dir)]  $$title ($$status)"; \
		fi; \
	done
	@echo ""
	@echo "  DL Episodes:"
	@for dir in series/DL/*/; do \
		if [ -f "$$dir/config.yaml" ]; then \
			title=$$(grep "title:" "$$dir/config.yaml" | head -1 | sed 's/.*: *"\(.*\)"/\1/'); \
			status=$$(grep "status:" "$$dir/config.yaml" | head -1 | sed 's/.*: *"\(.*\)"/\1/'); \
			echo "    [$$(basename $$dir)]  $$title ($$status)"; \
		fi; \
	done
	@echo ""
	@echo "  Exports:"
	@for profile in youtube_1080p youtube_4k shorts facebook instagram twitter transparent gif_preview; do \
		count=$$(find exports/$$profile -type f 2>/dev/null | wc -l); \
		echo "    $$profile: $$count files"; \
	done
	@echo ""

# ─── Internal ───────────────────────────────────────────────────────────────

.PHONY: _check-scene
_check-scene:
ifndef S
	$(error S is not set. Usage: make <target> S=path/to/scene.py C=ClassName)
endif
ifndef C
	$(error C is not set. Usage: make <target> S=path/to/scene.py C=ClassName)
endif
