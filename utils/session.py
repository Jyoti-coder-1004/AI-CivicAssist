import streamlit as st


def initialize_session_state():
    """Initialize application-level session state."""

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "All"

    if "selected_severity" not in st.session_state:
        st.session_state.selected_severity = "All"

    if "selected_status" not in st.session_state:
        st.session_state.selected_status = "All"

    if "dashboard_loaded" not in st.session_state:
        st.session_state.dashboard_loaded = True