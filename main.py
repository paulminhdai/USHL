import tkinter as tk
from tkinter import filedialog, ttk
from processPdf import replace_pdf
from generateReport import generate_reports
import threading

def select_file_fix_primex():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    input_file_var_fix_primex.set(file_path)
    message_label_fix_primex.config(text="")

def submit_fix_primex():
    input_pdf_path = input_file_var_fix_primex.get()
    new_text = new_text_var_fix_primex.get()

    if not input_pdf_path or not new_text:
        message_label_fix_primex.config(text="Please fill all fields", fg="orange")
        return

    try:
        output_pdf_path = replace_pdf(input_pdf_path, new_text)
        message_label_fix_primex.config(text=f"PDF processed and saved to {output_pdf_path}", fg="green")
    except Exception as e:
        message_label_fix_primex.config(text=f"An error occurred: {e}", fg="red")

def clear_message_fix_primex(event=None):
    message_label_fix_primex.config(text="")

def select_file_generate_reports():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    input_file_var_generate_reports.set(file_path)
    message_label_generate_reports.config(text="")

def select_directory_generate_reports():
    dir_path = filedialog.askdirectory()
    output_dir_var_generate_reports.set(dir_path)

def submit_generate_reports():
    input_file_path = input_file_var_generate_reports.get()
    output_dir = output_dir_var_generate_reports.get()

    if not input_file_path or not output_dir:
        message_label_generate_reports.config(text="Please fill all fields", fg="orange")
        return

    message_label_generate_reports.config(text="Processing...", fg="blue")

    def worker():
        try:
            generate_reports(input_file_path, output_dir)
            message_label_generate_reports.config(text="Completed to generate reports from the spreadsheet", fg="green")
        except Exception as e:
            message_label_generate_reports.config(text=f"An error occurred: {e}", fg="red")

    threading.Thread(target=worker, daemon=True).start()

def clear_message_generate_reports(event=None):
    message_label_generate_reports.config(text="")

# Create the main window
root = tk.Tk()
root.title("USHL Reports")

# Create a Notebook widget for tabbed interface
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Frame for Fix Primex Report
frame_fix_primex = ttk.Frame(notebook)
notebook.add(frame_fix_primex, text="Fix Primex Report")

tk.Label(frame_fix_primex, text="Browse Primex PDF Report File:").grid(row=0, column=0, padx=10, pady=5)
input_file_var_fix_primex = tk.StringVar()
input_file_entry_fix_primex = tk.Entry(frame_fix_primex, textvariable=input_file_var_fix_primex, width=50)
input_file_entry_fix_primex.grid(row=0, column=1, padx=10, pady=5)
tk.Button(frame_fix_primex, text="Browse", command=select_file_fix_primex).grid(row=0, column=2, padx=10, pady=5)

tk.Label(frame_fix_primex, text="Replace Referring Physician With:").grid(row=3, column=0, padx=10, pady=5)
new_text_var_fix_primex = tk.StringVar()
tk.Entry(frame_fix_primex, textvariable=new_text_var_fix_primex, width=50).grid(row=3, column=1, padx=10, pady=5)

message_label_fix_primex = tk.Label(frame_fix_primex, text="", fg="black")
message_label_fix_primex.grid(row=4, column=0, columnspan=3, pady=10)

input_file_entry_fix_primex.bind("<FocusIn>", clear_message_fix_primex)
tk.Entry(frame_fix_primex, textvariable=new_text_var_fix_primex, width=50).bind("<FocusIn>", clear_message_fix_primex)

tk.Button(frame_fix_primex, text="Submit", command=submit_fix_primex).grid(row=5, column=1, pady=30)

# Frame for Generate Reports
frame_generate_reports = ttk.Frame(notebook)
notebook.add(frame_generate_reports, text="Generate Reports")

tk.Label(frame_generate_reports, text="Input Excel File:").grid(row=0, column=0, padx=10, pady=5)
input_file_var_generate_reports = tk.StringVar()
input_file_entry_generate_reports = tk.Entry(frame_generate_reports, textvariable=input_file_var_generate_reports, width=50)
input_file_entry_generate_reports.grid(row=0, column=1, padx=10, pady=5)
tk.Button(frame_generate_reports, text="Browse", command=select_file_generate_reports).grid(row=0, column=2, padx=10, pady=5)

tk.Label(frame_generate_reports, text="Output Directory:").grid(row=1, column=0, padx=10, pady=5)
output_dir_var_generate_reports = tk.StringVar()
output_dir_entry_generate_reports = tk.Entry(frame_generate_reports, textvariable=output_dir_var_generate_reports, width=50)
output_dir_entry_generate_reports.grid(row=1, column=1, padx=10, pady=5)
tk.Button(frame_generate_reports, text="Browse", command=select_directory_generate_reports).grid(row=1, column=2, padx=10, pady=5)

message_label_generate_reports = tk.Label(frame_generate_reports, text="", fg="black")
message_label_generate_reports.grid(row=2, column=0, columnspan=3, pady=10)

input_file_entry_generate_reports.bind("<FocusIn>", clear_message_generate_reports)
output_dir_entry_generate_reports.bind("<FocusIn>", clear_message_generate_reports)

tk.Button(frame_generate_reports, text="Submit", command=submit_generate_reports).grid(row=3, column=1, pady=20)

# Start the GUI event loop
root.mainloop()
