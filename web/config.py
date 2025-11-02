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
    st.markdown(
        """
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
        }
        .success-message {
            color: #28a745;
            font-weight: bold;
        }
        .error-message {
            color: #dc3545;
            font-weight: bold;
        }
        .warning-message {
            color: #ffc107;
            font-weight: bold;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
