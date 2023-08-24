import tkinter as tk
from tkinter import Canvas, ttk, font
from PIL import Image, ImageTk
from database.database import *
from configparser import ConfigParser
from tkinter import messagebox 
from data import *
from utilities.utils import *
from data_visualization.data_visualization import DataVisualization

COLOR = '#%02x%02x%02x' % (174, 239, 206)
class LandingPage(ttk.Frame):
    def __init__(self, parent):
        #font Style
        self.button_font = font.Font(family="Bookman Old Style", size=10)
        self.text_font = font.Font(family="Bookman Old Style", size=10)
        self.heading_font = font.Font(family="Bookman Old Style", size=20, weight="bold")

        tk.Frame.__init__(self, parent, bg="white")
        self.pack(expand=True, fill="both")
        
        # Database Path
        config = ConfigParser()
        config.read('config.ini')
        self.db_path = config.get('Database', 'database_path')
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

        # Widgets for the left column
        welcome_label = tk.Label(overlay_canvas, text="Welcome to Movement Analysis!", font=self.heading_font, padx=20,  bg="white")
        welcome_label.pack(pady=50)

        # # Large space for text
        # large_space_label = tk.Label(overlay_canvas, text="", bg="white", pady=100)
        # large_space_label.pack()

        # Project Name
        project_name_label = tk.Label(overlay_canvas, text="Project Name:", font=self.text_font, bg="white", padx=10, pady=5)
        project_name_label.pack()

        self.project_name_entry = ttk.Entry(overlay_canvas)
        self.project_name_entry.pack()

        # Project Creator
        project_creator_label = tk.Label(overlay_canvas, text="Project Creator:", font=self.text_font, bg="white", padx=10, pady=5)
        project_creator_label.pack()

        self.project_creator_entry = ttk.Entry(overlay_canvas)
        self.project_creator_entry.pack()

        # Create a frame for recent projects
        recent_projects_frame = tk.Frame(overlay_canvas, background = "white")
        recent_projects_frame.pack()

        # Recent History
        recent_projects_label = tk.Label(recent_projects_frame, text="Recent Projects", font=self.text_font, bg="white")
        recent_projects_label.pack()

        self.createRecentProject(recent_projects_frame)
    
        # Start Button
        start_button = tk.Button(overlay_canvas, text="Create new", bg=COLOR, bd=0,width=20,padx=30 , font=self.button_font, command=self.start_app)
        start_button.pack(pady=20)

    def createRecentProject(self, parent):
        selected = tk.StringVar()
        self.treeView = ttk.Treeview(parent, columns=(1,2,3,4,5), height=10, show="headings", )
        self.treeView.column(1, anchor="center", stretch="no", width=50)
        self.treeView.column(2, anchor="center", stretch="no", width=100)
        self.treeView.column(3, anchor="center", stretch="no", width=100)
        self.treeView.column(4, anchor="center", stretch="no", width=100)
        self.treeView.column(5, anchor="center", stretch="no", width=100)

        self.treeView.heading(1, text="No.")
        self.treeView.heading(2, text="Project")
        self.treeView.heading(3, text="Scenario")
        self.treeView.heading(4, text="Student")
        self.treeView.heading(5, text="Created")
        self.displayData()
        self.treeView.pack()

        self.combobox = ttk.Combobox(parent, textvariable=selected, values=["All", *self.comboboxOptions()], font=self.text_font)
        self.combobox.bind("<<ComboboxSelected>>", self.on_combo_select)
        self.combobox.pack()
        deleteButton = tk.Button(parent, text ="Delete",bg= COLOR, bd=0,width=20,padx=10 , font=self.button_font, command=self.deleteHistory)
        deleteButton.pack( pady=3, anchor="e", padx=60)
        openButton = tk.Button(parent, text ="Open",bg= COLOR, bd=0,width=20,padx=10 , font=self.button_font, command=self.openHistory )
        openButton.pack( pady=3, anchor="e", padx=60)
        
    def comboboxOptions(self):
        project_list = selectAllProject(self.db_path)
        return [ project[0] for project in project_list]
         
    def displayData(self):
        histories = retreiveHistory(self.db_path)
        for index, history in enumerate(histories, start=0):
            student_id = history[0] 
            project = history[1]
            scenario = history[2]  
            student = history[3]
            createdDate = history[4]
            self.treeView.insert('',index, value=(student_id, project, scenario, student, createdDate))
        self.treeView.bind("<ButtonRelease-1>", self.on_click)

    def on_combo_select(self, event):
        for item in self.treeView.get_children():
            self.treeView.delete(item)
        selectedProject = self.combobox.get()
        self.selectedHistory = None
        if selectedProject == "All":
            self.displayData()
        else:
            selectedHistories = retreiveSelectedHistory(self.db_path, selectedProject)
            for index, selectedHistory in enumerate(selectedHistories, start=0):
                self.treeView.insert('',index, values=selectedHistory)
            self.treeView.bind("<ButtonRelease-1>", self.on_click)

    def on_click(self, event):
        history = self.treeView.identify_row(event.y)
        if history:
            history_id = history
            self.selectedHistory = self.treeView.item(history_id, "values")
            print("Clicked item values:", self.selectedHistory) 

    def deleteHistory(self):
        result = messagebox.askyesno("Confirmation", f"Do you want to delete?")
        if result:
            if self.selectedHistory != None:
                student_id = self.selectedHistory[0]
                deleteHistory(self.db_path, student_id)
                for item in self.treeView.get_children():
                    self.treeView.delete(item)    
                self.displayData()
                self.combobox['values'] = ["All", *self.comboboxOptions() ]  
            else:       
                messagebox.showerror("Error", "Please select the project before you delete!")
                
    def openHistory(self):
        result = messagebox.askyesno("Confirmation", f"Do you want to open this?")
        if result:
            if self.selectedHistory != None:
                student_id = self.selectedHistory[0]
                reference_df, student_df , status_df = retrieveSelectedDataframeList(self.db_path, student_id)        
                setReference_df(reference_df)
                setStudent_df(student_df)
                setStatus_df(status_df)
                
                # Switch to Data Visualization Page
                DataVisualization()
                self.pack_forget()
            else:       
                messagebox.showerror("Error", "Please select the project before you open!")
    # def on_double_click(self, event):
    #     history = self.treeView.identify_row(event.y)
    #     if history:
    #         history_id = history
    #         values = self.treeView.item(history_id, "values")
    #         result = messagebox.askyesnocancel("Action Selection", f"What do you want to do with {values[0]}?", default=messagebox.CANCEL)
    #         if result == True:
    #             # Delete the item
    #             self.treeView.delete(history_id)
    #         elif result == False:
    #             # Open the item (you can customize this action)
    #             pass
    #         print("Clicked item values:", values)

    def start_app(self):
        project_name = self.project_name_entry.get()
        # Switch to the project creation page and pass the project name
        self.master.show_project_creation(project_name)

  