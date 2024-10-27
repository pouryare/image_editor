"""
Filter Tools Module for Image Editor Application

This module handles all filter-related functionality for the Image Editor application.
It provides a variety of image filters and effects, including:
1. Basic filters (Negative, Black & White)
2. Artistic filters (Stylization, Sketch)
3. Color effects (Sepia, Emboss)
4. Binary operations (Threshold, Erosion, Dilation)

Each filter is implemented using OpenCV operations and can be toggled on/off.
The module maintains filter states and handles filter application/removal.

Key Features:
- Multiple filter types
- Toggle functionality
- Real-time preview
- Filter state management
- Undo capability

Dependencies:
- cv2 (OpenCV) for image processing
- numpy for array operations
- typing for type hints

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import Dict, Optional, TYPE_CHECKING
import cv2
import numpy as np
from tkinter import ttk

if TYPE_CHECKING:
    from image_editor import ImageEditor

class FilterTools:
    """
    Class containing all filter-related functionality for the Image Editor.
    
    This class manages the filter interface and handles the application
    and removal of various image filters.
    """
    
    def __init__(self, editor: 'ImageEditor') -> None:
        """
        Initialize the FilterTools class.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        Initializes:
            - Reference to main editor
            - Filter states dictionary
        """
        self.editor = editor
        # Initialize filter states
        self.filter_states: Dict[str, bool] = {
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
    
    def setup_filter_tools(self) -> None:
        """
        Set up the filter interface in the side frame.
        
        Creates:
        1. Filter title
        2. Filter buttons
        3. Additional filter options (if any)
        """
        # Refresh the side frame
        self.editor.refresh_side_frame()
        
        # Add title
        ttk.Label(
            self.editor.side_frame,
            text="Image Filters",
            font=('Helvetica', 12, 'bold'),
            style='Custom.TLabel'
        ).grid(row=0, column=0, pady=(0, 15))
        
        # Create filter buttons
        filter_buttons = [
            ("Negative", self.negative_filter),
            ("B&W", self.black_and_white_filter),
            ("Stylisation", self.stylisation_filter),
            ("Sketch", self.sketch_filter),
            ("Emboss", self.emboss_filter),
            ("Sepia", self.sepia_filter),
            ("Binary", self.binary_threshold_filter),
            ("Erosion", self.erosion_filter),
            ("Dilation", self.dilation_filter)
        ]
        
        # Add filter buttons to side frame
        for idx, (text, command) in enumerate(filter_buttons, 1):
            btn = ttk.Button(
                self.editor.side_frame,
                text=text,
                command=command,
                style='Filter.TButton'
            )
            btn.grid(row=idx, column=0, padx=5, pady=3, sticky='ew')
    
    def negative_filter(self) -> None:
        """
        Apply or remove negative filter.
        
        This filter inverts all pixel values in the image.
        Uses cv2.bitwise_not for the operation.
        """
        if not self.filter_states['negative']:
            self.editor.filtered_image = cv2.bitwise_not(self.editor.edited_image)
            self.filter_states['negative'] = True
        else:
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.filter_states['negative'] = False
            
        self.editor.display_image(self.editor.filtered_image)
    
    def black_and_white_filter(self) -> None:
        """
        Apply or remove black and white filter.
        
        Converts image to grayscale using cv2.cvtColor.
        Maintains 3 channels for compatibility with other filters.
        """
        if not self.filter_states['bw']:
            gray = cv2.cvtColor(self.editor.edited_image, cv2.COLOR_BGR2GRAY)
            self.editor.filtered_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            self.filter_states['bw'] = True
        else:
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.filter_states['bw'] = False
            
        self.editor.display_image(self.editor.filtered_image)
    
    def stylisation_filter(self) -> None:
        """
        Apply or remove stylisation filter.
        
        Uses cv2.stylization for artistic effect.
        Parameters:
        - sigma_s: Range between 0 to 200
        - sigma_r: Range between 0 to 1
        """
        if not self.filter_states['stylisation']:
            self.editor.filtered_image = cv2.stylization(
                self.editor.edited_image,
                sigma_s=150,
                sigma_r=0.25
            )
            self.filter_states['stylisation'] = True
        else:
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.filter_states['stylisation'] = False
            
        self.editor.display_image(self.editor.filtered_image)
    
    def sketch_filter(self) -> None:
        """
        Apply or remove sketch filter.
        
        Uses cv2.pencilSketch for pencil drawing effect.
        Parameters:
        - sigma_s: Edge preservation
        - sigma_r: Tone preservation
        - shade_factor: Intensity of shading
        """
        if not self.filter_states['sketch']:
            _, self.editor.filtered_image = cv2.pencilSketch(
                self.editor.edited_image,
                sigma_s=60,
                sigma_r=0.5,
                shade_factor=0.02
            )
            self.filter_states['sketch'] = True
        else:
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.filter_states['sketch'] = False
            
        self.editor.display_image(self.editor.filtered_image)
    
    def emboss_filter(self) -> None:
        """
        Apply or remove emboss filter.
        
        Uses custom kernel convolution for emboss effect:
        [[-1, -1,  0],
         [-1,  0,  1],
         [ 0,  1,  1]]
        """
        if not self.filter_states['emboss']:
            kernel = np.array([
                [-1, -1, 0],
                [-1, 0, 1],
                [0, 1, 1]
            ])
            self.editor.filtered_image = cv2.filter2D(
                self.editor.edited_image,
                -1,
                kernel
            )
            self.filter_states['emboss'] = True
        else:
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.filter_states['emboss'] = False
            
        self.editor.display_image(self.editor.filtered_image)
    
    def sepia_filter(self) -> None:
        """
        Apply or remove sepia filter.
        
        Uses matrix transformation:
        [[0.272, 0.534, 0.131],
         [0.349, 0.686, 0.168],
         [0.393, 0.769, 0.189]]
        """
        if not self.filter_states['sepia']:
            kernel = np.array([
                [0.272, 0.534, 0.131],
                [0.349, 0.686, 0.168],
                [0.393, 0.769, 0.189]
            ])
            self.editor.filtered_image = cv2.filter2D(
                self.editor.edited_image,
                -1,
                kernel
            )
            self.filter_states['sepia'] = True
        else:
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.filter_states['sepia'] = False
            
        self.editor.display_image(self.editor.filtered_image)
    
    def binary_threshold_filter(self) -> None:
        """
        Apply or remove binary threshold filter.
        
        Uses cv2.threshold for binary image effect.
        Threshold value: 127
        Maximum value: 255
        """
        if not self.filter_states['binary']:
            _, self.editor.filtered_image = cv2.threshold(
                self.editor.edited_image,
                127,
                255,
                cv2.THRESH_BINARY
            )
            self.filter_states['binary'] = True
        else:
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.filter_states['binary'] = False
            
        self.editor.display_image(self.editor.filtered_image)
    
    def erosion_filter(self) -> None:
        """
        Apply or remove erosion filter.
        
        Uses cv2.erode for morphological erosion.
        Kernel size: 5x5
        Iterations: 1
        """
        if not self.filter_states['erosion']:
            kernel = np.ones((5, 5), np.uint8)
            self.editor.filtered_image = cv2.erode(
                self.editor.edited_image,
                kernel,
                iterations=1
            )
            self.filter_states['erosion'] = True
        else:
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.filter_states['erosion'] = False
            
        self.editor.display_image(self.editor.filtered_image)
    
    def dilation_filter(self) -> None:
        """
        Apply or remove dilation filter.
        
        Uses cv2.dilate for morphological dilation.
        Kernel size: 5x5
        Iterations: 1
        """
        if not self.filter_states['dilation']:
            kernel = np.ones((5, 5), np.uint8)
            self.editor.filtered_image = cv2.dilate(
                self.editor.edited_image,
                kernel,
                iterations=1
            )
            self.filter_states['dilation'] = True
        else:
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.filter_states['dilation'] = False
            
        self.editor.display_image(self.editor.filtered_image)

