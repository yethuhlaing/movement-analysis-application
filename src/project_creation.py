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
    def __init__(self, parent, time_slider_widget, data_type):
        super().__init__(parent, text="Click to select Excel files.", bg="white")
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
            self.configure(bg="green")  # Change background color to green
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
            frames_in_seconds = self.frame_count / self.frame_rate
            self.time_slider_widget.set_frames_in_seconds(frames_in_seconds)
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
        self.selected_columns = {}  # Store selected columns for each tab
        
        self.title("Choose columns to exclude")
        self.geometry("400x300")

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
        heading_font = font.Font(family="Bookman Old Style", size=20, weight="bold")
        text_font = font.Font(family="Bookman Old Style", size=10)
        #This prevents elements going on columns
        empty_label_2 = tk.Label(self,text="AAAAAAAAAAAAaaaaaaaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",foreground="white",background="white")
        empty_label_2.grid(row=1, column=3, sticky='nsew')
    # GENERAL FRAME
        general_frame = ttk.LabelFrame(self, text="General", padding=(10, 10))
        general_frame.grid(row=1, column=4, padx=20, pady=20, sticky='nswe', columnspan=2)
        general_title = tk.Label(general_frame,text="General",font=heading_font, padx=20, justify="left", pady=20, background='white')
        general_title.grid(row=0, column=0, sticky='w')

        # Scenario Name
        scenario_name_label = tk.Label(general_frame, text="Scenario Name", font=text_font, pady=5)
        scenario_name_label.grid(row=1, column=0, sticky='w')

        self.scenario_name_var = tk.StringVar(value="")
        scenario_name_entry = ttk.Entry(general_frame, textvariable=self.scenario_name_var, width=20)
        scenario_name_entry.grid(row=1, column=1, sticky='w')

        # Heading "Duration" with a dropbox
        duration_label = tk.Label(general_frame, text="Duration", font=text_font, pady=5)
        duration_label.grid(row=2, column=0, sticky='w')

        duration_options = ["1 hour", "2 hours", "3 hours"]
        self.duration_var = tk.StringVar(value=duration_options[0])
        duration_dropdown = ttk.Combobox(general_frame, textvariable=self.duration_var, values=duration_options, state="readonly", width=20)
        duration_dropdown.grid(row=2, column=1, sticky='w')

        # TIME SLIDER for starting time
        time_slider_widget = TimeSliderWidget(general_frame)
        time_slider_widget.grid(row=3, column=0, columnspan=2, pady=10, sticky='w')

    # GRAPH FRAME
        graph_frame = ttk.LabelFrame(self, text="Graphical Visualization", padding=(10, 10))
        graph_frame.grid(row=6, column=4, padx=20, pady=20, sticky='nswe', columnspan=2)
        graph_title = tk.Label(graph_frame,text="Graphical Visualization",font=heading_font, padx=20, justify="left", pady=20, background='white')
        graph_title.grid(row=0, column=0, sticky='w')

        # Choosing Graph type
        graph_label = tk.Label(graph_frame, text="Graph Type", font=text_font, pady=5)
        graph_label.grid(row=1, column=0, sticky='w')

        graph_options = ["Single Graph", "Double Graph"]
        self.graph_var = tk.StringVar(value=graph_options[0])
        graph_dropdown = ttk.Combobox(graph_frame, textvariable=self.graph_var, values=graph_options, state="readonly", width=20)
        graph_dropdown.grid(row=1, column=1, sticky='w')

    #REFRENCE FRAME
        refrence_frame = ttk.LabelFrame(self, padding=(20, 20))
        refrence_frame.grid(row=9, column=4, padx=20, pady=20, rowspan=4, columnspan=2, sticky='nswe')
        reference_title = tk.Label(refrence_frame,text="Reference Information",font=heading_font, padx=20, justify="left", pady=20, background='white')
        reference_title.grid(row=0, column=0, sticky='w')

        # Refrence name
        refrence_name_label = tk.Label(refrence_frame, text="Refrence name", font=text_font, pady=5)
        refrence_name_label.grid(row=1, column=0, sticky='w')

        self.refrence_name_var = tk.StringVar(value="")
        refrence_name_entry = ttk.Entry(refrence_frame, textvariable=self.refrence_name_var, width=20)
        refrence_name_entry.grid(row=1, column=1, sticky='w')

        # File drop widget
        refrence_excel_label = ttk.Label(refrence_frame, text="Reference Excel", font=text_font)
        refrence_excel_label.grid(row=2, column=0, sticky='w')

        self.refrence_excel_widget = ExcelFileInputWidget(refrence_frame, time_slider_widget, "reference")
        self.refrence_excel_widget.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    # STUDENT FRAME
        student_frame = ttk.LabelFrame(self, text="Student Information", padding=(10, 10))
        student_frame.grid(row=13, column=4, padx=20, pady=20, sticky='nswe', columnspan=2)
        student_title = tk.Label(student_frame,text="Student Information",font=heading_font, padx=20, justify="left", pady=20, background='white')
        student_title.grid(row=0, column=0, sticky='w')

        # Student name
        student_name_label = tk.Label(student_frame, text="Name", font=text_font, pady=5)
        student_name_label.grid(row=1, column=0, sticky='w')

        self.student_name_var = tk.StringVar(value="")
        student_name_entry = ttk.Entry(student_frame, textvariable=self.student_name_var, width=20)
        student_name_entry.grid(row=1, column=1, sticky='w')

        # Student height
        height_label = tk.Label(student_frame, text="Height", font=text_font, pady=5)
        height_label.grid(row=2, column=0, sticky='w')

        self.height_var = tk.StringVar(value="")
        height_entry = ttk.Entry(student_frame, textvariable=self.height_var, width=20)
        height_entry.grid(row=2, column=1, sticky='w')

        # Student weight
        weight_label = tk.Label(student_frame, text="Weight", font=text_font, pady=5)
        weight_label.grid(row=3, column=0, sticky='w')

        self.weight_var = tk.StringVar(value="")
        weight_entry = ttk.Entry(student_frame, textvariable=self.weight_var, width=20)
        weight_entry.grid(row=3, column=1, sticky='w')

        # Student Excel Widget
        student_excel_label = ttk.Label(student_frame, text="Student Excel", font=text_font)
        student_excel_label.grid(row=4, column=0, sticky='w')

        self.student_excel_widget = ExcelFileInputWidget(student_frame, time_slider_widget, "student")
        self.student_excel_widget.grid(row=4, column=1, padx=10, pady=10, sticky='w')

    #CREATION FRAME
        #CREATION FRAME
        creation_frame = ttk.LabelFrame(self, padding=(20, 20))
        creation_frame.grid(row=0, column=0, padx=20, pady=20, rowspan=4, columnspan=2, sticky='nswe')

        # Title
        title_font = font.Font(size=24)
        creation_title = ttk.Label(creation_frame, text=f"Choose the category to examine", font=title_font)
        creation_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        # CHOOSE THE CATEGORY TO EXAMINE
        # CHOOSE THE CATEGORY TO EXAMINE
        # CHOOSE THE CATEGORY TO EXAMINE
        # Checkbox frame
        checkbox_frame = ttk.LabelFrame(creation_frame, text="Choose the category to examine", padding=(10, 10))
        checkbox_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

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
        # Create the checkboxes
        for idx, option in enumerate(options):
            var = tk.BooleanVar(value=True)  # Default checkboxes to active
            self.check_var_dict[option] = var
            checkbox = tk.Checkbutton(checkbox_frame, text=option, variable=var, bg="white", anchor='w')
            checkbox.grid(row=idx // 2, column=idx % 2, sticky='w')

        # Confirm button
        confirm_button = ttk.Button(creation_frame, text="Confirm", command=self.on_confirm)
        confirm_button.grid(row=8, column=2, columnspan=2, pady=(10, 0))


        start_button = tk.Button(self, text="Analyze", bg=COLOR, bd=0, width=20, padx=20,
                                 command=lambda: self.on_start_button_click())
        start_button.grid(row=19, column=5, columnspan=2, pady=20,sticky="ne")
    def on_confirm_columns(self, chosen_columns):
        selected_columns = []
        for selected_sheet_columns in chosen_columns.values():
            selected_columns.extend(selected_sheet_columns)
        self.column_array = selected_columns
        print("Selected Columns:", selected_columns)
        return None

    def on_confirm(self):
        chosen_sheets = [option for option, var in self.check_var_dict.items() if var.get()]
        spreadsheet_data = {}
        
        # Load data and extract column names for each chosen sheet
        for sheet_name in chosen_sheets:
            try:
                df = pd.read_excel(self.refrence_excel_widget.file_path, engine='openpyxl', sheet_name=sheet_name)
                columns = df.columns.tolist()
                spreadsheet_data[sheet_name] = columns
            except Exception as e:
                print(f"Error loading sheet '{sheet_name}': {e}")
        # Call the popup dialog
        popup = SpreadsheetPopup(self, spreadsheet_data)

    def on_start_button_click(self):
        # Gets selected checkboxes for sheet names
        chosen_sheets = [option for option, var in self.check_var_dict.items() if var.get()]
        input_dict = { 
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
                "categories": chosen_sheets,
                "movements": self.column_array,
                "scenerio": [self.scenario_name_var.get()],
                "duration": 30,
                "starting_time": self.refrence_excel_widget.time_slider_widget.slider.get(),                      #Implement
                "Graph_type": self.graph_var.get(),
                "ref_name": self.refrence_name_var.get(),               
                "ref_file": self.refrence_excel_widget.file_path,
                "student_name": self.student_name_var.get(),
                "student_file": self.student_excel_widget.get_file_path()
            },
            "dataframe": {
                "reference_df": [],
                "student_df": []
            },
            "summary_data": {
                "category" : [],
                "movement" : [],
                "minimum_time" : [],
                "maximum_time": [] ,
                "minimum_duration": [] ,
                "optimal_duration": [],
                "maximum_duration":[] ,
            }
        }
        print(input_dict)
        # Switch to the DataVisualization page and pass the data array
        self.master.show_visualize_data(input_dict)

