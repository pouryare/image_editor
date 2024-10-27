"""
Custom Type Definitions Module for Image Editor Application

This module defines custom types, type aliases, and type hints used throughout
the application. It provides:
1. Custom type definitions
2. Type aliases
3. Protocol classes
4. Type variables
5. Composite types
6. Generic types

Key Features:
- Type safety
- Code clarity
- Documentation
- Reusability
- Type validation
- IDE support

Dependencies:
- typing module
- numpy for array types
- Protocol for structural subtyping
- TypeVar for generic types

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import (
    TypeVar, 
    Protocol, 
    Union, 
    Tuple, 
    Dict, 
    List,
    Optional,
    Callable,
    TypedDict,
    NewType
)
from numpy.typing import NDArray
import numpy as np
from tkinter import Event

# Type variables for generic types
T = TypeVar('T')
ImageType = TypeVar('ImageType', bound=NDArray[np.uint8])

# Image-related types
class ImageArray(Protocol):
    """Protocol defining the interface for image arrays."""
    
    shape: Tuple[int, ...]
    dtype: np.dtype
    
    def __array__(self) -> NDArray[np.uint8]: ...

# Color types
RGBColor = Tuple[int, int, int]
BGRColor = Tuple[int, int, int]
ColorCode = Tuple[RGBColor, str]  # (RGB tuple, hex string)

# Coordinate types
Point = Tuple[int, int]
Rectangle = Tuple[int, int, int, int]  # x1, y1, x2, y2
Dimensions = Tuple[int, int]  # width, height

# Event handler types
EventCallback = Callable[[Event], None]
GenericCallback = Callable[[], None]

# Filter states
class FilterState(TypedDict):
    """Type definition for filter state dictionary."""
    
    negative: bool
    bw: bool
    stylisation: bool
    sketch: bool
    emboss: bool
    sepia: bool
    binary: bool
    erosion: bool
    dilation: bool

# Tool parameters
class DrawingParams(TypedDict):
    """Type definition for drawing parameters."""
    
    color: ColorCode
    thickness: int
    tool_type: str
    
class TextParams(TypedDict):
    """Type definition for text parameters."""
    
    text: str
    font: int
    scale: float
    color: ColorCode
    thickness: int
    
class BlurParams(TypedDict):
    """Type definition for blur parameters."""
    
    method: str
    kernel_size: int
    sigma: Optional[float]

# File operations
FilePath = NewType('FilePath', str)

class FileInfo(TypedDict):
    """Type definition for file information."""
    
    path: FilePath
    format: str
    size: int
    dimensions: Dimensions

# History management
class HistoryState(TypedDict):
    """Type definition for history state information."""
    
    image: ImageArray
    params: Dict[str, any]
    timestamp: float

# Canvas elements
CanvasItemId = NewType('CanvasItemId', int)

class CanvasObject(Protocol):
    """Protocol defining the interface for canvas objects."""
    
    id: CanvasItemId
    type: str
    coords: List[int]
    options: Dict[str, any]

# Error types
class ImageError(Exception):
    """Base exception class for image-related errors."""
    pass

class FileError(Exception):
    """Base exception class for file-related errors."""
    pass

class ToolError(Exception):
    """Base exception class for tool-related errors."""
    pass

# Composite types
ImageTransform = Callable[[ImageArray], ImageArray]
FilterFunction = Callable[[ImageArray, Dict[str, any]], ImageArray]

# Type aliases for common types
Size = Union[int, float]
PathLike = Union[str, FilePath]
ColorValue = Union[RGBColor, str]

# GUI-related types
class WidgetStyle(TypedDict):
    """Type definition for widget styles."""
    
    background: str
    foreground: str
    font: Tuple[str, int]
    padding: Union[int, Tuple[int, int]]

class WindowGeometry(TypedDict):
    """Type definition for window geometry."""
    
    width: int
    height: int
    x: int
    y: int

# Operation results
class OperationResult(TypedDict, total=False):
    """Type definition for operation results."""
    
    success: bool
    message: str
    data: Optional[Dict[str, any]]
    error: Optional[Exception]

# Validation types
class ValidationResult(TypedDict):
    """Type definition for validation results."""
    
    valid: bool
    errors: List[str]
    warnings: List[str]

# Type guards
def is_image_array(obj: any) -> bool:
    """
    Type guard to check if an object is a valid image array.
    
    Args:
        obj: Object to check
        
    Returns:
        bool: True if object is a valid image array
    """
    return (
        isinstance(obj, np.ndarray) and
        obj.dtype == np.uint8 and
        len(obj.shape) in (2, 3)
    )

def is_valid_color(color: any) -> bool:
    """
    Type guard to check if a value is a valid color.
    
    Args:
        color: Value to check
        
    Returns:
        bool: True if value is a valid color
    """
    if isinstance(color, tuple) and len(color) == 3:
        return all(isinstance(c, int) and 0 <= c <= 255 for c in color)
    if isinstance(color, str):
        return color.startswith('#') and len(color) in (4, 7)
    return False

def is_valid_dimensions(dims: any) -> bool:
    """
    Type guard to check if a value represents valid dimensions.
    
    Args:
        dims: Value to check
        
    Returns:
        bool: True if value represents valid dimensions
    """
    return (
        isinstance(dims, tuple) and
        len(dims) == 2 and
        all(isinstance(d, int) and d > 0 for d in dims)
    )

# Generic type constraints
def ensure_type(value: T, type_check: Callable[[T], bool], error_msg: str) -> T:
    """
    Ensure a value matches a type constraint.
    
    Args:
        value: Value to check
        type_check: Function to validate type
        error_msg: Error message if validation fails
        
    Returns:
        Original value if valid
        
    Raises:
        TypeError: If value fails type check
    """
    if not type_check(value):
        raise TypeError(error_msg)
    return value

# Export all types
__all__ = [
    'ImageArray',
    'RGBColor',
    'BGRColor',
    'ColorCode',
    'Point',
    'Rectangle',
    'Dimensions',
    'EventCallback',
    'GenericCallback',
    'FilterState',
    'DrawingParams',
    'TextParams',
    'BlurParams',
    'FilePath',
    'FileInfo',
    'HistoryState',
    'CanvasItemId',
    'CanvasObject',
    'ImageError',
    'FileError',
    'ToolError',
    'ImageTransform',
    'FilterFunction',
    'Size',
    'PathLike',
    'ColorValue',
    'WidgetStyle',
    'WindowGeometry',
    'OperationResult',
    'ValidationResult',
    'is_image_array',
    'is_valid_color',
    'is_valid_dimensions',
    'ensure_type'
]
