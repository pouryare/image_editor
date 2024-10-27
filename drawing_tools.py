"""
Drawing Tools Module for Image Editor Application

This module handles all drawing-related functionality for the Image Editor application.
It provides tools and utilities for freehand drawing on images, including:
1. Drawing tool initialization and setup
2. Color selection functionality
3. Drawing event handling
4. Canvas drawing operations
5. OpenCV image drawing operations

The module integrates both Tkinter canvas drawing for display and OpenCV drawing
for actual image manipulation.

Dependencies:
- tkinter and ttk for GUI components
- cv2 (OpenCV) for image manipulation
- numpy for image array operations
- typing for type hints

Author: [Your Name]
Date: October 2024
Version: 1.0
"""

from typing import Tuple, TYPE_CHECKING
import cv2
from tkinter import ttk, Canvas, ROUND, colorchooser

if TYPE_CHECKING:
    from image_editor import ImageEditor
    from tkinter import Event

class DrawingTools:
    """
    Class containing all drawing-related functionality for the Image Editor.
    
    This class manages the drawing interface and handles drawing operations
    on both the canvas and the actual image.
    """
    
    def __init__(self, editor: 'ImageEditor') -> None:
        """
        Initialize the DrawingTools class.
        
        Args:
            editor: Reference to the main ImageEditor instance
        """
        self.editor = editor
        self.drawing = False
        self.last_x = 0
        self.last_y = 0
    
    def setup_drawing_tools(self) -> None:
        """
        Set up the drawing tools interface in the side frame.
        
        Creates:
        1. Color picker button
        2. Color preview
        3. Drawing options (if any)
        """
        # Refresh the side frame
        self.editor.refresh_side_frame()
        
        # Set up canvas bindings for drawing
        self.editor.canvas.bind("<ButtonPress>", self.start_draw)
        self.editor.canvas.bind("<B1-Motion>", self.draw)
        
        # Create a copy of the edited image for drawing
        self.editor.filtered_image = self.editor.edited_image.copy()
        
        # Add drawing tools title
        ttk.Label(
            self.editor.side_frame,
            text="Drawing Tools",
            font=('Helvetica', 12, 'bold'),
            style='Custom.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Add color picker button
        self.draw_color_button = ttk.Button(
            self.editor.side_frame,
            text="Pick Color",
            command=self.choose_color,
            style='Secondary.TButton'
        )
        self.draw_color_button.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky='ew'
        )
        
        # Create color preview frame
        preview_frame = ttk.Frame(
            self.editor.side_frame,
            style='Custom.TFrame'
        )
        preview_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Add color preview label
        ttk.Label(
            preview_frame,
            text="Current Color:",
            style='Custom.TLabel'
        ).grid(row=0, column=0, padx=(0, 10))
        
        # Add color preview canvas
        self.color_preview = Canvas(
            preview_frame,
            width=30,
            height=30,
            bg=self.editor.color_code[1],
            highlightthickness=1,
            highlightbackground='white'
        )
        self.color_preview.grid(row=0, column=1)
    
    def choose_color(self) -> None:
        """
        Open color picker dialog and update the current drawing color.
        
        Updates:
        1. Color code tuple (RGB, Hex)
        2. Color preview display
        """
        color = colorchooser.askcolor(
            title="Choose Color",
            initialcolor=self.editor.color_code[1]
        )
        
        if color[0] is not None:
            self.editor.color_code = color
            if hasattr(self, 'color_preview'):
                self.color_preview.configure(bg=self.editor.color_code[1])
    
    def start_draw(self, event: 'Event') -> None:
        """
        Handle mouse button press to start drawing.
        
        Args:
            event: Tkinter event containing mouse coordinates
            
        Initializes:
        1. Starting coordinates for drawing
        2. List to store drawing operation IDs
        """
        self.editor.x = event.x
        self.editor.y = event.y
        self.editor.draw_ids = []
    
    def draw(self, event: 'Event') -> None:
        """
        Handle mouse motion to draw on both canvas and image.
        
        Args:
            event: Tkinter event containing mouse coordinates
            
        Performs:
        1. Drawing on the Tkinter canvas for immediate visual feedback
        2. Drawing on the OpenCV image for permanent changes
        """
        # Draw on canvas
        self.editor.draw_ids.append(
            self.editor.canvas.create_line(
                self.editor.x,
                self.editor.y,
                event.x,
                event.y,
                width=2,
                fill=self.editor.color_code[-1],
                capstyle=ROUND,
                smooth=True
            )
        )
        
        # Draw on image using OpenCV
        cv2.line(
            self.editor.filtered_image,
            (int(self.editor.x * self.editor.ratio),
             int(self.editor.y * self.editor.ratio)),
            (int(event.x * self.editor.ratio),
             int(event.y * self.editor.ratio)),
            (0, 0, 255),  # BGR color format
            thickness=int(self.editor.ratio * 2),
            lineType=8
        )
        
        # Update coordinates for next segment
        self.editor.x = event.x
        self.editor.y = event.y
    
    def convert_color_to_bgr(self, hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex color code to BGR format for OpenCV.
        
        Args:
            hex_color: Color in hexadecimal format (e.g., '#FF0000')
            
        Returns:
            Tuple containing BGR values
            
        Example:
            >>> convert_color_to_bgr('#FF0000')
            (0, 0, 255)  # Red in BGR
        """
        # Remove the '#' and convert to RGB
        rgb = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        # Convert RGB to BGR
        return (rgb[2], rgb[1], rgb[0])