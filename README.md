# LINE Sticker Maker — Claude Code Skill

> 用 AI 設計 LINE 貼圖的完整流程，從概念到上架。
> A Claude Code skill for designing LINE sticker sets with AI — from concept to submission-ready files.

<p align="center">
  <img src="docs/pipeline-overview.svg" alt="Pipeline Overview" width="700">
</p>

## What is this?

This is a **[Claude Code](https://claude.ai/claude-code) skill** — a structured set of instructions and scripts that guides Claude through the complete LINE sticker creation pipeline:

1. **Theme & Planning** — Character concept, expression list, set composition
2. **Character Design** — Style anchor prompt for visual consistency
3. **Batch Generation** — AI image generation with quality controls
4. **Quality Review** — Systematic checklist to catch common AI generation issues
5. **Post-Processing** — Automated background removal, resizing, and formatting
6. **Final Verification** — Format compliance and submission readiness

## Why a Skill?

AI image generation is powerful but unpredictable. Without guardrails, you'll hit these problems:

| Problem | Frequency | Impact |
|---------|-----------|--------|
| Duplicate characters in one image | Very common | Must regenerate |
| Inconsistent fonts across stickers | Always | Looks unprofessional |
| Characters not centered | Common | Bad cropping in chat |
| Wrong cultural/political symbols | Occasional | Controversy risk |
| Inconsistent character sizing | Common | Set looks sloppy |

This skill encodes **hard-won lessons** into reusable instructions, so you don't have to learn them the hard way.

## Quick Start

### 1. Install the Skill

Copy the skill to your Claude Code skills directory:

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/line-sticker-maker

# Copy files
cp SKILL.md ~/.claude/skills/line-sticker-maker/
cp -r scripts/ ~/.claude/skills/line-sticker-maker/scripts/
```

### 2. Install Dependencies

The post-processing script requires Pillow:

```bash
pip install Pillow
```

### 3. Use It

In Claude Code, just ask:

```
幫我設計一組 16 張的 LINE 貼圖，主題是 [你的主題]
```

or

```
Design a set of 16 LINE stickers featuring [your character concept]
```

Claude will automatically invoke the skill and guide you through the full pipeline.

## Project Structure

```
line-sticker-maker-skill/
├── SKILL.md                          # Main skill file (Claude Code reads this)
├── scripts/
│   └── process_stickers.py           # Post-processing: bg removal, resize, format
├── docs/
│   └── pipeline-overview.svg         # Visual pipeline diagram
├── examples/
│   └── sample-planning-table.md      # Example sticker planning table
├── LICENSE
└── README.md
```

## The Post-Processing Script

`scripts/process_stickers.py` converts raw AI-generated images to LINE-ready format:

```bash
# Basic usage
python3 scripts/process_stickers.py \
  --input-dir ./my-stickers \
  --output-dir ./line_format

# With per-sticker padding adjustments
python3 scripts/process_stickers.py \
  --input-dir ./my-stickers \
  --output-dir ./line_format \
  --padding-override "04:55,08:45"
```

### What it does:

- **Removes white backgrounds** → transparent PNG
- **Resizes to 370×320px** with centered character and safe margins
- **Generates main.png** (240×240) and **tab.png** (96×74)
- **Verifies** all file sizes are under 1MB

### Options:

| Flag | Default | Description |
|------|---------|-------------|
| `--input-dir` | (required) | Directory containing `sticker_*.png` files |
| `--output-dir` | (required) | Output directory for LINE-format files |
| `--default-padding` | `10` | Default padding in pixels |
| `--bg-threshold` | `240` | White background detection threshold (0-255) |
| `--padding-override` | `""` | Per-sticker padding, e.g. `"04:55,08:45"` |
| `--main-source` | `1` | Which sticker to use for main/tab images |

## Key Concept: Style Anchor

The **Style Anchor** is a fixed prompt prefix shared across all stickers to maintain visual consistency:

```
[Art style] + [Character description] + [Outfit details] + [Cultural markers] + [Composition rules] + [Technical specs]
```

Example:
```
Cute chibi kawaii style LINE sticker, exactly ONE single character
centered in the image, a round-faced boy with big expressive eyes
and rosy cheeks, thick black outline, cartoon style, high contrast
colors, simple clean white background, flat illustration, no shadow
```

Each sticker only varies the expression, pose, and text — everything else stays identical.

## LINE Creators Market Specs

| Asset | Size (px) | Format | Count |
|-------|-----------|--------|-------|
| Main image | 240 × 240 | PNG, transparent bg | 1 |
| Sticker body | 370 × 320 | PNG, transparent bg | 8 / 16 / 24 / 32 / 40 |
| Tab icon | 96 × 74 | PNG, transparent bg | 1 |

- All images: RGBA PNG, RGB color mode
- Max file size: 1MB per image
- Content must have ≥ 10px margin from edges

## Contributing

Found a new AI generation pitfall? Have a better prompt strategy? PRs welcome!

Areas where contributions would be especially valuable:
- **Animated sticker support** (APNG format)
- **Text overlay script** (`scripts/add_text.py`) for programmatic text addition
- **Additional style anchor templates** for different character types
- **Prompt strategies** for other AI image models

## License

MIT License — see [LICENSE](LICENSE) for details.

## Credits

Created by [Vista](https://www.vista.tw) — built from real experience designing LINE sticker sets with AI.
