import subprocess
import os
import webbrowser

# Define a function to run each script
def run_scripts(script):
    print(f"Running {script}...")
    subprocess.run(["python", script])
    print(f"{script} has finished running.")

# Run data cleaning script
run_scripts("data_cleaning_executable.py")

# Run skill extraction script
run_scripts("skill_extraction_executable.py")

# Run database creation script
run_scripts("database_creation_executable.py")

# Run Flask API server in background (non-blocking)
print("Starting Flask API server...")
flask_process = subprocess.Popen(["python", "api_endpoints_executable.py"]) 

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path relative to the script location
html_file_path = os.path.abspath(os.path.join(script_dir, "../frontend/index.html"))

# Check if the file exists before opening
if os.path.exists(html_file_path):
    print(f"Opening {html_file_path}...")
    webbrowser.open(f'file://{html_file_path}')
else:
    print(f"Error: File not found at {html_file_path}")

# Optionally, wait for Flask process to terminate (if needed)
try:
    flask_process.wait()
except KeyboardInterrupt:
    print("Flask server terminated manually.")
finally:
    print("Project execution completed.")