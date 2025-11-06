"""
Course Scheduling Agent for SE Program
Using PySWIP to interface with Prolog scheduling logic
"""

from typing import Any, final
from pyswip import Prolog
from .excel_handler import ExcelHandler


@final
class CourseScheduler:
    """Main class for course scheduling using Prolog"""

    prolog: Prolog
    excel_handler: ExcelHandler

    def __init__(self, prolog_file: str = "data/scheduler.pl"):
        """Initialize the scheduler with Prolog knowledge base"""
        self.prolog = Prolog()
        self.excel_handler = ExcelHandler(self.prolog)

        # Load the Prolog file
        try:
            self.prolog.consult(prolog_file)
            print(f"✓ Loaded Prolog knowledge base from {prolog_file}")
        except Exception as e:
            print(f"✗ Error loading Prolog file: {e}")
            raise

    def load_courses_from_excel(self, excel_file: str) -> None:
        """Load courses from Excel file and assert into Prolog"""
        self.excel_handler.load_courses_from_excel(excel_file)

    def load_professors_from_excel(self, excel_file: str) -> None:
        """Load professors and their capabilities from Excel"""
        self.excel_handler.load_professors_from_excel(excel_file)

    def load_all_data_from_excel(self, excel_file: str) -> None:
        """Load all data (courses and professors) from Excel file"""
        self.excel_handler.load_all_data_from_excel(excel_file)

    def get_excel_handler(self) -> ExcelHandler:
        """Get the Excel handler for direct access to Excel operations"""
        return self.excel_handler

    def clear_schedule(self) -> None:
        """Clear all scheduled courses"""
        query = "clear_schedule"
        _ = list(self.prolog.query(query))

    def get_courses_with_preferences(self) -> list[str]:
        """
        Get list of courses taught by professors who have time preferences.
        
        Returns:
            List of course IDs where at least one qualified professor has preferences
        """
        courses_query = "course(CourseID, _, _)"
        all_courses: list[dict[str, Any]] = list(self.prolog.query(courses_query))
        
        courses_with_prefs: list[str] = []
        
        for course in all_courses:
            course_id = str(course["CourseID"])
            
            # Check if any professor who can teach this course has preferences
            has_pref_query = f"can_teach(ProfID, {course_id}), has_preference(ProfID)"
            has_pref = list(self.prolog.query(has_pref_query))
            
            if has_pref:
                courses_with_prefs.append(course_id)
        
        return courses_with_prefs

    def get_courses_without_preferences(self) -> list[str]:
        """
        Get list of courses taught by professors without time preferences.
        
        Returns:
            List of course IDs where no qualified professor has preferences (flexible)
        """
        courses_query = "course(CourseID, _, _)"
        all_courses: list[dict[str, Any]] = list(self.prolog.query(courses_query))
        
        courses_without_prefs: list[str] = []
        
        for course in all_courses:
            course_id = str(course["CourseID"])
            
            # Check if any professor who can teach this course has preferences
            has_pref_query = f"can_teach(ProfID, {course_id}), has_preference(ProfID)"
            has_pref = list(self.prolog.query(has_pref_query))
            
            if not has_pref:
                courses_without_prefs.append(course_id)
        
        return courses_without_prefs

    def schedule_courses(self) -> dict[str, Any]:
        """
        Schedule all courses using CSP with MCV + Forward Checking.
        Automatically clears previous schedule before scheduling.
        
        Algorithm: MCV + Forward Checking
        - Uses Most Constrained Variable heuristic (schedule hard courses first)
        - Uses Forward Checking to prune search space after each assignment
        - Full backtracking ensures complete and sound solutions
        - Optimal balance between speed and quality
        
        Returns:
            dict with:
                - schedules: list of (course_data, flag) tuples
                  flag = "preference_not_met" if course didn't get preferred slot
                - total: total number of courses
                - unscheduled: list of course IDs that couldn't be scheduled
                - algorithm_used: which algorithm was used
                
            If returned dict is empty {}, it means scheduling is impossible.
        """
        # Always clear previous schedule first
        self.clear_schedule()
        
        # Get all courses
        courses_query = "course(CourseID, _, _)"
        all_courses_result: list[dict[str, Any]] = list(self.prolog.query(courses_query))
        
        if not all_courses_result:
            return {}  # No courses to schedule
        
        # Extract course IDs
        all_course_ids = [str(c["CourseID"]) for c in all_courses_result]
        
        # Use MCV + Forward Checking
        csp_query = "schedule_all_with_forward_checking"
        algorithm_used = "CSP with MCV + Forward Checking"
        
        try:
            # Execute CSP scheduling
            # This will either succeed (scheduling all courses) or fail (backtrack exhausted all possibilities)
            csp_result = list(self.prolog.query(csp_query))
            
            if not csp_result:
                # CSP failed - no valid complete schedule exists
                # Check partial schedule for debugging
                partial_schedule = self.get_schedule()
                
                if not partial_schedule:
                    # Truly impossible - no courses could be scheduled
                    return {}
                
                # Some courses were scheduled before failure
                scheduled_ids = [s["course_id"] for s in partial_schedule]
                unscheduled_ids = [cid for cid in all_course_ids if cid not in scheduled_ids]
                
                # Clear the partial schedule
                self.clear_schedule()
                
                return {
                    "schedules": [],
                    "total": len(all_course_ids),
                    "unscheduled": unscheduled_ids,
                    "algorithm_used": algorithm_used,
                    "status": "partial_failure"
                }
            
        except Exception as e:
            # Prolog query error
            print(f"CSP scheduling error: {e}")
            return {}
        
        # CSP succeeded! Get the full schedule
        schedule_details = self.get_schedule()
        
        if not schedule_details:
            # This shouldn't happen if CSP succeeded, but handle it
            return {}
        
        # Analyze which courses didn't get their preferred slots
        schedules_with_flags = []
        
        for detail in schedule_details:
            course_id = detail["course_id"]
            prof_name = detail["professor"]
            day = detail["day"]
            timeslot = detail["timeslot"]
            
            # Check if this course is taught by a professor with preferences
            has_pref_query = f"can_teach(ProfID, {course_id}), professor(ProfID, '{prof_name}'), has_preference(ProfID)"
            has_pref_result = list(self.prolog.query(has_pref_query))
            
            if has_pref_result:
                # Professor has preferences - check if this slot matches
                prof_id_query = f"professor(ProfID, '{prof_name}')"
                prof_id_result = list(self.prolog.query(prof_id_query))
                
                if prof_id_result:
                    prof_id = prof_id_result[0]["ProfID"]
                    
                    # Check if scheduled slot matches preference
                    pref_match_query = f"prefers({prof_id}, {day}, {timeslot})"
                    pref_match = list(self.prolog.query(pref_match_query))
                    
                    # Also check wildcard preferences (day = '_')
                    pref_wildcard_query = f"prefers({prof_id}, _, {timeslot})"
                    pref_wildcard = list(self.prolog.query(pref_wildcard_query))
                    
                    if not pref_match and not pref_wildcard:
                        # Has preference but didn't get it
                        flag = "preference_not_met"
                    else:
                        flag = None
                else:
                    flag = None
            else:
                # No preferences for this course
                flag = None
            
            schedules_with_flags.append((detail, flag))
        
        return {
            "schedules": schedules_with_flags,
            "total": len(all_course_ids),
            "unscheduled": [],  # Empty if CSP succeeded
            "algorithm_used": algorithm_used,
            "status": "success"
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

    def get_reserved_slots(self) -> list[dict[str, str]]:
        """Retrieve all reserved time slots"""
        query = "reserved(Room, Day, TimeSlot, Reason), time_slot(Day, TimeSlot, TimeRange)"
        results: list[dict[str, Any]] = list(self.prolog.query(query))

        if not results:
            return []

        reserved: list[dict[str, str]] = []
        for r in results:
            reserved.append(
                {
                    "room": str(r["Room"]),
                    "day": str(r["Day"]),
                    "timeslot": str(r["TimeSlot"]),
                    "time_range": str(r["TimeRange"]),
                    "reason": str(r["Reason"]),
                }
            )

        return reserved

    def get_room_schedule(self, room: str) -> list[dict[str, str]]:
        """Get schedule for a specific room"""
        query = (
            f"scheduled(ProfID, {room}, Day, TimeSlot, CourseID), "
            "course(CourseID, CourseName, _), "
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
                    "professor": str(r["ProfName"]),
                    "day": str(r["Day"]),
                    "timeslot": str(r["TimeSlot"]),
                    "time_range": str(r["TimeRange"]),
                }
            )

        return schedule

    def get_statistics(self) -> dict[str, Any]:
        """Get scheduling statistics"""
        stats: dict[str, Any] = {}

        # Count scheduled courses
        count_query = "count_scheduled(Count)"
        count_result: list[dict[str, Any]] = list(self.prolog.query(count_query))
        stats["scheduled_courses"] = (
            int(count_result[0]["Count"]) if count_result else 0
        )

        # Get professor workload
        workload_query = "professor_workload(ProfID, ProfName, Count)"
        workload_results: list[dict[str, Any]] = list(self.prolog.query(workload_query))
        stats["professor_workload"] = [
            {
                "id": str(r["ProfID"]),
                "name": str(r["ProfName"]),
                "courses": int(r["Count"]),
            }
            for r in workload_results
        ]

        # Get room utilization
        room_query = "room_utilization(Room, Used, Total, Percentage)"
        room_results: list[dict[str, Any]] = list(self.prolog.query(room_query))
        stats["room_utilization"] = [
            {
                "room": str(r["Room"]),
                "used_slots": int(r["Used"]),
                "total_slots": int(r["Total"]),
                "utilization": float(r["Percentage"]),
            }
            for r in room_results
        ]

        return stats

    def export_to_excel(self, output_file: str = "generated_schedule.xlsx") -> None:
        """Export schedule to Excel file organized by rooms"""
        schedule = self.get_schedule()
        reserved = self.get_reserved_slots()
        stats = self.get_statistics()

        self.excel_handler.export_schedule_to_excel(
            schedule, reserved, stats, output_file
        )