import tkinter as tk
from tkinter import ttk, font
COLOR = '#%02x%02x%02x' % (174, 239, 206)
class LandingPage(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="white")
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        # Add your landing page widgets here
        # For example, you can add labels, buttons, or images to welcome the user

        welcome_label = tk.Label(self, text="Welcome to Movement Analysis!", font=font.Font(size=25), padx=20)
        welcome_label.grid(row=0, column=0, columnspan=3, pady=50)

        # Large space for text
        large_space_label = tk.Label(self, text="", bg="white", pady=100)
        large_space_label.grid(row=1, column=0, columnspan=3)

        # Project Name
        project_name_label = tk.Label(self, text="Project Name:", font=font.Font(size=15), padx=10, pady=5)
        project_name_label.grid(row=2, column=0, sticky='e', padx=(100, 10), pady=5)

        self.project_name_entry = ttk.Entry(self)
        self.project_name_entry.grid(row=2, column=1, columnspan=2, sticky='w', pady=5)

        # Project Creator
        project_creator_label = tk.Label(self, text="Project Creator:", font=font.Font(size=15), padx=10, pady=5)
        project_creator_label.grid(row=3, column=0, sticky='e', padx=(100, 10), pady=5)

        self.project_creator_entry = ttk.Entry(self)
        self.project_creator_entry.grid(row=3, column=1, columnspan=2, sticky='w', pady=5)

        # Configure grid row and column resizing
        self.grid_rowconfigure(1, weight=1)  # Large space row
        self.grid_columnconfigure(0, weight=1)  # First column
        self.grid_columnconfigure(1, weight=1)  # Second column
        self.grid_columnconfigure(2, weight=1)  # Third column

        start_button = tk.Button(self, text="Start", bg="#aeefdc", bd=0, width=20, padx=20, command=self.start_app)
        start_button.grid(row=4, column=1, columnspan=2, pady=20)

    def start_app(self):
        project_name = self.project_name_entry.get()
        # Switch to the project creation page and pass the project name
        self.master.show_project_creation(project_name)