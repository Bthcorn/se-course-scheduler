
% ==================== ROOM FACTS ====================
% Define available rooms with capacity
% Format: room(RoomID, Capacity)
% NOTE: Only 2 rooms available - will make scheduling impossible

room(ecc802, 40).
room(ecc803, 40).

% ==================== TIME SLOT FACTS ====================
% Define time slots
% Format: time_slot(Day, TimeSlot, TimeRange)

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

% ==================== COURSE FACTS ====================
% Define courses
% Format: course(CourseID, CourseName, Year)

course(cs101, 'Programming Fundamentals', 1).
course(cs102, 'Data Structures', 1).
course(cs103, 'Discrete Mathematics', 2).
course(cs201, 'Database Systems', 2).
course(cs202, 'Web Development', 2).
course(cs203, 'Algorithm Design', 2).
course(cs301, 'Software Engineering', 3).
course(cs302, 'AI', 3).
course(cs303, 'UI/UX Design', 3).
course(cs401, 'Machine Learning', 4).
course(cs402, 'Mobile Development', 4).
course(cs403, 'Cloud Computing', 4).

% ==================== PROFESSOR FACTS ====================
% Define professors
% Format: professor(ProfID, ProfName)

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

% ==================== PROFESSOR PREFERENCE FACTS ====================
% Define professor preferences for specific days and time slots
% Format: prefers(ProfID, Day, TimeSlot)

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

% ==================== TEACHING CAPABILITY FACTS ====================
% Define which professors can teach which courses
% Format: can_teach(ProfID, CourseID)

can_teach(p001, cs302).  % Dr. Smith - AI
can_teach(p001, cs401).  % Dr. Smith - ML
can_teach(p001, cs103).  % Dr. Smith - Discrete Mathematics
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

% ==================== RESERVED TIME SLOT FACTS ====================
% Define reserved time slots for special events
% Format: reserved(Room, Day, TimeSlot, Reason)
% NOTE: Massive reservations to block almost all available slots
% With only 2 rooms and most slots reserved, scheduling 12 courses becomes impossible

% Room ecc802 - Almost completely blocked
reserved(ecc802, monday, morning, 'Department Meeting').
reserved(ecc802, monday, afternoon, 'Faculty Development').
reserved(ecc802, monday, evening, 'Evening Seminar').
reserved(ecc802, tuesday, morning, 'Research Seminar').
reserved(ecc802, tuesday, afternoon, 'Committee Meeting').
reserved(ecc802, tuesday, evening, 'Guest Lecture').
reserved(ecc802, wednesday, morning, 'Workshop').
reserved(ecc802, wednesday, afternoon, 'Staff Meeting').
reserved(ecc802, wednesday, evening, 'Training Session').
reserved(ecc802, thursday, morning, 'Department Review').
reserved(ecc802, thursday, afternoon, 'Curriculum Meeting').
reserved(ecc802, thursday, evening, 'Faculty Dinner').
reserved(ecc802, friday, morning, 'Planning Session').
reserved(ecc802, friday, afternoon, 'Social Event').
reserved(ecc802, friday, evening, 'Cleanup').
reserved(ecc802, saturday, morning, 'Maintenance').
reserved(ecc802, saturday, afternoon, 'Special Event').
reserved(ecc802, saturday, evening, 'Cleanup').
reserved(ecc802, sunday, morning, 'Closed').
reserved(ecc802, sunday, afternoon, 'Closed').
reserved(ecc802, sunday, evening, 'Closed').

% Room ecc803 - Almost completely blocked
reserved(ecc803, monday, morning, 'Student Club Meeting').
reserved(ecc803, monday, afternoon, 'Career Fair Setup').
reserved(ecc803, monday, evening, 'Student Event').
reserved(ecc803, tuesday, morning, 'Orientation').
reserved(ecc803, tuesday, afternoon, 'Advising Sessions').
reserved(ecc803, tuesday, evening, 'Club Activities').
reserved(ecc803, wednesday, morning, 'Lab Setup').
reserved(ecc803, wednesday, afternoon, 'Department Social').
reserved(ecc803, wednesday, evening, 'Movie Night').
reserved(ecc803, thursday, morning, 'Guest Speaker').
reserved(ecc803, thursday, afternoon, 'Workshop').
reserved(ecc803, thursday, evening, 'Networking Event').
reserved(ecc803, friday, morning, 'Career Services').
reserved(ecc803, friday, afternoon, 'Alumni Event').
reserved(ecc803, friday, evening, 'Weekend Setup').
reserved(ecc803, saturday, morning, 'Tournament').
reserved(ecc803, saturday, afternoon, 'Community Event').
reserved(ecc803, saturday, evening, 'Cleanup').
reserved(ecc803, sunday, morning, 'Closed').
reserved(ecc803, sunday, afternoon, 'Closed').
reserved(ecc803, sunday, evening, 'Closed').

% ==================== DYNAMIC FACTS ====================
% These facts will be dynamically asserted/retracted during scheduling
% Format: scheduled(ProfID, Room, Day, TimeSlot, CourseID)

:- dynamic scheduled/5.

% ==================== NOTES ====================
% This file is designed to make scheduling IMPOSSIBLE:
% 
% 1. Only 2 rooms available (ecc802, ecc803)
% 2. Both rooms have ALL time slots reserved (21 slots each = 42 total reservations)
% 3. 12 courses need to be scheduled
% 4. With 0 available slots across both rooms, scheduling is impossible
% 
% Expected Result:
% - The scheduler will fail to find a valid schedule
% - Should trigger error alert: "Unable to arrange all courses!"
% - This tests the error handling in the system
