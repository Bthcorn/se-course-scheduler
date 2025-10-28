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
        print("✓ Cleared existing schedule")

    def schedule_course(self, course_id: str) -> bool:
        """Schedule a specific course"""
        query = f"schedule_course({course_id})"
        results = list(self.prolog.query(query))

        if results:
            print(f"✓ Scheduled course: {course_id}")
            return True
        else:
            print(f"✗ Could not schedule course: {course_id}")
            return False

    def schedule_all_courses(self) -> dict[str, Any]:
        """Attempt to schedule all courses"""
        # Get all courses
        courses_query = "course(CourseID, _, _, _, _)"
        courses: list[dict[str, Any]] = list(self.prolog.query(courses_query))
        self.clear_schedule()

        scheduled: list[str] = []
        failed: list[str] = []

        # Try to schedule each course
        for course in courses:
            course_id = str(course["CourseID"])
            if self.schedule_course(course_id):
                scheduled.append(course_id)
            else:
                failed.append(course_id)

        return {
            "scheduled": scheduled,
            "failed": failed,
            "total": len(courses),
            "success_rate": len(scheduled) / len(courses) * 100 if courses else 0,
        }

    def get_schedule(self) -> list[dict[str, str]]:
        """Retrieve the complete schedule"""
        query = (
            "scheduled(ProfID, Room, Day, Period, CourseID), "
            "course(CourseID, CourseName, _, _, _), "
            "professor(ProfID, ProfName), "
            "time_slot(Day, Period, TimeRange)"
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
                    "room": str(r["Room"]),
                    "day": str(r["Day"]),
                    "period": str(r["Period"]),
                    "time_range": str(r["TimeRange"]),
                }
            )

        return schedule

    def get_reserved_slots(self) -> list[dict[str, str]]:
        """Retrieve all reserved time slots"""
        query = "reserved(Room, Day, Period, Reason), time_slot(Day, Period, TimeRange)"
        results: list[dict[str, Any]] = list(self.prolog.query(query))

        if not results:
            return []

        reserved: list[dict[str, str]] = []
        for r in results:
            reserved.append(
                {
                    "room": str(r["Room"]),
                    "day": str(r["Day"]),
                    "period": str(r["Period"]),
                    "time_range": str(r["TimeRange"]),
                    "reason": str(r["Reason"]),
                }
            )

        return reserved

    def get_room_schedule(self, room: str) -> list[dict[str, str]]:
        """Get schedule for a specific room"""
        query = (
            f"scheduled(ProfID, {room}, Day, Period, CourseID), "
            "course(CourseID, CourseName, _, _, _), "
            "professor(ProfID, ProfName), "
            "time_slot(Day, Period, TimeRange)"
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
                    "period": str(r["Period"]),
                    "time_range": str(r["TimeRange"]),
                }
            )

        return schedule

    def validate_schedule(self) -> bool:
        """Validate the schedule for conflicts"""
        query = "validate_schedule"
        results: list[dict[str, Any]] = list(self.prolog.query(query))

        if results:
            print("✓ Schedule validation passed - No conflicts found")
            return True
        else:
            print("✗ Schedule validation failed - Conflicts detected")
            return False

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

    def print_schedule_summary(self) -> None:
        """Print a formatted summary of the schedule"""
        schedule = self.get_schedule()
        reserved = self.get_reserved_slots()

        print("\n" + "=" * 80)
        print("GENERATED SCHEDULE SUMMARY".center(80))
        print("=" * 80 + "\n")

        # Get all rooms that have either scheduled or reserved slots
        all_rooms: set[str] = set()
        for item in schedule:
            all_rooms.add(item["room"])
        for item in reserved:
            all_rooms.add(item["room"])

        if not schedule and not reserved:
            print("No courses scheduled and no reserved slots.")
            return

        for room in sorted(all_rooms):
            print(f"\n{'Room ' + room.upper():^80}")
            print("-" * 80)
            print(
                f"{'Day':<12} {'Period':<12} {'Time':<15} {'Course/Activity':<25} {'Professor/Organizer':<20}"
            )
            print("-" * 80)

            # Get all time slots for this room
            room_schedule: list[dict[str, Any]] = [
                cls for cls in schedule if cls["room"] == room
            ]
            room_reserved: list[dict[str, Any]] = [
                res for res in reserved if res["room"] == room
            ]

            # Combine and sort all slots
            all_slots: list[dict[str, Any]] = []

            # Add scheduled courses
            for cls in room_schedule:
                course_slot: dict[str, Any] = {
                    "day": cls["day"],
                    "period": cls["period"],
                    "time_range": cls["time_range"],
                    "activity": cls["course_name"],
                    "person": cls["professor"],
                    "type": "course",
                }
                all_slots.append(course_slot)

            # Add reserved slots
            for res in room_reserved:
                reserved_slot: dict[str, Any] = {
                    "day": res["day"],
                    "period": res["period"],
                    "time_range": res["time_range"],
                    "activity": f"[RESERVED] {res['reason']}",
                    "person": "N/A",
                    "type": "reserved",
                }
                all_slots.append(reserved_slot)

            # Sort by day and period
            for slot in sorted(all_slots, key=lambda x: (x["day"], x["period"])):
                print(
                    f"{slot['day']:<12} {slot['period']:<12} {slot['time_range']:<15} {slot['activity']:<25} {slot['person']:<20}"
                )

        print("\n" + "=" * 80)

        # Print statistics
        stats = self.get_statistics()
        print(f"\nTotal Scheduled Courses: {stats['scheduled_courses']}")
        print("\nRoom Utilization:")
        room_util_data = stats.get("room_utilization", [])
        if isinstance(room_util_data, list):
            for room_stat in room_util_data:
                room_name = str(room_stat["room"]).upper()
                utilization_str = (
                    f"  {room_name}: {room_stat['utilization']:.1f}% "
                    f"({room_stat['used_slots']}/{room_stat['total_slots']} slots)"
                )
                print(utilization_str)
