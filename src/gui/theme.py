"""
Modern theme and styling for the Secure File Encryption Tool
"""

import tkinter as tk
from tkinter import ttk

class ModernTheme:
    """Modern color scheme and styling for the application"""
    
    # Color palette
    COLORS = {
        'primary': '#2563eb',        # Modern blue
        'primary_dark': '#1d4ed8',   # Darker blue for hover
        'secondary': '#10b981',      # Green for success
        'warning': '#f59e0b',        # Amber for warnings
        'danger': '#ef4444',         # Red for errors
        'background': '#f8fafc',     # Light gray background
        'surface': '#ffffff',        # White surface
        'text': '#1f2937',          # Dark gray text
        'text_secondary': '#6b7280', # Medium gray text
        'border': '#e5e7eb',        # Light border
        'accent': '#8b5cf6',        # Purple accent
    }
    
    # Typography
    FONTS = {
        'heading_large': ('Segoe UI', 18, 'bold'),
        'heading': ('Segoe UI', 14, 'bold'),
        'subheading': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'body_small': ('Segoe UI', 9),
        'monospace': ('Consolas', 10),
    }
    
    # Spacing
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
        'xxl': 48,
    }
    
    @classmethod
    def configure_styles(cls, root):
        """Configure modern ttk styles"""
        style = ttk.Style()
        
        # Configure modern button style
        style.configure('Modern.TButton',
                       background=cls.COLORS['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(cls.SPACING['md'], cls.SPACING['sm']))
        
        style.map('Modern.TButton',
                 background=[('active', cls.COLORS['primary_dark']),
                           ('pressed', cls.COLORS['primary_dark'])])
        
        # Success button style
        style.configure('Success.TButton',
                       background=cls.COLORS['secondary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(cls.SPACING['md'], cls.SPACING['sm']))
        
        style.map('Success.TButton',
                 background=[('active', '#059669'),
                           ('pressed', '#047857')])
        
        # Danger button style
        style.configure('Danger.TButton',
                       background=cls.COLORS['danger'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(cls.SPACING['md'], cls.SPACING['sm']))
        
        style.map('Danger.TButton',
                 background=[('active', '#dc2626'),
                           ('pressed', '#b91c1c')])
        
        # Modern frame style
        style.configure('Card.TFrame',
                       background=cls.COLORS['surface'],
                       relief='flat',
                       borderwidth=1)
        
        # Modern label styles
        style.configure('Heading.TLabel',
                       background=cls.COLORS['surface'],
                       foreground=cls.COLORS['text'],
                       font=cls.FONTS['heading'])
        
        style.configure('Subheading.TLabel',
                       background=cls.COLORS['surface'],
                       foreground=cls.COLORS['text'],
                       font=cls.FONTS['subheading'])
        
        style.configure('Body.TLabel',
                       background=cls.COLORS['surface'],
                       foreground=cls.COLORS['text_secondary'],
                       font=cls.FONTS['body'])
        
        # Success/Error labels
        style.configure('Success.TLabel',
                       background=cls.COLORS['surface'],
                       foreground=cls.COLORS['secondary'],
                       font=cls.FONTS['body'])
        
        style.configure('Error.TLabel',
                       background=cls.COLORS['surface'],
                       foreground=cls.COLORS['danger'],
                       font=cls.FONTS['body'])
        
        # Modern entry style
        style.configure('Modern.TEntry',
                       borderwidth=1,
                       relief='solid',
                       padding=cls.SPACING['sm'])
        
        # Progress bar style
        style.configure('Modern.Horizontal.TProgressbar',
                       background=cls.COLORS['primary'],
                       troughcolor=cls.COLORS['border'],
                       borderwidth=0,
                       lightcolor=cls.COLORS['primary'],
                       darkcolor=cls.COLORS['primary'])


class ModernWidgets:
    """Helper class for creating modern-styled widgets"""
    
    @staticmethod
    def create_card_frame(parent, **kwargs):
        """Create a modern card-style frame"""
        frame = ttk.Frame(parent, style='Card.TFrame', **kwargs)
        return frame
    
    @staticmethod
    def create_primary_button(parent, text, command=None, **kwargs):
        """Create a modern primary button"""
        button = ttk.Button(parent, text=text, command=command, 
                           style='Modern.TButton', **kwargs)
        return button
    
    @staticmethod
    def create_success_button(parent, text, command=None, **kwargs):
        """Create a modern success button"""
        button = ttk.Button(parent, text=text, command=command, 
                           style='Success.TButton', **kwargs)
        return button
    
    @staticmethod
    def create_danger_button(parent, text, command=None, **kwargs):
        """Create a modern danger button"""
        button = ttk.Button(parent, text=text, command=command, 
                           style='Danger.TButton', **kwargs)
        return button
    
    @staticmethod
    def create_heading_label(parent, text, **kwargs):
        """Create a heading label"""
        label = ttk.Label(parent, text=text, style='Heading.TLabel', **kwargs)
        return label
    
    @staticmethod
    def create_subheading_label(parent, text, **kwargs):
        """Create a subheading label"""
        label = ttk.Label(parent, text=text, style='Subheading.TLabel', **kwargs)
        return label
    
    @staticmethod
    def create_body_label(parent, text, **kwargs):
        """Create a body text label"""
        label = ttk.Label(parent, text=text, style='Body.TLabel', **kwargs)
        return label
    
    @staticmethod
    def create_modern_entry(parent, **kwargs):
        """Create a modern entry widget"""
        entry = ttk.Entry(parent, style='Modern.TEntry', **kwargs)
        return entry
