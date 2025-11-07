:- consult('facts.pl').

:- dynamic course/3.
:- dynamic professor/2.
:- dynamic can_teach/2.
:- dynamic prefers/3.


% Constraint rules
room_available(Room, Day, TimeSlot) :-
    \+ scheduled(_, Room, Day, TimeSlot, _),
    \+ reserved(Room, Day, TimeSlot, _).

professor_available(ProfID, Day, TimeSlot) :-
    \+ scheduled(ProfID, _, Day, TimeSlot, _).

year_available(CourseID, Day, TimeSlot) :-
    course(CourseID, _, Year),
    \+ (scheduled(_, _, Day, TimeSlot, OtherCourseID),
        course(OtherCourseID, _, Year),
        CourseID \= OtherCourseID).

course_not_scheduled(CourseID) :-
    \+ scheduled(_, _, _, _, CourseID).



find_assignment(CourseID, ProfID, Room, Day, TimeSlot) :-
    course(CourseID, _, _),
    can_teach(ProfID, CourseID),
    time_slot(Day, TimeSlot, _),
    room(Room, _),
    room_available(Room, Day, TimeSlot),
    professor_available(ProfID, Day, TimeSlot),
    year_available(CourseID, Day, TimeSlot),
    course_not_scheduled(CourseID).

find_preferred_assignment(CourseID, ProfID, Room, Day, TimeSlot) :-
    find_assignment(CourseID, ProfID, Room, Day, TimeSlot),
    prefers(ProfID, Day, TimeSlot).

find_fallback_assignment(CourseID, ProfID, Room, Day, TimeSlot) :-
    find_assignment(CourseID, ProfID, Room, Day, TimeSlot),
    \+ prefers(ProfID, Day, TimeSlot).


clear_schedule :-
    retractall(scheduled(_, _, _, _, _)).


schedule_course_csp(CourseID, ProfID, Room, Day, TimeSlot) :-
    find_preferred_assignment(CourseID, ProfID, Room, Day, TimeSlot).


schedule_course_csp(CourseID, ProfID, Room, Day, TimeSlot) :-
    find_fallback_assignment(CourseID, ProfID, Room, Day, TimeSlot),
    \+ would_block_preference(Room, Day, TimeSlot).


schedule_course_csp(CourseID, ProfID, Room, Day, TimeSlot) :-
    find_fallback_assignment(CourseID, ProfID, Room, Day, TimeSlot).

would_block_preference(Room, Day, TimeSlot) :-
    professor(ProfID, _),
    \+ scheduled(ProfID, _, _, _, _),  
    prefers(ProfID, Day, TimeSlot),     
    can_teach(ProfID, CourseID),        
    course_not_scheduled(CourseID),     
    \+ has_other_preference(ProfID, CourseID, Day, TimeSlot).  

% Check if professor has other preferred slots available
has_other_preference(ProfID, CourseID, BlockedDay, BlockedSlot) :-
    prefers(ProfID, Day, TimeSlot),
    (Day \= BlockedDay ; TimeSlot \= BlockedSlot),
    room(R, _),
    room_available(R, Day, TimeSlot),
    professor_available(ProfID, Day, TimeSlot).



% Count available slots (lower = more constrained)
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

% Sort courses by ascending order
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


schedule_all_with_forward_checking :-
    findall(CourseID, course(CourseID, _, _), AllCourses),
    schedule_with_dynamic_mcv(AllCourses).

schedule_with_dynamic_mcv([]).

schedule_with_dynamic_mcv(RemainingCourses) :-

    sort_by_constraints(RemainingCourses, [MostConstrained|OtherCourses]),
    schedule_course_csp(MostConstrained, ProfID, Room, Day, TimeSlot),
    assertz(scheduled(ProfID, Room, Day, TimeSlot, MostConstrained)),
    
    check_remaining_feasible(OtherCourses),
    
    schedule_with_dynamic_mcv(OtherCourses).

check_remaining_feasible([]).
check_remaining_feasible([CourseID|Rest]) :-
    % Must have at least one valid assignment
    (find_preferred_assignment(CourseID, _, _, _, _) ; 
     find_fallback_assignment(CourseID, _, _, _, _)),
    check_remaining_feasible(Rest).



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