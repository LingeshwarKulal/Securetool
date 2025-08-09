"""
Secure File Encryption Tool
Main application entry point
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from gui.main_window import MainWindow
from utils.logger import setup_logging

def main():
    """Main application entry point"""
    try:
        # Setup logging
        setup_logging()
        
        # Create and configure main window
        root = tk.Tk()
        root.title("Secure File Encryption Tool")
        root.geometry("800x600")
        root.minsize(600, 400)
        
        # Set window icon if available
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.ico")
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        except Exception:
            pass  # Icon not critical for functionality
        
        # Create main application window
        app = MainWindow(root)
        
        # Start the GUI event loop
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Application Error", f"Failed to start application:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
