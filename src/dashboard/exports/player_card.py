"""Player card image generation for PNG and animated GIF exports."""

from dataclasses import dataclass, field
from datetime import datetime
from io import BytesIO

from PIL import Image, ImageDraw

from .components import (
    draw_avatar_circle,
    draw_badge,
    draw_day_theme_box,
    draw_gradient_background,
    draw_metric_card,
    draw_progress_bar,
    draw_rounded_rect,
    draw_section_header,
    draw_week_row,
    get_font,
    get_result_color,
    get_status_color,
)
from .styles import DEFAULT_STYLE, CardStyle


@dataclass
class PlayerCardData:
    """Data structure for player card generation."""

    player_name: str
    player_rank: int
    tier: str
    reliability: float
    avg_normalized: float
    is_active: bool = True
    officer_role: str | None = None
    power: float = 0.0
    level: int = 1
    kill_count: int = 0
    current_week_data: dict = field(default_factory=dict)
    cycle_data: dict | None = None
    recent_weeks: list[dict] = field(default_factory=list)


def format_points(pts: float | None) -> str:
    """Format points for display."""
    if pts is None:
        return "--"
    if pts >= 1_000_000:
        return f"{pts / 1_000_000:.1f}M"
    elif pts >= 1_000:
        return f"{pts / 1_000:.0f}K"
    else:
        return f"{pts:.0f}"


def format_power_m(power: float) -> str:
    """Format raw power value as millions."""
    return f"{power / 1_000_000:.1f}M"


def get_rank_str(rank: int | None, total: int) -> str:
    """Format rank for display."""
    if rank is None:
        return "--"
    rank_suffix = "th" if 11 <= rank <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(rank % 10, "th")
    return f"#{rank}{rank_suffix}/{total}"


SHORT_THEMES = {
    "Radar Training": "Radar",
    "Base Expansion": "Base",
    "Age of Science": "Science",
    "Train Heroes": "Heroes",
    "Total Mobilization": "Mobilize",
    "Enemy Buster": "Buster",
}


def _draw_header(
    draw: ImageDraw.ImageDraw,
    data: PlayerCardData,
    y_offset: int,
    style: CardStyle,
) -> int:
    """Draw the header section with avatar, name, and badges."""
    x = style.padding
    y = y_offset

    # Avatar
    avatar_radius = 35
    avatar_center = (x + avatar_radius, y + avatar_radius)
    initials = "".join(word[0].upper() for word in data.player_name.split()[:2])
    draw_avatar_circle(draw, avatar_center, avatar_radius, initials, style)

    # Name
    name_x = x + avatar_radius * 2 + 20
    name_font = get_font(style.font_size_title, bold=True)
    draw.text((name_x, y + 5), data.player_name, fill=style.text_primary, font=name_font)

    # Badges row
    badge_y = y + 45
    badge_x = name_x

    # Active/Inactive badge
    status_color = style.color_success if data.is_active else style.color_danger
    status_text = "Active" if data.is_active else "Inactive"
    badge_width = draw_badge(draw, (badge_x, badge_y), status_text, status_color, style=style)
    badge_x += badge_width + 8

    # Rank badge
    badge_width = draw_badge(
        draw, (badge_x, badge_y), f"R{data.player_rank}", style.color_neutral, style=style
    )
    badge_x += badge_width + 8

    # Tier badge
    tier_color = style.tier_colors.get(data.tier, style.color_neutral)
    draw_badge(draw, (badge_x, badge_y), data.tier, tier_color, style=style)

    # Officer role badge (if applicable)
    if data.officer_role:
        badge_x += 80
        draw_badge(draw, (badge_x, badge_y), data.officer_role, style.color_info, style=style)

    return avatar_radius * 2 + 20


def _draw_stats_row(
    draw: ImageDraw.ImageDraw,
    data: PlayerCardData,
    y_offset: int,
    style: CardStyle,
) -> int:
    """Draw the stats row with power, level, kills, tier."""
    x = style.padding
    y = y_offset
    card_width = (style.width - style.padding * 2 - 30) // 4
    card_height = 60

    # Power
    draw_metric_card(
        draw, (x, y), (card_width, card_height), "Power", format_power_m(data.power), style
    )

    # Level
    draw_metric_card(
        draw,
        (x + card_width + 10, y),
        (card_width, card_height),
        "Level",
        f"{data.level}/35",
        style,
    )

    # Kills
    draw_metric_card(
        draw,
        (x + (card_width + 10) * 2, y),
        (card_width, card_height),
        "Kills",
        f"{data.kill_count:,}",
        style,
    )

    # Tier
    tier_color = style.tier_colors.get(data.tier, style.color_neutral)
    tier_x = x + (card_width + 10) * 3
    draw_rounded_rect(
        draw,
        (tier_x, y, tier_x + card_width, y + card_height),
        style.card_radius,
        fill=(40, 40, 60),
        outline=(60, 60, 80),
    )
    label_font = get_font(style.font_size_small)
    draw.text((tier_x + 10, y + 8), "TIER", fill=style.text_secondary, font=label_font)
    tier_font = get_font(style.font_size_header, bold=True)
    draw.text((tier_x + 10, y + 28), data.tier, fill=tier_color, font=tier_font)

    return card_height + 10


