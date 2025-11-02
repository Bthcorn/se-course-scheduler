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

- **Constraint-based Scheduling**: Uses Prolog for intelligent course scheduling with conflict resolution and validation
- **Modern Web Interface**: Streamlit-based web application with interactive dashboards and beautiful UI components
- **Excel Integration**: Import/export course and professor data from Excel files with structured sheet support
- **Real-time Statistics**: Visual analytics for room utilization and professor workload tracking
- **Flexible Export**: Export schedules in multiple formats (Excel, CSV, JSON) with preview
- **Interactive Filtering**: Filter schedules by room, day, and time period in the timetable view
- **Schedule Validation**: Built-in conflict detection and validation system
- **Multi-page Navigation**: Organized interface with dedicated pages for dashboard, timetable, statistics, settings, and export

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
- Real-time metrics including success rates
- Schedule preview with top 10 scheduled courses
- Visual action cards with gradient styling

### 📊 Timetable View

- Interactive schedule display with filtering options
- Filter by room, day, or time period
- View both scheduled courses and reserved slots
- Color-coded schedule visualization
- Detailed course and professor information

### 📈 Statistics

- Professor workload visualization
- Room utilization charts and percentages
- Detailed statistics tables
- Real-time analytics and metrics

### ⚙️ Settings

- Upload Excel files with course and professor data
- System information and data management
- Clear all data option
- Configuration management

### 📤 Export

- Export schedules in multiple formats (Excel, CSV, JSON)
- Download generated schedule files
- Data preview before export
- Flexible export options

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
├── web/                           # Web application
│   ├── app.py                     # Main Streamlit app router
│   ├── streamlit_app.py           # Streamlit entry point
│   ├── config.py                  # Configuration settings
│   ├── components.py              # Reusable UI components
│   ├── utils.py                   # Utility functions
│   └── pages/                     # Page components
│       ├── base_page.py           # Base page class
│       ├── dashboard.py           # Dashboard page
│       ├── timetable_view.py      # Timetable visualization
│       ├── statistics.py          # Statistics page
│       ├── settings.py            # Settings page
│       └── export.py              # Export page
├── data/                          # Data files
│   └── scheduler.pl               # Prolog knowledge base
├── run_web_app.py                 # Web app launcher script
├── run_cli.py                     # CLI launcher script
├── pyproject.toml                 # Project configuration
├── requirements.txt               # Python dependencies
├── uv.lock                        # UV lock file
├── PROJECT_STRUCTURE.md           # Detailed structure docs
└── README.md                      # This file
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
3. **Excel file errors**: Ensure Excel files have the correct sheet names and column headers (see Excel Data Format section)
4. **Scheduling conflicts**: Use the "Validate Schedule" button on the Dashboard to check for conflicts
5. **Virtual environment issues**: Use `uv sync` to properly set up the development environment
6. **Missing dependencies**: Verify `pyswip` is properly installed (may require SWI-Prolog development headers on some systems)
7. **Session state errors**: If you encounter session state issues, refresh the web application page
8. **Attribute errors**: Ensure all required session state variables are initialized by navigating through the app pages

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
- Uses [streamlit-shadcn-ui](https://github.com/sneddy/shadcn-ui-streamlit) for modern UI components
- Uses [PySWIP](https://github.com/yuce/pyswip) for Prolog integration
- Excel handling powered by [pandas](https://pandas.pydata.org/) and [openpyxl](https://openpyxl.readthedocs.io/)
- Powered by [SWI-Prolog](https://www.swi-prolog.org/) for constraint-based scheduling logic
