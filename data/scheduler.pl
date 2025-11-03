% scheduler.pl - Course Scheduling Agent for SE Program
% This file contains the Prolog logic for course scheduling

% ==================== FACTS ====================

% Define available rooms with capacity
room(ecc802, 40).
room(ecc803, 40).
room(ecc804, 30).
room(ecc805, 30).
room(ecc806, 50).

% Define time slots: time_slot(Day, Period, TimeRange)
time_slot(monday, morning, '09:00-12:00').
time_slot(monday, afternoon, '13:00-16:00').
time_slot(monday, evening, '17:00-20:00').
time_slot(tuesday, morning, '09:00-12:00').
time_slot(tuesday, afternoon, '13:00-16:00').
time_slot(tuesday, evening, '17:00-20:00').
time_slot(wednesday, morning, '09:00-12:00').
time_slot(wednesday, afternoon, '13:00-16:00').
time_slot(wednesday, evening, '17:00-20:00').
time_slot(thursday, morning, '09:00-12:00').
time_slot(thursday, afternoon, '13:00-16:00').
time_slot(thursday, evening, '17:00-20:00').
time_slot(friday, morning, '09:00-12:00').
time_slot(friday, afternoon, '13:00-16:00').
time_slot(friday, evening, '17:00-20:00').
time_slot(saturday, morning, '09:00-12:00').
time_slot(saturday, afternoon, '13:00-16:00').
time_slot(saturday, evening, '17:00-20:00').
time_slot(sunday, morning, '09:00-12:00').
time_slot(sunday, afternoon, '13:00-16:00').
time_slot(sunday, evening, '17:00-20:00').

% Define courses: course(CourseID, CourseName, Year, RequiredCapacity, Prerequisites)
course(cs101, 'Programming Fundamentals', 1, 35, []).
course(cs102, 'Data Structures', 1, 35, [cs101]).
course(cs103, 'Discrete Mathematics', 1, 30, []).
course(cs201, 'Database Systems', 2, 35, [cs101]).
course(cs202, 'Web Development', 2, 30, [cs101]).
course(cs203, 'Algorithm Design', 2, 35, [cs102]).
course(cs301, 'Software Engineering', 3, 35, [cs201, cs202]).
course(cs302, 'AI', 3, 30, [cs203]).
course(cs303, 'UI/UX Design', 3, 25, [cs202]).
course(cs401, 'Machine Learning', 4, 30, [cs302]).
course(cs402, 'Mobile Development', 4, 25, [cs202]).
course(cs403, 'Cloud Computing', 4, 30, [cs201]).

% Define professors: professor(ProfID, ProfName)
professor(p001, 'Dr. Smith').
professor(p002, 'Dr. Johnson').
professor(p003, 'Dr. Williams').
professor(p004, 'Dr. Brown').
professor(p005, 'Dr. Davis').
professor(p006, 'Dr. Wilson').
professor(p007, 'Dr. Taylor').
professor(p008, 'Dr. Anderson').
professor(p009, 'Dr. Martin').
professor(p010, 'Dr. Garcia').

% Define professor preferences: prefers(ProfID, Day, Period)
prefers(p001, monday, morning).
prefers(p001, wednesday, afternoon).
prefers(p002, monday, morning).
prefers(p002, thursday, afternoon).
prefers(p003, monday, morning).
prefers(p003, friday, afternoon).
prefers(p004, monday, morning).
prefers(p004, wednesday, afternoon).
prefers(p004, friday, morning).
prefers(p005, monday, morning).
prefers(p005, friday, morning).
prefers(p006, thursday, afternoon).
prefers(p007, monday, morning).
prefers(p007, wednesday, afternoon).
prefers(p008, tuesday, morning).
prefers(p008, thursday, afternoon).
prefers(p008, monday, morning).
prefers(p009, friday, morning).
prefers(p010, _, afternoon).


% Define professor capabilities: can_teach(ProfID, CourseID)
can_teach(p001, cs302).  % Dr. Smith - AI
can_teach(p001, cs401).  % Dr. Smith - ML
can_teach(p002, cs201).  % Dr. Johnson - DB
can_teach(p002, cs403).  % Dr. Johnson - Cloud
can_teach(p003, cs301).  % Dr. Williams - SE
can_teach(p004, cs202).  % Dr. Brown - Web Dev
can_teach(p004, cs303).  % Dr. Brown - UI/UX
can_teach(p005, cs102).  % Dr. Davis - Data Structures
can_teach(p006, cs203).  % Dr. Wilson - Algorithms
can_teach(p007, cs101).  % Dr. Taylor - Programming
can_teach(p008, cs402).  % Dr. Anderson - Mobile
can_teach(p009, cs401).  % Dr. Martin - ML
can_teach(p010, cs202).  % Dr. Garcia - Web
can_teach(p001, cs103).  % Dr. Smith - Discrete Mathematics

% ==================== DYNAMIC FACTS ====================
% These will store the generated schedule
:- dynamic scheduled/5.

% ==================== CONFLICTING SCHEDULES (FOR TESTING) ====================
% These predicates will cause validate_schedule to fail
% Conflict 1: Professor teaching two courses at the same time
% scheduled(p001, ecc802, monday, morning, cs302).   % Dr. Smith - AI
% scheduled(p001, ecc803, monday, morning, cs401).   % Dr. Smith - ML (conflict: same professor, same time)

% Conflict 2: Two courses in the same room at the same time
% scheduled(p002, ecc804, tuesday, afternoon, cs201).  % Dr. Johnson - DB
% scheduled(p003, ecc804, tuesday, afternoon, cs301). % Dr. Williams - SE (conflict: same room, same time)

