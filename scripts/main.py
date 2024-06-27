# Import necessary libraries
import os
import platform

# Main function
def main():

    # Define directories
    current_directory = os.getcwd()
    data_directory = os.path.join(current_directory, 'data')

if __name__ == '__main__':

    # Check the platform
    current_platform = platform.system()
    
    # Clear screen
    if current_platform == 'Windows':

        os.system('cls')

    else:

        os.system('clear')

    main()