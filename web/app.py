"""
Main Streamlit application entry point
A comprehensive web interface for course scheduling using Prolog
"""

import streamlit as st
from web.config import setup_page_config, apply_custom_css
from web.scheduler_initializer import initialize_scheduler, initialize_session_state
from web.views.dashboard import DashboardPage
from web.views.schedules_page import SchedulesPage


def main():
    """Main Streamlit application"""
    # Setup page configuration and styling
    setup_page_config()
    apply_custom_css()

    # Initialize scheduler (store in session state to persist across reruns)
    if "scheduler" not in st.session_state:
        scheduler, error = initialize_scheduler()
        if error:
            _ = st.error(f"Failed to initialize scheduler: {error}")
            st.stop()
        st.session_state.scheduler = scheduler
    else:
        scheduler = st.session_state.scheduler

    # Initialize session state
    initialize_session_state()

    # Simple navigation buttons
    st.sidebar.title("Navigation")
    
    if st.sidebar.button("Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
    
    if st.sidebar.button("Schedules", use_container_width=True):
        st.session_state.page = "Schedules"

    # Default page
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    # Route to appropriate page
    if st.session_state.page == "Dashboard":
        page_instance = DashboardPage(scheduler)
        page_instance.render()
    elif st.session_state.page == "Schedules":
        page_instance = SchedulesPage(scheduler)
        page_instance.render()


if __name__ == "__main__":
    main()
