#!/usr/bin/env python3
"""
Script to make the Python scripts executable.
"""

import os
import stat
from pathlib import Path

def main():
    """Make the Python scripts executable."""
    # Make sure we're in the correct directory
    os.chdir(Path(__file__).resolve().parent)
    
    # Get all Python scripts
    scripts = [
        "app.py",
        "run.py",
        "init_db.py",
        "test_ai.py",
        "create_env.py",
        "make_executable.py"
    ]
    
    # Make each script executable
    for script in scripts:
        script_path = Path(script)
        if script_path.exists():
            # Add execute permission
            current_mode = script_path.stat().st_mode
            script_path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            print(f"Made {script} executable")
        else:
            print(f"Warning: {script} not found")
    
    print("\nAll scripts are now executable.")
    print("You can now run the application with: ./run.py")

if __name__ == "__main__":
    main() 