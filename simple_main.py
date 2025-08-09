"""
Simplified Main Window for Debugging
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os

class SimpleMainWindow:
    """Simplified main application window for debugging"""
    
    def __init__(self, root):
        self.root = root
        self.selected_items = []
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the simplified user interface"""
        # Main container
        main_container = tk.Frame(self.root, bg='#f8fafc')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        header_frame = tk.Frame(main_container, bg='white', relief='solid', bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = tk.Label(header_frame, text="🔒 Secure File Encryption Tool",
                              font=('Arial', 18, 'bold'), bg='white', fg='#1f2937')
        title_label.pack(pady=20)
        
        # File selection section
        selection_frame = tk.Frame(main_container, bg='white', relief='solid', bd=1)
        selection_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Section header
        selection_header = tk.Label(selection_frame, text="📁 File Selection",
                                   font=('Arial', 14, 'bold'), bg='white', fg='#1f2937')
        selection_header.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        # Browse buttons
        button_frame = tk.Frame(selection_frame, bg='white')
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        browse_files_btn = tk.Button(button_frame, text="📄 Browse Files", 
                                   command=self.browse_files,
                                   font=('Arial', 10), bg='#2563eb', fg='white',
                                   relief='raised', bd=2, padx=10, pady=5)
        browse_files_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        browse_folder_btn = tk.Button(button_frame, text="📂 Browse Folder", 
                                    command=self.browse_folder,
                                    font=('Arial', 10), bg='#2563eb', fg='white',
                                    relief='raised', bd=2, padx=10, pady=5)
        browse_folder_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(button_frame, text="🗑️ Clear Selection", 
                            command=self.clear_selection,
                            font=('Arial', 10), bg='#6b7280', fg='white',
                            relief='raised', bd=2, padx=10, pady=5)
        clear_btn.pack(side=tk.LEFT)
        
        # File list
        list_label = tk.Label(selection_frame, text="Selected files and folders:",
                            font=('Arial', 10), bg='white', fg='#6b7280')
        list_label.pack(anchor=tk.W, padx=20, pady=(0, 5))
        
        # Listbox frame
        listbox_frame = tk.Frame(selection_frame, bg='white')
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.files_listbox = tk.Listbox(listbox_frame, 
                                       bg='white', fg='#1f2937',
                                       selectbackground='#2563eb',
                                       selectforeground='white',
                                       font=('Arial', 10),
                                       relief='solid', bd=1)
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.files_listbox.yview)
        
        # Operations section - THIS IS THE CRITICAL PART
        operations_frame = tk.Frame(main_container, bg='white', relief='solid', bd=1)
        operations_frame.pack(fill=tk.X)
        
        # Operations header
        ops_header = tk.Label(operations_frame, text="⚡ Operations",
                            font=('Arial', 14, 'bold'), bg='white', fg='#1f2937')
        ops_header.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        # BUTTON AREA - BRIGHT COLORED FOR VISIBILITY
        button_area = tk.Frame(operations_frame, bg='yellow', relief='solid', bd=3, height=100)
        button_area.pack(fill=tk.X, padx=20, pady=(0, 20))
        button_area.pack_propagate(False)  # Maintain fixed height
        
        # Test label
        test_label = tk.Label(button_area, text="OPERATION BUTTONS BELOW:",
                            font=('Arial', 12, 'bold'), bg='yellow', fg='black')
        test_label.pack(pady=(10, 5))
        
        # Button container
        btn_container = tk.Frame(button_area, bg='yellow')
        btn_container.pack()
        
        # ENCRYPT BUTTON
        self.encrypt_btn = tk.Button(btn_container, text="🔒 ENCRYPT FILES", 
                                   command=self.encrypt_files,
                                   font=('Arial', 12, 'bold'),
                                   bg='green', fg='white',
                                   relief='raised', bd=3,
                                   width=18, height=2)
        self.encrypt_btn.pack(side=tk.LEFT, padx=(10, 5))
        
        # DECRYPT BUTTON  
        self.decrypt_btn = tk.Button(btn_container, text="🔓 DECRYPT FILES", 
                                   command=self.decrypt_files,
                                   font=('Arial', 12, 'bold'),
                                   bg='red', fg='white',
                                   relief='raised', bd=3,
                                   width=18, height=2)
        self.decrypt_btn.pack(side=tk.LEFT, padx=(5, 10))
        
        # Status area
        status_frame = tk.Frame(operations_frame, bg='white')
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.status_var = tk.StringVar(value="Ready - Select files and use operation buttons above")
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                              font=('Arial', 10), bg='white', fg='#6b7280')
        status_label.pack()
        
    def browse_files(self):
        """Browse and select files"""
        files = filedialog.askopenfilenames(title="Select Files")
        for file_path in files:
            if file_path not in self.selected_items:
                self.selected_items.append(file_path)
        self.update_files_list()
        
    def browse_folder(self):
        """Browse and select folder"""
        folder = filedialog.askdirectory(title="Select Folder")
        if folder and folder not in self.selected_items:
            self.selected_items.append(folder)
        self.update_files_list()
            
    def clear_selection(self):
        """Clear all selected items"""
        self.selected_items.clear()
        self.update_files_list()
        
    def update_files_list(self):
        """Update the files listbox"""
        self.files_listbox.delete(0, tk.END)
        for item in self.selected_items:
            display_name = os.path.basename(item)
            if os.path.isdir(item):
                display_name += " (folder)"
            self.files_listbox.insert(tk.END, display_name)
        
        # Update status
        count = len(self.selected_items)
        self.status_var.set(f"Ready - {count} item(s) selected. Use operation buttons to encrypt/decrypt.")
            
    def encrypt_files(self):
        """Test encrypt function"""
        if not self.selected_items:
            messagebox.showwarning("No Selection", "Please select files or folders first!")
            return
        
        # Show simple message for testing
        count = len(self.selected_items)
        messagebox.showinfo("Encrypt Test", f"ENCRYPT function called!\nSelected {count} items for encryption.")
        self.status_var.set(f"Encrypt clicked - {count} items ready for encryption")
        
    def decrypt_files(self):
        """Test decrypt function"""
        if not self.selected_items:
            messagebox.showwarning("No Selection", "Please select files first!")
            return
            
        # Show simple message for testing
        count = len(self.selected_items)
        messagebox.showinfo("Decrypt Test", f"DECRYPT function called!\nSelected {count} items for decryption.")
        self.status_var.set(f"Decrypt clicked - {count} items ready for decryption")
