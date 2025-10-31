#!/usr/bin/env python3
"""
Launcher script for the CLI Course Scheduler application
"""

import sys


def main():
    """Launch the CLI application"""

    # Import and run the main function
    try:
        from src.main import main as cli_main

        cli_main()
    except ImportError as e:
        print(f"Error importing CLI application: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error running CLI application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
