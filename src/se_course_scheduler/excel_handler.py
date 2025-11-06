
import pandas as pd
from pyswip import Prolog


class ExcelHandler:
    """Handles all Excel file operations for the course scheduling system"""

    prolog: Prolog

    def __init__(self, prolog: Prolog):
        """Initialize with a Prolog instance for data assertion"""
        self.prolog = prolog

    def load_courses_from_excel(self, excel_file: str) -> None:
        """Load courses from Excel file and assert into Prolog"""
        try:
            df = pd.read_excel(excel_file, sheet_name="Courses")
            for _, row in df.iterrows():
                course_id = str(row["CourseID"])
                course_name = str(row["CourseName"])
                year = int(row["Year"])

                course_query = (
                    f"assertz(course({course_id}, '{course_name}', {year}))"
                )

                _ = list(self.prolog.query(course_query))
            print(f"✓ Loaded {len(df)} courses from Excel")

        except (FileNotFoundError, KeyError, ValueError, Exception) as e:
            print(f"✗ Error loading courses from Excel: {e}")
            raise

    def load_professors_from_excel(self, excel_file: str) -> None:
        """Load professors, teaching capabilities, and preferences from Excel"""
        try:
            df_prof = pd.read_excel(excel_file, sheet_name="Professors")
            for _, row in df_prof.iterrows():
                professor_id = str(row["ProfessorID"])
                professor_name = str(row["ProfessorName"])
                professor_query = (
                    f"assertz(professor({professor_id}, '{professor_name}'))"
                )
                _ = list(self.prolog.query(professor_query))
            print(f"✓ Loaded {len(df_prof)} professors from Excel")
            
            df_teach = pd.read_excel(excel_file, sheet_name="CanTeach")
            for _, row in df_teach.iterrows():
                teach_prof_id = str(row["ProfessorID"])
                course_id = str(row["CourseID"])
                teach_query = f"assertz(can_teach({teach_prof_id}, {course_id}))"
                _ = list(self.prolog.query(teach_query))
            print(f"✓ Loaded {len(df_teach)} teaching capabilities from Excel")
            
            try:
                df_pref = pd.read_excel(excel_file, sheet_name="Preferences")
                for _, row in df_pref.iterrows():
                    pref_prof_id = str(row["ProfessorID"])
                    day = str(row["Day"]).lower()
                    time_slot = str(row["TimeSlot"]).lower()
                    
                    if day == "_":
                        pref_query = f"assertz(prefers({pref_prof_id}, _, {time_slot}))"
                    else:
                        pref_query = f"assertz(prefers({pref_prof_id}, {day}, {time_slot}))"
                    _ = list(self.prolog.query(pref_query))
                print(f"✓ Loaded {len(df_pref)} professor preferences from Excel")
            except ValueError:
                print("ℹ No preferences sheet found in Excel file (optional)")

        except (FileNotFoundError, KeyError, ValueError, Exception) as e:
            print(f"✗ Error loading professors from Excel: {e}")
            raise

    def load_all_data_from_excel(self, excel_file: str) -> None:
        """Load all data (courses and professors) from Excel file"""
        self.prolog.retractall("course(_, _, _)")
        self.prolog.retractall("professor(_, _)")
        self.prolog.retractall("can_teach(_, _)")
        self.prolog.retractall("prefers(_, _, _)")
        
        self.load_courses_from_excel(excel_file)
        self.load_professors_from_excel(excel_file)
