import subprocess
import sys
import os
from multiprocessing import Process

# Define the path to the latest scripts
latest_script_path = "Latest_Matches/toSQL/"

# List of latest scripts to run
latest_scripts = [
    "Latest_Batting_toSQL.py",
    "Latest_Bowling_toSQL.py",
    "Latest_Match_Data_toSQL.py",
    "Latest_MVP_toSQL.py",
    "Latest_Overs_toSQL.py",
    "Latest_Stats_toSQL.py"
]

# Function to run a latest script in a new terminal window
def run_latest_script_in_terminal(script):
    if sys.platform == 'win32':  # Check if running on Windows
        subprocess.Popen(["start", "cmd", "/k", "python", os.path.join(latest_script_path, script)], shell=True)
    elif sys.platform == 'darwin':  # Check if running on macOS
        subprocess.Popen(["open", "-a", "Terminal", "python", os.path.join(latest_script_path, script)])
    elif sys.platform == 'linux':  # Check if running on Linux
        subprocess.Popen(["x-terminal-emulator", "-e", "python3", os.path.join(latest_script_path, script)])

# Function to run the pipeline for latest scripts
def run_latest_pipeline():
    # Run each latest script in a separate terminal window
    for script in latest_scripts:
        run_latest_script_in_terminal(script)

# Run the pipeline for latest scripts
if __name__ == "__main__":
    run_latest_pipeline()
