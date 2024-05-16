import tkinter as tk
from tkinter import ttk, font, filedialog
import pandas as pd
COLOR = '#%02x%02x%02x' % (174, 239, 206)
from generate_pdf import analyze
class TimeSliderWidget():
    def __init__(self, parent):
        self.button_font = font.Font(family="Bookman Old Style", size=11)
        self.text_font = font.Font(family="Bookman Old Style", size=11)
        self.heading_font = font.Font(family="Bookman Old Style", size=15, weight="bold")

        self.frames_in_seconds = 0  # Default value, to be set later

        self.result_label = tk.Label(parent, text="Selected Time: 0 seconds", background="white", font=self.text_font)
        self.result_label.pack(anchor="w", pady=10)
        self.slider = ttk.Scale(parent, from_=0, to=self.frames_in_seconds, orient="horizontal", length=400)
        self.slider.pack()

        self.slider.bind("<Motion>", self.update_selected_time)

    def set_frames_in_seconds(self, frames_in_seconds):
        self.frames_in_seconds = frames_in_seconds
        self.slider.config(to=frames_in_seconds)

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
        self.frame_rate : int = None
        self.file_path: str = None
        self.data_type:str = data_type 
        self.total_frame: int = None
    def select_file(self, event):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        self.file_path = file_path
        if file_path:
            self.configure(bg=COLOR)  # Change background color to green
            trimmed_filename = file_path.rstrip('/').split('/')[-1]
            self["text"] = trimmed_filename
            if self.data_type == "reference":
                total_frame, frame_rate, frames_in_seconds = process_excel(file_path)
                self.frame_rate = frame_rate
                self.total_frame = total_frame
                self.time_slider_widget.set_frames_in_seconds(frames_in_seconds)

    def getFrameRate(self):
        return self.frame_rate

    def get_file_path(self):
        return self.file_path


def process_excel(file_path):
    try:
        # Read data from different sheets
        general_info_df = pd.read_excel(file_path, engine='openpyxl', sheet_name='General Information')
        joint_angles_df = pd.read_excel(file_path, engine='openpyxl', sheet_name='Joint Angles XZY')
        # Retrieve frame count from the last cell of the first column of Center Of Mass sheet
        total_frame = int(joint_angles_df.iloc[-1, 0])
        # Retrieve frame rate from cell (b,5) of General Information sheet
        frame_rate = int(general_info_df.iloc[3, 1])
        # Set frames_in_seconds value in the TimeSliderWidget
        frames_in_seconds = total_frame/240

        print("Frame Count", total_frame)
        print("Seconds", frames_in_seconds)
        return total_frame, frame_rate, frames_in_seconds 
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        


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
                "project_name": "Demo Movement",
                "project_creator": "Ye Thu Hlaing"
            },
            "informationData": {
                "height": "12",
                "weight": "12",
                "student_name": "Johnson"
            },
            "visualizationData": {
                "categories": {
                    "Segment Orientation - Quat": ["Pelvis q1", "L5 q3", "T12 q0"],
                    "Segment Orientation - Euler": ["L5 x", "L3 z", "T12 z"],
                    "Segment Position": ["L5 x", "L5 z", "L3 z", "T8 x"],
                    "Segment Velocity": ["L5 y", "T12 y", "T8 z"]
                },
                "scenario": "Sprint Running",
                "duration": "100000000",
                "total_frames": 100,
                "starting_time": 1,
                "frame_rate": 240,
                "Graph_type": "Single Graph",
                "ref_name": "HI",
                "ref_file": "C:/Users/yethu/Desktop/Movement Analysis Project/data/REference 240Hz data/Real horse riding/Reference Realhorse1-007 ext trot 1_frames_1138-2337.xlsx",
                "student_name": "Johnson",
                "student_file": "C:/Users/yethu/Desktop/Movement Analysis Project/data/Student 240Hzdata/Sudent1 horse1-008 ext trot 1_frames_552-1904.xlsx"
            },
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
                "total_frames": self.refrence_excel_widget.total_frame,
                "starting_time": self.refrence_excel_widget.time_slider_widget.slider.get(),
                "frame_rate": self.refrence_excel_widget.getFrameRate(),
                "Graph_type": self.graph_var.get(),
                "ref_name": self.refrence_name_var.get(),               
                "ref_file": self.refrence_excel_widget.file_path,
                "student_name": self.student_name_var.get(),
                "student_file": self.student_excel_widget.get_file_path()
            },
        }
 
        analyze(user_data)

        # Switch to the DataVisualization page and pass the data array
        # self.master.show_visualize_data()


