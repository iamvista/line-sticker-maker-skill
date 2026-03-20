---
name: line-sticker-maker
description: |
  Design and produce LINE sticker sets (static). Handles the full pipeline: theme planning,
  character design, AI image generation, quality review, and post-processing to LINE's exact
  format specs. Use this skill when the user mentions LINE stickers, LINE 貼圖, sticker design,
  貼圖製作, or wants to create a set of chat stickers. Also trigger when the user references
  LINE Creators Market, sticker submission, or asks to make cute/chibi character sticker packs.
---

# LINE Sticker Maker

A complete pipeline for designing and producing LINE sticker sets, from concept to submission-ready files.

## LINE Creators Market Format Specs

These are non-negotiable — LINE will reject submissions that don't match:

| Asset | Size (px) | Format | Count |
|-------|-----------|--------|-------|
| Main image | 240 x 240 | PNG, transparent bg | 1 |
| Sticker body | 370 x 320 | PNG, transparent bg | 8, 16, 24, 32, or 40 |
| Chat tab icon | 96 x 74 | PNG, transparent bg | 1 |

Additional rules:
- All images must have transparent backgrounds (RGBA PNG)
- Max file size: 1MB per sticker
- Keep a 10px margin around content (nothing touching the edges)
- Colour mode: RGB (no CMYK)

## Pipeline Overview

```
1. Theme & Planning ──► 2. Character Design ──► 3. Batch Generation ──► 4. Quality Review ──► 5. Post-Processing ──► 6. Final Check
```

Follow each phase in order. Do not skip the Quality Review — it catches problems that are expensive to fix later.

---

## Phase 1: Theme & Planning

Start by defining the sticker set's identity:

1. **Character concept**: Who is the character? What makes them recognizable? (e.g., "Q版小兵 in camouflage with round face and big eyes")
2. **Visual style**: Chibi/kawaii, flat illustration, thick outlines, cartoon — pick one and stick with it
3. **Text language**: Traditional Chinese, Simplified Chinese, English, Japanese, or none
4. **Expression/situation list**: Plan ALL stickers before generating any. Each sticker needs:
   - Text (the chat phrase)
   - Emotion/action (what the character is doing)
   - Use case (when someone would send this sticker)

Create a planning table like this:

| # | Text | Action | Emotion | Use Case |
|---|------|--------|---------|----------|
| 01 | 收到！ | Saluting | Proud | Confirming a message |
| 02 | 累死了… | Lying on ground | Exhausted | After a long day |

**Balancing the set**: A good sticker set covers these categories:
- Greetings (早安、晚安、你好)
- Affirmatives (OK、收到、讚)
- Emotions (開心、難過、生氣、害怕)
- Actions (加油、衝啊、快逃)
- Reactions (不要啊、謝謝、抱歉)

Present the full table to the user for approval before generating anything.

---

## Phase 2: Character Design — The Style Anchor

Consistency is the #1 challenge in AI-generated sticker sets. To fight style drift across images, build a **style anchor prompt** — a base prompt that every sticker shares.

### Building the Style Anchor

Structure it with these required elements:

```
[Art style] + [Character description] + [Outfit details] + [Cultural markers] + [Composition rules] + [Technical specs]
```

Example:
```
Cute chibi kawaii style LINE sticker, exactly ONE single character centered in the image,
a round-faced boy with big expressive eyes and rosy cheeks,
wearing green camouflage military uniform and helmet with Taiwan ROC flag patch,
thick black outline, cartoon style, high contrast colors,
simple clean white background, sticker design, flat illustration, no shadow
```

### Critical Rules for the Style Anchor

These come from hard-won experience generating sticker sets:

1. **"exactly ONE single character centered in the image"** — Without this, the AI frequently generates 2 characters side by side. This is the single most common failure mode. Include it in EVERY prompt.

2. **"centered in the image" / "centered layout"** — Without explicit centering instructions, characters drift to one side, leaving empty space.

3. **Cultural/political symbols** — Be extremely explicit about what symbols to use and what to avoid. For Taiwanese themes, explicitly say "Taiwan ROC flag" AND "no red star, no communist symbols." The AI defaults to generic military imagery which can produce politically sensitive content.

4. **"white background"** — Generates cleanest results for background removal. Colored or gradient backgrounds make post-processing harder.

5. **Font consistency** — This is a known weakness of AI image generation. The AI will use different fonts across stickers unless constrained. Mitigations:
   - Specify the exact font style in the prompt: "bold sans-serif Traditional Chinese text" or "rounded bold Chinese characters"
   - Better approach: generate images WITHOUT text, then add text programmatically in post-processing using a consistent font (see Phase 5)

### Per-Sticker Prompt Template

For each sticker, append the unique elements to the style anchor:

```
{style_anchor}, [specific expression], [specific action/pose], [specific props if any].
Bold Traditional Chinese text '[貼圖文字]' centered at the bottom.
```

---

## Phase 3: Batch Generation

### Model Selection

Use `generate-image` skill with these model recommendations:
- **Google Gemini 3 Pro** (`google/gemini-3-pro-image-preview`): Best for cute/chibi styles, handles Chinese text well, good character consistency. Recommended default.
- **FLUX.2 Pro** (`black-forest-labs/flux.2-pro`): Alternative if Gemini produces unwanted artifacts.

### Generation Strategy

