#!/usr/bin/env python3
"""
Seeed Studio 风格封面生成器
============================
生成带有毛玻璃卡片叠加效果的专业教程/视频封面。
支持品牌 Logo 放置、可配置的标题/副标题/型号文字、自动卡片尺寸调整。

Usage:
    python generate_cover.py -b photo.jpg -t "标题" -s "副标题" -m "型号" -l logo.png -o cover.jpg
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import argparse
import os


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """
    绘制圆角矩形
    
    Args:
        draw: PIL ImageDraw 对象
        xy: (x1, y1, x2, y2) 矩形坐标
        radius: 圆角半径
        fill: 填充颜色 (RGBA 元组)
        outline: 边框颜色 (可选)
        width: 边框宽度
    """
    x1, y1, x2, y2 = xy
    r = radius
    # 主体矩形（去掉四个角）
    draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill)
    draw.rectangle([x1, y1 + r, x2, y2 - r], fill=fill)
    # 四个圆角扇形
    draw.pieslice([x1, y1, x1 + 2 * r, y1 + 2 * r], 180, 270, fill=fill)           # 左上
    draw.pieslice([x2 - 2 * r, y1, x2, y1 + 2 * r], 270, 360, fill=fill)           # 右上
    draw.pieslice([x1, y2 - 2 * r, x1 + 2 * r, y2], 90, 180, fill=fill)             # 左下
    draw.pieslice([x2 - 2 * r, y2 - 2 * r, x2, y2], 0, 90, fill=fill)               # 右下

    if outline:
        # 绘制边框弧线
        draw.arc([x1, y1, x1 + 2 * r, y1 + 2 * r], 180, 270, fill=outline, width=width)
        draw.arc([x2 - 2 * r, y1, x2, y1 + 2 * r], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - 2 * r, x1 + 2 * r, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - 2 * r, y2 - 2 * r, x2, y2], 0, 90, fill=outline, width=width)
        # 绘制边框直线
        draw.line([(x1 + r, y1), (x2 - r, y1)], fill=outline, width=width)          # 上边
        draw.line([(x1 + r, y2), (x2 - r, y2)], fill=outline, width=width)          # 下边
        draw.line([(x1, y1 + r), (x1, y2 - r)], fill=outline, width=width)          # 左边
        draw.line([(x2, y1 + r), (x2, y2 - r)], fill=outline, width=width)          # 右边


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
    text_align="center",        # 文字对齐方式: "center" 居中, "left" 左对齐
    logo_position="auto",       # Logo 位置: "auto" 卡片左上, "topleft" 固定左上, "center" 顶部居中
):
    """
    生成 Seeed Studio 风格封面图片

    Args:
        background_image: 背景图片路径
        title: 主标题文字（大号白色）
        subtitle: 副标题文字（灰色，可选）
        model_name: 型号名称（绿色标签，可选）
        brand_logo: 品牌 Logo 图片路径（可选）
        output_path: 输出文件路径
        blur_radius: 背景高斯模糊半径（默认 2）
        brightness: 背景亮度乘数（默认 0.75）
        overlay_alpha: 暗色叠加层不透明度（默认 60）
        card_alpha: 卡片背景不透明度（默认 90）
        text_align: 文字对齐方式 "center" 或 "left"
        logo_position: Logo 位置 "auto", "topleft" 或 "center"
    """
    # ===== 1. 加载并处理背景图片 =====
    bg_img = Image.open(background_image)
    w, h = bg_img.size
    # 以 3840px 为基准计算缩放比例，所有元素按比例自适应
    base_unit = w / 3840

    # 轻微模糊处理，让背景不分散注意力
    bg = bg_img.copy()
    bg = bg.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    # 降低亮度，让前景文字更突出
    enhancer = ImageEnhance.Brightness(bg)
    bg = enhancer.enhance(brightness)
    # 叠加半透明黑色蒙版，增强对比度
    dark_overlay = Image.new("RGBA", (w, h), (0, 0, 0, overlay_alpha))
    bg_rgba = bg.convert("RGBA")
    bg = Image.alpha_composite(bg_rgba, dark_overlay)

    # ===== 2. 加载字体 =====
    font_bold = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    font_regular = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

    # 字体不存在时自动查找备选
    if not os.path.exists(font_bold):
        import subprocess
        result = subprocess.run(
            ["fc-match", "-v", "Noto Sans CJK SC:weight=bold"],
            capture_output=True, text=True,
        )
        for line in result.stdout.split("\n"):
            if "file:" in line:
                font_bold = line.split('"')[1]
                break

    # ===== 3. 计算元素尺寸 =====
    logo_h = int(75 * base_unit)                        # Logo 高度
    model_font_size = int(72 * base_unit)               # 型号文字字号
    title_font_size = int(160 * base_unit)              # 主标题字号
    subtitle_font_size = int(60 * base_unit)            # 副标题字号
    bottom_font_size = int(42 * base_unit)              # 底部信息条字号

    model_font = ImageFont.truetype(font_bold, model_font_size)
    title_font = ImageFont.truetype(font_bold, title_font_size)
    subtitle_font = ImageFont.truetype(font_regular, subtitle_font_size)
    info_font = ImageFont.truetype(font_regular, bottom_font_size)

    # 测量标题宽度，用于计算卡片尺寸
    temp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    title_bbox = temp_draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]

    # ===== 4. 计算卡片尺寸和位置 =====
    text_padding = int(120 * base_unit)                 # 文字与卡片边缘的内边距
    card_w = title_w + text_padding * 2                 # 卡片宽度 = 标题宽 + 左右内边距
    card_h = int(880 * base_unit)                       # 卡片高度
    card_radius = int(35 * base_unit)                   # 圆角半径

    # 根据文字对齐方式决定卡片水平位置
    if text_align == "center":
        card_x = (w - card_w) // 2                      # 居中
    else:
        card_x = int(120 * base_unit)                   # 左对齐

    card_y = int(380 * base_unit)                       # 卡片垂直位置（偏下）

    # 确保卡片不超出图片右边界
    if card_x + card_w > w - 40:
        card_w = w - card_x - 40

    # ===== 5. 绘制毛玻璃卡片 =====
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card)
    card_color = (30, 35, 45, card_alpha)               # 深色半透明背景
    card_border_color = (255, 255, 255, 60)             # 半透明白色边框
    draw_rounded_rect(
        card_draw,
        [card_x, card_y, card_x + card_w, card_y + card_h],
        card_radius,
        card_color,
        card_border_color,
        2,
    )

    # 将卡片合成到背景
    bg = Image.alpha_composite(bg, card)
    cover = bg.convert("RGB")
    cover_rgba = cover.convert("RGBA")

    # ===== 6. 粘贴 Logo =====
    if brand_logo and os.path.exists(brand_logo):
        logo_img = Image.open(brand_logo)
        lw, lh = logo_img.size
        new_lw = int(lw * logo_h / lh)
        logo_resized = logo_img.resize((new_lw, logo_h), Image.LANCZOS)
        if logo_resized.mode != "RGBA":
            logo_resized = logo_resized.convert("RGBA")

        if logo_position == "center":
            # Logo 顶部居中
            logo_x = (w - new_lw) // 2
            logo_y = int(30 * base_unit)
        elif logo_position == "topleft":
            # Logo 固定左上角
            logo_x = int(50 * base_unit)
            logo_y = int(30 * base_unit)
        else:
            # auto 模式：Logo 在卡片左上角附近，与边框留 gap 避免重合
            gap = int(20 * base_unit)
            logo_x = card_x + gap                            # 卡片左边 + 间距
            logo_y = card_y - logo_h - gap + int(15 * base_unit)  # 卡片上方 + 间距

        cover_rgba.paste(logo_resized, (logo_x, logo_y), logo_resized)

    # ===== 7. 绘制文字 =====
    cover_final = cover_rgba.convert("RGB")
    draw = ImageDraw.Draw(cover_final)

    card_left = card_x
    card_right = card_x + card_w

    def get_text_x(text, font):
        """根据对齐方式计算文字的水平位置"""
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        if text_align == "center":
            return (card_left + card_right - tw) // 2       # 水平居中
        return card_left + text_padding                      # 左对齐

    # 从卡片顶部开始排列文字
    text_y = card_y + int(120 * base_unit)

    # 型号名称（绿色）
    if model_name:
        draw.text(
            (get_text_x(model_name, model_font), text_y),
            model_name, font=model_font, fill=(139, 195, 74),
        )
        text_y += int(135 * base_unit)

    # 主标题（白色）
    draw.text(
        (get_text_x(title, title_font), text_y),
        title, font=title_font, fill=(255, 255, 255),
    )
    text_y += int(225 * base_unit)

    # 副标题（浅灰色）
    if subtitle:
        draw.text(
            (get_text_x(subtitle, subtitle_font), text_y),
            subtitle, font=subtitle_font, fill=(230, 230, 230),
        )

    # ===== 8. 底部信息条 =====
    bottom_bar_h = int(110 * base_unit)
    bottom_bar = Image.new("RGBA", (w, bottom_bar_h), (0, 0, 0, 100))
    cover_final_rgba = cover_final.convert("RGBA")
    cover_final_rgba.paste(bottom_bar, (0, h - bottom_bar_h), bottom_bar)

    cover_final = cover_final_rgba.convert("RGB")
    draw = ImageDraw.Draw(cover_final)

    # 底部品牌文字（根据对齐方式决定位置）
    if brand_logo:
        info_text = "seeed studio"
        info_bbox = draw.textbbox((0, 0), info_text, font=info_font)
        info_w = info_bbox[2] - info_bbox[0]
        if text_align == "center":
            # 居中放置
            draw.text(
                ((w - info_w) // 2, h - bottom_bar_h + int(30 * base_unit)),
                info_text, font=info_font, fill=(139, 195, 74),
            )
        else:
            # 左下角
            draw.text(
                (int(55 * base_unit), h - bottom_bar_h + int(30 * base_unit)),
                info_text, font=info_font, fill=(139, 195, 74),
            )

    # ===== 9. 保存输出 =====
    cover_final.save(output_path, quality=98)
    print(f"Cover saved to: {output_path}")
    return output_path


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="生成 Seeed Studio 风格封面图片")
    parser.add_argument("--background", "-b", required=True, help="背景图片路径")
    parser.add_argument("--title", "-t", required=True, help="主标题文字")
    parser.add_argument("--subtitle", "-s", default="", help="副标题文字")
    parser.add_argument("--model", "-m", default="", help="型号名称（绿色标签）")
    parser.add_argument("--logo", "-l", default=None, help="品牌 Logo 图片路径")
    parser.add_argument("--output", "-o", default="cover_output.jpg", help="输出文件路径")
    parser.add_argument("--blur", type=int, default=2, help="背景模糊半径")
    parser.add_argument("--brightness", type=float, default=0.75, help="背景亮度 (0-1)")
    parser.add_argument(
        "--text-align", default="center", choices=["center", "left"],
        help="文字对齐方式: center(居中) 或 left(左对齐)",
    )
    parser.add_argument(
        "--logo-position", default="auto", choices=["auto", "topleft", "center"],
        help="Logo 位置: auto(卡片左上), topleft(固定左上), center(顶部居中)",
    )

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
        text_align=args.text_align,
        logo_position=args.logo_position,
    )


if __name__ == "__main__":
    main()
