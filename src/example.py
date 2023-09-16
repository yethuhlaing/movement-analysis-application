import tkinter as tk

# Create a Tkinter window
root = tk.Tk()
root.title("Options")

# Create a Listbox widget
listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True)

# Insert 100 options into the Listbox
for i in range(1, 101):
    listbox.insert(tk.END, f"Option {i}")

# Create 10 columns by placing multiple Listboxes side by side
num_columns = 10
listboxes = []

for i in range(num_columns):
    column_listbox = tk.Listbox(root)
    column_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    listboxes.append(column_listbox)

# Populate the columns with options
options = [f"Option {i}" for i in range(1, 101)]

for i, option in enumerate(options):
    column_index = i % num_columns
    listboxes[column_index].insert(tk.END, option)

# Start the Tkinter main loop
root.mainloop()