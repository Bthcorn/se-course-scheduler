# SE Course Scheduler

A comprehensive course scheduling system for Software Engineering programs that uses Prolog for constraint-based scheduling logic and Streamlit for an intuitive web interface.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Install SWI-Prolog](#install-swiprolog)
  - [Install Python Dependencies](#install-python-dependencies)
- [Usage](#usage)
  - [Web Application (Recommended)](#web-application-recommended)
  - [Command Line Interface](#command-line-interface)
- [Web Application Features](#web-application-features)
  - [🏠 Dashboard](#-dashboard)
  - [📊 Schedule View](#-schedule-view)
  - [📈 Statistics](#-statistics)
  - [⚙️ Settings](#-settings)
  - [📤 Export](#-export)
- [Excel Data Format](#excel-data-format)
- [Project Structure](#project-structure)
- [Development](#development)
  - [Testing](#testing)
  - [Code Formatting](#code-formatting)
  - [Type Checking](#type-checking)
  - [Development Setup](#development-setup)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
  - [Getting Help](#getting-help)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Features

- **Constraint-based Scheduling**: Uses Prolog for intelligent course scheduling with conflict resolution
- **Web Interface**: Modern Streamlit-based web application with interactive dashboards
- **Excel Integration**: Import/export course and professor data from Excel files
- **Real-time Statistics**: Visual analytics for room utilization and professor workload
- **Flexible Export**: Export schedules in multiple formats (Excel, CSV, JSON)
- **Interactive Filtering**: Filter schedules by room, day, and time period

## Installation

### Prerequisites

- Python 3.9 or higher
- SWI-Prolog (for the Prolog engine)

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
Download from [SWI-Prolog website](https://www.swi-prolog.org/download/stable)

### Install Python Dependencies

Using uv (recommended):

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Web Application (Recommended)

Launch the Streamlit web application:

```bash
python run_web_app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Command Line Interface

Run the basic scheduler:

```bash
python run_cli.py
```

Or from the src directory:

```bash
cd src && python main.py
```

Run with Excel data (use the web app for Excel functionality):

```bash
cd src && python main.py
```

## Web Application Features

### 🏠 Dashboard

- Overview of scheduled courses and statistics
- Quick actions for scheduling, clearing, and validation
- Real-time metrics and success rates

### 📊 Schedule View

- Interactive schedule display with filtering options
- Filter by room, day, or time period
- View both scheduled courses and reserved slots

### 📈 Statistics

- Professor workload visualization
- Room utilization charts
- Detailed statistics tables

### ⚙️ Settings

- Upload Excel files with course and professor data
- System information and data management
- Clear all data option

### 📤 Export

- Export schedules in multiple formats
- Download Excel, CSV, or JSON files
- Data preview before export

## Excel Data Format

The system expects Excel files with the following sheets:

### Courses Sheet

| Column           | Description                          |
| ---------------- | ------------------------------------ |
| CourseID         | Unique course identifier             |
| CourseName       | Course name                          |
| Year             | Academic year                        |
| RequiredCapacity | Student capacity                     |
| Prerequisites    | Comma-separated prerequisite courses |

### Professors Sheet

| Column        | Description                 |
| ------------- | --------------------------- |
| ProfessorID   | Unique professor identifier |
| ProfessorName | Professor name              |

### CanTeach Sheet

| Column      | Description          |
| ----------- | -------------------- |
| ProfessorID | Professor identifier |
| CourseID    | Course identifier    |

### Preferences Sheet (Optional)

| Column      | Description                           |
| ----------- | ------------------------------------- |
| ProfessorID | Professor identifier                  |
| Day         | Preferred day (monday, tuesday, etc.) |
| Period      | Preferred period (morning, afternoon) |

## Project Structure

```
se-course-scheduler/
├── src/                           # Source code
│   ├── se_course_scheduler/       # Core package
│   │   ├── course_scheduler.py    # Main scheduling logic
│   │   └── excel_handler.py       # Excel file operations
│   └── main.py                    # CLI entry point
├── web/                          # Web application
│   └── streamlit_app.py          # Streamlit web app
├── data/                         # Data files
│   ├── scheduler.pl              # Prolog knowledge base
│   └── generated_schedule.xlsx   # Generated schedules
├── docs/                         # Documentation (empty)
├── .mypy_cache/                  # MyPy cache
├── .venv/                        # Virtual environment
├── __pycache__/                  # Python cache
├── run_web_app.py               # Main web app launcher
├── run_cli.py                   # Main CLI launcher
├── pyproject.toml               # Project configuration
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── .python-version              # Python version specification
├── uv.lock                      # UV lock file
└── README.md                    # This file
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed structure documentation.

## Development

### Testing

Tests are not yet implemented. When available, run:

```bash
python -m pytest tests/
```

### Code Formatting

```bash
black .
isort .
```

### Type Checking

```bash
mypy .
```

### Development Setup

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

## Troubleshooting

### Common Issues

1. **Prolog not found**: Ensure SWI-Prolog is installed and in your PATH
2. **Import errors**: Install all dependencies using `uv sync` or `pip install -r requirements.txt`
3. **Excel file errors**: Ensure Excel files have the correct sheet names and column headers
4. **Scheduling conflicts**: Check the Prolog knowledge base for constraint definitions
5. **Virtual environment issues**: Use `uv sync` to properly set up the development environment
6. **Missing dependencies**: Verify `pyswip` is properly installed (may require SWI-Prolog development headers on some systems)

### Getting Help

- Check the console output for detailed error messages
- Ensure all required dependencies are installed
- Verify Excel file format matches the expected structure

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Uses [PySWIP](https://github.com/yuce/pyswip) for Prolog integration
- Excel handling powered by [pandas](https://pandas.pydata.org/) and [openpyxl](https://openpyxl.readthedocs.io/)
