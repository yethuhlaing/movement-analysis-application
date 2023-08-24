import tkinter as tk
from tkinter import PhotoImage, ttk, font
from data_visualization.data_visualization import DataVisualization
from landing_page.landing_page import LandingPage
from project_creation import ProjectCreation
from configparser import ConfigParser

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('Movement Analysis')
        #page height for pdf printing, addjusting might be needed
        self.page_height = 800
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

    # functions to switch between frames
    def show_project_creation(self, project_name, project_creator):
        if self.project_creation:
            self.project_creation.destroy()
        self.landing_page.pack_forget()
        self.project_creation = ProjectCreation(self, project_name=project_name,project_creator=project_creator)
        self.project_creation.pack(expand=True, fill="both")

    def show_visualize_data(self, data):
        if self.data_visualization:
            self.data_visualization.pack_forget()
        self.project_creation.pack_forget()
        self.data_visualization = DataVisualization(data)
        self.data_visualization.pack(expand=True, fill="both")

    def save_current_frame_as_pdf(self, output_path):
        if self.data_visualization:
            total_pages = 3  # Adjust based on the number of pages your content spans
            all_captured_images = []
            for page_number in range(1, total_pages + 1):
                captured_image = capture_frame_page(self.data_visualization, self.page_height, page_number)
                all_captured_images.append(captured_image)
            images_to_pdf(all_captured_images, output_path)

if __name__ == "__main__":
    app = App()
    app.mainloop()
