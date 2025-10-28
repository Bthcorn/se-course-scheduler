"""
SE Course Scheduler Package

A comprehensive course scheduling system for Software Engineering programs
using Prolog for constraint-based scheduling and Streamlit for web interface.
"""

from .course_scheduler import CourseScheduler
from .excel_handler import ExcelHandler

__version__ = "0.1.0"
__all__ = ["CourseScheduler", "ExcelHandler"]
