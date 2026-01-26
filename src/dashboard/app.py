"""Main Streamlit dashboard application."""

import streamlit as st

st.set_page_config(
    page_title="Last War Butler",
    page_icon="🏰",
    layout="wide",
)

st.title("Last War Butler Dashboard")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to", ["Overview", "Players", "Import Members", "Duel VS", "War Results", "Analytics"]
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

    from src.data.duel_tracker import (
        TIER_THRESHOLDS,
        aggregate_cycle_stats,
        aggregate_daily_to_weekly,
        assign_week_to_cycle,
        create_cycle,
        create_week,
        get_all_cycles,
        get_cycle_report,
        get_recent_weeks,
        get_rolling_report,
        get_text_summary,
        get_week_daily_breakdown,
        get_weekly_report,
        import_daily_simple_csv,
        import_weekly_csv,
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
                        "Core": "#28a745",
                        "Strong": "#17a2b8",
                        "Standard": "#ffc107",
                        "Probation": "#dc3545",
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
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        result = report["result"]
                        if result:
                            color = (
                                "#28a745"
                                if result == "win"
                                else "#dc3545"
                                if result == "loss"
                                else "#ffc107"
                            )
                            st.markdown(
                                f"**Result:** <span style='color:{color}'>{result.upper()}</span>",
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown("**Result:** Pending")
                    with col2:
                        st.metric("Alliance Total", f"{report['alliance_total']:,.0f}")
                    with col3:
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
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Weeks in Cycle", report["week_count"])
                    with col2:
                        st.metric("Total Points", f"{report['total_alliance_points']:,.0f}")
                    with col3:
                        st.metric("Wins", report["wins"])
                    with col4:
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
                                    "Points": f"{w['alliance_total']:,.0f}",
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
            # Week and Day selection
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

            st.markdown("---")
            st.markdown("**CSV Format:** `PlayerName,Points`")

            daily_csv_input = st.text_area(
                "Paste daily CSV data:",
                height=200,
                placeholder="PlayerName,Points\nDragonSlayer,200\nIronFist,150\nShadowKnight,180",
                key="daily_csv_input",
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Import Daily Stats", type="primary"):
                    if daily_csv_input.strip():
                        week_id = week_options[selected_week]
                        day_number = day_options[selected_day]
                        imported, errors = import_daily_simple_csv(
                            week_id, day_number, daily_csv_input.strip()
                        )
                        if errors:
                            st.error("Import failed:")
                            for err in errors:
                                st.text(f"  {err}")
                        else:
                            st.success(f"Imported {imported} records for {selected_day}!")
                            st.rerun()
                    else:
                        st.warning("Please paste CSV data first.")

            with col2:
                if st.button("Aggregate Daily to Weekly"):
                    week_id = week_options[selected_week]
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

                        st.markdown("---")

                    # Player breakdown table
                    if breakdown["players"]:
                        st.markdown("**Player Scores by Day**")

                        # Build table data
                        table_data = []
                        for player in breakdown["players"]:
                            row = {
                                "Player": player["player_name"],
                                "Total": player["total"],
                                "Days": player["days_participated"],
                            }
                            # Add each day's score
                            for day_num in range(1, 7):
                                theme = DUEL_DAY_THEMES.get(day_num, f"Day {day_num}")
                                score = player["days"].get(day_num)
                                row[theme] = score if score is not None else "-"
                            table_data.append(row)

                        df = pd.DataFrame(table_data)
                        st.dataframe(df, hide_index=True, use_container_width=True)

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
                col1, col2 = st.columns(2)
                with col1:
                    result = st.selectbox("Result", ["win", "loss", "draw"])
                with col2:
                    total = st.number_input("Alliance Total", min_value=0, value=0)

                if st.button("Update Week"):
                    try:
                        set_week_result(week_id, result, float(total) if total > 0 else None)
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
