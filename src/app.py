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
        input_dict = { 
            "headingData" : {
                "project_name": "House Riding",
                "project_creator": "Ye Thu"
            },
            "informationData": {
                "height": 34,
                "weight" : 23,
                "student_name": "adsasdfdasf"
            } ,
            "visualizationData": {
                "categories": ["Joint Angles XZY", "Joint Angles ZXY"],
                "movements": ["L5S1 Lateral Bending", "L5S1 Axial Bending" ], 
                "scenerio": ["Horse Riding"],
                "duration": 180,
                "starting_time": 20,
                "Graph_type": "Double Graph" , 
                # Graph type options =>["Single Graph", "Double Graph"],
                "fig_size": (15,5),
                "ref_name": "JohnSon",
                "ref_file": "C:/Users/yethu/Desktop/Movement Analysis Project/data/Reference downsampled data/Simulator riding/Reference Harjusimu-003 Extended walk.xlsx",
                "student_name": "Toni",
                "student_file": "C:/Users/yethu/Desktop/Movement Analysis Project/data/Student downsampled data/simulator riding/Sudent1-003Harju ext walk.xlsx"
            }
        }

        self.data_visualization = DataVisualization(input_dict)
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

    def show_visualize_data(self, data):
        if self.data_visualization:
            self.data_visualization.pack_forget()
        self.project_creation.pack_forget()
        self.data_visualization = DataVisualization(self, data)
        self.data_visualization.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = App()
    app.mainloop()
