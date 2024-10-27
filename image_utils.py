"""
Image Utilities Module for Image Editor Application

This module provides utility functions for image processing and display operations.
It handles:
1. Image display and rendering
2. Image resizing and scaling
3. Canvas management
4. Coordinate calculations
5. Color space conversions
6. Image preprocessing

Key Features:
- Aspect ratio preservation
- Dynamic scaling
- Efficient memory usage
- Canvas centering
- Border handling
- Color management

Dependencies:
- cv2 (OpenCV) for image processing
- PIL for image conversion
- tkinter for canvas operations
- numpy for array operations
- typing for type hints

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import Optional, Tuple, TYPE_CHECKING
import cv2
from PIL import Image, ImageTk
import numpy as np

if TYPE_CHECKING:
    from image_editor import ImageEditor

class ImageUtils:
    """
    Class containing utility functions for image processing and display.
    
    This class provides helper methods for image manipulation and
    canvas rendering operations.
    """
    
    def __init__(self, editor: 'ImageEditor') -> None:
        """
        Initialize the ImageUtils class.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        Initializes:
            - Reference to main editor
            - Canvas dimensions
            - Display parameters
        """
        self.editor = editor
        self.default_width: int = 900
        self.default_height: int = 700
        self.padding: int = 100  # Padding around image
        
    def display_image(self, image: Optional[np.ndarray] = None) -> None:
        """
        Display an image on the canvas with proper scaling and centering.
        
        Args:
            image: OpenCV image array (BGR format) to display
                  If None, displays the current edited image
                  
        Process:
        1. Clear canvas
        2. Convert color space
        3. Calculate dimensions
        4. Resize if necessary
        5. Create PhotoImage
        6. Center and display
        7. Add border
        """
        try:
            # Clear existing content
            self.editor.canvas.delete("all")
            
            # Use provided image or current edited image
            if image is None:
                image = self.editor.edited_image.copy()
            
            # Convert color space for display
            display_image = self._convert_to_display_format(image)
            
            # Get image dimensions
            height, width = image.shape[:2]
            
            # Calculate display dimensions
            new_width, new_height = self._calculate_display_dimensions(
                width, height
            )
            
            # Calculate scale ratio
            self.editor.ratio = height / new_height
            
            # Resize image
            display_image = self._resize_image(
                display_image,
                new_width,
                new_height
            )
            
            # Create PhotoImage
            self.editor.new_image = ImageTk.PhotoImage(
                Image.fromarray(display_image)
            )
            
            # Configure canvas size
            canvas_width = max(new_width + self.padding, self.default_width)
            canvas_height = max(new_height + self.padding, self.default_height)
            self.editor.canvas.config(
                width=canvas_width,
                height=canvas_height
            )
            
            # Calculate center position
            x_center = canvas_width // 2
            y_center = canvas_height // 2
            
            # Store offsets for other operations
            self.editor.x_offset = x_center - new_width // 2
            self.editor.y_offset = y_center - new_height // 2
            
            # Display image
            self.editor.canvas.create_image(
                x_center,
                y_center,
                image=self.editor.new_image
            )
            
            # Add border
            self._add_border(
                x_center,
                y_center,
                new_width,
                new_height
            )
            
        except Exception as e:
            print(f"Error in display_image: {e}")
            
    def _convert_to_display_format(self, image: np.ndarray) -> np.ndarray:
        """
        Convert image from BGR to RGB format for display.
        
        Args:
            image: OpenCV image array in BGR format
            
        Returns:
            numpy.ndarray: Image array in RGB format
            
        Handles color space conversion for proper display.
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    def _calculate_display_dimensions(
        self,
        width: int,
        height: int
    ) -> Tuple[int, int]:
        """
        Calculate appropriate display dimensions maintaining aspect ratio.
        
        Args:
            width: Original image width
            height: Original image height
            
        Returns:
            Tuple containing new width and height
            
        Ensures image fits within display area while preserving aspect ratio.
        """
        ratio = height / width
        max_width = self.default_width - self.padding
        max_height = self.default_height - self.padding
        
        if height > max_height or width > max_width:
            if ratio < 1:
                new_width = max_width
                new_height = int(new_width * ratio)
            else:
                new_height = max_height
                new_width = int(new_height * (width / height))
        else:
            new_width = width
            new_height = height
            
        return new_width, new_height
    
    def _resize_image(
        self,
        image: np.ndarray,
        width: int,
        height: int
    ) -> np.ndarray:
        """
        Resize image to specified dimensions.
        
        Args:
            image: Image array to resize
            width: Target width
            height: Target height
            
        Returns:
            numpy.ndarray: Resized image array
            
        Uses cv2.INTER_AREA for downsizing and cv2.INTER_LINEAR for upsizing.
        """
        original_height, original_width = image.shape[:2]
        
        # Choose interpolation method based on scaling direction
        if width * height < original_width * original_height:
            interpolation = cv2.INTER_AREA  # For downsizing
        else:
            interpolation = cv2.INTER_LINEAR  # For upsizing
            
        return cv2.resize(
            image,
            (width, height),
            interpolation=interpolation
        )
    
    def _add_border(
        self,
        x_center: int,
        y_center: int,
        width: int,
        height: int
    ) -> None:
        """
        Add decorative border around the displayed image.
        
        Args:
            x_center: Center x coordinate
            y_center: Center y coordinate
            width: Image width
            height: Image height
            
        Creates a rectangular border with rounded corners (if implemented).
        """
        self.editor.canvas.create_rectangle(
            x_center - width//2 - 2,
            y_center - height//2 - 2,
            x_center + width//2 + 2,
            y_center + height//2 + 2,
            outline='#3498db',
            width=2
        )
        
    def get_image_info(self) -> dict:
        """
        Get current image information.
        
        Returns:
            dict: Dictionary containing image information
            
        Information includes:
        - Dimensions
        - Color channels
        - Data type
        - Memory usage
        """
        if self.editor.edited_image is None:
            return {}
            
        height, width = self.editor.edited_image.shape[:2]
        channels = self.editor.edited_image.shape[2] if len(self.editor.edited_image.shape) > 2 else 1
        
        return {
            'width': width,
            'height': height,
            'channels': channels,
            'dtype': str(self.editor.edited_image.dtype),
            'size_mb': self.editor.edited_image.nbytes / (1024 * 1024)
        }
    
    def get_canvas_coordinates(self, image_x: int, image_y: int) -> Tuple[int, int]:
        """
        Convert image coordinates to canvas coordinates.
        
        Args:
            image_x: X coordinate in image space
            image_y: Y coordinate in image space
            
        Returns:
            Tuple of canvas x, y coordinates
            
        Used for coordinate conversion between image and display space.
        """
        canvas_x = int(image_x / self.editor.ratio) + self.editor.x_offset
        canvas_y = int(image_y / self.editor.ratio) + self.editor.y_offset
        return canvas_x, canvas_y
    
    def get_image_coordinates(self, canvas_x: int, canvas_y: int) -> Tuple[int, int]:
        """
        Convert canvas coordinates to image coordinates.
        
        Args:
            canvas_x: X coordinate in canvas space
            canvas_y: Y coordinate in canvas space
            
        Returns:
            Tuple of image x, y coordinates
            
        Used for coordinate conversion between display and image space.
        """
        image_x = int((canvas_x - self.editor.x_offset) * self.editor.ratio)
        image_y = int((canvas_y - self.editor.y_offset) * self.editor.ratio)
        return image_x, image_y
