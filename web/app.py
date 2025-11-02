"""
Main Streamlit application entry point
A comprehensive web interface for course scheduling using Prolog
"""
import streamlit as st
from web.config import setup_page_config, apply_custom_css
from web.utils import initialize_scheduler, initialize_session_state, setup_navigation
from web.pages.dashboard import DashboardPage
from web.pages.timetable_view import TimetableViewPage
from web.pages.statistics import StatisticsPage
from web.pages.settings import SettingsPage
from web.pages.export import ExportPage


def main():
    """Main Streamlit application"""
    # Setup page configuration and styling
    setup_page_config()
    apply_custom_css()

    # Header
    _ = st.markdown(
        '<h1 class="main-header">📚 SE Course Scheduler</h1>',
        unsafe_allow_html=True,
    )

    # Initialize scheduler
    scheduler, error = initialize_scheduler()

    if error:
        _ = st.error(f"Failed to initialize scheduler: {error}")
        st.stop()

    # Setup navigation
    page = setup_navigation()

    # Initialize session state
    initialize_session_state()

    # Route to appropriate page using classes
    if page == "🏠 Dashboard":
        page_instance = DashboardPage(scheduler)
        page_instance.render()
    elif page == "📅 Timetable View":
        page_instance = TimetableViewPage(scheduler)
        page_instance.render()
    elif page == "📈 Statistics":
        page_instance = StatisticsPage(scheduler)
        page_instance.render()
    elif page == "⚙️ Settings":
        page_instance = SettingsPage(scheduler)
        page_instance.render()
    elif page == "📤 Export":
        page_instance = ExportPage(scheduler)
        page_instance.render()


if __name__ == "__main__":
    main()