def _draw_vs_combat(
    draw: ImageDraw.ImageDraw,
    data: PlayerCardData,
    y_offset: int,
    style: CardStyle,
) -> int:
    """Draw VS Combat Performance section."""
    x = style.padding
    y = y_offset

    # Section header
    header_height = draw_section_header(draw, (x, y), "VS Combat Performance", style)
    y += header_height + 5

    # Two-column layout
    col_width = (style.width - style.padding * 2 - 20) // 2

    # Left column: Reliability
    draw_rounded_rect(
        draw,
        (x, y, x + col_width, y + 80),
        style.card_radius,
        fill=(40, 40, 60),
        outline=(60, 60, 80),
    )
    label_font = get_font(style.font_size_small)
    draw.text((x + 12, y + 10), "RELIABILITY", fill=style.text_secondary, font=label_font)

    reliability_pct = data.reliability * 100
    value_font = get_font(style.font_size_header, bold=True)
    if data.reliability >= 0.75:
        rel_color = style.color_success
    elif data.reliability >= 0.50:
        rel_color = style.color_warning
    else:
        rel_color = style.color_danger
    draw.text((x + 12, y + 28), f"{reliability_pct:.0f}%", fill=rel_color, font=value_font)

    # Progress bar
    draw_progress_bar(
        draw, (x + 12, y + 58), (col_width - 24, 10), data.reliability, rel_color, style=style
    )

    # Right column: Avg Normalized Points
    right_x = x + col_width + 20
    draw_rounded_rect(
        draw,
        (right_x, y, right_x + col_width, y + 80),
        style.card_radius,
        fill=(40, 40, 60),
        outline=(60, 60, 80),
    )
    draw.text((right_x + 12, y + 10), "AVG NORMALIZED", fill=style.text_secondary, font=label_font)
    draw.text(
        (right_x + 12, y + 28),
        f"{data.avg_normalized:.1f}",
        fill=style.text_primary,
        font=value_font,
    )

    # Points description
    small_font = get_font(style.font_size_small)
    draw.text(
        (right_x + 12, y + 58),
        "points per day (4-week avg)",
        fill=style.text_muted,
        font=small_font,
    )

    return 80 + header_height + 15


def _draw_current_week(
    draw: ImageDraw.ImageDraw,
    data: PlayerCardData,
    y_offset: int,
    style: CardStyle,
) -> int:
    """Draw current week day theme performance."""
    x = style.padding
    y = y_offset

    week_data = data.current_week_data
    if not week_data or "days" not in week_data:
        return 0

    week_num = week_data.get("week_number", "?")
    header_height = draw_section_header(draw, (x, y), f"Current Week (Week {week_num})", style)
    y += header_height + 5

    # 6 day boxes
    box_width = (style.width - style.padding * 2 - 50) // 6
    box_height = 70

    days = week_data.get("days", {})

    for day_num in range(1, 7):
        day_info = days.get(day_num, {})
        theme = day_info.get("theme", f"Day {day_num}")
        points = day_info.get("points")
        rank = day_info.get("rank")
        total = day_info.get("total", 0)

        display_theme = SHORT_THEMES.get(theme, theme)
        points_str = format_points(points)
        rank_str = get_rank_str(rank, total) if rank else "--"
        status_color = get_status_color(points, style)

        box_x = x + (day_num - 1) * (box_width + 10)
        draw_day_theme_box(
            draw,
            (box_x, y),
            (box_width, box_height),
            display_theme,
            points_str,
            rank_str,
            status_color,
            style,
        )

    return box_height + header_height + 15