% ==================== RULES ====================

% Check if room has sufficient capacity for course
room_suitable(Room, CourseID) :-
    room(Room, Capacity),
    course(CourseID, _, _, RequiredCapacity, _),
    Capacity >= RequiredCapacity.

% Check if a time slot is available (no existing assignment)
time_available(Room, Day, Period) :-
    \+ scheduled(_, Room, Day, Period, _),
    \+ reserved(Room, Day, Period, _).

% Check if professor is available at given time
professor_available(ProfID, Day, Period) :-
    \+ scheduled(ProfID, _, Day, Period, _).

% Check if course has already been scheduled
course_not_scheduled(CourseID) :-
    \+ scheduled(_, _, _, _, CourseID).

% Define reserved time slots: reserved(Room, Day, Period, Reason)
reserved(ecc802, monday, afternoon, 'Department Meeting').
reserved(ecc802, tuesday, afternoon, 'Faculty Development').
reserved(ecc803, wednesday, morning, 'Student Club Meeting').
reserved(ecc804, thursday, afternoon, 'Guest Lecture Series').
reserved(ecc805, friday, morning, 'Career Services Workshop').
reserved(ecc806, monday, morning, 'Administrative Meeting').
reserved(ecc802, wednesday, afternoon, 'Research Seminar').
reserved(ecc803, friday, afternoon, 'Department Social Event').

% Check if all prerequisites are satisfied
% For simplicity in POC, we assume prerequisites are scheduled in earlier semesters
prerequisites_met(CourseID) :-
    course(CourseID, _, _, _, _).  % Simplified - always true for POC

% Find a valid assignment for a course
find_assignment(CourseID, ProfID, Room, Day, Period) :-
    course(CourseID, _, _, _, _),
    can_teach(ProfID, CourseID),
    room_suitable(Room, CourseID),
    time_slot(Day, Period, _),
    time_available(Room, Day, Period),
    professor_available(ProfID, Day, Period),
    prerequisites_met(CourseID),
    course_not_scheduled(CourseID).

% Find assignment with professor preference
find_preferred_assignment(CourseID, ProfID, Room, Day, Period) :-
    find_assignment(CourseID, ProfID, Room, Day, Period),
    prefers(ProfID, Day, Period).

% Find assignment without preference (fallback)
find_fallback_assignment(CourseID, ProfID, Room, Day, Period) :-
    find_assignment(CourseID, ProfID, Room, Day, Period),
    \+ prefers(ProfID, Day, Period).

% Schedule a course with the best available option (prioritizes preferences)
schedule_course(CourseID) :-
    % First try to find an assignment with professor preference
    (
        find_preferred_assignment(CourseID, ProfID, Room, Day, Period),
        assertz(scheduled(ProfID, Room, Day, Period, CourseID))
        ;
    % If no preferred slot available, fall back to any valid assignment
        find_fallback_assignment(CourseID, ProfID, Room, Day, Period),
        assertz(scheduled(ProfID, Room, Day, Period, CourseID))
    ).

% Get all scheduled classes
get_schedule(Schedule) :-
    findall(
        schedule(CourseID, CourseName, ProfName, Room, Day, Period, TimeRange),
        (
            scheduled(ProfID, Room, Day, Period, CourseID),
            course(CourseID, CourseName, _, _, _),
            professor(ProfID, ProfName),
            time_slot(Day, Period, TimeRange)
        ),
        Schedule
    ).

% Get schedule for a specific room
get_room_schedule(Room, Schedule) :-
    findall(
        schedule(CourseID, CourseName, ProfName, Day, Period, TimeRange),
        (
            scheduled(ProfID, Room, Day, Period, CourseID),
            course(CourseID, CourseName, _, _, _),
            professor(ProfID, ProfName),
            time_slot(Day, Period, TimeRange)
        ),
        Schedule
    ).

% Clear all scheduled courses
clear_schedule :-
    retractall(scheduled(_, _, _, _, _)).

% Validate schedule - check for conflicts
validate_schedule :-
    \+ (
        scheduled(Prof, _, Day, Period, Course1),
        scheduled(Prof, _, Day, Period, Course2),
        Course1 \= Course2
    ),
    \+ (
        scheduled(_, Room, Day, Period, Course1),
        scheduled(_, Room, Day, Period, Course2),
        Course1 \= Course2
    ).

% Count scheduled courses
count_scheduled(Count) :-
    findall(1, scheduled(_, _, _, _, _), List),
    length(List, Count).

% Get professor workload
professor_workload(ProfID, ProfName, CourseCount) :-
    professor(ProfID, ProfName),
    findall(1, scheduled(ProfID, _, _, _, _), Courses),
    length(Courses, CourseCount).

% Get room utilization
room_utilization(Room, UsedSlots, TotalSlots, Percentage) :-
    room(Room, _),
    findall(1, scheduled(_, Room, _, _, _), Used),
    length(Used, UsedSlots),
    findall(1, reserved(Room, _, _, _), Reserved),
    length(Reserved, ReservedSlots),
    TotalSlots = 21,  % 7 days * 3 periods
    AvailableSlots is TotalSlots - ReservedSlots,
    Percentage is (UsedSlots / AvailableSlots) * 100.

% Get all reserved time slots
get_reserved_slots(ReservedList) :-
    findall(
        reserved(Room, Day, Period, TimeRange, Reason),
        (
            reserved(Room, Day, Period, Reason),
            time_slot(Day, Period, TimeRange)
        ),
        ReservedList
    ).
