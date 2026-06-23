# Cover Design Skill / 封面设计 Skill

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

Generate professional tutorial/video covers in **Seeed Studio** brand style with glassmorphism card overlay.

### Preview

![Preview](assets/preview.jpg)

### Features

- **Glassmorphism card overlay** — Auto-sized to fit your title
- **Brand logo support** — Top-left logo placement
- **Configurable text layers** — Model name (green), title (white), subtitle (gray)
- **Background processing** — Blur + brightness + dark overlay for readability
- **Responsive sizing** — All elements scale proportionally to image width
- **CLI & Python API** — Use from command line or import as module

### Quick Start

#### Command Line

```bash
python scripts/generate_cover.py \
  --background photo.jpg \
  --title "Your Title Here" \
  --subtitle "Subtitle text" \
  --model "Model-Name" \
  --logo assets/logo.png \
  --output cover.jpg
```

#### Python API

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

### Parameters

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

### File Structure

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

### Customization

Replace `assets/logo.png` with your own brand logo (PNG with transparency recommended).

### Requirements

- Python 3.7+
- Pillow (`pip install pillow`)
- Noto Sans CJK font (for Chinese text support)

---

<a name="chinese"></a>
## 中文

使用 **Seeed Studio** 品牌风格的毛玻璃卡片叠加效果，生成专业的教程/视频封面。

### 预览

![Preview](assets/preview.jpg)

### 功能特点

- **毛玻璃卡片叠加** — 根据标题自动调整大小
- **品牌 Logo 支持** — 左上角 Logo 放置
- **可配置文字层级** — 型号名（绿色）、主标题（白色）、副标题（灰色）
- **背景处理** — 模糊 + 亮度 + 暗色叠加，确保文字清晰可读
- **响应式尺寸** — 所有元素按比例缩放，适配不同分辨率
- **CLI 和 Python API** — 支持命令行调用和模块导入

### 快速开始

#### 命令行

```bash
python scripts/generate_cover.py \
  --background photo.jpg \
  --title "reBot-Arm-B601-RS电源组装" \
  --subtitle "详细步骤图解 · 从零开始组装" \
  --model "reBot-Arm-B601" \
  --logo assets/logo.png \
  --output cover.jpg
```

#### Python API

```python
from scripts.generate_cover import generate_cover

generate_cover(
    background_image="photo.jpg",
    title="你的标题",
    subtitle="副标题文字",
    model_name="型号名称",
    brand_logo="assets/logo.png",
    output_path="cover.jpg",
)
```

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|-----------|----------|---------|-------------|
| `--background` / `-b` | 是 | — | 背景图片路径 |
| `--title` / `-t` | 是 | — | 主标题文字 |
| `--subtitle` / `-s` | 否 | `""` | 副标题文字 |
| `--model` / `-m` | 否 | `""` | 型号名称（绿色标签） |
| `--logo` / `-l` | 否 | `None` | 品牌 Logo 路径 |
| `--output` / `-o` | 否 | `cover_output.jpg` | 输出文件路径 |
| `--blur` | 否 | `2` | 背景模糊半径 |
| `--brightness` | 否 | `0.75` | 背景亮度 (0-1) |

### 文件结构

```
cover-design/
├── SKILL.md              # Skill 元数据和指令
├── README.md             # 本文件
├── scripts/
│   └── generate_cover.py # 封面生成主脚本
└── assets/
    ├── logo.png          # 默认品牌 Logo (seeed studio)
    └── preview.jpg       # 示例输出预览
```

### 自定义

将 `assets/logo.png` 替换为你自己的品牌 Logo（推荐使用带透明通道的 PNG）。

### 环境要求

- Python 3.7+
- Pillow (`pip install pillow`)
- Noto Sans CJK 字体（用于中文显示）

## License / 许可证

MIT
