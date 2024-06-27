# Import necessary libraries
import os
import platform
import tkinter as tk

from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

# Define necessary functions
# Function to clear screen
def clear_screen():
    
    # Clear screen
    if platform.system() == 'Windows':
        os.system('cls')

    else:
        os.system('clear')


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
    # selected_folder = select_folder(initial_directory=data_directory)
    selected_folder = '/Users/mahar1s/Documents/github/drawing-white-lines/data/1550'

    # List all files in the selected folder
    files_in_folder = os.listdir(selected_folder)
    
    # Sort the files
    files_in_folder.sort()

    # Select the first image
    image_selected = files_in_folder[0]


if __name__ == '__main__':

    # Clear screen
    clear_screen()
    
    # Call the main function
    main()

