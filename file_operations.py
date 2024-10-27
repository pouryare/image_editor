"""
File Operations Module for Image Editor Application

This module handles all file-related operations for the Image Editor application,
including:
1. File opening/loading
2. File saving
3. Format conversions
4. Error handling
5. File type validation

Key Features:
- Multiple format support
- Error recovery
- Path handling
- Format validation
- Safe file operations
- Progress tracking (if implemented)

Supported Formats:
- JPEG/JPG
- PNG
- BMP
- Additional formats supported by OpenCV

Dependencies:
- cv2 (OpenCV) for image I/O
- tkinter for file dialogs
- os and sys for path operations
- typing for type hints

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import Optional, Tuple, List, TYPE_CHECKING
from tkinter import filedialog
import cv2
import os
import sys

if TYPE_CHECKING:
    from image_editor import ImageEditor

class FileOperations:
    """
    Class containing all file-related functionality for the Image Editor.
    
    This class manages file operations including loading, saving,
    and format handling.
    """
    
    def __init__(self, editor: 'ImageEditor') -> None:
        """
        Initialize the FileOperations class.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        Initializes:
            - Reference to main editor
            - Supported file types
            - Default paths
        """
        self.editor = editor
        self.supported_formats: tuple = (
            '.jpg', '.jpeg', '.png', '.bmp', '.gif'
        )
        self.current_file: Optional[str] = None
        
    def upload_image(self) -> None:
        """
        Handle image upload/opening operation.
        
        Processes:
        1. File selection dialog
        2. Image loading
        3. Initial display
        4. Error handling
        
        Updates editor's image buffers on successful load.
        """
        try:
            # Clear existing canvas
            self.editor.canvas.delete("all")
            
            # Define file types for dialog
            filetypes = (
                ('Image files', '*.jpg *.jpeg *.png *.bmp *.gif'),
                ('All files', '*.*')
            )
            
            # Open file dialog
            filename = filedialog.askopenfilename(
                title='Open Image',
                filetypes=filetypes
            )
            
            # Check if file was selected
            if not filename:
                return
                
            # Validate file format
            if not self._validate_file_format(filename):
                raise ValueError("Unsupported file format")
                
            # Load and store image
            self._load_image(filename)
            
        except Exception as e:
            print(f"Error in upload_action: {e}")
            self._handle_upload_error(e)
            
    def save_image(self) -> None:
        """
        Handle image saving operation.
        
        Processes:
        1. File save dialog
        2. Format selection
        3. Image saving
        4. Error handling
        
        Supports multiple image formats with appropriate quality settings.
        """
        try:
            if self.editor.edited_image is None:
                raise ValueError("No image to save")
                
            # Define file types for dialog
            filetypes = (
                ('JPEG files', '*.jpg'),
                ('PNG files', '*.png'),
                ('BMP files', '*.bmp'),
                ('All files', '*.*')
            )
            
            # Open save dialog
            filename = filedialog.asksaveasfilename(
                title='Save Image',
                defaultextension='.jpg',
                filetypes=filetypes
            )
            
            # Check if filename was provided
            if not filename:
                return
                
            # Save image
            self._save_image(filename)
            
            # Update current file
            self.current_file = filename
            
        except Exception as e:
            print(f"Error in save_action: {e}")
            self._handle_save_error(e)
            
    def _validate_file_format(self, filename: str) -> bool:
        """
        Validate if file has a supported format.
        
        Args:
            filename: Path to the file
            
        Returns:
            bool: True if format is supported, False otherwise
            
        Checks file extension against list of supported formats.
        """
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.supported_formats
    
    def _load_image(self, filename: str) -> None:
        """
        Load image from file and initialize editor buffers.
        
        Args:
            filename: Path to the image file
            
        Raises:
            ValueError: If image cannot be loaded
            
        Updates all image buffers in the editor.
        """
        # Load image
        image = cv2.imread(filename)
        if image is None:
            raise ValueError("Could not load image")
            
        # Update editor buffers
        self.editor.original_image = image
        self.editor.edited_image = image.copy()
        self.editor.filtered_image = image.copy()
        
        # Store filename
        self.current_file = filename
        
        # Display image
        self.editor.display_image(self.editor.edited_image)
        
    def _save_image(self, filename: str) -> None:
        """
        Save image to file with appropriate format settings.
        
        Args:
            filename: Path where to save the image
            
        Raises:
            ValueError: If image cannot be saved
            
        Handles different formats with appropriate quality settings.
        """
        # Get file extension
        ext = os.path.splitext(filename)[1].lower()
        
        # Prepare image for saving
        if ext == '.jpg' or ext == '.jpeg':
            # JPEG quality parameters
            params = [cv2.IMWRITE_JPEG_QUALITY, 95]
        elif ext == '.png':
            # PNG compression parameters
            params = [cv2.IMWRITE_PNG_COMPRESSION, 9]
        else:
            # Default parameters for other formats
            params = []
            
        # Save image
        success = cv2.imwrite(filename, self.editor.edited_image, params)
        if not success:
            raise ValueError("Failed to save image")
            
    def _handle_upload_error(self, error: Exception) -> None:
        """
        Handle errors during image upload.
        
        Args:
            error: The exception that occurred
            
        Implements appropriate error recovery and user feedback.
        """
        error_type = type(error).__name__
        if error_type == 'ValueError':
            print("Invalid image file or format")
        elif error_type == 'MemoryError':
            print("Image too large to load")
        else:
            print(f"Error loading image: {str(error)}")
            
    def _handle_save_error(self, error: Exception) -> None:
        """
        Handle errors during image save.
        
        Args:
            error: The exception that occurred
            
        Implements appropriate error recovery and user feedback.
        """
        error_type = type(error).__name__
        if error_type == 'ValueError':
            print("Error saving image")
        elif error_type == 'PermissionError':
            print("Permission denied when saving file")
        else:
            print(f"Error saving image: {str(error)}")
            
    def get_temp_filename(self) -> str:
        """
        Generate temporary filename for intermediate saves.
        
        Returns:
            str: Path to temporary file
            
        Used for:
        1. Automatic backups
        2. Undo/redo operations
        3. Recovery points
        """
        base_dir = self._get_temp_dir()
        return os.path.join(base_dir, f"temp_image_{id(self)}.jpg")
        
    def _get_temp_dir(self) -> str:
        """
        Get appropriate temporary directory based on platform.
        
        Returns:
            str: Path to temporary directory
            
        Handles different operating systems appropriately.
        """
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))
        
    def cleanup_temp_files(self) -> None:
        """
        Clean up temporary files created by the application.
        
        Called during:
        1. Application shutdown
        2. New file load
        3. Explicit cleanup request
        """
        try:
            temp_file = self.get_temp_filename()
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except Exception as e:
            print(f"Error cleaning up temporary files: {e}")
