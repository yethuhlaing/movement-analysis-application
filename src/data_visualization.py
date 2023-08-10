import tkinter as tk
from tkinter import PhotoImage, ttk, font
from utils import current_date, current_time, COLOR
from data_analysis import *
# input_dict = { 
#     "headingData" : {
#         "project_name": "House Riding",
#         "project_creator": "Ye Thu"
#     },
#     "informationData": {
#         "height": 34,
#         "weight" : 23,
#         "student_name": "adsasdfdasf"
#     } ,
#     "visualizationData": {
#         "categories": ["Joint Angles XZY", "L5S1 Axial Bending "],
#         "movements": ["L5S1 Flexion/Extension", "L5S1 Axial Bending"], 
#         "scenerio": ["Horse Riding"],
#         "duration": 3,
#         "starting_time": 0.2,
#         "Graph_type": ["Single Graph", "Double Graph"],
#         "fig_size": (15,5),
#         "ref_name": "Reference",
#         "ref_file": "../../data/Reference downsampled data/Simulator riding/Reference Harjusimu-003 Extended walk.xlsx",
#         "student_name": "Toni",
#         "student_file": "../../data/Student downsampled data/simulator riding/Sudent1-003Harju ext walk.xlsx"
#     }
# }

class DataVisualization(ttk.Frame):
    def __init__(self, input_list):
        tk.Frame.__init__(self, bg="white")
        self.configure(bg="white")
        self.pack(expand=True, fill="both")
        
        #Accepting the data from the last previous page
        headingData = input_list["headingData"]
        informationData = input_list["informationData"]
        visualizationData  = input_list["visualizationData"]                    

        ## Heading 
        project_name, project_creator = headingData.values()
        heading_font = font.Font(family="Bookman Old Style", size=20, weight="bold")
        heading = tk.Label(self,text=f"{project_name}",font=heading_font, padx=20, justify="left", pady=20, background='white')
        heading.pack(anchor=tk.W)
        
        InformationFrame(self, informationData)
        VisualizationFrame(self, visualizationData)

class InformationFrame(ttk.Frame):
    def __init__(self, parent, informationData):
        tk.Frame.__init__(self, parent, bg="white")
        self.height, self.weight, self.student_name = informationData.values()
        self.bmi = round(self.weight / ((self.height/100) ** 2), 2)
        self.create_widgets()
        self.pack(expand = True, fill = 'both', padx = 20, pady = 20)

    def create_widgets(self):
        text_font = font.Font(family="Bookman Old Style", size=13)
        # Create the first frame
        infoFrame = tk.Frame(self, bg='red')
        infoFrame.grid(row=0, column=0, pady=10, sticky='nsew')
        # Set the grid weights to control the resizing behavior
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=6)
        self.grid_columnconfigure(1, weight=4)

        # Create the first sub-frame
        sub_frame1 = tk.Frame(infoFrame, background="white")
        sub_frame1.grid(row=0, column=0, sticky='nsew')

        # Create the second sub-frame
        sub_frame2 = tk.Frame(infoFrame, background="white")
        sub_frame2.grid(row=0, column=1, sticky='nsew')

        infoFrame.grid_rowconfigure(0, weight=1)
        infoFrame.grid_columnconfigure(0, weight=5)
        infoFrame.grid_columnconfigure(1, weight=5)
        # Add widgets to the frames
        height = tk.Label(sub_frame1, text=f"Height - {self.height} cm", justify='left', background="white" , font=text_font)
        height.pack()
        weight = tk.Label(sub_frame1, text=f"Weight - {self.weight} kg", justify='left', background="white", font=text_font)
        weight.pack()
        bmi = tk.Label(sub_frame1, text=f"BMI - {self.bmi}", justify='left', background="white", font=text_font)
        bmi.pack()
        date = tk.Label(sub_frame2, text=f"Date - {current_date}", justify='right' , font=text_font, background="white" )
        date.pack()
        time = tk.Label(sub_frame2, text=f"Time - {current_time}", justify='right', font=text_font, background="white" )
        time.pack()
        creater = tk.Label(sub_frame2, text=f"Student - {self.student_name}", justify='right', font=text_font, background="white" )
        creater.pack()

        # Create the second frame
        optionFrame = tk.Frame(self, background="white" )
        optionFrame.grid(row=0, column=1, sticky='nsew')


        button_font = font.Font(family="Bookman Old Style", size=10)
        backButton = tk.Button(optionFrame, text ="Go Back", bg= COLOR, bd=0, width=20, padx=30, font=button_font )
        backButton.pack( pady=10)
        saveButton = tk.Button(optionFrame, text ="Save as PDF",bg= COLOR, bd=0,width=20,padx=30 , font=button_font)
        saveButton.pack( pady=10)

