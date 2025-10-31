# Project Structure

This document describes the organized structure of the SE Course Scheduler project.

## Directory Layout

```
se-course-scheduler/
├── src/                           # Source code
│   ├── __init__.py
│   ├── se_course_scheduler/       # Core package
│   │   ├── __init__.py
│   │   ├── course_scheduler.py    # Main scheduling logic
│   │   └── excel_handler.py       # Excel file operations
│   └── main.py                    # CLI entry point
├── web/                          # Web application
│   ├── __init__.py
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
├── README.md                    # Project documentation
└── PROJECT_STRUCTURE.md         # This file
```

## Package Organization

### Core Package (`src/se_course_scheduler/`)

- **`course_scheduler.py`**: Main scheduling logic using Prolog
- **`excel_handler.py`**: Excel file import/export functionality
- **`__init__.py`**: Package initialization and exports

### Web Application (`web/`)

- **`streamlit_app.py`**: Complete Streamlit web interface
### Data Files (`data/`)

- **`scheduler.pl`**: Prolog knowledge base with scheduling rules
- **`generated_schedule.xlsx`**: Example output files

### CLI Applications (`src/`)

- **`main.py`**: Command-line interface for basic scheduling

## Usage

### Web Application

```bash
python run_web_app.py
```

### CLI Application

```bash
python run_cli.py
# or
cd src && python main.py
```

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run specific modules
cd src && python main.py
```

## Import Structure

The package uses relative imports within the `src/se_course_scheduler/` package and absolute imports from the package root:

```python
# From web applications
from se_course_scheduler import CourseScheduler, ExcelHandler

# From CLI applications
from se_course_scheduler import CourseScheduler
```

## Benefits of This Structure

1. **Separation of Concerns**: Web, CLI, and core logic are separated
2. **Scalability**: Easy to add new interfaces or modules
3. **Maintainability**: Clear organization makes code easier to maintain
4. **Documentation**: Centralized docs directory for project documentation
5. **Data Management**: Dedicated data directory for input/output files
6. **Development Environment**: Proper virtual environment and cache management
