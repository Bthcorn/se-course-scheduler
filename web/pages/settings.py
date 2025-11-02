"""
Settings page for the Streamlit application
"""

import os
import streamlit as st
from web.utils import check_scheduler_initialized
from web.pages.base_page import BasePage


class SettingsPage(BasePage):
    """Settings page class"""

    def render(self):
        """Render the Settings page"""
        _ = st.header("Settings")

        # Data upload section
        _ = st.subheader("Upload Data")

        uploaded_file = st.file_uploader(
            "Upload Excel file with course and professor data",
            type=["xlsx", "xls"],
            help=(
                "Excel file should contain sheets: 'Courses', 'Professors', "
                "'CanTeach', and optionally 'Preferences'"
            ),
        )

        if uploaded_file is not None:
            try:
                # Save uploaded file temporarily
                with open("temp_upload.xlsx", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Load data
                with st.spinner("Loading data from Excel file..."):
                    self.scheduler = check_scheduler_initialized(self.scheduler)
                    self.scheduler.load_all_data_from_excel("temp_upload.xlsx")

                _ = st.success("Data loaded successfully!")

                # Clean up temp file
                os.remove("temp_upload.xlsx")

            except (FileNotFoundError, KeyError, ValueError, ImportError) as e:
                _ = st.error(f"Error loading data: {str(e)}")

        # System information
        _ = st.subheader("System Information")
        _ = st.info(
            "This system uses Prolog for course scheduling logic and supports "
            "Excel data import/export."
        )

        # Clear all data option
        if st.button("🗑️ Clear All Data", type="secondary"):
            self.scheduler = check_scheduler_initialized(self.scheduler)
            self.scheduler.clear_schedule()
            st.session_state.schedule_generated = False
            st.session_state.current_schedule = []
            st.session_state.current_reserved = []
            st.session_state.current_stats = {}
            _ = st.success("All data cleared!")
