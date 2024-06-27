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


# Function to define when a button is pressed
def on_button_press(event):

    global start_x, start_y

    start_x = event.x
    start_y = event.y


# Function to define when a button is released
def on_button_release(event, canvas):
    
    global start_x, start_y, lines

    end_x = event.x
    end_y = event.y

    if start_x is not None and start_y is not None:

        # Draw a line on the canvas
        line_id = canvas.create_line(start_x, start_y, end_x, end_y, fill='white', width=marker_width)
        lines.append(line_id)

        # Update the start position
        start_x = None
        start_y = None


# Function to undo the last annotation
def undo_last_annotation(canvas):

    global lines

    if lines:

        last_line = lines.pop()
        canvas.delete(last_line)


# Main function
def main():

    global start_x, start_y, lines, marker_width

    # Define the marker width
    marker_width = 4

    # Initialize lines as a list to store the lines drawn
    lines = []

    # Define directories
    current_directory = os.getcwd()
    data_directory = os.path.join(current_directory, 'data')

    # Start a pop-up window to select a folder
    selected_folder = select_folder(initial_directory=data_directory)
    
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
    root.title(f'Annotate {image_selected}')

    # Make the window non-resizable
    root.resizable(False, False)

    # Load the image
    image = Image.open(path_to_image)
    image = image.resize((int(image.width/2.5), int(image.height/2.5)))
    photo = ImageTk.PhotoImage(image)

    # Create a canvas to display the image and annotate
    # Make the canvas full-screen
    canvas = tk.Canvas(root, cursor='arrow', width=image.width, height=image.height)
    canvas.pack(fill=tk.BOTH, expand=tk.YES)

    # Display the image on the canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    # Keep a reference to the image
    # This prevents the image from being garbage collected meaning if might not be displayed 
    # and ensures that there is reference to the image as long as the canvas is displayed
    canvas.image = photo
    
    # Bind mouse events to the canvas
    canvas.bind('<ButtonPress-1>', lambda event: on_button_press(event))
    canvas.bind('<ButtonRelease-1>', lambda event: on_button_release(event, canvas))

    # Add an undo button
    undo_button = tk.Button(root, text='Undo', command=lambda: undo_last_annotation(canvas))
    undo_button.pack(side=tk.BOTTOM)

    # Run the main loop
    root.mainloop()


if __name__ == '__main__':

    # Clear screen
    clear_screen()
    
    # Call the main function
    main()

