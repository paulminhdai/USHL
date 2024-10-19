import tkinter as tk
from tkinter import filedialog
from generateReport import generate_reports
import threading

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    input_file_var.set(file_path)
    message_label.config(text="")

def select_directory():
    dir_path = filedialog.askdirectory()
    output_dir_var.set(dir_path)

def submit():
    input_pdf_path = input_file_var.get()
    output_dir = output_dir_var.get()

    if not input_pdf_path or not output_dir:
        message_label.config(text="Please fill all fields", fg="orange")
        return

    # Show processing message
    message_label.config(text="Processing...", fg="blue")

    def worker():
        try:
            generate_reports(input_pdf_path, output_dir)
            message_label.config(text="Completed to generate reports from the spreadsheet", fg="green")
        except Exception as e:
            message_label.config(text=f"An error occurred: {e}", fg="red")

    # Run the report generation in a separate thread to keep the GUI responsive
    threading.Thread(target=worker, daemon=True).start()
    
def clear_message(event=None):
    message_label.config(text="")

# Create the main window
root = tk.Tk()
root.title("Generate reports from spreadsheet")

# Create and place the widgets
tk.Label(root, text="Input Excel File:").grid(row=0, column=0, padx=10, pady=5)
input_file_var = tk.StringVar()
input_file_entry = tk.Entry(root, textvariable=input_file_var, width=50)
input_file_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=5)
output_dir_var = tk.StringVar()
output_dir_entry = tk.Entry(root, textvariable=output_dir_var, width=50)
output_dir_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_directory).grid(row=1, column=2, padx=10, pady=5)

# Message label to display results
message_label = tk.Label(root, text="", fg="black")
message_label.grid(row=2, column=0, columnspan=3, pady=10)

# Bind input fields to clear the message label
input_file_entry.bind("<FocusIn>", clear_message)
output_dir_entry.bind("<FocusIn>", clear_message)

tk.Button(root, text="Submit", command=submit).grid(row=3, column=1, pady=20)

# Start the GUI event loop
root.mainloop()
