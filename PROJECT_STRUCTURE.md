# Project Structure

This document describes the organized structure of the SE Course Scheduler project.

## Directory Layout

```
se-course-scheduler/
├── src/                           # Source code
│   ├── __init__.py
│   ├── se_course_scheduler/       # Core package
│   │   ├── __init__.py
│   │   ├── course_scheduler.py    # Main scheduling logic with Prolog integration
│   │   └── excel_handler.py       # Excel file import/export operations
│   └── main.py                    # CLI entry point
├── web/                           # Web application
│   ├── __init__.py
│   ├── app.py                     # Main Streamlit app router and navigation
│   ├── streamlit_app.py           # Streamlit entry point
│   ├── config.py                  # Application configuration settings
│   ├── components.py              # Reusable UI components (tables, cards, etc.)
│   ├── utils.py                   # Utility functions (scheduler initialization, messages)
│   └── pages/                     # Page components (modular page structure)
│       ├── __init__.py
│       ├── base_page.py           # Base page class for all pages
│       ├── dashboard.py           # Dashboard page with metrics and quick actions
│       ├── timetable_view.py      # Timetable visualization with filtering
│       ├── statistics.py          # Statistics page with charts and analytics
│       ├── settings.py            # Settings page for data upload and management
│       └── export.py              # Export page for schedule downloads
├── data/                          # Data files
│   └── scheduler.pl               # Prolog knowledge base with scheduling rules
├── run_web_app.py                 # Web app launcher script
├── run_cli.py                     # CLI launcher script
├── pyproject.toml                 # Project configuration and dependencies
├── requirements.txt               # Python dependencies (legacy)
├── uv.lock                        # UV lock file for dependency management
├── README.md                      # Project documentation
└── PROJECT_STRUCTURE.md           # This file
```

## Package Organization

### Core Package (`src/se_course_scheduler/`)

- **`course_scheduler.py`**: Main scheduling logic using Prolog
- **`excel_handler.py`**: Excel file import/export functionality
- **`__init__.py`**: Package initialization and exports

### Web Application (`web/`)

The web application is organized into a modular structure:

#### Core Files
- **`app.py`**: Main application router handling page navigation and routing
- **`streamlit_app.py`**: Entry point that initializes and runs the Streamlit application
- **`config.py`**: Application-wide configuration including page titles and settings
- **`components.py`**: Reusable UI components used across multiple pages
- **`utils.py`**: Shared utility functions for scheduler initialization and message display

#### Pages (`web/pages/`)
- **`base_page.py`**: Abstract base class defining the interface for all pages
- **`dashboard.py`**: Main dashboard with metrics, quick actions, and schedule preview
- **`timetable_view.py`**: Interactive timetable visualization with filtering capabilities
- **`statistics.py`**: Statistics and analytics with charts and detailed metrics
- **`settings.py`**: Settings page for Excel file uploads and data management
- **`export.py`**: Export functionality for downloading schedules in various formats

### Data Files (`data/`)

- **`scheduler.pl`**: Prolog knowledge base containing:
  - Room definitions with capacities
  - Time slot definitions
  - Course definitions with prerequisites
  - Professor information and capabilities
  - Scheduling rules and constraints
  - Validation logic

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

The package uses both absolute and relative imports:

### From Web Applications

```python
# Import core scheduler
from src.se_course_scheduler import CourseScheduler

# Import page components
from web.pages.dashboard import DashboardPage
from web.pages.timetable_view import TimetableViewPage
from web.pages.statistics import StatisticsPage
from web.pages.settings import SettingsPage
from web.pages.export import ExportPage

# Import utilities and components
from web.utils import check_scheduler_initialized, display_messages
from web.components import display_schedule_table
from web.config import PAGE_CONFIG
```

### From CLI Applications

```python
# Import core scheduler
from src.se_course_scheduler import CourseScheduler

# Or from the package directly
from se_course_scheduler import CourseScheduler
```

### Package Exports

The `src/se_course_scheduler/__init__.py` file exports the main classes:

```python
from .course_scheduler import CourseScheduler
from .excel_handler import ExcelHandler

__all__ = ["CourseScheduler", "ExcelHandler"]
```

## Architecture Overview

### Component Interaction

```
┌─────────────────┐
│  Streamlit UI   │
│  (web/app.py)   │
└────────┬────────┘
         │
         ├───► Dashboard Page
         ├───► Timetable View Page
         ├───► Statistics Page
         ├───► Settings Page
         └───► Export Page
              │
              ▼
    ┌─────────────────┐
    │  CourseScheduler │
    │  (Core Logic)    │
    └────────┬────────┘
             │
             ├───► Prolog Engine (scheduler.pl)
             └───► Excel Handler
```

### Data Flow

1. **User Input** → Web Pages → CourseScheduler
2. **CourseScheduler** → Prolog Knowledge Base → Scheduling Logic
3. **Scheduling Results** → Session State → UI Display
4. **Export** → Excel/CSV/JSON → Download

## Benefits of This Structure

1. **Separation of Concerns**: 
   - Web UI, CLI, and core logic are cleanly separated
   - Each page is a self-contained module
   - Core scheduling logic is independent of UI

2. **Modularity**: 
   - Easy to add new pages by extending `BasePage`
   - Reusable components reduce code duplication
   - Configuration centralized in `config.py`

3. **Scalability**: 
   - Simple to add new interfaces (REST API, etc.)
   - Easy to extend with new features
   - Component-based UI architecture

4. **Maintainability**: 
   - Clear organization makes code easier to maintain
   - Type hints and structured code
   - Centralized utility functions

5. **Data Management**: 
   - Dedicated data directory for Prolog knowledge base
   - Session state management for web app
   - Flexible import/export capabilities

6. **Development Environment**: 
   - Proper virtual environment support (uv)
   - Type checking with mypy
   - Code formatting standards
