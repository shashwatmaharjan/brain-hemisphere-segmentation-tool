# Import necessary libraries
import os
import platform
import tkinter as tk
import imghdr

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


# Function to load an image on the canvas
def load_image(canvas, image_path):

    # Load the image
    image = Image.open(image_path)
    image = image.resize((int(image.width/2.5), int(image.height/2.5)))
    photo = ImageTk.PhotoImage(image)

    # Display the image on the canvas
    canvas.image = photo

    # Keep a reference to the image
    # This prevents the image from being garbage collected meaning if might not be displayed 
    # and ensures that there is reference to the image as long as the canvas is displayed
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                         

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
    
    # If lines is not empty, pop the last line and delete it from the canvas
    if lines:

        line_id = lines.pop()
        canvas.delete(line_id)


# Function to go to previous image
def previous_image(canvas, image_files_in_folder, selected_folder):

    global current_image_index

    if current_image_index > 0:

        current_image_index = current_image_index - 1
    
        # Load the previous image
        path_to_image = os.path.join(selected_folder, image_files_in_folder[current_image_index])

        # Load the new image
        load_image(canvas, path_to_image)

        # Update the title
        root.title(f'Annotate {image_files_in_folder[current_image_index]}')


# Function to go to next image
def next_image(canvas, image_files_in_folder, selected_folder):

    global current_image_index

    if current_image_index < len(image_files_in_folder) - 1:
    
        current_image_index = current_image_index + 1

        # Load the next image
        path_to_image = os.path.join(selected_folder, image_files_in_folder[current_image_index])

        # Load the new image
        load_image(canvas, path_to_image)

        # Update the title
        root.title(f'Annotate {image_files_in_folder[current_image_index]}')


# Main function
def main():

    global start_x, start_y, lines, marker_width, current_image_index, root

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

    # List all files in the selected folder and filter out only image files
    files_in_folder = os.listdir(selected_folder)
    files_in_folder.sort()

    # Initialize an empty list to store image files
    image_files_in_folder = []
    
    for file in files_in_folder:

        if imghdr.what(os.path.join(selected_folder, file)):
                       
            image_files_in_folder.append(file)

    # Initialize current image index
    current_image_index = 0

    # Select the first image
    path_to_image = os.path.join(selected_folder, image_files_in_folder[current_image_index])

    # Create a main window
    root = tk.Tk()
    root.title(f'Annotate {image_files_in_folder[current_image_index]}')

    # Make the window non-resizable
    root.resizable(False, False)

    # Create a canvas to display the image and annotate
    # Make the canvas full-screen
    # 666 and 832 is based on the size of the .tif image
    canvas = tk.Canvas(root, cursor='arrow', width=666, height=832)
    canvas.pack(fill=tk.BOTH, expand=tk.YES)

    # Load the first image
    load_image(canvas, path_to_image)
    
    # Bind mouse events to the canvas
    canvas.bind('<ButtonPress-1>', lambda event: on_button_press(event))
    canvas.bind('<ButtonRelease-1>', lambda event: on_button_release(event, canvas))

    # Create a frame to hold the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Create a sub-frame to center the buttons
    center_frame = tk.Frame(button_frame)
    center_frame.pack(side=tk.BOTTOM)

    # Create Previous button
    previous_button = tk.Button(center_frame, text='Previous', command=lambda: previous_image(canvas, image_files_in_folder, selected_folder))
    previous_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Create Undo button
    undo_button = tk.Button(center_frame, text='Undo', command=lambda: undo_last_annotation(canvas))
    undo_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Create Next button
    next_button = tk.Button(center_frame, text='Next', command=lambda: next_image(canvas, image_files_in_folder, selected_folder))
    next_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Run the main loop
    root.mainloop()


if __name__ == '__main__':

    # Clear screen
    clear_screen()
    
    # Call the main function
    main()

