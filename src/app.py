import tkinter as tk
from tkinter import PhotoImage, ttk, font
from data_visualization import DataVisualization
from first_page import LandingPage
from second_page import ProjectCreation
from database import create_tables
from configparser import ConfigParser
from data import *
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

        # Database Initialization
        config = ConfigParser()
        config.read('config.ini')
        db_path = config.get('Database', 'database_path')
        create_tables(db_path)

        # User Data
        # setUserData({})
        # setDataframe({})
        # Create instances of the LandingPage
        # self.first_page = LandingPage(self)
        # self.second_page = None
        # self.data_visualization = None

        # Show the landing page initially using pack
        # self.first_page.pack(expand=True, fill="both")
        # DataVisualization(self)
        ProjectCreation(self,"adsdsaf", "sadfads")
    # functions to switch between frames
    def show_second_page(self, project_name,project_creator):
        if self.second_page:
            self.second_page.destroy()
        self.first_page.pack_forget()
        self.second_page = ProjectCreation(self, project_name=project_name,project_creator=project_creator)
        self.second_page.pack(expand=True, fill="both")

    def show_visualize_data(self):
        if self.data_visualization:
            self.data_visualization.pack_forget()
        if self.first_page:
            self.first_page.pack_forget()
        if self.second_page:
            self.second_page.pack_forget()
        self.data_visualization = DataVisualization(self)
        self.data_visualization.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = App()
    app.mainloop()
