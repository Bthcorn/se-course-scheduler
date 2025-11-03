"""
Dashboard page for the Streamlit application
"""

import streamlit as st
import streamlit_shadcn_ui as ui
from web.utils import check_scheduler_initialized, display_messages
from web.components import display_schedule_table
from web.views.base_page import BasePage


class DashboardPage(BasePage):
    """Dashboard page class"""

    @staticmethod
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
            width="stretch",
        )

    def render(self):
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
            result = st.session_state.get("schedule_result", {})
            success_rate = result.get("success_rate", 0)
            ui.metric_card(
                title="Success Rate",
                content=f"{success_rate:.1f}%" if success_rate > 0 else "N/A",
                description="success rate",
                key="success_rate_card",
            )

        # Quick actions
        _ = st.markdown("### Quick Actions")
        _ = st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            with st.container():
                if self.render_action_card(
                    title="🔄 Schedule Courses",
                    description="Generate schedule for all available courses",
                    button_text="Schedule All Courses",
                    button_key="schedule_courses_btn",
                    button_variant="default",
                    gradient_start="#667eea",
                    gradient_end="#764ba2",
                    border_color="#667eea",
                ):
                    self.scheduler = check_scheduler_initialized(self.scheduler)

                    with st.spinner("Scheduling courses..."):
                        result = self.scheduler.schedule_all_courses()
                        st.session_state.schedule_result = result
                        st.session_state.schedule_generated = True
                        st.session_state.current_schedule = (
                            self.scheduler.get_schedule()
                        )
                        st.session_state.current_reserved = (
                            self.scheduler.get_reserved_slots()
                        )
                        st.session_state.current_stats = self.scheduler.get_statistics()

                        if result.get("scheduled"):
                            st.session_state.success_message = (
                                f"Successfully scheduled "
                                f"{len(result['scheduled'])} courses!"
                            )

                        if result.get("failed"):
                            st.session_state.warning_message = (
                                f"Failed to schedule {len(result['failed'])} "
                                f"courses: {', '.join(result['failed'])}"
                            )

                        st.rerun()

        with col2:
            with st.container():
                if self.render_action_card(
                    title="🗑️ Clear Schedule",
                    description="Remove all scheduled courses and reset",
                    button_text="Clear Schedule",
                    button_key="clear_schedule_btn",
                    button_variant="destructive",
                    gradient_start="#f093fb",
                    gradient_end="#f5576c",
                    border_color="#f5576c",
                ):
                    self.scheduler = check_scheduler_initialized(self.scheduler)

                    self.scheduler.clear_schedule()
                    st.session_state.schedule_generated = False
                    st.session_state.current_schedule = []
                    st.session_state.current_reserved = []
                    st.session_state.current_stats = {}
                    st.session_state.schedule_result = {}
                    st.session_state.success_message = "Schedule cleared!"
                    st.rerun()

        with col3:
            with st.container():
                if self.render_action_card(
                    title="✅ Validate Schedule",
                    description="Check for conflicts and constraint violations",
                    button_text="Validate Schedule",
                    button_key="validate_btn",
                    button_variant="outline",
                    gradient_start="#4facfe",
                    gradient_end="#00f2fe",
                    border_color="#4facfe",
                ):
                    self.scheduler = check_scheduler_initialized(self.scheduler)

                    if self.scheduler.validate_schedule():
                        st.session_state.success_message = (
                            "Schedule validation passed - No conflicts found!"
                        )
                    else:
                        st.session_state.warning_message = (
                            "Schedule validation failed - Conflicts detected!"
                        )

                    # Refresh to show the message
                    st.rerun()

        # Recent schedule preview
        if st.session_state.current_schedule:
            _ = st.markdown("<br>", unsafe_allow_html=True)
            _ = st.subheader("Recent Schedule Preview")
            display_schedule_table(
                st.session_state.current_schedule[:10], "Recent Schedule"
            )

            if len(st.session_state.current_schedule) > 10:
                _ = st.info(
                    f"Showing first 10 of {len(st.session_state.current_schedule)} "
                    "scheduled courses. Use 'Timetable View' for complete details."
                )
