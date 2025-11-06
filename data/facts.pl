
% ==================== DYNAMIC DECLARATIONS ====================
% Allow runtime modification of these predicates for Excel import
:- dynamic course/3.
:- dynamic professor/2.
:- dynamic can_teach/2.
:- dynamic prefers/3.
:- dynamic scheduled/5.

% ==================== ROOM FACTS ====================
% Define available rooms with capacity
% Format: room(RoomID, Capacity)

room(ecc802, 40).
room(ecc803, 40).
room(ecc804, 30).
room(ecc805, 30).
room(ecc806, 50).

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
% Note: Use '_' for Day to indicate any day (e.g., p010 prefers any afternoon)

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

reserved(ecc802, monday, afternoon, 'Department Meeting').
reserved(ecc802, tuesday, afternoon, 'Faculty Development').
reserved(ecc802, wednesday, afternoon, 'Research Seminar').
reserved(ecc803, wednesday, morning, 'Student Club Meeting').
reserved(ecc803, friday, afternoon, 'Department Social Event').
reserved(ecc804, thursday, afternoon, 'Guest Lecture Series').
reserved(ecc805, friday, morning, 'Career Services Workshop').
reserved(ecc806, monday, morning, 'Administrative Meeting').

% ==================== DYNAMIC FACTS ====================
% These facts will be dynamically asserted/retracted during scheduling
% Format: scheduled(ProfID, Room, Day, TimeSlot, CourseID)
% Note: Dynamic declaration moved to top of file

% ==================== TEST DATA (COMMENTED OUT) ====================
% Uncomment these to test conflict detection
% These predicates will cause validate_schedule to fail

% Conflict 1: Professor teaching two courses at the same time
% scheduled(p001, ecc802, monday, morning, cs302).   % Dr. Smith - AI
% scheduled(p001, ecc803, monday, morning, cs401).   % Dr. Smith - ML (conflict: same professor, same time)

% Conflict 2: Two courses in the same room at the same time
% scheduled(p002, ecc804, tuesday, afternoon, cs201).  % Dr. Johnson - DB
% scheduled(p003, ecc804, tuesday, afternoon, cs301). % Dr. Williams - SE (conflict: same room, same time)
