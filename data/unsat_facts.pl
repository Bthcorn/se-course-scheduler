
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

prefers(p001, monday, morning).      % Prefers Monday morning
prefers(p001, wednesday, afternoon). % Prefers Wednesday afternoon
prefers(p002, monday, morning).      % Prefers Monday morning
prefers(p002, thursday, afternoon).  % Prefers Thursday afternoon
prefers(p003, monday, morning).      % Prefers Monday morning
prefers(p003, friday, afternoon).    % Prefers Friday afternoon
prefers(p004, monday, morning).      % Prefers Monday morning
prefers(p004, wednesday, afternoon). % Prefers Wednesday afternoon
prefers(p004, friday, morning).      % Prefers Friday morning
prefers(p005, monday, morning).      % Prefers Monday morning
prefers(p005, friday, morning).      % Prefers Friday morning
prefers(p006, thursday, afternoon).  % Prefers Thursday afternoon
prefers(p007, monday, morning).      % Prefers Monday morning
prefers(p007, wednesday, afternoon). % Prefers Wednesday afternoon
prefers(p008, tuesday, morning).     % Prefers Tuesday morning
prefers(p008, thursday, afternoon).  % Prefers Thursday afternoon
prefers(p008, monday, morning).      % Prefers Monday morning
prefers(p009, friday, morning).      % Prefers Friday morning
prefers(p010, _, afternoon).         % Prefers any afternoon

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
% Note: These reserved slots will force courses to be scheduled in non-preferred times

reserved(ecc802, monday, morning, 'Department Meeting').       % Blocks preferred time
reserved(ecc802, monday, afternoon, 'Faculty Development').
reserved(ecc802, tuesday, afternoon, 'Research Seminar').
reserved(ecc803, monday, morning, 'Student Club Meeting').     % Blocks preferred time
reserved(ecc803, wednesday, afternoon, 'Department Social').   % Blocks preferred time
reserved(ecc804, monday, morning, 'Guest Lecture').            % Blocks preferred time
reserved(ecc804, thursday, afternoon, 'Workshop').             % Blocks preferred time
reserved(ecc805, friday, morning, 'Career Services').          % Blocks preferred time
reserved(ecc806, monday, morning, 'Administrative Meeting').   % Blocks preferred time
reserved(ecc806, wednesday, afternoon, 'Board Meeting').       % Blocks preferred time
reserved(ecc802, monday, morning, 'Special Event').         % Blocks preferred time
reserved(ecc805, monday, morning, 'Special Event').         % Blocks preferred time
reserved(ecc803, monday, morning, 'Special Event').         % Blocks preferred time
reserved(ecc804, monday, morning, 'Special Event').         % Blocks preferred time

% ==================== DYNAMIC FACTS ====================
% These facts will be dynamically asserted/retracted during scheduling
% Format: scheduled(ProfID, Room, Day, TimeSlot, CourseID)

:- dynamic scheduled/5.

% ==================== UNSATISFIED SCHEDULE EXAMPLES ====================
% These are example schedules where professors DON'T get their preferred slots
% Uncomment to test the system's ability to detect preference violations

% Example 1: Dr. Smith (p001) prefers Monday morning, but scheduled on Tuesday evening
% scheduled(p001, ecc802, tuesday, evening, cs302).  % AI - NOT preferred time

% Example 2: Dr. Johnson (p002) prefers Monday morning, but scheduled on Wednesday afternoon
% scheduled(p002, ecc803, wednesday, afternoon, cs201).  % DB - NOT preferred time

% Example 3: Dr. Williams (p003) prefers Monday morning or Friday afternoon, but scheduled on Thursday morning
% scheduled(p003, ecc804, thursday, morning, cs301).  % SE - NOT preferred time

% Example 4: Dr. Brown (p004) prefers Monday morning, Wed afternoon, or Fri morning, but scheduled on Tuesday evening
% scheduled(p004, ecc805, tuesday, evening, cs202).  % Web Dev - NOT preferred time

% Example 5: Dr. Davis (p005) prefers Monday morning or Friday morning, but scheduled on Wednesday afternoon
% scheduled(p005, ecc806, wednesday, afternoon, cs102).  % Data Structures - NOT preferred time

% Example 6: Dr. Wilson (p006) prefers Thursday afternoon, but scheduled on Monday evening
% scheduled(p006, ecc802, monday, evening, cs203).  % Algorithms - NOT preferred time

% Example 7: Dr. Taylor (p007) prefers Monday morning or Wednesday afternoon, but scheduled on Saturday morning
% scheduled(p007, ecc803, saturday, morning, cs101).  % Programming - NOT preferred time

% Example 8: Dr. Anderson (p008) prefers Tuesday/Monday morning or Thursday afternoon, but scheduled on Friday evening
% scheduled(p008, ecc804, friday, evening, cs402).  % Mobile Dev - NOT preferred time

% Example 9: Dr. Martin (p009) prefers Friday morning, but scheduled on Tuesday afternoon
% scheduled(p009, ecc805, tuesday, afternoon, cs401).  % ML - NOT preferred time

% Example 10: Dr. Garcia (p010) prefers any afternoon, but scheduled on Wednesday morning
% scheduled(p010, ecc806, wednesday, morning, cs202).  % Web Dev - NOT preferred time (should be afternoon)

% ==================== NOTES ====================
% This file is designed to create scheduling scenarios where:
% 1. All courses CAN be scheduled (no hard conflicts)
% 2. But many/all professors DON'T get their preferred time slots
% 3. Reserved slots block many preferred times
% 4. Demonstrates the difference between feasible and optimal schedules
% 5. Useful for testing preference violation detection and flagging
