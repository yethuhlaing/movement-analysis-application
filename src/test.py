import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Create a Treeview widget
tree = ttk.Treeview(root)
tree.pack()

# Define table data
table_data = [
    ["Data 1", "Data 2", "Data 3"],
    ["Data 4", "Data 5", "Data 6"],
    ["Data 7", "Data 8", "Data 9"],
    ["Data 10", "Data 11", "Data 12"],
]

# Configure border width for specific tags
tree.tag_configure('oddrow', borderwidth=2)
tree.tag_configure('evenrow', borderwidth=1)

# Add table data to the Treeview
for i, row in enumerate(table_data):
    # Determine the tag for the row
    tag = 'oddrow' if i % 2 == 0 else 'evenrow'

    # Insert the row into the Treeview
    tree.insert('', 'end', values=row, tags=(tag,))

root.mainloop()
