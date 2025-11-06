# SE Course Scheduler

A comprehensive course scheduling system for Software Engineering programs that uses Prolog for constraint-based scheduling logic and Streamlit for an intuitive web interface.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Install SWI-Prolog](#install-swiprolog)
  - [Install Python Dependencies](#install-python-dependencies)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Web Application (Recommended)](#web-application-recommended)
  - [Creating Sample Excel Data](#creating-sample-excel-data)
- [Web Application Features](#web-application-features)
  - [🏠 Dashboard](#-dashboard)
  - [📅 Timetable View](#-timetable-view)
- [Excel Data Format](#excel-data-format)
- [Project Structure](#project-structure)
- [Algorithm Details](#algorithm-details)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- **Constraint-based Scheduling**: Uses Prolog with CSP (Constraint Satisfaction Problem) algorithms
- **MCV + Forward Checking**: Most Constrained Variable heuristic with forward checking for efficient scheduling
- **Modern Web Interface**: Streamlit-based web application with interactive dashboards
- **Excel Integration**: Import/export course and professor data from Excel files
- **Preference Support**: Handles professor time preferences with fallback options
- **Real-time Visualization**: View schedules organized by year and by room
- **Conflict Detection**: Built-in validation to prevent scheduling conflicts

## Installation

### Prerequisites

- **Python 3.9 or higher**
- **SWI-Prolog** (required for the Prolog engine)

### Install SWI-Prolog

**macOS (using Homebrew):**
```bash
brew install swi-prolog
```

**Ubuntu/Debian:**
```bash
sudo apt-get install swi-prolog
```

**Windows:**
Download and install from [SWI-Prolog website](https://www.swi-prolog.org/download/stable)

**Verify Installation:**
```bash
swipl --version
```

### Install Python Dependencies

1. **Create a virtual environment** (recommended):
```bash
python3 -m venv myenv
source myenv/bin/activate  # On macOS/Linux
# OR on Windows:
# myenv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

**Alternative using uv** (if you have uv installed):
```bash
uv sync
```

## Quick Start

1. **Install SWI-Prolog** (see above)

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the web application**:
```bash
python run_web_app.py
```

4. **Open your browser** to `http://localhost:8501`

5. **Upload Excel data** or use the sample data already in `data/sample_course_data.xlsx`

6. **Generate schedules** by clicking "Generate Schedules" on the Dashboard

## Usage

### Web Application (Recommended)

Launch the Streamlit web application:

```bash
python run_web_app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

**Navigation:**
- **Dashboard**: Upload Excel files, view course overview, and generate schedules
- **Schedules**: View generated schedules organized by year and by room

### Creating Sample Excel Data

To create a sample Excel template file:

```bash
python create_sample_excel.py
```

This will generate `data/sample_course_data.xlsx` with sample courses, professors, teaching capabilities, and preferences. You can use this as a template for your own data.

## Web Application Features

### 🏠 Dashboard

- **Available Rooms**: View all available rooms and their capacities
- **Course Data Overview**: See courses organized by academic year (1-4)
- **Import Course Data**: Upload Excel files (.xlsx, .xls) with course and professor information
- **Generate Schedules**: Create optimal schedules using CSP with MCV + Forward Checking algorithm
- **Status Messages**: Get feedback on scheduling success, partial failures, and preference satisfaction

### 📅 Timetable View

- **Year-wise Schedules**: View weekly schedules organized by academic year
- **Room-wise Schedules**: See schedules organized by room with availability visualization
- **Color-coded Display**:
  - 🟢 Green: Courses scheduled with preferences met
  - 🔴 Red: Courses scheduled but preferences not met
  - 🟠 Orange: Reserved time slots
  - ⬜ White: Available slots
- **Interactive Tables**: HTML tables showing complete schedule information

## Excel Data Format

The system expects Excel files (`.xlsx` or `.xls`) with the following sheets:

### Courses Sheet

| Column     | Description              | Example           |
| ---------- | ------------------------ | ----------------- |
| CourseID   | Unique course identifier | cs101             |
| CourseName | Course name              | Programming Fundamentals |
| Year       | Academic year (1-4)      | 1                 |

### Professors Sheet

| Column        | Description                 | Example    |
| ------------- | --------------------------- | ---------- |
| ProfessorID   | Unique professor identifier | p001       |
| ProfessorName | Professor name              | Dr. Smith  |

### CanTeach Sheet

| Column      | Description          | Example |
| ----------- | -------------------- | ------- |
| ProfessorID | Professor identifier | p001    |
| CourseID    | Course identifier    | cs101   |

### Preferences Sheet (Optional)

| Column      | Description                           | Example    |
| ----------- | ------------------------------------- | ---------- |
| ProfessorID | Professor identifier                  | p001       |
| Day         | Preferred day (lowercase)             | monday     |
| TimeSlot    | Preferred time slot (lowercase)       | morning    |

**Note:**
- Day values: `monday`, `tuesday`, `wednesday`, `thursday`, `friday`
- TimeSlot values: `morning`, `afternoon`, `evening`
- Use `_` (underscore) in Day column for "any day" preference
- If Preferences sheet is missing, all professors are considered flexible

## Project Structure

```
se-course-scheduler/
├── src/                           # Source code
│   ├── se_course_scheduler/       # Core package
│   │   ├── course_scheduler.py    # Main scheduling logic (CSP implementation)
│   │   └── excel_handler.py       # Excel file operations
│   └── main.py                    # CLI entry point (optional)
├── web/                           # Web application
│   ├── app.py                     # Main Streamlit app router
│   ├── streamlit_app.py          # Streamlit entry point
│   ├── config.py                  # Configuration settings
│   ├── components.py              # Reusable UI components
│   ├── utils.py                   # Utility functions
│   └── views/                     # Page components
│       ├── base_page.py           # Base page class
│       ├── dashboard.py           # Dashboard page
│       └── timetable_view.py      # Timetable visualization
├── data/                          # Data files
│   ├── scheduler.pl               # Prolog knowledge base (CSP algorithm)
│   ├── facts.pl                   # Base facts (rooms, time slots)
│   ├── sample_course_data.xlsx    # Sample Excel template
│   └── error_facts.pl             # Error test cases
├── create_sample_excel.py         # Script to generate sample Excel
├── run_web_app.py                 # Web app launcher script
├── pyproject.toml                  # Project configuration
├── requirements.txt               # Python dependencies
└── README.md                       # This file
```

## Algorithm Details

The scheduler uses a **Constraint Satisfaction Problem (CSP)** approach with:

### MCV (Most Constrained Variable) Heuristic
- Courses are sorted by the number of available scheduling slots
- Courses with fewer options are scheduled first
- Reduces search space and improves efficiency

### Forward Checking
- After each course assignment, checks if remaining courses still have valid options
- Prunes impossible branches early
- Prevents deep backtracking

### Preference Handling
- Tries preferred time slots first for each professor
- Falls back to any valid slot if preferences can't be met
- Marks courses that didn't get preferred slots for visibility

### Backtracking
- When a child node fails (no valid assignment found):
  1. Prolog automatically backtracks to the previous choice point
  2. Tries the next available assignment for the current course
  3. If all options exhausted, backtracks further up the tree
  4. Continues until a solution is found or all possibilities exhausted

## Troubleshooting

### Common Issues

1. **"Prolog not found" or "pyswip import error"**
   - Ensure SWI-Prolog is installed: `swipl --version`
   - On Linux, you may need: `sudo apt-get install swi-prolog-dev`
   - Reinstall pyswip: `pip install --force-reinstall pyswip`

2. **"Module not found" errors**
   - Ensure you're in the project root directory
   - Activate your virtual environment: `source myenv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

3. **NumPy installation errors (Python 3.13)**
   - If you encounter build errors with numpy 2.0.2 on Python 3.13, the requirements.txt has been updated to use `numpy>=2.1.0`
   - NumPy 2.0.2 doesn't build on Python 3.13, but 2.1.0+ works correctly
   - If issues persist, manually install: `pip install "numpy>=2.1.0"`

4. **Excel file errors**
   - Ensure Excel file has correct sheet names: `Courses`, `Professors`, `CanTeach`, `Preferences`
   - Check column headers match exactly (case-sensitive)
   - Verify file is `.xlsx` or `.xls` format

5. **"Unable to arrange all courses" error**
   - Too many constraints (reserved slots, limited rooms/time slots)
   - Try reducing reserved time slots
   - Add more rooms or time slots in `data/facts.pl`
   - Check that professors can teach the courses (CanTeach sheet)

6. **Port 8501 already in use**
   - Stop other Streamlit applications
   - Or change port in `run_web_app.py`: `--server.port 8502`

7. **Session state errors in web app**
   - Refresh the browser page
   - Clear browser cache if issues persist

### Getting Help

- Check console output for detailed error messages
- Verify all dependencies are installed: `pip list`
- Ensure SWI-Prolog is accessible: `which swipl` (macOS/Linux) or `where swipl` (Windows)
- Review Excel file format matches the expected structure

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Uses [PySWIP](https://github.com/yuce/pyswip) for Prolog integration
- Excel handling powered by [pandas](https://pandas.pydata.org/) and [openpyxl](https://openpyxl.readthedocs.io/)
- Powered by [SWI-Prolog](https://www.swi-prolog.org/) for constraint-based scheduling logic
