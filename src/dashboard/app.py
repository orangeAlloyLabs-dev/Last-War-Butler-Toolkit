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
page = st.sidebar.radio("Go to", ["Overview", "Players", "War Results", "Analytics"])

if page == "Overview":
    st.header("Alliance Overview")
    st.info("Connect your database and Discord bot to see alliance statistics here.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Members", "—")
    with col2:
        st.metric("Alliance Power", "—")
    with col3:
        st.metric("War Win Rate", "—")

elif page == "Players":
    st.header("Player Management")
    st.info("Player tracking will be displayed here once data is available.")

    # Placeholder for player table
    st.subheader("Player List")
    st.text("No players tracked yet.")

elif page == "War Results":
    st.header("War Results")
    st.info("War history and results will be displayed here.")

    # Placeholder for war results
    st.subheader("Recent Wars")
    st.text("No war results recorded yet.")

elif page == "Analytics":
    st.header("Analytics")
    st.info("Charts and analytics will be displayed here once data is available.")

    # Placeholder for charts
    st.subheader("Performance Trends")
    st.text("Add war results to see analytics.")

st.sidebar.markdown("---")
st.sidebar.markdown("**Last War Butler Toolkit**")
st.sidebar.markdown("v0.1.0")
