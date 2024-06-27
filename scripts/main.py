# Import necessary libraries
import os
import platform
import tkinter as tk

from tkinter import filedialog

# Define necessary functions
# Function to select a folder
def select_folder(initial_directory):
    
    # Define a root window
    root = tk.Tk()

    # Hide the root window
    root.withdraw()

    # Select a folder
    folder_selected = filedialog.askdirectory(initialdir=initial_directory, title='Sample You Want to Annotate')

    return folder_selected

# Main function
def main():

    # Define directories
    current_directory = os.getcwd()
    data_directory = os.path.join(current_directory, 'data')

    # Start a pop-up window to select a folder
    selected_folder = select_folder(initial_directory=data_directory)
    
if __name__ == '__main__':

    # Check the platform
    current_platform = platform.system()
    
    # Clear screen
    if current_platform == 'Windows':

        os.system('cls')

    else:

        os.system('clear')

    main()