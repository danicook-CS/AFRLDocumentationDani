# SEAVUE_GUI
#     Description: This is the front end design for the users to pick the script they would like to run, 
#     the videos they are running with that script, the csv file they would like their data to be displayed,
#     and the start time for the video cutting process.
#     If user selects combine video that method is within this code.

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import subprocess
import os
from video_processing import combine_video_clips  

# Function to run a script with specified parameters
def run_script(script_name, video_files, video_folder, base_folder_name, csv_results_file, start_time):
    script_path = f"SEAVUE_{script_name}.py" # Name of script that will be running
    command = ['python', script_path] + video_files + [video_folder, base_folder_name, script_name, str(start_time), csv_results_file]
    subprocess.Popen(command)

# Function to prompt user and get selected video files
def get_video_paths():
    video_paths = filedialog.askopenfilenames(filetypes=[("Video Files", "*.MP4;*.mp4")], title="Select all your videos to run...")
    return video_paths if video_paths else []

# Function to prompt user and get start time for video processing
def get_start_time_popup():
    start_time_dialog = simpledialog.askstring("Start Time", "Please enter the start time in MM:SS format (e.g., 05:30):")
    if start_time_dialog:
        try:
            min, sec = map(int, start_time_dialog.split(':'))
            start_time = min * 60 + sec
            return start_time
        except ValueError:
            messagebox.showerror("Error", "Invalid input format. Please use MM:SS.")
            return get_start_time_popup()
    else:
        return None

# Function to prompt user and select CSV results file
def select_csv_file():
    csv_results_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")], title="Select your CSV file...")
    return csv_results_file if csv_results_file else None

# Function to handle running a selected script based on user input
def handle_run():
    selected_script = script_var.get() # Get the selected script from dropdown
    video_paths = get_video_paths()
    print(video_paths)
    if video_paths:
        first_video_path = video_paths[0]
        video_folder = os.path.dirname(first_video_path)
        base_folder_name = os.path.basename(video_folder)
        print(base_folder_name)
        
        # Create the output folder path
        print(video_folder)
        
        # Select CSV results file
        csv_results_file = select_csv_file()
        
        start_time = get_start_time_popup()
        if start_time is not None:
            if csv_results_file:
                # If user wants to just combine the videos
                if selected_script == "combine_only":
                    # Combine the selected videos into a single video
                    video_files = [os.path.basename(path) for path in video_paths]
                    combine_video_clips(video_files, video_folder, os.path.join(video_folder, f"{base_folder_name}_finalvid.mp4"))
                    # Inform user that they were combined correctly
                    messagebox.showinfo("Success", "Videos combined successfully!")
                else:
                    # If user picks any other script it will run that script
                    run_script(selected_script, list(video_paths), video_folder, base_folder_name, csv_results_file, start_time)
            else:
                messagebox.showerror("Error", "No CSV file selected. Please select a CSV file.")

# Create the main Tkinter window
root = tk.Tk()
root.title("SEAVUE Script Selector")

# Dropdown menu to select the script
script_options = ["extraction_only", "combine_only", "full_process"]
script_var = tk.StringVar(root)
script_var.set(script_options[0])

script_dropdown = tk.OptionMenu(root, script_var, *script_options)
script_dropdown.pack(pady=10)

# Button to select videos and run the selected script
select_button = tk.Button(root, text="Select Videos and Run Script", command=handle_run)
select_button.pack(pady=10)

# Start the main event loop
root.mainloop()