def _draw_cycle_totals(
    draw: ImageDraw.ImageDraw,
    data: PlayerCardData,
    y_offset: int,
    style: CardStyle,
) -> int:
    """Draw cycle total day theme performance."""
    x = style.padding
    y = y_offset

    cycle_data = data.cycle_data
    if not cycle_data or "day_totals" not in cycle_data:
        return 0

    cycle_num = cycle_data.get("cycle_number", "?")
    header_height = draw_section_header(draw, (x, y), f"Cycle Totals (Cycle {cycle_num})", style)
    y += header_height + 5

    # 6 day boxes
    box_width = (style.width - style.padding * 2 - 50) // 6
    box_height = 70

    day_totals = cycle_data.get("day_totals", {})
    weeks_in_cycle = cycle_data.get("weeks_in_cycle", 0)

    for day_num in range(1, 7):
        day_info = day_totals.get(day_num, {})
        theme = day_info.get("theme", f"Day {day_num}")
        total_pts = day_info.get("total_points", 0)
        times_participated = day_info.get("times_participated", 0)
        rank = day_info.get("rank")
        total_players = day_info.get("total_players", 0)

        display_theme = SHORT_THEMES.get(theme, theme)
        points_str = format_points(total_pts) if times_participated > 0 else "--"
        if rank and times_participated > 0:
            rank_str = get_rank_str(rank, total_players)
        else:
            rank_str = f"0/{weeks_in_cycle}wks"
        if times_participated > 0:
            status_color = get_status_color(total_pts, style)
        else:
            status_color = style.color_neutral

        box_x = x + (day_num - 1) * (box_width + 10)
        draw_day_theme_box(
            draw,
            (box_x, y),
            (box_width, box_height),
            display_theme,
            points_str,
            rank_str,
            status_color,
            style,
        )

    return box_height + header_height + 15


def _draw_recent_weeks(
    draw: ImageDraw.ImageDraw,
    data: PlayerCardData,
    y_offset: int,
    style: CardStyle,
) -> int:
    """Draw recent weeks table."""
    x = style.padding
    y = y_offset

    if not data.recent_weeks:
        return 0

    header_height = draw_section_header(draw, (x, y), "Recent Weeks", style)
    y += header_height + 5

    # Table background
    table_width = style.width - style.padding * 2
    table_height = len(data.recent_weeks) * 28 + 32
    draw_rounded_rect(
        draw,
        (x, y, x + table_width, y + table_height),
        style.card_radius,
        fill=(40, 40, 60),
        outline=(60, 60, 80),
    )

    # Table header
    header_font = get_font(style.font_size_small, bold=True)
    col_week = 80
    col_opponent = 200
    col_result = 70
    draw.text((x + 12, y + 8), "Week", fill=style.text_secondary, font=header_font)
    draw.text((x + 12 + col_week, y + 8), "Opponent", fill=style.text_secondary, font=header_font)
    draw.text(
        (x + 12 + col_week + col_opponent, y + 8),
        "Result",
        fill=style.text_secondary,
        font=header_font,
    )
    draw.text(
        (x + 12 + col_week + col_opponent + col_result, y + 8),
        "Points",
        fill=style.text_secondary,
        font=header_font,
    )

    # Rows
    row_y = y + 32
    for week in data.recent_weeks:
        result_color = get_result_color(week.get("result", ""), style)
        draw_week_row(
            draw,
            (x + 12, row_y),
            table_width - 24,
            week.get("week", ""),
            week.get("opponent", "TBD"),
            week.get("result", "PENDING"),
            week.get("points", "-"),
            result_color,
            style,
        )
        row_y += 28

    return table_height + header_height + 15


def _draw_footer(
    draw: ImageDraw.ImageDraw,
    y_offset: int,
    style: CardStyle,
) -> int:
    """Draw the footer with branding."""
    x = style.padding
    y = y_offset

    font = get_font(style.font_size_small)
    footer_text = f"Generated by Last War Butler | {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    draw.text((x, y), footer_text, fill=style.text_muted, font=font)

    return 20


def generate_player_card_png(
    data: PlayerCardData,
    style: CardStyle | None = None,
) -> bytes:
    """Generate a PNG image of the player card.

    Args:
        data: PlayerCardData with all player information
        style: Optional CardStyle for customization

    Returns:
        PNG image as bytes
    """
    if style is None:
        style = DEFAULT_STYLE

    # Create image with RGB mode for gradient
    img = Image.new("RGB", (style.width, style.height))
    draw_gradient_background(img, style.bg_gradient_start, style.bg_gradient_end)

    draw = ImageDraw.Draw(img)

    # Draw sections
    y = style.padding

    # Header
    y += _draw_header(draw, data, y, style)
    y += style.section_gap

    # Stats row
    y += _draw_stats_row(draw, data, y, style)
    y += style.section_gap

    # VS Combat Performance
    y += _draw_vs_combat(draw, data, y, style)
    y += style.section_gap - 10

    # Current Week (if data available)
    current_week_height = _draw_current_week(draw, data, y, style)
    if current_week_height > 0:
        y += current_week_height
        y += style.section_gap - 10

    # Cycle Totals (if data available)
    cycle_height = _draw_cycle_totals(draw, data, y, style)
    if cycle_height > 0:
        y += cycle_height
        y += style.section_gap - 10

    # Recent Weeks
    recent_height = _draw_recent_weeks(draw, data, y, style)
    if recent_height > 0:
        y += recent_height
        y += style.section_gap

    # Footer
    _draw_footer(draw, style.height - 30, style)

    # Convert to bytes
    buffer = BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)
    return buffer.getvalue()


