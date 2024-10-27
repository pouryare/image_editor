"""
Blur Tools Module for Image Editor Application

This module handles all blur-related functionality for the Image Editor application.
It provides three main types of blur effects:
1. Average (Box) Blur
2. Gaussian Blur
3. Median Blur

Each blur type offers different characteristics and use cases:
- Average Blur: Simple and fast, good for noise reduction
- Gaussian Blur: More natural-looking blur, preserves edges better
- Median Blur: Excellent for removing salt-and-pepper noise

The module provides real-time preview of blur effects with adjustable intensity
using slider controls.

Key Features:
- Multiple blur types
- Interactive intensity control
- Real-time preview
- Optimized performance
- Edge case handling

Dependencies:
- cv2 (OpenCV) for blur operations
- tkinter for GUI components
- typing for type hints

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import Optional, TYPE_CHECKING
from tkinter import ttk, Scale, HORIZONTAL
import cv2

if TYPE_CHECKING:
    from image_editor import ImageEditor

class BlurTools:
    """
    Class containing all blur-related functionality for the Image Editor.
    
    This class manages the blur interface and handles the application
    of various blur effects with adjustable parameters.
    """
    
    def __init__(self, editor: 'ImageEditor') -> None:
        """
        Initialize the BlurTools class.
        
        Args:
            editor: Reference to the main ImageEditor instance
        
        Initializes:
            - Reference to main editor
            - Slider variables
        """
        self.editor = editor
        self.average_slider: Optional[Scale] = None
        self.gaussian_slider: Optional[Scale] = None
        self.median_slider: Optional[Scale] = None
    
    def setup_blur_tools(self) -> None:
        """
        Set up the blur interface in the side frame.
        
        Creates:
        1. Blur tools title
        2. Average blur slider
        3. Gaussian blur slider
        4. Median blur slider
        """
        # Refresh the side frame
        self.editor.refresh_side_frame()
        
        # Add title
        ttk.Label(
            self.editor.side_frame,
            text="Blur Effects",
            font=('Helvetica', 12, 'bold'),
            style='Custom.TLabel'
        ).grid(row=0, column=0, pady=(0, 15))
        
        # Setup Average Blur controls
        self._setup_average_blur()
        
        # Setup Gaussian Blur controls
        self._setup_gaussian_blur()
        
        # Setup Median Blur controls
        self._setup_median_blur()
    
    def _setup_average_blur(self) -> None:
        """
        Set up the average blur controls.
        
        Creates:
        1. Label for average blur
        2. Slider for controlling blur intensity
        """
        ttk.Label(
            self.editor.side_frame,
            text="Average Blur",
            style='Custom.TLabel'
        ).grid(row=1, column=0, padx=5, sticky='sw')
        
        self.average_slider = Scale(
            self.editor.side_frame,
            from_=0,
            to=256,
            orient=HORIZONTAL,
            command=self.apply_average_blur,
            length=200,
            bg='#34495e',
            fg='white',
            troughcolor='#2c3e50',
            highlightthickness=0
        )
        self.average_slider.grid(row=2, column=0, padx=5, sticky='ew')
    
    def _setup_gaussian_blur(self) -> None:
        """
        Set up the Gaussian blur controls.
        
        Creates:
        1. Label for Gaussian blur
        2. Slider for controlling blur intensity
        """
        ttk.Label(
            self.editor.side_frame,
            text="Gaussian Blur",
            style='Custom.TLabel'
        ).grid(row=3, column=0, padx=5, pady=(20,0), sticky='sw')
        
        self.gaussian_slider = Scale(
            self.editor.side_frame,
            from_=0,
            to=256,
            orient=HORIZONTAL,
            command=self.apply_gaussian_blur,
            length=200,
            bg='#34495e',
            fg='white',
            troughcolor='#2c3e50',
            highlightthickness=0
        )
        self.gaussian_slider.grid(row=4, column=0, padx=5, sticky='ew')
    
    def _setup_median_blur(self) -> None:
        """
        Set up the median blur controls.
        
        Creates:
        1. Label for median blur
        2. Slider for controlling blur intensity
        """
        ttk.Label(
            self.editor.side_frame,
            text="Median Blur",
            style='Custom.TLabel'
        ).grid(row=5, column=0, padx=5, pady=(20,0), sticky='sw')
        
        self.median_slider = Scale(
            self.editor.side_frame,
            from_=0,
            to=256,
            orient=HORIZONTAL,
            command=self.apply_median_blur,
            length=200,
            bg='#34495e',
            fg='white',
            troughcolor='#2c3e50',
            highlightthickness=0
        )
        self.median_slider.grid(row=6, column=0, padx=5, sticky='ew')
    
    def apply_average_blur(self, value: str) -> None:
        """
        Apply average (box) blur to the image.
        
        Args:
            value: Blur kernel size as string (converted to int)
            
        Notes:
            - Kernel size must be odd
            - Larger kernel size = stronger blur effect
            - Uses cv2.blur for the operation
        """
        # Convert value to integer
        kernel_size = int(float(value))
        
        # Ensure kernel size is odd
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        # Apply blur if kernel size > 1
        if kernel_size > 1:
            self.editor.filtered_image = cv2.blur(
                self.editor.edited_image,
                (kernel_size, kernel_size)
            )
            self.editor.display_image(self.editor.filtered_image)
        else:
            # Reset to original image if kernel size is too small
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.editor.display_image(self.editor.filtered_image)
    
    def apply_gaussian_blur(self, value: str) -> None:
        """
        Apply Gaussian blur to the image.
        
        Args:
            value: Blur kernel size as string (converted to int)
            
        Notes:
            - Kernel size must be odd
            - Uses cv2.GaussianBlur with automatic sigma calculation
            - More natural-looking blur than average blur
        """
        # Convert value to integer
        kernel_size = int(float(value))
        
        # Ensure kernel size is odd
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        # Apply blur if kernel size > 1
        if kernel_size > 1:
            self.editor.filtered_image = cv2.GaussianBlur(
                self.editor.edited_image,
                (kernel_size, kernel_size),
                0  # Auto-calculate sigma
            )
            self.editor.display_image(self.editor.filtered_image)
        else:
            # Reset to original image if kernel size is too small
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.editor.display_image(self.editor.filtered_image)
    
    def apply_median_blur(self, value: str) -> None:
        """
        Apply median blur to the image.
        
        Args:
            value: Blur kernel size as string (converted to int)
            
        Notes:
            - Kernel size must be odd
            - Effective for removing salt-and-pepper noise
            - More computationally intensive than other blur types
        """
        # Convert value to integer
        kernel_size = int(float(value))
        
        # Ensure kernel size is odd
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        # Apply blur if kernel size > 1
        if kernel_size > 1:
            self.editor.filtered_image = cv2.medianBlur(
                self.editor.edited_image,
                kernel_size
            )
            self.editor.display_image(self.editor.filtered_image)
        else:
            # Reset to original image if kernel size is too small
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.editor.display_image(self.editor.filtered_image)
    
    def reset_blur_sliders(self) -> None:
        """
        Reset all blur sliders to their initial positions.
        
        This method is called when:
        1. Switching to a different tool
        2. Applying changes
        3. Canceling changes
        """
        if self.average_slider:
            self.average_slider.set(0)
        if self.gaussian_slider:
            self.gaussian_slider.set(0)
        if self.median_slider:
            self.median_slider.set(0)
