"""
Configuration and styling for Streamlit application
"""

import streamlit as st


def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="SE Course Scheduler",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def apply_custom_css():
    """Apply custom CSS styling"""
    # Currently no custom CSS needed
    pass
