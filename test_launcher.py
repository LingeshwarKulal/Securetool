#!/usr/bin/env python3
"""
Simple test launcher for the encryption tool
"""
import tkinter as tk
from simple_main import SimpleMainWindow

def main():
    root = tk.Tk()
    root.title("🔒 Secure File Encryption Tool - DEBUG VERSION")
    root.geometry("900x700")
    root.minsize(800, 600)
    
    app = SimpleMainWindow(root)
    
    print("=== DEBUG VERSION LAUNCHED ===")
    print("If you can see the yellow button area with green/red buttons, the issue is in the original code.")
    print("If you can't see buttons here either, it's a system/tkinter issue.")
    
    root.mainloop()

if __name__ == "__main__":
    main()
