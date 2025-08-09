"""
Modern password dialog with enhanced UI/UX
"""

import tkinter as tk
from tkinter import ttk
import re
from gui.theme import ModernTheme, ModernWidgets

class ModernPasswordDialog:
    """Modern password input dialog with strength validation"""
    
    def __init__(self, parent, title="Enter Password"):
        self.parent = parent
        self.title = title
        self.password = None
        self.dialog = None
        
        # Variables
        self.password_var = None
        self.confirm_var = None
        self.show_password_var = None
        self.strength_var = None
        self.match_var = None
        
        # UI elements
        self.password_entry = None
        self.confirm_entry = None
        self.strength_label = None
        self.strength_progress = None
        self.match_label = None
        self.ok_button = None
        self.req_labels = []
        
    def get_password(self):
        """Show dialog and return password"""
        self.create_dialog()
        self.dialog.wait_window()
        return self.password
        
    def create_dialog(self):
        """Create the modern password dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("550x700")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.configure(bg=ModernTheme.COLORS['background'])
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        # Main container
        main_container = tk.Frame(self.dialog, bg=ModernTheme.COLORS['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.SPACING['lg'], 
                           pady=ModernTheme.SPACING['lg'])
        
        # Header card
        header_card = ModernWidgets.create_card_frame(main_container, 
                                                     padding=ModernTheme.SPACING['xl'])
        header_card.pack(fill=tk.X, pady=(0, ModernTheme.SPACING['lg']))
        
        # Title with icon
        title_frame = tk.Frame(header_card, bg=ModernTheme.COLORS['surface'])
        title_frame.pack(fill=tk.X)
        
        title_icon = ModernWidgets.create_heading_label(title_frame, "🔐")
        title_icon.pack(side=tk.LEFT, padx=(0, ModernTheme.SPACING['sm']))
        
        title_label = ModernWidgets.create_heading_label(title_frame, self.title)
        title_label.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle_label = ModernWidgets.create_body_label(
            header_card, 
            "Enter a strong password to protect your files"
        )
        subtitle_label.pack(anchor=tk.W, pady=(ModernTheme.SPACING['sm'], 0))
        
        # Password input card
        input_card = ModernWidgets.create_card_frame(main_container, 
                                                    padding=ModernTheme.SPACING['lg'])
        input_card.pack(fill=tk.X, pady=(0, ModernTheme.SPACING['md']))
        
        # Password entry
        password_label = ModernWidgets.create_subheading_label(input_card, "Password")
        password_label.pack(anchor=tk.W, pady=(0, ModernTheme.SPACING['sm']))
        
        self.password_var = tk.StringVar()
        self.password_entry = ModernWidgets.create_modern_entry(
            input_card, textvariable=self.password_var, show="*", width=40
        )
        self.password_entry.pack(fill=tk.X, pady=(0, ModernTheme.SPACING['sm']))
        self.password_entry.bind('<KeyRelease>', self.check_password_strength)
        self.password_entry.focus()
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        show_checkbox = ttk.Checkbutton(input_card, text="Show password", 
                                       variable=self.show_password_var,
                                       command=self.toggle_password_visibility)
        show_checkbox.pack(anchor=tk.W, pady=(0, ModernTheme.SPACING['lg']))
        
        # Password strength card
        strength_card = ModernWidgets.create_card_frame(main_container, 
                                                       padding=ModernTheme.SPACING['lg'])
        strength_card.pack(fill=tk.X, pady=(0, ModernTheme.SPACING['md']))
        
        # Strength header
        strength_header = ModernWidgets.create_subheading_label(strength_card, "Password Strength")
        strength_header.pack(anchor=tk.W, pady=(0, ModernTheme.SPACING['sm']))
        
        # Strength indicator
        self.strength_var = tk.StringVar(value="Enter password...")
        self.strength_label = ModernWidgets.create_body_label(strength_card, "")
        self.strength_label.configure(textvariable=self.strength_var)
        self.strength_label.pack(anchor=tk.W, pady=(0, ModernTheme.SPACING['sm']))
        
        # Strength progress bar
        self.strength_progress = ttk.Progressbar(strength_card, 
                                               style='Modern.Horizontal.TProgressbar',
                                               maximum=100)
        self.strength_progress.pack(fill=tk.X, pady=(0, ModernTheme.SPACING['lg']))
        
        # Requirements card
        req_card = ModernWidgets.create_card_frame(main_container, 
                                                  padding=ModernTheme.SPACING['lg'])
        req_card.pack(fill=tk.X, pady=(0, ModernTheme.SPACING['md']))
        
        # Requirements header
        req_header = ModernWidgets.create_subheading_label(req_card, "Password Requirements")
        req_header.pack(anchor=tk.W, pady=(0, ModernTheme.SPACING['sm']))
        
        # Requirements list
        requirements = [
            "At least 12 characters long",
            "Contains uppercase letters (A-Z)",
            "Contains lowercase letters (a-z)", 
            "Contains numbers (0-9)",
            "Contains special characters (!@#$%^&*)"
        ]
        
        self.req_labels = []
        for req in requirements:
            req_frame = tk.Frame(req_card, bg=ModernTheme.COLORS['surface'])
            req_frame.pack(fill=tk.X, pady=ModernTheme.SPACING['xs'])
            
            # Status icon
            icon_label = tk.Label(req_frame, text="✗", 
                                fg=ModernTheme.COLORS['danger'],
                                bg=ModernTheme.COLORS['surface'],
                                font=ModernTheme.FONTS['body'])
            icon_label.pack(side=tk.LEFT, padx=(0, ModernTheme.SPACING['sm']))
            
            # Requirement text
            req_label = tk.Label(req_frame, text=req,
                               fg=ModernTheme.COLORS['text_secondary'],
                               bg=ModernTheme.COLORS['surface'],
                               font=ModernTheme.FONTS['body'])
            req_label.pack(side=tk.LEFT)
            
            self.req_labels.append(icon_label)
        
        # Confirm password card
        confirm_card = ModernWidgets.create_card_frame(main_container, 
                                                      padding=ModernTheme.SPACING['lg'])
        confirm_card.pack(fill=tk.X, pady=(0, ModernTheme.SPACING['md']))
        
        # Confirm password entry
        confirm_label = ModernWidgets.create_subheading_label(confirm_card, "Confirm Password")
        confirm_label.pack(anchor=tk.W, pady=(0, ModernTheme.SPACING['sm']))
        
        self.confirm_var = tk.StringVar()
        self.confirm_entry = ModernWidgets.create_modern_entry(
            confirm_card, textvariable=self.confirm_var, show="*", width=40
        )
        self.confirm_entry.pack(fill=tk.X, pady=(0, ModernTheme.SPACING['sm']))
        self.confirm_entry.bind('<KeyRelease>', self.check_password_match)
        
        # Password match indicator
        self.match_var = tk.StringVar(value="")
        self.match_label = ModernWidgets.create_body_label(confirm_card, "")
        self.match_label.configure(textvariable=self.match_var)
        self.match_label.pack(anchor=tk.W)
        
        # Button card
        button_card = ModernWidgets.create_card_frame(main_container, 
                                                     padding=ModernTheme.SPACING['lg'])
        button_card.pack(fill=tk.X)
        
        # Buttons
        button_frame = tk.Frame(button_card, bg=ModernTheme.COLORS['surface'])
        button_frame.pack(fill=tk.X)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked)
        cancel_btn.pack(side=tk.RIGHT, padx=(ModernTheme.SPACING['sm'], 0))
        
        self.ok_button = ModernWidgets.create_success_button(
            button_frame, "OK", self.ok_clicked
        )
        self.ok_button.pack(side=tk.RIGHT)
        self.ok_button.configure(state="disabled")
        
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.configure(show="")
            self.confirm_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
            self.confirm_entry.configure(show="*")
            
    def check_password_strength(self, event=None):
        """Check and display password strength"""
        password = self.password_var.get()
        
        # Check requirements
        requirements_met = [
            len(password) >= 12,
            bool(re.search(r'[A-Z]', password)),
            bool(re.search(r'[a-z]', password)),
            bool(re.search(r'[0-9]', password)),
            bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        ]
        
        # Update requirement labels
        for i, (req_met, label) in enumerate(zip(requirements_met, self.req_labels)):
            if req_met:
                label.configure(text="✓", foreground=ModernTheme.COLORS['secondary'])
            else:
                label.configure(text="✗", foreground=ModernTheme.COLORS['danger'])
        
        # Calculate strength
        if not password:
            strength_text = "Enter password..."
            strength_value = 0
            color = ModernTheme.COLORS['text_secondary']
        else:
            score = sum(requirements_met)
            if score <= 2:
                strength_text = "Weak"
                strength_value = 25
                color = ModernTheme.COLORS['danger']
            elif score == 3:
                strength_text = "Fair"
                strength_value = 50
                color = ModernTheme.COLORS['warning']
            elif score == 4:
                strength_text = "Good"
                strength_value = 75
                color = ModernTheme.COLORS['primary']
            else:
                strength_text = "Very Strong"
                strength_value = 100
                color = ModernTheme.COLORS['secondary']
        
        self.strength_var.set(strength_text)
        self.strength_label.configure(foreground=color)
        self.strength_progress['value'] = strength_value
        
        self.check_can_proceed()
        
    def check_password_match(self, event=None):
        """Check if passwords match"""
        password = self.password_var.get()
        confirm = self.confirm_var.get()
        
        if not confirm:
            self.match_var.set("")
        elif password == confirm:
            self.match_var.set("✓ Passwords match")
            self.match_label.configure(foreground=ModernTheme.COLORS['secondary'])
        else:
            self.match_var.set("✗ Passwords do not match")
            self.match_label.configure(foreground=ModernTheme.COLORS['danger'])
        
        self.check_can_proceed()
        
    def check_can_proceed(self):
        """Check if user can proceed (enable/disable OK button)"""
        password = self.password_var.get()
        confirm = self.confirm_var.get()
        
        # Minimum requirements for proceeding
        requirements_met = [
            len(password) >= 12,
            bool(re.search(r'[A-Z]', password)),
            bool(re.search(r'[a-z]', password)),
            bool(re.search(r'[0-9]', password)),
            bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        ]
        
        can_proceed = (
            all(requirements_met) and  # All requirements must be met
            password == confirm and
            len(password) > 0
        )
        
        self.ok_button.configure(state="normal" if can_proceed else "disabled")
        
    def ok_clicked(self):
        """Handle OK button click"""
        self.password = self.password_var.get()
        self.dialog.destroy()
            
    def cancel_clicked(self):
        """Handle Cancel button click"""
        self.password = None
        self.dialog.destroy()
