"""
Main module for the SE Course Scheduler
"""

import os

from .se_course_scheduler import CourseScheduler


def main():
    """Main function to demonstrate the scheduler"""

    print("\n" + "=" * 80)
    print("SE COURSE SCHEDULING AGENT - POC".center(80))
    print("=" * 80 + "\n")

    # Initialize scheduler
    # Determine the correct path to scheduler.pl
    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file_path))
    prolog_path = os.path.join(project_root, "data", "scheduler.pl")

    scheduler = CourseScheduler(prolog_path)

    # Option 1: Use built-in data from Prolog file
    print("\n[Using built-in Prolog data]")

    # Schedule all courses
    print("\nAttempting to schedule all courses...")
    result = scheduler.schedule_all_courses()

    print("\nScheduling Results:")
    print(f"  Successfully scheduled: {len(result['scheduled'])} courses")
    print(f"  Failed to schedule: {len(result['failed'])} courses")
    print(f"  Success rate: {result['success_rate']:.1f}%")

    if result["failed"]:
        print(f"  Failed courses: {', '.join(result['failed'])}")

    # Validate schedule
    print("\nValidating schedule...")
    _ = scheduler.validate_schedule()

    # Print summary
    scheduler.print_schedule_summary()

    # Get statistics
    stats = scheduler.get_statistics()
    print("\n" + "-" * 80)
    print("PROFESSOR WORKLOAD")
    print("-" * 80)
    for prof in stats.get("professor_workload", []):
        if prof["courses"] > 0:
            print(f"  {prof['name']}: {prof['courses']} course(s)")

    # Export to Excel
    print("\nExporting schedule to Excel...")
    scheduler.export_to_excel("generated_schedule.xlsx")

    print("\n" + "=" * 80)
    print("Scheduling Complete!".center(80))
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
