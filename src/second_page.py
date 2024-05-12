import tkinter as tk
from tkinter import ttk, font, filedialog
from data import *
import pandas as pd
COLOR = '#%02x%02x%02x' % (174, 239, 206)
from data_visualization import analyze
class TimeSliderWidget():
    def __init__(self, parent):
        self.button_font = font.Font(family="Bookman Old Style", size=11)
        self.text_font = font.Font(family="Bookman Old Style", size=11)
        self.heading_font = font.Font(family="Bookman Old Style", size=15, weight="bold")

        self.frames_in_seconds = 0  # Default value, to be set later

        self.result_label = tk.Label(parent, text="Selected Time: 0 seconds", background="white", font=self.text_font)
        self.result_label.pack(anchor="w", pady=10)
        self.slider = ttk.Scale(parent, from_=0, to=self.frames_in_seconds, orient="horizontal", length=400)
        # self.slider = ttk.Scale(self, from_=0, to=self.frames_in_seconds, orient="horizontal", length=700, style="Custom.Horizontal.TScale" )
        self.slider.pack()



        self.slider.bind("<Motion>", self.update_selected_time)

    def set_frames_in_seconds(self, frames_in_seconds):
        self.frames_in_seconds = frames_in_seconds
        self.slider.config(to=frames_in_seconds)
        print(self.frames_in_seconds)

    def update_selected_time(self, event):
        selected_time = int(self.slider.get())
        self.result_label.config(text=f"Selected Time: {selected_time} seconds", font=self.text_font)

class ExcelFileInputWidget(tk.Button):
    def __init__(self, parent, time_slider_widget, data_type):
        super().__init__(parent, text="Click to select an Excel", bg="white", borderwidth=1, width= 20,padx=15, pady=5)
        self.default_bg = "white"
        self.configure(cursor="hand2")
        self.time_slider_widget = time_slider_widget  # Reference to TimeSliderWidget
        self.bind("<Button-1>", self.select_file)
        self.frame_count = None
        self.frame_rate = None
        self.file_path = None
        self.data_type = data_type

    def select_file(self, event):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        self.file_path = file_path
        if file_path:
            self.configure(bg=COLOR)  # Change background color to green
            trimmed_filename = file_path.rstrip('/').split('/')[-1]
            self["text"] = trimmed_filename
            if self.data_type == "reference":
                self.process_excel(file_path)

    def process_excel(self, file_path):
        try:
            # Read data from different sheets
            general_info_df = pd.read_excel(file_path, engine='openpyxl', sheet_name='General Information')
            joint_angles_df = pd.read_excel(file_path, engine='openpyxl', sheet_name='Joint Angles XZY')
            # Retrieve frame count from the last cell of the first column of Center Of Mass sheet
            self.frame_count = joint_angles_df.iloc[-1, 0]
            # Retrieve frame rate from cell (b,5) of General Information sheet
            self.frame_rate = general_info_df.iloc[3, 1]
            # Set frames_in_seconds value in the TimeSliderWidget
            frames_in_seconds = self.frame_count
            self.time_slider_widget.set_frames_in_seconds(frames_in_seconds)
            print("Count", frames_in_seconds)
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None, None
    def get_file_path(self):
        return self.file_path



        


