"""
Statistics page for the Streamlit application
"""

from typing import Any
import streamlit as st
import pandas as pd
import plotly.express as px
from web.pages.base_page import BasePage


class StatisticsPage(BasePage):
    """Statistics page class"""

    @staticmethod
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

    @staticmethod
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

    def render(self):
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
            self.create_professor_workload_chart(st.session_state.current_stats)

        # Room utilization
        _ = st.subheader("Room Utilization")
        if not st.session_state.current_stats.get("room_utilization"):
            _ = st.info("No room utilization data available.")
        else:
            self.create_room_utilization_chart(st.session_state.current_stats)

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
