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
    "Go to", ["Overview", "Players", "Import Members", "War Results", "Analytics"]
)


def get_player_stats():
    """Get player statistics from database."""
    try:
        from src.data.models import Player
        from src.data.storage import get_session, init_database

        init_database()
        with get_session() as session:
            players = session.query(Player).all()
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

    stats = get_player_stats()

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

        col1, col2 = st.columns([1, 4])

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

        # Delete section
        st.markdown("---")
        st.subheader("Remove Members")

        # Multi-select for deletion
        player_options = {
            f"{row['Name']} (R{row['Rank']}, {row['Power']:.1f}M)": row["ID"]
            for _, row in df.iterrows()
        }
        selected = st.multiselect(
            "Select members to remove:",
            options=list(player_options.keys()),
        )

        if selected:
            if st.button(f"Delete {len(selected)} Member(s)", type="secondary"):
                try:
                    with get_session() as session:
                        deleted = 0
                        for name in selected:
                            player_id = player_options[name]
                            player = session.query(Player).filter(Player.id == player_id).first()
                            if player:
                                session.delete(player)
                                deleted += 1
                        session.commit()
                    st.success(f"Deleted {deleted} member(s)!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting members: {e}")

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
    else:
        st.info("No players tracked yet. Go to **Import Members** to add your alliance members.")

elif page == "Import Members":
    st.header("Add Members")
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
