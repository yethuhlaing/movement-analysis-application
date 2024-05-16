import tkinter as tk
import time
import threading
from tkinter import Canvas, ttk, font
from PIL import Image, ImageTk
from tkinter import messagebox 
from utils import *

COLOR = '#%02x%02x%02x' % (174, 239, 206)
class LandingPage(ttk.Frame):
    def __init__(self, parent):
        self.root = parent
        tk.Frame.__init__(self, self.root, bg="white")
        self.pack(expand=True, fill="both")
        
        #font Style
        self.button_font = font.Font(family="Bookman Old Style", size=10)
        self.text_font = font.Font(family="Bookman Old Style", size=10)
        self.heading_font = font.Font(family="Bookman Old Style", size=20, weight="bold")
        self.create_widgets()

        
    def create_widgets(self):
        # Background image
        # Using the configure even image is resized to the window size
        # Implementing a delay in the resizing possibly makes it smoother
        bg_image = Image.open("../assets/landing_page_bg.png")
        bg_image = bg_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas = Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        canvas.grid(row=0, column=0, columnspan=3)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        def resizer(event):
            global bg1, resized_bg, new_bg # Needed for garbage collector
            bg1 = Image.open("../assets/landing_page_bg.png")
            resized_bg = bg1.resize((event.width, event.height),Image.Resampling.LANCZOS)
            new_bg = ImageTk.PhotoImage(resized_bg)
            canvas.create_image(0, 0, image=new_bg, anchor="nw")
        self.bind('<Configure>', resizer)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Overlay canvas for the left column
        overlay_canvas = Canvas(self, width=self.winfo_screenwidth() // 2, height=self.winfo_screenheight(), bg="white", highlightthickness=0)
        overlay_canvas.grid(row=0, column=0, sticky="nsew")

        # Heading Label
        welcome_label = tk.Label(overlay_canvas, text="Welcome to Movement Analysis!", font=self.heading_font, padx=20,  bg="white")
        welcome_label.pack(pady=50)
        
        # Create three frames
        frame1 = tk.Frame(overlay_canvas, bg="white")
        frame2 = tk.Frame(overlay_canvas, bg="white")
        frame3 = tk.Frame(overlay_canvas, bg="white")

        # Pack the frames on the right side
        frame1.pack(fill="x", pady= (90,0))
        frame2.pack(fill="x")
        frame3.pack(fill="x")


        # Project Name
        self.project_name_entry = ttk.Entry(frame1, width=30)
        self.project_name_entry.pack( side="right")
        project_name_label = tk.Label(frame1, text="Project Name:", font=self.text_font, bg="white", padx=10, pady=5)
        project_name_label.pack(side="right")


        # Project Creator
        self.project_creator_entry = ttk.Entry(frame2, width=30)
        self.project_creator_entry.pack( side="right")
        project_creator_label = tk.Label(frame2, text="Project Creator:", font=self.text_font, bg="white", padx=10, pady=5)
        project_creator_label.pack(side="right")

    
        # Start Button
        start_button = tk.Button(frame3, text="Create", bg=COLOR, bd=0,width=20,padx=10 , font=self.button_font, command=self.start_app)
        start_button.pack(side="right", pady=20)


    def start_app(self):
        project_name = self.project_name_entry.get()
        project_creator = self.project_creator_entry.get()
        # Switch to the project creation page and pass the project name
        self.master.show_second_page(project_name,project_creator)

  