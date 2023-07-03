import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tkinter import filedialog, Button, Label, Tk, messagebox


# Class to handle file modification events
class MyEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(extension_to_watch):
            # Execute the SASS command
            execute_sass(event.src_path)


# Function to execute the SASS command
def execute_sass(scss_file):
    css_file = os.path.splitext(scss_file)[0] + '.css'
    command = sass_command.format(scss_file, css_file)
    subprocess.call(command, shell=True)


# Function to choose the directory to watch
def choose_directory():
    global root_directory
    root_directory = filedialog.askdirectory()
    folder_label.config(text="Selected Directory: " + root_directory)


# Function to toggle the surveillance
def toggle_surveillance():
    global observer, toggle_button, root_directory
    if not root_directory:
        messagebox.showwarning("No Directory Selected", "Please select a directory first.")
        return

    if observer:
        observer.stop()
        observer.join()
        observer = None
        toggle_button.config(text="Enable Surveillance")
        messagebox.showinfo("Surveillance Disabled", "Surveillance disabled.")
    else:
        observer = Observer()
        event_handler = MyEventHandler()
        observer.schedule(event_handler, root_directory, recursive=True)
        observer.start()
        toggle_button.config(text="Disable Surveillance")
        messagebox.showinfo("Surveillance Enabled", "Surveillance enabled for the directory: " + root_directory)


# Root directory to watch
root_directory = ''

# SASS command to execute
sass_command = 'sass {} {}'

# Extension of files to watch
extension_to_watch = '.scss'

observer = None

# Create the interface window
window = Tk()
window.title("SASS File Surveillance")
window.geometry("400x200")

# Label to display the selected directory
folder_label = Label(window, text="Selected Directory: " + root_directory)
folder_label.pack(pady=10)

# Button to choose the directory to watch
choose_folder_button = Button(window, text="Choose a Directory", command=choose_directory)
choose_folder_button.pack(pady=10)

# Button to toggle surveillance
toggle_button = Button(window, text="Enable Surveillance", command=toggle_surveillance)
toggle_button.pack(pady=10)

# Main loop of the interface
window.mainloop()

# Stop the observer if the interface is closed
if observer:
    observer.stop()
    observer.join()
