import os

from .se_course_scheduler import CourseScheduler


def main():

    print("SE COURSE SCHEDULING AGENT - POC".center(80))

    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file_path))
    prolog_path = os.path.join(project_root, "data", "scheduler.pl")

    scheduler = CourseScheduler(prolog_path)

    print("\n[Using built-in Prolog data]")

    print("\nAttempting to schedule all courses...")
    result = scheduler.schedule_courses()

    if not result:
        print("\n❌ Unable to schedule courses - no valid schedule exists")
    elif result.get("status") == "partial_failure":
        unscheduled = result.get("unscheduled", [])
        print(
            f"\n⚠️  Partially scheduled: {len(result['schedules'])}/{result['total']} courses"
        )
        print(f"  Failed to schedule: {', '.join(unscheduled)}")
    else:
        print(
            f"\n✅ Successfully scheduled {len(result['schedules'])}/{result['total']} courses"
        )
        print(f"  Algorithm used: {result.get('algorithm_used', 'Unknown')}")

        schedule = scheduler.get_schedule()
        if schedule:
            print("\n" + "-" * 80)
            print("SCHEDULE SUMMARY")
            print("-" * 80)
            for item in schedule:
                print(f"  {item['course_name']} ({item['course_id']})")
                print(f"    Professor: {item['professor']}")
                print(
                    f"    Room: {item['room']}, {item['day']} {item['timeslot']} ({item['time_range']})"
                )
                print()

    print("\n" + "=" * 80)
    print("Scheduling Complete!".center(80))
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
