import os
import concurrent.futures

# Define the path to the scripts
script_path = "Prev_Matches/toSQL/"

# List of scripts to run
scripts = [
    "Batting_toSQL.py",
    "Bowling_toSQL.py",
    "Match_Data_toSQL.py",
    "MVP_Data_toSQL.py",
    "Overs_toSQL.py",
    "Stats_toSQL.py"
]

# Function to run a script
def run_script(script):
    os.system(f"python {os.path.join(script_path, script)}")

# Function to run the pipeline
def run_pipeline():
    # Use ThreadPoolExecutor to run scripts concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_script, scripts)

if __name__ == "__main__":
    run_pipeline()
