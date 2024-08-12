import tkinter as tk
from tkinter import filedialog, messagebox
from processPdf import replace_pdf


def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    input_file_var.set(file_path)
    

def submit():
    input_pdf_path = input_file_var.get()
    new_text = new_text_var.get()

    if not input_pdf_path or not new_text:
        messagebox.showwarning("Input Error", "Please fill all fields")
        return
    try:
        output_pdf_path = replace_pdf(input_pdf_path, new_text)
        messagebox.showinfo("Success", f"PDF processed and saved to {output_pdf_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Create the main window
root = tk.Tk()
root.title("USHL PDF Report Replace")

# Create and place the widgets
tk.Label(root, text="Input PDF File:").grid(row=0, column=0, padx=10, pady=5)
input_file_var = tk.StringVar()
tk.Entry(root, textvariable=input_file_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Replace Referring Physician With:").grid(row=3, column=0, padx=10, pady=5)
new_text_var = tk.StringVar()
tk.Entry(root, textvariable=new_text_var, width=50).grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Submit", command=submit).grid(row=4, column=1, pady=20)

# Start the GUI event loop
root.mainloop()