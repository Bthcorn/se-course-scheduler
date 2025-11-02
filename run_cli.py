#!/usr/bin/env python3
"""
Launcher script for the CLI Course Scheduler application
"""

import sys

from src.main import main as cli_main


def main():
    """Launch the CLI application"""

    # Run the main function
    try:
        cli_main()
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error running CLI application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
