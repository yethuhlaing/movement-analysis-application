import tkinter as tk
from tkinter import ttk, font

COLOR = '#%02x%02x%02x' % (174, 239, 206)

class ProjectCreation(ttk.Frame):
    def __init__(self, parent, project_name):
        tk.Frame.__init__(self, parent, bg="white")
        self.create_widgets(project_name)
        self.pack(expand=True, fill="both")

    def create_widgets(self, project_name):
        # Create a LabelFrame to group the checkboxes
        checkbox_frame = ttk.LabelFrame(self, text="Choose the category to examine", padding=(10, 10))
        checkbox_frame.grid(row=0, column=0, padx=50, pady=30, sticky='nsew')

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

        self.check_var = []
        for idx, option in enumerate(options):
            var = tk.BooleanVar(value=True)  # Default checkboxes to active
            self.check_var.append(var)
            checkbox = tk.Checkbutton(checkbox_frame, text=option, variable=var, bg="white", anchor='w')
            checkbox.grid(row=idx // 2, column=idx % 2, sticky='w')

        # Create a LabelFrame for the "General" section
        general_frame = ttk.LabelFrame(self, text="General", padding=(10, 10))
        general_frame.grid(row=0, column=1, padx=50, pady=30, sticky='nsew', rowspan=3, columnspan=2)

        # Heading "Choose Scenario" with a dropbox
        scenario_label = tk.Label(general_frame, text="Choose Scenario", font=font.Font(size=12), pady=5)
        scenario_label.grid(row=0, column=0, sticky='w')

        scenario_options = ["Scenario A", "Scenario B", "Scenario C"]
        self.scenario_var = tk.StringVar(value=scenario_options[0])
        scenario_dropdown = ttk.Combobox(general_frame, textvariable=self.scenario_var, values=scenario_options, state="readonly", width=20)
        scenario_dropdown.grid(row=0, column=1, sticky='w')

        # Heading "Duration" with a dropbox
        duration_label = tk.Label(general_frame, text="Duration", font=font.Font(size=12), pady=5)
        duration_label.grid(row=1, column=0, sticky='w')

        duration_options = ["1 hour", "2 hours", "3 hours"]
        self.duration_var = tk.StringVar(value=duration_options[0])
        duration_dropdown = ttk.Combobox(general_frame, textvariable=self.duration_var, values=duration_options, state="readonly", width=20)
        duration_dropdown.grid(row=1, column=1, sticky='w')

        # Heading "Starting Time" with a dropbox
        time_label = tk.Label(general_frame, text="Starting Time", font=font.Font(size=12), pady=5)
        time_label.grid(row=2, column=0, sticky='w')

        time_options = ["09:00 AM", "12:00 PM", "03:00 PM"]
        self.time_var = tk.StringVar(value=time_options[0])
        time_dropdown = ttk.Combobox(general_frame, textvariable=self.time_var, values=time_options, state="readonly", width=20)
        time_dropdown.grid(row=2, column=1, sticky='w')

        # Create a LabelFrame for the "Graphical Visualization" section
        graph_frame = ttk.LabelFrame(self, text="Graphical Visualization", padding=(10, 10))
        graph_frame.grid(row=1, column=1, padx=50, pady=30, sticky='nsew', columnspan=2)

        # Heading "Graph Type" with a dropbox
        graph_label = tk.Label(graph_frame, text="Graph Type", font=font.Font(size=12), pady=5)
        graph_label.grid(row=0, column=0, sticky='w')

        graph_options = ["Bar Graph", "Pie Chart", "Line Graph"]
        self.graph_var = tk.StringVar(value=graph_options[0])
        graph_dropdown = ttk.Combobox(graph_frame, textvariable=self.graph_var, values=graph_options, state="readonly", width=20)
        graph_dropdown.grid(row=0, column=1, sticky='w')

        # Heading "Figure Size" with a dropbox
        size_label = tk.Label(graph_frame, text="Figure Size", font=font.Font(size=12), pady=5)
        size_label.grid(row=1, column=0, sticky='w')

        size_options = ["Small", "Medium", "Large"]
        self.size_var = tk.StringVar(value=size_options[0])
        size_dropdown = ttk.Combobox(graph_frame, textvariable=self.size_var, values=size_options, state="readonly", width=20)
        size_dropdown.grid(row=1, column=1, sticky='w')

        # Create a LabelFrame for the "Reference Information" section
        reference_frame = ttk.LabelFrame(self, text="Reference Information", padding=(10, 10))
        reference_frame.grid(row=2, column=1, padx=50, pady=30, sticky='nsew', columnspan=2)

        # Heading "Name" with a text box
        name_label = tk.Label(reference_frame, text="Name", font=font.Font(size=12), pady=5)
        name_label.grid(row=0, column=0, sticky='w')

        self.name_var = tk.StringVar(value="")
        name_entry = ttk.Entry(reference_frame, textvariable=self.name_var, width=20)
        name_entry.grid(row=0, column=1, sticky='w')

        # Heading "Upload Reference Data" with a drag and drop box
        def on_file_drop(event):
            file_path = event.data
            print("Uploaded File Path:", file_path)

        drop_box_label = tk.Label(reference_frame, text="Upload Reference Data", font=font.Font(size=12), pady=5)
        drop_box_label.grid(row=1, column=0, sticky='w')

        drop_box_frame = ttk.Frame(reference_frame, width=200, height=100, relief='sunken', borderwidth=2)
        drop_box_frame.grid(row=1, column=1, sticky='w')

        drop_box_frame.bind("<<Drop>>", on_file_drop)  # Use "DND_DND_RELEASE" event type

        # Create a LabelFrame for the "Student Information" section
        student_frame = ttk.LabelFrame(self, text="Student Information", padding=(10, 10))
        student_frame.grid(row=3, column=1, padx=50, pady=30, sticky='nsew', columnspan=2)

        # Heading "Name" with a text box
        student_name_label = tk.Label(student_frame, text="Name", font=font.Font(size=12), pady=5)
        student_name_label.grid(row=0, column=0, sticky='w')

        self.student_name_var = tk.StringVar(value="")
        student_name_entry = ttk.Entry(student_frame, textvariable=self.student_name_var, width=20)
        student_name_entry.grid(row=0, column=1, sticky='w')

        # Heading "Height" with a text box
        height_label = tk.Label(student_frame, text="Height", font=font.Font(size=12), pady=5)
        height_label.grid(row=1, column=0, sticky='w')

        self.height_var = tk.StringVar(value="")
        height_entry = ttk.Entry(student_frame, textvariable=self.height_var, width=20)
        height_entry.grid(row=1, column=1, sticky='w')

        # Heading "Weight" with a text box
        weight_label = tk.Label(student_frame, text="Weight", font=font.Font(size=12), pady=5)
        weight_label.grid(row=2, column=0, sticky='w')

        self.weight_var = tk.StringVar(value="")
        weight_entry = ttk.Entry(student_frame, textvariable=self.weight_var, width=20)
        weight_entry.grid(row=2, column=1, sticky='w')

        # Heading "Upload Student Data" with a drag and drop box
        def on_student_data_drop(event):
            file_path = event.data
            print("Uploaded Student Data File Path:", file_path)

        student_drop_box_label = tk.Label(student_frame, text="Upload Student Data", font=font.Font(size=12), pady=5)
        student_drop_box_label.grid(row=3, column=0, sticky='w')

        student_drop_box_frame = ttk.Frame(student_frame, width=200, height=100, relief='sunken', borderwidth=2)
        student_drop_box_frame.grid(row=3, column=1, sticky='w')

        student_drop_box_frame.bind("<<Drop>>", on_student_data_drop)  # Use "DND_DND_RELEASE" event type

        start_button = tk.Button(self, text="Start", bg=COLOR, bd=0, width=20, padx=20,
                                 command=lambda: self.on_start_button_click(project_name))
        start_button.grid(row=4, column=1, columnspan=2, pady=20)

        def on_start_button_click(self, project_name):
            # Get the selected categories from the checkboxes
            selected_categories = [option for option, var in zip(self.check_var, options) if var.get()]
            print("Selected Categories:", selected_categories)