def generate_player_card_gif(
    data: PlayerCardData,
    style: CardStyle | None = None,
) -> bytes:
    """Generate an animated GIF of the player card.

    The animation reveals sections progressively:
    1. Header + Stats
    2. VS Combat Performance
    3. Current Week themes
    4. Cycle totals
    5. Recent Weeks table
    6. Full card (hold)

    Args:
        data: PlayerCardData with all player information
        style: Optional CardStyle for customization

    Returns:
        GIF image as bytes
    """
    if style is None:
        style = DEFAULT_STYLE

    frames: list[Image.Image] = []
    durations = [1000, 1000, 1000, 1000, 1000, 2000]  # milliseconds per frame

    # Calculate section heights
    temp_img = Image.new("RGB", (style.width, style.height))
    temp_draw = ImageDraw.Draw(temp_img)

    sections = []
    y = style.padding

    # Section 1: Header
    header_h = _draw_header(temp_draw, data, y, style)
    sections.append(("header", y, header_h))
    y += header_h + style.section_gap

    # Section 2: Stats
    stats_h = _draw_stats_row(temp_draw, data, y, style)
    sections.append(("stats", y, stats_h))
    y += stats_h + style.section_gap

    # Section 3: VS Combat
    vs_h = _draw_vs_combat(temp_draw, data, y, style)
    sections.append(("vs_combat", y, vs_h))
    y += vs_h + style.section_gap - 10

    # Section 4: Current Week
    current_h = _draw_current_week(temp_draw, data, y, style)
    if current_h > 0:
        sections.append(("current_week", y, current_h))
        y += current_h + style.section_gap - 10

    # Section 5: Cycle Totals
    cycle_h = _draw_cycle_totals(temp_draw, data, y, style)
    if cycle_h > 0:
        sections.append(("cycle_totals", y, cycle_h))
        y += cycle_h + style.section_gap - 10

    # Section 6: Recent Weeks
    recent_h = _draw_recent_weeks(temp_draw, data, y, style)
    if recent_h > 0:
        sections.append(("recent_weeks", y, recent_h))

    # Generate frames with progressive reveal
    reveal_groups = [
        ["header", "stats"],  # Frame 1
        ["vs_combat"],  # Frame 2
        ["current_week"],  # Frame 3
        ["cycle_totals"],  # Frame 4
        ["recent_weeks"],  # Frame 5
        [],  # Frame 6 (full, no new sections)
    ]

    visible_sections: set[str] = set()

    for i, group in enumerate(reveal_groups):
        # Add new sections to visible set
        visible_sections.update(group)

        # Create frame
        frame = Image.new("RGB", (style.width, style.height))
        draw_gradient_background(frame, style.bg_gradient_start, style.bg_gradient_end)
        frame_draw = ImageDraw.Draw(frame)

        # Draw visible sections
        for section_name, section_y, section_h in sections:
            if section_name in visible_sections:
                if section_name == "header":
                    _draw_header(frame_draw, data, section_y, style)
                elif section_name == "stats":
                    _draw_stats_row(frame_draw, data, section_y, style)
                elif section_name == "vs_combat":
                    _draw_vs_combat(frame_draw, data, section_y, style)
                elif section_name == "current_week":
                    _draw_current_week(frame_draw, data, section_y, style)
                elif section_name == "cycle_totals":
                    _draw_cycle_totals(frame_draw, data, section_y, style)
                elif section_name == "recent_weeks":
                    _draw_recent_weeks(frame_draw, data, section_y, style)

        # Always draw footer on last frame
        if i == len(reveal_groups) - 1:
            _draw_footer(frame_draw, style.height - 30, style)

        # Convert to palette mode for GIF
        frame_p = frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
        frames.append(frame_p)

    # Save as GIF
    buffer = BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=durations[: len(frames)],
        loop=0,
        optimize=True,
    )
    buffer.seek(0)
    return buffer.getvalue()
