import tkinter as tk
from tkinter import PhotoImage, ttk, font
from configparser import ConfigParser
from utils import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from data_analysis import *
import sqlite3
from data import *
from tkinter import messagebox
from database import *


# Python libraries
from fpdf import FPDF
from datetime import datetime, timedelta

class DataVisualization(ttk.Frame):
    def __init__(self, parent):
        self.root = parent
        tk.Frame.__init__(self, self.root, bg="white")
        self.pack(expand=True, fill="both")

        ## Heading 
        headingData = getHeadingData()
        project_name, project_creator = headingData.values()
        

        heading_font = font.Font(family="Bookman Old Style", size=20, weight="bold")
        heading = tk.Label(self,text=f"{project_name}",font=heading_font, padx=20, justify="left", pady=5, background='white')
        heading.pack(anchor=tk.CENTER)

        InformationFrame(self, self.root)
        VisualizationFrame(self)


class InformationFrame(ttk.Frame):
    def __init__(self, parent, root):
        # Database Path
        self.root = root
        config = ConfigParser()
        config.read('config.ini')
        self.db_path = config.get('Database', 'database_path')
        tk.Frame.__init__(self, parent, bg="white")
        
        informationData = getInformationData()
        self.height, self.weight, self.student_name = informationData.values()
        self.bmi = round(self.weight / ((self.height/100) ** 2), 2)
        self.create_widgets()
        self.pack(expand = False, fill = 'both', pady = 20)

    def create_widgets(self):

        text_font = font.Font(family="Bookman Old Style", size=10)
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
        date = tk.Label(sub_frame2, text=f"Date - {current_date()}", justify='right' , font=text_font, background="white" )
        date.pack()
        time = tk.Label(sub_frame2, text=f"Time - {current_time()}", justify='right', font=text_font, background="white" )
        time.pack()
        creater = tk.Label(sub_frame2, text=f"Student - {self.student_name}", justify='right', font=text_font, background="white" )
        creater.pack()

        # Create the second frame

        optionFrame = tk.Frame(self, background="white" )
        optionFrame.grid(row=0, column=1, sticky='nsew')
        button_font = font.Font(family="Bookman Old Style", size=10)
        # backButton = tk.Button(optionFrame, text ="Back", bg= COLOR, bd=0, width=20, padx=30, font=button_font , command=lambda: self.previousPage())
        # backButton.pack( pady=3, anchor="e", padx=60)
        saveButton = tk.Button(optionFrame, text ="Save Data",bg= COLOR, bd=0,width=20,padx=30 , font=button_font, command=lambda: self.saveMessageBox())
        saveButton.pack( pady=3, anchor="e", padx=60)
        summarizeButton = tk.Button(optionFrame, text ="Summarize",bg= COLOR, bd=0,width=20,padx=30 , font=button_font,command=self.showSummary)
        summarizeButton.pack( pady=3, anchor="e", padx=60)
    
    def saveMessageBox(self):
        print("Desried", USER_DATA)
        # project = USER_DATA["headingData"]["project_name"]
        # scenario = USER_DATA["visualizationData"]["scenario"]
        # student = USER_DATA["informationData"]["student_name"]
        # reference_df_list = serializeDataframeList(DATAFRAME["reference_df"])
        # student_df_list = serializeDataframeList(DATAFRAME["student_df"])
        # status_df_list = serializeDataframeList(DATAFRAME["status_df"])
        # userData = serialize(USER_DATA)
        # createdDate = current_date()
        if insertHistory(self.db_path):
            messagebox.showinfo("Success", "The user data is saved successfully!")
        else:
            messagebox.showerror("Error", "There is some error in saving your data!")

    def previousPage(self):
        # ProjectCreation()
        pass

    def showSummary(self):
        SummaryWidget(self.root)


WIDTH = 210
HEIGHT = 297
FILENAME="report.pdf"
TEST_DATE = "10/20/20"

def analyze(frame, visualizationData):
    threads = []
    pdf = FPDF() # A4 (210 by 297 mm)
    
    ''' First Page '''
    pdf.add_page()
    pdf.image("../assets/letterhead_cropped.png", 0, 0, WIDTH)
    create_title(TEST_DATE, pdf)

    ''' Second Page '''
    pdf.add_page()
    # Starting position for the first image
    total_width = 210
    left_width = (2 / 3) * total_width - 30  
    right_width = (1 / 3) * total_width - 20  
    left_x_position = 5
    left_y_position = 20
    right_x_position = WIDTH/2
    right_y_position = 20
    visualCount = 0
    for category, movementArray in visualizationData["categories"].items():
        for index, movement in enumerate(movementArray):
            
            _, scenerio, duration, starting_time, Graph_type, ref_name, ref_file, student_name, student_file = visualizationData.values()
            reference_df = readCategory(ref_file, category, ["Frame", movement], duration, starting_time)
            student_df = readCategory(student_file,category, ["Frame", movement], duration, starting_time)

            min_value = reference_df.min().min()
            max_value = reference_df.max().max() 
            status_df = calculateThreshold(student_df, movement, min_value, max_value)
            grid_line = True
            line_width = 1.2
            horizontal_line = False

            if visualCount > 3:
                pdf.add_page()
            # Overwrite Files

            filename = f'{category}-{movement} {Graph_type}'
            graphFilePath = makeFilePath(filename)
            title = filename
            ComparisionGraph(Graph_type, graphFilePath, title, [reference_df, student_df], [ref_name, student_name], movement, min_value, max_value, grid_line, line_width, horizontal_line)
            pdf.image(f"{graphFilePath}.png", left_x_position, left_y_position, left_width)


            filename = f'{category}-{movement} Pie Chart'
            pieChartFilePath = makeFilePath(filename)
            title = filename
            pieChart(status_df, pieChartFilePath, title)
            pdf.image(f"{pieChartFilePath}.png", right_x_position, right_y_position, right_width) 
            
            left_y_position += 100
            right_y_position += 100
            visualCount += 1
    pdf.output(FILENAME, 'F')
    DeleteTempFiles()

def create_title(day, pdf):
    # Unicode is not yet supported in the py3k version; use windows-1252 standard font
    pdf.set_font('Arial', '', 24)  
    pdf.ln(60)
    pdf.write(5, f"Covid Analytics Report")
    pdf.ln(10)
    pdf.set_font('Arial', '', 16)
    pdf.write(4, f'{day}')
    pdf.ln(5)




def create_information_widget(self, parentFrame):

    Optimal, TooHigh, TooLow, minimum_time_inMinute, maximum_time_inMinute = outputCriticalValues(self.status_df, self.movement)

    if TooHigh != None:
        TooHighText = f"TooHigh Total duration' - {TooHigh} minute"
    else:
        TooHighText = "There is no high Duration!"


    if Optimal != None:
        OptimalText = f"Optimal Total duration' - {Optimal} minute"
    else:
        OptimalText = "There is no Optimal Duration"

    if TooLow != None:
        TooLowText = f"TooLow Total duration' - {TooLow} minute"
    else:
        TooLowText = "There is no low Duration!"

