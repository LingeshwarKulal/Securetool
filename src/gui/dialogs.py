"""
Dialog windows for password input and progress display
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
from gui.theme import ModernTheme, ModernWidgets

class PasswordDialog:
    """Password input dialog with strength validation"""
    
    def __init__(self, parent, title="Enter Password"):
        self.parent = parent
        self.password = None
        self.dialog = None
        self.title = title
        
    def get_password(self):
        """Show dialog and return entered password"""
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
        
        # Password entry
        ttk.Label(main_frame, text="Password:").pack(anchor=tk.W)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, 
                                       show="*", width=40)
        self.password_entry.pack(fill=tk.X, pady=(5, 10))
        self.password_entry.bind('<KeyRelease>', self.check_password_strength)
        self.password_entry.focus()
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        show_cb = ttk.Checkbutton(main_frame, text="Show password", 
                                 variable=self.show_password_var,
                                 command=self.toggle_password_visibility)
        show_cb.pack(anchor=tk.W, pady=(0, 10))
        
        # Password strength indicator
        strength_frame = ttk.Frame(main_frame)
        strength_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(strength_frame, text="Password Strength:").pack(anchor=tk.W)
        self.strength_var = tk.StringVar(value="Very Weak")
        self.strength_label = ttk.Label(strength_frame, textvariable=self.strength_var)
        self.strength_label.pack(anchor=tk.W)
        
        # Strength bar
        self.strength_progress = ttk.Progressbar(strength_frame, length=300, maximum=100)
        self.strength_progress.pack(fill=tk.X, pady=(5, 0))
        
        # Password requirements
        req_frame = ttk.LabelFrame(main_frame, text="Password Requirements", padding="10")
        req_frame.pack(fill=tk.X, pady=(0, 20))
        
        requirements = [
            "At least 12 characters long",
            "Contains uppercase letters (A-Z)",
            "Contains lowercase letters (a-z)",
            "Contains numbers (0-9)",
            "Contains special characters (!@#$%^&*)"
        ]
        
        self.req_labels = []
        for req in requirements:
            label = ttk.Label(req_frame, text=f"✗ {req}", foreground="red")
            label.pack(anchor=tk.W)
            self.req_labels.append(label)
        
        # Confirm password
        ttk.Label(main_frame, text="Confirm Password:").pack(anchor=tk.W)
        self.confirm_var = tk.StringVar()
        self.confirm_entry = ttk.Entry(main_frame, textvariable=self.confirm_var, 
                                      show="*", width=40)
        self.confirm_entry.pack(fill=tk.X, pady=(5, 20))
        self.confirm_entry.bind('<KeyRelease>', self.check_password_match)
        
        # Password match indicator
        self.match_var = tk.StringVar(value="")
        self.match_label = ttk.Label(main_frame, textvariable=self.match_var)
        self.match_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.ok_button = ttk.Button(button_frame, text="OK", command=self.ok_clicked,
                                   state="disabled")
        self.ok_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.RIGHT)
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.ok_clicked())
        self.dialog.bind('<Escape>', lambda e: self.cancel_clicked())
        
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
                label.configure(text=label.cget("text").replace("✗", "✓"), foreground="green")
            else:
                text = label.cget("text")
                if "✓" in text:
                    label.configure(text=text.replace("✓", "✗"), foreground="red")
        
        # Calculate strength
        strength_score = sum(requirements_met)
        
        if strength_score == 0:
            strength_text = "Very Weak"
            strength_color = "red"
            progress_value = 0
        elif strength_score == 1:
            strength_text = "Weak"
            strength_color = "red"
            progress_value = 20
        elif strength_score == 2:
            strength_text = "Fair"
            strength_color = "orange"
            progress_value = 40
        elif strength_score == 3:
            strength_text = "Good"
            strength_color = "yellow"
            progress_value = 60
        elif strength_score == 4:
            strength_text = "Strong"
            strength_color = "lightgreen"
            progress_value = 80
        else:
            strength_text = "Very Strong"
            strength_color = "green"
            progress_value = 100
            
        self.strength_var.set(strength_text)
        self.strength_label.configure(foreground=strength_color)
        self.strength_progress.configure(value=progress_value)
        
        # Check if password meets minimum requirements for OK button
        self.check_can_proceed()
        
    def check_password_match(self, event=None):
        """Check if passwords match"""
        password = self.password_var.get()
        confirm = self.confirm_var.get()
        
        if not confirm:
            self.match_var.set("")
        elif password == confirm:
            self.match_var.set("✓ Passwords match")
            self.match_label.configure(foreground="green")
        else:
            self.match_var.set("✗ Passwords do not match")
            self.match_label.configure(foreground="red")
            
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


class ProgressDialog:
    """Progress dialog for long-running operations"""
    
    def __init__(self, parent, title="Operation in Progress"):
        self.parent = parent
        self.dialog = None
        self.title = title
        self.cancelled = False
        
    def show(self, operation_func, *args, **kwargs):
        """Show progress dialog and run operation"""
        self.create_dialog()
        
        # Start operation in thread
        import threading
        thread = threading.Thread(target=self._run_operation, 
                                 args=(operation_func, args, kwargs), daemon=True)
        thread.start()
        
        self.dialog.wait_window()
        return not self.cancelled
        
    def create_dialog(self):
        """Create the progress dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("400x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 100,
            self.parent.winfo_rooty() + 100
        ))
        
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status label
        self.status_var = tk.StringVar(value="Starting operation...")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.pack(pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var,
                                           maximum=100, length=300)
        self.progress_bar.pack(pady=(0, 20))
        
        # Cancel button
        self.cancel_button = ttk.Button(main_frame, text="Cancel", 
                                       command=self.cancel_operation)
        self.cancel_button.pack()
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel_operation)
        
    def update_progress(self, progress, status=""):
        """Update progress bar and status"""
        if self.dialog:
            self.dialog.after(0, lambda: self._update_ui(progress, status))
            
    def _update_ui(self, progress, status):
        """Update UI elements (called from main thread)"""
        self.progress_var.set(progress)
        if status:
            self.status_var.set(status)
            
    def cancel_operation(self):
        """Cancel the operation"""
        self.cancelled = True
        if self.dialog:
            self.dialog.destroy()
            
    def complete_operation(self, success=True):
        """Complete the operation"""
        if self.dialog:
            self.dialog.after(0, self.dialog.destroy)
            
    def _run_operation(self, operation_func, args, kwargs):
        """Run the operation in background thread"""
        try:
            result = operation_func(*args, **kwargs)
            self.complete_operation(True)
            return result
        except Exception as e:
            self.complete_operation(False)
            messagebox.showerror("Operation Failed", f"Operation failed:\n{str(e)}")


