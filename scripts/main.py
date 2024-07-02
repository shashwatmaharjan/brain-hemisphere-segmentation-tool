# Import necessary libraries
import os
import platform
import tkinter as tk
import io

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


# Function to check if a file is an image
def is_image(file_path):

    try:

        # Verify that it is, in fact, an image
        img = Image.open(file_path)
        img.verify()  # Verify that it is, in fact, an image
        return True
    
    except (IOError, SyntaxError):

        return False
    

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
    
    # Return the actual image object for further processing
    return image


# Function to define when a button is pressed
def on_button_press(event):

    global start_x, start_y

    start_x = event.x
    start_y = event.y


# Function to define when a button is released
def on_button_release(event, canvas):
    
    global start_x, start_y

    end_x = event.x
    end_y = event.y

    if drawing_mode == 'straight':
    
        draw_straight_line(end_x, end_y, canvas)
    
    # Update the start position
    start_x = None
    start_y = None


# Function to draw a straight line
def draw_straight_line(end_x, end_y, canvas):

    global start_x, start_y

    if start_x is not None and start_y is not None:

        line_id = canvas.create_line(start_x, start_y, end_x, end_y, fill='white', 
                                     width=straight_line_marker_width)
        lines.append(line_id)
        
        # Append the drawing action to the list
        drawing_actions.append(('line', (start_x, start_y, end_x, end_y)))

        # Update the start position
        start_x = None
        start_y = None


# Function to draw a freehand line
def draw_freehand_line(event, canvas):

    global start_x, start_y

    if start_x is not None and start_y is not None:

        end_x, end_y = event.x, event.y
        
        # Smooth the line by capturing intermediate points
        line_id = canvas.create_line(start_x, start_y, end_x, end_y, fill='white',
                                     width=freehand_line_marker_width, smooth=tk.TRUE, splinesteps=36)
        lines.append(line_id)
        
        # Update the start position
        start_x = end_x
        start_y = end_y


# Function to switch between straight and freehand drawing modes
def toggle_drawing_mode(canvas):

    global drawing_mode
    
    # The logic is confusing because we want to switch between the two modes
    # Trust me it works
    if drawing_mode == 'straight':

        canvas.bind('<B1-Motion>', lambda event: draw_freehand_line(event, canvas))
        drawing_mode = 'freehand'
        draw_mode_button.config(text='Mode: Freehand')
    
    else:

        # Unbind any existing motion binding before binding a new one
        canvas.bind('<B1-Motion>', lambda event: None)
        canvas.bind('<ButtonPress-1>', lambda event: on_button_press(event))
        canvas.bind('<ButtonRelease-1>', lambda event: on_button_release(event, canvas))
        drawing_mode = 'straight'
        draw_mode_button.config(text='Mode: Straight Line')


# Function to undo the last annotation
def undo_last_annotation(canvas):
    
    # If lines is not empty, pop the last line and delete it from the canvas
    if lines:
        
        # Delete the last line
        line_id = lines.pop()

        # Delete the line from the canvas
        canvas.delete(line_id)


# Function to clear all annotations
def clear_all_annotations(canvas):
    
    # Delete all lines from the canvas
    for line_id in lines:

        canvas.delete(line_id)
    
    # Clear the lines list
    lines.clear()


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


# Function to redraw drawings on image
def redraw_drawing_on_image(path_to_image, canvas):

    # Load the base image
    base_image = load_image(canvas, path_to_image)

    # Draw the lines on the image
    draw = ImageDraw.Draw(base_image)

    # Redraw all actions
    for action in drawing_actions:

        if action[0] == 'line':

            # Correctly access the tuple for drawing a line
            start_x, start_y, end_x, end_y = action[1]
            draw.line((start_x, start_y, end_x, end_y), fill='white', width=straight_line_marker_width)
    
    return base_image


