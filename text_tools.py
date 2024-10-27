"""
Text Tools Module for Image Editor Application

This module handles all text-related functionality for the Image Editor application.
It provides tools for adding and manipulating text overlays on images, including:
1. Text input and placement
2. Font selection and sizing
3. Color selection
4. Text positioning
5. Text style management

Key Features:
- Interactive text placement
- Color picker integration
- Font customization
- Real-time preview
- Multiple text overlays
- Undo capability

Dependencies:
- cv2 (OpenCV) for image text rendering
- tkinter for GUI components and color picker
- typing for type hints
- numpy for image manipulation

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import Tuple, Optional, TYPE_CHECKING
from tkinter import ttk, colorchooser
import cv2
import numpy as np

if TYPE_CHECKING:
    from image_editor import ImageEditor
    from tkinter import Event, Entry

class TextTools:
    """
    Class containing all text-related functionality for the Image Editor.
    
    This class manages text overlay operations including text input,
    placement, and styling.
    """
    
    def __init__(self, editor: 'ImageEditor') -> None:
        """
        Initialize the TextTools class.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        Initializes:
            - Reference to main editor
            - Text properties
            - Default values
        """
        self.editor = editor
        self.text_entry: Optional[Entry] = None
        self.default_text: str = "Sample Text"
        self.default_font = cv2.FONT_HERSHEY_SIMPLEX
        self.default_font_scale: float = 2.0
        self.default_thickness: int = 5
        
    def setup_text_tools(self) -> None:
        """
        Set up the text tools interface in the side frame.
        
        Creates:
        1. Text input field
        2. Color picker
        3. Font options (if implemented)
        4. Instructions
        """
        # Initialize text as default
        self.editor.text_extracted = self.default_text
        
        # Refresh the side frame
        self.editor.refresh_side_frame()
        
        # Add title
        ttk.Label(
            self.editor.side_frame,
            text="Add Text",
            font=('Helvetica', 12, 'bold'),
            style='Custom.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Add text input area
        self._setup_text_input()
        
        # Add color picker
        self._setup_color_picker()
        
        # Add instructions
        self._setup_instructions()
        
        # Bind canvas event
        self.editor.canvas.bind("<ButtonPress>", self.start_text_placement)
        
    def _setup_text_input(self) -> None:
        """
        Set up the text input area.
        
        Creates:
        1. Text input label
        2. Text entry field
        3. Sets default text
        """
        ttk.Label(
            self.editor.side_frame,
            text="Enter Text:",
            style='Custom.TLabel'
        ).grid(row=1, column=0, padx=5, pady=5, sticky='sw')
        
        self.text_entry = ttk.Entry(
            self.editor.side_frame,
            width=30
        )
        self.text_entry.grid(row=2, column=0, columnspan=2, padx=5, sticky='ew')
        self.text_entry.insert(0, self.editor.text_extracted)
        
    def _setup_color_picker(self) -> None:
        """
        Set up the color picker button and preview.
        
        Creates:
        1. Color picker button
        2. Color preview
        3. Sets default color
        """
        ttk.Button(
            self.editor.side_frame,
            text="Choose Color",
            command=self.choose_color,
            style='Secondary.TButton'
        ).grid(row=3, column=0, columnspan=2, padx=5, pady=15, sticky='ew')
        
    def _setup_instructions(self) -> None:
        """
        Set up the instruction text for using text tools.
        
        Creates:
        1. Instructions title
        2. Step-by-step instructions
        """
        ttk.Label(
            self.editor.side_frame,
            text="Instructions:",
            font=('Helvetica', 10, 'bold'),
            style='Custom.TLabel'
        ).grid(row=4, column=0, columnspan=2, padx=5, pady=(15,5), sticky='w')
        
        ttk.Label(
            self.editor.side_frame,
            text="1. Enter text above\n2. Choose color (optional)\n3. Click on image to place text",
            style='Custom.TLabel'
        ).grid(row=5, column=0, columnspan=2, padx=5, sticky='w')
        
    def choose_color(self) -> None:
        """
        Open color picker dialog and update the current text color.
        
        Notes:
            - Uses tkinter's colorchooser
            - Updates color code in editor
            - Updates color preview if available
        """
        color = colorchooser.askcolor(
            title="Choose Color",
            initialcolor=self.editor.color_code[1]
        )
        
        if color[0] is not None:
            self.editor.color_code = color
            self._update_color_preview()
            
    def _update_color_preview(self) -> None:
        """
        Update the color preview display if it exists.
        
        Updates the preview canvas with the currently selected color.
        """
        if hasattr(self.editor, 'color_preview'):
            self.editor.color_preview.configure(bg=self.editor.color_code[1])
            
    def start_text_placement(self, event: 'Event') -> None:
        """
        Handle mouse click to place text on the image.
        
        Args:
            event: Tkinter event containing click coordinates
            
        Places text at the clicked location with current settings.
        """
        # Get current text from entry field
        if self.text_entry and self.text_entry.get():
            self.editor.text_extracted = self.text_entry.get()
        
        try:
            # Convert color from RGB to BGR for OpenCV
            r, g, b = tuple(map(int, self.editor.color_code[0]))
        except (TypeError, ValueError):
            # Use default color (blue) if color conversion fails
            r, g, b = 0, 0, 255
        
        # Calculate actual image coordinates
        start_x = int(event.x * self.editor.ratio)
        start_y = int(event.y * self.editor.ratio)
        
        # Create a copy of the image for text placement
        self.editor.filtered_image = self.editor.edited_image.copy()
        
        # Add text to image
        self.editor.filtered_image = cv2.putText(
            self.editor.filtered_image,
            self.editor.text_extracted,
            (start_x, start_y),
            self.default_font,
            self.default_font_scale,
            (b, g, r),
            self.default_thickness
        )
        
        # Update display
        self.editor.display_image(self.editor.filtered_image)
        
    def calculate_text_size(self, text: str) -> Tuple[int, int]:
        """
        Calculate the pixel size of text with current settings.
        
        Args:
            text: The text to measure
            
        Returns:
            Tuple containing width and height of text in pixels
            
        Used for:
        1. Positioning text
        2. Preventing text from going off-image
        3. Spacing multiple text elements
        """
        return cv2.getTextSize(
            text,
            self.default_font,
            self.default_font_scale,
            self.default_thickness
        )[0]
        
    def validate_position(self, x: int, y: int, text_size: Tuple[int, int]) -> Tuple[int, int]:
        """
        Validate and adjust text position to ensure it's within image bounds.
        
        Args:
            x: Desired x coordinate
            y: Desired y coordinate
            text_size: Size of text (width, height)
            
        Returns:
            Tuple of adjusted x, y coordinates
            
        Ensures text remains visible within image boundaries.
        """
        img_height, img_width = self.editor.filtered_image.shape[:2]
        text_width, text_height = text_size
        
        # Adjust x coordinate
        x = max(text_height, min(x, img_width - text_width))
        
        # Adjust y coordinate
        y = max(text_height, min(y, img_height - text_height))
        
        return x, y
