"""
Main GUI Window for Secure File Encryption Tool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path

from core.encryption import EncryptionEngine
from core.file_manager import FileManager
from gui.dialogs import ProgressDialog
from gui.modern_dialogs import ModernPasswordDialog
from gui.theme import ModernTheme, ModernWidgets
from utils.config import Config

class MainWindow:
    """Main application window"""
    
    def __init__(self, root):
        self.root = root
        self.encryption_engine = EncryptionEngine()
        self.file_manager = FileManager()
        self.config = Config()
        
        # Selected files/folders
        self.selected_items = []
        
        # Apply modern theme
        self.apply_modern_theme()
        
        # Setup GUI
        self.setup_ui()
        self.setup_menu()
        
    def apply_modern_theme(self):
        """Apply modern theme to the application"""
        # Configure root window
        self.root.configure(bg=ModernTheme.COLORS['background'])
        self.root.title("🔒 Secure File Encryption Tool - Zplus Cyber Secure Technologies")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Center the window
        self.center_window()
        
        # Configure modern styles
        ModernTheme.configure_styles(self.root)
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """Setup the modern user interface"""
        # Main container with background
        main_container = tk.Frame(self.root, bg=ModernTheme.COLORS['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)
        
        # Header section
        header_frame = tk.Frame(main_container, bg='white', relief='solid', bd=1, padx=32, pady=32)
        header_frame.pack(fill=tk.X, pady=(0, 24))
        
        # App icon and title
        title_frame = tk.Frame(header_frame, bg=ModernTheme.COLORS['surface'])
        title_frame.pack(fill=tk.X)
        
        # Title with icon
        title_label = tk.Label(title_frame, text="🔒 Secure File Encryption Tool",
                              font=('Segoe UI', 18, 'bold'), bg='white', fg='#1f2937')
        title_label.pack(side=tk.LEFT)
        
        # Company name
        company_label = tk.Label(title_frame, text="Zplus Cyber Secure Technologies Pvt Ltd",
                                font=('Segoe UI', 12, 'bold'), bg='white', fg='#2563eb')
        company_label.pack(side=tk.LEFT, padx=(16, 0))
        
        # Version badge
        version_label = tk.Label(title_frame, text="v1.0", 
                                font=('Segoe UI', 9), bg='white', fg='#6b7280')
        version_label.pack(side=tk.RIGHT, padx=(8, 0))
        
        # Subtitle
        subtitle_label = tk.Label(header_frame, text="Secure your files with military-grade AES-256 encryption",
                                 font=('Segoe UI', 10), bg='white', fg='#6b7280')
        subtitle_label.pack(anchor=tk.W, pady=(8, 0))
        
        # File selection section
        selection_card = tk.Frame(main_container, bg='white', relief='solid', bd=1, padx=24, pady=24)
        selection_card.pack(fill=tk.BOTH, expand=True, pady=(0, 16))
        
        # Section header
        selection_header = tk.Label(selection_card, text="📁 File Selection",
                                   font=('Segoe UI', 12, 'bold'), bg='white', fg='#1f2937')
        selection_header.pack(anchor=tk.W, pady=(0, 16))
        
        # Button row
        button_row = tk.Frame(selection_card, bg='white')
        button_row.pack(fill=tk.X, pady=(0, 16))
        
        # Modern buttons with improved styling
        browse_files_btn = ttk.Button(button_row, text="📄 Browse Files", command=self.browse_files)
        browse_files_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        browse_folder_btn = ttk.Button(button_row, text="📂 Browse Folder", command=self.browse_folder)
        browse_folder_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        clear_btn = ttk.Button(button_row, text="🗑️ Clear Selection", command=self.clear_selection)
        clear_btn.pack(side=tk.LEFT)
        
        # File list with modern styling
        list_frame = tk.Frame(selection_card, bg='white')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # List header
        list_header = tk.Label(list_frame, text="Selected files and folders:",
                              font=('Segoe UI', 10), bg='white', fg='#6b7280')
        list_header.pack(anchor=tk.W, pady=(0, 8))
        
        # Listbox with scrollbar
        listbox_frame = tk.Frame(list_frame, bg='#e5e7eb', relief=tk.SOLID, bd=1)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.files_listbox = tk.Listbox(listbox_frame, 
                                       bg='white',
                                       fg='#1f2937',
                                       selectbackground='#2563eb',
                                       selectforeground='white',
                                       font=('Segoe UI', 10),
                                       borderwidth=0,
                                       highlightthickness=0,
                                       activestyle='none')
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,1), pady=1)
        
        self.files_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.files_listbox.yview)
        
        # Operations section
        operations_card = tk.Frame(main_container, bg='white', relief='solid', bd=1, padx=24, pady=24)
        operations_card.pack(fill=tk.X, pady=(0, 16))
        
        # Section header
        operations_header = tk.Label(operations_card, text="⚡ Operations",
                                    font=('Segoe UI', 12, 'bold'), bg='white', fg='#1f2937')
        operations_header.pack(anchor=tk.W, pady=(0, 16))
        
        # Operation buttons with basic tkinter buttons for guaranteed visibility
        ops_button_frame = tk.Frame(operations_card, bg='yellow', relief='solid', bd=3, height=100)
        ops_button_frame.pack(fill=tk.X, pady=(10, 24), padx=10)
        ops_button_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Add a label to confirm this section is visible
        button_label = tk.Label(ops_button_frame, text="BUTTONS AREA - TESTING:", 
                               font=('Arial', 14, 'bold'), bg='yellow', fg='black')
        button_label.place(x=10, y=5)
        
        # Operation buttons - using basic tk.Button with explicit colors
        self.encrypt_btn = tk.Button(ops_button_frame, text="🔒 ENCRYPT FILES", 
                                   command=self.encrypt_files, 
                                   font=('Arial', 12, 'bold'),
                                   bg='green', fg='white',
                                   width=20, height=2,
                                   relief='raised', bd=3)
        self.encrypt_btn.place(x=10, y=40)
        
        self.decrypt_btn = tk.Button(ops_button_frame, text="🔓 DECRYPT FILES", 
                                   command=self.decrypt_files,
                                   font=('Arial', 12, 'bold'),
                                   bg='red', fg='white',
                                   width=20, height=2,
                                   relief='raised', bd=3)
        self.decrypt_btn.place(x=300, y=40)
        
        # Progress section
        progress_frame = tk.Frame(operations_card, bg='white')
        progress_frame.pack(fill=tk.X)
        
        # Progress bar with modern styling
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                           variable=self.progress_var,
                                           maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 8))
        
        # Status with icon
        status_frame = tk.Frame(progress_frame, bg='white')
        status_frame.pack(fill=tk.X)
        
        status_icon = tk.Label(status_frame, text="✅", bg='white')
        status_icon.pack(side=tk.LEFT, padx=(0, 4))
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(status_frame, text="", font=('Segoe UI', 10), 
                                   bg='white', fg='#6b7280')
        self.status_label.configure(textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT)
        
    def setup_menu(self):
        """Setup application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Browse Files...", command=self.browse_files)
        file_menu.add_command(label="Browse Folder...", command=self.browse_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Settings...", command=self.show_settings)
        tools_menu.add_command(label="Secure Delete...", command=self.secure_delete)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        
    def browse_files(self):
        """Browse and select files"""
        files = filedialog.askopenfilenames(
            title="Select Files to Encrypt/Decrypt",
            filetypes=[
                ("All Files", "*.*"),
                ("Encrypted Files", "*.enc"),
                ("Text Files", "*.txt"),
                ("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp"),
                ("Document Files", "*.pdf;*.doc;*.docx;*.xls;*.xlsx")
            ]
        )
        
        for file_path in files:
            self.add_item_to_selection(file_path)
            
    def browse_folder(self):
        """Browse and select folder"""
        folder = filedialog.askdirectory(title="Select Folder to Encrypt/Decrypt")
        if folder:
            self.add_item_to_selection(folder)
            
    def add_item_to_selection(self, item_path):
        """Add item to selection list"""
        if item_path not in self.selected_items:
            self.selected_items.append(item_path)
            self.update_files_listbox()
            
    def clear_selection(self):
        """Clear all selected items"""
        self.selected_items.clear()
        self.update_files_listbox()
        
    def update_files_listbox(self):
        """Update the files listbox display"""
        self.files_listbox.delete(0, tk.END)
        for item in self.selected_items:
            # Show just the filename/folder name
            display_name = os.path.basename(item)
            if os.path.isdir(item):
                display_name += " (folder)"
            self.files_listbox.insert(tk.END, display_name)
            
    def encrypt_files(self):
        """Encrypt selected files"""
        if not self.selected_items:
            messagebox.showwarning("No Selection", "Please select files or folders to encrypt.")
            return
            
        # Get password
        password_dialog = ModernPasswordDialog(self.root, "Encryption Password")
        password = password_dialog.get_password()
        
        if not password:
            return
            
        # Get output directory
        output_dir = filedialog.askdirectory(title="Select Output Directory for Encrypted Files")
        if not output_dir:
            return
            
        # Start encryption in background thread
        self.start_operation_thread(self._encrypt_worker, password, output_dir)
        
    def decrypt_files(self):
        """Decrypt selected files"""
        if not self.selected_items:
            messagebox.showwarning("No Selection", "Please select files to decrypt.")
            return
            
        # Verify that selected items are encrypted files
        encrypted_files = [f for f in self.selected_items if f.endswith('.enc')]
        if not encrypted_files:
            messagebox.showwarning("Invalid Selection", 
                                 "Please select encrypted files (.enc extension) to decrypt.")
            return
            
        # Get password
        password_dialog = ModernPasswordDialog(self.root, "Decryption Password")
        password = password_dialog.get_password()
        
        if not password:
            return
            
        # Get output directory
        output_dir = filedialog.askdirectory(title="Select Output Directory for Decrypted Files")
        if not output_dir:
            return
            
        # Start decryption in background thread
        self.start_operation_thread(self._decrypt_worker, password, output_dir, encrypted_files)
        
    def start_operation_thread(self, worker_func, *args):
        """Start operation in background thread"""
        self.set_ui_state(False)
        self.progress_var.set(0)
        
        thread = threading.Thread(target=worker_func, args=args, daemon=True)
        thread.start()
        
    def _encrypt_worker(self, password, output_dir):
        """Background worker for encryption"""
        try:
            total_items = len(self.selected_items)
            
            for i, item_path in enumerate(self.selected_items):
                self.update_status(f"Encrypting: {os.path.basename(item_path)}", "working")
                
                if os.path.isfile(item_path):
                    # Encrypt file
                    output_path = os.path.join(output_dir, 
                                              os.path.basename(item_path) + '.enc')
                    self.encryption_engine.encrypt_file(item_path, output_path, password)
                    
                elif os.path.isdir(item_path):
                    # Encrypt folder
                    folder_name = os.path.basename(item_path)
                    output_path = os.path.join(output_dir, folder_name + '.enc')
                    self.file_manager.encrypt_folder(item_path, output_path, 
                                                   self.encryption_engine, password)
                
                # Update progress
                progress = ((i + 1) / total_items) * 100
                self.progress_var.set(progress)
                
            self.update_status("Encryption completed successfully!", "success")
            messagebox.showinfo("Success", "Files encrypted successfully!")
            
        except Exception as e:
            self.update_status("Encryption failed!", "error")
            messagebox.showerror("Encryption Error", f"Encryption failed:\n{str(e)}")
            
        finally:
            self.set_ui_state(True)
            self.progress_var.set(0)
            
    def _decrypt_worker(self, password, output_dir, encrypted_files):
        """Background worker for decryption"""
        try:
            total_items = len(encrypted_files)
            
            for i, file_path in enumerate(encrypted_files):
                self.update_status(f"Decrypting: {os.path.basename(file_path)}", "working")
                
                # Remove .enc extension for output
                base_name = os.path.basename(file_path)[:-4]  # Remove .enc
                output_path = os.path.join(output_dir, base_name)
                
                if file_path.endswith('.enc'):
                    # Check if it's a folder or file
                    if self.file_manager.is_encrypted_folder(file_path):
                        self.file_manager.decrypt_folder(file_path, output_path,
                                                       self.encryption_engine, password)
                    else:
                        self.encryption_engine.decrypt_file(file_path, output_path, password)
                
                # Update progress
                progress = ((i + 1) / total_items) * 100
                self.progress_var.set(progress)
                
            self.update_status("Decryption completed successfully!", "success")
            messagebox.showinfo("Success", "Files decrypted successfully!")
            
        except Exception as e:
            self.update_status("Decryption failed!", "error")
            messagebox.showerror("Decryption Error", f"Decryption failed:\n{str(e)}")
            
        finally:
            self.set_ui_state(True)
            self.progress_var.set(0)
            
    def update_status(self, message, status_type="info"):
        """Update status message with icon and color"""
        icon_map = {
            "info": "ℹ️",
            "success": "✅", 
            "error": "❌",
            "warning": "⚠️",
            "working": "⚡"
        }
        
        icon = icon_map.get(status_type, "ℹ️")
        formatted_message = f"{icon} {message}"
        self.root.after(0, lambda: self.status_var.set(formatted_message))
        
    def set_ui_state(self, enabled):
        """Enable/disable UI elements during operations"""
        state = "normal" if enabled else "disabled"
        self.encrypt_btn.configure(state=state)
        self.decrypt_btn.configure(state=state)
        
    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo("Settings", "Settings dialog coming soon!")
        
    def secure_delete(self):
        """Show secure delete dialog"""
        messagebox.showinfo("Secure Delete", "Secure delete feature coming soon!")
        
    def show_help(self):
        """Show help documentation"""
        help_text = """
Secure File Encryption Tool - User Guide

ENCRYPTION:
1. Select files or folders using Browse buttons
2. Click 'Encrypt Files'
3. Enter a strong password
4. Choose output directory
5. Wait for completion

DECRYPTION:
1. Select encrypted files (.enc extension)
2. Click 'Decrypt Files'
3. Enter the correct password
4. Choose output directory
5. Wait for completion

SECURITY TIPS:
- Use strong passwords (12+ characters, mixed case, numbers, symbols)
- Remember your passwords - they cannot be recovered
- Keep backups of important files
- Store encrypted files in secure locations

SUPPORTED FEATURES:
- AES-256 encryption
- File and folder encryption
- Batch operations
- Progress tracking
- Cross-platform support
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("User Guide")
        help_window.geometry("600x500")
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.configure(state="disabled")
        
        scrollbar = ttk.Scrollbar(text_widget)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=text_widget.yview)
        
    def show_about(self):
        """Show modern about dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("500x600")
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()
        about_window.configure(bg=ModernTheme.COLORS['background'])
        
        # Center the dialog
        about_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 200,
            self.root.winfo_rooty() + 50
        ))
        
        # Main container
        main_container = tk.Frame(about_window, bg=ModernTheme.COLORS['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.SPACING['lg'], 
                           pady=ModernTheme.SPACING['lg'])
        
        # Header card
        header_card = ModernWidgets.create_card_frame(main_container, 
                                                     padding=ModernTheme.SPACING['xl'])
        header_card.pack(fill=tk.X, pady=(0, ModernTheme.SPACING['lg']))
        
        # App icon and title
        title_frame = tk.Frame(header_card, bg=ModernTheme.COLORS['surface'])
        title_frame.pack(fill=tk.X)
        
        app_icon = ModernWidgets.create_heading_label(
            title_frame, "🔒", font=("Segoe UI", 24)
        )
        app_icon.pack(side=tk.LEFT, padx=(0, ModernTheme.SPACING['md']))
        
        title_info = tk.Frame(title_frame, bg=ModernTheme.COLORS['surface'])
        title_info.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        app_title = ModernWidgets.create_heading_label(
            title_info, "Secure File Encryption Tool"
        )
        app_title.pack(anchor=tk.W)
        
        company_title = ModernWidgets.create_subheading_label(
            title_info, "Zplus Cyber Secure Technologies Pvt Ltd"
        )
        company_title.pack(anchor=tk.W)
        
        version_label = ModernWidgets.create_body_label(title_info, "Version 1.0")
        version_label.pack(anchor=tk.W)
        
        # Description card
        desc_card = ModernWidgets.create_card_frame(main_container, 
                                                   padding=ModernTheme.SPACING['lg'])
        desc_card.pack(fill=tk.X, pady=(0, ModernTheme.SPACING['md']))
        
        desc_label = ModernWidgets.create_body_label(
            desc_card,
            "A desktop application for secure file and folder encryption\n"
            "using industry-standard AES-256 encryption."
        )
        desc_label.pack(anchor=tk.W)
        
        # Features card
        features_card = ModernWidgets.create_card_frame(main_container, 
                                                       padding=ModernTheme.SPACING['lg'])
        features_card.pack(fill=tk.X, pady=(0, ModernTheme.SPACING['md']))
        
        features_header = ModernWidgets.create_subheading_label(features_card, "Features")
        features_header.pack(anchor=tk.W, pady=(0, ModernTheme.SPACING['sm']))
        
        features = [
            "🛡️ Military-grade AES-256 encryption",
            "📁 File and folder encryption",
            "🔐 Password protection",
            "🖥️ Cross-platform support",
            "👥 User-friendly interface",
            "⚡ Fast encryption/decryption"
        ]
        
        for feature in features:
            feature_label = ModernWidgets.create_body_label(features_card, feature)
            feature_label.pack(anchor=tk.W, pady=ModernTheme.SPACING['xs'])
        
        # Tech info card
        tech_card = ModernWidgets.create_card_frame(main_container, 
                                                   padding=ModernTheme.SPACING['lg'])
        tech_card.pack(fill=tk.X, pady=(0, ModernTheme.SPACING['md']))
        
        tech_header = ModernWidgets.create_subheading_label(tech_card, "Technical Information")
        tech_header.pack(anchor=tk.W, pady=(0, ModernTheme.SPACING['sm']))
        
        tech_info = [
            "Built with Python and tkinter",
            "Encryption powered by the cryptography library",
            "Modern UI/UX design",
            "Secure random salt and IV generation"
        ]
        
        for info in tech_info:
            info_label = ModernWidgets.create_body_label(tech_card, f"• {info}")
            info_label.pack(anchor=tk.W, pady=ModernTheme.SPACING['xs'])
        
        # Footer card
        footer_card = ModernWidgets.create_card_frame(main_container, 
                                                     padding=ModernTheme.SPACING['lg'])
        footer_card.pack(fill=tk.X)
        
        copyright_label = ModernWidgets.create_body_label(
            footer_card, "© 2025 Zplus Cyber Secure Technologies Pvt Ltd"
        )
        copyright_label.pack(anchor=tk.W)
        
        # Close button
        close_btn = ModernWidgets.create_primary_button(
            footer_card, "Close", about_window.destroy
        )
        close_btn.pack(anchor=tk.E, pady=(ModernTheme.SPACING['md'], 0))