# Function to save the current annotated image
def save_annotated_image(canvas, image_path, output_path):

    # Redraw all drawings on the image
    annotated_image = redraw_drawing_on_image(image_path, canvas)

    # Check if output path has an extension, if not, add a default
    if not output_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):

        # Default to tiff if no extension provided
        output_path = output_path + '.tiff'

    # Save the annotated image
    annotated_image.save(output_path)


# Main function
def main():

    global start_x, start_y
    global lines
    global straight_line_marker_width, freehand_line_marker_width
    global drawing_mode
    global current_image_index
    global draw_mode_button
    global root
    global drawing_actions

    # Initialize a default drawing mode
    drawing_mode = 'straight'

    # Initialize a list to keep track of all drawing actions
    drawing_actions = []

    # Define the marker width
    straight_line_marker_width = 4
    freehand_line_marker_width = 6

    # Initialize lines as a list to store the lines drawn
    lines = []

    # Define directories
    current_directory = os.getcwd()
    unannotated_data_directory = os.path.join(current_directory, 'data', 'unannotated')
    annotated_data_directory = os.path.join(current_directory, 'data', 'annotated')
    
    # If annotated data directory does not exist, create it
    if not os.path.exists(annotated_data_directory):

        os.makedirs(annotated_data_directory)

    # Start a pop-up window to select a folder
    selected_folder = select_folder(initial_directory=unannotated_data_directory)
    
    # If a folder is not selected, exit the program
    if not selected_folder:

        print('No folder selected. Exiting the program...')

        return

    # List all files in the selected folder and filter out only image files
    files_in_folder = os.listdir(selected_folder)
    files_in_folder.sort()

    # Initialize an empty list to store image files
    image_files_in_folder = []
    
    # Check if the file is an image
    for file in files_in_folder:

        if is_image(os.path.join(selected_folder, file)):
                       
            image_files_in_folder.append(file)
    
    # If there are no image files in the selected folder, exit the program
    if not image_files_in_folder:

        print('No image files in the selected folder. Exiting the program...')
    
        return
    
    # Get the folder name or sample number
    sample_number = os.path.basename(selected_folder)

    # Create a folder in the annotated data directory with the sample number if it does not exist
    if not os.path.exists(os.path.join(annotated_data_directory, sample_number)):

        os.makedirs(os.path.join(annotated_data_directory, sample_number))
    
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

    # Default to straight line drawing
    canvas.bind('<B1-Motion>', lambda event: None)

    # Create a frame to hold the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Create a sub-frame to hold left side buttons
    left_frame = tk.Frame(button_frame)
    left_frame.pack(side=tk.LEFT)

    # Create Previous button
    previous_button = tk.Button(left_frame, text='Previous', command=lambda: previous_image(canvas, image_files_in_folder, selected_folder))
    previous_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Create Save button
    save_button = tk.Button(left_frame, text='Save', command=lambda: save_annotated_image(canvas, 
                                                                                          path_to_image,
                                                                                          os.path.join(annotated_data_directory, sample_number, image_files_in_folder[current_image_index].split('.')[0])))
    save_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Create Next button
    next_button = tk.Button(left_frame, text='Next', command=lambda: next_image(canvas, image_files_in_folder, selected_folder))
    next_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Create a frame to hold the mode button
    center_frame = tk.Frame(button_frame)
    center_frame.pack(side=tk.LEFT, padx=50)

    # Create a button to toggle between drawing modes
    draw_mode_button = tk.Button(center_frame, text='Mode: Straight Line', command=lambda: toggle_drawing_mode(canvas))
    draw_mode_button.pack(padx=5, pady=5)

    # Create a frame to hold right side buttons
    right_frame = tk.Frame(button_frame)
    right_frame.pack(side=tk.RIGHT)

    # Create Undo button
    undo_button = tk.Button(right_frame, text='Undo', command=lambda: undo_last_annotation(canvas))
    undo_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Create Clear All button
    clear_all_button = tk.Button(right_frame, text='Clear All', command=lambda: clear_all_annotations(canvas))
    clear_all_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Run the main loop
    root.mainloop()


if __name__ == '__main__':

    # Clear screen
    clear_screen()
    
    # Call the main function
    main()

