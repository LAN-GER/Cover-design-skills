#!/usr/bin/env python3
"""
Seeed Studio style cover generator.
Generates professional tutorial/video covers with branded glassmorphism card overlay.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import argparse
import os


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """Draw a rounded rectangle on PIL ImageDraw."""
    x1, y1, x2, y2 = xy
    r = radius
    draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill)
    draw.rectangle([x1, y1 + r, x2, y2 - r], fill=fill)
    draw.pieslice([x1, y1, x1 + 2 * r, y1 + 2 * r], 180, 270, fill=fill)
    draw.pieslice([x2 - 2 * r, y1, x2, y1 + 2 * r], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2 * r, x1 + 2 * r, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2 * r, y2 - 2 * r, x2, y2], 0, 90, fill=fill)

    if outline:
        draw.arc([x1, y1, x1 + 2 * r, y1 + 2 * r], 180, 270, fill=outline, width=width)
        draw.arc([x2 - 2 * r, y1, x2, y1 + 2 * r], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - 2 * r, x1 + 2 * r, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - 2 * r, y2 - 2 * r, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([(x1 + r, y1), (x2 - r, y1)], fill=outline, width=width)
        draw.line([(x1 + r, y2), (x2 - r, y2)], fill=outline, width=width)
        draw.line([(x1, y1 + r), (x1, y2 - r)], fill=outline, width=width)
        draw.line([(x2, y1 + r), (x2, y2 - r)], fill=outline, width=width)


def generate_cover(
    background_image,
    title,
    subtitle="",
    model_name="",
    brand_logo=None,
    output_path="cover_output.jpg",
    blur_radius=2,
    brightness=0.75,
    overlay_alpha=60,
    card_alpha=90,
):
    """
    Generate a Seeed Studio style cover image.

    Args:
        background_image: Path to the background image
        title: Main title text (large, white)
        subtitle: Subtitle text (gray, optional)
        model_name: Model name text (green label, optional)
        brand_logo: Path to brand logo image (optional)
        output_path: Output file path
        blur_radius: Gaussian blur radius for background (default: 2)
        brightness: Background brightness multiplier (default: 0.75)
        overlay_alpha: Dark overlay alpha (0-255, default: 60)
        card_alpha: Card background alpha (0-255, default: 90)
    """
    # Load background
    bg_img = Image.open(background_image)
    w, h = bg_img.size

    # Apply blur and brightness adjustment
    bg = bg_img.copy()
    bg = bg.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    enhancer = ImageEnhance.Brightness(bg)
    bg = enhancer.enhance(brightness)

    # Apply dark overlay
    dark_overlay = Image.new("RGBA", (w, h), (0, 0, 0, overlay_alpha))
    bg_rgba = bg.convert("RGBA")
    bg = Image.alpha_composite(bg_rgba, dark_overlay)

    # Load fonts
    font_bold = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    font_regular = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

    if not os.path.exists(font_bold):
        # Fallback font search
        import subprocess
        result = subprocess.run(
            ["fc-match", "-v", "Noto Sans CJK SC:weight=bold"],
            capture_output=True, text=True,
        )
        for line in result.stdout.split("\n"):
            if "file:" in line:
                font_bold = line.split('"')[1]
                break

    # --- Sizing calculations ---
    # Use relative sizing based on image width
    base_unit = w / 3840  # Normalize to 4K reference

    logo_h = int(75 * base_unit)
    model_font_size = int(72 * base_unit)
    title_font_size = int(160 * base_unit)
    subtitle_font_size = int(60 * base_unit)
    bottom_font_size = int(42 * base_unit)

    # Create font objects
    model_font = ImageFont.truetype(font_bold, model_font_size)
    title_font = ImageFont.truetype(font_bold, title_font_size)
    subtitle_font = ImageFont.truetype(font_regular, subtitle_font_size)
    info_font = ImageFont.truetype(font_regular, bottom_font_size)

    # Measure title width to size the card
    temp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    title_bbox = temp_draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]

    # Card dimensions with padding
    card_x = int(120 * base_unit)
    text_padding = int(120 * base_unit)
    card_w = title_w + text_padding * 2
    card_h = int(880 * base_unit)
    card_y = int(240 * base_unit)
    card_radius = int(35 * base_unit)

    # Ensure card doesn't exceed image width
    if card_x + card_w > w - 40:
        card_w = w - card_x - 40

    # --- Draw glassmorphism card ---
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card)
    card_color = (30, 35, 45, card_alpha)
    card_border_color = (255, 255, 255, 60)

    draw_rounded_rect(
        card_draw,
        [card_x, card_y, card_x + card_w, card_y + card_h],
        card_radius,
        card_color,
        card_border_color,
        2,
    )

    bg = Image.alpha_composite(bg, card)
    cover = bg.convert("RGB")

    # --- Paste logo ---
    cover_rgba = cover.convert("RGBA")
    if brand_logo and os.path.exists(brand_logo):
        logo_img = Image.open(brand_logo)
        lw, lh = logo_img.size
        new_lw = int(lw * logo_h / lh)
        logo_resized = logo_img.resize((new_lw, logo_h), Image.LANCZOS)
        if logo_resized.mode != "RGBA":
            logo_resized = logo_resized.convert("RGBA")
        cover_rgba.paste(logo_resized, (int(50 * base_unit), int(30 * base_unit)), logo_resized)

    # --- Draw text ---
    cover_final = cover_rgba.convert("RGB")
    draw = ImageDraw.Draw(cover_final)

    text_x = card_x + text_padding
    text_y = card_y + int(120 * base_unit)

    # Model name (green)
    if model_name:
        draw.text((text_x, text_y), model_name, font=model_font, fill=(139, 195, 74))
        text_y += int(135 * base_unit)

    # Title (white)
    draw.text((text_x, text_y), title, font=title_font, fill=(255, 255, 255))
    text_y += int(225 * base_unit)

    # Subtitle (light gray)
    if subtitle:
        draw.text((text_x, text_y), subtitle, font=subtitle_font, fill=(230, 230, 230))

    # --- Bottom info bar ---
    bottom_bar_h = int(110 * base_unit)
    bottom_bar = Image.new("RGBA", (w, bottom_bar_h), (0, 0, 0, 100))
    cover_final_rgba = cover_final.convert("RGBA")
    cover_final_rgba.paste(bottom_bar, (0, h - bottom_bar_h), bottom_bar)

    cover_final = cover_final_rgba.convert("RGB")
    draw = ImageDraw.Draw(cover_final)

    # Bottom brand text
    if brand_logo:
        draw.text(
            (int(55 * base_unit), h - bottom_bar_h + int(30 * base_unit)),
            "seeed studio",
            font=info_font,
            fill=(139, 195, 74),
        )

    # Save output
    cover_final.save(output_path, quality=98)
    print(f"Cover saved to: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate Seeed Studio style cover image")
    parser.add_argument("--background", "-b", required=True, help="Background image path")
    parser.add_argument("--title", "-t", required=True, help="Main title text")
    parser.add_argument("--subtitle", "-s", default="", help="Subtitle text")
    parser.add_argument("--model", "-m", default="", help="Model name (green label)")
    parser.add_argument("--logo", "-l", default=None, help="Brand logo image path")
    parser.add_argument("--output", "-o", default="cover_output.jpg", help="Output file path")
    parser.add_argument("--blur", type=int, default=2, help="Background blur radius")
    parser.add_argument("--brightness", type=float, default=0.75, help="Background brightness")

    args = parser.parse_args()

    generate_cover(
        background_image=args.background,
        title=args.title,
        subtitle=args.subtitle,
        model_name=args.model,
        brand_logo=args.logo,
        output_path=args.output,
        blur_radius=args.blur,
        brightness=args.brightness,
    )


if __name__ == "__main__":
    main()
