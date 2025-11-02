"""
Export page for the Streamlit application
"""

from datetime import datetime
import json
import os
import streamlit as st
import pandas as pd
from web.utils import check_scheduler_initialized
from web.pages.base_page import BasePage


class ExportPage(BasePage):
    """Export page class"""

    def render(self):
        """Render the Export page"""
        _ = st.header("Export Schedule")

        if not st.session_state.schedule_generated:
            _ = st.warning("No schedule to export. Please generate a schedule first.")
            return

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
                    output_file = (
                        f"schedule_export_"
                        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    )
                    self.scheduler = check_scheduler_initialized(self.scheduler)
                    self.scheduler.export_to_excel(output_file)

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
