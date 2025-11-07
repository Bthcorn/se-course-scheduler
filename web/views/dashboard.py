import streamlit as st
from web.views.base_page import BasePage


class DashboardPage(BasePage):

    def render(self):
        st.title("SE Course Scheduler")

        # Available Rooms Section
        st.subheader("Available Rooms")

        # Get room data from Prolog
        rooms_query = "room(RoomID, Capacity)"
        rooms = list(self.scheduler.prolog.query(rooms_query))

        # Display rooms as buttons/chips
        if rooms:
            cols = st.columns(len(rooms))
            for idx, room_data in enumerate(rooms):
                with cols[idx]:
                    st.button(
                        str(room_data["RoomID"]).upper(),
                        key=f"room_btn_{idx}",
                        use_container_width=True,
                    )

        st.markdown("---")

        st.subheader("Course Data Overview")

        years = [1, 2, 3, 4]
        cols = st.columns(2)

        for idx, year in enumerate(years):
            with cols[idx % 2]:
                with st.container(border=True):
                    courses_query = f"course(CourseID, CourseName, {year}), can_teach(ProfID, CourseID), professor(ProfID, ProfName)"
                    courses = list(self.scheduler.prolog.query(courses_query))

                    if courses:
                        seen_courses = set()
                        course_list = []
                        for course in courses:
                            course_id = str(course["CourseID"])
                            if course_id not in seen_courses:
                                seen_courses.add(course_id)
                                course_name = str(course["CourseName"])
                                prof_name = str(course["ProfName"])
                                course_list.append(
                                    f"{len(course_list) + 1}. {course_name} ( Professor {prof_name} )"
                                )

                        st.markdown(f"**Year {year} ( {len(course_list)} courses )**")
                        for course_text in course_list:
                            st.text(course_text)
                    else:
                        st.markdown(f"**Year {year} ( 0 courses )**")
                        st.text("No courses available")

        st.markdown("---")

        st.subheader("Import Course Data")
        st.text("Upload your course information from Excel files (.xlsx, .xls)")

        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["xlsx", "xls"],
            key="course_upload",
            label_visibility="collapsed",
        )

        if uploaded_file is not None:
            try:
                import tempfile
                import os

                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".xlsx"
                ) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                with st.spinner("Loading data from Excel..."):
                    self.scheduler.prolog.retractall("course(_, _, _)")
                    self.scheduler.prolog.retractall("professor(_, _)")
                    self.scheduler.prolog.retractall("can_teach(_, _)")
                    self.scheduler.prolog.retractall("prefers(_, _, _)")

                    from src.se_course_scheduler.excel_handler import ExcelHandler

                    excel_handler = ExcelHandler(self.scheduler.prolog)
                    excel_handler.load_courses_from_excel(tmp_path)
                    excel_handler.load_professors_from_excel(tmp_path)

                os.unlink(tmp_path)

                st.success("✅ Successfully loaded course data from Excel!")
                st.info(
                    "ℹ️ Rooms and time slots are using hardcoded facts (not imported from Excel)"
                )

            except Exception as e:
                st.error(f"❌ Error loading Excel file: {str(e)}")
                st.info(
                    "Please ensure your Excel file has the required sheets: Courses, Professors, CanTeach, and optionally Preferences"
                )

        st.markdown("---")

        if st.button("Generate Schedules", type="primary", use_container_width=True):
            with st.spinner(
                "Generating schedules using CSP with MCV + Forward Checking..."
            ):
                result = self.scheduler.schedule_courses()

                if not result:
                    st.error(
                        "❌ Unable to arrange all courses with current constraints"
                    )
                    st.markdown(
                        """
                        <script>
                        alert("Unable to arrange all courses! No valid schedule exists.");
                        </script>
                        """,
                        unsafe_allow_html=True,
                    )
                elif result.get("status") == "partial_failure":
                    unscheduled = result.get("unscheduled", [])
                    st.error(
                        f"❌ Could not schedule {len(unscheduled)} courses: {', '.join(unscheduled)}"
                    )
                    st.info(
                        f"Algorithm used: {result.get('algorithm_used', 'Unknown')}"
                    )
                    st.warning(
                        "Try reducing constraints (fewer reserved slots) or adding more rooms/time slots"
                    )
                else:
                    st.session_state.schedule_result = result
                    st.session_state.schedule_generated = True

                    flagged_count = sum(
                        1
                        for _, flag in result["schedules"]
                        if flag == "preference_not_met"
                    )
                    total_scheduled = len(result["schedules"])

                    st.session_state.generation_message = f"✅ Successfully scheduled {total_scheduled}/{result['total']} courses!"
                    st.session_state.generation_info = f"ℹ️ Algorithm: {result.get('algorithm_used', 'CSP Backtracking')}"

                    if flagged_count > 0:
                        st.session_state.generation_warning = f"⚠️ {flagged_count} courses did not get their preferred time slots (but all courses are scheduled)"

                    st.rerun()

        if "generation_message" in st.session_state:
            st.success(st.session_state.generation_message)
            del st.session_state.generation_message

        if "generation_info" in st.session_state:
            st.info(st.session_state.generation_info)
            del st.session_state.generation_info

        if "generation_warning" in st.session_state:
            st.warning(st.session_state.generation_warning)
            del st.session_state.generation_warning
