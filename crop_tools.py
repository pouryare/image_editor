"""
Crop Tools Module for Image Editor Application

This module handles all crop-related functionality for the Image Editor application.
It provides tools for selecting and cropping image regions, including:
1. Crop tool initialization and setup
2. Selection rectangle drawing
3. Coordinate calculation and validation
4. Final crop operation execution

The module integrates both the visual representation of the crop selection on the canvas
and the actual image cropping using OpenCV.

Key Features:
- Interactive crop selection
- Real-time visual feedback
- Coordinate validation
- Aspect ratio preservation (optional)
- Bounds checking

Dependencies:
- tkinter and ttk for GUI components
- cv2 (OpenCV) for image manipulation
- numpy for array operations
- typing for type hints

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import Optional, Tuple, TYPE_CHECKING
import numpy as np
from tkinter import ttk

if TYPE_CHECKING:
    from image_editor import ImageEditor
    from tkinter import Event

class CropTools:
    """
    Class containing all cropping-related functionality for the Image Editor.
    
    This class manages the cropping interface and handles crop operations
    on both the canvas and the actual image.
    """
    
    def __init__(self, editor: 'ImageEditor') -> None:
        """
        Initialize the CropTools class.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        Initializes:
            - Reference to main editor
            - Crop coordinates
            - Selection rectangle ID
        """
        self.editor = editor
        self.crop_start_x: int = 0
        self.crop_start_y: int = 0
        self.crop_end_x: int = 0
        self.crop_end_y: int = 0
        self.rectangle_id: int = 0
        
        # Minimum crop dimensions
        self.MIN_CROP_SIZE: int = 10
    
    def setup_crop_tools(self) -> None:
        """
        Set up the cropping interface in the side frame.
        
        Creates:
        1. Title and instructions
        2. Crop options (if any)
        3. Binds necessary events to canvas
        """
        # Reset crop variables
        self.rectangle_id = 0
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        
        # Create a copy of the edited image for cropping
        self.editor.filtered_image = self.editor.edited_image.copy()
        
        # Refresh the side frame
        self.editor.refresh_side_frame()
        
        # Add title
        ttk.Label(
            self.editor.side_frame,
            text="Crop Image",
            font=('Helvetica', 12, 'bold'),
            style='Custom.TLabel'
        ).grid(row=0, column=0, pady=(0, 10))
        
        # Add instructions
        ttk.Label(
            self.editor.side_frame,
            text="1. Click and drag to select area\n2. Release to crop",
            style='Custom.TLabel'
        ).grid(row=1, column=0, pady=5)
        
        # Add additional instructions
        ttk.Label(
            self.editor.side_frame,
            text="Press ESC to cancel crop\nMinimum size: 10x10 pixels",
            style='Custom.TLabel'
        ).grid(row=2, column=0, pady=(20, 5))
        
        # Bind canvas events
        self.editor.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.editor.canvas.bind("<B1-Motion>", self.update_crop)
        self.editor.canvas.bind("<ButtonRelease-1>", self.end_crop)
        self.editor.canvas.bind("<Escape>", self.cancel_crop)
    
    def start_crop(self, event: 'Event') -> None:
        """
        Handle mouse button press to start crop selection.
        
        Args:
            event: Tkinter event containing mouse coordinates
        """
        # Get the click coordinates
        self.crop_start_x = event.x
        self.crop_start_y = event.y
        
        # Save the current rectangle_id
        self.rectangle_id = 0
    
    def update_crop(self, event: 'Event') -> None:
        """
        Handle mouse motion to update crop selection rectangle.
        
        Args:
            event: Tkinter event containing current mouse coordinates
        """
        # Remove previous rectangle if it exists
        if self.rectangle_id:
            self.editor.canvas.delete(self.rectangle_id)
        
        # Update end coordinates
        self.crop_end_x = event.x
        self.crop_end_y = event.y
        
        # Draw new selection rectangle with dashed line for better visibility
        self.rectangle_id = self.editor.canvas.create_rectangle(
            self.crop_start_x, self.crop_start_y,
            self.crop_end_x, self.crop_end_y,
            outline='#2ecc71',  # Green color
            width=2,
            dash=(4, 2)  # Dashed line pattern
        )
    
    def end_crop(self, event: 'Event') -> None:
        """
        Handle mouse release to finalize crop operation.
        
        Args:
            event: Tkinter event containing final mouse coordinates
        """
        try:
            # Check if selection is too small
            if not self._validate_crop_size():
                print("Crop selection too small. Minimum size is 10x10 pixels.")
                return
            
            # Calculate image coordinates
            start_x = min(self.crop_start_x, self.crop_end_x)
            start_y = min(self.crop_start_y, self.crop_end_y)
            end_x = max(self.crop_start_x, self.crop_end_x)
            end_y = max(self.crop_start_y, self.crop_end_y)
            
            # Adjust for canvas offset and scale
            start_x = int((start_x - self.editor.x_offset) * self.editor.ratio)
            start_y = int((start_y - self.editor.y_offset) * self.editor.ratio)
            end_x = int((end_x - self.editor.x_offset) * self.editor.ratio)
            end_y = int((end_y - self.editor.y_offset) * self.editor.ratio)
            
            # Ensure coordinates are within image bounds
            height, width = self.editor.edited_image.shape[:2]
            start_x = max(0, min(start_x, width))
            start_y = max(0, min(start_y, height))
            end_x = max(0, min(end_x, width))
            end_y = max(0, min(end_y, height))
            
            # Create slices for cropping
            y_slice = slice(start_y, end_y)
            x_slice = slice(start_x, end_x)
            
            # Apply crop
            self.editor.filtered_image = self.editor.edited_image[y_slice, x_slice].copy()
            
            # Clear the selection rectangle
            if self.rectangle_id:
                self.editor.canvas.delete(self.rectangle_id)
            
            # Display the cropped image
            self.editor.display_image(self.editor.filtered_image)
            
        except Exception as e:
            print(f"Error during crop operation: {e}")
            # Revert to original image on error
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.editor.display_image(self.editor.filtered_image)
            
        finally:
            # Reset crop coordinates
            self._reset_crop_state()
    
    def cancel_crop(self, event: Optional['Event'] = None) -> None:
        """
        Cancel the current crop operation.
        
        Args:
            event: Optional Tkinter event (for key binding)
        """
        # Clear selection rectangle
        if self.rectangle_id:
            self.editor.canvas.delete(self.rectangle_id)
        
        # Reset crop state
        self._reset_crop_state()
        
        # Revert to original image
        self.editor.filtered_image = self.editor.edited_image.copy()
        self.editor.display_image(self.editor.filtered_image)
    
    def _validate_crop_size(self) -> bool:
        """
        Validate if the crop selection meets minimum size requirements.
        
        Returns:
            bool: True if selection size is valid, False otherwise
        """
        width = abs(self.crop_end_x - self.crop_start_x)
        height = abs(self.crop_end_y - self.crop_start_y)
        return width >= self.MIN_CROP_SIZE and height >= self.MIN_CROP_SIZE
    
    def _reset_crop_state(self) -> None:
        """Reset all crop-related state variables."""
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.rectangle_id = 0
    
    def get_crop_dimensions(self) -> Tuple[int, int]:
        """
        Get the dimensions of the current crop selection.
        
        Returns:
            Tuple containing width and height of selection
        """
        width = abs(self.crop_end_x - self.crop_start_x)
        height = abs(self.crop_end_y - self.crop_start_y)
        return (width, height)