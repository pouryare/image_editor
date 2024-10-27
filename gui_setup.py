"""
GUI Setup Module for Image Editor Application

This module handles the graphical user interface setup for the Image Editor application.
It contains the GUISetup class which is responsible for:
1. Setting up and configuring all GUI styles
2. Creating the main window layout
3. Setting up the header, main menu, and footer
4. Configuring widget styles and themes

The module uses ttk for themed widgets and implements a modern, dark-themed interface
with custom styles for buttons, frames, and labels.

Dependencies:
- tkinter and ttk for GUI components
- tkinter.font for custom font configurations
- PhotoImage for logo handling

Author: Pouryare
Date: October 2024
Version: 1.0
"""

from typing import Any, TYPE_CHECKING
from tkinter import ttk, PhotoImage, Canvas, RIDGE
from tkinter.font import Font

if TYPE_CHECKING:
    from image_editor import ImageEditor

class GUISetup:
    """
    Class containing all GUI setup methods for the Image Editor application.
    
    This class uses static methods to configure and create the GUI elements,
    allowing for better organization and separation of concerns.
    """
    
    @staticmethod
    def setup_styles(editor: 'ImageEditor') -> None:
        """
        Configure and set up all GUI styles for the application.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        This method sets up:
        1. Main window style
        2. Custom button styles
        3. Label styles
        4. Frame styles
        5. Custom fonts and colors
        """
        # Configure main window style
        editor.master.configure(bg='#2c3e50')
        
        # Create and configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main button style configuration
        style.configure(
            'Main.TButton',
            padding=12,
            font=('Helvetica', 11),
            background='#3498db',
            foreground='#ffffff'
        )
        
        # Secondary button style
        style.configure(
            'Secondary.TButton',
            padding=10,
            font=('Helvetica', 10),
            background='#2ecc71'
        )
        
        # Filter button style
        style.configure(
            'Filter.TButton',
            padding=10,
            font=('Helvetica', 10),
            background='#27ae60'
        )
        
        # Label style configuration
        style.configure(
            'Custom.TLabel',
            font=('Helvetica', 11),
            foreground='#ffffff',
            background='#2c3e50'
        )
        
        # Frame style configuration
        style.configure(
            'Custom.TFrame',
            background='#2c3e50'
        )
        
        # Apply button style
        style.configure(
            'Apply.TButton',
            padding=12,
            font=('Helvetica', 11, 'bold'),
            background='#27ae60',
            foreground='#ffffff'
        )
        
        # Cancel button style
        style.configure(
            'Cancel.TButton',
            padding=12,
            font=('Helvetica', 11),
            background='#e74c3c',
            foreground='#ffffff'
        )

    @staticmethod
    def setup_gui(editor: 'ImageEditor') -> None:
        """
        Set up the main GUI layout and components.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        This method:
        1. Configures the main window
        2. Creates the main container
        3. Sets up the header, main menu, and footer
        """
        # Configure main window
        editor.master.geometry('1400x1000+50+10')
        editor.master.minsize(1400, 1000)
        editor.master.title('Image Editor Pro')
        editor.master.configure(bg='#2c3e50')
        editor.master.resizable(True, True)
        
        # Create main container
        editor.main_container = ttk.Frame(
            editor.master,
            style='Custom.TFrame'
        )
        editor.main_container.pack(
            fill='both',
            expand=True,
            padx=20,
            pady=20
        )
        
        # Set up main components
        GUISetup.create_header(editor)
        GUISetup.create_main_menu(editor)
        GUISetup.create_footer(editor)

    @staticmethod
    def create_header(editor: 'ImageEditor') -> None:
        """
        Create and set up the application header.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        Creates:
        1. Logo display
        2. Application title
        3. Subtitle/description
        """
        # Create header frame
        editor.frame_header = ttk.Frame(
            editor.main_container,
            style='Custom.TFrame'
        )
        editor.frame_header.pack(fill='x', pady=(0, 20))
        
        # Configure grid weights
        editor.frame_header.grid_columnconfigure(1, weight=1)
        
        # Add logo
        try:
            logo_path = editor.get_logo_path()
            editor.logo = PhotoImage(file=logo_path).subsample(3, 3)
            logo_label = ttk.Label(
                editor.frame_header,
                image=editor.logo,
                style='Custom.TLabel'
            )
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo_label = ttk.Label(
                editor.frame_header,
                text="📷",
                font=('Helvetica', 24),
                style='Custom.TLabel'
            )
        logo_label.grid(row=0, column=0, rowspan=2, padx=(0, 20))
        
        # Create title with custom font
        title_font = Font(family="Helvetica", size=16, weight="bold")
        title = ttk.Label(
            editor.frame_header,
            text='Advanced Image Editor',
            font=title_font,
            style='Custom.TLabel'
        )
        title.grid(row=0, column=1, sticky='w')
        
        # Add subtitle
        subtitle = ttk.Label(
            editor.frame_header,
            text='Edit, enhance, and transform your images with professional tools',
            style='Custom.TLabel'
        )
        subtitle.grid(row=1, column=1, sticky='w')

    @staticmethod
    def create_main_menu(editor: 'ImageEditor') -> None:
        """
        Create and set up the main menu area.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        Creates:
        1. Left sidebar with control buttons
        2. Main canvas area
        3. Right sidebar for tool options
        """
        # Create main content area
        editor.content_frame = ttk.Frame(
            editor.main_container,
            style='Custom.TFrame'
        )
        editor.content_frame.pack(fill='both', expand=True)
        
        # Configure grid weights
        editor.content_frame.grid_columnconfigure(1, weight=3)
        editor.content_frame.grid_columnconfigure(2, weight=1)
        editor.content_frame.grid_rowconfigure(0, weight=1)
        
        # Create left sidebar
        editor.frame_menu = ttk.Frame(
            editor.content_frame,
            style='Custom.TFrame',
            width=180
        )
        editor.frame_menu.grid(row=0, column=0, sticky='ns', padx=(0, 20))
        editor.frame_menu.pack_propagate(False)
        editor.frame_menu.config(relief=RIDGE, padding=(20, 15))
        
        # Add menu buttons
        menu_buttons = [
            ("📂 Upload", editor.upload_action),
            ("✂️ Crop", editor.crop_action),
            ("📝 Text", editor.text_action),
            ("🎨 Draw", editor.draw_action),
            ("🎭 Filters", editor.filter_action),
            ("🌫️ Blur", editor.blur_action),
            ("⚖️ Adjust", editor.adjust_action),
            ("🔄 Rotate", editor.rotate_action),
            ("↔️ Flip", editor.flip_action),
            ("💾 Save", editor.save_action)
        ]
        
        for idx, (text, command) in enumerate(menu_buttons):
            btn = ttk.Button(
                editor.frame_menu,
                text=text,
                command=command,
                style='Main.TButton'
            )
            btn.grid(row=idx, column=0, padx=5, pady=5, sticky='ew')
        
        # Create canvas area
        editor.canvas_frame = ttk.Frame(
            editor.content_frame,
            style='Custom.TFrame'
        )
        editor.canvas_frame.grid(row=0, column=1, sticky='nsew')
        
        # Create canvas with dark background
        editor.canvas = Canvas(
            editor.canvas_frame,
            bg="#34495e",
            width=900,
            height=700
        )
        editor.canvas.pack(padx=10, pady=10, expand=True, fill='both')

    @staticmethod
    def create_footer(editor: 'ImageEditor') -> None:
        """
        Create and set up the application footer.
        
        Args:
            editor: Reference to the main ImageEditor instance
            
        Creates:
        1. Footer container
        2. Action buttons (Apply, Cancel, Revert)
        """
        # Create footer container
        editor.footer_container = ttk.Frame(
            editor.main_container,
            style='Custom.TFrame'
        )
        editor.footer_container.pack(
            fill='x',
            side='bottom',
            pady=(0, 30)
        )
        
        # Create button container
        editor.apply_and_cancel = ttk.Frame(
            editor.footer_container,
            style='Custom.TFrame'
        )
        editor.apply_and_cancel.pack()
        
        # Add footer buttons
        footer_buttons = [
            ("✓ Apply Changes", editor.apply_action, 'Apply.TButton'),
            ("✗ Cancel", editor.cancel_action, 'Cancel.TButton'),
            ("↺ Revert All", editor.revert_action, 'Main.TButton')
        ]
        
        for idx, (text, command, style) in enumerate(footer_buttons):
            btn = ttk.Button(
                editor.apply_and_cancel,
                text=text,
                command=command,
                style=style,
                width=20
            )
            btn.grid(row=0, column=idx, padx=15, pady=10)