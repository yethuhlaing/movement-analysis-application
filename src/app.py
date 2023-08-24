import tkinter as tk
from tkinter import PhotoImage, ttk, font
from data_visualization.data_visualization import DataVisualization
from landing_page.landing_page import LandingPage
from project_creation.project_creation import ProjectCreation
from database.database import create_tables
from configparser import ConfigParser
from data import *
from utilities.utils import *

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
        self.landing_page = LandingPage(self)
        self.project_creation = None
        self.data_visualization = None

        # Show the landing page initially using pack
        self.landing_page.pack(expand=True, fill="both")
        # DataVisualization()
        # DataVisualization()
    # functions to switch between frames
    def show_project_creation(self, project_name):
    def show_project_creation(self, project_name):
        if self.project_creation:
            self.project_creation.destroy()
        self.landing_page.pack_forget()
        self.project_creation = ProjectCreation(self, project_name=project_name)
        self.project_creation = ProjectCreation(self, project_name=project_name)
        self.project_creation.pack(expand=True, fill="both")

    def show_visualize_data(self, data):
        if self.data_visualization:
            self.data_visualization.pack_forget()
        self.project_creation.pack_forget()
        self.data_visualization = DataVisualization(self, self, data)
        self.data_visualization.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = App()
    app.mainloop()
