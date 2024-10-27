"""
Adjust Tools Module for Image Editor Application

This module handles all image adjustment functionality for the Image Editor application.
It provides tools for adjusting basic image properties including:
1. Brightness
2. Saturation
3. Color balance
4. Contrast (if implemented)

The module provides real-time preview of adjustments using slider controls
and maintains proper color space conversions for accurate results.

Key Features:
- Real-time adjustment preview
- Multiple adjustment parameters
- Color space handling
- Value range validation
- Smooth transitions

Dependencies:
- cv2 (OpenCV) for image processing
- numpy for array operations
- tkinter for GUI components
- typing for type hints

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import Optional, TYPE_CHECKING
from tkinter import ttk, Scale, HORIZONTAL
import cv2
import numpy as np

if TYPE_CHECKING:
    from image_editor import ImageEditor
    from tkinter import Event

class AdjustTools:
    """
    Class containing all adjustment-related functionality for the Image Editor.
    
    This class manages the adjustment interface and handles various
    image adjustment operations with real-time preview.
    """
    
    def __init__(self, editor: 'ImageEditor') -> None:
        """
        Initialize the AdjustTools class.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        Initializes:
            - Reference to main editor
            - Slider variables
            - Default values
        """
        self.editor = editor
        self.brightness_slider: Optional[Scale] = None
        self.saturation_slider: Optional[Scale] = None
        
        # Default adjustment values
        self.DEFAULT_BRIGHTNESS: float = 1.0
        self.DEFAULT_SATURATION: float = 0.0
    
    def setup_adjust_tools(self) -> None:
        """
        Set up the adjustment interface in the side frame.
        
        Creates:
        1. Adjustment tools title
        2. Brightness slider
        3. Saturation slider
        4. Other adjustment controls (if implemented)
        """
        # Create a copy of the edited image for adjustments
        self.editor.filtered_image = self.editor.edited_image.copy()
        
        # Refresh the side frame
        self.editor.refresh_side_frame()
        
        # Add title
        ttk.Label(
            self.editor.side_frame,
            text="Adjust Image",
            font=('Helvetica', 12, 'bold'),
            style='Custom.TLabel'
        ).grid(row=0, column=0, pady=(0, 15))
        
        # Setup brightness control
        self._setup_brightness_control()
        
        # Setup saturation control
        self._setup_saturation_control()
    
    def _setup_brightness_control(self) -> None:
        """
        Set up the brightness adjustment controls.
        
        Creates:
        1. Label for brightness
        2. Slider for controlling brightness level
        3. Sets default value
        """
        ttk.Label(
            self.editor.side_frame,
            text="Brightness",
            style='Custom.TLabel'
        ).grid(row=1, column=0, padx=5, sticky='sw')
        
        self.brightness_slider = Scale(
            self.editor.side_frame,
            from_=0,
            to_=2,
            resolution=0.1,
            orient=HORIZONTAL,
            command=self.apply_brightness,
            length=200,
            bg='#34495e',
            fg='white',
            troughcolor='#2c3e50',
            highlightthickness=0
        )
        self.brightness_slider.grid(row=2, column=0, padx=5, sticky='ew')
        self.brightness_slider.set(self.DEFAULT_BRIGHTNESS)
    
    def _setup_saturation_control(self) -> None:
        """
        Set up the saturation adjustment controls.
        
        Creates:
        1. Label for saturation
        2. Slider for controlling saturation level
        3. Sets default value
        """
        ttk.Label(
            self.editor.side_frame,
            text="Saturation",
            style='Custom.TLabel'
        ).grid(row=3, column=0, padx=5, pady=(20,0), sticky='sw')
        
        self.saturation_slider = Scale(
            self.editor.side_frame,
            from_=-200,
            to=200,
            resolution=0.5,
            orient=HORIZONTAL,
            command=self.apply_saturation,
            length=200,
            bg='#34495e',
            fg='white',
            troughcolor='#2c3e50',
            highlightthickness=0
        )
        self.saturation_slider.grid(row=4, column=0, padx=5, sticky='ew')
        self.saturation_slider.set(self.DEFAULT_SATURATION)
    
    def apply_brightness(self, value: str) -> None:
        """
        Apply brightness adjustment to the image.
        
        Args:
            value: Brightness multiplier as string (converted to float)
            
        Notes:
            - value < 1.0: darker image
            - value = 1.0: original image
            - value > 1.0: brighter image
            
        Implementation uses cv2.convertScaleAbs for proper value handling.
        """
        try:
            brightness_value = float(value)
            self.editor.filtered_image = cv2.convertScaleAbs(
                self.editor.edited_image.copy(),
                alpha=brightness_value
            )
            self.editor.display_image(self.editor.filtered_image)
        except (ValueError, cv2.error) as e:
            print(f"Error applying brightness: {e}")
            # Revert to original image on error
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.editor.display_image(self.editor.filtered_image)
    
    def apply_saturation(self, event: str) -> None:
        """
        Apply saturation adjustment to the image.
        
        Args:
            event: Saturation adjustment value as string
            
        Notes:
            - Converts image to HSV color space
            - Adjusts S channel
            - Converts back to BGR
            - Handles value clamping
        """
        try:
            # Convert image to HSV
            img_hsv = cv2.cvtColor(
                self.editor.edited_image.copy(),
                cv2.COLOR_BGR2HSV
            ).astype("float32")
            
            # Calculate saturation factor
            saturation_value = float(self.saturation_slider.get())
            saturation_factor = (saturation_value + 200) / 200
            
            # Apply saturation adjustment
            img_hsv[:, :, 1] = img_hsv[:, :, 1] * saturation_factor
            
            # Clamp values to valid range
            img_hsv[:, :, 1] = np.clip(img_hsv[:, :, 1], 0, 255)
            
            # Convert back to BGR
            self.editor.filtered_image = cv2.cvtColor(
                img_hsv.astype("uint8"),
                cv2.COLOR_HSV2BGR
            )
            
            self.editor.display_image(self.editor.filtered_image)
            
        except (ValueError, cv2.error) as e:
            print(f"Error applying saturation: {e}")
            # Revert to original image on error
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.editor.display_image(self.editor.filtered_image)
    
    def reset_adjustments(self) -> None:
        """
        Reset all adjustment sliders to their default values.
        
        This method is called when:
        1. Switching to a different tool
        2. Applying changes
        3. Canceling changes
        4. Reverting to original image
        """
        if self.brightness_slider:
            self.brightness_slider.set(self.DEFAULT_BRIGHTNESS)
        if self.saturation_slider:
            self.saturation_slider.set(self.DEFAULT_SATURATION)
    
    def get_adjustment_values(self) -> dict:
        """
        Get current values of all adjustment sliders.
        
        Returns:
            dict: Dictionary containing current adjustment values
            
        Used for:
        1. Saving adjustment state
        2. Applying multiple adjustments
        3. Debugging
        """
        return {
            'brightness': float(self.brightness_slider.get()) if self.brightness_slider else self.DEFAULT_BRIGHTNESS,
            'saturation': float(self.saturation_slider.get()) if self.saturation_slider else self.DEFAULT_SATURATION
        }
