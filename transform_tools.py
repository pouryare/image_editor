"""
Transform Tools Module for Image Editor Application

This module handles all image transformation operations for the Image Editor application.
It provides tools for basic geometric transformations including:
1. Rotation (90° left/right)
2. Flips (horizontal/vertical)
3. Basic image transformations
4. Transformation state management

Key Features:
- Multiple transformation options
- Lossless transformations
- Proper aspect ratio handling
- Quick preview
- State tracking

Dependencies:
- cv2 (OpenCV) for image transformations
- tkinter for GUI components
- typing for type hints

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import Optional, TYPE_CHECKING
from tkinter import ttk
import cv2

if TYPE_CHECKING:
    from image_editor import ImageEditor

class TransformTools:
    """
    Class containing all transformation-related functionality for the Image Editor.
    
    This class manages both rotation and flip operations, providing a unified
    interface for image transformations.
    """
    
    def __init__(self, editor: 'ImageEditor') -> None:
        """
        Initialize the TransformTools class.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        Initializes:
            - Reference to main editor
            - Transform state tracking
        """
        self.editor = editor
        self.current_rotation: int = 0  # Tracks current rotation in degrees
        self.is_flipped_h: bool = False  # Tracks horizontal flip state
        self.is_flipped_v: bool = False  # Tracks vertical flip state
    
    def setup_rotation_tools(self) -> None:
        """
        Set up the rotation interface in the side frame.
        
        Creates:
        1. Rotation title
        2. Rotation buttons (left/right)
        3. Current rotation indicator
        """
        # Refresh the side frame
        self.editor.refresh_side_frame()
        
        # Add title
        ttk.Label(
            self.editor.side_frame,
            text="Rotate Image",
            font=('Helvetica', 12, 'bold'),
            style='Custom.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Create buttons frame
        btn_frame = ttk.Frame(
            self.editor.side_frame,
            style='Custom.TFrame'
        )
        btn_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)
        
        # Add rotation buttons
        ttk.Button(
            btn_frame,
            text="↺ Rotate Left",
            command=self.rotate_left,
            style='Secondary.TButton'
        ).grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Button(
            btn_frame,
            text="↻ Rotate Right",
            command=self.rotate_right,
            style='Secondary.TButton'
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # Add rotation indicator
        self.rotation_label = ttk.Label(
            self.editor.side_frame,
            text=f"Current Rotation: {self.current_rotation}°",
            style='Custom.TLabel'
        )
        self.rotation_label.grid(row=2, column=0, columnspan=2, pady=10)
    
    def setup_flip_tools(self) -> None:
        """
        Set up the flip interface in the side frame.
        
        Creates:
        1. Flip title
        2. Flip buttons (horizontal/vertical)
        3. Flip state indicators
        """
        # Refresh the side frame
        self.editor.refresh_side_frame()
        
        # Add title
        ttk.Label(
            self.editor.side_frame,
            text="Flip Image",
            font=('Helvetica', 12, 'bold'),
            style='Custom.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Create buttons frame
        btn_frame = ttk.Frame(
            self.editor.side_frame,
            style='Custom.TFrame'
        )
        btn_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)
        
        # Add flip buttons
        ttk.Button(
            btn_frame,
            text="⇕ Vertical Flip",
            command=self.flip_vertical,
            style='Secondary.TButton'
        ).grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Button(
            btn_frame,
            text="⇔ Horizontal Flip",
            command=self.flip_horizontal,
            style='Secondary.TButton'
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # Add flip state indicators
        self.flip_state_label = ttk.Label(
            self.editor.side_frame,
            text=self._get_flip_state_text(),
            style='Custom.TLabel'
        )
        self.flip_state_label.grid(row=2, column=0, columnspan=2, pady=10)
    
    def rotate_left(self) -> None:
        """
        Rotate image 90 degrees counterclockwise.
        
        Notes:
            - Uses cv2.ROTATE_90_COUNTERCLOCKWISE
            - Updates rotation state
            - Updates display
        """
        try:
            self.editor.filtered_image = cv2.rotate(
                self.editor.filtered_image,
                cv2.ROTATE_90_COUNTERCLOCKWISE
            )
            self.current_rotation = (self.current_rotation - 90) % 360
            self._update_rotation_label()
            self.editor.display_image(self.editor.filtered_image)
        except cv2.error as e:
            print(f"Error rotating image left: {e}")
    
    def rotate_right(self) -> None:
        """
        Rotate image 90 degrees clockwise.
        
        Notes:
            - Uses cv2.ROTATE_90_CLOCKWISE
            - Updates rotation state
            - Updates display
        """
        try:
            self.editor.filtered_image = cv2.rotate(
                self.editor.filtered_image,
                cv2.ROTATE_90_CLOCKWISE
            )
            self.current_rotation = (self.current_rotation + 90) % 360
            self._update_rotation_label()
            self.editor.display_image(self.editor.filtered_image)
        except cv2.error as e:
            print(f"Error rotating image right: {e}")
    
    def flip_vertical(self) -> None:
        """
        Flip image vertically (up/down).
        
        Notes:
            - Uses cv2.flip with flipCode=0
            - Toggles vertical flip state
            - Updates display
        """
        try:
            self.editor.filtered_image = cv2.flip(
                self.editor.filtered_image,
                0  # flipCode=0 for vertical flip
            )
            self.is_flipped_v = not self.is_flipped_v
            self._update_flip_state_label()
            self.editor.display_image(self.editor.filtered_image)
        except cv2.error as e:
            print(f"Error flipping image vertically: {e}")
    
    def flip_horizontal(self) -> None:
        """
        Flip image horizontally (left/right).
        
        Notes:
            - Uses cv2.flip with flipCode=1
            - Toggles horizontal flip state
            - Updates display
        """
        try:
            self.editor.filtered_image = cv2.flip(
                self.editor.filtered_image,
                1  # flipCode=1 for horizontal flip
            )
            self.is_flipped_h = not self.is_flipped_h
            self._update_flip_state_label()
            self.editor.display_image(self.editor.filtered_image)
        except cv2.error as e:
            print(f"Error flipping image horizontally: {e}")
    
    def _update_rotation_label(self) -> None:
        """
        Update the rotation state label.
        
        Updates the display to show current rotation angle.
        """
        if hasattr(self, 'rotation_label'):
            self.rotation_label.config(
                text=f"Current Rotation: {self.current_rotation}°"
            )
    
    def _update_flip_state_label(self) -> None:
        """
        Update the flip state label.
        
        Updates the display to show current flip states.
        """
        if hasattr(self, 'flip_state_label'):
            self.flip_state_label.config(text=self._get_flip_state_text())
    
    def _get_flip_state_text(self) -> str:
        """
        Get the current flip state text.
        
        Returns:
            str: Description of current flip states
            
        Example:
            "Flipped: Horizontal"
            "Flipped: Vertical"
            "Flipped: Horizontal and Vertical"
        """
        states = []
        if self.is_flipped_h:
            states.append("Horizontal")
        if self.is_flipped_v:
            states.append("Vertical")
        
        if states:
            return f"Flipped: {' and '.join(states)}"
        return "No Flips Applied"
    
    def reset_transforms(self) -> None:
        """
        Reset all transformation states.
        
        Called when:
        1. Loading new image
        2. Reverting changes
        3. Applying changes
        """
        self.current_rotation = 0
        self.is_flipped_h = False
        self.is_flipped_v = False
        
        # Update labels if they exist
        if hasattr(self, 'rotation_label'):
            self._update_rotation_label()
        if hasattr(self, 'flip_state_label'):
            self._update_flip_state_label()
