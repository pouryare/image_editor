"""
Constants and Configuration Module for Image Editor Application

This module defines all constant values and configuration parameters used throughout
the application. It centralizes:
1. Default values
2. Configuration parameters
3. Color definitions
4. Size constraints
5. File settings
6. UI constants
7. Tool parameters

Key Features:
- Centralized configuration
- Type hints for all constants
- Grouped constants
- Documentation for each constant
- Easy modification
- Version tracking

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import Tuple, Dict, Final
from enum import Enum, auto

# Direct exports for commonly used constants
DEFAULT_COLOR: Final[Tuple[Tuple[int, int, int], str]] = ((255, 0, 0), '#ff0000')
WINDOW_SIZE: Final[Tuple[int, int]] = (1400, 1000)
MIN_WINDOW_SIZE: Final[Tuple[int, int]] = (1400, 1000)
CANVAS_DEFAULT_SIZE: Final[Tuple[int, int]] = (900, 700)
CANVAS_PADDING: Final[int] = 100

# Application Information
APP_NAME: Final[str] = "Image Editor Pro"
APP_VERSION: Final[str] = "1.0.0"
APP_AUTHOR: Final[str] = "Your Name"
APP_DESCRIPTION: Final[str] = "Professional Image Editing Application"

# Color Definitions
class Colors:
    """Color constants used throughout the application."""
    
    # Main theme colors
    PRIMARY: Final[str] = '#3498db'    # Blue
    SECONDARY: Final[str] = '#2ecc71'  # Green
    DANGER: Final[str] = '#e74c3c'     # Red
    WARNING: Final[str] = '#f1c40f'    # Yellow
    INFO: Final[str] = '#2c3e50'       # Dark Blue
    
    # Background colors
    BG_DARK: Final[str] = '#2c3e50'    # Dark background
    BG_LIGHT: Final[str] = '#34495e'   # Light background
    
    # Text colors
    TEXT_LIGHT: Final[str] = '#ffffff'  # White text
    TEXT_DARK: Final[str] = '#2c3e50'   # Dark text
    
    # Border colors
    BORDER: Final[str] = '#3498db'      # Border blue

# Font Settings
class Fonts:
    """Font configurations for the application."""
    
    TITLE: Final[Tuple[str, int, str]] = ('Helvetica', 16, 'bold')
    SUBTITLE: Final[Tuple[str, int]] = ('Helvetica', 11)
    BUTTON: Final[Tuple[str, int]] = ('Helvetica', 11)
    LABEL: Final[Tuple[str, int]] = ('Helvetica', 10)

# File Settings
class FileSettings:
    """File-related constants and settings."""
    
    SUPPORTED_FORMATS: Final[Tuple[str, ...]] = (
        '.jpg', '.jpeg', '.png', '.bmp', '.gif'
    )
    
    DEFAULT_SAVE_FORMAT: Final[str] = '.jpg'
    
    JPEG_QUALITY: Final[int] = 95
    PNG_COMPRESSION: Final[int] = 9
    
    MAX_FILE_SIZE: Final[int] = 50 * 1024 * 1024  # 50MB

# Tool Parameters
class ToolParams:
    """Parameters for various tools and operations."""
    
    # Drawing parameters
    DRAW_LINE_WIDTH: Final[int] = 2
    DRAW_LINE_TYPE: Final[int] = 8
    
    # Text parameters
    DEFAULT_FONT: Final[int] = 0  # cv2.FONT_HERSHEY_SIMPLEX
    DEFAULT_FONT_SCALE: Final[float] = 2.0
    DEFAULT_TEXT_THICKNESS: Final[int] = 5
    
    # Blur parameters
    MAX_BLUR_SIZE: Final[int] = 256
    DEFAULT_BLUR_SIZE: Final[int] = 0
    
    # Brightness/Saturation parameters
    BRIGHTNESS_RANGE: Final[Tuple[float, float]] = (0.0, 2.0)
    BRIGHTNESS_DEFAULT: Final[float] = 1.0
    SATURATION_RANGE: Final[Tuple[float, float]] = (-200.0, 200.0)
    SATURATION_DEFAULT: Final[float] = 0.0

# UI States
class UIState(Enum):
    """Enumeration of possible UI states."""
    
    IDLE = auto()
    DRAWING = auto()
    CROPPING = auto()
    ADDING_TEXT = auto()
    APPLYING_FILTER = auto()
    ADJUSTING = auto()
    TRANSFORMING = auto()

# Filter States
class FilterStates:
    """Default states for various filters."""
    
    DEFAULT_STATES: Final[Dict[str, bool]] = {
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

# History Settings
class HistorySettings:
    """Constants for history management."""
    
    MAX_HISTORY_STATES: Final[int] = 10
    INITIAL_POSITION: Final[int] = -1

# Error Messages
class ErrorMessages:
    """Standard error messages used in the application."""
    
    FILE_NOT_FOUND: Final[str] = "Could not find the specified file"
    INVALID_FORMAT: Final[str] = "Unsupported file format"
    LOAD_ERROR: Final[str] = "Error loading image"
    SAVE_ERROR: Final[str] = "Error saving image"
    MEMORY_ERROR: Final[str] = "Not enough memory to process image"
    PERMISSION_ERROR: Final[str] = "Permission denied when accessing file"

# Style Configurations
class StyleConfig:
    """Style configurations for widgets."""
    
    BUTTON_STYLES: Final[Dict[str, Dict[str, any]]] = {
        'Main.TButton': {
            'padding': 12,
            'font': ('Helvetica', 11),
            'background': '#3498db',
            'foreground': '#ffffff'
        },
        'Secondary.TButton': {
            'padding': 10,
            'font': ('Helvetica', 10),
            'background': '#2ecc71'
        },
        'Filter.TButton': {
            'padding': 10,
            'font': ('Helvetica', 10),
            'background': '#27ae60'
        }
    }
    
    LABEL_STYLES: Final[Dict[str, Dict[str, any]]] = {
        'Custom.TLabel': {
            'font': ('Helvetica', 11),
            'foreground': '#ffffff',
            'background': '#2c3e50'
        }
    }
    
    FRAME_STYLES: Final[Dict[str, Dict[str, any]]] = {
        'Custom.TFrame': {
            'background': '#2c3e50'
        }
    }

# Version Information
VERSION_INFO: Final[Dict[str, str]] = {
    'major': '1',
    'minor': '0',
    'patch': '0',
    'release': 'stable',
    'build': '2024.1',
    'full': '1.0.0-stable'
}

# Export all constants at module level for easy access
__all__ = [
    'DEFAULT_COLOR',
    'WINDOW_SIZE',
    'MIN_WINDOW_SIZE',
    'CANVAS_DEFAULT_SIZE',
    'CANVAS_PADDING',
    'APP_NAME',
    'APP_VERSION',
    'APP_AUTHOR',
    'APP_DESCRIPTION',
    'Colors',
    'Fonts',
    'FileSettings',
    'ToolParams',
    'UIState',
    'FilterStates',
    'HistorySettings',
    'ErrorMessages',
    'StyleConfig',
    'VERSION_INFO'
]