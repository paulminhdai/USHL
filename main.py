import tkinter as tk
from tkinter import filedialog
from processPdf import replace_pdf

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    input_file_var.set(file_path)
    # Clear the message when a new file is selected
    message_label.config(text="")

def submit():
    input_pdf_path = input_file_var.get()
    new_text = new_text_var.get()

    if not input_pdf_path or not new_text:
        message_label.config(text="Please fill all fields", fg="orange")
        return

    try:
        output_pdf_path = replace_pdf(input_pdf_path, new_text)
        message_label.config(text=f"PDF processed and saved to {output_pdf_path}", fg="green")
    except Exception as e:
        message_label.config(text=f"An error occurred: {e}", fg="red")

def clear_message(event=None):
    message_label.config(text="")

# Create the main window
root = tk.Tk()
root.title("USHL PDF Report Replace")

# Create and place the widgets
tk.Label(root, text="Browse Primex PDF Report File:").grid(row=0, column=0, padx=10, pady=5)
input_file_var = tk.StringVar()
input_file_entry = tk.Entry(root, textvariable=input_file_var, width=50)
input_file_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Replace Referring Physician With:").grid(row=3, column=0, padx=10, pady=5)
new_text_var = tk.StringVar()
tk.Entry(root, textvariable=new_text_var, width=50).grid(row=3, column=1, padx=10, pady=5)

# Message label to display results
message_label = tk.Label(root, text="", fg="black")
message_label.grid(row=4, column=0, columnspan=3, pady=10)

# Bind input fields to clear the message label
input_file_entry.bind("<FocusIn>", clear_message)
tk.Entry(root, textvariable=new_text_var, width=50).bind("<FocusIn>", clear_message)

tk.Button(root, text="Submit", command=submit).grid(row=5, column=1, pady=30)

# Start the GUI event loop
root.mainloop()
