"""
Utility functions for the Streamlit application
"""

import os
from typing import Optional
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


def check_scheduler_initialized(
    scheduler: Optional[CourseScheduler],
) -> CourseScheduler:
    """Check if scheduler is initialized, show error if not"""
    if scheduler is None:
        _ = st.error("Scheduler is not initialized. Please refresh the page.")
        st.stop()
    return scheduler


def display_messages():
    """Display and clear stored success/warning messages"""
    if st.session_state.success_message:
        _ = st.success(st.session_state.success_message)
        st.session_state.success_message = None
    if st.session_state.warning_message:
        _ = st.warning(st.session_state.warning_message)
        st.session_state.warning_message = None


def extract_unique_values(items: list[dict], key: str) -> list[str]:
    """Extract unique values from a list of dicts by key"""
    return sorted(set(item[key] for item in items))


def apply_filters(
    schedule: list[dict],
    reserved: list[dict],
    room: str,
    day: str,
    period: str,
) -> tuple[list[dict], list[dict]]:
    """Apply filters to schedule and reserved lists"""
    filtered_schedule = schedule.copy()
    filtered_reserved = reserved.copy()

    if room != "All":
        filtered_schedule = [item for item in filtered_schedule if item["room"] == room]
        filtered_reserved = [item for item in filtered_reserved if item["room"] == room]

    if day != "All":
        filtered_schedule = [item for item in filtered_schedule if item["day"] == day]
        filtered_reserved = [item for item in filtered_reserved if item["day"] == day]

    if period != "All":
        filtered_schedule = [
            item for item in filtered_schedule if item["period"] == period
        ]
        filtered_reserved = [
            item for item in filtered_reserved if item["period"] == period
        ]

    return filtered_schedule, filtered_reserved


def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        "schedule_generated": False,
        "current_schedule": [],
        "current_reserved": [],
        "current_stats": {},
        "success_message": None,
        "warning_message": None,
    }
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def setup_navigation():
    """Setup sidebar navigation"""
    _ = st.sidebar.title("Navigation")

    nav_items = [
        ("🏠 Dashboard", "🏠 Dashboard"),
        ("📅 Timetable View", "📅 Timetable View"),
        ("📈 Statistics", "📈 Statistics"),
        ("⚙️ Settings", "⚙️ Settings"),
        ("📤 Export", "📤 Export"),
    ]

    for label, page_name in nav_items:
        if st.sidebar.button(label, width="stretch"):
            st.session_state.page = page_name

    if "page" not in st.session_state:
        st.session_state.page = "🏠 Dashboard"

    return st.session_state.page
