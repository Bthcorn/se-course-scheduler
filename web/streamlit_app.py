"""
Streamlit Web Application for SE Course Scheduler
A comprehensive web interface for course scheduling using Prolog
"""

from datetime import datetime
import json
import os
from typing import Any, Optional
import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import plotly.express as px
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
)


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


def render_action_card(
    title: str,
    description: str,
    button_text: str,
    button_key: str,
    button_variant: str,
    gradient_start: str,
    gradient_end: str,
    border_color: str,
):
    """Render a reusable action card component"""
    _ = st.markdown(
        f"""
        <div style='padding: 1rem; border-radius: 0.5rem; 
        background: linear-gradient(135deg, {gradient_start}08 0%, {gradient_end}08 100%);
        border-left: 4px solid {border_color}; margin-bottom: 1rem;
        text-align: center;'>
        <h4 style='color: #1f77b4; margin: 0 0 0.5rem 0; font-weight: 600;'>
        {title}</h4>
        <p style='margin: 0 0 1rem 0; color: #666; font-size: 0.9em;'>
        {description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return ui.button(
        key=button_key,
        text=button_text,
        variant=button_variant,
        size="lg",
        use_container_width=True,
    )


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

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


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

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


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
        ("📊 Schedule View", "📊 Schedule View"),
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


def render_dashboard_page(scheduler: Optional[CourseScheduler]):
    """Render the Dashboard page"""
    _ = st.header("Dashboard")
    display_messages()

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ui.metric_card(
            title="Scheduled Courses",
            content=f"{len(st.session_state.current_schedule)}",
            description="total scheduled courses",
            key="schedule_count_card",
        )

    with col2:
        ui.metric_card(
            title="Reserved Slots",
            content=f"{len(st.session_state.current_reserved)}",
            description="total reserved slots",
            key="reserved_count_card",
        )

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
        ui.metric_card(
            title="Active Rooms",
            content=f"{total_rooms}",
            description="total active rooms",
            key="active_rooms_card",
        )

    with col4:
        value = "N/A"
        if st.session_state.current_stats.get("scheduled_courses", 0) > 0:
            success_rate = (
                len(st.session_state.current_schedule)
                / st.session_state.current_stats["scheduled_courses"]
            ) * 100
            value = f"{success_rate:.1f}%"

        ui.metric_card(
            title="Success Rate",
            content=value,
            description="success rate",
            key="success_rate_card",
        )

    # Quick actions
    _ = st.markdown("### Quick Actions")
    _ = st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        with st.container():
            if render_action_card(
                title="🔄 Schedule Courses",
                description="Generate schedule for all available courses",
                button_text="Schedule All Courses",
                button_key="schedule_courses_btn",
                button_variant="default",
                gradient_start="#667eea",
                gradient_end="#764ba2",
                border_color="#667eea",
            ):
                scheduler = check_scheduler_initialized(scheduler)

                with st.spinner("Scheduling courses..."):
                    result = scheduler.schedule_all_courses()
                    st.session_state.schedule_generated = True
                    st.session_state.current_schedule = scheduler.get_schedule()
                    st.session_state.current_reserved = scheduler.get_reserved_slots()
                    st.session_state.current_stats = scheduler.get_statistics()

                    if result["scheduled"]:
                        st.session_state.success_message = (
                            f"Successfully scheduled "
                            f"{len(result['scheduled'])} courses!"
                        )

                    if result["failed"]:
                        st.session_state.warning_message = (
                            f"Failed to schedule {len(result['failed'])} "
                            f"courses: {', '.join(result['failed'])}"
                        )

                st.rerun()

    with col2:
        with st.container():
            if render_action_card(
                title="🗑️ Clear Schedule",
                description="Remove all scheduled courses and reset",
                button_text="Clear Schedule",
                button_key="clear_schedule_btn",
                button_variant="destructive",
                gradient_start="#f093fb",
                gradient_end="#f5576c",
                border_color="#f5576c",
            ):
                scheduler = check_scheduler_initialized(scheduler)

                scheduler.clear_schedule()
                st.session_state.schedule_generated = False
                st.session_state.current_schedule = []
                st.session_state.current_reserved = []
                st.session_state.current_stats = {}
                st.session_state.success_message = "Schedule cleared!"
                st.rerun()

    with col3:
        with st.container():
            if render_action_card(
                title="✅ Validate Schedule",
                description="Check for conflicts and constraint violations",
                button_text="Validate Schedule",
                button_key="validate_btn",
                button_variant="outline",
                gradient_start="#4facfe",
                gradient_end="#00f2fe",
                border_color="#4facfe",
            ):
                scheduler = check_scheduler_initialized(scheduler)

                if scheduler.validate_schedule():
                    st.session_state.success_message = (
                        "Schedule validation passed - No conflicts found!"
                    )
                else:
                    st.session_state.warning_message = (
                        "Schedule validation failed - Conflicts detected!"
                    )

    # Recent schedule preview
    if st.session_state.current_schedule:
        _ = st.subheader("Recent Schedule Preview")
        display_schedule_table(
            st.session_state.current_schedule[:10], "Recent Schedule"
        )

        if len(st.session_state.current_schedule) > 10:
            _ = st.info(
                f"Showing first 10 of {len(st.session_state.current_schedule)} "
                "scheduled courses. Use 'Schedule View' for complete details."
            )


def render_schedule_view_page():
    """Render the Schedule View page"""
    _ = st.header("Schedule View")

    if not st.session_state.schedule_generated:
        _ = st.warning(
            "No schedule generated yet. Please schedule courses from the Dashboard."
        )
        return

    # Filter options
    col1, col2, col3 = st.columns(3)

    all_items = st.session_state.current_schedule + st.session_state.current_reserved

    with col1:
        rooms = ["All"] + extract_unique_values(all_items, "room")
        selected_room = st.selectbox("Filter by Room", rooms)

    with col2:
        days = ["All"] + extract_unique_values(all_items, "day")
        selected_day = st.selectbox("Filter by Day", days)

    with col3:
        periods = ["All"] + extract_unique_values(all_items, "period")
        selected_period = st.selectbox("Filter by Period", periods)

    # Apply filters
    filtered_schedule, filtered_reserved = apply_filters(
        st.session_state.current_schedule,
        st.session_state.current_reserved,
        selected_room,
        selected_day,
        selected_period,
    )

    # Display filtered results
    if filtered_schedule:
        st.subheader("Scheduled Courses")
        display_schedule_table(filtered_schedule, "Scheduled Courses")

    if filtered_reserved:
        st.subheader("Reserved Slots")
        display_schedule_table(filtered_reserved, "Reserved Slots")

    if not filtered_schedule and not filtered_reserved:
        st.info("No items match the selected filters.")


def format_cell_content(
    course_name: str, professor: str, room: str, is_reserved: bool = False
) -> str:
    """Format cell content with HTML styling"""
    if is_reserved:
        return (
            f"<div style='text-align: center;'>"
            f"<strong style='color: #1976d2; font-size: 1.1em;'>[RESERVED]</strong><br/>"
            f"<span style='color: #666;'>{course_name}</span><br/>"
            f"<span style='color: #999; font-size: 0.9em;'>Room: {room}</span>"
            f"</div>"
        )
    else:
        return (
            f"<div style='text-align: center;'>"
            f"<strong style='color: #1f77b4; font-size: 1.1em; font-weight: 600;'>"
            f"{course_name}</strong><br/>"
            f"<span style='color: #ff6b35; font-style: italic; font-weight: 500;'>"
            f"{professor}</span><br/>"
            f"<span style='color: #666; font-size: 0.85em;'>Room: {room}</span>"
            f"</div>"
        )


def create_timetable_data(
    schedule: list[dict[str, str]],
    reserved: list[dict[str, str]],
    room_filter: str,
    professor_filter: str,
) -> dict[str, dict[str, dict[str, list[str]]]]:
    """Create timetable data structure: {room: {day: {period: [items]}}}"""
    days_order = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    periods_order = ["morning", "afternoon", "evening"]

    # Group by room
    timetables_by_room: dict[str, dict[str, dict[str, list[str]]]] = {}

    # Helper function to initialize timetable
    def init_timetable():
        timetable: dict[str, dict[str, list[str]]] = {}
        for day in days_order:
            timetable[day] = {}
            for period in periods_order:
                timetable[day][period] = []
        return timetable

    # Add scheduled courses
    for item in schedule:
        room = item.get("room", "")
        professor = item.get("professor", "")

        # Apply filters
        if room_filter != "All" and room != room_filter:
            continue
        if professor_filter != "All" and professor != professor_filter:
            continue

        if room not in timetables_by_room:
            timetables_by_room[room] = init_timetable()

        day = item.get("day", "").lower()
        period = item.get("period", "").lower()

        if day in timetables_by_room[room] and period in timetables_by_room[room][day]:
            course_name = item.get("course_name", "")
            cell_content = format_cell_content(course_name, professor, room, False)
            timetables_by_room[room][day][period].append(cell_content)

    # Add reserved slots
    for item in reserved:
        room = item.get("room", "")
        reason = item.get("reason", "Reserved")

        # Apply filters
        if room_filter != "All" and room != room_filter:
            continue

        if room not in timetables_by_room:
            timetables_by_room[room] = init_timetable()

        day = item.get("day", "").lower()
        period = item.get("period", "").lower()

        if day in timetables_by_room[room] and period in timetables_by_room[room][day]:
            cell_content = format_cell_content(reason, "", room, True)
            timetables_by_room[room][day][period].append(cell_content)

    return timetables_by_room


def render_timetable_for_room(room: str, timetable: dict[str, dict[str, list[str]]]):
    """Render a timetable table for a specific room"""
    days_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    periods_order = ["Morning", "Afternoon", "Evening"]

    # Create HTML table
    html_table = (
        "<table style='width:100%; border-collapse: collapse; margin-bottom: 2rem;'>"
    )
    html_table += "<thead><tr style='background-color: #1f77b4; color: white;'>"
    html_table += (
        f"<th colspan='4' style='padding: 12px; border: 1px solid #ddd; "
        f"text-align: center; font-size: 1.2em;'>"
        f"Room: {room.upper()}</th>"
    )
    html_table += "</tr><tr style='background-color: #f0f2f6;'>"
    html_table += (
        "<th style='padding: 10px; border: 1px solid #ddd; text-align: left; "
        "font-weight: 600;'>Day</th>"
    )
    for period in periods_order:
        html_table += (
            f"<th style='padding: 10px; border: 1px solid #ddd; text-align: center; "
            f"font-weight: 600;'>{period}</th>"
        )
    html_table += "</tr></thead><tbody>"

    for day in days_order:
        day_lower = day.lower()
        html_table += (
            "<tr><td style='padding: 12px; border: 1px solid #ddd; "
            "font-weight: bold; background-color: #f9f9f9; width: 120px;'>"
            f"{day}</td>"
        )

        for period in periods_order:
            period_lower = period.lower()
            items = timetable.get(day_lower, {}).get(period_lower, [])
            cell_style = (
                "padding: 15px; border: 1px solid #ddd; "
                "vertical-align: middle; min-height: 100px; text-align: center;"
            )

            if items:
                # Check if reserved
                is_reserved = any("[RESERVED]" in item for item in items)
                bg_color = "#e3f2fd" if is_reserved else "#f1f8e9"
                cell_style += f" background-color: {bg_color};"
                cell_content = (
                    "<br><hr style='margin: 8px 0; border: 0; "
                    "border-top: 1px solid rgba(0,0,0,0.1);'>"
                ).join(items)
            else:
                cell_style += " background-color: #fafafa; color: #999;"
                cell_content = "<em style='font-size: 0.9em;'>Available</em>"

            html_table += f"<td style='{cell_style}'>{cell_content}</td>"

        html_table += "</tr>"

    html_table += "</tbody></table>"

    return html_table


def render_timetable_page():
    """Render the Timetable View page"""
    _ = st.header("Timetable View")

    if not st.session_state.schedule_generated:
        _ = st.warning(
            "No schedule generated yet. Please schedule courses from the Dashboard."
        )
        return

    # Filters
    all_items = st.session_state.current_schedule + st.session_state.current_reserved
    rooms = ["All"] + extract_unique_values(all_items, "room")
    professors = ["All"] + extract_unique_values(
        st.session_state.current_schedule, "professor"
    )

    col1, col2 = st.columns(2)
    with col1:
        selected_room = st.selectbox(
            "Filter by Room", rooms, key="timetable_room_filter"
        )
    with col2:
        selected_professor = st.selectbox(
            "Filter by Professor", professors, key="timetable_professor_filter"
        )

    # Create timetable data grouped by room
    timetables_by_room = create_timetable_data(
        st.session_state.current_schedule,
        st.session_state.current_reserved,
        selected_room,
        selected_professor,
    )

    if not timetables_by_room:
        _ = st.info("No schedules found matching the selected filters.")
        return

    # Display separate table for each room
    _ = st.markdown("<br>", unsafe_allow_html=True)
    _ = st.subheader("Room Timetables")

    # Sort rooms for consistent display
    sorted_rooms = sorted(timetables_by_room.keys())

    for room in sorted_rooms:
        timetable = timetables_by_room[room]
        html_table = render_timetable_for_room(room, timetable)
        _ = st.markdown(html_table, unsafe_allow_html=True)


def render_statistics_page():
    """Render the Statistics page"""
    _ = st.header("Statistics")

    if not st.session_state.current_stats:
        _ = st.warning("No statistics available. Please generate a schedule first.")
        return

    # Professor workload
    _ = st.subheader("Professor Workload")
    if not st.session_state.current_stats.get("professor_workload"):
        _ = st.info("No professor workload data available.")
    else:
        create_professor_workload_chart(st.session_state.current_stats)

    # Room utilization
    _ = st.subheader("Room Utilization")
    if not st.session_state.current_stats.get("room_utilization"):
        _ = st.info("No room utilization data available.")
    else:
        create_room_utilization_chart(st.session_state.current_stats)

    # Detailed statistics tables
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.current_stats.get("professor_workload"):
            _ = st.subheader("Professor Details")
            prof_df = pd.DataFrame(st.session_state.current_stats["professor_workload"])
            st.dataframe(prof_df, width="stretch")

    with col2:
        if st.session_state.current_stats.get("room_utilization"):
            _ = st.subheader("Room Details")
            room_df = pd.DataFrame(st.session_state.current_stats["room_utilization"])
            st.dataframe(room_df, width="stretch")


def render_settings_page(scheduler: Optional[CourseScheduler]):
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
                scheduler = check_scheduler_initialized(scheduler)
                scheduler.load_all_data_from_excel("temp_upload.xlsx")

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
        scheduler = check_scheduler_initialized(scheduler)
        scheduler.clear_schedule()
        st.session_state.schedule_generated = False
        st.session_state.current_schedule = []
        st.session_state.current_reserved = []
        st.session_state.current_stats = {}
        _ = st.success("All data cleared!")


def render_export_page(scheduler: Optional[CourseScheduler]):
    """Render the Export page"""
    _ = st.header("Export Schedule")

    if not st.session_state.schedule_generated:
        _ = st.warning("No schedule to export. Please generate a schedule first.")
        return

    # Export options
    _ = st.subheader("Export Options")

    col1, col2 = st.columns(2)

    with col1:
        export_format = st.selectbox("Export Format", ["Excel (.xlsx)", "CSV", "JSON"])

    with col2:
        st.checkbox("Include Reserved Slots", value=True)

    # Generate export
    if st.button("📥 Generate Export", type="primary"):
        try:
            if export_format == "Excel (.xlsx)":
                output_file = (
                    f"schedule_export_"
                    f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                )
                scheduler = check_scheduler_initialized(scheduler)
                scheduler.export_to_excel(output_file)

                # Read the file and provide download
                with open(output_file, "rb") as f:
                    _ = st.download_button(
                        label="Download Excel File",
                        data=f.read(),
                        file_name=output_file,
                        mime=(
                            "application/vnd.openxmlformats-officedocument."
                            "spreadsheetml.sheet"
                        ),
                    )

                # Clean up
                os.remove(output_file)

            elif export_format == "CSV":
                df = pd.DataFrame(st.session_state.current_schedule)
                csv = df.to_csv(index=False)

                _ = st.download_button(
                    label="Download CSV File",
                    data=csv,
                    file_name=(
                        f"schedule_export_"
                        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    ),
                    mime="text/csv",
                )

            elif export_format == "JSON":
                json_data = json.dumps(st.session_state.current_schedule, indent=2)

                _ = st.download_button(
                    label="Download JSON File",
                    data=json_data,
                    file_name=(
                        f"schedule_export_"
                        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    ),
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


def main():
    """Main Streamlit application"""
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

    # Route to appropriate page
    if page == "🏠 Dashboard":
        render_dashboard_page(scheduler)
    elif page == "📊 Schedule View":
        render_schedule_view_page()
    elif page == "📅 Timetable View":
        render_timetable_page()
    elif page == "📈 Statistics":
        render_statistics_page()
    elif page == "⚙️ Settings":
        render_settings_page(scheduler)
    elif page == "📤 Export":
        render_export_page(scheduler)


if __name__ == "__main__":
    main()
