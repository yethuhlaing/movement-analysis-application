import tkinter as tk
from tkinter import ttk, font, filedialog
import pandas as pd
COLOR = '#%02x%02x%02x' % (174, 239, 206)

class TimeSliderWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.frames_in_seconds = 0  # Default value, to be set later

        self.label = ttk.Label(self, text="Select Starting Time:")
        self.label.grid(row=0, column=0, columnspan=2)

        self.slider = ttk.Scale(self, from_=0, to=self.frames_in_seconds, orient="horizontal", length=200)
        self.slider.grid(row=1, column=0, columnspan=2)

        self.result_label = ttk.Label(self, text="Selected Time: 0 seconds")
        self.result_label.grid(row=2, column=0, columnspan=2)

        self.slider.bind("<Motion>", self.update_selected_time)

    def set_frames_in_seconds(self, frames_in_seconds):
        self.frames_in_seconds = frames_in_seconds
        self.slider.config(to=frames_in_seconds)

    def update_selected_time(self, event):
        selected_time = self.slider.get()
        self.result_label.config(text=f"Selected Time: {selected_time:.2f} seconds")

class ExcelFileInputWidget(tk.Label):
    def __init__(self, parent, time_slider_widget):
        super().__init__(parent, text="Click to select Excel files.", bg="white")
        self.default_bg = "white"
        self.configure(cursor="hand2")
        self.time_slider_widget = time_slider_widget  # Reference to TimeSliderWidget
        self.bind("<Button-1>", self.select_file)
        self.frame_count = None
        self.frame_rate = None
        self.file_path = None

    def select_file(self, event):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            self.configure(bg="green")  # Change background color to green
            trimmed_filename = file_path.rstrip('/').split('/')[-1]
            self["text"] = trimmed_filename
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
            self.file_path = file_path
            # Set frames_in_seconds value in the TimeSliderWidget
            frames_in_seconds = self.frame_count / self.frame_rate
            self.time_slider_widget.set_frames_in_seconds(frames_in_seconds)
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None, None

    
class ProjectCreation(ttk.Frame):
    def __init__(self, parent, project_name,project_creator):
        tk.Frame.__init__(self, parent, bg="white")
        self.project_name = project_name
        self.project_creator = project_creator
        self.data = []
        self.create_widgets()
        self.pack(expand=True, fill="both")

    def create_widgets(self):
    # GENERAL FRAME
        general_frame = ttk.LabelFrame(self, text="General", padding=(10, 10))
        general_frame.grid(row=0, column=3, padx=50, pady=30, sticky='nsew', rowspan=3, columnspan=2)

        # Heading "Duration" with a dropbox
        duration_label = tk.Label(general_frame, text="Duration", font=font.Font(size=12), pady=5)
        duration_label.grid(row=1, column=0, sticky='w')
        
        duration_options = ["1 hour", "2 hours", "3 hours"]
        self.duration_var = tk.StringVar(value=duration_options[0])
        duration_dropdown = ttk.Combobox(general_frame, textvariable=self.duration_var, values=duration_options, state="readonly", width=20)
        duration_dropdown.grid(row=1, column=1, sticky='w')

        # TIME SLIDER for starting time
        time_slider_widget = TimeSliderWidget(general_frame)
        time_slider_widget.grid(row=2, column=0, columnspan=2, sticky='w')

    #CREATION FRAME
        creation_frame = ttk.LabelFrame(self, padding=(10, 10))
        creation_frame.grid(row=0, column=0, padx=50, pady=30, sticky='nsew', rowspan=3, columnspan=2)
        title_font = font.Font(size=24)
        creation_title = ttk.Label(creation_frame, text=f"{self.project_name} by {self.project_creator}", font=title_font)
        creation_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))  # Adding some vertical padding

        # Asks for scenario name
        scenario_name_label = tk.Label(creation_frame, text="Scenario Name", font=font.Font(size=12), pady=5)
        scenario_name_label.grid(row=1, column=0, sticky='w')
        self.scenario_name_var = tk.StringVar(value="")
        scenario_name_entry = ttk.Entry(creation_frame, textvariable=self.scenario_name_var, width=20)
        scenario_name_entry.grid(row=1, column=1, sticky='w')

        # File drop widget
        refrence_excel_label = ttk.Label(creation_frame, text="Reference Excel", font=font.Font(size=12))
        refrence_excel_label.grid(row=2, column=0, sticky='w')
        self.refrence_excel_widget = ExcelFileInputWidget(creation_frame, time_slider_widget)
        self.refrence_excel_widget.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        # Create a LabelFrame to group the checkboxes
        checkbox_frame = ttk.LabelFrame(creation_frame, text="Choose the category to examine", padding=(10, 10))
        checkbox_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # List of options with checkboxes
        options = [
            "Segment Angular Velocity",
            "Segment Orientation - Quat",
            "Segment Orientation - Euler",
            "Segment Position",
            "Ergonomic Joint Angles ZXY",
            "Center of Mass",
            "Sensor Free Acceleration",
            "Segment Velocity",
            "Segment Acceleration",
            "Joint Angles XZY",
            "Joint Angles ZXY",
            "Sensor Orientation - Quat",
            "Sensor Orientation - Euler",
            "Sensor Magnetic Field"
        ]

        # Create a dictionary to store the BooleanVar instances for each category
        self.check_var_dict = {}

        # Create the checkboxes with corresponding BooleanVar instances
        for idx, option in enumerate(options):
            var = tk.BooleanVar(value=True)  # Default checkboxes to active
            self.check_var_dict[option] = var
            checkbox = tk.Checkbutton(checkbox_frame, text=option, variable=var, bg="white", anchor='w')
            checkbox.grid(row=idx // 2, column=idx % 2, sticky='w')
        # Confirm button for check boxes
        # Confirm button for check boxes (you can add it here)
        confirm_button = ttk.Button(creation_frame, text="Confirm") # command=function call to the column thing
        confirm_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))  # Adding some vertical padding

    #GRAPH FRAME
        graph_frame = ttk.LabelFrame(self, text="Graphical Visualization", padding=(10, 10))
        graph_frame.grid(row=1, column=3, padx=50, pady=30, sticky='nsew', columnspan=2)

        # Choosing Graph type
        graph_label = tk.Label(graph_frame, text="Graph Type", font=font.Font(size=12), pady=5)
        graph_label.grid(row=0, column=0, sticky='w')
        graph_options = ["Single Graph", "Double Graph"]
        self.graph_var = tk.StringVar(value=graph_options[0])
        graph_dropdown = ttk.Combobox(graph_frame, textvariable=self.graph_var, values=graph_options, state="readonly", width=20)
        graph_dropdown.grid(row=0, column=1, sticky='w')

    # STUDENT FRAME
        student_frame = ttk.LabelFrame(self, text="Student Information", padding=(10, 10))
        student_frame.grid(row=3, column=3, padx=50, pady=30, sticky='nsew', columnspan=2)

        # Student name
        student_name_label = tk.Label(student_frame, text="Name", font=font.Font(size=12), pady=5)
        student_name_label.grid(row=0, column=0, sticky='w')

        self.student_name_var = tk.StringVar(value="")
        student_name_entry = ttk.Entry(student_frame, textvariable=self.student_name_var, width=20)
        student_name_entry.grid(row=0, column=1, sticky='w')

        # Student height
        height_label = tk.Label(student_frame, text="Height", font=font.Font(size=12), pady=5)
        height_label.grid(row=1, column=0, sticky='w')

        self.height_var = tk.StringVar(value="")
        height_entry = ttk.Entry(student_frame, textvariable=self.height_var, width=20)
        height_entry.grid(row=1, column=1, sticky='w')

        # Student weight
        weight_label = tk.Label(student_frame, text="Weight", font=font.Font(size=12), pady=5)
        weight_label.grid(row=2, column=0, sticky='w')

        self.weight_var = tk.StringVar(value="")
        weight_entry = ttk.Entry(student_frame, textvariable=self.weight_var, width=20)
        weight_entry.grid(row=2, column=1, sticky='w')

        # STUDENT EXCEL WIDGET HERE
        # STUDENT EXCEL WIDGET HERE
        # STUDENT EXCEL WIDGET HERE

        start_button = tk.Button(self, text="Analyze", bg=COLOR, bd=0, width=20, padx=20,
                                 command=lambda: self.on_start_button_click())
        start_button.grid(row=4, column=1, columnspan=2, pady=20)

    def on_start_button_click(self):
        # Gets selected checkboxes for sheet names
        chosen_sheets = [option for option, var in self.check_var_dict.items() if var.get()]
        input_dict = { 
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
                "category": chosen_sheets,
                "movement": ["L5S1 Flexion/Extension",  ], #Implement reading function
                "scenerio": [self.scenario_name_var.get()], #Idk why this is an array
                "duration": self.refrence_excel_widget.frame_count,
                "starting_time": 0.2,                      #Implement
                "Graph_type": self.graph_var.get(),
                "ref_name": "kati",               
                "ref_file": self.refrence_excel_widget.file_path,
                "student_name": self.student_name_var.get(),
                "student_file": "../../data/Student downsampled data/simulator riding/Sudent1-003Harju ext walk.xlsx"
            }
        }
        print(input_dict)
        # Switch to the DataVisualization page and pass the data array
        self.master.show_visualize_data(input_dict)

