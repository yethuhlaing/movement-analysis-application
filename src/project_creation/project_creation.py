import tkinter as tk
from tkinter import ttk, font, filedialog
from data import *
import pandas as pd
from data import *
COLOR = '#%02x%02x%02x' % (174, 239, 206)

class TimeSliderWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent,background="white")
        self.frames_in_seconds = 0  # Default value, to be set later
        self.label = ttk.Label(self, text="Select Starting Time:", background="white")
        self.label.grid(row=0, column=0, columnspan=2)

        self.slider = ttk.Scale(self, from_=0, to=self.frames_in_seconds, orient="horizontal", length=200)
        self.slider.grid(row=1, column=0, columnspan=2)

        self.result_label = ttk.Label(self, text="Selected Time: 0 seconds", background="white")
        self.result_label.grid(row=2, column=0, columnspan=2) 

        self.slider.bind("<Motion>", self.update_selected_time)

    def set_frames_in_seconds(self, frames_in_seconds):
        self.frames_in_seconds = frames_in_seconds
        self.slider.config(to=frames_in_seconds)

    def update_selected_time(self, event):
        selected_time = int(self.slider.get())
        self.result_label.config(text=f"Selected Time: {selected_time:.2f} seconds")

class ExcelFileInputWidget(tk.Button):
    def __init__(self, parent, time_slider_widget, data_type):
        super().__init__(parent, text="Click to select an Excel", bg=COLOR, borderwidth=0, width= 30,padx=30, pady=5)
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


class SpreadsheetPopup(tk.Toplevel):
    def __init__(self, parent, spreadsheet_data):
        super().__init__(parent)
        self.parent = parent
        self.spreadsheet_data = spreadsheet_data
        self.selected_columns = {}  # Store excluded columns for each tab

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        for sheet_name, columns in spreadsheet_data.items():
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text=sheet_name)
            
            listbox = tk.Listbox(tab_frame, selectmode=tk.MULTIPLE)
            listbox.pack(fill="both", expand=True)
            
            for column in columns:
                listbox.insert(tk.END, column)
            
            # Store the listbox for each tab along with its selected indices
            self.selected_columns[sheet_name] = {
                'listbox': listbox,
                'selected_indices': []
            }
        
        finish_selection_button = ttk.Button(self, text="Finish Selection", command=self.finish_selection)
        finish_selection_button.pack(pady=10)
        
        confirm_columns_button = ttk.Button(self, text="Confirm Columns", command=self.confirm_columns)
        confirm_columns_button.pack(pady=5)
        
        # Bind tab changes to update the selection on the listboxes
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
    def on_tab_change(self, event):
        # Get the current tab's sheet name
        current_tab_index = self.notebook.index(self.notebook.select())
        current_sheet_name = list(self.spreadsheet_data.keys())[current_tab_index]
        
        # Restore the selection for the current tab
        if current_sheet_name in self.selected_columns:
            selected_indices = self.selected_columns[current_sheet_name]['selected_indices']
            listbox = self.selected_columns[current_sheet_name]['listbox']
            listbox.selection_clear(0, tk.END)
            for idx in selected_indices:
                listbox.selection_set(idx)
        
    def finish_selection(self):
        current_tab_index = self.notebook.index(self.notebook.select())
        current_sheet_name = list(self.spreadsheet_data.keys())[current_tab_index]
        listbox = self.selected_columns[current_sheet_name]['listbox']
        selected_indices = listbox.curselection()
        self.selected_columns[current_sheet_name]['selected_indices'] = selected_indices
        print("Finished selecting columns for:", current_sheet_name)
        
    def confirm_columns(self):    
        chosen_columns = {}    
        for sheet_name in self.spreadsheet_data.keys():    
            listbox = self.selected_columns[sheet_name]['listbox']    
            selected_indices = self.selected_columns[sheet_name]['selected_indices']    
            selected_columns = [listbox.get(idx) for idx in selected_indices]    
            chosen_columns[sheet_name] = selected_columns    
        print(chosen_columns)    
        self.parent.on_confirm_columns(chosen_columns)
        self.destroy()

