#!/usr/bin/env python3
"""
Launcher script for the CLI Course Scheduler application
"""

import sys
import os


def main():
    """Launch the CLI application"""

    # Add the src directory to Python path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(script_dir, "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    # Import and run the main function
    try:
        from main import main as cli_main

        cli_main()
    except ImportError as e:
        print(f"Error importing CLI application: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error running CLI application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
