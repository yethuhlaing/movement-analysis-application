import tkinter as tk
from tkinter import Canvas, ttk, font
from PIL import Image, ImageTk
import math
COLOR = '#%02x%02x%02x' % (174, 239, 206)
class LandingPage(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="white")
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        # Background image
        # Using the configure even image is resized to the window size
        # Implementing a delay in the resizing possibly makes it smoother
        bg_image = Image.open("temp_bgimg.jpg")
        bg_image = bg_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas = Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        canvas.grid(row=0, column=0, columnspan=3)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        def resizer(event):
            global bg1, resized_bg, new_bg
            bg1 = Image.open("temp_bgimg.jpg")
            resized_bg = bg1.resize((event.width, event.height),Image.Resampling.LANCZOS)
            new_bg = ImageTk.PhotoImage(resized_bg)
            canvas.create_image(0, 0, image=new_bg, anchor="nw")
        self.bind('<Configure>', resizer)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Overlay canvas for the left column
        overlay_canvas = Canvas(self, width=self.winfo_screenwidth() // 2, height=self.winfo_screenheight(), bg="white", highlightthickness=0)
        overlay_canvas.grid(row=0, column=0, sticky="nsew")

        # Widgets for the left column
        welcome_label = tk.Label(overlay_canvas, text="Welcome to Movement Analysis!", font=font.Font(size=25), padx=20)
        welcome_label.pack(pady=50)

        # Large space for text
        large_space_label = tk.Label(overlay_canvas, text="", bg="white", pady=100)
        large_space_label.pack()

        # Project Name
        project_name_label = tk.Label(overlay_canvas, text="Project Name:", font=font.Font(size=15), padx=10, pady=5)
        project_name_label.pack()

        self.project_name_entry = ttk.Entry(overlay_canvas)
        self.project_name_entry.pack()

        # Project Creator
        project_creator_label = tk.Label(overlay_canvas, text="Project Creator:", font=font.Font(size=15), padx=10, pady=5)
        project_creator_label.pack()

        self.project_creator_entry = ttk.Entry(overlay_canvas)
        self.project_creator_entry.pack()

        # Start Button
        start_button = tk.Button(overlay_canvas, text="Start", bg="#aeefdc", bd=0, width=20, padx=20, command=self.start_app)
        start_button.pack(pady=20)

    def start_app(self):
        project_name = self.project_name_entry.get()
        # Switch to the project creation page and pass the project name
        self.master.show_project_creation(project_name)