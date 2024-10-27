"""
Image Editor - Core Class Module

This module contains the main ImageEditor class which serves as the core of the application.
It integrates all the different components and manages the overall state of the application.

The ImageEditor class is responsible for:
1. Maintaining the application state
2. Coordinating between different tools and features
3. Managing image data and transformations
4. Handling the main GUI layout

Features:
- Image loading and saving
- Multiple editing tools (draw, crop, text, etc.)
- Various image filters and effects
- Image transformations
- State management for undo/redo operations

Dependencies:
- OpenCV (cv2) for image processing
- Tkinter for GUI
- PIL for image handling
- NumPy for numerical operations

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import Tuple, Dict, Optional, Any
import cv2
import numpy as np
from tkinter import ttk, Tk
from PIL import Image, ImageTk
import os
import sys

# Import all tool modules
from gui_setup import GUISetup
from drawing_tools import DrawingTools
from crop_tools import CropTools
from filter_tools import FilterTools
from blur_tools import BlurTools
from adjust_tools import AdjustTools
from transform_tools import TransformTools
from text_tools import TextTools
from file_operations import FileOperations
from image_utils import ImageUtils
from action_handlers import ActionHandlers
from constants import DEFAULT_COLOR, WINDOW_SIZE, MIN_WINDOW_SIZE

class ImageEditor:
    """
    Main class for the Image Editor application.
    
    This class integrates all the different components of the image editor and
    manages the overall state and functionality of the application.
    """
    
    def __init__(self, master: Tk) -> None:
        """
        Initialize the Image Editor application.
        
        Args:
            master (Tk): The root Tkinter window
            
        The initialization process:
        1. Sets up initial state variables
        2. Initializes image buffers
        3. Sets up the GUI
        4. Initializes all tools
        """
        # Main window reference
        self.master: Tk = master
        
        # Image state variables
        self.filtered_image: Optional[np.ndarray] = None
        self.edited_image: Optional[np.ndarray] = None
        self.original_image: Optional[np.ndarray] = None
        
        # Canvas positioning variables
        self.ratio: float = 1.0
        self.x: int = 0
        self.y: int = 0
        self.x_offset: int = 0
        self.y_offset: int = 0
        
        # Tool state variables
        self.draw_ids: list = []
        self.text_extracted: str = "Sample Text"
        self.color_code: Tuple[Tuple[int, int, int], str] = DEFAULT_COLOR
        
        # Crop tool variables
        self.rectangle_id: int = 0
        self.crop_start_x: int = 0
        self.crop_start_y: int = 0
        self.crop_end_x: int = 0
        self.crop_end_y: int = 0
        
        # Filter states
        self.active_filters: Dict[str, bool] = {
            'negative': False,
            'bw': False,
            'stylisation': False,
            'sketch': False,
            'emboss': False,
            'sepia': False,
            'binary': False,
            'erosion': False,
            'dilation': False
        }
        
        # Initialize GUI and tools
        self._init_gui()
        self._init_tools()
        
    def get_logo_path(self) -> str:
        """
        Get the path to the application logo file.
        
        Returns:
            str: Path to the logo file
        """
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(application_path, 'python_logo.gif')
    
    def _init_gui(self) -> None:
        """Initialize the graphical user interface components."""
        GUISetup.setup_styles(self)
        GUISetup.setup_gui(self)
    
    def _init_tools(self) -> None:
        """Initialize all tool modules."""
        # Initialize each tool module with reference to self
        self.drawing_tools = DrawingTools(self)
        self.crop_tools = CropTools(self)
        self.filter_tools = FilterTools(self)
        self.blur_tools = BlurTools(self)
        self.adjust_tools = AdjustTools(self)
        self.transform_tools = TransformTools(self)
        self.text_tools = TextTools(self)
        self.file_ops = FileOperations(self)
        self.image_utils = ImageUtils(self)
        self.action_handlers = ActionHandlers(self)

    # Method delegation to tools
    def upload_action(self) -> None:
        """Delegate to FileOperations."""
        self.file_ops.upload_image()

    def save_action(self) -> None:
        """Delegate to FileOperations."""
        self.file_ops.save_image()

    def draw_action(self) -> None:
        """Delegate to DrawingTools."""
        self.drawing_tools.setup_drawing_tools()

    def crop_action(self) -> None:
        """Delegate to CropTools."""
        self.crop_tools.setup_crop_tools()

    def text_action(self) -> None:
        """Delegate to TextTools."""
        self.text_tools.setup_text_tools()

    def filter_action(self) -> None:
        """Delegate to FilterTools."""
        self.filter_tools.setup_filter_tools()

    def blur_action(self) -> None:
        """Delegate to BlurTools."""
        self.blur_tools.setup_blur_tools()

    def adjust_action(self) -> None:
        """Delegate to AdjustTools."""
        self.adjust_tools.setup_adjust_tools()

    def rotate_action(self) -> None:
        """Delegate to TransformTools."""
        self.transform_tools.setup_rotation_tools()

    def flip_action(self) -> None:
        """Delegate to TransformTools."""
        self.transform_tools.setup_flip_tools()

    def apply_action(self) -> None:
        """Delegate to ActionHandlers."""
        self.action_handlers.apply_changes()

    def cancel_action(self) -> None:
        """Delegate to ActionHandlers."""
        self.action_handlers.cancel_changes()

    def revert_action(self) -> None:
        """Delegate to ActionHandlers."""
        self.action_handlers.revert_all()

    def display_image(self, image: Optional[np.ndarray] = None) -> None:
        """Delegate to ImageUtils."""
        self.image_utils.display_image(image)

    def refresh_side_frame(self) -> None:
        """
        Refresh the side frame of the application.
        
        This method:
        1. Removes the existing side frame if it exists
        2. Unbinds any existing canvas events
        3. Refreshes the image display
        4. Creates a new side frame
        """
        try:
            self.side_frame.grid_forget()
        except AttributeError:
            pass
        
        # Unbind all canvas events
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")
        
        # Refresh image display
        self.image_utils.display_image(self.edited_image)
        
        # Create new side frame
        self.side_frame = ttk.Frame(
            self.content_frame,
            style='Custom.TFrame',
            width=250
        )
        self.side_frame.grid(row=0, column=2, sticky='ns', padx=20)
        self.side_frame.grid_propagate(False)
        self.side_frame.config(relief='groove', padding=(15, 15))