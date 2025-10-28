#!/usr/bin/env python3
"""
Launcher script for the Streamlit Course Scheduler application
"""

import subprocess
import sys
import os


def main():
    """Launch the Streamlit application"""

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "streamlit_app.py")

    # Add the src directory to Python path
    project_root = os.path.dirname(script_dir)
    src_path = os.path.join(project_root, "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    # Set working directory to project root for data file access
    os.chdir(project_root)

    # Launch streamlit
    print("Starting SE Course Scheduler Web Application...")
    print("The application will open in your default web browser.")
    print("Press Ctrl+C to stop the application.")

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                app_path,
                "--server.port",
                "8501",
                "--server.address",
                "localhost",
            ]
        )
    except KeyboardInterrupt:
        print("\nApplication stopped.")
    except Exception as e:
        print(f"Error launching application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
