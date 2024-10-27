"""
Image Editor Application - Main Entry Point

This module serves as the entry point for the Image Editor application. It initializes the main
Tkinter window and creates an instance of the ImageEditor class. The module is responsible for:
1. Setting up the root window
2. Initializing the application
3. Setting up the application icon
4. Starting the main event loop

The application is a feature-rich image editor with capabilities including:
- Basic image operations (crop, rotate, flip)
- Filters and effects
- Drawing tools
- Text overlay
- Image adjustments (brightness, contrast, etc.)

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import NoReturn
from tkinter import Tk, PhotoImage
from image_editor import ImageEditor

def setup_window_icon(root: Tk, app: ImageEditor) -> None:
    """
    Set up the application window icon.
    
    Args:
        root (Tk): The root Tkinter window
        app (ImageEditor): Instance of the ImageEditor class
    
    Note:
        Silently fails if the icon file is not found to prevent application crash
    """
    try:
        logo_path = app.get_logo_path()
        photo = PhotoImage(file=logo_path)
        root.iconphoto(False, photo)
    except Exception as e:
        print(f"Warning: Could not load application icon: {e}")
        pass

def main() -> NoReturn:
    """
    Main entry point of the application.
    
    This function:
    1. Creates the root Tkinter window
    2. Initializes the ImageEditor application
    3. Sets up the window icon
    4. Starts the main event loop
    
    The function doesn't return as it enters the Tkinter main loop.
    """
    # Initialize the root window
    root = Tk()
    
    # Create the main application instance
    app = ImageEditor(root)
    
    # Set up the window icon
    setup_window_icon(root, app)
    
    # Start the main event loop
    # This will block until the window is closed
    root.mainloop()

if __name__ == "__main__":
    main()