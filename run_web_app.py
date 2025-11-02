#!/usr/bin/env python3
"""
Launcher script for the Streamlit Course Scheduler application
"""

import subprocess
import sys


def main():
    """Launch the Streamlit application"""

    app_path = "web/streamlit_app.py"

    # Launch streamlit
    print("Starting SE Course Scheduler Web Application...")
    print("The application will open in your default web browser.")
    print("Press Ctrl+C to stop the application.")

    try:
        _ = subprocess.run(
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
            ],
            check=False,
        )
    except KeyboardInterrupt:
        print("\nApplication stopped.")
    except (FileNotFoundError, OSError, subprocess.SubprocessError) as e:
        print(f"Error launching application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