SpreadsheetData = {
    "Segment Orientation - Quat": [
        "Pelvis q0", "Pelvis q1", "Pelvis q2", "Pelvis q3", "L5 q0", "L5 q1", "L5 q2", "L5 q3", "L3 q0", "L3 q1",
        "L3 q2", "L3 q3", "T12 q0", "T12 q1", "T12 q2", "T12 q3", "T8 q0", "T8 q1", "T8 q2", "T8 q3", "Neck q0",
        "Neck q1", "Neck q2", "Neck q3", "Head q0", "Head q1", "Head q2", "Head q3", "Right Shoulder q0",
        "Right Shoulder q1", "Right Shoulder q2", "Right Shoulder q3", "Right Upper Arm q0", "Right Upper Arm q1",
        "Right Upper Arm q2", "Right Upper Arm q3", "Right Forearm q0", "Right Forearm q1", "Right Forearm q2",
        "Right Forearm q3", "Right Hand q0", "Right Hand q1", "Right Hand q2", "Right Hand q3", "Left Shoulder q0",
        "Left Shoulder q1", "Left Shoulder q2", "Left Shoulder q3", "Left Upper Arm q0", "Left Upper Arm q1",
        "Left Upper Arm q2", "Left Upper Arm q3", "Left Forearm q0", "Left Forearm q1", "Left Forearm q2",
        "Left Forearm q3", "Left Hand q0", "Left Hand q1", "Left Hand q2", "Left Hand q3", "Right Upper Leg q0",
        "Right Upper Leg q1", "Right Upper Leg q2", "Right Upper Leg q3", "Right Lower Leg q0", "Right Lower Leg q1",
        "Right Lower Leg q2", "Right Lower Leg q3", "Right Foot q0", "Right Foot q1", "Right Foot q2", "Right Foot q3",
        "Right Toe q0", "Right Toe q1", "Right Toe q2", "Right Toe q3", "Left Upper Leg q0", "Left Upper Leg q1",
        "Left Upper Leg q2", "Left Upper Leg q3", "Left Lower Leg q0", "Left Lower Leg q1", "Left Lower Leg q2",
        "Left Lower Leg q3", "Left Foot q0", "Left Foot q1", "Left Foot q2", "Left Foot q3", "Left Toe q0", "Left Toe q1",
        "Left Toe q2", "Left Toe q3"],
    "Segment Orientation - Euler": [
        "Pelvis x", "Pelvis y", "Pelvis z", "L5 x", "L5 y", "L5 z", "L3 x", "L3 y", "L3 z", "T12 x", "T12 y", "T12 z", 
        "T8 x", "T8 y", "T8 z", "Neck x", "Neck y", "Neck z", "Head x", "Head y", "Head z", "Right Shoulder x", 
        "Right Shoulder y", "Right Shoulder z", "Right Upper Arm x", "Right Upper Arm y", "Right Upper Arm z", 
        "Right Forearm x", "Right Forearm y", "Right Forearm z", "Right Hand x", "Right Hand y", "Right Hand z", 
        "Left Shoulder x", "Left Shoulder y", "Left Shoulder z", "Left Upper Arm x", "Left Upper Arm y", "Left Upper Arm z", 
        "Left Forearm x", "Left Forearm y", "Left Forearm z", "Left Hand x", "Left Hand y", "Left Hand z", 
        "Right Upper Leg x", "Right Upper Leg y", "Right Upper Leg z", "Right Lower Leg x", "Right Lower Leg y", 
        "Right Lower Leg z", "Right Foot x", "Right Foot y", "Right Foot z", "Right Toe x", "Right Toe y", "Right Toe z", 
        "Left Upper Leg x", "Left Upper Leg y", "Left Upper Leg z", "Left Lower Leg x", "Left Lower Leg y", 
        "Left Lower Leg z", "Left Foot x", "Left Foot y", "Left Foot z", "Left Toe x", "Left Toe y", "Left Toe z"
    ],
    "Segment Position" : [
        "Pelvis x", "Pelvis y", "Pelvis z", "L5 x", "L5 y", "L5 z", "L3 x", "L3 y", "L3 z",
        "T12 x", "T12 y", "T12 z", "T8 x", "T8 y", "T8 z", "Neck x", "Neck y", "Neck z",
        "Head x", "Head y", "Head z", "Right Shoulder x", "Right Shoulder y", "Right Shoulder z",
        "Right Upper Arm x", "Right Upper Arm y", "Right Upper Arm z", "Right Forearm x", "Right Forearm y", "Right Forearm z",
        "Right Hand x", "Right Hand y", "Right Hand z", "Left Shoulder x", "Left Shoulder y", "Left Shoulder z",
        "Left Upper Arm x", "Left Upper Arm y", "Left Upper Arm z", "Left Forearm x", "Left Forearm y", "Left Forearm z",
        "Left Hand x", "Left Hand y", "Left Hand z", "Right Upper Leg x", "Right Upper Leg y", "Right Upper Leg z",
        "Right Lower Leg x", "Right Lower Leg y", "Right Lower Leg z", "Right Foot x", "Right Foot y", "Right Foot z",
        "Right Toe x", "Right Toe y", "Right Toe z", "Left Upper Leg x", "Left Upper Leg y", "Left Upper Leg z",
        "Left Lower Leg x", "Left Lower Leg y", "Left Lower Leg z", "Left Foot x", "Left Foot y", "Left Foot z",
        "Left Toe x", "Left Toe y", "Left Toe z"
    ],
    "Segment Velocity": [
        "Pelvis x", "Pelvis y", "Pelvis z", "L5 x", "L5 y", "L5 z", "L3 x", "L3 y", "L3 z",
        "T12 x", "T12 y", "T12 z", "T8 x", "T8 y", "T8 z", "Neck x", "Neck y", "Neck z",
        "Head x", "Head y", "Head z", "Right Shoulder x", "Right Shoulder y", "Right Shoulder z",
        "Right Upper Arm x", "Right Upper Arm y", "Right Upper Arm z", "Right Forearm x", "Right Forearm y", "Right Forearm z",
        "Right Hand x", "Right Hand y", "Right Hand z", "Left Shoulder x", "Left Shoulder y", "Left Shoulder z",
        "Left Upper Arm x", "Left Upper Arm y", "Left Upper Arm z", "Left Forearm x", "Left Forearm y", "Left Forearm z",
        "Left Hand x", "Left Hand y", "Left Hand z", "Right Upper Leg x", "Right Upper Leg y", "Right Upper Leg z",
        "Right Lower Leg x", "Right Lower Leg y", "Right Lower Leg z", "Right Foot x", "Right Foot y", "Right Foot z",
        "Right Toe x", "Right Toe y", "Right Toe z", "Left Upper Leg x", "Left Upper Leg y", "Left Upper Leg z",
        "Left Lower Leg x", "Left Lower Leg y", "Left Lower Leg z", "Left Foot x", "Left Foot y", "Left Foot z",
        "Left Toe x", "Left Toe y", "Left Toe z"
    ],
    "Segment Acceleration": [
        "Pelvis x", "Pelvis y", "Pelvis z", "L5 x", "L5 y", "L5 z", "L3 x", "L3 y", "L3 z",
        "T12 x", "T12 y", "T12 z", "T8 x", "T8 y", "T8 z", "Neck x", "Neck y", "Neck z",
        "Head x", "Head y", "Head z", "Right Shoulder x", "Right Shoulder y", "Right Shoulder z",
        "Right Upper Arm x", "Right Upper Arm y", "Right Upper Arm z", "Right Forearm x", "Right Forearm y", "Right Forearm z",
        "Right Hand x", "Right Hand y", "Right Hand z", "Left Shoulder x", "Left Shoulder y", "Left Shoulder z",
        "Left Upper Arm x", "Left Upper Arm y", "Left Upper Arm z", "Left Forearm x", "Left Forearm y", "Left Forearm z",
        "Left Hand x", "Left Hand y", "Left Hand z", "Right Upper Leg x", "Right Upper Leg y", "Right Upper Leg z",
        "Right Lower Leg x", "Right Lower Leg y", "Right Lower Leg z", "Right Foot x", "Right Foot y", "Right Foot z",
        "Right Toe x", "Right Toe y", "Right Toe z", "Left Upper Leg x", "Left Upper Leg y", "Left Upper Leg z",
        "Left Lower Leg x", "Left Lower Leg y", "Left Lower Leg z", "Left Foot x", "Left Foot y", "Left Foot z",
        "Left Toe x", "Left Toe y", "Left Toe z"
    ],
    "Segment Angular Velocity": [
        "Pelvis x", "Pelvis y", "Pelvis z", "L5 x", "L5 y", "L5 z", "L3 x", "L3 y", "L3 z",
        "T12 x", "T12 y", "T12 z", "T8 x", "T8 y", "T8 z", "Neck x", "Neck y", "Neck z",
        "Head x", "Head y", "Head z", "Right Shoulder x", "Right Shoulder y", "Right Shoulder z",
        "Right Upper Arm x", "Right Upper Arm y", "Right Upper Arm z", "Right Forearm x", "Right Forearm y", "Right Forearm z",
        "Right Hand x", "Right Hand y", "Right Hand z", "Left Shoulder x", "Left Shoulder y", "Left Shoulder z",
        "Left Upper Arm x", "Left Upper Arm y", "Left Upper Arm z", "Left Forearm x", "Left Forearm y", "Left Forearm z",
        "Left Hand x", "Left Hand y", "Left Hand z", "Right Upper Leg x", "Right Upper Leg y", "Right Upper Leg z",
        "Right Lower Leg x", "Right Lower Leg y", "Right Lower Leg z", "Right Foot x", "Right Foot y", "Right Foot z",
        "Right Toe x", "Right Toe y", "Right Toe z", "Left Upper Leg x", "Left Upper Leg y", "Left Upper Leg z",
        "Left Lower Leg x", "Left Lower Leg y", "Left Lower Leg z", "Left Foot x", "Left Foot y", "Left Foot z",
        "Left Toe x", "Left Toe y", "Left Toe z"
    ],
    "Segment Angular Acceleration": [
        "Pelvis x", "Pelvis y", "Pelvis z", "L5 x", "L5 y", "L5 z", "L3 x", "L3 y", "L3 z",
        "T12 x", "T12 y", "T12 z", "T8 x", "T8 y", "T8 z", "Neck x", "Neck y", "Neck z",
        "Head x", "Head y", "Head z", "Right Shoulder x", "Right Shoulder y", "Right Shoulder z",
        "Right Upper Arm x", "Right Upper Arm y", "Right Upper Arm z", "Right Forearm x", "Right Forearm y", "Right Forearm z",
        "Right Hand x", "Right Hand y", "Right Hand z", "Left Shoulder x", "Left Shoulder y", "Left Shoulder z",
        "Left Upper Arm x", "Left Upper Arm y", "Left Upper Arm z", "Left Forearm x", "Left Forearm y", "Left Forearm z",
        "Left Hand x", "Left Hand y", "Left Hand z", "Right Upper Leg x", "Right Upper Leg y", "Right Upper Leg z",
        "Right Lower Leg x", "Right Lower Leg y", "Right Lower Leg z", "Right Foot x", "Right Foot y", "Right Foot z",
        "Right Toe x", "Right Toe y", "Right Toe z", "Left Upper Leg x", "Left Upper Leg y", "Left Upper Leg z",
        "Left Lower Leg x", "Left Lower Leg y", "Left Lower Leg z", "Left Foot x", "Left Foot y", "Left Foot z",
        "Left Toe x", "Left Toe y", "Left Toe z"
    ],
    "Joint Angles ZXY" : [
        "L5S1 Lateral Bending", "L5S1 Axial Bending", "L5S1 Flexion/Extension",
        "L4L3 Lateral Bending", "L4L3 Axial Rotation", "L4L3 Flexion/Extension",
        "L1T12 Lateral Bending", "L1T12 Axial Rotation", "L1T12 Flexion/Extension",
        "T9T8 Lateral Bending", "T9T8 Axial Rotation", "T9T8 Flexion/Extension",
        "T1C7 Lateral Bending", "T1C7 Axial Rotation", "T1C7 Flexion/Extension",
        "C1 Head Lateral Bending", "C1 Head Axial Rotation", "C1 Head Flexion/Extension",
        "Right T4 Shoulder Abduction/Adduction", "Right T4 Shoulder Internal/External Rotation", "Right T4 Shoulder Flexion/Extension",
        "Right Shoulder Abduction/Adduction", "Right Shoulder Internal/External Rotation", "Right Shoulder Flexion/Extension",
        "Right Elbow Ulnar Deviation/Radial Deviation", "Right Elbow Pronation/Supination", "Right Elbow Flexion/Extension",
        "Right Wrist Ulnar Deviation/Radial Deviation", "Right Wrist Pronation/Supination", "Right Wrist Flexion/Extension",
        "Left T4 Shoulder Abduction/Adduction", "Left T4 Shoulder Internal/External Rotation", "Left T4 Shoulder Flexion/Extension",
        "Left Shoulder Abduction/Adduction", "Left Shoulder Internal/External Rotation", "Left Shoulder Flexion/Extension",
        "Left Elbow Ulnar Deviation/Radial Deviation", "Left Elbow Pronation/Supination", "Left Elbow Flexion/Extension",
        "Left Wrist Ulnar Deviation/Radial Deviation", "Left Wrist Pronation/Supination", "Left Wrist Flexion/Extension",
        "Right Hip Abduction/Adduction", "Right Hip Internal/External Rotation", "Right Hip Flexion/Extension",
        "Right Knee Abduction/Adduction", "Right Knee Internal/External Rotation", "Right Knee Flexion/Extension",
        "Right Ankle Abduction/Adduction", "Right Ankle Internal/External Rotation", "Right Ankle Dorsiflexion/Plantarflexion",
        "Right Ball Foot Abduction/Adduction", "Right Ball Foot Internal/External Rotation", "Right Ball Foot Flexion/Extension",
        "Left Hip Abduction/Adduction", "Left Hip Internal/External Rotation", "Left Hip Flexion/Extension",
        "Left Knee Abduction/Adduction", "Left Knee Internal/External Rotation", "Left Knee Flexion/Extension",
        "Left Ankle Abduction/Adduction", "Left Ankle Internal/External Rotation", "Left Ankle Dorsiflexion/Plantarflexion",
        "Left Ball Foot Abduction/Adduction", "Left Ball Foot Internal/External Rotation", "Left Ball Foot Flexion/Extension"
    ],
    "Joint Angles XZY": [
        "L5S1 Lateral Bending", "L5S1 Axial Bending", "L5S1 Flexion/Extension",
        "L4L3 Lateral Bending", "L4L3 Axial Rotation", "L4L3 Flexion/Extension",
        "L1T12 Lateral Bending", "L1T12 Axial Rotation", "L1T12 Flexion/Extension",
        "T9T8 Lateral Bending", "T9T8 Axial Rotation", "T9T8 Flexion/Extension",
        "T1C7 Lateral Bending", "T1C7 Axial Rotation", "T1C7 Flexion/Extension",
        "C1 Head Lateral Bending", "C1 Head Axial Rotation", "C1 Head Flexion/Extension",
        "Right T4 Shoulder Abduction/Adduction", "Right T4 Shoulder Internal/External Rotation", "Right T4 Shoulder Flexion/Extension",
        "Right Shoulder Abduction/Adduction", "Right Shoulder Internal/External Rotation", "Right Shoulder Flexion/Extension",
        "Right Elbow Ulnar Deviation/Radial Deviation", "Right Elbow Pronation/Supination", "Right Elbow Flexion/Extension",
        "Right Wrist Ulnar Deviation/Radial Deviation", "Right Wrist Pronation/Supination", "Right Wrist Flexion/Extension",
        "Left T4 Shoulder Abduction/Adduction", "Left T4 Shoulder Internal/External Rotation", "Left T4 Shoulder Flexion/Extension",
        "Left Shoulder Abduction/Adduction", "Left Shoulder Internal/External Rotation", "Left Shoulder Flexion/Extension",
        "Left Elbow Ulnar Deviation/Radial Deviation", "Left Elbow Pronation/Supination", "Left Elbow Flexion/Extension",
        "Left Wrist Ulnar Deviation/Radial Deviation", "Left Wrist Pronation/Supination", "Left Wrist Flexion/Extension",
        "Right Hip Abduction/Adduction", "Right Hip Internal/External Rotation", "Right Hip Flexion/Extension",
        "Right Knee Abduction/Adduction", "Right Knee Internal/External Rotation", "Right Knee Flexion/Extension",
        "Right Ankle Abduction/Adduction", "Right Ankle Internal/External Rotation", "Right Ankle Dorsiflexion/Plantarflexion",
        "Right Ball Foot Abduction/Adduction", "Right Ball Foot Internal/External Rotation", "Right Ball Foot Flexion/Extension",
        "Left Hip Abduction/Adduction", "Left Hip Internal/External Rotation", "Left Hip Flexion/Extension",
        "Left Knee Abduction/Adduction", "Left Knee Internal/External Rotation", "Left Knee Flexion/Extension",
        "Left Ankle Abduction/Adduction", "Left Ankle Internal/External Rotation", "Left Ankle Dorsiflexion/Plantarflexion",
        "Left Ball Foot Abduction/Adduction", "Left Ball Foot Internal/External Rotation", "Left Ball Foot Flexion/Extension"
    ],
    'Ergonomic Joint Angles ZXY': [
        "T8_Head Lateral Bending", "T8_Head Axial Bending", "T8_Head Flexion/Extension",
        "T8_LeftUpperArm Lateral Bending", "T8_LeftUpperArm Axial Bending", "T8_LeftUpperArm Flexion/Extension",
        "T8_RightUpperArm Lateral Bending", "T8_RightUpperArm Axial Bending", "T8_RightUpperArm Flexion/Extension",
        "Pelvis_T8 Lateral Bending", "Pelvis_T8 Axial Bending", "Pelvis_T8 Flexion/Extension",
        "Vertical_Pelvis Lateral Bending", "Vertical_Pelvis Axial Bending", "Vertical_Pelvis Flexion/Extension",
        "Vertical_T8 Lateral Bending", "Vertical_T8 Axial Bending", "Vertical_T8 Flexion/Extension"
    ],
    'Ergonomic Joint Angles XZY': [
        "T8_Head Lateral Bending", "T8_Head Axial Bending", "T8_Head Flexion/Extension",
        "T8_LeftUpperArm Lateral Bending", "T8_LeftUpperArm Axial Bending", "T8_LeftUpperArm Flexion/Extension",
        "T8_RightUpperArm Lateral Bending", "T8_RightUpperArm Axial Bending", "T8_RightUpperArm Flexion/Extension",
        "Pelvis_T8 Lateral Bending", "Pelvis_T8 Axial Bending", "Pelvis_T8 Flexion/Extension",
        "Vertical_Pelvis Lateral Bending", "Vertical_Pelvis Axial Bending", "Vertical_Pelvis Flexion/Extension",
        "Vertical_T8 Lateral Bending", "Vertical_T8 Axial Bending", "Vertical_T8 Flexion/Extension"
    ],
    "Center of Mass": [
        "CoM pos x", "CoM pos y", "CoM pos z",
        "CoM vel x", "CoM vel y", "CoM vel z",
        "CoM acc x", "CoM acc y", "CoM acc z"
    ]
    
}