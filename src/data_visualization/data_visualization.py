import tkinter as tk
from tkinter import PhotoImage, ttk, font
from utils import current_date, current_time, COLOR, STYLE_SHEETS
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_analysis.data_analysis import *
import sqlite3
#from data import *
class DataVisualization(ttk.Frame):
    def __init__(self,user_data):
        tk.Frame.__init__(self, bg="white")
        self.configure(bg="white")
        self.pack(expand=True, fill="both")

        headingData = user_data["headingData"]
        ## Heading 
        project_name, project_creator = headingData.values()
        heading_font = font.Font(family="Bookman Old Style", size=20, weight="bold")
        heading = tk.Label(self,text=f"{project_name}",font=heading_font, padx=20, justify="left", pady=20, background='white')
        heading.pack(anchor=tk.W)
        InformationFrame(self,user_data)
        VisualizationFrame(self,user_data)


class InformationFrame(ttk.Frame):
    def __init__(self, parent,user_data):
        tk.Frame.__init__(self, parent, bg="white")
        informationData = user_data["informationData"]
        self.height, self.weight, self.student_name = informationData.values()
        self.bmi = round(self.weight / ((self.height/100) ** 2), 2)
        self.create_widgets()
        self.pack(expand = False, fill = 'both', pady = 20)

    def create_widgets(self):
        text_font = font.Font(family="Bookman Old Style", size=13)
        # Create the first frame
        infoFrame = tk.Frame(self, bg='red')
        infoFrame.grid(row=0, column=0, pady=0, sticky='nsew')
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
        backButton = tk.Button(optionFrame, text ="Back", bg= COLOR, bd=0, width=20, padx=30, font=button_font )
        backButton.pack( pady=3, anchor="e", padx=60)
        saveButton = tk.Button(optionFrame, text ="Save",bg= COLOR, bd=0,width=20,padx=30 , font=button_font)
        saveButton.pack( pady=3, anchor="e", padx=60)
        savePDFButton = tk.Button(optionFrame, text ="Save as PDF",bg= COLOR, bd=0,width=20,padx=30 , font=button_font,)#command=self.master.save_current_frame_as_pdf("test.pdf"))
        savePDFButton.pack( pady=3, anchor="e", padx=60)


