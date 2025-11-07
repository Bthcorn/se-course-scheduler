
room(ecc802, 40).
room(ecc803, 40).
room(ecc804, 30).
room(ecc805, 30).
room(ecc806, 50).


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



reserved(ecc802, monday, morning, 'Department Meeting').       % Blocks preferred time
reserved(ecc802, monday, afternoon, 'Faculty Development').
reserved(ecc802, tuesday, afternoon, 'Research Seminar').
reserved(ecc803, monday, morning, 'Student Club Meeting').     % Blocks 
reserved(ecc803, wednesday, afternoon, 'Department Social').   % Blocks 
reserved(ecc804, monday, morning, 'Guest Lecture').            % Blocks 
reserved(ecc804, thursday, afternoon, 'Workshop').             % Blocks 
reserved(ecc805, friday, morning, 'Career Services').          % Blocks 
reserved(ecc806, monday, morning, 'Administrative Meeting').   % Blocks 
reserved(ecc806, wednesday, afternoon, 'Board Meeting').       % Blocks 
reserved(ecc802, monday, morning, 'Special Event').         % Blocks 
reserved(ecc805, monday, morning, 'Special Event').         % Blocks 
reserved(ecc803, monday, morning, 'Special Event').         % Block 
reserved(ecc804, monday, morning, 'Special Event').         % Blocks 


:- dynamic scheduled/5.


% Test cases
% scheduled(p001, ecc802, tuesday, evening, cs302).  % AI - NOT preferred time
% scheduled(p002, ecc803, wednesday, afternoon, cs201).  % DB - NOT preferred time


