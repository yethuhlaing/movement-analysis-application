import tkinter as tk
from tkinter import PhotoImage, ttk, font
from first_page import LandingPage
from second_page import ProjectCreation
from utils import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('Movement Analysis')

        # setting tkinter window size
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))

        # logo
        filepath = '../assets/lab-logo.png'
        p1 = PhotoImage(file=filepath)
        self.iconphoto(False, p1)

        # Create instances of the LandingPage
        self.first_page = LandingPage(self)
        self.second_page = None

        # Show the landing page initially using pack
        self.first_page.pack(expand=True, fill="both")
        
    # functions to switch between frames
    def show_second_page(self, project_name,project_creator):
        if self.second_page:
            self.second_page.destroy()
        self.first_page.pack_forget()
        self.second_page = ProjectCreation(self, project_name=project_name,project_creator=project_creator)
        self.second_page.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = App()
    app.mainloop()
