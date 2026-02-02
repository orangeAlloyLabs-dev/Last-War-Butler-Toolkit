"""Reusable drawing components for player card export."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .styles import DEFAULT_STYLE, FONT_BOLD_PATHS, FONT_PATHS, CardStyle


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Get a font with fallback chain."""
    paths = FONT_BOLD_PATHS if bold else FONT_PATHS
    for path in paths:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def draw_gradient_background(
    img: Image.Image,
    start_color: tuple[int, int, int],
    end_color: tuple[int, int, int],
    vertical: bool = True,
) -> None:
    """Draw a gradient background on the image."""
    width, height = img.size
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            if vertical:
                ratio = y / height
            else:
                ratio = x / width
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            pixels[x, y] = (r, g, b)


def draw_rounded_rect(
    draw: ImageDraw.ImageDraw,
    bbox: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, ...] | None = None,
    outline: tuple[int, ...] | None = None,
    width: int = 1,
) -> None:
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = bbox
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)


def draw_badge(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    text: str,
    bg_color: tuple[int, int, int],
    text_color: tuple[int, int, int] = (255, 255, 255),
    style: CardStyle | None = None,
) -> int:
    """Draw a badge with text and return the width."""
    if style is None:
        style = DEFAULT_STYLE

    font = get_font(style.font_size_small, bold=False)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding_h = 8
    padding_v = 4
    badge_width = text_width + padding_h * 2
    badge_height = text_height + padding_v * 2

    x, y = position
    draw_rounded_rect(
        draw,
        (x, y, x + badge_width, y + badge_height),
        style.badge_radius,
        fill=bg_color,
    )
    draw.text(
        (x + padding_h, y + padding_v - 1),
        text,
        fill=text_color,
        font=font,
    )
    return badge_width


def draw_metric_card(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    size: tuple[int, int],
    label: str,
    value: str,
    style: CardStyle | None = None,
) -> None:
    """Draw a metric card with label and value."""
    if style is None:
        style = DEFAULT_STYLE

    x, y = position
    w, h = size

    # Card background
    draw_rounded_rect(
        draw,
        (x, y, x + w, y + h),
        style.card_radius,
        fill=(40, 40, 60),
        outline=(60, 60, 80),
    )

    # Label
    label_font = get_font(style.font_size_small)
    draw.text(
        (x + 10, y + 8),
        label.upper(),
        fill=style.text_secondary,
        font=label_font,
    )

    # Value
    value_font = get_font(style.font_size_header, bold=True)
    draw.text(
        (x + 10, y + 28),
        value,
        fill=style.text_primary,
        font=value_font,
    )


def draw_progress_bar(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    size: tuple[int, int],
    progress: float,
    color: tuple[int, int, int],
    bg_color: tuple[int, int, int] = (60, 60, 80),
    style: CardStyle | None = None,
) -> None:
    """Draw a progress bar."""
    if style is None:
        style = DEFAULT_STYLE

    x, y = position
    w, h = size

    # Background
    draw_rounded_rect(draw, (x, y, x + w, y + h), h // 2, fill=bg_color)

    # Progress
    progress = max(0.0, min(1.0, progress))
    if progress > 0:
        progress_width = int(w * progress)
        if progress_width > h:
            draw_rounded_rect(draw, (x, y, x + progress_width, y + h), h // 2, fill=color)


def draw_avatar_circle(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    radius: int,
    initials: str,
    style: CardStyle | None = None,
) -> None:
    """Draw a circular avatar with initials."""
    if style is None:
        style = DEFAULT_STYLE

    x, y = center

    # Draw gradient circle (approximated with solid colors)
    draw.ellipse(
        (x - radius, y - radius, x + radius, y + radius),
        fill=style.accent_gradient_start,
    )

    # Draw initials
    font = get_font(radius, bold=True)
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw.text(
        (x - text_width // 2, y - text_height // 2 - 4),
        initials,
        fill=style.text_primary,
        font=font,
    )


def draw_section_header(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    text: str,
    style: CardStyle | None = None,
) -> int:
    """Draw a section header and return the height."""
    if style is None:
        style = DEFAULT_STYLE

    font = get_font(style.font_size_body, bold=True)
    draw.text(position, text, fill=style.text_primary, font=font)
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1] + 8


def draw_day_theme_box(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    size: tuple[int, int],
    theme: str,
    points: str,
    rank_str: str,
    status_color: tuple[int, int, int],
    style: CardStyle | None = None,
) -> None:
    """Draw a day theme performance box."""
    if style is None:
        style = DEFAULT_STYLE

    x, y = position
    w, h = size

    # Box background
    draw_rounded_rect(
        draw,
        (x, y, x + w, y + h),
        style.badge_radius,
        fill=(40, 40, 60),
        outline=(60, 60, 80),
    )

    # Theme name
    theme_font = get_font(style.font_size_small, bold=True)
    draw.text((x + 6, y + 6), theme, fill=style.text_primary, font=theme_font)

    # Points
    points_font = get_font(style.font_size_body, bold=True)
    draw.text((x + 6, y + 24), points, fill=style.text_primary, font=points_font)

    # Rank with status color
    rank_font = get_font(style.font_size_small)
    draw.text((x + 6, y + 46), rank_str, fill=status_color, font=rank_font)


def draw_week_row(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    width: int,
    week: str,
    opponent: str,
    result: str,
    points: str,
    result_color: tuple[int, int, int],
    style: CardStyle | None = None,
) -> int:
    """Draw a week row in the recent weeks table."""
    if style is None:
        style = DEFAULT_STYLE

    x, y = position
    row_height = 28
    font = get_font(style.font_size_small)

    # Column widths
    col_week = 80
    col_opponent = 200
    col_result = 70

    # Week
    draw.text((x, y + 6), week, fill=style.text_primary, font=font)

    # Opponent
    draw.text((x + col_week, y + 6), opponent, fill=style.text_secondary, font=font)

    # Result
    draw.text((x + col_week + col_opponent, y + 6), result, fill=result_color, font=font)

    # Points
    draw.text(
        (x + col_week + col_opponent + col_result, y + 6),
        points,
        fill=style.text_primary,
        font=font,
    )

    return row_height


def get_status_color(points: float | None, style: CardStyle | None = None) -> tuple[int, int, int]:
    """Get status color based on points threshold."""
    if style is None:
        style = DEFAULT_STYLE

    if points is None:
        return style.color_neutral
    if points >= 7_200_000:
        return style.color_success
    elif points >= 3_600_000:
        return style.color_warning
    else:
        return style.color_danger


def get_result_color(result: str, style: CardStyle | None = None) -> tuple[int, int, int]:
    """Get color for win/loss/draw result."""
    if style is None:
        style = DEFAULT_STYLE

    result_lower = result.lower()
    if result_lower == "win":
        return style.color_success
    elif result_lower == "loss":
        return style.color_danger
    elif result_lower == "draw":
        return style.color_warning
    return style.color_neutral
