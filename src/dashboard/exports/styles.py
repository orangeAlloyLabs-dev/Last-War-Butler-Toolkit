"""Style constants for player card export."""

from dataclasses import dataclass, field


@dataclass
class CardStyle:
    """Style configuration for player card images."""

    # Canvas dimensions
    width: int = 800
    height: int = 1000

    # Colors - Dark theme matching dashboard
    bg_gradient_start: tuple[int, int, int] = (26, 26, 46)  # #1a1a2e
    bg_gradient_end: tuple[int, int, int] = (22, 33, 62)  # #16213e
    card_bg: tuple[int, int, int, int] = (255, 255, 255, 13)  # rgba(255,255,255,0.05)
    border_color: tuple[int, int, int, int] = (255, 255, 255, 26)  # rgba(255,255,255,0.1)

    # Text colors
    text_primary: tuple[int, int, int] = (255, 255, 255)
    text_secondary: tuple[int, int, int] = (153, 153, 153)  # rgba(255,255,255,0.6)
    text_muted: tuple[int, int, int] = (128, 128, 128)  # rgba(255,255,255,0.5)

    # Accent colors
    accent_gradient_start: tuple[int, int, int] = (102, 126, 234)  # #667eea
    accent_gradient_end: tuple[int, int, int] = (118, 75, 162)  # #764ba2

    # Status colors
    color_success: tuple[int, int, int] = (34, 197, 94)  # #22c55e
    color_warning: tuple[int, int, int] = (234, 179, 8)  # #eab308
    color_danger: tuple[int, int, int] = (239, 68, 68)  # #ef4444
    color_info: tuple[int, int, int] = (59, 130, 246)  # #3b82f6
    color_neutral: tuple[int, int, int] = (108, 117, 125)  # #6c757d

    # Tier colors
    tier_colors: dict[str, tuple[int, int, int]] = field(
        default_factory=lambda: {
            "Core": (34, 197, 94),  # green
            "Strong": (59, 130, 246),  # blue
            "Standard": (234, 179, 8),  # yellow
            "Probation": (239, 68, 68),  # red
        }
    )

    # Spacing
    padding: int = 24
    section_gap: int = 20
    card_radius: int = 12
    badge_radius: int = 4

    # Font sizes (will be scaled based on available fonts)
    font_size_title: int = 28
    font_size_header: int = 20
    font_size_body: int = 16
    font_size_small: int = 12
    font_size_metric: int = 32


# Default style instance
DEFAULT_STYLE = CardStyle()


# Font fallback chain for cross-platform support
FONT_PATHS = [
    # macOS
    "/System/Library/Fonts/SFNSText.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    # Linux
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    # Windows
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
]

FONT_BOLD_PATHS = [
    # macOS
    "/System/Library/Fonts/SFNSText-Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial Bold.ttf",
    # Linux
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    # Windows
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
]
