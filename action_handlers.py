"""
Action Handlers Module for Image Editor Application

This module handles all action-related operations for the Image Editor application.
It manages:
1. Apply changes
2. Cancel operations
3. Revert to original
4. State management
5. Action history (if implemented)
6. Undo/Redo operations (if implemented)

Key Features:
- State tracking
- Change management
- History tracking
- Error recovery
- Action validation
- Operation logging

Dependencies:
- numpy for array operations
- typing for type hints
- cv2 (OpenCV) for image operations

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import Optional, List, Dict, TYPE_CHECKING
import numpy as np
import cv2

if TYPE_CHECKING:
    from image_editor import ImageEditor

class ActionHandlers:
    """
    Class containing all action-related functionality for the Image Editor.
    
    This class manages the application's action stack and handles
    applying, canceling, and reverting changes.
    """
    
    def __init__(self, editor: 'ImageEditor') -> None:
        """
        Initialize the ActionHandlers class.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        Initializes:
            - Reference to main editor
            - Action history
            - State tracking variables
        """
        self.editor = editor
        self.history: List[np.ndarray] = []
        self.history_position: int = -1
        self.max_history: int = 10  # Maximum number of states to store
        
    def apply_changes(self) -> None:
        """
        Apply current changes to the edited image.
        
        Process:
        1. Validate changes
        2. Update image buffers
        3. Update display
        4. Add to history
        5. Reset filter states
        """
        try:
            if self.editor.filtered_image is not None:
                # Create deep copy of filtered image
                self.editor.edited_image = self.editor.filtered_image.copy()
                
                # Update display
                self.editor.display_image(self.editor.edited_image)
                
                # Add to history
                self._add_to_history(self.editor.edited_image.copy())
                
                # Reset all filter states
                self._reset_filter_states()
                
        except Exception as e:
            print(f"Error applying changes: {e}")
            self._handle_action_error("apply")
            
    def cancel_changes(self) -> None:
        """
        Cancel current changes and revert to last saved state.
        
        Process:
        1. Reset filtered image
        2. Update display
        3. Reset tool states
        4. Clear temporary data
        """
        try:
            # Reset filtered image to edited image
            self.editor.filtered_image = self.editor.edited_image.copy()
            
            # Update display
            self.editor.display_image(self.editor.edited_image)
            
            # Reset tool states
            self._reset_tool_states()
            
        except Exception as e:
            print(f"Error canceling changes: {e}")
            self._handle_action_error("cancel")
            
    def revert_all(self) -> None:
        """
        Revert all changes and return to original image.
        
        Process:
        1. Reset to original image
        2. Clear history
        3. Reset all states
        4. Update display
        """
        try:
            if self.editor.original_image is not None:
                # Reset all image buffers
                self.editor.edited_image = self.editor.original_image.copy()
                self.editor.filtered_image = self.editor.original_image.copy()
                
                # Update display
                self.editor.display_image(self.editor.original_image)
                
                # Clear history
                self.clear_history()
                
                # Reset all states
                self._reset_all_states()
                
        except Exception as e:
            print(f"Error reverting changes: {e}")
            self._handle_action_error("revert")
            
    def _add_to_history(self, image: np.ndarray) -> None:
        """
        Add current state to history stack.
        
        Args:
            image: Current image state to store
            
        Manages history size and position.
        """
        # Remove any redo states
        if self.history_position < len(self.history) - 1:
            self.history = self.history[:self.history_position + 1]
            
        # Add new state
        self.history.append(image.copy())
        self.history_position += 1
        
        # Maintain maximum history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.history_position -= 1
            
    def _reset_filter_states(self) -> None:
        """
        Reset all filter states to default.
        
        Resets:
        1. Filter toggles
        2. Filter parameters
        3. Active filter tracking
        """
        for key in self.editor.active_filters:
            self.editor.active_filters[key] = False
            
    def _reset_tool_states(self) -> None:
        """
        Reset all tool states to default.
        
        Resets:
        1. Drawing tools
        2. Text tools
        3. Transform states
        4. Selection states
        """
        # Reset drawing
        self.editor.draw_ids = []
        
        # Reset crop
        self.editor.rectangle_id = 0
        self.editor.crop_start_x = 0
        self.editor.crop_start_y = 0
        self.editor.crop_end_x = 0
        self.editor.crop_end_y = 0
        
    def _reset_all_states(self) -> None:
        """
        Reset all application states to default.
        
        Resets:
        1. Filter states
        2. Tool states
        3. Transform states
        4. History
        """
        self._reset_filter_states()
        self._reset_tool_states()
        
        # Reset additional states
        self.editor.text_extracted = "Sample Text"
        self.editor.color_code = ((255, 0, 0), '#ff0000')
        
    def _handle_action_error(self, action_type: str) -> None:
        """
        Handle errors during action operations.
        
        Args:
            action_type: Type of action that failed
            
        Implements appropriate error recovery based on action type.
        """
        if action_type == "apply":
            # Revert to last known good state
            self.cancel_changes()
        elif action_type == "cancel":
            # Try to revert to original
            self.revert_all()
        elif action_type == "revert":
            print("Critical error: Unable to revert changes")
            
    def undo(self) -> None:
        """
        Undo last action if available.
        
        Process:
        1. Check history availability
        2. Restore previous state
        3. Update display
        4. Update history position
        """
        if self.history_position > 0:
            self.history_position -= 1
            self.editor.edited_image = self.history[self.history_position].copy()
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.editor.display_image(self.editor.edited_image)
            
    def redo(self) -> None:
        """
        Redo last undone action if available.
        
        Process:
        1. Check redo availability
        2. Restore next state
        3. Update display
        4. Update history position
        """
        if self.history_position < len(self.history) - 1:
            self.history_position += 1
            self.editor.edited_image = self.history[self.history_position].copy()
            self.editor.filtered_image = self.editor.edited_image.copy()
            self.editor.display_image(self.editor.edited_image)
            
    def clear_history(self) -> None:
        """
        Clear action history.
        
        Called when:
        1. Loading new image
        2. Reverting to original
        3. Explicit history clear request
        """
        self.history = []
        self.history_position = -1
        
    def get_history_info(self) -> Dict[str, int]:
        """
        Get information about current history state.
        
        Returns:
            Dictionary containing history information
            
        Information includes:
        - Current position
        - Total states
        - Available undo/redo steps
        """
        return {
            'position': self.history_position,
            'total_states': len(self.history),
            'can_undo': self.history_position > 0,
            'can_redo': self.history_position < len(self.history) - 1
        }
