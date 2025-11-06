"""
Initialization functions for the Streamlit application
"""

import os
import streamlit as st
from src.se_course_scheduler import CourseScheduler


def initialize_scheduler():
    """Initialize the course scheduler"""
    try:
        # Determine the correct path to scheduler.pl from any working directory
        current_file_path = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(current_file_path))
        prolog_path = os.path.join(project_root, "data", "scheduler.pl")

        scheduler = CourseScheduler(prolog_path)
        return scheduler, None
    except (FileNotFoundError, OSError, ImportError, RuntimeError) as e:
        return None, f"Failed to initialize scheduler: {str(e)}"


def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        "schedule_generated": False,
    }
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

