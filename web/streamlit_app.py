"""
Streamlit Web Application for SE Course Scheduler
A comprehensive web interface for course scheduling using Prolog
"""

from datetime import datetime
import os
from typing import Any
import streamlit as st
import pandas as pd
import plotly.express as px  # pyright: ignore[reportMissingTypeStubs]
from src.se_course_scheduler import CourseScheduler


# Page configuration
st.set_page_config(
    page_title="SE Course Scheduler",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
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
)  # pyright: ignore[reportUnusedCallResult]


def initialize_scheduler():
    """Initialize the course scheduler"""
    try:
        # Determine the correct path to scheduler.pl from any working directory
        import os

        current_file_path = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(current_file_path))
        prolog_path = os.path.join(project_root, "data", "scheduler.pl")

        scheduler = CourseScheduler(prolog_path)
        return scheduler, None
    except Exception as e:
        return None, f"Failed to initialize scheduler: {str(e)}"


def display_schedule_table(schedule: list[dict[str, str]], title: str = "Schedule"):
    """Display schedule in a formatted table"""
    if not schedule:
        st.warning(f"No {title.lower()} found.")  # pyright: ignore[reportUnusedCallResult]
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


def create_room_utilization_chart(stats: dict[str, Any]) -> None:
    """Create room utilization chart"""
    if not stats.get("room_utilization"):
        return None

    room_data = stats["room_utilization"]
    if not room_data:
        return None

    df = pd.DataFrame(room_data)

    fig = px.bar(
        df,
        x="room",
        y="utilization",
        title="Room Utilization Percentage",
        labels={"room": "Room", "utilization": "Utilization %"},
        color="utilization",
        color_continuous_scale="Blues",
    )

    fig.update_layout(
        xaxis_title="Room", yaxis_title="Utilization (%)", showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


def create_professor_workload_chart(stats: dict[str, Any]) -> None:
    """Create professor workload chart"""
    if not stats.get("professor_workload"):
        return None

    prof_data = stats["professor_workload"]
    if not prof_data:
        return None

    # Filter out professors with 0 courses
    active_profs = [p for p in prof_data if p["courses"] > 0]
    if not active_profs:
        return None

    df = pd.DataFrame(active_profs)

    fig = px.bar(
        df,
        x="name",
        y="courses",
        title="Professor Workload",
        labels={"name": "Professor", "courses": "Number of Courses"},
        color="courses",
        color_continuous_scale="Greens",
    )

    fig.update_layout(
        xaxis_title="Professor", yaxis_title="Number of Courses", showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


def main():
    """Main Streamlit application"""

    # Header
    _ = st.markdown(
        '<h1 class="main-header">📚 SE Course Scheduler</h1>', unsafe_allow_html=True
    )

    # Initialize scheduler
    scheduler, error = initialize_scheduler()

    if error:
        _ = st.error(f"Failed to initialize scheduler: {error}")
        st.stop()

    # Sidebar navigation
    _ = st.sidebar.title("Navigation")

    # Navigation buttons
    if st.sidebar.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = "🏠 Dashboard"
    if st.sidebar.button("📊 Schedule View", use_container_width=True):
        st.session_state.page = "📊 Schedule View"
    if st.sidebar.button("📈 Statistics", use_container_width=True):
        st.session_state.page = "📈 Statistics"
    if st.sidebar.button("⚙️ Settings", use_container_width=True):
        st.session_state.page = "⚙️ Settings"
    if st.sidebar.button("📤 Export", use_container_width=True):
        st.session_state.page = "📤 Export"

    # Initialize page if not set
    if "page" not in st.session_state:
        st.session_state.page = "🏠 Dashboard"

    page = st.session_state.page

    # Initialize session state
    if "schedule_generated" not in st.session_state:
        st.session_state.schedule_generated = False
    if "current_schedule" not in st.session_state:
        st.session_state.current_schedule = []
    if "current_reserved" not in st.session_state:
        st.session_state.current_reserved = []
    if "current_stats" not in st.session_state:
        st.session_state.current_stats = {}

    # Dashboard Page
    if page == "🏠 Dashboard":
        _ = st.header("Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            _ = st.metric("Scheduled Courses", len(st.session_state.current_schedule))

        with col2:
            _ = st.metric("Reserved Slots", len(st.session_state.current_reserved))

        with col3:
            total_rooms = len(
                set(
                    [
                        item["room"]
                        for item in st.session_state.current_schedule
                        + st.session_state.current_reserved
                    ]
                )
            )
            _ = st.metric("Active Rooms", total_rooms)

        with col4:
            if st.session_state.current_stats.get("scheduled_courses", 0) > 0:
                success_rate = (
                    len(st.session_state.current_schedule)
                    / st.session_state.current_stats["scheduled_courses"]
                ) * 100
                _ = st.metric("Success Rate", f"{success_rate:.1f}%")
            else:
                _ = st.metric("Success Rate", "N/A")

        # Quick actions
        st.subheader("Quick Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔄 Schedule All Courses", type="primary"):
                if scheduler is None:
                    _ = st.error(
                        "Scheduler is not initialized. Please refresh the page."
                    )
                    st.stop()

                with st.spinner("Scheduling courses..."):
                    result = scheduler.schedule_all_courses()
                    st.session_state.schedule_generated = True
                    st.session_state.current_schedule = scheduler.get_schedule()
                    st.session_state.current_reserved = scheduler.get_reserved_slots()
                    st.session_state.current_stats = scheduler.get_statistics()

                    if result["scheduled"]:
                        _ = st.success(
                            f"Successfully scheduled {len(result['scheduled'])} courses!"
                        )
                    if result["failed"]:
                        _ = st.warning(
                            f"Failed to schedule {len(result['failed'])} courses: {', '.join(result['failed'])}"
                        )

        with col2:
            if st.button("🗑️ Clear Schedule"):
                if scheduler is None:
                    _ = st.error(
                        "Scheduler is not initialized. Please refresh the page."
                    )
                    st.stop()

                scheduler.clear_schedule()
                st.session_state.schedule_generated = False
                st.session_state.current_schedule = []
                st.session_state.current_reserved = []
                st.session_state.current_stats = {}
                _ = st.success("Schedule cleared!")

        with col3:
            if st.button("✅ Validate Schedule"):
                if scheduler is None:
                    _ = st.error(
                        "Scheduler is not initialized. Please refresh the page."
                    )
                    st.stop()
                if scheduler.validate_schedule():
                    _ = st.success("Schedule validation passed - No conflicts found!")
                else:
                    _ = st.error("Schedule validation failed - Conflicts detected!")

        # Recent schedule preview
        if st.session_state.current_schedule:
            _ = st.subheader("Recent Schedule Preview")
            display_schedule_table(
                st.session_state.current_schedule[:10], "Recent Schedule"
            )

            if len(st.session_state.current_schedule) > 10:
                _ = st.info(
                    f"Showing first 10 of {len(st.session_state.current_schedule)} scheduled courses. Use 'Schedule View' for complete details."
                )

    # Schedule View Page
    elif page == "📊 Schedule View":
        _ = st.header("Schedule View")

        if not st.session_state.schedule_generated:
            _ = st.warning(
                "No schedule generated yet. Please schedule courses from the Dashboard."
            )
        else:
            # Filter options
            col1, col2, col3 = st.columns(3)

            with col1:
                rooms = sorted(
                    set(
                        [
                            item["room"]
                            for item in st.session_state.current_schedule
                            + st.session_state.current_reserved
                        ]
                    )
                )
                selected_room = st.selectbox("Filter by Room", ["All"] + rooms)

            with col2:
                days = sorted(
                    set(
                        [
                            item["day"]
                            for item in st.session_state.current_schedule
                            + st.session_state.current_reserved
                        ]
                    )
                )
                selected_day = st.selectbox("Filter by Day", ["All"] + days)

            with col3:
                periods = sorted(
                    set(
                        [
                            item["period"]
                            for item in st.session_state.current_schedule
                            + st.session_state.current_reserved
                        ]
                    )
                )
                selected_period = st.selectbox("Filter by Period", ["All"] + periods)

            # Apply filters
            filtered_schedule = st.session_state.current_schedule.copy()
            filtered_reserved = st.session_state.current_reserved.copy()

            if selected_room != "All":
                filtered_schedule = [
                    item for item in filtered_schedule if item["room"] == selected_room
                ]
                filtered_reserved = [
                    item for item in filtered_reserved if item["room"] == selected_room
                ]

            if selected_day != "All":
                filtered_schedule = [
                    item for item in filtered_schedule if item["day"] == selected_day
                ]
                filtered_reserved = [
                    item for item in filtered_reserved if item["day"] == selected_day
                ]

            if selected_period != "All":
                filtered_schedule = [
                    item
                    for item in filtered_schedule
                    if item["period"] == selected_period
                ]
                filtered_reserved = [
                    item
                    for item in filtered_reserved
                    if item["period"] == selected_period
                ]

            # Display filtered results
            if filtered_schedule:
                st.subheader("Scheduled Courses")
                display_schedule_table(filtered_schedule, "Scheduled Courses")

            if filtered_reserved:
                st.subheader("Reserved Slots")
                display_schedule_table(filtered_reserved, "Reserved Slots")

            if not filtered_schedule and not filtered_reserved:
                st.info("No items match the selected filters.")

    # Statistics Page
    elif page == "📈 Statistics":
        _ = st.header("Statistics")

        if not st.session_state.current_stats:
            _ = st.warning("No statistics available. Please generate a schedule first.")
        else:
            # Professor workload
            _ = st.subheader("Professor Workload")
            workload_chart = create_professor_workload_chart(
                st.session_state.current_stats
            )
            if workload_chart:
                _ = st.plotly_chart(workload_chart, use_container_width=True)
            else:
                _ = st.info("No professor workload data available.")

            # Room utilization
            _ = st.subheader("Room Utilization")
            utilization_chart = create_room_utilization_chart(
                st.session_state.current_stats
            )
            if utilization_chart:
                _ = st.plotly_chart(utilization_chart, use_container_width=True)
            else:
                _ = st.info("No room utilization data available.")

            # Detailed statistics tables
            col1, col2 = st.columns(2)

            with col1:
                if st.session_state.current_stats.get("professor_workload"):
                    _ = st.subheader("Professor Details")
                    prof_df = pd.DataFrame(
                        st.session_state.current_stats["professor_workload"]
                    )
                    st.dataframe(prof_df, width="stretch")

            with col2:
                if st.session_state.current_stats.get("room_utilization"):
                    _ = st.subheader("Room Details")
                    room_df = pd.DataFrame(
                        st.session_state.current_stats["room_utilization"]
                    )
                    st.dataframe(room_df, width="stretch")

    # Settings Page
    elif page == "⚙️ Settings":
        _ = st.header("Settings")

        # Data upload section
        _ = st.subheader("Upload Data")

        uploaded_file = st.file_uploader(
            "Upload Excel file with course and professor data",
            type=["xlsx", "xls"],
            help="Excel file should contain sheets: 'Courses', 'Professors', 'CanTeach', and optionally 'Preferences'",
        )

        if uploaded_file is not None:
            try:
                # Save uploaded file temporarily
                with open("temp_upload.xlsx", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Load data
                with st.spinner("Loading data from Excel file..."):
                    if scheduler is None:
                        _ = st.error(
                            "Scheduler is not initialized. Please refresh the page."
                        )
                        st.stop()
                    scheduler.load_all_data_from_excel("temp_upload.xlsx")

                _ = st.success("Data loaded successfully!")

                # Clean up temp file
                os.remove("temp_upload.xlsx")

            except (FileNotFoundError, KeyError, ValueError, ImportError) as e:
                _ = st.error(f"Error loading data: {str(e)}")

        # System information
        _ = st.subheader("System Information")
        _ = st.info(
            "This system uses Prolog for course scheduling logic and supports Excel data import/export."
        )

        # Clear all data option
        if st.button("🗑️ Clear All Data", type="secondary"):
            if scheduler is None:
                _ = st.error("Scheduler is not initialized. Please refresh the page.")
                st.stop()
            scheduler.clear_schedule()
            st.session_state.schedule_generated = False
            st.session_state.current_schedule = []
            st.session_state.current_reserved = []
            st.session_state.current_stats = {}
            _ = st.success("All data cleared!")

    # Export Page
    elif page == "📤 Export":
        _ = st.header("Export Schedule")

        if not st.session_state.schedule_generated:
            _ = st.warning("No schedule to export. Please generate a schedule first.")
        else:
            # Export options
            _ = st.subheader("Export Options")

            col1, col2 = st.columns(2)

            with col1:
                export_format = st.selectbox(
                    "Export Format", ["Excel (.xlsx)", "CSV", "JSON"]
                )

            with col2:
                st.checkbox("Include Reserved Slots", value=True)

            # Generate export
            if st.button("📥 Generate Export", type="primary"):
                try:
                    if export_format == "Excel (.xlsx)":
                        # Generate Excel file
                        output_file = f"schedule_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                        if scheduler is None:
                            _ = st.error(
                                "Scheduler is not initialized. Please refresh the page."
                            )
                            st.stop()
                        scheduler.export_to_excel(output_file)

                        # Read the file and provide download
                        with open(output_file, "rb") as f:
                            _ = st.download_button(
                                label="Download Excel File",
                                data=f.read(),
                                file_name=output_file,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            )

                        # Clean up
                        os.remove(output_file)

                    elif export_format == "CSV":
                        # Generate CSV
                        df = pd.DataFrame(st.session_state.current_schedule)
                        csv = df.to_csv(index=False)

                        _ = st.download_button(
                            label="Download CSV File",
                            data=csv,
                            file_name=f"schedule_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                        )

                    elif export_format == "JSON":
                        # Generate JSON
                        import json

                        json_data = json.dumps(
                            st.session_state.current_schedule, indent=2
                        )

                        _ = st.download_button(
                            label="Download JSON File",
                            data=json_data,
                            file_name=f"schedule_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                        )

                    _ = st.success("Export generated successfully!")

                except (FileNotFoundError, PermissionError, ValueError) as e:
                    _ = st.error(f"Error generating export: {str(e)}")

            # Preview data
            _ = st.subheader("Data Preview")
            if st.session_state.current_schedule:
                st.dataframe(
                    pd.DataFrame(st.session_state.current_schedule),
                    width="stretch",
                )


if __name__ == "__main__":
    main()
