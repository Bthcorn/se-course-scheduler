from typing import Any, final
from pyswip import Prolog
from .excel_handler import ExcelHandler


@final
class CourseScheduler:

    prolog: Prolog
    excel_handler: ExcelHandler

    def __init__(self, prolog_file: str = "data/scheduler.pl"):
        self.prolog = Prolog()
        self.excel_handler = ExcelHandler(self.prolog)
        self.prolog_file = prolog_file

        try:
            self.prolog.consult(prolog_file)
            print(f"Loaded Prolog knowledge base from {prolog_file}")
        except Exception as e:
            print(f"Error loading Prolog file: {e}")
            raise

    def load_courses_from_excel(self, excel_file: str) -> None:
        self.excel_handler.load_courses_from_excel(excel_file)

    def load_professors_from_excel(self, excel_file: str) -> None:
        self.excel_handler.load_professors_from_excel(excel_file)

    def clear_schedule(self) -> None:
        query = "clear_schedule"
        _ = list(self.prolog.query(query))

    def reset_to_defaults(self) -> None:
        self.prolog.retractall("course(_, _, _)")
        self.prolog.retractall("professor(_, _)")
        self.prolog.retractall("can_teach(_, _)")
        self.prolog.retractall("prefers(_, _, _)")
        self.clear_schedule()

        try:
            self.prolog.consult(self.prolog_file)
            print(f"Reset to default Prolog facts from {self.prolog_file}")
        except Exception as e:
            print(f"Error reloading Prolog file: {e}")
            raise

    def schedule_courses(self) -> dict[str, Any]:
        self.clear_schedule()

        courses_query = "course(CourseID, _, _)"
        all_courses_result: list[dict[str, Any]] = list(
            self.prolog.query(courses_query)
        )

        if not all_courses_result:
            return {}

        all_course_ids = [str(c["CourseID"]) for c in all_courses_result]
        csp_query = "schedule_all_with_forward_checking"
        algorithm_used = "CSP with MCV + Forward Checking"

        try:
            csp_result = list(self.prolog.query(csp_query))

            if not csp_result:
                partial_schedule = self.get_schedule()

                if not partial_schedule:
                    return {}

                scheduled_ids = [s["course_id"] for s in partial_schedule]
                unscheduled_ids = [
                    cid for cid in all_course_ids if cid not in scheduled_ids
                ]

                self.clear_schedule()

                return {
                    "schedules": [],
                    "total": len(all_course_ids),
                    "unscheduled": unscheduled_ids,
                    "algorithm_used": algorithm_used,
                    "status": "partial_failure",
                }

        except Exception as e:
            print(f"CSP scheduling error: {e}")
            return {}

        schedule_details = self.get_schedule()

        if not schedule_details:
            return {}

        schedules_with_flags = []

        for detail in schedule_details:
            course_id = detail["course_id"]
            prof_name = detail["professor"]
            day = detail["day"]
            timeslot = detail["timeslot"]

            has_pref_query = f"can_teach(ProfID, {course_id}), professor(ProfID, '{prof_name}'), has_preference(ProfID)"
            has_pref_result = list(self.prolog.query(has_pref_query))

            if has_pref_result:
                prof_id_query = f"professor(ProfID, '{prof_name}')"
                prof_id_result = list(self.prolog.query(prof_id_query))

                if prof_id_result:
                    prof_id = prof_id_result[0]["ProfID"]

                    pref_match_query = f"prefers({prof_id}, {day}, {timeslot})"
                    pref_match = list(self.prolog.query(pref_match_query))

                    pref_wildcard_query = f"prefers({prof_id}, _, {timeslot})"
                    pref_wildcard = list(self.prolog.query(pref_wildcard_query))

                    if not pref_match and not pref_wildcard:
                        flag = "preference_not_met"
                    else:
                        flag = None
                else:
                    flag = None
            else:
                flag = None

            schedules_with_flags.append((detail, flag))

        return {
            "schedules": schedules_with_flags,
            "total": len(all_course_ids),
            "unscheduled": [],
            "algorithm_used": algorithm_used,
            "status": "success",
        }

    def get_schedule(self) -> list[dict[str, str]]:
        """Retrieve the complete schedule"""
        query = (
            "scheduled(ProfID, Room, Day, TimeSlot, CourseID), "
            "course(CourseID, CourseName, Year), "
            "professor(ProfID, ProfName), "
            "time_slot(Day, TimeSlot, TimeRange)"
        )
        results: list[dict[str, Any]] = list(self.prolog.query(query))

        if not results:
            return []

        schedule: list[dict[str, str]] = []
        for r in results:
            schedule.append(
                {
                    "course_id": str(r["CourseID"]),
                    "course_name": str(r["CourseName"]),
                    "year": str(r["Year"]),
                    "professor": str(r["ProfName"]),
                    "room": str(r["Room"]),
                    "day": str(r["Day"]),
                    "timeslot": str(r["TimeSlot"]),
                    "time_range": str(r["TimeRange"]),
                }
            )

        return schedule