class VisualizationFrame(ttk.Frame):
    def __init__(self, parent,user_data):
        self.visualizationData  = user_data["visualizationData"]                    

        canvas = tk.Canvas(parent, bg="white", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(parent, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        frame = tk.Frame(canvas, background="white")
        frame.pack(fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        for category in self.visualizationData["categories"]:
            for movement in self.visualizationData["movements"]:
                GraphicalWidget(frame, category, movement, self.visualizationData,user_data) 
        SummaryWidget(frame,user_data)
        # Update the scroll region
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


class GraphicalWidget(ttk.Frame):
    def __init__(self, parent, category, movement, visualizationData,user_data):
        tk.Frame.__init__(self, parent, bg="white", pady=20)
        self.category = category
        self.movement = movement
        _, _, self.scenerio, self.duration, self.starting_time, self.Graph_type, self.ref_name, self.ref_file, self.student_name, self.student_file = visualizationData.values()

        # Appending Data to Summary Table
        user_data["summary_data"]["category"].append(self.category)
        user_data["summary_data"]["movement"].append(self.movement)

        self.min_critical = tk.DoubleVar()
        self.line_width = tk.DoubleVar()
        self.max_critical = tk.DoubleVar() 
        self.graph_style = tk.StringVar()
        self.graph_style.set("default")
        self.grid_line = tk.BooleanVar()
        self.grid_line.set(False)
        self.horizontal_line = tk.BooleanVar()
        self.horizontal_line.set(True)
        screen_width = parent.winfo_screenwidth()
        self.pack(expand = True, fill="both",padx = 20)
        self.config(width=screen_width)
        # Create three frames
        self.heading_frame = tk.Frame(self, bg=COLOR)
        self.graph_frame = tk.Frame(self, bg="white", pady=5)
        self.information_frame = tk.Frame(self, bg="white",  pady=5)

        # Place the frames using grid
        self.heading_frame.grid(row=0, column=0, sticky="nsew")
        self.graph_frame.grid(row=1, column=0, sticky="nsew")
        self.information_frame.grid(row=2, column=0, sticky="nsew")

        # Allow the column to expand
        self.grid_columnconfigure(0, weight=1)

        # Initialize the content
        text_font = font.Font(family="Bookman Old Style", size=12)
        category_label = tk.Label(self.heading_frame, text= self.category, justify='center', background=COLOR , font=text_font, pady=5)
        category_label.pack()

        self.create_graph_widget(self.graph_frame)
        self.create_information_widget(self.information_frame,user_data)

    def create_graph_widget(self, parentFrame):
        self.parentFrame = parentFrame
        # Set the grid weights to control the resizing behavior
        self.parentFrame.grid_rowconfigure(0, weight=1)
        self.parentFrame.grid_columnconfigure(0, weight=7)
        self.parentFrame.grid_columnconfigure(1, weight=3)

        self.reference_df = readCategory(self.ref_file, self.category, ["Frame", self.movement], self.duration, self.starting_time)
        self.student_df = readCategory(self.student_file,self.category, ["Frame", self.movement], self.duration, self.starting_time)
        min_value = self.reference_df.min().min()
        max_value = self.reference_df.max().max() 

        # Create the Graph Frame 
        self.BarGraph = tk.Frame(self.parentFrame, bg='white')
        self.BarGraph.grid(row=0, column=0, sticky='nsew')
        self.initializeBarGraph(self.BarGraph, min_value, max_value, False,1, True)

        # Create the Piechart frame
        self.PieChart = tk.Frame(self.parentFrame, bg='white')
        self.PieChart.grid(row=0, column=1, pady=10, sticky='nsew')
        self.statusDataframe = calculateThreshold(self.student_df, self.movement, min_value, max_value)
        self.initializePieChart(self.statusDataframe, self.PieChart)

    def initializeBarGraph(self, parent, min_value, max_value, grid_line, line_width, horizontal_line):
        if self.Graph_type == "Single Graph":
            fig = ComparisionGraph([self.reference_df, self.student_df], [self.ref_name, self.student_name], self.movement, min_value, max_value, grid_line, line_width, horizontal_line)
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
        else:
            fig = ComparisionGraph2([self.reference_df, self.student_df], [self.ref_name, self.student_name], self.movement, min_value, max_value, grid_line, line_width, horizontal_line)
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)

    def initializePieChart(self, statusDataframe, parent):
        fig = pieChart(statusDataframe)
        canvas = FigureCanvasTkAgg(fig, master=parent )
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack( fill=tk.BOTH, expand=True )

    def create_information_widget(self, parentFrame,user_data):

        text_font = font.Font(family="Bookman Old Style", size=13)

        parentFrame.grid_rowconfigure(0, weight=1)
        parentFrame.grid_columnconfigure(0, weight=3)
        parentFrame.grid_columnconfigure(1, weight=3)
        parentFrame.grid_columnconfigure(2, weight=3)   
        parentFrame.grid_columnconfigure(3, weight=3)   
        parentFrame.grid_columnconfigure(4, weight=3)   

        thresholdFrame = tk.Frame(parentFrame, bg='white')
        thresholdFrame.grid(row=0, column=0, pady=0, sticky='nsew')
        # # Add widgets to the frames
        min_critical_frame = ttk.Frame(thresholdFrame)
        min_critical_frame.grid(row=0, column=0, padx=10, pady=10)
        min_critical_label = tk.Label(min_critical_frame, text="Minimum threshold", font=text_font, background="white")
        min_critical_label.grid(row=0, column=0, sticky='w')
        min_critical_widget = ttk.Entry(min_critical_frame, width=20, textvariable=self.min_critical, background="white")
        min_critical_widget.grid(row=0, column=1, sticky='w')
        
        max_critical_frame  = ttk.Frame(thresholdFrame)
        max_critical_frame.grid(row=1, column=0, padx=10, pady=10)
        max_critical_label = tk.Label(max_critical_frame, text="Maximum threshold", font=text_font, background="white")
        max_critical_label.grid(row=0, column=0, sticky='w')
        max_critical_widget = ttk.Entry(max_critical_frame, width=20, textvariable=self.max_critical, background="white")
        max_critical_widget.grid(row=0, column=1, sticky='w')


        # # Create the second frame
        informationFrame = tk.Frame(parentFrame, background="white" )
        informationFrame.grid(row=0, column=1, sticky='nsew')

        line_width_frame  = ttk.Frame(informationFrame)
        line_width_frame.grid(row=0, column=0, padx=10, pady=10)
        line_width_label = tk.Label(line_width_frame, text="Line Width", font=text_font, background="white")
        line_width_label.grid(row=0, column=0, sticky='w') 
        line_width_widget = ttk.Entry(line_width_frame, width=25, textvariable=self.line_width, background="white")
        line_width_widget.grid(row=0, column=1, sticky='w')

        graph_style_frame  = ttk.Frame(informationFrame)
        graph_style_frame.grid(row=1, column=0, padx=10, pady=10)
        graph_style_label = tk.Label(graph_style_frame, text="Graph Style", font=text_font, background="white")
        graph_style_label.grid(row=0, column=0, sticky='w')
        self.graph_style_widget = ttk.Combobox(graph_style_frame,width=20, background="white", textvariable=self.graph_style,)
        self.graph_style_widget["values"] = STYLE_SHEETS
        self.graph_style_widget.current()
        self.graph_style_widget.grid(row=0, column=1, sticky='w')

        # Create the second frame
        informationFrame2 = tk.Frame(parentFrame, background="white" )
        informationFrame2.grid(row=0, column=2, sticky='nsew')
        style = ttk.Style(informationFrame2)
        style.configure("Custom.TCheckbutton", background="white", font= text_font)
        grid_line_checkbox = ttk.Checkbutton(informationFrame2, text="Grid Line", variable=self.grid_line, style="Custom.TCheckbutton")
        grid_line_checkbox.pack(anchor=tk.W, padx=10, pady=10)
        horizontal_line_checkbox = ttk.Checkbutton(informationFrame2, text="Horizontal Line", variable=self.horizontal_line, style="Custom.TCheckbutton")
        horizontal_line_checkbox.pack(anchor=tk.W, padx=10, pady=10)

        UpdateButtonFrame = tk.Frame(parentFrame, background="white" )
        UpdateButtonFrame.grid(row=0, column=3, sticky='nsew')
        button_font = font.Font(family="Bookman Old Style", size=10)
        update_button = tk.Button(UpdateButtonFrame, text="Update",bg= COLOR,bd=0,width=20,padx=30, command=self.UpdateGraphInformation, font=button_font)
        update_button.pack()

        outputFrame = tk.Frame(parentFrame, background="white" )
        outputFrame.grid(row=0, column=4, sticky='nsew')
        Optimal, TooHigh, TooLow, minimum_time_inMinute, maximum_time_inMinute = outputCriticalValues(self.statusDataframe, self.movement)
        # Appending Data to Summary Table
        user_data["summary_data"]["minimum_time"].append(minimum_time_inMinute)
        user_data["summary_data"]["maximum_time"].append(maximum_time_inMinute)
        user_data["summary_data"]["minimum_duration"].append(TooLow)
        user_data["summary_data"]["optimal_duration"].append(Optimal)
        user_data["summary_data"]["maximum_duration"].append(TooHigh)
        if TooHigh != None:
            TooHighText = f"Total duration for  'Too high' - {TooHigh} second ({TooHigh/60:.1f} minute)"
        else:
            TooHighText = "There is no high Duration!"
        TooHighLabel = ttk.Label(outputFrame, text=TooHighText, font= text_font, background="white", anchor='w')
        TooHighLabel.pack()

        if Optimal != None:
            OptimalText = f"Total duration for  'Optimal' - {Optimal} second ({Optimal/60:.1f} minute)"
        else:
            OptimalText = "There is no Optimal Duration"
        OptimalLabel = ttk.Label(outputFrame, text=OptimalText, font= text_font, background="white", anchor='w')
        OptimalLabel.pack()

        if TooLow != None:
            TooLowText = f"Total duration for 'Too Low' - {TooLow} second ({TooLow/60:.1f} minute)"
        else:
            TooLowText = "There is no low Duration!"
        TooLowLabel = ttk.Label(outputFrame, text=TooLowText, font= text_font, background="white", anchor='w')
        TooLowLabel.pack()

    def UpdateGraphInformation(self):
        # Create the Graph Frame 
        self.BarGraph.destroy()
        self.BarGraph = tk.Frame(self.graph_frame, bg='white')
        self.BarGraph.grid(row=0, column=0, sticky='nsew')
        self.initializeBarGraph(self.BarGraph, self.min_critical.get(), self.max_critical.get(),  self.grid_line.get(), self.line_width.get(), self.horizontal_line.get())

        # Create the Piechart frame
        self.PieChart.destroy()
        self.PieChart = tk.Frame(self.graph_frame, bg='white')
        self.PieChart.grid(row=0, column=1, pady=10, sticky='nsew')
        self.statusDataframe = calculateThreshold(self.student_df, self.movement, self.min_critical.get(), self.max_critical.get())
        self.initializePieChart(self.statusDataframe, self.PieChart)


class SummaryWidget(ttk.Frame):
    def __init__(self, parent,user_data):
        tk.Frame.__init__(self, parent, bg="white")
        self.pack(expand = True, fill = 'both', padx=10, pady=20)
        self.create_table(user_data)
    def create_table(self,user_data):
        style = ttk.Style()
        text_fonts = font.Font(family="Bookman Old Style", size=13)
        style.configure("Treeview.Heading", font=text_fonts, rowheight=40, relief="flat")
        style.configure("Treeview", rowheight=40, borderwidth=0)
        style = ttk.Style()
            
        # Configure the style for the TreeView
        table = ttk.Treeview(self, columns = (1,2,3,4,5,6,7), show = 'headings')
        table.pack( fill='x')

        table.tag_configure('oddrow', background='white')
        table.tag_configure('evenrow', background=COLOR)

        table.heading("#1",text="Category")
        table.heading("#2",text="Movement")
        table.heading("#3",text="Minimum Time(min)")
        table.heading("#4",text="Maximum Time(min)")
        table.heading("#5",text="Minimum Duration(min)")
        table.heading("#6",text="Optimal Duration(min)")
        table.heading("#7",text="Maximum Duration(min)") 

        for idx, category in enumerate(user_data["summary_data"]["category"]):
            # Determine the tag for the row
            tag = 'oddrow' if idx % 2 == 0 else 'evenrow'

            movement = user_data["summary_data"]["movement"][idx]
            min_time = user_data["summary_data"]["minimum_time"][idx]
            max_time = user_data["summary_data"]["maximum_time"][idx]
            min_duration = user_data["summary_data"]["minimum_duration"][idx]
            optimal_duration = user_data["summary_data"]["optimal_duration"][idx]
            max_duration = user_data["summary_data"]["maximum_duration"][idx]
            
            table.insert("", idx, text=str(idx), values=(category, movement, min_time, max_time, min_duration, optimal_duration, max_duration),tags=(tag,))            

        scrollbar_table = ttk.Scrollbar(self, orient = 'vertical', command = table.yview)
        table.configure(yscrollcommand = scrollbar_table.set)
        scrollbar_table.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')