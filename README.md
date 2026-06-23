# Cover Design Skill

Generate professional tutorial/video covers in **Seeed Studio** brand style with glassmorphism card overlay.

## Preview

![Preview](assets/preview.jpg)

## Features

- **Glassmorphism card overlay** — Auto-sized to fit your title
- **Brand logo support** — Top-left logo placement
- **Configurable text layers** — Model name (green), title (white), subtitle (gray)
- **Background processing** — Blur + brightness + dark overlay for readability
- **Responsive sizing** — All elements scale proportionally to image width
- **CLI & Python API** — Use from command line or import as module

## Quick Start

### Command Line

```bash
python scripts/generate_cover.py \
  --background photo.jpg \
  --title "reBot-Arm-B601-RS电源组装" \
  --subtitle "详细步骤图解 · 从零开始组装" \
  --model "reBot-Arm-B601" \
  --logo assets/logo.png \
  --output cover.jpg
```

### Python API

```python
from scripts.generate_cover import generate_cover

generate_cover(
    background_image="photo.jpg",
    title="Your Title",
    subtitle="Your subtitle",
    model_name="Model-Name",
    brand_logo="assets/logo.png",
    output_path="cover.jpg",
)
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--background` / `-b` | Yes | — | Background image path |
| `--title` / `-t` | Yes | — | Main title text |
| `--subtitle` / `-s` | No | `""` | Subtitle text |
| `--model` / `-m` | No | `""` | Model name (green label) |
| `--logo` / `-l` | No | `None` | Brand logo path |
| `--output` / `-o` | No | `cover_output.jpg` | Output file path |
| `--blur` | No | `2` | Background blur radius |
| `--brightness` | No | `0.75` | Background brightness (0-1) |

## File Structure

```
cover-design/
├── SKILL.md              # Skill metadata and instructions
├── README.md             # This file
├── scripts/
│   └── generate_cover.py # Main cover generator script
└── assets/
    ├── logo.png          # Default brand logo (seeed studio)
    └── preview.jpg       # Sample output preview
```

## Customization

Replace `assets/logo.png` with your own brand logo (PNG with transparency recommended).

## Requirements

- Python 3.7+
- Pillow (`pip install pillow`)
- Noto Sans CJK font (for Chinese text support)

## License

MIT
