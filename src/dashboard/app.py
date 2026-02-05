"""Main Streamlit dashboard application."""

import streamlit as st

st.set_page_config(
    page_title="Last War Butler",
    page_icon="🏰",
    layout="wide",
)

# Custom CSS for dark theme matching HTML mockup
st.markdown(
    """
    <style>
    /* Main background — deep dark gradient */
    .stApp {
        background: linear-gradient(160deg, #0b0b1a 0%, #111827 100%);
    }

    /* Sidebar — solid dark panel */
    [data-testid="stSidebar"] {
        background: #0d0d1f;
        border-right: 1px solid #2a2a4a;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background: rgba(102, 126, 234, 0.08);
        border-left: 3px solid #667eea;
    }

    /* Metric cards — solid dark panels */
    [data-testid="stMetric"] {
        background: #1e1e38;
        border: 1px solid #2a2a4a;
        border-radius: 14px;
        padding: 20px;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3);
    }

    [data-testid="stMetricLabel"] {
        color: #6b7280;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 32px;
        font-weight: 700;
    }

    [data-testid="stMetricDelta"] {
        color: #f59e0b;
    }

    /* Section headers — left accent bar */
    .stMarkdown h2, .stMarkdown h3 {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .stMarkdown h2::before, .stMarkdown h3::before {
        content: "";
        display: inline-block;
        width: 3px;
        height: 22px;
        border-radius: 2px;
        background: linear-gradient(180deg, #667eea, #764ba2);
        flex-shrink: 0;
    }

    /* Data tables — dark card with alternating rows */
    [data-testid="stDataFrame"] {
        background: #1e1e38;
        border: 1px solid #2a2a4a;
        border-radius: 14px;
        overflow: hidden;
    }

    [data-testid="stDataFrame"] [data-testid="StyledDataFrameRowCell"]:nth-child(odd) {
        background: #15152a;
    }

    [data-testid="stDataFrame"] [data-testid="StyledDataFrameRowCell"]:nth-child(even) {
        background: #1a1a30;
    }

    /* Buttons — primary gradient with glow */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 0 16px rgba(102, 126, 234, 0.35);
    }

    .stButton > button[kind="secondary"] {
        background: transparent;
        border: 1px solid #3a3a5a;
        color: #9ca3af;
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: #9ca3af;
        color: #ffffff;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: #1e1e38;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
    }

    /* Info/Warning/Error boxes */
    .stAlert {
        background: #1e1e38;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
    }

    /* Tabs — solid dark */
    .stTabs [data-baseweb="tab-list"] {
        background: #1e1e38;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: #9ca3af;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* Inputs and selects — dark solid with border */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: #1a1a30;
        border: 1px solid #3a3a5a;
        border-radius: 8px;
        color: white;
    }

    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
    }

    /* Multiselect */
    .stMultiSelect > div > div {
        background: #1a1a30;
        border: 1px solid #3a3a5a;
        border-radius: 8px;
    }

    .stMultiSelect > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
    }

    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    /* Dividers */
    hr {
        border-color: #2a2a4a;
    }

    /* Caption/muted text */
    .stCaption, small {
        color: #6b7280;
    }

    /* Download button — secondary style */
    .stDownloadButton > button {
        background: transparent;
        border: 1px solid #3a3a5a;
        color: #9ca3af;
    }

    .stDownloadButton > button:hover {
        border-color: #9ca3af;
        color: #ffffff;
    }

    /* Chart containers */
    [data-testid="stVegaLiteChart"],
    .stPlotlyChart {
        background: #1e1e38;
        border: 1px solid #2a2a4a;
        border-radius: 14px;
        padding: 12px;
        overflow: hidden;
        box-sizing: border-box;
    }

    /* Day performance grid */
    .day-perf-grid { display:grid; grid-template-columns:repeat(6,1fr); gap:8px; }
    .day-box { background:#1e1e38; border:1px solid #2a2a4a;
      border-radius:6px; padding:10px 6px; text-align:center; }
    .day-box .day-label { font-size:10px; font-weight:600; color:#6b7280; margin-bottom:4px; }
    .day-box .day-value { font-size:16px; font-weight:700; }
    .day-box .day-value.green { color:#22c55e; }
    .day-box .day-value.amber { color:#f59e0b; }
    .day-box .day-value.red { color:#ef4444; }

    /* --- Sidebar hierarchical navigation --- */
    .sidebar-brand {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 4px 0 12px 0;
    }

    .nav-section-label {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        color: #6b7280;
        letter-spacing: 1.5px;
        padding: 12px 0 6px 0;
    }

    [data-testid="stSidebar"] .stButton {
        width: 100% !important;
        display: flex !important;
        justify-content: flex-start !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: none !important;
        border-left: 3px solid transparent !important;
        border-radius: 0 !important;
        text-align: left !important;
        font-size: 14px;
        color: #9ca3af;
        padding: 8px 12px 8px 20px !important;
        width: 100%;
        box-shadow: none !important;
        transform: none !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.04) !important;
        transform: none !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"],
    [data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {
        color: #ffffff !important;
        background: rgba(102, 126, 234, 0.08) !important;
        border-left: 3px solid #667eea !important;
    }

    .nav-child-marker {
        display: none;
        height: 0;
        margin: 0;
        padding: 0;
    }

    .nav-child-marker + div .stButton > button {
        padding-left: 52px !important;
        font-size: 13px;
    }

    .sidebar-footer {
        text-align: center;
        color: #6b7280;
        font-size: 12px;
        padding: 8px 0;
    }

    .sidebar-version {
        color: #4b5563;
        font-size: 11px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Navigation hierarchy ---
NAV_STRUCTURE = [
    {
        "section": "Dashboard",
        "items": [
            {"icon": "◉", "label": "Overview", "page": "Overview", "children": []},
            {"icon": "♛", "label": "Player Summary", "page": "Player Summary", "children": []},
            {"icon": "⚔", "label": "Duel VS Report", "page": "Duel VS", "children": []},
            {"icon": "📊", "label": "Analytics", "page": "Analytics", "children": []},
            {"icon": "🏆", "label": "War Results", "page": "War Results", "children": []},
            {"icon": "📅", "label": "Events", "page": "Events", "children": []},
        ],
    },
    {
        "section": "Management",
        "items": [
            {
                "icon": "👥",
                "label": "Players",
                "page": "Players",
                "children": [
                    {"label": "Import Members", "page": "Import Members"},
                    {"label": "Update Kills", "page": "Update Kills"},
                ],
            },
            {"icon": "⚙", "label": "Settings", "page": "Settings", "children": []},
        ],
    },
]


def _is_group_active(item: dict, current_page: str) -> bool:
    """Check if a nav group (parent or any child) is the current page."""
    if item["page"] == current_page:
        return True
    return any(c["page"] == current_page for c in item.get("children", []))


def _navigate_to(page_name: str) -> None:
    """Set the active page in session state."""
    st.session_state["page"] = page_name


st.title("Last War Butler Dashboard")
st.markdown("---")

# Sidebar navigation
if "page" not in st.session_state:
    st.session_state["page"] = "Overview"

# Brand header
st.sidebar.markdown(
    '<div class="sidebar-brand">🏰 Last War Butler</div>',
    unsafe_allow_html=True,
)

current_page = st.session_state["page"]

for section in NAV_STRUCTURE:
    st.sidebar.markdown(
        f'<div class="nav-section-label">{section["section"]}</div>',
        unsafe_allow_html=True,
    )
    for item in section["items"]:
        group_active = _is_group_active(item, current_page)
        is_active = item["page"] == current_page

        st.sidebar.button(
            f"{item['icon']}  {item['label']}",
            key=f"nav_{item['page']}",
            on_click=_navigate_to,
            args=(item["page"],),
            use_container_width=True,
            type="primary" if is_active else "secondary",
        )

        if group_active and item.get("children"):
            for child in item["children"]:
                is_child_active = child["page"] == current_page
                # Marker div for CSS child-indentation
                st.sidebar.markdown(
                    '<div class="nav-child-marker"></div>',
                    unsafe_allow_html=True,
                )
                st.sidebar.button(
                    child["label"],
                    key=f"nav_{child['page']}",
                    on_click=_navigate_to,
                    args=(child["page"],),
                    use_container_width=True,
                    type="primary" if is_child_active else "secondary",
                )

page = st.session_state["page"]


ALLIANCE_MEMBER_LIMIT = 100


def get_player_stats(active_only: bool = True):
    """Get player statistics from database."""
    try:
        from src.data.models import Player
        from src.data.storage import get_session, init_database

        init_database()
        with get_session() as session:
            query = session.query(Player)
            if active_only:
                query = query.filter(Player.is_active == True)  # noqa: E712
            players = query.all()
            total_members = len(players)
            total_power = sum(p.power for p in players)
            return {
                "total_members": total_members,
                "total_power": total_power,
                "players": [
                    (p.id, p.name, p.rank, p.officer_role, p.power, p.level) for p in players
                ],
            }
    except Exception:
        return {"total_members": 0, "total_power": 0, "players": []}


def get_inactive_players():
    """Get inactive (soft-deleted) players."""
    try:
        from src.data.models import Player
        from src.data.storage import get_session, init_database

        init_database()
        with get_session() as session:
            players = session.query(Player).filter(Player.is_active == False).all()  # noqa: E712
            return [(p.id, p.name, p.rank, p.power) for p in players]
    except Exception:
        return []


def get_active_member_count():
    """Get count of active members."""
    try:
        from src.data.models import Player
        from src.data.storage import get_session, init_database

        init_database()
        with get_session() as session:
            return session.query(Player).filter(Player.is_active == True).count()  # noqa: E712
    except Exception:
        return 0


def get_total_alliance_kills(active_only: bool = True) -> int:
    """Get total kill count across all active players."""
    try:
        from sqlalchemy import func as sql_func

        from src.data.models import Player
        from src.data.storage import get_session, init_database

        init_database()
        with get_session() as session:
            query = session.query(sql_func.sum(Player.kill_count))
            if active_only:
                query = query.filter(Player.is_active == True)  # noqa: E712
            result = query.scalar()
            return result or 0
    except Exception:
        return 0


def format_power_m(power: float) -> str:
    """Format raw power value as millions with 1 decimal (e.g., 163321088 -> '163.3M')."""
    return f"{power / 1_000_000:.1f}M"


def render_sparkline_svg(
    values: list[float],
    color: str = "#667eea",
    with_fill: bool = False,
    gradient_id: str = "sparkGrad",
) -> str:
    """Build an inline SVG sparkline from a list of numbers."""
    if not values or len(values) < 2:
        return ""
    min_v = min(values)
    max_v = max(values)
    spread = max_v - min_v if max_v != min_v else 1.0
    step = 120 / (len(values) - 1)
    points = " ".join(
        f"{i * step:.1f},{30 - (v - min_v) / spread * 26:.1f}" for i, v in enumerate(values)
    )
    fill_html = ""
    if with_fill:
        last_x = (len(values) - 1) * step
        fill_html = (
            f'<defs><linearGradient id="{gradient_id}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{color}" stop-opacity="0.3"/>'
            f'<stop offset="100%" stop-color="{color}" stop-opacity="0"/>'
            f"</linearGradient></defs>"
            f'<polygon fill="url(#{gradient_id})" '
            f'points="{points} {last_x:.1f},32 0,32"/>'
        )
    return (
        f'<div style="height:32px;margin-top:8px;">'
        f'<svg viewBox="0 0 120 32" preserveAspectRatio="none" '
        f'style="width:100%;height:100%;">'
        f"{fill_html}"
        f'<polyline fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" points="{points}"/>'
        f"</svg></div>"
    )


def render_section_header(title: str) -> str:
    """Return HTML for a styled section header with purple gradient accent bar."""
    return (
        f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">'
        f'<div style="width:3px;height:22px;border-radius:2px;'
        f'background:linear-gradient(180deg,#667eea,#764ba2);flex-shrink:0;"></div>'
        f'<span style="font-size:13px;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:1.2px;color:#9ca3af;">{title}</span></div>'
    )


def render_tier_badge(tier: str) -> str:
    """Return HTML for a styled tier badge."""
    tier_styles = {
        "Core": ("rgba(34,197,94,0.15)", "#22c55e"),
        "Strong": ("rgba(59,130,246,0.15)", "#3b82f6"),
        "Standard": ("rgba(234,179,8,0.15)", "#eab308"),
        "Probation": ("rgba(239,68,68,0.15)", "#ef4444"),
    }
    bg, fg = tier_styles.get(tier, ("rgba(108,117,125,0.15)", "#6c757d"))
    return (
        f'<span style="display:inline-block;padding:3px 10px;border-radius:100px;'
        f"font-size:11px;font-weight:700;letter-spacing:0.5px;"
        f'background:{bg};color:{fg};">{tier}</span>'
    )


def render_events_summary(
    events: list,
    event_type_icons: dict,
    display_tz: str = "EST",
    tz_options: dict | None = None,
) -> str:
    """Render compact events summary HTML grouped by day."""
    from datetime import datetime
    from zoneinfo import ZoneInfo

    if not events:
        return (
            '<div style="background:#1e1e38;border:1px solid #2a2a4a;border-radius:14px;'
            'padding:20px;text-align:center;color:#6b7280;font-size:13px;">'
            "No events scheduled for the next 7 days</div>"
        )

    # Timezone conversion helper
    def convert_event_time(dt: datetime) -> datetime:
        """Convert naive EST datetime to target timezone."""
        if tz_options is None or display_tz == "EST":
            return dt
        est = ZoneInfo("America/New_York")
        target = ZoneInfo(tz_options.get(display_tz, "America/New_York"))
        aware_dt = dt.replace(tzinfo=est)
        return aware_dt.astimezone(target)

    # Group events by day label (using converted times for day grouping)
    today = datetime.now().date()
    grouped: dict[str, list] = {}

    for event in events:
        converted_dt = convert_event_time(event.start_datetime)
        if hasattr(converted_dt, "date"):
            event_date = converted_dt.date()
        else:
            event_date = event.start_datetime.date()
        delta = (event_date - today).days

        if delta == 0:
            day_label = "Today"
        elif delta == 1:
            day_label = "Tomorrow"
        else:
            day_label = event_date.strftime("%A")  # Weekday name

        if day_label not in grouped:
            grouped[day_label] = []
        grouped[day_label].append((event, converted_dt))

    # Build HTML
    html_parts = [
        '<div style="background:#1e1e38;border:1px solid #2a2a4a;border-radius:14px;'
        'overflow:hidden;">'
    ]

    for i, (day_label, day_events) in enumerate(grouped.items()):
        # Day header
        border_top = "border-top:1px solid #2a2a4a;" if i > 0 else ""
        html_parts.append(
            f'<div style="padding:10px 14px;{border_top}">'
            f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:0.8px;color:#6b7280;margin-bottom:8px;">{day_label}</div>'
        )

        # Events for this day
        for event, converted_dt in day_events:
            icon = event_type_icons.get(event.event_type, "📅")
            time_str = converted_dt.strftime("%-I:%M %p")
            tz_label = f" {display_tz}" if display_tz != "EST" else ""
            html_parts.append(
                f'<div style="display:flex;align-items:center;gap:10px;padding:6px 0;'
                f'font-size:13px;">'
                f'<span style="flex-shrink:0;">{icon}</span>'
                f'<span style="color:#667eea;min-width:85px;">{time_str}{tz_label}</span>'
                f'<span style="color:#ffffff;">{event.title}</span>'
                f"</div>"
            )

        html_parts.append("</div>")

    html_parts.append("</div>")
    return "".join(html_parts)


if page == "Overview":
    from datetime import datetime

    import altair as alt
    import pandas as pd

    from src.data.models import AllianceEvent, DuelWeek, KillHistory, KillImport
    from src.data.storage import get_session, init_database

    init_database()

    # --- Upcoming Events Summary ---
    from datetime import timedelta

    # Timezone options for overview
    OVERVIEW_TZ_OPTIONS = {
        "EST": "America/New_York",
        "BRT": "America/Sao_Paulo",
        "KST": "Asia/Seoul",
    }

    # Header with timezone selector
    tz_col1, tz_col2 = st.columns([3, 1])
    with tz_col1:
        st.markdown(render_section_header("Upcoming Events"), unsafe_allow_html=True)
    with tz_col2:
        selected_tz = st.selectbox(
            "Timezone",
            options=list(OVERVIEW_TZ_OPTIONS.keys()),
            index=0,
            key="overview_events_tz",
            label_visibility="collapsed",
        )

    EVENT_TYPE_ICONS_OVERVIEW = {
        "Duel VS": "⚔",
        "Kill Event": "🎯",
        "Alliance War": "🏰",
        "Rally": "🚩",
        "Resource Event": "📦",
        "Training Event": "🏋",
        "Custom": "📅",
    }

    try:
        with get_session() as session:
            now = datetime.now()
            week_ahead = now + timedelta(days=7)
            upcoming_events = (
                session.query(AllianceEvent)
                .filter(AllianceEvent.start_datetime >= now)
                .filter(AllianceEvent.start_datetime <= week_ahead)
                .order_by(AllianceEvent.start_datetime)
                .all()
            )
            st.markdown(
                render_events_summary(
                    upcoming_events, EVENT_TYPE_ICONS_OVERVIEW, selected_tz, OVERVIEW_TZ_OPTIONS
                ),
                unsafe_allow_html=True,
            )
    except Exception:
        st.markdown(
            '<div style="background:#1e1e38;border:1px solid #2a2a4a;border-radius:14px;'
            'padding:20px;text-align:center;color:#6b7280;font-size:13px;">'
            "Unable to load events</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    st.markdown(render_section_header("Alliance Overview"), unsafe_allow_html=True)

    stats = get_player_stats()
    total_kills = get_total_alliance_kills()

    # --- Gather sparkline data ---
    members_sparkline_values: list[float] = []
    kills_sparkline_values: list[float] = []
    winrate_sparkline_values: list[float] = []

    try:
        with get_session() as session:
            # Members sparkline: player_count from last 8 KillImport batches
            recent_imports = (
                session.query(KillImport).order_by(KillImport.recorded_at.desc()).limit(8).all()
            )
            if recent_imports:
                members_sparkline_values = [
                    float(imp.player_count) for imp in reversed(recent_imports)
                ]

            # Kills sparkline: sum of kills from KillHistory grouped by import batch
            from sqlalchemy import func as sql_func

            kill_sums = (
                session.query(
                    KillHistory.import_id,
                    sql_func.sum(KillHistory.kill_count),
                )
                .filter(KillHistory.import_id.isnot(None))
                .group_by(KillHistory.import_id)
                .order_by(KillHistory.import_id.desc())
                .limit(8)
                .all()
            )
            if kill_sums:
                kills_sparkline_values = [float(s[1]) for s in reversed(kill_sums)]

            # Win rate sparkline: from DuelWeek results (rolling win %)
            recent_weeks = (
                session.query(DuelWeek)
                .filter(DuelWeek.result.isnot(None))
                .order_by(DuelWeek.week_number.desc())
                .limit(8)
                .all()
            )
            if recent_weeks:
                ordered_weeks = list(reversed(recent_weeks))
                cumulative_wins = 0
                for i, w in enumerate(ordered_weeks):
                    if w.result == "win":
                        cumulative_wins += 1
                    winrate_sparkline_values.append(cumulative_wins / (i + 1) * 100)
    except Exception:
        pass

    # Synthetic power sparkline (upward curve — no historical power data)
    power_sparkline_values = [60, 64, 66, 70, 74, 78, 84, 90]

    # --- Metric cards with sparklines ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Members", stats["total_members"])
        if members_sparkline_values:
            st.markdown(
                render_sparkline_svg(members_sparkline_values, "#667eea"),
                unsafe_allow_html=True,
            )
    with col2:
        total_power = stats["total_power"]
        total_power_m = total_power / 1_000_000
        if total_power_m >= 1000:
            power_str = f"{total_power_m / 1000:.2f}B"
        else:
            power_str = f"{total_power_m:.1f}M"
        st.metric("Alliance Power", power_str)
        power_spark = render_sparkline_svg(
            power_sparkline_values,
            "#f59e0b",
            with_fill=True,
            gradient_id="sparkPower",
        )
        st.markdown(power_spark, unsafe_allow_html=True)
    with col3:
        st.metric("Total Kills", f"{total_kills:,}")
        if kills_sparkline_values:
            st.markdown(
                render_sparkline_svg(kills_sparkline_values, "#22c55e"),
                unsafe_allow_html=True,
            )
    with col4:
        # Compute win rate
        win_rate_str = "—"
        try:
            with get_session() as session:
                all_results = session.query(DuelWeek).filter(DuelWeek.result.isnot(None)).all()
                if all_results:
                    wins = sum(1 for w in all_results if w.result == "win")
                    win_rate_str = f"{wins / len(all_results) * 100:.0f}%"
        except Exception:
            pass
        st.metric("War Win Rate", win_rate_str)
        if winrate_sparkline_values:
            st.markdown(
                render_sparkline_svg(winrate_sparkline_values, "#667eea"),
                unsafe_allow_html=True,
            )

    # --- Charts: Kill History + Power by Tier ---
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("**Kill History (Last 7 Days)**")
        try:
            with get_session() as session:
                from datetime import datetime, timedelta

                seven_days_ago = datetime.now() - timedelta(days=7)
                kill_data = (
                    session.query(
                        sql_func.date(KillHistory.recorded_at).label("date"),
                        sql_func.sum(KillHistory.kill_count).label("total_kills"),
                    )
                    .filter(KillHistory.recorded_at >= seven_days_ago)
                    .group_by(sql_func.date(KillHistory.recorded_at))
                    .order_by(sql_func.date(KillHistory.recorded_at))
                    .all()
                )
                if kill_data:
                    kh_df = pd.DataFrame(
                        [{"date": str(r.date), "kills": int(r.total_kills)} for r in kill_data]
                    )
                    kh_df["date"] = pd.to_datetime(kh_df["date"])
                    chart = (
                        alt.Chart(kh_df)
                        .mark_area(
                            line={"color": "#f59e0b", "strokeWidth": 2.5},
                            color=alt.Gradient(
                                gradient="linear",
                                stops=[
                                    alt.GradientStop(color="rgba(245,158,11,0.25)", offset=0),
                                    alt.GradientStop(color="rgba(245,158,11,0)", offset=1),
                                ],
                                x1=1,
                                x2=1,
                                y1=0,
                                y2=1,
                            ),
                        )
                        .encode(
                            x=alt.X(
                                "date:T",
                                title=None,
                                scale=alt.Scale(
                                    domain=[
                                        (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
                                        datetime.now().strftime("%Y-%m-%d"),
                                    ]
                                ),
                            ),
                            y=alt.Y("kills:Q", title="Total Kills"),
                        )
                        .configure_view(fill="#1e1e38", strokeWidth=0)
                        .configure_axis(
                            gridColor="#2a2a4a",
                            labelColor="#6b7280",
                            titleColor="#9ca3af",
                        )
                        .properties(height=220, width="container")
                    )
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("No kill history data in the last 7 days.")
        except Exception:
            st.info("No kill history data available.")

    with chart_col2:
        st.markdown("**Power Distribution by Tier**")
        try:
            from src.data.duel_tracker import get_rolling_report
            from src.data.models import Player

            rolling = get_rolling_report(weeks=4)
            if rolling:
                # Build tier -> total power mapping
                tier_power: dict[str, float] = {}
                player_tiers: dict[int, str] = {p["player_id"]: p["tier"] for p in rolling}
                with get_session() as session:
                    players = session.query(Player).filter(Player.is_active == True).all()  # noqa: E712
                    for p in players:
                        t = player_tiers.get(p.id, "Probation")
                        tier_power[t] = tier_power.get(t, 0) + p.power

                if tier_power:
                    tier_colors = {
                        "Core": "#22c55e",
                        "Strong": "#3b82f6",
                        "Standard": "#eab308",
                        "Probation": "#ef4444",
                    }
                    tier_order = ["Core", "Strong", "Standard", "Probation"]
                    tp_df = pd.DataFrame(
                        [
                            {"Tier": t, "Power": tier_power.get(t, 0) / 1_000_000_000}
                            for t in tier_order
                            if tier_power.get(t, 0) > 0
                        ]
                    )
                    chart = (
                        alt.Chart(tp_df)
                        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                        .encode(
                            x=alt.X(
                                "Tier:N",
                                sort=tier_order,
                                title=None,
                                axis=alt.Axis(labelAngle=0),
                            ),
                            y=alt.Y("Power:Q", title="Power (B)"),
                            color=alt.Color(
                                "Tier:N",
                                scale=alt.Scale(
                                    domain=list(tier_colors.keys()),
                                    range=list(tier_colors.values()),
                                ),
                                legend=None,
                            ),
                        )
                        .configure_view(fill="#1e1e38", strokeWidth=0)
                        .configure_axis(
                            gridColor="#2a2a4a",
                            labelColor="#6b7280",
                            titleColor="#9ca3af",
                        )
                        .properties(height=220, width="container")
                    )
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("No tier data available.")
            else:
                st.info("No duel data available for tier chart.")
        except Exception:
            st.info("No tier data available.")

    # --- Top Players Table ---
    if stats["players"]:
        st.markdown("**Top Players by Power**")
        sorted_players = sorted(stats["players"], key=lambda p: p[4], reverse=True)[:5]

        # Try to get tier data for badges
        player_tiers_map: dict[int, str] = {}
        try:
            from src.data.duel_tracker import get_rolling_report

            rolling = get_rolling_report(weeks=4)
            if rolling:
                player_tiers_map = {p["player_id"]: p["tier"] for p in rolling}
        except Exception:
            pass

        rows_html = ""
        for p_id, p_name, p_rank, p_officer, p_power, p_level in sorted_players:
            tier = player_tiers_map.get(p_id, "—")
            tier_html = render_tier_badge(tier) if tier != "—" else "—"
            power_display = format_power_m(p_power)
            rows_html += (
                f"<tr>"
                f"<td style='color:#fff;font-weight:600;padding:10px 14px;'>{p_name}</td>"
                f"<td style='padding:10px 14px;'>{tier_html}</td>"
                f"<td style='padding:10px 14px;color:#9ca3af;'>{power_display}</td>"
                f"<td style='padding:10px 14px;color:#9ca3af;'>R{p_rank}</td>"
                f"<td style='padding:10px 14px;color:#9ca3af;'>{p_level}</td>"
                f"</tr>"
            )

        table_html = (
            '<div style="background:#1e1e38;border:1px solid #2a2a4a;border-radius:14px;'
            'overflow:hidden;margin-top:4px;">'
            '<table style="width:100%;border-collapse:separate;border-spacing:0;font-size:13px;">'
            "<thead><tr>"
            '<th style="text-align:left;padding:10px 14px;font-size:11px;font-weight:700;'
            "text-transform:uppercase;letter-spacing:0.8px;color:#6b7280;"
            'border-bottom:1px solid #2a2a4a;">Player</th>'
            '<th style="text-align:left;padding:10px 14px;font-size:11px;font-weight:700;'
            "text-transform:uppercase;letter-spacing:0.8px;color:#6b7280;"
            'border-bottom:1px solid #2a2a4a;">Tier</th>'
            '<th style="text-align:left;padding:10px 14px;font-size:11px;font-weight:700;'
            "text-transform:uppercase;letter-spacing:0.8px;color:#6b7280;"
            'border-bottom:1px solid #2a2a4a;">Power</th>'
            '<th style="text-align:left;padding:10px 14px;font-size:11px;font-weight:700;'
            "text-transform:uppercase;letter-spacing:0.8px;color:#6b7280;"
            'border-bottom:1px solid #2a2a4a;">Rank</th>'
            '<th style="text-align:left;padding:10px 14px;font-size:11px;font-weight:700;'
            "text-transform:uppercase;letter-spacing:0.8px;color:#6b7280;"
            'border-bottom:1px solid #2a2a4a;">Level</th>'
            "</tr></thead>"
            f"<tbody>{rows_html}</tbody></table></div>"
        )
        st.markdown(table_html, unsafe_allow_html=True)

    if stats["total_members"] == 0:
        st.info("No members imported yet. Go to **Import Members** to add your alliance members.")

elif page == "Players":
    st.header("Player Management")

    import pandas as pd

    from src.data.models import Player
    from src.data.storage import get_session, init_database

    init_database()

    VALID_OFFICER_ROLES = ["", "Leader", "Warlord", "Recruiter", "Muse", "Butler"]

    # Show active member count
    active_count = get_active_member_count()
    st.metric("Active Members", f"{active_count}/{ALLIANCE_MEMBER_LIMIT}")

    stats = get_player_stats(active_only=True)

    if stats["players"]:
        # Create editable dataframe with raw values (not formatted)
        df = pd.DataFrame(
            stats["players"],
            columns=["ID", "Name", "Rank", "Officer", "Power", "Level"],
        )
        # Replace None with empty string for officer
        df["Officer"] = df["Officer"].fillna("")
        df = df.sort_values("Power", ascending=False)

        st.markdown("Edit values directly in the table. Select members below to delete.")

        edited_df = st.data_editor(
            df,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small", disabled=True),
                "Name": st.column_config.TextColumn("Player Name", required=True),
                "Rank": st.column_config.SelectboxColumn(
                    "Rank", options=[1, 2, 3, 4, 5], required=True, width="small"
                ),
                "Officer": st.column_config.SelectboxColumn(
                    "Officer", options=VALID_OFFICER_ROLES, width="small"
                ),
                "Power": st.column_config.NumberColumn("Power (M)", min_value=0.0, format="%.1f"),
                "Level": st.column_config.NumberColumn("Level", min_value=1, max_value=35, step=1),
            },
            hide_index=True,
            use_container_width=True,
            num_rows="fixed",
            key="player_editor",
        )

        col1, col2, col3 = st.columns([1, 1, 3])

        with col1:
            if st.button("Save Changes", type="primary"):
                try:
                    with get_session() as session:
                        updated = 0
                        for _, row in edited_df.iterrows():
                            player = session.query(Player).filter(Player.id == row["ID"]).first()
                            if player:
                                player.name = row["Name"]
                                player.rank = int(row["Rank"])
                                player.officer_role = row["Officer"] if row["Officer"] else None
                                player.power = float(row["Power"])
                                player.level = int(row["Level"])
                                updated += 1
                        session.commit()
                    st.success(f"Updated {updated} members!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving changes: {e}")

        with col2:
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="Export CSV",
                data=csv_data,
                file_name="alliance_members.csv",
                mime="text/csv",
            )

        # Deactivate section (soft-delete)
        st.markdown("---")
        st.subheader("Deactivate Members")
        st.caption(
            "Deactivated members are removed from the active roster "
            "but their duel stats are preserved."
        )

        # Multi-select for deactivation
        player_options = {
            f"{row['Name']} (R{row['Rank']}, {format_power_m(row['Power'])})": row["ID"]
            for _, row in df.iterrows()
        }
        selected = st.multiselect(
            "Select members to deactivate:",
            options=list(player_options.keys()),
        )

        if selected:
            # Check if this would leave 0 active members
            remaining = len(df) - len(selected)
            if remaining < 1:
                st.warning("Cannot deactivate all members. At least 1 active member must remain.")
            elif st.button(f"Deactivate {len(selected)} Member(s)", type="secondary"):
                try:
                    with get_session() as session:
                        deactivated = 0
                        for name in selected:
                            player_id = player_options[name]
                            player = session.query(Player).filter(Player.id == player_id).first()
                            if player:
                                player.is_active = False
                                deactivated += 1
                        session.commit()
                    st.success(f"Deactivated {deactivated} member(s)!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deactivating members: {e}")

        # Quick stats
        st.markdown("---")
        st.subheader("Quick Stats")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Power", format_power_m(df["Power"].mean()))
        with col2:
            st.metric("Highest Power", format_power_m(df["Power"].max()))
        with col3:
            st.metric("Average Level", f"{df['Level'].mean():.1f}")

    # Inactive members section
    inactive_players = get_inactive_players()
    if inactive_players:
        st.markdown("---")
        with st.expander(f"Inactive Members ({len(inactive_players)})", expanded=False):
            st.caption("These members have been deactivated. Their duel stats are preserved.")

            inactive_df = pd.DataFrame(
                inactive_players,
                columns=["ID", "Name", "Rank", "Power"],
            )
            inactive_df = inactive_df.sort_values("Name")

            st.dataframe(
                inactive_df,
                column_config={
                    "ID": st.column_config.NumberColumn("ID", width="small"),
                    "Name": st.column_config.TextColumn("Player Name"),
                    "Rank": st.column_config.NumberColumn("Rank", width="small"),
                    "Power": st.column_config.NumberColumn("Power (M)", format="%.1f"),
                },
                hide_index=True,
                use_container_width=True,
            )

            # Reactivate section
            reactivate_options = {
                f"{row['Name']} (R{row['Rank']}, {format_power_m(row['Power'])})": row["ID"]
                for _, row in inactive_df.iterrows()
            }
            selected_reactivate = st.multiselect(
                "Select members to reactivate:",
                options=list(reactivate_options.keys()),
                key="reactivate_select",
            )

            if selected_reactivate:
                # Check if reactivating would exceed limit
                new_total = active_count + len(selected_reactivate)
                if new_total > ALLIANCE_MEMBER_LIMIT:
                    st.warning(
                        f"Cannot reactivate {len(selected_reactivate)} member(s). "
                        f"Would exceed {ALLIANCE_MEMBER_LIMIT} member limit "
                        f"({active_count} active + {len(selected_reactivate)} = {new_total})."
                    )
                elif st.button(f"Reactivate {len(selected_reactivate)} Member(s)", type="primary"):
                    try:
                        with get_session() as session:
                            reactivated = 0
                            for name in selected_reactivate:
                                player_id = reactivate_options[name]
                                player = (
                                    session.query(Player).filter(Player.id == player_id).first()
                                )
                                if player:
                                    player.is_active = True
                                    reactivated += 1
                            session.commit()
                        st.success(f"Reactivated {reactivated} member(s)!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error reactivating members: {e}")

    if not stats["players"] and not inactive_players:
        st.info("No players tracked yet. Go to **Import Members** to add your alliance members.")

elif page == "Player Summary":
    st.markdown(render_section_header("Player Summary"), unsafe_allow_html=True)

    import pandas as pd

    from src.data.duel_tracker import (
        TIER_THRESHOLDS,
        get_all_players_current_week_daily_points,
        get_all_players_cycle_theme_totals,
        get_current_cycle,
        get_current_week,
        get_player_current_week_daily_points,
        get_player_cycle_theme_totals,
        get_recent_weeks,
        get_rolling_report,
    )
    from src.data.models import DUEL_DAY_THEMES, Player
    from src.data.storage import get_session, init_database

    init_database()

    # Get active players for selector
    stats = get_player_stats(active_only=True)

    if not stats["players"]:
        st.info("No players tracked yet. Go to **Import Members** to add your alliance members.")
    else:
        # Player selector dropdown
        player_options = {}
        for p_id, p_name, p_rank, p_officer, p_power, p_level in stats["players"]:
            label = f"{p_name} (R{p_rank}, {format_power_m(p_power)})"
            player_options[label] = p_id

        selected_player_label = st.selectbox(
            "Select Player", list(player_options.keys()), key="player_summary_select"
        )
        selected_player_id = player_options[selected_player_label]

        # Get full player data
        with get_session() as session:
            player = session.query(Player).filter(Player.id == selected_player_id).first()

            if player:
                # === Header Section ===
                st.markdown("---")
                col_avatar, col_info = st.columns([1, 4])

                with col_avatar:
                    # Avatar with initials
                    initials = "".join(word[0].upper() for word in player.name.split()[:2])
                    st.markdown(
                        f"""
                        <div style="
                            width: 80px;
                            height: 80px;
                            border-radius: 50%;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            color: white;
                            font-size: 28px;
                            font-weight: bold;
                            margin: 10px auto;
                        ">{initials}</div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col_info:
                    # Player name and ID
                    st.markdown(f"### {player.name}")
                    st.caption(f"Database ID: {player.id}")

                    # Status badges
                    badge_cols = st.columns(4)
                    with badge_cols[0]:
                        status_color = "#22c55e" if player.is_active else "#ef4444"
                        status_text = "Active" if player.is_active else "Inactive"
                        st.markdown(
                            f"<span style='background-color:{status_color};color:white;"
                            f"padding:2px 8px;border-radius:4px;font-size:12px;'>"
                            f"{status_text}</span>",
                            unsafe_allow_html=True,
                        )
                    with badge_cols[1]:
                        st.markdown(
                            f"<span style='background-color:#6c757d;color:white;"
                            f"padding:2px 8px;border-radius:4px;font-size:12px;'>"
                            f"R{player.rank}</span>",
                            unsafe_allow_html=True,
                        )
                    with badge_cols[2]:
                        if player.officer_role:
                            st.markdown(
                                f"<span style='background-color:#3b82f6;color:white;"
                                f"padding:2px 8px;border-radius:4px;font-size:12px;'>"
                                f"{player.officer_role}</span>",
                                unsafe_allow_html=True,
                            )
                    with badge_cols[3]:
                        join_date = player.created_at.strftime("%Y-%m-%d")
                        st.caption(f"Joined: {join_date}")

                # === Stats Grid (4 metrics) ===
                st.markdown("---")
                st.markdown(render_section_header("Player Stats"), unsafe_allow_html=True)

                # Get tier from rolling report
                rolling = get_rolling_report(weeks=4)
                player_rolling = next(
                    (p for p in rolling if p["player_id"] == selected_player_id), None
                )

                tier = "Probation"
                reliability = 0.0
                weeks_participated = 0
                total_weeks = 0
                avg_normalized = 0.0
                if player_rolling:
                    tier = player_rolling["tier"]
                    reliability = player_rolling["reliability"]
                    weeks_participated = player_rolling["weeks_participated"]
                    total_weeks = player_rolling["total_weeks"]
                    avg_normalized = player_rolling["avg_normalized_points"]

                # Tier colors
                tier_colors = {
                    "Core": "#22c55e",
                    "Strong": "#3b82f6",
                    "Standard": "#eab308",
                    "Probation": "#ef4444",
                }
                tier_color = tier_colors.get(tier, "#6c757d")

                stat_cols = st.columns(5)
                with stat_cols[0]:
                    st.metric("Current Power", format_power_m(player.power))
                with stat_cols[1]:
                    st.metric("Base Level", f"{player.level}/35")
                with stat_cols[2]:
                    st.metric("Alliance Rank", f"R{player.rank}")
                with stat_cols[3]:
                    st.metric("Kill Count", f"{player.kill_count:,}")
                    if player.kill_count_updated_at:
                        st.caption(
                            f"Updated: {player.kill_count_updated_at.strftime('%Y-%m-%d %H:%M')}"
                        )
                with stat_cols[4]:
                    st.markdown(
                        f"**Performance Tier**<br>"
                        f"<span style='color:{tier_color};font-size:24px;font-weight:bold;'>"
                        f"{tier}</span>",
                        unsafe_allow_html=True,
                    )

                # === VS Combat Performance Section ===
                st.markdown("---")
                st.markdown(render_section_header("VS Combat Performance"), unsafe_allow_html=True)

                if player_rolling and weeks_participated > 0:
                    perf_cols = st.columns(3)

                    # 1. Current Cycle Stats
                    with perf_cols[0]:
                        st.markdown("**Current Cycle Stats**")
                        total_points = player_rolling["avg_raw_points"] * weeks_participated
                        target_points = 1_000_000  # 1M target per cycle
                        progress = min(total_points / target_points, 1.0)
                        met_target = total_points >= target_points

                        st.metric("Total Points", f"{total_points:,.0f}")
                        st.progress(progress)
                        status_color = "#22c55e" if met_target else "#eab308"
                        status_text = "Met" if met_target else "Below"
                        st.markdown(
                            f"Target: 1M | "
                            f"<span style='color:{status_color};'>{status_text}</span>",
                            unsafe_allow_html=True,
                        )

                    # 2. Participation Rate
                    with perf_cols[1]:
                        st.markdown("**Participation Rate**")
                        reliability_pct = reliability * 100
                        st.metric("Reliability", f"{reliability_pct:.0f}%")
                        st.progress(reliability)
                        if reliability >= 0.75:
                            rel_color = "#22c55e"
                            rel_status = "Excellent"
                        elif reliability >= 0.50:
                            rel_color = "#eab308"
                            rel_status = "Moderate"
                        else:
                            rel_color = "#ef4444"
                            rel_status = "Low"
                        st.markdown(
                            f"<span style='color:{rel_color};'>{rel_status}</span> "
                            f"({weeks_participated}/{total_weeks} weeks)",
                            unsafe_allow_html=True,
                        )

                    # 3. Latest Week Performance
                    with perf_cols[2]:
                        st.markdown("**4-Week Average**")
                        st.metric("Avg Points/Week", f"{player_rolling['avg_raw_points']:,.0f}")
                        st.metric("Avg Normalized", f"{avg_normalized:.1f}")
                else:
                    st.info("No VS combat data available for this player in the last 4 weeks.")

                # === Kill Growth Section ===
                st.markdown("---")
                st.markdown(render_section_header("Kill Growth"), unsafe_allow_html=True)

                from src.data.duel_tracker import (
                    get_player_kill_growth_metrics,
                    get_player_kill_history,
                )

                kill_metrics = get_player_kill_growth_metrics(selected_player_id)

                if kill_metrics["current_kills"] > 0 or kill_metrics["recent_imports"]:
                    # Kill growth metrics row
                    kill_cols = st.columns(3)
                    with kill_cols[0]:
                        st.metric("Current Kills", f"{kill_metrics['current_kills']:,}")
                    with kill_cols[1]:
                        gained = kill_metrics["kills_gained_since_last"]
                        gained_str = f"+{gained:,}" if gained >= 0 else f"{gained:,}"
                        st.metric("Since Last Update", gained_str)
                    with kill_cols[2]:
                        avg_growth = kill_metrics["avg_weekly_growth"]
                        st.metric("Avg Weekly Growth", f"+{avg_growth:,.0f}")

                    # Kill history chart
                    st.markdown("**Kill History**")
                    range_option = st.selectbox(
                        "Date Range",
                        options=["1 Week", "4 Weeks", "Lifetime"],
                        index=0,
                        key="kill_history_range",
                    )
                    days_map = {"1 Week": 7, "4 Weeks": 28, "Lifetime": None}
                    kill_history = get_player_kill_history(
                        selected_player_id, days=days_map[range_option]
                    )
                    if kill_history and len(kill_history) > 1:
                        kill_df = pd.DataFrame(kill_history)
                        kill_df["date"] = pd.to_datetime(kill_df["date"]).dt.normalize()
                        kill_df = kill_df.set_index("date")

                        # Build a date range spanning the full selected period
                        selected_days = days_map[range_option]
                        if selected_days is not None:
                            range_start = pd.Timestamp.now().normalize() - pd.Timedelta(
                                days=selected_days
                            )
                        else:
                            range_start = kill_df.index.min()
                        full_range = pd.date_range(
                            range_start, pd.Timestamp.now().normalize(), freq="D"
                        )
                        kill_df = kill_df.reindex(full_range)

                        st.line_chart(kill_df["kills"])
                    else:
                        st.info("Not enough data points for the selected range.")

                    # Recent imports kill progression
                    if kill_metrics["recent_imports"]:
                        st.markdown("**Recent Imports**")
                        imports_data = []
                        for imp in kill_metrics["recent_imports"]:
                            gained_str = (
                                f"+{imp['gained']:,}" if imp["gained"] is not None else "--"
                            )
                            date_str = imp["recorded_at"].strftime("%Y-%m-%d")
                            imports_data.append(
                                {
                                    "Date": date_str,
                                    "Kills": f"{imp['kill_count']:,}",
                                    "Growth": gained_str,
                                }
                            )
                        st.dataframe(
                            pd.DataFrame(imports_data),
                            hide_index=True,
                            use_container_width=True,
                        )
                else:
                    st.info("No kill data available for this player.")

                # === Day Performance Section ===
                st.markdown("---")
                st.markdown(render_section_header("Day Theme Performance"), unsafe_allow_html=True)

                # Shortened theme names for display
                short_themes = {
                    "Radar Training": "Radar",
                    "Base Expansion": "Base",
                    "Age of Science": "Science",
                    "Train Heroes": "Heroes",
                    "Total Mobilization": "Mobilize",
                    "Enemy Buster": "Buster",
                }

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

                def get_rank_str(rank: int | None, total: int) -> str:
                    """Format rank for display."""
                    if rank is None:
                        return ""
                    rank_suffix = (
                        "th"
                        if 11 <= rank <= 13
                        else {1: "st", 2: "nd", 3: "rd"}.get(rank % 10, "th")
                    )
                    return f" {rank}{rank_suffix} of {total}"

                def get_status_color_icon(pts: float | None) -> tuple[str, str]:
                    """Get status color and icon based on points threshold."""
                    if pts is None:
                        return "#6c757d", "--"  # gray for no data
                    if pts >= 7_200_000:
                        return "#22c55e", "✓"  # green
                    elif pts >= 3_600_000:
                        return "#eab308", "⚠"  # yellow
                    else:
                        return "#ef4444", "✗"  # red

                # Get current week data
                current_week = get_current_week()
                current_week_data = get_player_current_week_daily_points(selected_player_id)
                all_current_week = get_all_players_current_week_daily_points()

                # Get current cycle data
                current_cycle = get_current_cycle()
                cycle_data = None
                all_cycle_totals = {}
                if current_cycle:
                    cycle_data = get_player_cycle_theme_totals(selected_player_id, current_cycle.id)
                    all_cycle_totals = get_all_players_cycle_theme_totals(current_cycle.id)

                has_current_week_data = (
                    "error" not in current_week_data
                    and current_week_data.get("days")
                    and any(d["points"] is not None for d in current_week_data["days"].values())
                )
                has_cycle_data = (
                    cycle_data
                    and "error" not in cycle_data
                    and cycle_data.get("day_totals")
                    and any(d["times_participated"] > 0 for d in cycle_data["day_totals"].values())
                )

                if has_current_week_data or has_cycle_data:
                    # === Current Week Section ===
                    if has_current_week_data:
                        week_num = current_week_data.get("week_number", "?")
                        st.markdown(f"**Current Week (Week {week_num})**")

                        # Build HTML day-perf-grid
                        day_boxes_html = ""
                        for day_num in range(1, 7):
                            day_info = current_week_data["days"].get(day_num, {})
                            theme = day_info.get("theme", f"Day {day_num}")
                            points = day_info.get("points")
                            display_theme = short_themes.get(theme, theme)
                            pts_str = format_points(points)

                            rank_html = ""
                            color_class = ""
                            if points is not None:
                                day_scores = []
                                for pid, pdata in all_current_week.items():
                                    if day_num in pdata:
                                        day_scores.append((pid, pdata[day_num]))
                                day_scores.sort(key=lambda x: x[1], reverse=True)
                                total_players = len(day_scores)
                                rank = None
                                for idx_r, (pid, _) in enumerate(day_scores):
                                    if pid == selected_player_id:
                                        rank = idx_r + 1
                                        break

                                status_color, status_icon = get_status_color_icon(points)
                                rank_str = get_rank_str(rank, total_players)
                                rank_html = (
                                    f'<div style="font-size:11px;color:{status_color};'
                                    f'margin-top:4px;">{status_icon}{rank_str}</div>'
                                )
                                if points >= 7_200_000:
                                    color_class = "green"
                                elif points >= 3_600_000:
                                    color_class = "amber"
                                else:
                                    color_class = "red"
                            else:
                                pts_str = "--"

                            day_boxes_html += (
                                f'<div class="day-box">'
                                f'<div class="day-label">{display_theme}</div>'
                                f'<div class="day-value {color_class}">{pts_str}</div>'
                                f"{rank_html}</div>"
                            )

                        st.markdown(
                            f'<div class="day-perf-grid">{day_boxes_html}</div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown("")  # Spacer

                    # === Cycle Total Section ===
                    if has_cycle_data:
                        cycle_num = cycle_data.get("cycle_number", "?")
                        weeks_in_cycle = cycle_data.get("weeks_in_cycle", 0)
                        st.markdown(f"**Cycle Total (Cycle {cycle_num})**")

                        # Build HTML day-perf-grid for cycle totals
                        cycle_boxes_html = ""
                        for day_num in range(1, 7):
                            day_info = cycle_data["day_totals"].get(day_num, {})
                            theme = day_info.get("theme", f"Day {day_num}")
                            total_pts = day_info.get("total_points", 0)
                            times_participated = day_info.get("times_participated", 0)
                            display_theme = short_themes.get(theme, theme)
                            pts_str = format_points(total_pts)

                            rank_html = ""
                            color_class = ""
                            if times_participated > 0:
                                day_scores = []
                                for pid, pdata in all_cycle_totals.items():
                                    if day_num in pdata:
                                        day_scores.append((pid, pdata[day_num]))
                                day_scores.sort(key=lambda x: x[1], reverse=True)
                                total_players = len(day_scores)
                                rank = None
                                for idx_r, (pid, _) in enumerate(day_scores):
                                    if pid == selected_player_id:
                                        rank = idx_r + 1
                                        break

                                status_color, status_icon = get_status_color_icon(total_pts)
                                rank_str = get_rank_str(rank, total_players)
                                wks_txt = f"{times_participated}/{weeks_in_cycle} wks"
                                rank_html = (
                                    f'<div style="font-size:11px;color:{status_color};'
                                    f'margin-top:4px;">{status_icon}{rank_str}</div>'
                                    f'<div style="font-size:10px;color:#6b7280;'
                                    f'margin-top:2px;">{wks_txt}</div>'
                                )
                                if total_pts >= 7_200_000:
                                    color_class = "green"
                                elif total_pts >= 3_600_000:
                                    color_class = "amber"
                                else:
                                    color_class = "red"
                            else:
                                pts_str = "--"

                            cycle_boxes_html += (
                                f'<div class="day-box">'
                                f'<div class="day-label">{display_theme}</div>'
                                f'<div class="day-value {color_class}">{pts_str}</div>'
                                f"{rank_html}</div>"
                            )

                        st.markdown(
                            f'<div class="day-perf-grid">{cycle_boxes_html}</div>',
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("No daily performance data available.")

                # === Recent Weeks Table ===
                st.markdown("---")
                st.markdown(
                    render_section_header("Recent Weeks Performance"),
                    unsafe_allow_html=True,
                )

                recent_weeks = get_recent_weeks(count=4)
                if recent_weeks:
                    from src.data.models import DuelWeeklyStats

                    week_data = []
                    for week in recent_weeks:
                        week_stats = (
                            session.query(DuelWeeklyStats)
                            .filter(
                                DuelWeeklyStats.week_id == week.id,
                                DuelWeeklyStats.player_id == selected_player_id,
                            )
                            .first()
                        )
                        if week_stats:
                            week_data.append(
                                {
                                    "Week": f"Week {week.week_number}",
                                    "Opponent": week.opponent_name or "TBD",
                                    "Result": (week.result or "pending").upper(),
                                    "Points": f"{week_stats.raw_points:,.0f}",
                                    "Days": week_stats.days_participated,
                                    "Normalized": f"{week_stats.normalized_points:.1f}",
                                }
                            )
                        else:
                            week_data.append(
                                {
                                    "Week": f"Week {week.week_number}",
                                    "Opponent": week.opponent_name or "TBD",
                                    "Result": (week.result or "pending").upper(),
                                    "Points": "-",
                                    "Days": "-",
                                    "Normalized": "-",
                                }
                            )

                    if week_data:
                        df = pd.DataFrame(week_data)
                        st.dataframe(df, hide_index=True, use_container_width=True)
                    else:
                        st.info("No recent week data available.")
                else:
                    st.info("No duel weeks recorded yet.")

                # === Export Player Card Section ===
                st.markdown("---")
                st.subheader("Export Player Card")

                from src.dashboard.exports import (
                    PlayerCardData,
                    generate_player_card_gif,
                    generate_player_card_png,
                )

                # Build card data from existing variables
                # Prepare current week data with ranks
                export_current_week_data = {}
                if has_current_week_data:
                    export_days = {}
                    for day_num in range(1, 7):
                        day_info = current_week_data["days"].get(day_num, {})
                        points = day_info.get("points")
                        rank = None
                        total_players = 0
                        if points is not None:
                            day_scores = []
                            for pid, pdata in all_current_week.items():
                                if day_num in pdata:
                                    day_scores.append((pid, pdata[day_num]))
                            day_scores.sort(key=lambda x: x[1], reverse=True)
                            total_players = len(day_scores)
                            for idx, (pid, _) in enumerate(day_scores):
                                if pid == selected_player_id:
                                    rank = idx + 1
                                    break
                        export_days[day_num] = {
                            "theme": day_info.get("theme", f"Day {day_num}"),
                            "points": points,
                            "rank": rank,
                            "total": total_players,
                        }
                    export_current_week_data = {
                        "week_number": current_week_data.get("week_number", "?"),
                        "days": export_days,
                    }

                # Prepare cycle data with ranks
                export_cycle_data = None
                if has_cycle_data:
                    export_day_totals = {}
                    for day_num in range(1, 7):
                        day_info = cycle_data["day_totals"].get(day_num, {})
                        total_pts = day_info.get("total_points", 0)
                        times_participated = day_info.get("times_participated", 0)
                        rank = None
                        total_players = 0
                        if times_participated > 0:
                            day_scores = []
                            for pid, pdata in all_cycle_totals.items():
                                if day_num in pdata:
                                    day_scores.append((pid, pdata[day_num]))
                            day_scores.sort(key=lambda x: x[1], reverse=True)
                            total_players = len(day_scores)
                            for idx, (pid, _) in enumerate(day_scores):
                                if pid == selected_player_id:
                                    rank = idx + 1
                                    break
                        export_day_totals[day_num] = {
                            "theme": day_info.get("theme", f"Day {day_num}"),
                            "total_points": total_pts,
                            "times_participated": times_participated,
                            "rank": rank,
                            "total_players": total_players,
                        }
                    export_cycle_data = {
                        "cycle_number": cycle_data.get("cycle_number", "?"),
                        "weeks_in_cycle": cycle_data.get("weeks_in_cycle", 0),
                        "day_totals": export_day_totals,
                    }

                # Prepare recent weeks data
                export_recent_weeks = []
                if recent_weeks:
                    for week in recent_weeks:
                        week_stats = (
                            session.query(DuelWeeklyStats)
                            .filter(
                                DuelWeeklyStats.week_id == week.id,
                                DuelWeeklyStats.player_id == selected_player_id,
                            )
                            .first()
                        )
                        points_str = f"{week_stats.raw_points:,.0f}" if week_stats else "-"
                        export_recent_weeks.append(
                            {
                                "week": f"Week {week.week_number}",
                                "opponent": week.opponent_name or "TBD",
                                "result": (week.result or "pending").upper(),
                                "points": points_str,
                            }
                        )

                card_data = PlayerCardData(
                    player_name=player.name,
                    player_rank=player.rank,
                    tier=tier,
                    reliability=reliability,
                    avg_normalized=avg_normalized,
                    is_active=player.is_active,
                    officer_role=player.officer_role,
                    power=player.power,
                    level=player.level,
                    kill_count=player.kill_count,
                    current_week_data=export_current_week_data,
                    cycle_data=export_cycle_data,
                    recent_weeks=export_recent_weeks,
                )

                export_cols = st.columns(2)
                with export_cols[0]:
                    png_bytes = generate_player_card_png(card_data)
                    st.download_button(
                        label="Download PNG",
                        data=png_bytes,
                        file_name=f"player_card_{player.name.replace(' ', '_')}.png",
                        mime="image/png",
                    )
                with export_cols[1]:
                    gif_bytes = generate_player_card_gif(card_data)
                    st.download_button(
                        label="Download Animated GIF",
                        data=gif_bytes,
                        file_name=f"player_card_{player.name.replace(' ', '_')}.gif",
                        mime="image/gif",
                    )

                # === Placeholder Sections (Coming Soon) ===
                st.markdown("---")
                st.subheader("Coming Soon")

                placeholder_cols = st.columns(2)
                with placeholder_cols[0]:
                    st.info(
                        "**Resource Donations**\n\n"
                        "Track alliance resource contributions and donation history."
                    )
                    st.info(
                        "**Rally/Titan Participation**\n\n"
                        "Monitor participation in rallies and titan battles."
                    )
                with placeholder_cols[1]:
                    st.info(
                        "**Achievement Badges**\n\n"
                        "Earn badges for milestones and exceptional performance."
                    )
                    st.info(
                        "**Recent Activity Log**\n\nView recent actions and contributions timeline."
                    )

elif page == "Import Members":
    st.header("Add Members")

    # Show current member count
    active_count = get_active_member_count()
    st.metric("Active Members", f"{active_count}/{ALLIANCE_MEMBER_LIMIT}")

    st.markdown("Enter member data using comma-separated format for fast entry.")

    import pandas as pd

    VALID_OFFICER_ROLES = {"leader", "warlord", "recruiter", "muse", "butler"}

    def parse_member_line(line: str) -> dict | str:
        """Parse a single line of member data.

        Format: Name, Rank, Officer, Power(M), Level
        Example: Cafeh, 4, None, 145.2, 30

        Returns dict on success, error string on failure.
        """
        line = line.strip()
        if not line:
            return "Empty line"

        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 5:
            return f"Expected 5 fields, got {len(parts)}"

        name, rank_str, officer_str, power_str, level_str = parts

        # Validate name
        if not name or len(name) < 1:
            return "Name is required"

        # Validate rank (1-5)
        try:
            rank = int(rank_str)
            if rank < 1 or rank > 5:
                return f"Rank must be 1-5, got {rank}"
        except ValueError:
            return f"Invalid rank: {rank_str}"

        # Validate officer role
        officer = officer_str.strip()
        if officer.lower() in ("none", "-", ""):
            officer = None
        elif officer.lower() not in VALID_OFFICER_ROLES:
            return f"Invalid officer: {officer}. Valid: Leader/Warlord/Recruiter/Muse/Butler/None"
        else:
            # Normalize capitalization
            officer = officer.capitalize()

        # Validate power
        try:
            power = float(power_str)
            if power < 0:
                return f"Power must be positive, got {power}"
        except ValueError:
            return f"Invalid power: {power_str}"

        # Validate level
        try:
            level = int(level_str)
            if level < 1 or level > 35:
                return f"Level must be 1-35, got {level}"
        except ValueError:
            return f"Invalid level: {level_str}"

        return {
            "name": name,
            "rank": rank,
            "officer": officer,
            "power": power,
            "level": level,
        }

    st.markdown("**Format:** `Name, Rank, Officer, Power(M), Level`")
    st.markdown("**Example:** `Cafeh, 4, None, 145.2, 30`")
    st.markdown("**Officer roles:** Leader, Warlord, Recruiter, Muse, Butler, or None")

    # Text area for bulk input
    input_text = st.text_area(
        "Quick Add (one member per line):",
        height=200,
        placeholder="Cafeh, 4, None, 145.2, 30\nLolcks, 4, None, 100.5, 30\n"
        "The Bear, 4, Butler, 109.5, 30",
    )

    # Parse button
    if st.button("Parse & Preview"):
        if input_text.strip():
            lines = input_text.strip().split("\n")
            parsed_members = []
            errors = []

            for i, line in enumerate(lines, 1):
                if not line.strip():
                    continue
                result = parse_member_line(line)
                if isinstance(result, str):
                    errors.append(f"Line {i}: {result}")
                else:
                    parsed_members.append(result)

            # Store in session state
            st.session_state["parsed_members"] = parsed_members
            st.session_state["parse_errors"] = errors
        else:
            st.warning("Please enter member data first.")

    # Display errors if any
    if "parse_errors" in st.session_state and st.session_state["parse_errors"]:
        st.error("**Errors found:**")
        for err in st.session_state["parse_errors"]:
            st.text(f"  {err}")

    # Display preview table
    if "parsed_members" in st.session_state and st.session_state["parsed_members"]:
        st.markdown("---")
        st.subheader("Preview")

        preview_data = []
        for m in st.session_state["parsed_members"]:
            preview_data.append(
                {
                    "Name": m["name"],
                    "Rank": f"R{m['rank']}",
                    "Officer": m["officer"] if m["officer"] else "-",
                    "Power": f"{m['power']:.1f}M",
                    "Level": m["level"],
                }
            )

        df = pd.DataFrame(preview_data)
        st.dataframe(df, hide_index=True, use_container_width=True)

        st.markdown(f"**{len(preview_data)} members** ready to import")

        # Check member limit before import
        current_active = get_active_member_count()
        new_total = current_active + len(preview_data)
        if new_total > ALLIANCE_MEMBER_LIMIT:
            st.error(
                f"Cannot import {len(preview_data)} member(s). "
                f"Would exceed {ALLIANCE_MEMBER_LIMIT} member limit "
                f"({current_active} active + {len(preview_data)} = {new_total}). "
                f"You can import up to {ALLIANCE_MEMBER_LIMIT - current_active} more members."
            )
        else:
            # Import button
            if st.button("Import Members", type="primary"):
                try:
                    from src.data.models import Player
                    from src.data.storage import get_session, init_database

                    init_database()

                    with get_session() as session:
                        imported = 0
                        for m in st.session_state["parsed_members"]:
                            player = Player(
                                name=m["name"],
                                rank=m["rank"],
                                officer_role=m["officer"],
                                power=m["power"],
                                level=m["level"],
                            )
                            session.add(player)
                            imported += 1
                        session.commit()

                    st.success(f"Successfully imported {imported} members!")
                    # Clear session state
                    del st.session_state["parsed_members"]
                    if "parse_errors" in st.session_state:
                        del st.session_state["parse_errors"]
                    st.balloons()
                except Exception as e:
                    st.error(f"Error importing members: {e}")

    # ── Update Members section ────────────────────────────────────────
    st.markdown("---")
    st.subheader("Update Members")
    st.markdown(
        "Paste bulk data to update **Rank** and **Power** for existing members.\n\n"
        "**Format:** `Name, Rank, Power` — one per line"
    )

    def parse_update_line(line: str) -> dict | str:
        """Parse a single update line: Name, Rank, Power.

        Returns dict on success, error string on failure.
        """
        line = line.strip()
        if not line:
            return "Empty line"

        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3:
            return f"Expected 3 fields (Name, Rank, Power), got {len(parts)}"

        name, rank_str, power_str = parts

        if not name:
            return "Name is required"

        try:
            rank = int(rank_str)
            if rank < 1 or rank > 5:
                return f"Rank must be 1-5, got {rank}"
        except ValueError:
            return f"Invalid rank: {rank_str}"

        try:
            power = float(power_str)
            if power < 0:
                return f"Power must be >= 0, got {power}"
        except ValueError:
            return f"Invalid power: {power_str}"

        return {"name": name, "rank": rank, "power": power}

    update_input = st.text_area(
        "Bulk Update (one member per line):",
        height=200,
        placeholder="Cafeh, 4, 145200000\nLolcks, 3, 100500000\nThe Bear, 4, 109500000",
        key="update_input",
    )

    if st.button("Parse & Match", key="update_parse_btn"):
        if not update_input.strip():
            st.warning("Please enter update data first.")
        else:
            lines = update_input.strip().split("\n")
            parsed_entries: list[dict] = []
            parse_errors: list[str] = []

            for i, line in enumerate(lines, 1):
                if not line.strip():
                    continue
                result = parse_update_line(line)
                if isinstance(result, str):
                    parse_errors.append(f"Line {i}: {result}")
                else:
                    parsed_entries.append(result)

            # Fetch active players for matching
            stats = get_player_stats(active_only=True)
            active_players = stats["players"]  # (id, name, rank, officer, power, level)

            # Build lookup: lowercase name -> player tuple
            name_lookup: dict[str, tuple] = {}
            for p in active_players:
                name_lookup[p[1].strip().lower()] = p

            matched: list[dict] = []
            unmatched: list[dict] = []

            for entry in parsed_entries:
                key = entry["name"].strip().lower()
                if key in name_lookup:
                    p = name_lookup[key]
                    matched.append(
                        {
                            "player_id": p[0],
                            "player_name": p[1],
                            "new_rank": entry["rank"],
                            "new_power": entry["power"],
                            "old_rank": p[2],
                            "old_power": p[4],
                        }
                    )
                else:
                    unmatched.append(
                        {
                            "input_name": entry["name"],
                            "new_rank": entry["rank"],
                            "new_power": entry["power"],
                        }
                    )

            st.session_state["update_matched"] = matched
            st.session_state["update_unmatched"] = unmatched
            st.session_state["update_parse_errors"] = parse_errors

    # Show parse errors
    if st.session_state.get("update_parse_errors"):
        st.error("**Parse errors:**")
        for err in st.session_state["update_parse_errors"]:
            st.text(f"  {err}")

    # Show matched preview
    if st.session_state.get("update_matched"):
        st.markdown("#### Matched Members")
        preview_rows = []
        for m in st.session_state["update_matched"]:
            preview_rows.append(
                {
                    "Name": m["player_name"],
                    "Old Rank": f"R{m['old_rank']}",
                    "New Rank": f"R{m['new_rank']}",
                    "Old Power": format_power_m(m["old_power"]),
                    "New Power": format_power_m(m["new_power"]),
                }
            )
        st.dataframe(pd.DataFrame(preview_rows), hide_index=True, use_container_width=True)

    # Show unmatched entries with fix-it selectboxes
    if st.session_state.get("update_unmatched"):
        st.markdown("#### Unmatched Entries")
        st.warning(
            f"{len(st.session_state['update_unmatched'])} name(s) could not be matched. "
            "Use the dropdowns below to pick the correct player, or choose **Skip**."
        )

        # Build list of already-matched player IDs
        matched_ids = {m["player_id"] for m in st.session_state.get("update_matched", [])}

        # Get active players for the selectbox options
        stats = get_player_stats(active_only=True)
        available_players = [p for p in stats["players"] if p[0] not in matched_ids]
        player_options = ["Skip"] + [
            f"{p[1]} (R{p[2]}, {format_power_m(p[4])})" for p in available_players
        ]

        for idx, entry in enumerate(st.session_state["update_unmatched"]):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(
                    f"**{entry['input_name']}** → R{entry['new_rank']}, "
                    f"{format_power_m(entry['new_power'])}"
                )
            with col2:
                st.selectbox(
                    f"Match for '{entry['input_name']}'",
                    options=player_options,
                    key=f"update_fix_{idx}",
                    label_visibility="collapsed",
                )

        if st.button("Apply Matches", key="update_apply_matches"):
            newly_matched = []
            still_unmatched = []

            for idx, entry in enumerate(st.session_state["update_unmatched"]):
                selection = st.session_state.get(f"update_fix_{idx}", "Skip")
                if selection == "Skip":
                    # Skip — drop this entry
                    continue
                # Find the player from available_players by matching the label
                for p in available_players:
                    label = f"{p[1]} (R{p[2]}, {format_power_m(p[4])})"
                    if label == selection:
                        newly_matched.append(
                            {
                                "player_id": p[0],
                                "player_name": p[1],
                                "new_rank": entry["new_rank"],
                                "new_power": entry["new_power"],
                                "old_rank": p[2],
                                "old_power": p[4],
                            }
                        )
                        break
                else:
                    still_unmatched.append(entry)

            # Merge newly matched into matched list
            current_matched = st.session_state.get("update_matched", [])
            current_matched.extend(newly_matched)
            st.session_state["update_matched"] = current_matched
            st.session_state["update_unmatched"] = still_unmatched

            # Clean up selectbox keys
            cleanup_count = len(st.session_state.get("update_unmatched", [])) + len(newly_matched)
            for idx in range(cleanup_count):
                key = f"update_fix_{idx}"
                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()

    # Update button — only when there are matched entries and no unmatched remain
    if st.session_state.get("update_matched") and not st.session_state.get("update_unmatched"):
        st.markdown("---")
        st.markdown(f"**{len(st.session_state['update_matched'])} member(s)** ready to update.")

        if st.button("Update Members", type="primary", key="update_members_btn"):
            try:
                from src.data.models import Player
                from src.data.storage import get_session, init_database

                init_database()

                with get_session() as session:
                    updated = 0
                    for m in st.session_state["update_matched"]:
                        player = session.query(Player).get(m["player_id"])
                        if player:
                            player.rank = m["new_rank"]
                            player.power = m["new_power"]
                            updated += 1
                    session.commit()

                st.success(f"Successfully updated {updated} member(s)!")

                # Clear session state
                for key in [
                    "update_matched",
                    "update_unmatched",
                    "update_parse_errors",
                ]:
                    if key in st.session_state:
                        del st.session_state[key]

                st.rerun()
            except Exception as e:
                st.error(f"Error updating members: {e}")

elif page == "Update Kills":
    st.header("Update Kill Counts")

    from datetime import datetime

    import pandas as pd

    from src.data.models import KillHistory, KillImport, Player
    from src.data.storage import get_session, init_database

    init_database()

    # Show current total kills
    total_kills = get_total_alliance_kills()
    st.metric("Total Alliance Kills", f"{total_kills:,}")

    # --- Previous Imports Section ---
    st.markdown("---")
    st.subheader("Previous Imports")

    with get_session() as session:
        imports = session.query(KillImport).order_by(KillImport.recorded_at.desc()).all()
        if imports:
            import_data = []
            for imp in imports:
                import_data.append(
                    {
                        "id": imp.id,
                        "Label": imp.label,
                        "Date": imp.recorded_at.strftime("%Y-%m-%d %H:%M"),
                        "Players": imp.player_count,
                        "Created": imp.created_at.strftime("%Y-%m-%d %H:%M"),
                    }
                )

            # Display imports table with delete buttons
            for imp_row in import_data:
                col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 2, 1])
                with col1:
                    st.text(imp_row["Label"])
                with col2:
                    st.text(imp_row["Date"])
                with col3:
                    st.text(str(imp_row["Players"]))
                with col4:
                    st.text(imp_row["Created"])
                with col5:
                    if st.button("Delete", key=f"del_import_{imp_row['id']}"):
                        st.session_state["delete_import_id"] = imp_row["id"]
                        st.session_state["delete_import_label"] = imp_row["Label"]

            # Delete confirmation dialog
            if st.session_state.get("delete_import_id"):
                st.warning(
                    f"Are you sure you want to delete import "
                    f"'{st.session_state['delete_import_label']}'? "
                    "This will remove all associated kill history records."
                )
                confirm_label = st.text_input(
                    "Type the import label to confirm deletion:",
                    key="delete_confirm_label",
                )
                col_confirm, col_cancel = st.columns(2)
                with col_confirm:
                    if st.button("Confirm Delete", type="primary"):
                        if confirm_label == st.session_state["delete_import_label"]:
                            with get_session() as del_session:
                                import_to_delete = del_session.query(KillImport).get(
                                    st.session_state["delete_import_id"]
                                )
                                if import_to_delete:
                                    del_session.delete(import_to_delete)
                                    del_session.commit()
                                    st.success("Import deleted successfully!")
                            # Clear state
                            del st.session_state["delete_import_id"]
                            del st.session_state["delete_import_label"]
                            if "delete_confirm_label" in st.session_state:
                                del st.session_state["delete_confirm_label"]
                            st.rerun()
                        else:
                            st.error("Label does not match. Deletion cancelled.")
                with col_cancel:
                    if st.button("Cancel"):
                        del st.session_state["delete_import_id"]
                        del st.session_state["delete_import_label"]
                        if "delete_confirm_label" in st.session_state:
                            del st.session_state["delete_confirm_label"]
                        st.rerun()
        else:
            st.info("No previous imports found.")

    # --- New Import Section ---
    st.markdown("---")
    st.subheader("New Import")

    # Import label and date inputs
    col_label, col_date, col_time = st.columns([3, 1, 1])
    with col_label:
        default_label = f"Import {datetime.now().strftime('%Y-%m-%d')}"
        import_label = st.text_input(
            "Import Label:",
            value=default_label,
            placeholder="Week 12 snapshot",
            key="import_label",
        )
    with col_date:
        import_date = st.date_input(
            "Record Date:",
            value=datetime.now().date(),
            key="import_date",
        )
    with col_time:
        import_time = st.time_input(
            "Time:",
            value=datetime.now().time().replace(second=0, microsecond=0),
            key="import_time",
        )

    # Warn if future date
    import_datetime = datetime.combine(import_date, import_time)
    if import_datetime > datetime.now():
        st.warning("Selected date/time is in the future.")

    st.markdown(
        "Paste kill count data to update player kill counts.\n\n"
        "**Format:** `Name, Kills` — one per line"
    )

    def parse_kill_line(line: str) -> dict | str:
        """Parse a single kill update line: Name, Kills.

        Returns dict on success, error string on failure.
        """
        line = line.strip()
        if not line:
            return "Empty line"

        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 2:
            return f"Expected 2 fields (Name, Kills), got {len(parts)}"

        name, kills_str = parts

        if not name:
            return "Name is required"

        try:
            kills = int(kills_str.replace(",", ""))
            if kills < 0:
                return f"Kills must be >= 0, got {kills}"
        except ValueError:
            return f"Invalid kills: {kills_str}"

        return {"name": name, "kills": kills}

    kills_input = st.text_area(
        "Kill Data (one member per line):",
        height=200,
        placeholder="Cafeh, 1234567\nLolcks, 987654\nThe Bear, 555000",
        key="kills_input",
    )

    if st.button("Parse & Match", key="kills_parse_btn"):
        if not kills_input.strip():
            st.warning("Please enter kill data first.")
        else:
            lines = kills_input.strip().split("\n")
            parsed_entries: list[dict] = []
            parse_errors: list[str] = []

            for i, line in enumerate(lines, 1):
                if not line.strip():
                    continue
                result = parse_kill_line(line)
                if isinstance(result, str):
                    parse_errors.append(f"Line {i}: {result}")
                else:
                    parsed_entries.append(result)

            # Fetch active players for matching
            stats = get_player_stats(active_only=True)
            active_players = stats["players"]  # (id, name, rank, officer, power, level)

            # Get kill counts for active players
            with get_session() as session:
                player_kills = {}
                for p in active_players:
                    player = session.query(Player).filter(Player.id == p[0]).first()
                    if player:
                        player_kills[p[0]] = player.kill_count

            # Build lookup: lowercase name -> player tuple
            name_lookup: dict[str, tuple] = {}
            for p in active_players:
                name_lookup[p[1].strip().lower()] = p

            matched: list[dict] = []
            unmatched: list[dict] = []

            for entry in parsed_entries:
                key = entry["name"].strip().lower()
                if key in name_lookup:
                    p = name_lookup[key]
                    old_kills = player_kills.get(p[0], 0)
                    matched.append(
                        {
                            "player_id": p[0],
                            "player_name": p[1],
                            "new_kills": entry["kills"],
                            "old_kills": old_kills,
                        }
                    )
                else:
                    unmatched.append(
                        {
                            "input_name": entry["name"],
                            "new_kills": entry["kills"],
                        }
                    )

            st.session_state["kills_matched"] = matched
            st.session_state["kills_unmatched"] = unmatched
            st.session_state["kills_parse_errors"] = parse_errors

    # Show parse errors
    if st.session_state.get("kills_parse_errors"):
        st.error("**Parse errors:**")
        for err in st.session_state["kills_parse_errors"]:
            st.text(f"  {err}")

    # Show matched preview
    if st.session_state.get("kills_matched"):
        st.markdown("#### Matched Members")
        preview_rows = []
        for m in st.session_state["kills_matched"]:
            change = m["new_kills"] - m["old_kills"]
            change_str = f"+{change:,}" if change >= 0 else f"{change:,}"
            preview_rows.append(
                {
                    "Name": m["player_name"],
                    "Old Kills": f"{m['old_kills']:,}",
                    "New Kills": f"{m['new_kills']:,}",
                    "Change": change_str,
                }
            )
        st.dataframe(pd.DataFrame(preview_rows), hide_index=True, use_container_width=True)

    # Show unmatched entries with fix-it selectboxes
    if st.session_state.get("kills_unmatched"):
        st.markdown("#### Unmatched Entries")
        st.warning(
            f"{len(st.session_state['kills_unmatched'])} name(s) could not be matched. "
            "Use the dropdowns below to pick the correct player, or choose **Skip**."
        )

        # Build list of already-matched player IDs
        matched_ids = {m["player_id"] for m in st.session_state.get("kills_matched", [])}

        # Get active players for the selectbox options
        stats = get_player_stats(active_only=True)
        available_players = [p for p in stats["players"] if p[0] not in matched_ids]
        player_options = ["Skip"] + [
            f"{p[1]} (R{p[2]}, {format_power_m(p[4])})" for p in available_players
        ]

        for idx, entry in enumerate(st.session_state["kills_unmatched"]):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**{entry['input_name']}** → {entry['new_kills']:,} kills")
            with col2:
                st.selectbox(
                    f"Match for '{entry['input_name']}'",
                    options=player_options,
                    key=f"kills_fix_{idx}",
                    label_visibility="collapsed",
                )

        if st.button("Apply Matches", key="kills_apply_matches"):
            # Get kill counts for matching
            with get_session() as session:
                player_kills = {}
                for p in available_players:
                    player = session.query(Player).filter(Player.id == p[0]).first()
                    if player:
                        player_kills[p[0]] = player.kill_count

            newly_matched = []

            for idx, entry in enumerate(st.session_state["kills_unmatched"]):
                selection = st.session_state.get(f"kills_fix_{idx}", "Skip")
                if selection == "Skip":
                    continue
                # Find the player from available_players by matching the label
                for p in available_players:
                    label = f"{p[1]} (R{p[2]}, {format_power_m(p[4])})"
                    if label == selection:
                        old_kills = player_kills.get(p[0], 0)
                        newly_matched.append(
                            {
                                "player_id": p[0],
                                "player_name": p[1],
                                "new_kills": entry["new_kills"],
                                "old_kills": old_kills,
                            }
                        )
                        break

            # Merge newly matched into matched list
            current_matched = st.session_state.get("kills_matched", [])
            current_matched.extend(newly_matched)
            st.session_state["kills_matched"] = current_matched
            st.session_state["kills_unmatched"] = []

            # Clean up selectbox keys
            cleanup_count = len(st.session_state.get("kills_unmatched", [])) + len(newly_matched)
            for idx in range(cleanup_count):
                key = f"kills_fix_{idx}"
                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()

    # Update button — only when there are matched entries and no unmatched remain
    if st.session_state.get("kills_matched") and not st.session_state.get("kills_unmatched"):
        st.markdown("---")
        st.markdown(f"**{len(st.session_state['kills_matched'])} member(s)** ready to update.")

        if st.button("Update Kills", type="primary", key="update_kills_btn"):
            # Validate import label
            label = st.session_state.get("import_label", "").strip()
            if not label:
                st.error("Import label is required.")
            else:
                try:
                    # Get import date/time from session state
                    record_date = st.session_state.get("import_date", datetime.now().date())
                    record_time = st.session_state.get(
                        "import_time", datetime.now().time().replace(second=0, microsecond=0)
                    )
                    record_datetime = datetime.combine(record_date, record_time)

                    with get_session() as session:
                        # Create the import batch record
                        kill_import = KillImport(
                            label=label,
                            recorded_at=record_datetime,
                            player_count=len(st.session_state["kills_matched"]),
                        )
                        session.add(kill_import)
                        session.flush()  # Get the import ID

                        updated = 0
                        now = datetime.now()
                        for m in st.session_state["kills_matched"]:
                            player = session.query(Player).get(m["player_id"])
                            if player:
                                # Create history record linked to import
                                history = KillHistory(
                                    player_id=player.id,
                                    kill_count=m["new_kills"],
                                    recorded_at=record_datetime,
                                    import_id=kill_import.id,
                                )
                                session.add(history)

                                # Update player
                                player.kill_count = m["new_kills"]
                                player.kill_count_updated_at = record_datetime
                                updated += 1
                        session.commit()

                    st.success(f"Successfully updated {updated} member(s)!")

                    # Clear session state
                    for key in [
                        "kills_matched",
                        "kills_unmatched",
                        "kills_parse_errors",
                        "import_label",
                        "import_date",
                        "import_time",
                    ]:
                        if key in st.session_state:
                            del st.session_state[key]

                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating kills: {e}")

elif page == "Duel VS":
    st.markdown(render_section_header("Duel VS Tracker"), unsafe_allow_html=True)

    import pandas as pd
    import plotly.express as px

    # Performance thresholds for daily breakdown pie charts
    DAILY_TARGET_THRESHOLD = 7_200_000  # 7.2M - Target Performance
    DAILY_BELOW_TARGET_THRESHOLD = 3_600_000  # 3.6M - Below Target threshold

    from src.data.duel_tracker import (
        TIER_THRESHOLDS,
        aggregate_cycle_stats,
        aggregate_daily_to_weekly,
        assign_week_to_cycle,
        create_cycle,
        create_week,
        delete_daily_stats_for_day,
        get_all_cycles,
        get_cycle_report,
        get_daily_stats_for_day,
        get_day,
        get_recent_weeks,
        get_rolling_report,
        get_text_summary,
        get_week_daily_breakdown,
        get_weekly_report,
        import_daily_simple_csv,
        import_weekly_csv,
        parse_daily_simple_csv,
        record_daily_stats,
        set_week_result,
    )
    from src.data.models import DUEL_DAY_THEMES
    from src.data.storage import get_session, init_database

    init_database()

    duel_view = st.selectbox(
        "Select View",
        [
            "Rolling Report",
            "Weekly Report",
            "Cycle Report",
            "Import Weekly",
            "Import Daily",
            "Daily Breakdown",
            "Manage Weeks",
        ],
        key="duel_view",
    )

    if duel_view == "Rolling Report":
        st.subheader("4-Week Rolling Report")

        rolling = get_rolling_report(weeks=4)

        if rolling:
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                tier_filter = st.multiselect(
                    "Filter by Tier",
                    ["Core", "Strong", "Standard", "Probation"],
                    default=["Core", "Strong", "Standard", "Probation"],
                )
            with col2:
                show_inactive = st.checkbox("Show inactive players (0 weeks)", value=False)

            # Filter data
            filtered = [
                p
                for p in rolling
                if p["tier"] in tier_filter and (show_inactive or p["weeks_participated"] > 0)
            ]

            if filtered:
                df = pd.DataFrame(filtered)
                df = df.rename(
                    columns={
                        "player_name": "Player",
                        "weeks_participated": "Weeks",
                        "total_weeks": "Total",
                        "avg_raw_points": "Avg Pts",
                        "avg_normalized_points": "Avg Norm",
                        "reliability": "Reliability",
                        "tier": "Tier",
                    }
                )
                df = df[["Player", "Weeks", "Total", "Avg Pts", "Avg Norm", "Reliability", "Tier"]]
                df["Reliability"] = (df["Reliability"] * 100).astype(int).astype(str) + "%"

                # Color tiers
                def tier_color(tier):
                    colors = {
                        "Core": "#22c55e",
                        "Strong": "#3b82f6",
                        "Standard": "#eab308",
                        "Probation": "#ef4444",
                    }
                    return colors.get(tier, "#6c757d")

                st.dataframe(
                    df,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "Tier": st.column_config.TextColumn("Tier", width="small"),
                        "Reliability": st.column_config.TextColumn("Reliability", width="small"),
                    },
                )

                # Summary stats — tier count badges
                st.markdown("---")
                tier_counts = df["Tier"].value_counts()
                tier_badge_items = [
                    ("#22c55e", "Core", tier_counts.get("Core", 0)),
                    ("#3b82f6", "Strong", tier_counts.get("Strong", 0)),
                    ("#eab308", "Standard", tier_counts.get("Standard", 0)),
                    ("#ef4444", "Probation", tier_counts.get("Probation", 0)),
                ]
                badges_html = '<div style="display:flex;gap:16px;margin-bottom:20px;">'
                for dot_color, tier_name, count in tier_badge_items:
                    badges_html += (
                        f'<div style="display:flex;align-items:center;gap:6px;'
                        f'font-size:12px;font-weight:600;color:#9ca3af;">'
                        f'<div style="width:8px;height:8px;border-radius:50%;'
                        f'background:{dot_color};"></div>'
                        f"{tier_name} <strong style='color:#fff;'>{count}</strong></div>"
                    )
                badges_html += "</div>"
                st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.info("No players match the current filters.")
        else:
            st.info("No duel weeks recorded yet. Create a week and import stats to see the report.")

        # Show tier thresholds
        with st.expander("Tier Thresholds"):
            for tier, thresholds in TIER_THRESHOLDS.items():
                rel = thresholds["min_reliability"] * 100
                norm = thresholds["min_avg_normalized"]
                st.text(f"{tier}: Reliability >= {rel:.0f}%, Avg Norm >= {norm}")

    elif duel_view == "Weekly Report":
        st.subheader("Weekly Report")

        weeks = get_recent_weeks(count=10)
        if weeks:
            week_options = {}
            for w in weeks:
                opponent = w.opponent_name or "TBD"
                result = w.result or "pending"
                week_options[f"Week {w.week_number}: vs {opponent} ({result})"] = w.id
            selected_week = st.selectbox("Select Week", list(week_options.keys()))

            if selected_week:
                week_id = week_options[selected_week]
                report = get_weekly_report(week_id)

                if "error" not in report:
                    # Header
                    col1, col2 = st.columns(2)
                    with col1:
                        result = report["result"]
                        if result:
                            color = (
                                "#22c55e"
                                if result == "win"
                                else "#ef4444"
                                if result == "loss"
                                else "#eab308"
                            )
                            st.markdown(
                                f"**Result:** <span style='color:{color}'>{result.upper()}</span>",
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown("**Result:** Pending")
                    with col2:
                        st.metric("Participants", report["player_count"])

                    # Player stats table
                    if report["players"]:
                        df = pd.DataFrame(report["players"])
                        df = df.rename(
                            columns={
                                "player_name": "Player",
                                "raw_points": "Points",
                                "days_participated": "Days",
                                "normalized_points": "Normalized",
                                "kills_snapshot": "Kills",
                                "kills_gained": "Kill Growth",
                            }
                        )

                        # Format kills columns
                        df["Kills"] = df["Kills"].apply(
                            lambda x: f"{int(x):,}" if pd.notna(x) else "--"
                        )
                        df["Kill Growth"] = df["Kill Growth"].apply(
                            lambda x: f"+{int(x):,}"
                            if pd.notna(x) and x >= 0
                            else (f"{int(x):,}" if pd.notna(x) else "--")
                        )

                        df = df[["Player", "Points", "Days", "Normalized", "Kills", "Kill Growth"]]
                        df["Points"] = df["Points"].astype(int)
                        df["Normalized"] = df["Normalized"].round(1)

                        st.dataframe(df, hide_index=True, use_container_width=True)

                    # Text summary
                    with st.expander("Text Summary (copy/paste)"):
                        summary = get_text_summary(week_id)
                        st.code(summary, language=None)
        else:
            st.info("No duel weeks recorded yet.")

    elif duel_view == "Cycle Report":
        st.subheader("Cycle Report (4-Week Performance)")

        cycles = get_all_cycles()
        if cycles:
            cycle_options = {}
            for c in cycles:
                label = f"Cycle {c.cycle_number}"
                if c.name:
                    label += f": {c.name}"
                label += f" (started {c.start_date.strftime('%Y-%m-%d')})"
                cycle_options[label] = c.id
            selected_cycle = st.selectbox(
                "Select Cycle", list(cycle_options.keys()), key="cycle_report_select"
            )

            if selected_cycle:
                cycle_id = cycle_options[selected_cycle]
                report = get_cycle_report(cycle_id)

                if "error" not in report:
                    # Display cycle header with name
                    cycle_header = f"Cycle {report['cycle_number']}"
                    if report.get("name"):
                        cycle_header += f" - {report['name']}"
                    st.markdown(f"### {cycle_header}")

                    # Header metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Weeks in Cycle", report["week_count"])
                    with col2:
                        st.metric("Wins", report["wins"])
                    with col3:
                        st.metric("Losses", report["losses"])

                    # Weeks summary
                    if report["weeks"]:
                        st.markdown("---")
                        st.markdown("**Weeks in this Cycle**")
                        week_data = []
                        for w in report["weeks"]:
                            result_str = w["result"].upper() if w["result"] else "Pending"
                            week_data.append(
                                {
                                    "Week": w["week_number"],
                                    "Opponent": w["opponent_name"] or "TBD",
                                    "Result": result_str,
                                }
                            )
                        st.dataframe(
                            pd.DataFrame(week_data),
                            hide_index=True,
                            use_container_width=True,
                        )

                    # Player stats
                    if report["players"]:
                        st.markdown("---")
                        st.markdown("**Player Performance**")

                        player_df = pd.DataFrame(report["players"])
                        player_df = player_df.rename(
                            columns={
                                "player_name": "Player",
                                "total_points": "Total Pts",
                                "weeks_participated": "Weeks",
                                "avg_weekly_points": "Avg/Week",
                            }
                        )
                        player_df = player_df[["Player", "Total Pts", "Weeks", "Avg/Week"]]
                        player_df["Total Pts"] = player_df["Total Pts"].astype(int)

                        st.dataframe(player_df, hide_index=True, use_container_width=True)

                        # Summary
                        st.markdown("---")
                        full_participation = sum(
                            1
                            for p in report["players"]
                            if p["weeks_participated"] == report["week_count"]
                        )
                        st.markdown(
                            f"**{full_participation}/{report['player_count']}** players "
                            f"participated in all {report['week_count']} weeks"
                        )
                    else:
                        st.info(
                            "No player stats available. "
                            "Aggregate cycle stats from the Manage Weeks tab."
                        )
                else:
                    st.error(report["error"])
        else:
            st.info(
                "No cycles created yet. "
                "Go to the Manage Weeks tab to create a cycle and assign weeks to it."
            )

    elif duel_view == "Import Weekly":
        st.subheader("Import Weekly Stats")
        st.markdown("**CSV Format:** `Week,PlayerName,Points,DaysParticipated`")

        weeks = get_recent_weeks(count=10)
        if not weeks:
            st.warning("Create a duel week first before importing stats.")
        else:
            st.markdown(f"**Available weeks:** {', '.join([str(w.week_number) for w in weeks])}")

            csv_input = st.text_area(
                "Paste CSV data:",
                height=200,
                placeholder="Week,PlayerName,Points,DaysParticipated\n1,DragonSlayer,1200,7\n1,IronFist,1100,6",
            )

            if st.button("Import Stats", type="primary"):
                if csv_input.strip():
                    imported, errors = import_weekly_csv(csv_input.strip())
                    if errors:
                        st.error("Import failed:")
                        for err in errors:
                            st.text(f"  {err}")
                    else:
                        st.success(f"Successfully imported {imported} records!")
                        st.rerun()
                else:
                    st.warning("Please paste CSV data first.")

    elif duel_view == "Import Daily":
        st.subheader("Import Daily Stats")

        weeks = get_recent_weeks(count=10)
        if not weeks:
            st.warning("Create a duel week first before importing stats.")
        else:
            # Week and Day selection (shared at top)
            col1, col2 = st.columns(2)
            with col1:
                week_options = {
                    f"Week {w.week_number}: vs {w.opponent_name or 'TBD'}": w.id for w in weeks
                }
                selected_week = st.selectbox(
                    "Select Week", list(week_options.keys()), key="daily_import_week"
                )
            with col2:
                day_options = {
                    f"Day {num} - {theme}": num for num, theme in DUEL_DAY_THEMES.items()
                }
                selected_day = st.selectbox(
                    "Select Day", list(day_options.keys()), key="daily_import_day"
                )

            week_id = week_options[selected_week]
            day_number = day_options[selected_day]

            # Get the day object and existing stats
            day = get_day(week_id, day_number)
            existing_stats = []
            if day:
                existing_stats = get_daily_stats_for_day(day.id)

            has_existing = len(existing_stats) > 0

            # --- Section 1: Existing Records ---
            with st.expander(
                f"Existing Records ({len(existing_stats)} players)", expanded=has_existing
            ):
                if existing_stats:
                    import pandas as pd

                    # Create editable dataframe
                    df = pd.DataFrame(existing_stats)
                    df = df.rename(columns={"player_name": "Player", "points": "Points"})

                    edited_df = st.data_editor(
                        df[["Player", "Points"]],
                        column_config={
                            "Player": st.column_config.TextColumn("Player", disabled=True),
                            "Points": st.column_config.NumberColumn(
                                "Points", min_value=0, format="%.0f"
                            ),
                        },
                        hide_index=True,
                        use_container_width=True,
                        key="daily_stats_editor",
                    )

                    if st.button("Save Changes", key="save_daily_edits"):
                        # Find changes and update
                        changes = 0
                        for idx, row in edited_df.iterrows():
                            original = existing_stats[idx]
                            if row["Points"] != original["points"]:
                                record_daily_stats(
                                    day_id=day.id,
                                    player_id=original["player_id"],
                                    points=row["Points"],
                                )
                                changes += 1
                        if changes > 0:
                            st.success(f"Updated {changes} record(s)!")
                            st.rerun()
                        else:
                            st.info("No changes detected.")
                else:
                    st.info("No records for this day yet.")

            # --- Section 2: Import New Data ---
            with st.expander("Import New Data", expanded=not has_existing):
                st.markdown("**CSV Format:** `PlayerName,Points`")

                daily_csv_input = st.text_area(
                    "Paste daily CSV data:",
                    height=150,
                    placeholder="PlayerName,Points\nDragonSlayer,200\nIronFist,150\nShadowKnight,180",
                    key="daily_csv_input",
                )

                # Initialize session state for preview
                if "import_preview" not in st.session_state:
                    st.session_state.import_preview = None
                if "import_preview_key" not in st.session_state:
                    st.session_state.import_preview_key = None

                # Current key for preview cache
                preview_key = f"{week_id}_{day_number}_{hash(daily_csv_input)}"

                col_preview, col_confirm = st.columns(2)
                with col_preview:
                    if st.button("Preview Import", key="preview_daily_import"):
                        if daily_csv_input.strip():
                            records, errors = parse_daily_simple_csv(
                                week_id, day_number, daily_csv_input.strip()
                            )
                            if errors:
                                st.error("Validation errors:")
                                for err in errors:
                                    st.text(f"  {err}")
                                st.session_state.import_preview = None
                            else:
                                st.session_state.import_preview = records
                                st.session_state.import_preview_key = preview_key
                        else:
                            st.warning("Please paste CSV data first.")

                # Show preview comparison if available and still valid
                if (
                    st.session_state.import_preview
                    and st.session_state.import_preview_key == preview_key
                ):
                    import pandas as pd

                    preview_records = st.session_state.import_preview

                    # Build comparison table
                    existing_map = {s["player_name"]: s["points"] for s in existing_stats}
                    comparison = []
                    for rec in preview_records:
                        existing_pts = existing_map.get(rec["player_name"])
                        change = ""
                        status = "New"
                        if existing_pts is not None:
                            diff = rec["points"] - existing_pts
                            change = f"{diff:+.0f}" if diff != 0 else "0"
                            status = "Update" if diff != 0 else "Same"
                        comparison.append(
                            {
                                "Player": rec["player_name"],
                                "Existing": existing_pts if existing_pts is not None else "-",
                                "New": rec["points"],
                                "Change": change if existing_pts is not None else "-",
                                "Status": status,
                            }
                        )

                    st.markdown("**Preview:**")
                    preview_df = pd.DataFrame(comparison)
                    st.dataframe(preview_df, hide_index=True, use_container_width=True)

                    with col_confirm:
                        if st.button("Confirm Import", type="primary", key="confirm_daily_import"):
                            imported, errors = import_daily_simple_csv(
                                week_id, day_number, daily_csv_input.strip()
                            )
                            if errors:
                                st.error("Import failed:")
                                for err in errors:
                                    st.text(f"  {err}")
                            else:
                                st.session_state.import_preview = None
                                st.success(f"Imported {imported} records for {selected_day}!")
                                st.rerun()

            # --- Section 3: Clear Day Data ---
            with st.expander("Clear Day Data", expanded=False):
                if has_existing and day:
                    st.warning(
                        f"This will permanently delete all {len(existing_stats)} records "
                        f"for Day {day_number}."
                    )
                    confirm_text = st.text_input(
                        f"Type `DELETE {day_number}` to confirm:",
                        key="confirm_delete_day",
                    )
                    if st.button("Delete All Records", type="secondary", key="delete_day_data"):
                        if confirm_text == f"DELETE {day_number}":
                            deleted = delete_daily_stats_for_day(day.id)
                            st.success(f"Deleted {deleted} records for Day {day_number}.")
                            st.rerun()
                        else:
                            st.error(f"Please type exactly: DELETE {day_number}")
                else:
                    st.info("No records to delete for this day.")

            # --- Aggregate Button at Bottom ---
            st.markdown("---")
            if st.button("Aggregate Daily to Weekly", key="aggregate_daily_weekly"):
                count = aggregate_daily_to_weekly(week_id)
                if count > 0:
                    st.success(f"Aggregated {count} players' daily stats to weekly totals!")
                    st.rerun()
                else:
                    st.info("No daily stats found to aggregate for this week.")

    elif duel_view == "Daily Breakdown":
        st.subheader("Daily Breakdown")

        weeks = get_recent_weeks(count=10)
        if weeks:
            week_options = {
                f"Week {w.week_number}: vs {w.opponent_name or 'TBD'}": w.id for w in weeks
            }
            selected_week = st.selectbox(
                "Select Week", list(week_options.keys()), key="daily_breakdown_week"
            )

            if selected_week:
                week_id = week_options[selected_week]
                breakdown = get_week_daily_breakdown(week_id)

                if "error" not in breakdown:
                    # Day totals summary
                    if breakdown["days"]:
                        st.markdown("**Daily Totals**")
                        day_cols = st.columns(6)
                        for i, day_info in enumerate(breakdown["days"]):
                            with day_cols[i]:
                                theme = day_info["theme"] or f"Day {day_info['day_number']}"
                                st.metric(
                                    theme,
                                    f"{day_info['total_points']:,.0f}",
                                    f"{day_info['participant_count']} players",
                                )

                        # Performance distribution pie charts
                        if breakdown["players"]:
                            st.markdown("**Performance Distribution**")
                            st.caption(
                                "Target: ≥7.2M | Below Target: 3.6M to <7.2M | "
                                "Underperforming: <3.6M"
                            )
                            pie_cols = st.columns(6)

                            # Define colors for consistency
                            perf_colors = {
                                "Target": "#22c55e",
                                "Below Target": "#eab308",
                                "Underperforming": "#ef4444",
                            }

                            for i, day_info in enumerate(breakdown["days"]):
                                day_num = day_info["day_number"]
                                theme = day_info["theme"] or f"Day {day_num}"

                                # Categorize players for this day
                                target_count = 0
                                below_target_count = 0
                                underperforming_count = 0

                                for player in breakdown["players"]:
                                    score = player["days"].get(day_num)
                                    if score is not None:
                                        if score >= DAILY_TARGET_THRESHOLD:
                                            target_count += 1
                                        elif score >= DAILY_BELOW_TARGET_THRESHOLD:
                                            below_target_count += 1
                                        else:
                                            underperforming_count += 1

                                with pie_cols[i]:
                                    # Only show chart if there are participants
                                    total = (
                                        target_count + below_target_count + underperforming_count
                                    )
                                    if total > 0:
                                        pie_data = pd.DataFrame(
                                            {
                                                "Category": [
                                                    "Target",
                                                    "Below Target",
                                                    "Underperforming",
                                                ],
                                                "Count": [
                                                    target_count,
                                                    below_target_count,
                                                    underperforming_count,
                                                ],
                                            }
                                        )
                                        # Filter out zero values for cleaner chart
                                        pie_data = pie_data[pie_data["Count"] > 0]

                                        fig = px.pie(
                                            pie_data,
                                            values="Count",
                                            names="Category",
                                            color="Category",
                                            color_discrete_map=perf_colors,
                                            hole=0.3,
                                        )
                                        fig.update_layout(
                                            showlegend=False,
                                            margin=dict(l=0, r=0, t=25, b=0),
                                            title=dict(
                                                text=f"Day {day_num}",
                                                font=dict(size=12),
                                                x=0.5,
                                            ),
                                            height=180,
                                        )
                                        fig.update_traces(
                                            textposition="inside",
                                            textinfo="value",
                                            hovertemplate="%{label}: %{value}<extra></extra>",
                                        )
                                        st.plotly_chart(
                                            fig, use_container_width=True, key=f"pie_day_{day_num}"
                                        )
                                    else:
                                        st.caption(f"Day {day_num}")
                                        st.caption("No data")

                            # Legend
                            legend_cols = st.columns(3)
                            with legend_cols[0]:
                                st.markdown("🟢 **Target** (≥7.2M)")
                            with legend_cols[1]:
                                st.markdown("🟡 **Below Target** (3.6M-7.2M)")
                            with legend_cols[2]:
                                st.markdown("🔴 **Underperforming** (<3.6M)")

                        st.markdown("---")

                    # Player breakdown table
                    if breakdown["players"]:
                        st.markdown("**Player Scores by Day**")

                        # Build table data with numeric values for proper sorting
                        table_data = []
                        for player in breakdown["players"]:
                            row = {
                                "Player": player["player_name"],
                                "Total": float(player["total"]),
                                "Days": player["days_participated"],
                            }
                            # Add each day's score (0 for missing days)
                            for day_num in range(1, 7):
                                theme = DUEL_DAY_THEMES.get(day_num, f"Day {day_num}")
                                score = player["days"].get(day_num)
                                row[theme] = float(score) if score is not None else 0.0
                            table_data.append(row)

                        df = pd.DataFrame(table_data)

                        st.dataframe(
                            df,
                            hide_index=True,
                            use_container_width=True,
                        )

                        # Participation summary
                        st.markdown("---")
                        total_players = len(breakdown["players"])
                        full_week_players = sum(
                            1 for p in breakdown["players"] if p["days_participated"] == 6
                        )
                        st.markdown(
                            f"**{full_week_players}/{total_players}** players "
                            "participated all 6 days"
                        )
                    else:
                        st.info(
                            "No daily stats recorded for this week. "
                            "Use the Import Daily tab to add data."
                        )
                else:
                    st.error(breakdown["error"])
        else:
            st.info("No duel weeks recorded yet.")

    elif duel_view == "Manage Weeks":
        st.subheader("Manage Duel Weeks & Cycles")

        # Create new cycle section
        st.markdown("**Create New Cycle**")
        col1, col2 = st.columns(2)
        with col1:
            new_cycle_num = st.number_input(
                "Cycle Number", min_value=1, value=1, key="new_cycle_num"
            )
        with col2:
            from datetime import datetime

            new_cycle_date = st.date_input(
                "Cycle Start Date", value=datetime.now(), key="new_cycle_date"
            )

        new_cycle_name = st.text_input(
            "League Name (optional)", placeholder="e.g., Gold League, Diamond League"
        )

        if st.button("Create Cycle"):
            try:
                cycle = create_cycle(
                    cycle_number=int(new_cycle_num),
                    start_date=datetime.combine(new_cycle_date, datetime.min.time()),
                    name=new_cycle_name if new_cycle_name.strip() else None,
                )
                cycle_display = f"Cycle {cycle.cycle_number}"
                if cycle.name:
                    cycle_display += f" - {cycle.name}"
                st.success(f"Created {cycle_display}!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        st.markdown("---")

        # Create new week
        st.markdown("**Create New Week**")
        col1, col2, col3 = st.columns(3)
        with col1:
            new_week_num = st.number_input("Week Number", min_value=1, value=1)
        with col2:
            new_week_date = st.date_input("Start Date", value=datetime.now())
        with col3:
            new_opponent = st.text_input("Opponent Name", placeholder="Enemy Alliance")

        if st.button("Create Week"):
            try:
                week = create_week(
                    week_number=int(new_week_num),
                    start_date=datetime.combine(new_week_date, datetime.min.time()),
                    opponent_name=new_opponent if new_opponent else None,
                )
                st.success(f"Created Week {week.week_number}!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        st.markdown("---")

        # Assign weeks to cycles
        weeks = get_recent_weeks(count=10)
        cycles = get_all_cycles()

        if weeks and cycles:
            st.markdown("**Assign Weeks to Cycle**")

            week_options_assign = {
                f"Week {w.week_number}: vs {w.opponent_name or 'TBD'}": w for w in weeks
            }
            selected_week_name = st.selectbox(
                "Select Week", list(week_options_assign.keys()), key="assign_week"
            )
            selected_week_obj = week_options_assign[selected_week_name]

            # Show current cycle assignment
            current_cycle = "None"
            if selected_week_obj.cycle_id:
                for c in cycles:
                    if c.id == selected_week_obj.cycle_id:
                        current_cycle = f"Cycle {c.cycle_number}"
                        break
            st.markdown(f"**Current cycle:** {current_cycle}")

            cycle_options = {"(None)": None}
            for c in cycles:
                label = f"Cycle {c.cycle_number}"
                if c.name:
                    label += f": {c.name}"
                cycle_options[label] = c.id
            new_cycle = st.selectbox(
                "Assign to Cycle", list(cycle_options.keys()), key="assign_cycle"
            )

            if st.button("Assign Week to Cycle"):
                try:
                    assign_week_to_cycle(selected_week_obj.id, cycle_options[new_cycle])
                    st.success(f"Assigned {selected_week_name} to {new_cycle}!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

            st.markdown("---")

            # Aggregate cycle stats
            st.markdown("**Aggregate Cycle Stats**")
            cycle_agg_options = {}
            for c in cycles:
                label = f"Cycle {c.cycle_number}"
                if c.name:
                    label += f": {c.name}"
                cycle_agg_options[label] = c.id
            selected_cycle_agg = st.selectbox(
                "Select Cycle", list(cycle_agg_options.keys()), key="agg_cycle"
            )

            if st.button("Aggregate Cycle Stats"):
                try:
                    cycle_id = cycle_agg_options[selected_cycle_agg]
                    count = aggregate_cycle_stats(cycle_id)
                    if count > 0:
                        st.success(f"Aggregated stats for {count} players!")
                        st.rerun()
                    else:
                        st.info("No weeks assigned to this cycle yet.")
                except Exception as e:
                    st.error(f"Error: {e}")

            st.markdown("---")

        # Update existing week result
        if weeks:
            st.markdown("**Update Week Result**")
            week_options = {
                f"Week {w.week_number}: vs {w.opponent_name or 'TBD'}": w.id for w in weeks
            }
            selected = st.selectbox(
                "Select Week to Update", list(week_options.keys()), key="update_week"
            )

            if selected:
                week_id = week_options[selected]
                result = st.selectbox("Result", ["win", "loss", "draw"])

                if st.button("Update Week"):
                    try:
                        set_week_result(week_id, result)
                        st.success("Week updated!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

elif page == "War Results":
    st.header("War Results")
    st.info("War history and results will be displayed here.")

    st.subheader("Recent Wars")
    st.text("No war results recorded yet.")

elif page == "Analytics":
    st.header("Analytics")
    st.info("Charts and analytics will be displayed here once data is available.")

    st.subheader("Performance Trends")
    st.text("Add war results to see analytics.")

elif page == "Events":
    from datetime import date, datetime, time
    from zoneinfo import ZoneInfo

    from src.data.models import AllianceEvent
    from src.data.storage import get_event_types, get_session, init_database

    init_database()

    st.header("Alliance Events")

    # Timezone mapping
    TIMEZONE_OPTIONS = {
        "EST": "America/New_York",
        "CST": "America/Chicago",
        "MST": "America/Denver",
        "PST": "America/Los_Angeles",
        "UTC": "UTC",
        "GMT": "Europe/London",
        "BRT": "America/Sao_Paulo",
        "KST": "Asia/Seoul",
    }

    # Event type icons for display
    EVENT_TYPE_ICONS = {
        "Duel VS": "⚔",
        "Kill Event": "🎯",
        "Alliance War": "🏰",
        "Rally": "🚩",
        "Resource Event": "📦",
        "Training Event": "🏋",
        "Custom": "📅",
    }

    def get_event_icon(event_type: str) -> str:
        """Get icon for an event type."""
        return EVENT_TYPE_ICONS.get(event_type, "📅")

    def convert_to_display_tz(dt: datetime, display_tz: str) -> datetime:
        """Convert naive EST datetime to display timezone."""
        if dt is None:
            return None
        est = ZoneInfo("America/New_York")
        target_tz = ZoneInfo(TIMEZONE_OPTIONS.get(display_tz, "America/New_York"))
        # Treat stored datetime as EST
        est_aware = dt.replace(tzinfo=est)
        return est_aware.astimezone(target_tz)

    def format_event_datetime(
        start_dt: datetime,
        end_dt: datetime | None,
        display_tz: str,
    ) -> str:
        """Format event datetime range for display."""
        start_converted = convert_to_display_tz(start_dt, display_tz)
        start_str = start_converted.strftime("%a %b %d, %I:%M %p")

        if end_dt:
            end_converted = convert_to_display_tz(end_dt, display_tz)
            # Check if same day
            if start_converted.date() == end_converted.date():
                end_str = end_converted.strftime("%I:%M %p")
            else:
                end_str = end_converted.strftime("%a %b %d, %I:%M %p")
            return f"{start_str} - {end_str} {display_tz}"
        return f"{start_str} {display_tz}"

    # Timezone selector in header
    col_header, col_tz = st.columns([3, 1])
    with col_tz:
        display_tz = st.selectbox(
            "Display Timezone",
            options=list(TIMEZONE_OPTIONS.keys()),
            index=0,
            key="events_display_tz",
        )

    # Get events from database
    with get_session() as session:
        now = datetime.now()
        upcoming_events = (
            session.query(AllianceEvent)
            .filter(AllianceEvent.start_datetime >= now)
            .order_by(AllianceEvent.start_datetime)
            .all()
        )
        past_events = (
            session.query(AllianceEvent)
            .filter(AllianceEvent.start_datetime < now)
            .order_by(AllianceEvent.start_datetime.desc())
            .limit(20)
            .all()
        )

        # Convert to dicts while session is open
        upcoming_data = [
            {
                "id": e.id,
                "title": e.title,
                "description": e.description,
                "event_type": e.event_type,
                "start_datetime": e.start_datetime,
                "end_datetime": e.end_datetime,
            }
            for e in upcoming_events
        ]
        past_data = [
            {
                "id": e.id,
                "title": e.title,
                "description": e.description,
                "event_type": e.event_type,
                "start_datetime": e.start_datetime,
                "end_datetime": e.end_datetime,
            }
            for e in past_events
        ]

    # Upcoming Events section
    st.subheader("Upcoming Events")

    if not upcoming_data:
        st.info("No upcoming events scheduled.")
    else:
        for event in upcoming_data:
            with st.container():
                col_icon, col_info, col_delete = st.columns([0.5, 8, 1.5])

                with col_icon:
                    st.markdown(
                        f"<div style='font-size:24px;padding-top:8px;'>"
                        f"{get_event_icon(event['event_type'])}</div>",
                        unsafe_allow_html=True,
                    )

                with col_info:
                    st.markdown(f"**{event['title']}**")
                    st.caption(
                        format_event_datetime(
                            event["start_datetime"],
                            event["end_datetime"],
                            display_tz,
                        )
                    )
                    if event["description"]:
                        st.text(event["description"])

                with col_delete:
                    if st.button("🗑 Delete", key=f"delete_event_{event['id']}"):
                        st.session_state[f"confirm_delete_{event['id']}"] = True

                    if st.session_state.get(f"confirm_delete_{event['id']}", False):
                        st.warning("Are you sure?")
                        col_yes, col_no = st.columns(2)
                        with col_yes:
                            if st.button("Yes", key=f"confirm_yes_{event['id']}"):
                                with get_session() as del_session:
                                    evt = del_session.get(AllianceEvent, event["id"])
                                    if evt:
                                        del_session.delete(evt)
                                        del_session.commit()
                                st.session_state.pop(f"confirm_delete_{event['id']}", None)
                                st.rerun()
                        with col_no:
                            if st.button("No", key=f"confirm_no_{event['id']}"):
                                st.session_state.pop(f"confirm_delete_{event['id']}", None)
                                st.rerun()

                st.markdown("---")

    # Add New Event section
    st.subheader("Add New Event")
    st.caption("All times are entered in EST (Eastern Standard Time)")

    event_types = get_event_types()

    with st.form("add_event_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            new_event_type = st.selectbox("Event Type", options=event_types)
            new_title = st.text_input("Title", max_chars=200)

        with col2:
            new_description = st.text_area("Description (optional)", max_chars=1000, height=100)

        st.markdown("**Event Time (EST)**")
        col_start, col_end = st.columns(2)

        with col_start:
            st.markdown("Start")
            start_date = st.date_input("Start Date", value=date.today(), key="start_date")
            start_time = st.time_input("Start Time", value=time(8, 0), key="start_time")

        with col_end:
            st.markdown("End (optional)")
            has_end_time = st.checkbox("Has end time", value=True)
            if has_end_time:
                end_date = st.date_input("End Date", value=date.today(), key="end_date")
                end_time = st.time_input("End Time", value=time(22, 0), key="end_time")

        submitted = st.form_submit_button("Add Event", type="primary")

        if submitted:
            if not new_title.strip():
                st.error("Please enter an event title.")
            else:
                start_datetime = datetime.combine(start_date, start_time)
                end_datetime = None
                if has_end_time:
                    end_datetime = datetime.combine(end_date, end_time)
                    if end_datetime <= start_datetime:
                        st.error("End time must be after start time.")
                        st.stop()

                with get_session() as session:
                    new_event = AllianceEvent(
                        title=new_title.strip(),
                        description=new_description.strip() if new_description else None,
                        event_type=new_event_type,
                        start_datetime=start_datetime,
                        end_datetime=end_datetime,
                    )
                    session.add(new_event)
                    session.commit()

                st.success(f"Event '{new_title}' added!")
                st.rerun()

    # Past Events section (collapsed)
    with st.expander("Past Events"):
        if not past_data:
            st.info("No past events.")
        else:
            for event in past_data:
                col_icon, col_info = st.columns([0.5, 9.5])

                with col_icon:
                    st.markdown(
                        f"<div style='font-size:20px;opacity:0.6;'>"
                        f"{get_event_icon(event['event_type'])}</div>",
                        unsafe_allow_html=True,
                    )

                with col_info:
                    st.markdown(f"**{event['title']}**")
                    st.caption(
                        format_event_datetime(
                            event["start_datetime"],
                            event["end_datetime"],
                            display_tz,
                        )
                    )

elif page == "Settings":
    st.header("Settings")

    from src.data.storage import (
        DEFAULT_EVENT_TYPES,
        DEFAULT_RELIABILITY_THRESHOLD,
        get_event_types,
        get_reliability_threshold,
        init_database,
        set_event_types,
        set_reliability_threshold,
    )

    init_database()

    st.subheader("VS Combat Reliability Threshold")

    # Get current threshold
    current_threshold = get_reliability_threshold()

    st.markdown(
        """
        The **reliability threshold** determines the minimum daily points a player must
        score to have that day counted as "reliable" for VS combat participation.

        **Reliability** is calculated as: `days meeting threshold / total days`

        This affects player tier assignments in the rolling report.
        """
    )

    # Display current threshold
    current_threshold_m = current_threshold / 1_000_000
    st.info(f"**Current threshold:** {current_threshold:,.0f} points ({current_threshold_m:.1f}M)")

    # Input for new threshold
    col1, col2 = st.columns([2, 1])

    with col1:
        new_threshold_m = st.number_input(
            "New threshold (in millions)",
            min_value=0.0,
            max_value=50.0,
            value=current_threshold_m,
            step=0.1,
            format="%.1f",
            help="Enter the threshold in millions (e.g., 7.2 for 7,200,000 points)",
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save Threshold", type="primary"):
            new_threshold = new_threshold_m * 1_000_000
            set_reliability_threshold(new_threshold)
            st.success(f"Threshold updated to {new_threshold:,.0f} points ({new_threshold_m:.1f}M)")
            st.rerun()

    # Reset to default button
    default_threshold_m = DEFAULT_RELIABILITY_THRESHOLD / 1_000_000
    if current_threshold != DEFAULT_RELIABILITY_THRESHOLD:
        if st.button(
            f"Reset to Default ({default_threshold_m:.1f}M)",
            type="secondary",
        ):
            set_reliability_threshold(float(DEFAULT_RELIABILITY_THRESHOLD))
            st.success(f"Threshold reset to default ({DEFAULT_RELIABILITY_THRESHOLD:,.0f} points)")
            st.rerun()

    # Explanation expander
    with st.expander("How reliability affects tier assignments"):
        st.markdown(
            """
            **Tier Thresholds:**
            - **Core**: 90%+ reliability AND 150+ avg normalized points
            - **Strong**: 75%+ reliability AND 100+ avg normalized points
            - **Standard**: 50%+ reliability AND 50+ avg normalized points
            - **Probation**: Below Standard thresholds

            **Example:**
            With a 7.2M threshold over 4 weeks (24 days total):
            - A player who scores 7.2M+ on 22 days has 91.7% reliability (Core eligible)
            - A player who scores 7.2M+ on 18 days has 75% reliability (Strong eligible)
            - A player who scores 7.2M+ on 12 days has 50% reliability (Standard eligible)

            **Note:** Players must meet BOTH the reliability AND normalized points thresholds
            to qualify for a tier.
            """
        )

    st.markdown("---")

    # Event Types Section
    st.subheader("Event Types")
    st.markdown("Configure the available event types for alliance event scheduling.")

    current_event_types = get_event_types()

    # Display current event types with delete buttons
    st.markdown("**Current Types:**")
    types_to_delete = []

    for i, event_type in enumerate(current_event_types):
        col_type, col_delete = st.columns([4, 1])
        with col_type:
            st.text(event_type)
        with col_delete:
            if st.button("🗑", key=f"delete_type_{i}", help=f"Delete {event_type}"):
                types_to_delete.append(event_type)

    # Process deletions
    if types_to_delete:
        updated_types = [t for t in current_event_types if t not in types_to_delete]
        if updated_types:
            set_event_types(updated_types)
            st.success(f"Removed: {', '.join(types_to_delete)}")
            st.rerun()
        else:
            st.error("Cannot delete all event types. At least one type must remain.")

    # Add new event type
    st.markdown("**Add New Type:**")
    col_add_input, col_add_btn = st.columns([3, 1])

    with col_add_input:
        new_type = st.text_input(
            "New event type",
            max_chars=50,
            label_visibility="collapsed",
            placeholder="Enter new event type...",
        )

    with col_add_btn:
        if st.button("Add", type="primary", key="add_event_type"):
            if new_type.strip():
                if new_type.strip() in current_event_types:
                    st.error("This event type already exists.")
                else:
                    updated_types = current_event_types + [new_type.strip()]
                    set_event_types(updated_types)
                    st.success(f"Added: {new_type.strip()}")
                    st.rerun()
            else:
                st.error("Please enter an event type name.")

    # Reset to defaults button
    if current_event_types != DEFAULT_EVENT_TYPES:
        st.markdown("")
        if st.button("Reset to Defaults", type="secondary", key="reset_event_types"):
            set_event_types(DEFAULT_EVENT_TYPES)
            st.success("Event types reset to defaults.")
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<div class="sidebar-footer">Last War Butler Toolkit<br>'
    '<span class="sidebar-version">v0.1.0</span></div>',
    unsafe_allow_html=True,
)