class SettingsDialog:
    """Settings configuration dialog"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.dialog = None
        
    def show(self):
        """Show settings dialog"""
        self.create_dialog()
        self.dialog.wait_window()
        
    def create_dialog(self):
        """Create the settings dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Settings")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Security tab
        security_frame = ttk.Frame(notebook, padding="10")
        notebook.add(security_frame, text="Security")
        
        # Default encryption settings
        ttk.Label(security_frame, text="Default Encryption Algorithm:").pack(anchor=tk.W)
        self.algorithm_var = tk.StringVar(value=self.config.get('encryption_algorithm', 'AES-256-GCM'))
        algorithm_combo = ttk.Combobox(security_frame, textvariable=self.algorithm_var,
                                      values=['AES-256-GCM', 'AES-256-CBC', 'Fernet'],
                                      state="readonly")
        algorithm_combo.pack(fill=tk.X, pady=(5, 15))
        
        # Key derivation iterations
        ttk.Label(security_frame, text="Key Derivation Iterations:").pack(anchor=tk.W)
        self.iterations_var = tk.StringVar(value=str(self.config.get('pbkdf2_iterations', 100000)))
        iterations_entry = ttk.Entry(security_frame, textvariable=self.iterations_var)
        iterations_entry.pack(fill=tk.X, pady=(5, 15))
        
        # Secure deletion passes
        ttk.Label(security_frame, text="Secure Deletion Passes:").pack(anchor=tk.W)
        self.deletion_passes_var = tk.StringVar(value=str(self.config.get('secure_deletion_passes', 3)))
        passes_spin = ttk.Spinbox(security_frame, from_=1, to=10, 
                                 textvariable=self.deletion_passes_var)
        passes_spin.pack(fill=tk.X, pady=(5, 15))
        
        # General tab
        general_frame = ttk.Frame(notebook, padding="10")
        notebook.add(general_frame, text="General")
        
        # Default output directory
        ttk.Label(general_frame, text="Default Output Directory:").pack(anchor=tk.W)
        output_frame = ttk.Frame(general_frame)
        output_frame.pack(fill=tk.X, pady=(5, 15))
        
        self.output_dir_var = tk.StringVar(value=self.config.get('default_output_dir', ''))
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(output_frame, text="Browse...", 
                  command=self.browse_output_dir).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Auto-clear selection after operation
        self.auto_clear_var = tk.BooleanVar(value=self.config.get('auto_clear_selection', True))
        ttk.Checkbutton(general_frame, text="Auto-clear selection after operation",
                       variable=self.auto_clear_var).pack(anchor=tk.W, pady=(0, 10))
        
        # Show progress notifications
        self.show_notifications_var = tk.BooleanVar(value=self.config.get('show_notifications', True))
        ttk.Checkbutton(general_frame, text="Show progress notifications",
                       variable=self.show_notifications_var).pack(anchor=tk.W, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Save", command=self.save_settings).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Reset to Defaults", 
                  command=self.reset_defaults).pack(side=tk.LEFT)
        
    def browse_output_dir(self):
        """Browse for default output directory"""
        from tkinter import filedialog
        directory = filedialog.askdirectory(title="Select Default Output Directory")
        if directory:
            self.output_dir_var.set(directory)
            
    def save_settings(self):
        """Save settings to configuration"""
        try:
            # Validate iterations
            iterations = int(self.iterations_var.get())
            if iterations < 10000:
                messagebox.showwarning("Invalid Setting", 
                                     "Key derivation iterations must be at least 10,000")
                return
                
            # Validate deletion passes
            passes = int(self.deletion_passes_var.get())
            if passes < 1 or passes > 10:
                messagebox.showwarning("Invalid Setting", 
                                     "Secure deletion passes must be between 1 and 10")
                return
                
            # Save all settings
            self.config.set('encryption_algorithm', self.algorithm_var.get())
            self.config.set('pbkdf2_iterations', iterations)
            self.config.set('secure_deletion_passes', passes)
            self.config.set('default_output_dir', self.output_dir_var.get())
            self.config.set('auto_clear_selection', self.auto_clear_var.get())
            self.config.set('show_notifications', self.show_notifications_var.get())
            
            self.config.save()
            messagebox.showinfo("Settings Saved", "Settings have been saved successfully.")
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
            
    def reset_defaults(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("Reset Settings", 
                              "Are you sure you want to reset all settings to defaults?"):
            self.algorithm_var.set('AES-256-GCM')
            self.iterations_var.set('100000')
            self.deletion_passes_var.set('3')
            self.output_dir_var.set('')
            self.auto_clear_var.set(True)
            self.show_notifications_var.set(True)
