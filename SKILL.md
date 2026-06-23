---
name: cover-design
description: Generate professional tutorial/video covers in Seeed Studio brand style. Use when the user needs to create cover images for tutorials, product guides, assembly instructions, or video thumbnails. Features glassmorphism card overlay, branded logo placement, configurable title/subtitle/model text, and automatic card sizing to fit content. Supports custom background images and brand logos.
---

# Cover Design

Generate branded cover images with glassmorphism card overlay.

## Default Cover Layout (Default Cover Template)

```
          [seeed studio logo]  ← Logo at top-left, near card corner with gap
    +-----------------------------+
    |  Model-Name (green)         |
    |      Main Title (white)     |  ← Card centered, text centered
    |      Subtitle (gray)        |
    +-----------------------------+
                                     
    seeed studio  ← Bottom-left (fixed)
```

**Default behavior (no extra flags needed):**
- Card centered horizontally
- All text centered in card
- Logo at card top-left corner with gap (avoids overlapping border)
- Brand text at bottom-left

## Quick Start

```bash
python scripts/generate_cover.py \
  --background <bg_image.jpg> \
  --title "Main Title" \
  --subtitle "Subtitle text" \
  --model "Model-Name" \
  --logo assets/logo.png \
  --output cover.jpg
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--background` / `-b` | Yes | — | Background image path |
| `--title` / `-t` | Yes | — | Main title (large white text) |
| `--subtitle` / `-s` | No | `""` | Subtitle (gray text below title) |
| `--model` / `-m` | No | `""` | Model name (green label above title) |
| `--logo` / `-l` | No | `None` | Brand logo image path |
| `--output` / `-o` | No | `cover_output.jpg` | Output file path |
| `--blur` | No | `2` | Background blur radius |
| `--brightness` | No | `0.75` | Background brightness (0-1) |
| `--text-align` | No | `center` | Text alignment in card: `center` or `left` |
| `--logo-position` | No | `auto` | Logo position: `auto`(default), `topleft`, `center` |

### Programmatic Usage

```python
from scripts.generate_cover import generate_cover

generate_cover(
    background_image="photo.jpg",
    title="reBot-Arm-B601-DM电源组装",
    subtitle="详细步骤图解 · 从零开始组装",
    model_name="reBot-Arm-B601",
    brand_logo="assets/logo.png",
    output_path="cover.jpg",
)
```

## Design Spec

- **Background**: Gaussian blur (radius 2) + brightness 0.75 + dark overlay (alpha 60)
- **Card**: Dark semi-transparent rounded rectangle, auto-sized to fit title width, centered
- **Logo (auto mode)**: Positioned near card top-left with 20px gap, avoids overlapping card border
- **Text**: Centered in card by default
- **Colors**: Green `#8BC34A` for model/brand, white `#FFFFFF` for title, light gray `#E6E6E6` for subtitle
- **Sizing**: Proportional to image width (4K reference base), all elements scale automatically
- **Bottom bar**: Semi-transparent black strip, brand text fixed at bottom-left

## Assets

- `assets/logo.png` — Default brand logo (seeed studio)
- `assets/preview.jpg` — Sample output preview

Replace `assets/logo.png` with a custom logo when working with different brands.
