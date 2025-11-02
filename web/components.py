"""
Reusable UI components for the Streamlit application
"""

import streamlit as st
import pandas as pd


def display_schedule_table(schedule: list[dict[str, str]], title: str = "Schedule"):
    """Display schedule in a formatted table"""
    if not schedule:
        st.warning(f"No {title.lower()} found.")
        return

    df = pd.DataFrame(schedule)

    # Format the display
    if "time_range" in df.columns:
        df["Time"] = df["time_range"]
    if "course_name" in df.columns:
        df["Course"] = df["course_name"]
    if "professor" in df.columns:
        df["Professor"] = df["professor"]

    # Select relevant columns for display
    display_columns = []
    for col in ["Course", "Professor", "room", "day", "period", "Time"]:
        if col in df.columns:
            display_columns.append(col)

    if display_columns:
        st.dataframe(df[display_columns], width="stretch")
