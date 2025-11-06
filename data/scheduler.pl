% ==================== LOAD FACTS ====================
:- consult('unsat_facts.pl').

% ==================== DYNAMIC DECLARATIONS ====================
% Allow runtime modification of these predicates for Excel import
:- dynamic course/3.
:- dynamic professor/2.
:- dynamic can_teach/2.
:- dynamic prefers/3.

% ==================== CONSTRAINT RULES ====================

room_available(Room, Day, TimeSlot) :-
    \+ scheduled(_, Room, Day, TimeSlot, _),
    \+ reserved(Room, Day, TimeSlot, _).

professor_available(ProfID, Day, TimeSlot) :-
    \+ scheduled(ProfID, _, Day, TimeSlot, _).

course_not_scheduled(CourseID) :-
    \+ scheduled(_, _, _, _, CourseID).

% ==================== ASSIGNMENT FINDING RULES ====================

find_assignment(CourseID, ProfID, Room, Day, TimeSlot) :-
    course(CourseID, _, _),
    can_teach(ProfID, CourseID),
    time_slot(Day, TimeSlot, _),
    room(Room, _),
    room_available(Room, Day, TimeSlot),
    professor_available(ProfID, Day, TimeSlot),
    course_not_scheduled(CourseID).

find_preferred_assignment(CourseID, ProfID, Room, Day, TimeSlot) :-
    find_assignment(CourseID, ProfID, Room, Day, TimeSlot),
    prefers(ProfID, Day, TimeSlot).

find_fallback_assignment(CourseID, ProfID, Room, Day, TimeSlot) :-
    find_assignment(CourseID, ProfID, Room, Day, TimeSlot),
    \+ prefers(ProfID, Day, TimeSlot).

% Clear all scheduled courses
clear_schedule :-
    retractall(scheduled(_, _, _, _, _)).

% ==================== CSP SCHEDULING WITH BACKTRACKING ====================

% CSP scheduling for a single course - tries preferred first, then fallback
% Used by MCV and Forward Checking algorithms
schedule_course_csp(CourseID, ProfID, Room, Day, TimeSlot) :-
    % Try preferred assignment first
    find_preferred_assignment(CourseID, ProfID, Room, Day, TimeSlot).

schedule_course_csp(CourseID, ProfID, Room, Day, TimeSlot) :-
    % If preferred fails, try any valid assignment
    find_fallback_assignment(CourseID, ProfID, Room, Day, TimeSlot).

% ==================== HELPER PREDICATES FOR HEURISTICS ====================

% Count available slots for a course (lower = more constrained)
count_available_slots(CourseID, Count) :-
    findall(
        1,
        (
            can_teach(ProfID, CourseID),
            time_slot(Day, TimeSlot, _),
            room(Room, _),
            room_available(Room, Day, TimeSlot),
            professor_available(ProfID, Day, TimeSlot)
        ),
        Slots
    ),
    length(Slots, Count).

% Sort courses by number of available slots (ascending)
sort_by_constraints(Courses, SortedCourses) :-
    findall(
        Count-CourseID,
        (
            member(CourseID, Courses),
            count_available_slots(CourseID, Count)
        ),
        CountPairs
    ),
    keysort(CountPairs, SortedPairs),
    pairs_values(SortedPairs, SortedCourses).

% Extract values from key-value pairs
pairs_values([], []).
pairs_values([_-Value|Rest], [Value|Values]) :-
    pairs_values(Rest, Values).

% ==================== ADVANCED CSP: FORWARD CHECKING ====================

% Schedule with forward checking - prune domains after each assignment
schedule_all_with_forward_checking :-
    findall(CourseID, course(CourseID, _, _), AllCourses),
    sort_by_constraints(AllCourses, SortedCourses),
    schedule_with_fc(SortedCourses).

schedule_with_fc([]).  % Base case

schedule_with_fc([CourseID|Rest]) :-
    % Find valid assignment
    schedule_course_csp(CourseID, ProfID, Room, Day, TimeSlot),
    
    % Assert it
    assertz(scheduled(ProfID, Room, Day, TimeSlot, CourseID)),
    
    % Check if remaining courses still have valid assignments (forward checking)
    check_remaining_feasible(Rest),
    
    % Continue with rest
    schedule_with_fc(Rest).

% Check if all remaining courses have at least one valid assignment
check_remaining_feasible([]).
check_remaining_feasible([CourseID|Rest]) :-
    % Must have at least one valid assignment
    (find_preferred_assignment(CourseID, _, _, _, _) ; 
     find_fallback_assignment(CourseID, _, _, _, _)),
    check_remaining_feasible(Rest).

% ==================== QUERY RULES ====================

has_preference(ProfID) :-
    prefers(ProfID, _, _).

get_schedule(Schedule) :-
    findall(
        schedule(CourseID, CourseName, ProfName, Room, Day, TimeSlot, TimeRange),
        (
            scheduled(ProfID, Room, Day, TimeSlot, CourseID),
            course(CourseID, CourseName, _),
            professor(ProfID, ProfName),
            time_slot(Day, TimeSlot, TimeRange)
        ),
        Schedule
    ).