class ProjectCreation(ttk.Frame):
    def __init__(self, parent, project_name,project_creator):
        tk.Frame.__init__(self, parent, bg="white")
        self.project_name = project_name
        self.project_creator = project_creator
        self.data = []
        self.spreadsheet_tabs = {}
        self.create_widgets()
        self.pack(expand=True, fill="both")


    def create_widgets(self):
        self.button_font = font.Font(family="Bookman Old Style", size=11)
        self.text_font = font.Font(family="Bookman Old Style", size=11)
        self.heading_font = font.Font(family="Bookman Old Style", size=15, weight="bold")
        style = ttk.Style()
        style.configure("Custom.TLabelframe", background="white", font=("Bookman Old Style", 20))
        style.configure("TLabelFrame.Label", background="white", font=("Bookman Old Style", 20))

        # Divided Two Frame
        leftFrame = tk.Frame(self, background="red")
        rightFrame = tk.Frame(self, background="white", padx=30)

        leftFrame.grid(row=0, column=0, sticky="nsew")
        rightFrame.grid(row=0, column=1, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        self.create_right_frame(rightFrame)
        self.create_left_frame(leftFrame)

    def create_left_frame(self, leftFrame):
        # Configure grid weights to center the parent frame
        leftFrame.grid_rowconfigure(0, weight=1)
        leftFrame.grid_columnconfigure(0, weight=1)

        # Create a frame for the projectInfoFrame 
        projectInfoFrame = tk.Frame(leftFrame, borderwidth=2, relief="solid")
        projectInfoFrame.grid(row=0, column=0, padx=10,  sticky="nswe")

        # Create a frame for the categoryChoosingFrame
        categoryChoosingFrame = tk.Frame(leftFrame, borderwidth=2, relief="solid")
        categoryChoosingFrame.grid(row=1, column=0, padx=10,  sticky="nswe")

        # Configure grid weights to allow vertical expansion
        leftFrame.grid_rowconfigure(0, weight=1)
        leftFrame.grid_rowconfigure(1, weight=1)


        # Project Information Frame


        projectNameFrame = tk.Frame(projectInfoFrame, bg="white")
        projectNameFrame.pack()
        projectNameLabel = tk.Label(projectNameFrame, text="Project Name - ", font=self.heading_font, pady=5, padx= 10)
        projectNameLabel.pack(side="left")
        projectName = tk.Label(projectNameFrame, text=self.project_name, font=self.heading_font, pady=5)
        projectName.pack(side="left")

        projectCreatorFrame = tk.Frame(projectInfoFrame, bg="white")
        projectCreatorFrame.pack()
        projectCreatorLabel = tk.Label(projectCreatorFrame, text="Project Creator - ", font=self.heading_font, pady=5, padx= 10)
        projectCreatorLabel.pack(side="left")
        projectCreator = tk.Label(projectCreatorFrame, text=self.project_creator, font=self.heading_font, pady=5)
        projectCreator.pack(side="left")

        scenarioFrame = tk.Frame(projectInfoFrame, bg="white")
        scenarioFrame.pack()
        scenario_name_label = tk.Label(scenarioFrame, text="Scenario Name", font=self.text_font, pady=5, padx=10)
        scenario_name_label.pack(side="left")
        self.scenario_name_var = tk.StringVar(value="")
        scenario_name_entry = ttk.Entry(scenarioFrame, textvariable=self.scenario_name_var, width=20)
        scenario_name_entry.pack(side="left")

        referenceFrame = tk.Frame(projectInfoFrame, bg="white")
        referenceFrame.pack()
        refrence_name_label = tk.Label(referenceFrame, text="Refrence name", font=self.text_font, pady=5, padx=10)
        refrence_name_label.pack(side="left")
        self.refrence_name_var = tk.StringVar(value="")
        refrence_name_entry = ttk.Entry(referenceFrame, textvariable=self.refrence_name_var, width=20)
        refrence_name_entry.pack(side="left")

        studentFrame = tk.Frame(projectInfoFrame, bg="white")
        studentFrame.pack()
        student_name_label = tk.Label(studentFrame, text="Student name", font=self.text_font, pady=5, padx=10)
        student_name_label.pack(side="left")
        self.student_name_var = tk.StringVar(value="")
        student_name_entry = ttk.Entry(studentFrame, textvariable=self.student_name_var, width=20)
        student_name_entry.pack(side="left")

        refrenceExcelFrame = tk.Frame(projectInfoFrame, bg="white")
        refrenceExcelFrame.pack()
        refrence_excel_label = tk.Label(refrenceExcelFrame, text="Reference Excel", font=self.text_font)
        refrence_excel_label.pack(side="left")
        self.refrence_excel_widget = ExcelFileInputWidget(refrenceExcelFrame, self.time_slider_widget, "reference")
        self.refrence_excel_widget.pack(side="left")

        studentExcelFrame = tk.Frame(projectInfoFrame, bg="white")
        studentExcelFrame.pack()
        student_excel_label = tk.Label(studentExcelFrame, text="Student Excel", font=self.text_font)
        student_excel_label.pack(side="left")
        self.student_excel_widget = ExcelFileInputWidget(studentExcelFrame, self.time_slider_widget, "student")
        self.student_excel_widget.pack(side="left")

        heightFrame = tk.Frame(projectInfoFrame, bg="white")
        heightFrame.pack()
        height_label = tk.Label(heightFrame, text="Height(cm)", font=self.text_font, pady=5, padx=10)
        height_label.pack(side="left")
        self.height_var = tk.StringVar(value="")
        height_entry = ttk.Entry(heightFrame, textvariable=self.height_var, width=20)
        height_entry.pack(side="left")

        weightFrame = tk.Frame(projectInfoFrame, bg="white")
        weightFrame.pack()
        weight_label = tk.Label(weightFrame, text="Weight(kg)", font=self.text_font, pady=5, padx=10)
        weight_label.pack(side="left")
        self.weight_var = tk.StringVar(value="")
        weight_entry = ttk.Entry(weightFrame, textvariable=self.weight_var, width=20)
        weight_entry.pack(side="left")



        # CategoryChoosing Frame
        
        checkboxFrame = ttk.Labelframe(categoryChoosingFrame,text="Choose the category to examine" )
        checkboxFrame.pack()
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
        
        # Create and place checkboxes in two columns
        for i, option in enumerate(options):
            var = tk.BooleanVar(value=True)
            self.check_var_dict[option] = var
            checkbox = ttk.Checkbutton(checkboxFrame, text=option, variable=var)
            if i < len(options) // 2:
                # Place in the left column
                checkbox.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            else:
                # Place in the right column
                checkbox.grid(row=i - len(options) // 2, column=1, sticky="w", padx=10, pady=5)

        # # Create the checkboxes
        # for idx, option in enumerate(options):
        #     var = tk.BooleanVar(value=True)  # Default checkboxes to active
        #     self.check_var_dict[option] = var
        #     checkbox = tk.Checkbutton(checkboxFrame, text=option, variable=var, bg="white", anchor='w')
        #     checkbox.pack()

        # Confirm button
        confirm_button = ttk.Button(categoryChoosingFrame, text="Confirm", command=self.on_confirm)
        confirm_button.pack()

        categoryChoosingFrame.grid(row=1, column=0, padx=10, pady=10)









    def create_right_frame(self, rightFrame):


    # GENERAL FRAME
        sliderFrame = tk.Frame(rightFrame)
        self.time_slider_widget = TimeSliderWidget(sliderFrame)
        self.time_slider_widget.pack(side="left")
        sliderFrame.pack(fill="x")
        # Heading "Duration" with a dropbox
        durationFrame = tk.Frame(rightFrame, bg="white")
        duration_label = tk.Label(durationFrame, text="Duration", font=self.text_font, bg="white", padx=10, pady=5)
        duration_label.pack(side="left")
        self.duration_var = tk.IntVar(value=0)
        duration_entry = ttk.Entry(durationFrame, textvariable=self.duration_var, width=20)
        duration_entry.pack(side="left")
        durationFrame.pack(fill="x")

        graphFrame = tk.Frame(rightFrame, bg="white")
        # Choosing Graph type
        graph_label = tk.Label(graphFrame, text="Graph Type", font=self.text_font, padx=10, pady=5)
        graph_label.pack(side="left")
        graph_options = ["Single Graph", "Double Graph"]
        self.graph_var = tk.StringVar(value=graph_options[0])
        graph_dropdown = ttk.Combobox(graphFrame, textvariable=self.graph_var, font=self.text_font, values=graph_options, state="readonly", width=20)
        graph_dropdown.pack(side="left")
        graphFrame.pack(fill="x")


        start_button = tk.Button(rightFrame, text="Analyze", bg=COLOR, bd=0, width=20, padx=20,
                                 command=lambda: self.on_start_button_click())
        start_button.pack(anchor="n")
    def on_confirm_columns(self, chosen_columns):
        self.chosen_columns = chosen_columns
        return None

    def on_confirm(self):
        chosen_sheets = [option for option, var in self.check_var_dict.items() if var.get()]
        spreadsheet_data = {}
        
        # Load data and extract column names for each chosen sheet
        for sheet_name in chosen_sheets:
            try:
                df = pd.read_excel(self.refrence_excel_widget.file_path, engine='openpyxl', sheet_name=sheet_name)
                columns = df.columns.tolist()[1:]
                spreadsheet_data[sheet_name] = columns
            except Exception as e:
                print(f"Error loading sheet '{sheet_name}': {e}")
        # Call the popup dialog
        popup = SpreadsheetPopup(self, spreadsheet_data)

    def on_start_button_click(self):
        # Gets selected checkboxes for sheet names
        chosen_sheets = [option for option, var in self.check_var_dict.items() if var.get()]
        user_data = { 
            "headingData" : {
                "project_name": self.project_name,
                "project_creator": self.project_creator
            },
            "informationData": {
                "height": int(self.height_var.get()),
                "weight" : int(self.weight_var.get()),
                "student_name": self.student_name_var.get()
            } ,
            "visualizationData": {
                "categories": self.chosen_columns,
                "scenerio": [self.scenario_name_var.get()],
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
        setUserData(user_data)
        x = getUserData()
        print(x)
        # Switch to the DataVisualization page and pass the data array
        self.master.show_visualize_data()