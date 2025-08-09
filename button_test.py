#!/usr/bin/env python3
"""
Simple test to verify button functionality
"""
import tkinter as tk

def test_button():
    """Test if buttons work"""
    print("Button clicked!")

# Create main window
root = tk.Tk()
root.title("Button Test")
root.geometry("600x400")

# Create test frame
test_frame = tk.Frame(root, bg='yellow', relief='solid', bd=2)
test_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Create test label
test_label = tk.Label(test_frame, text="BUTTON TEST AREA", 
                     font=('Arial', 16, 'bold'), bg='yellow')
test_label.pack(pady=10)

# Create test buttons
btn1 = tk.Button(test_frame, text="🔒 ENCRYPT TEST", 
                command=test_button,
                font=('Arial', 12, 'bold'),
                bg='green', fg='white',
                width=20, height=2)
btn1.pack(pady=10)

btn2 = tk.Button(test_frame, text="🔓 DECRYPT TEST", 
                command=test_button,
                font=('Arial', 12, 'bold'),
                bg='red', fg='white',
                width=20, height=2)
btn2.pack(pady=10)

print("Test window created. If you can see buttons, tkinter is working fine.")
root.mainloop()
