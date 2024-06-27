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

    # Destroy the root window
    root.destroy()

    return folder_selected


# Main function
def main():

    # Define directories
    current_directory = os.getcwd()
    data_directory = os.path.join(current_directory, 'data')

    # Start a pop-up window to select a folder
    selected_folder = select_folder(initial_directory=data_directory)
    # selected_folder = '/Users/mahar1s/Documents/github/drawing-white-lines/data/1550'
    
    # If a folder is not selected, exit the program
    if not selected_folder:

        print('No folder selected. Exiting the program...')

        return

    # List all files in the selected folder
    files_in_folder = os.listdir(selected_folder)
    files_in_folder.sort()

    # Select the first image
    image_selected = files_in_folder[0]
    path_to_image = os.path.join(selected_folder, image_selected)

    # Create a main window
    root = tk.Tk()
    root.title('Annotate the Image')

    # Load the image
    image = Image.open(path_to_image)
    image = image.resize((int(image.width/2.5), int(image.height/2.5)))
    photo = ImageTk.PhotoImage(image)

    # Create a canvas to display the image and annotate
    # Make the canvas full-screen
    canvas = tk.Canvas(root, cursor='pencil', width=image.width, height=image.height)
    canvas.pack(fill=tk.BOTH, expand=tk.YES)

    # Display the image on the canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    # Keep a reference to the image
    # This prevents the image from being garbage collected meaning if might not be displayed 
    # and ensures that there is reference to the image as long as the canvas is displayed
    canvas.image = photo

    # Run the main loop
    root.mainloop()


if __name__ == '__main__':

    # Clear screen
    clear_screen()
    
    # Call the main function
    main()