1. **Generate in batches of 4** — parallel generation is faster, and if a batch has issues, you only redo 4 instead of 16.
2. **Review each batch immediately** — show the user before moving to the next batch. Catching problems early saves time.
3. **Save originals at full resolution** — post-processing will handle resizing. Name files consistently: `sticker_01_keyword.png`, `sticker_02_keyword.png`, etc.

### Output Directory Structure

```
project-name/
├── sticker_01_roger.png      # Original full-res images
├── sticker_02_awesome.png
├── ...
├── process_stickers.py       # Post-processing script
└── line_format/              # Final submission-ready files
    ├── main.png              # 240x240
    ├── tab.png               # 96x74
    ├── 01.png                # 370x320
    ├── 02.png
    └── ...
```

---

## Phase 4: Quality Review Checklist

After generating all stickers, review EVERY image against this checklist. These are ranked by how often they occur:

### Must-Fix (will get rejected or cause controversy)

- [ ] **Duplicate characters**: Does any sticker show 2 characters instead of 1? (Very common with AI generation)
- [ ] **Political/cultural symbols**: Any unintended flags, stars, or symbols? Check helmets, patches, badges closely
- [ ] **Text accuracy**: Is the Chinese text correct? No wrong characters, no simplified when traditional is intended?
- [ ] **Offensive content**: Anything that could be misinterpreted?

### Should-Fix (quality issues)

- [ ] **Centering**: Is the character centered? Any sticker where the character is pushed to one side?
- [ ] **Size consistency**: Compare all stickers side by side. Is one character noticeably larger or smaller than others? The character should occupy roughly the same proportion of the frame across all stickers.
- [ ] **Font consistency**: Are the text styles uniform across all stickers? (Size, weight, font family)
- [ ] **Style consistency**: Does any sticker look like it belongs to a different set? (Different outline weight, different color palette, different proportions)

### Nice-to-Fix (polish)

- [ ] **Expression clarity**: At 96px (chat preview size), can you tell what the emotion is?
- [ ] **Text readability**: At small size, can you read the text?
- [ ] **Color vibrancy**: Any sticker that looks washed out compared to others?

### Fixing Common Issues

**Duplicate characters**: Regenerate with stronger emphasis — add "absolutely only one character, single figure, solo" to the prompt.

**Off-center composition**: Add "centered layout, square composition, character in the exact center of the image" to the prompt.

**Inconsistent size**: This often happens when one source image is square (fills the frame) while others are landscape (more whitespace). Fix in post-processing by adjusting the padding parameter per-sticker — increase padding for stickers where the character is too large.

**Inconsistent fonts**: The most reliable fix is to generate images WITHOUT text and add text programmatically. See the `scripts/add_text.py` bundled script.

---

## Phase 5: Post-Processing

Use the bundled `scripts/process_stickers.py` to convert all images to LINE-ready format. The script handles:

1. **Background removal** — converts white/near-white pixels to transparent
2. **Resizing** — fits each sticker to 370x320px with proper margins
3. **Main image** — creates 240x240px version from the first sticker
4. **Tab icon** — creates 96x74px version from the first sticker

Run it:
```bash
python3 scripts/process_stickers.py --input-dir /path/to/originals --output-dir /path/to/line_format
```

### Per-Sticker Size Adjustment

If a specific sticker's character is too large or small compared to others, override its padding:

```bash
python3 scripts/process_stickers.py --input-dir /path/to/originals --output-dir /path/to/line_format --padding-override "04:55,08:45"
```

This sets sticker 04 to 55px padding and sticker 08 to 45px padding (default is 10px). Higher padding = smaller character.

### Adding Text Programmatically (Optional)

If font consistency is a problem, generate stickers WITHOUT text, then use:

```bash
python3 scripts/add_text.py --input-dir /path/to/line_format --font /path/to/font.ttf --texts "01:收到！,02:讚啦！,03:累死了…"
```

Good free fonts for LINE stickers:
- **Noto Sans TC Bold** — clean, modern, widely available
- **jf open 粗圓體** — rounded, cute, good for kawaii style
- **源泉圓體** — friendly, rounded

---

## Phase 6: Final Verification

Before declaring the set complete:

1. **Verify all file dimensions**:
```bash
python3 -c "
from PIL import Image
import os
for f in sorted(os.listdir('line_format')):
    if f.endswith('.png'):
        img = Image.open(f'line_format/{f}')
        print(f'{f:20s} {img.size[0]}x{img.size[1]}  mode={img.mode}')
"
```

2. **Check file sizes** — all must be under 1MB:
```bash
ls -lh line_format/*.png
```

3. **Visual spot check** — open 3-4 random stickers at the small preview size (96px height) and confirm they're still readable and expressive.

4. **Present summary table** to the user showing all 16+ stickers with their text and status.

---

## Appendix: Common Prompt Pitfalls

| Problem | Bad Prompt | Good Prompt |
|---------|-----------|-------------|
| Two characters | "a soldier giving thumbs up" | "exactly ONE single character, a soldier giving thumbs up, solo figure" |
| Wrong symbols | "military soldier with helmet" | "military soldier with helmet with Taiwan ROC flag patch, no red star" |
| Off-center | "soldier pumping fist" | "soldier pumping fist, centered in image, centered layout, square composition" |
| Text issues | "'加油！' at the bottom" | "bold sans-serif Traditional Chinese text '加油！' centered at the bottom in black" |
| Style drift | (varying descriptions) | (use a fixed style anchor prepended to every prompt) |
