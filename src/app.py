import tkinter as tk
from tkinter import PhotoImage, ttk, font
from data_visualization import DataVisualization
from landing_page import LandingPage
from project_creation import ProjectCreation

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
        self.landing_page = None
        self.project_creation = None
        input_list = ["HorseBack Riding","Ye Thu Hlaing", 180, 70, "Johnson", "JointXYZ","L5S1 Flexion/Extension"]
        self.data_visualization = DataVisualization(input_list)
        # Show the landing page initially using pack
        # self.landing_page.pack(expand=True, fill="both")
        self.data_visualization.pack(expand=True, fill="both")

    # functions to switch between frames
    def show_project_creation(self, project_name):
        if self.project_creation:
            self.project_creation.destroy()
        self.landing_page.pack_forget()
        self.project_creation = ProjectCreation(self, project_name=project_name)
        self.project_creation.pack(expand=True, fill="both")

    # just an example of how to get data
    def show_visualize_data(self, project_name, student_name, height, weight):
        self.project_creation.grid_forget()
        self.visualize_data = DataVisualization(self, 
            project_name=project_name, 
            student_name=student_name,
            height=height, 
            weight=weight)
        self.visualize_data.grid(row=0, column=0, sticky='nsew')


if __name__ == "__main__":
    app = App()
    app.mainloop()
