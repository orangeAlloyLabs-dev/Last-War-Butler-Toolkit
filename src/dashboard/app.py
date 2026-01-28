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
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Sidebar glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Section title accent bar */
    .stSubheader, h2 {
        border-left: 4px solid transparent;
        border-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%) 1;
        padding-left: 12px;
    }

    /* Metric cards styling */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }

    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.6);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
    }

    /* Data tables */
    [data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
    }

    /* Buttons */
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
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
    }

    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }

    /* Info/Warning/Error boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 4px;
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: rgba(255, 255, 255, 0.6);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* Select boxes and inputs */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: white;
    }

    /* Multiselect */
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }

    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    /* Dividers */
    hr {
        border-color: rgba(255, 255, 255, 0.1);
    }

    /* Caption/muted text */
    .stCaption, small {
        color: rgba(255, 255, 255, 0.5);
    }

    /* Download button */
    .stDownloadButton > button {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Last War Butler Dashboard")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Players",
        "Player Summary",
        "Import Members",
        "Duel VS",
        "War Results",
        "Analytics",
    ],
)


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


if page == "Overview":
    st.header("Alliance Overview")

    stats = get_player_stats()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Members", stats["total_members"])
    with col2:
        # Power is stored as display value (e.g., 145.2 for 145.2M)
        total_power = stats["total_power"]
        if total_power >= 1000:
            power_str = f"{total_power / 1000:.2f}B"
        else:
            power_str = f"{total_power:.1f}M"
        st.metric("Alliance Power", power_str)
    with col3:
        st.metric("War Win Rate", "—")

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
                "Level": st.column_config.NumberColumn("Level", min_value=1, max_value=60, step=1),
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
            f"{row['Name']} (R{row['Rank']}, {row['Power']:.1f}M)": row["ID"]
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
            st.metric("Average Power", f"{df['Power'].mean():.1f}M")
        with col2:
            st.metric("Highest Power", f"{df['Power'].max():.1f}M")
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
                f"{row['Name']} (R{row['Rank']}, {row['Power']:.1f}M)": row["ID"]
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
    st.header("Player Summary")

    import pandas as pd

    from src.data.duel_tracker import (
        TIER_THRESHOLDS,
        get_player_daily_averages,
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
            label = f"{p_name} (R{p_rank}, {p_power:.1f}M)"
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
                st.subheader("Player Stats")

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

                stat_cols = st.columns(4)
                with stat_cols[0]:
                    power_str = f"{player.power:.1f}M"
                    st.metric("Current Power", power_str)
                with stat_cols[1]:
                    st.metric("Base Level", f"{player.level}/60")
                with stat_cols[2]:
                    st.metric("Alliance Rank", f"R{player.rank}")
                with stat_cols[3]:
                    st.markdown(
                        f"**Performance Tier**<br>"
                        f"<span style='color:{tier_color};font-size:24px;font-weight:bold;'>"
                        f"{tier}</span>",
                        unsafe_allow_html=True,
                    )

                # === VS Combat Performance Section ===
                st.markdown("---")
                st.subheader("VS Combat Performance")

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

                # === Day Performance Section ===
                st.markdown("---")
                st.subheader("Day Theme Performance")

                daily_avgs = get_player_daily_averages(selected_player_id, weeks=4)

                if "error" not in daily_avgs and daily_avgs.get("day_averages"):
                    day_cols = st.columns(6)
                    for i, (day_num, day_data) in enumerate(daily_avgs["day_averages"].items()):
                        with day_cols[i]:
                            theme = day_data["theme"]
                            avg_pts = day_data["avg_points"]
                            times = day_data["times_participated"]
                            total_opp = day_data["total_opportunities"]

                            # Shortened theme names for display
                            short_themes = {
                                "Radar Training": "Radar",
                                "Base Expansion": "Base",
                                "Age of Science": "Science",
                                "Train Heroes": "Heroes",
                                "Total Mobilization": "Mobilize",
                                "Enemy Buster": "Buster",
                            }
                            display_theme = short_themes.get(theme, theme)

                            st.markdown(f"**{display_theme}**")
                            if avg_pts >= 1_000_000:
                                pts_str = f"{avg_pts / 1_000_000:.1f}M"
                            elif avg_pts >= 1_000:
                                pts_str = f"{avg_pts / 1_000:.0f}K"
                            else:
                                pts_str = f"{avg_pts:.0f}"
                            st.metric("Avg", pts_str, label_visibility="collapsed")
                            st.caption(f"{times}/{total_opp} weeks")
                else:
                    st.info("No daily performance data available.")

                # === Recent Weeks Table ===
                st.markdown("---")
                st.subheader("Recent Weeks Performance")

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
            if level < 1 or level > 60:
                return f"Level must be 1-60, got {level}"
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

elif page == "Duel VS":
    st.header("Duel VS Tracker")

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

    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "Rolling Report",
            "Weekly Report",
            "Cycle Report",
            "Import Weekly",
            "Import Daily",
            "Daily Breakdown",
            "Manage Weeks",
        ]
    )

    with tab1:
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

                # Summary stats
                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)
                tier_counts = df["Tier"].value_counts()
                with col1:
                    st.metric("Core", tier_counts.get("Core", 0))
                with col2:
                    st.metric("Strong", tier_counts.get("Strong", 0))
                with col3:
                    st.metric("Standard", tier_counts.get("Standard", 0))
                with col4:
                    st.metric("Probation", tier_counts.get("Probation", 0))
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

    with tab2:
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
                            }
                        )
                        df = df[["Player", "Points", "Days", "Normalized"]]
                        df["Points"] = df["Points"].astype(int)
                        df["Normalized"] = df["Normalized"].round(1)

                        st.dataframe(df, hide_index=True, use_container_width=True)

                    # Text summary
                    with st.expander("Text Summary (copy/paste)"):
                        summary = get_text_summary(week_id)
                        st.code(summary, language=None)
        else:
            st.info("No duel weeks recorded yet.")

    with tab3:
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

    with tab4:
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

    with tab5:
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

    with tab6:
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

    with tab7:
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

st.sidebar.markdown("---")
st.sidebar.markdown("**Last War Butler Toolkit**")
st.sidebar.markdown("v0.1.0")
