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
        self.prolog_file = prolog_file

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

    def clear_schedule(self) -> None:
        """Clear all scheduled courses"""
        query = "clear_schedule"
        _ = list(self.prolog.query(query))

    def reset_to_defaults(self) -> None:
        """
        Reset all dynamic data to default Prolog facts.
        Clears all courses, professors, teaching capabilities, preferences, and schedules,
        then reloads the default facts from the Prolog file.
        """
        # Clear all dynamic facts
        self.prolog.retractall("course(_, _, _)")
        self.prolog.retractall("professor(_, _)")
        self.prolog.retractall("can_teach(_, _)")
        self.prolog.retractall("prefers(_, _, _)")
        self.clear_schedule()
        
        # Reload the Prolog file to restore default facts
        try:
            self.prolog.consult(self.prolog_file)
            print(f"✓ Reset to default Prolog facts from {self.prolog_file}")
        except Exception as e:
            print(f"✗ Error reloading Prolog file: {e}")
            raise

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