class ProjectCreation(ttk.Frame):
    def __init__(self, parent, project_name,project_creator):
        tk.Frame.__init__(self, parent, bg="white")
        self.project_name = project_name
        self.project_creator = project_creator
        self.data = []
        self.spreadsheet_tabs = {}
        self.create_widgets()
        self.pack(expand=True, fill="both")


    def SpreadsheetPopup(self, parent, spreadsheet_data):
        self.spreadsheet_data = spreadsheet_data
        self.tab_listboxes = {}  
        self.tab_data = {}

        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True)

        s = ttk.Style()
        s.configure('TNotebook.Tab', padding=[1, 5], borderWidth=0, background= COLOR)

        for tab_name , columns in spreadsheet_data.items():
            tab_frame = tk.Frame(self.notebook, background="white" )
            self.notebook.add(tab_frame, text=tab_name )
            
            self.listbox = tk.Listbox(tab_frame, selectmode=tk.MULTIPLE, relief="flat", borderwidth=0, background="white")
            self.listbox.pack(fill="both", expand=True)
            for column in columns:
                self.listbox.insert(tk.END, f"{column}")
            self.listbox.bind("<<ListboxSelect>>", self.on_select)
            self.tab_listboxes[tab_name] = self.listbox

    

        # Bind tab changes to update the selection on the listboxes
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_select(self, event):
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        selected_data = []

        # Get selected items from the listbox in the current tab
        current_listbox = self.tab_listboxes[selected_tab]
        selected_indices = current_listbox.curselection()
        for index in selected_indices:
            selected_data.append(current_listbox.get(index))

        self.tab_data[selected_tab] = selected_data

    def on_tab_change(self, event):
        self.selectedListbox.delete(0, tk.END)
        for tab_name, data in self.tab_data.items():
            tab_name = f"{tab_name}"
            self.selectedListbox.insert(tk.END, f" {tab_name}")
            for index, category  in enumerate(data):
                self.selectedListbox.insert(tk.END, f"  {index+1})  {category}")
            self.selectedListbox.insert(tk.END, "")


        

    def create_widgets(self):
        self.button_font = font.Font(family="Bookman Old Style", size=11)
        self.text_font = font.Font(family="Bookman Old Style", size=11)
        self.heading_font = font.Font(family="Bookman Old Style", size=13)
        style = ttk.Style()
        style.configure("Custom.TLabelframe", background="white", font=("Bookman Old Style", 20))
        style.configure("TLabelFrame.Label", background="white", font=("Bookman Old Style", 20))
        
        # Divided Two Frame
        leftFrame = tk.Frame(self, background="white",padx=20, pady=20)
        middleFrame = tk.Frame(self, background="white", padx=80, pady=30)
        rightFrame = tk.Frame(self, background="white", padx=5, pady=10)
        bottomFrame = tk.Frame(self, background="white", padx=5, pady=10)

        leftFrame.grid(row=0, column=0, sticky="nsew")
        middleFrame.grid(row=0, column=1, sticky="nsew")
        rightFrame.grid(row=0, column=2,  sticky="nsew")

        bottomFrame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)

        self.create_middle_frame(middleFrame)
        self.create_left_frame(leftFrame)
        self.create_right_frame(rightFrame)
        self.create_bottom_frame(bottomFrame)
    def create_left_frame(self, leftFrame):
        # Configure grid weights to center the parent frame
        leftFrame.grid_rowconfigure(0, weight=1)
        leftFrame.grid_columnconfigure(0, weight=1)

        # Create a frame for the projectInfoFrame 
        projectInfoFrame = tk.Frame(leftFrame, bg="white")
        projectInfoFrame.grid(row=0, column=0, padx=10,  sticky="nswe")

        # Create a frame for the categoryChoosingFrame
        categoryChoosingFrame = tk.Frame(leftFrame, borderwidth=2, relief="solid")
        categoryChoosingFrame.grid(row=1, column=0, padx=10,  sticky="nswe")

        # Configure grid weights to allow vertical expansion
        leftFrame.grid_rowconfigure(0, weight=1)
        leftFrame.grid_rowconfigure(1, weight=1)


        # Project Information Frame

        projectNameFrame = tk.Frame(projectInfoFrame, bg="white")
        projectNameFrame.pack(anchor="w")
        projectNameLabel = tk.Label(projectNameFrame, text="Project Name - ", font=self.heading_font, pady=5, padx= 10, bg="white")
        projectNameLabel.pack(side="left")
        projectName = tk.Label(projectNameFrame, text=self.project_name, font=self.heading_font, pady=5, bg="white")
        projectName.pack(side="left")

        projectCreatorFrame = tk.Frame(projectInfoFrame, bg="white")
        projectCreatorFrame.pack(anchor="w")
        projectCreatorLabel = tk.Label(projectCreatorFrame, text="Project Creator - ", font=self.heading_font, pady=5, padx= 10, bg="white")
        projectCreatorLabel.pack(side="left")
        projectCreator = tk.Label(projectCreatorFrame, text=self.project_creator, font=self.heading_font, pady=5, bg="white")
        projectCreator.pack(side="left")

        scenarioFrame = tk.Frame(projectInfoFrame, bg="white")
        scenarioFrame.pack(anchor="e")
        scenario_name_label = tk.Label(scenarioFrame, text="Scenario Name", font=self.text_font, pady=5, padx=10, bg="white")
        scenario_name_label.pack(side="left")
        self.scenario_name_var = tk.StringVar(value="")
        scenario_name_entry = ttk.Entry(scenarioFrame, textvariable=self.scenario_name_var, width=30)
        scenario_name_entry.pack(side="left")

        referenceFrame = tk.Frame(projectInfoFrame, bg="white")
        referenceFrame.pack(anchor="e")
        refrence_name_label = tk.Label(referenceFrame, text="Refrence name", font=self.text_font, pady=5, padx=10, bg="white")
        refrence_name_label.pack(side="left")
        self.refrence_name_var = tk.StringVar(value="")
        refrence_name_entry = ttk.Entry(referenceFrame, textvariable=self.refrence_name_var, width=30)
        refrence_name_entry.pack(side="left")

        studentFrame = tk.Frame(projectInfoFrame, bg="white")
        studentFrame.pack(anchor="e")
        student_name_label = tk.Label(studentFrame, text="Student name", font=self.text_font, pady=5, padx=10, bg="white")
        student_name_label.pack(side="left")
        self.student_name_var = tk.StringVar(value="")
        student_name_entry = ttk.Entry(studentFrame, textvariable=self.student_name_var, width=30)
        student_name_entry.pack(side="left")

        refrenceExcelFrame = tk.Frame(projectInfoFrame, bg="white")
        refrenceExcelFrame.pack(anchor="e")
        refrence_excel_label = tk.Label(refrenceExcelFrame, text="Reference Excel", font=self.text_font, padx=10, bg="white")
        refrence_excel_label.pack(side="left")
        self.refrence_excel_widget = ExcelFileInputWidget(refrenceExcelFrame, self.time_slider_widget, "reference")
        self.refrence_excel_widget.pack(side="left")

        studentExcelFrame = tk.Frame(projectInfoFrame, bg="white")
        studentExcelFrame.pack(anchor="e",pady=5)
        student_excel_label = tk.Label(studentExcelFrame, text="Student Excel", font=self.text_font, padx=10, bg="white")
        student_excel_label.pack(side="left")
        self.student_excel_widget = ExcelFileInputWidget(studentExcelFrame, self.time_slider_widget, "student")
        self.student_excel_widget.pack(side="left")

    def create_right_frame(self, rightFrame):
        self.selectedListbox = tk.Listbox(rightFrame, selectmode=tk.MULTIPLE, relief="solid", borderwidth=1, background="white")
        self.selectedListbox.pack(fill="both", expand=True, padx=10)

        
        start_button = tk.Button(rightFrame, text="Analyze", bg=COLOR, bd=0, 
                                 command=lambda: self.on_start_button_click(), height=2)
        start_button.pack(padx=10,  fill="x", expand=True)

    def create_middle_frame(self, middleFrame):
    # GENERAL FRAME
        self.time_slider_widget = TimeSliderWidget(middleFrame)
        
        # Heading "Duration" with a dropbox
        durationFrame = tk.Frame(middleFrame, bg="white")
        duration_label = tk.Label(durationFrame, text="Duration", font=self.text_font, bg="white", padx=10, pady=5)
        duration_label.pack(side="left")
        self.duration_var = tk.StringVar(value="")
        duration_entry = ttk.Entry(durationFrame, textvariable=self.duration_var, width=30)
        duration_entry.pack(side="left")
        durationFrame.pack(anchor="w")

        graphFrame = tk.Frame(middleFrame, bg="white")
        # Choosing Graph type
        graph_label = tk.Label(graphFrame, text="Graph Type", font=self.text_font, padx=10, pady=5, bg="white")
        graph_label.pack(side="left")
        graph_options = ["Single Graph", "Double Graph"]
        self.graph_var = tk.StringVar(value=graph_options[0])
        graph_dropdown = ttk.Combobox(graphFrame, textvariable=self.graph_var, font=self.text_font, values=graph_options, state="readonly", width=20)
        graph_dropdown.pack(side="left")
        graphFrame.pack(anchor="w")

        # self.popupFrame = tk.Frame(middleFrame, bg="white")
        # self.popupFrame.pack(fill="both", expand=True)
        heightFrame = tk.Frame(middleFrame, bg="white")
        heightFrame.pack(anchor="w")
        height_label = tk.Label(heightFrame, text="Height(cm)", font=self.text_font, pady=5, padx=10, background="white")
        height_label.pack(side="left")
        self.height_var = tk.StringVar(value="")
        height_entry = ttk.Entry(heightFrame, textvariable=self.height_var, width=30)
        height_entry.pack(side="left")

        weightFrame = tk.Frame(middleFrame, bg="white")
        weightFrame.pack(anchor="w")
        weight_label = tk.Label(weightFrame, text="Weight(kg)", font=self.text_font, pady=5, padx=10, background="white")
        weight_label.pack(side="left")
        self.weight_var = tk.StringVar(value="")
        weight_entry = ttk.Entry(weightFrame, textvariable=self.weight_var, width=30)
        weight_entry.pack(side="left")


    def create_bottom_frame(self, bottomFrame):
        spreadsheet_data = SpreadsheetData
        self.SpreadsheetPopup(bottomFrame, spreadsheet_data)

    def on_confirm_columns(self, chosen_columns):
        self.chosen_columns = chosen_columns
        return None

    def on_start_button_click(self):
        # Gets selected checkboxes for sheet names
        self.chosen_columns = self.tab_data
        testing_user_data = {
            "headingData": {
                "project_name": "adsdsaf",
                "project_creator": "sadfads"
            },
            "informationData": {
                "height": "12",
                "weight": "12",
                "student_name": "asa"
            },
            "visualizationData": {
                "categories": {
                    "Segment Orientation - Quat": ["Pelvis q1", "L5 q3", "T12 q0"],
                    "Segment Orientation - Euler": ["L5 x", "L3 z", "T12 z"],
                    "Segment Position": ["L5 x", "L5 z", "L3 z", "T8 x"],
                    "Segment Velocity": ["L5 y", "T12 y", "T8 z"]
                },
                "scenario": "Demo",
                "duration": "100",
                "starting_time": 108,
                "Graph_type": "Single Graph",
                "ref_name": "HI",
                "ref_file": "C:/Users/yethu/Desktop/Movement Analysis Project/data/REference 240Hz data/Real horse riding/Reference Realhorse1-007 ext trot 1_frames_1138-2337.xlsx",
                "student_name": "asa",
                "student_file": "C:/Users/yethu/Desktop/Movement Analysis Project/data/Student 240Hzdata/Sudent1 horse1-008 ext trot 1_frames_552-1904.xlsx"
            },
            "summaryData": {
                "category": [],
                "movement": [],
                "minimum_time": [],
                "maximum_time": [],
                "minimum_duration": [],
                "optimal_duration": [],
                "maximum_duration": []
            }
            }

        
        user_data = {
            "headingData" : {
                "project_name": self.project_name,
                "project_creator": self.project_creator
            },
            "informationData": {
                "height": self.height_var.get(),
                "weight" : self.weight_var.get(),
                "student_name": self.student_name_var.get()
            } ,
            "visualizationData": {
                "categories": self.chosen_columns,
                "scenario": self.scenario_name_var.get(),
                "duration": self.duration_var.get(),
                "starting_time": int(self.refrence_excel_widget.time_slider_widget.slider.get()),
                "Graph_type": self.graph_var.get(),
                "ref_name": self.refrence_name_var.get(),               
                "ref_file": self.refrence_excel_widget.file_path,
                "student_name": self.student_name_var.get(),
                "student_file": self.student_excel_widget.get_file_path()
            },
            "summaryData": {
                "category" : [],
                "movement" : [],
                "minimum_time" : [],
                "maximum_time": [] ,
                "minimum_duration": [] ,
                "optimal_duration": [],
                "maximum_duration":[],
            }
        }

        
        analyze("frame", testing_user_data["visualizationData"])

        # Switch to the DataVisualization page and pass the data array
        # self.master.show_visualize_data()
