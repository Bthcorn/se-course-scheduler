"""
Settings page for the Streamlit application
"""

import os
import streamlit as st
import pandas as pd
from web.utils import check_scheduler_initialized
from web.pages.base_page import BasePage


class SettingsPage(BasePage):
    """Settings page class"""

    def render(self):
        """Render the Settings page"""
        _ = st.header("Settings")

        # Excel file structure visualization
        _ = st.subheader("📋 Excel File Structure")

        with st.expander("View Excel File Structure", expanded=True):
            st.markdown(
                """
                Your Excel file should contain the following sheets with the columns shown below.
                All column names are **case-sensitive** and must match exactly.
                """
            )

            # Courses sheet
            st.markdown("### 1. **Courses** Sheet (Required)")
            courses_example = pd.DataFrame(
                {
                    "CourseID": ["CS101", "CS201", "CS301"],
                    "CourseName": [
                        "Introduction to Programming",
                        "Data Structures",
                        "Database Systems",
                    ],
                    "Year": [1, 2, 3],
                    "RequiredCapacity": [50, 40, 30],
                    "Prerequisites": ["", "CS101", "CS201,CS101"],
                }
            )
            st.dataframe(courses_example, use_container_width=True, hide_index=True)
            st.caption(
                "💡 **Prerequisites** column is optional. Leave empty or use "
                "comma-separated CourseIDs."
            )

            st.divider()

            # Professors sheet
            st.markdown("### 2. **Professors** Sheet (Required)")
            professors_example = pd.DataFrame(
                {
                    "ProfessorID": ["P001", "P002", "P003"],
                    "ProfessorName": [
                        "Dr. John Smith",
                        "Dr. Jane Doe",
                        "Dr. Bob Wilson",
                    ],
                }
            )
            st.dataframe(professors_example, use_container_width=True, hide_index=True)

            st.divider()

            # CanTeach sheet
            st.markdown("### 3. **CanTeach** Sheet (Required)")
            can_teach_example = pd.DataFrame(
                {
                    "ProfessorID": ["P001", "P001", "P002", "P002", "P003"],
                    "CourseID": ["CS101", "CS201", "CS101", "CS301", "CS201"],
                }
            )
            st.dataframe(can_teach_example, use_container_width=True, hide_index=True)
            st.caption(
                "💡 This sheet defines which professors can teach which courses."
            )

            st.divider()

            # Preferences sheet (optional)
            st.markdown("### 4. **Preferences** Sheet (Optional)")
            preferences_example = pd.DataFrame(
                {
                    "ProfessorID": ["P001", "P001", "P002"],
                    "Day": ["monday", "tuesday", "wednesday"],
                    "Period": ["morning", "afternoon", "evening"],
                }
            )
            st.dataframe(preferences_example, use_container_width=True, hide_index=True)
            st.caption(
                "💡 **Day** values: monday, tuesday, wednesday, thursday, friday, saturday, sunday "
                "(lowercase)\n\n"
                "💡 **Period** values: morning, afternoon, evening (lowercase)"
            )

        st.divider()

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