class VisualizationFrame(ttk.Frame):
    def __init__(self, parent, visualizationData):
        self.visualizationData = visualizationData
        tk.Frame.__init__(self, parent, bg="white")

        self.pack( expand=True, fill="both", padx = 20, pady = 20)
        self.create_canvas()

    def create_canvas(self):
        # Create a canvas widget
        canvas = tk.Canvas(self, height="600" ,highlightthickness=0, relief='ridge')
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Create a scrollbar widget

        scrollbar = ttk.Scrollbar(self, orient = 'vertical', command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")


        # Configure canvas scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox("all")))

        # Create a frame inside the canvas to hold the content
        frame = tk.Frame(canvas)
        frame.grid(sticky="ew")
        for category in self.visualizationData["categories"]:
            GraphEntry(frame, category, self.visualizationData )
        
        SummaryEntry(frame)
        
        canvas.create_window((0, 0), window=frame, anchor="nw")


    
class GraphEntry(ttk.Frame):
    def __init__(self, parent, category, visualizationData ):
        tk.Frame.__init__(self, parent, bg="white")
        self.category = category
        _, self.movement, self.scenerio, self.duration, self.starting_time, self.Graph_type, self.fig_size, self.ref_name, self.ref_file, self.student_name, self.student_file = visualizationData.values()
        self.pack(expand = True, fill = 'both')
        self.create_widget()

    def create_widget(self):
        # Create three frames
        heading_frame = tk.Frame(self, bg=COLOR,padx=50, pady=10, height=50,width=1500)
        graph_frame = tk.Frame(self, bg="white", padx=50, pady=10, height=200,width=1500 )
        information_frame = tk.Frame(self, bg="blue", padx=10, pady=10, height=200,width=1500)

        # Configure grid layout manager
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Place frames using grid layout
        heading_frame.grid(row=0, column=0, sticky="ew", pady=(10,0))
        graph_frame.grid(row=1, column=0, sticky="ew", )
        information_frame.grid(row=2, column=0, sticky="ew",  pady=(0,10))

        # Initialize the content
        text_font = font.Font(family="Bookman Old Style", size=12)
        category_label = tk.Label(heading_frame, text= self.category, justify='center', background=COLOR , font=text_font)
        category_label.pack()

        self.create_graphs(graph_frame)


    def create_graphs(self, parentFrame):

        # Set the grid weights to control the resizing behavior
        parentFrame.grid_rowconfigure(0, weight=1)
        parentFrame.grid_columnconfigure(0, weight=7)
        parentFrame.grid_columnconfigure(1, weight=3)

        # Create the Graph 
        BarGraph = tk.Frame(parentFrame, bg='red', height=100)
        BarGraph.grid(row=0, column=0, pady=10, sticky='nsew')
        # Initialize the content
        reference_df = readCategory(self.ref_file, self.category, self.movement, self.rame, self.starting_time, .2)
        reference_df
        # Create the second frame
        PieChart = tk.Frame(parentFrame, bg='blue', height=100)
        PieChart.grid(row=0, column=1, pady=10, sticky='nsew')


class SummaryEntry(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="white")
        self.pack(expand = True, fill = 'both')
        self.create_table()
    def create_table(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10, "bold"), rowheight=40)
        style.configure("Treeview", rowheight=40, borderwidth=0)
        style = ttk.Style()

        # Configure the style for the TreeView
        table = ttk.Treeview(self, columns = (1,2,3,4,5,6), show = 'headings')
        table.pack( fill='x')

        # heading = ["Movement", 'Evaluation Time', 'Minimum No', 'Minimum Frequency', 'Maximum No.', 'Minimum Frequency']
        movement = ['Bob', 'Maria', 'Alex', 'James', 'Susan', 'Henry', 'Lisa', 'Anna', 'Lisa']
        evaluation_Time = ['Smith', 'Brown', 'Wilson', 'Thomson', 'Cook', 'Taylor', 'Walker', 'Clark']
        min_number = ['Bob', 'Maria', 'Alex', 'James', 'Susan', 'Henry', 'Lisa', 'Anna', 'Lisa']
        min_frequency = ['Bob', 'Maria', 'Alex', 'James', 'Susan', 'Henry', 'Lisa', 'Anna', 'Lisa']
        max_number = ['Smith', 'Brown', 'Wilson', 'Thomson', 'Cook', 'Taylor', 'Walker', 'Clark']
        max_frequency = ['Bob', 'Maria', 'Alex', 'James', 'Susan', 'Henry', 'Lisa', 'Anna', 'Lisa']
        table_data = [movement,evaluation_Time, min_number, min_frequency, max_number, max_frequency]

        table.tag_configure('oddrow', background='white')
        table.tag_configure('evenrow', background=COLOR)

        table.heading("#1",text="Movement")
        table.heading("#2",text="Evaluation Time")
        table.heading("#3",text="Minimum No.")
        table.heading("#4",text="Minimum Frequency")
        table.heading("#5",text="Maximum No.")
        table.heading("#6",text="Maximum Frequency") 

        for i, row in enumerate(table_data):
            # Determine the tag for the row
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'

            # Insert the row into the Treeview
            table.insert('', 'end', values=row, tags=(tag,))
            

        scrollbar_table = ttk.Scrollbar(self, orient = 'vertical', command = table.yview)
        table.configure(yscrollcommand = scrollbar_table.set)
        scrollbar_table.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')


