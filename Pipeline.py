import subprocess
import sys

# Define the path to the scripts
script_path = "Prev_Matches/toSQL/"

# List of scripts to run
scripts = ["Batting_toSQL.py", "Bowling_toSQL.py", "Match_Data_toSQL.py"]

# Function to run a script in a new terminal
def run_script_in_terminal(script):
    if sys.platform == 'win32':  # Check if running on Windows
        command = f"start cmd /k python {script_path}{script}"
    else:  # Assume Linux or macOS
        command = f"x-terminal-emulator -e python3 {script_path}{script}"
    subprocess.Popen(command, shell=True)

# Run each script in a separate terminal
for script in scripts:
    run_script_in_terminal(script)
