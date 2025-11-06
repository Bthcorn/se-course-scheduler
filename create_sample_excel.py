"""
Script to create a sample Excel template for course scheduling data
Run this to generate sample_course_data.xlsx
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
import os

def create_sample_excel():
    """Create a sample Excel file with course scheduling data"""
    
    # Create Excel writer
    output_file = 'data/sample_course_data.xlsx'
    
    # Sample data for Courses
    courses_data = {
        'CourseID': [
            # Year 1 - 6 courses
            'cs101', 'cs102', 'cs103', 'cs104', 'cs105', 'cs106',
            # Year 2 - 6 courses
            'cs201', 'cs202', 'cs203', 'cs204', 'cs205', 'cs206',
            # Year 3 - 6 courses
            'cs301', 'cs302', 'cs303', 'cs304', 'cs305', 'cs306',
            # Year 4 - 6 courses
            'cs401', 'cs402', 'cs403', 'cs404', 'cs405', 'cs406'
        ],
        'CourseName': [
            # Year 1
            'Programming Fundamentals', 'Data Structures', 'Discrete Mathematics',
            'Computer Architecture', 'Digital Logic', 'Calculus I',
            # Year 2
            'Database Systems', 'Web Development', 'Algorithm Design',
            'Operating Systems', 'Computer Networks', 'Statistics',
            # Year 3
            'Software Engineering', 'AI', 'UI/UX Design',
            'Computer Graphics', 'Compiler Design', 'Information Security',
            # Year 4
            'Machine Learning', 'Mobile Development', 'Cloud Computing',
            'Data Mining', 'Blockchain', 'IoT Systems'
        ],
        'Year': [
            1, 1, 1, 1, 1, 1,  # Year 1
            2, 2, 2, 2, 2, 2,  # Year 2
            3, 3, 3, 3, 3, 3,  # Year 3
            4, 4, 4, 4, 4, 4   # Year 4
        ]
    }
    
    # Sample data for Professors
    professors_data = {
        'ProfessorID': ['p001', 'p002', 'p003', 'p004', 'p005', 
                        'p006', 'p007', 'p008', 'p009', 'p010',
                        'p011', 'p012', 'p013', 'p014', 'p015'],
        'ProfessorName': ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams', 'Dr. Brown', 'Dr. Davis',
                          'Dr. Wilson', 'Dr. Taylor', 'Dr. Anderson', 'Dr. Martin', 'Dr. Garcia',
                          'Dr. Lee', 'Dr. Martinez', 'Dr. Rodriguez', 'Dr. White', 'Dr. Harris']
    }
    
    # Sample data for CanTeach (which professor can teach which course)
    # Assign different professors to avoid preference conflicts
    can_teach_data = {
        'ProfessorID': [
            # Year 1 courses - 6 different professors
            'p001', 'p002', 'p003', 'p004', 'p005', 'p006',  # cs101-106
            # Year 2 courses - 6 different professors
            'p007', 'p008', 'p009', 'p010', 'p011', 'p012',  # cs201-206
            # Year 3 courses - 6 different professors (cs305 is p010, not p002)
            'p013', 'p014', 'p015', 'p001', 'p010', 'p003',  # cs301-306
            # Year 4 courses - 6 different professors (cs403 is p002)
            'p004', 'p005', 'p002', 'p007', 'p008', 'p009'   # cs401-406
        ],
        'CourseID': [
            # Year 1
            'cs101', 'cs102', 'cs103', 'cs104', 'cs105', 'cs106',
            # Year 2
            'cs201', 'cs202', 'cs203', 'cs204', 'cs205', 'cs206',
            # Year 3
            'cs301', 'cs302', 'cs303', 'cs304', 'cs305', 'cs306',
            # Year 4
            'cs401', 'cs402', 'cs403', 'cs404', 'cs405', 'cs406'
        ]
    }
    
    # Sample data for Preferences
    # Each professor gets ONE preference for their assigned course
    # Spread across different days/times to maximize satisfaction
    # Note: We have 8 reserved slots, so some preferences may conflict
    preferences_data = {
        'ProfessorID': [
            # Year 1 professors (cs101-cs106: p001-p006)
            'p001', 'p002', 'p003', 'p004', 'p005', 'p006',
            # Year 2 professors (cs201-cs206: p007-p012)
            'p007', 'p008', 'p009', 'p010', 'p011', 'p012',
            # Year 3 professors (cs301-cs306: p013, p014, p015, p001, p010, p003)
            'p013', 'p014', 'p015',
            # Year 4 professors (cs401-cs406: p004, p005, p002, p007, p008, p009)
            # p001, p002, p003, p004, p005 teach 2 courses, so give them 2 preferences each
            'p001', 'p002', 'p003', 'p004', 'p005',
            'p007', 'p008', 'p009', 'p010'
        ],
        'Day': [
            # Year 1 preferences - different days
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'monday',
            # Year 2 preferences - different days
            'tuesday', 'wednesday', 'thursday', 'friday', 'monday', 'wednesday',
            # Year 3 preferences - different days
            'thursday', 'friday', 'tuesday',
            # Additional preferences for professors teaching 2 courses
            'wednesday',  # p001 (2nd preference for cs304)
            'thursday',   # p002 (2nd preference for cs403)
            'thursday',   # p003 (2nd preference for cs306)
            'monday',     # p004 (2nd preference for cs401)
            'tuesday',    # p005 (2nd preference for cs402)
            # Year 4 additional professors
            'wednesday',  # p007 (2nd preference for cs404)
            'friday',     # p008 (2nd preference for cs405)
            'monday',     # p009 (2nd preference for cs406)
            'tuesday'     # p010 (2nd preference for cs305)
        ],
        'TimeSlot': [
            # Year 1 time slots - varied
            'morning', 'morning', 'morning', 'morning', 'morning', 'afternoon',
            # Year 2 time slots - varied
            'morning', 'morning', 'morning', 'afternoon', 'morning', 'afternoon',
            # Year 3 time slots - varied
            'morning', 'morning', 'afternoon',
            # Additional time slots for professors teaching 2 courses
            'afternoon',  # p001 (2nd pref)
            'afternoon',  # p002 (2nd pref)
            'afternoon',  # p003 (2nd pref)
            'afternoon',  # p004 (2nd pref)
            'afternoon',  # p005 (2nd pref)
            # Year 4 additional
            'morning',    # p007 (2nd pref)
            'morning',    # p008 (2nd pref)
            'afternoon',  # p009 (2nd pref)
            'afternoon'   # p010 (2nd pref)
        ]
    }
    
    # Create DataFrames
    df_courses = pd.DataFrame(courses_data)
    df_professors = pd.DataFrame(professors_data)
    df_can_teach = pd.DataFrame(can_teach_data)
    df_preferences = pd.DataFrame(preferences_data)
    
    # Write to Excel with formatting
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_courses.to_excel(writer, sheet_name='Courses', index=False)
        df_professors.to_excel(writer, sheet_name='Professors', index=False)
        df_can_teach.to_excel(writer, sheet_name='CanTeach', index=False)
        df_preferences.to_excel(writer, sheet_name='Preferences', index=False)
        
        # Get the workbook and apply formatting
        workbook = writer.book
        
        # Format each sheet
        for sheet_name in ['Courses', 'Professors', 'CanTeach', 'Preferences']:
            sheet = workbook[sheet_name]
            
            # Format header row
            header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
            header_font = Font(bold=True, color='FFFFFF')
            
            for cell in sheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Auto-adjust column widths
            for column in sheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                sheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"✅ Sample Excel file created successfully: {output_file}")
    print("\nFile contains 4 sheets:")
    print("  1. Courses - Course information (CourseID, CourseName, Year)")
    print("  2. Professors - Professor information (ProfessorID, ProfessorName)")
    print("  3. CanTeach - Teaching capabilities (ProfessorID, CourseID)")
    print("  4. Preferences - Time preferences (ProfessorID, Day, TimeSlot)")
    print("\nYou can use this file as a template for importing course data.")

if __name__ == '__main__':
    create_sample_excel()
