from utils import *
from data_analysis import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
import time
import subprocess
import os
import platform
import tkinter as tk
HEADING = "Movement Analytics Report"
LASTHEADING = "Summary Result"

def analyze(user_data: list, file_path: str, button):

    WIDTH, HEIGHT = A4
    # Default Setting should be reset in the looping
    GRAPH_WIDTH = (WIDTH*2/3) - 20
    GRAPH_HEIGHT = (HEIGHT/3)-50
    PIE_HEIGHT = GRAPH_HEIGHT-100
    PIE_WIDTH = (WIDTH - GRAPH_WIDTH)-50
    GRAPH_X_POSITION = 10
    GRAPH_Y_POSITION = HEIGHT - GRAPH_HEIGHT - 40
    PIE_X_POSITION = (WIDTH*2/3)+10
    PIE_Y_POSITION = HEIGHT - PIE_HEIGHT -40
    TEXT_X_POSITION = PIE_X_POSITION
    TEXT_Y_POSITION = PIE_Y_POSITION - 70


    FONT = "Helvetica"
    TABLE_ROW_COLOR = '#%02x%02x%02x' % (174, 239, 206)

    SUMMARY_DATA = []
    headingData = user_data["headingData"]
    informationData =user_data["informationData"]
    visualizationData = user_data["visualizationData"]
    
    # Create a PDF canvas
    c = canvas.Canvas(file_path, pagesize=A4)

    # Add the letterhead image
    img = ImageReader("./assets/letterhead.png")
    c.drawImage(img, 0, 0, WIDTH, HEIGHT)

    # Set font and write text

    c.setFont(FONT, 12)
    c.drawString(52, HEIGHT - 300, f"Date: {current_date()}")
    c.drawString(52, HEIGHT - 320, f"Time: {current_time()}")
    c.drawString(52, HEIGHT - 340, "Project Name - {}".format(headingData["project_name"]))
    c.drawString(52, HEIGHT - 360,  "Creator Name- {}".format(headingData["project_creator"]))
    c.drawString(52, HEIGHT - 380, "Scenario - {}".format(visualizationData["scenario"]))
    c.drawString(52, HEIGHT - 400, "Student Name - {}".format(visualizationData["student_name"]))
    c.drawString(52, HEIGHT - 420,  "Weight - {} kg".format(informationData["weight"]))
    c.drawString(52, HEIGHT - 440, "Height - {} cm".format(informationData["height"]))
    c.showPage()
    ''' Second Page '''
    visualCount = 0


    # Start time
    start_time = time.time()
    try:
        for category, movementArray in visualizationData["categories"].items():
            for index, movement in enumerate(movementArray):
                _, _, duration,total_frames, starting_time, downSampled, frame_rate, Graph_type, ref_name, ref_file, student_name, student_file, horizontal_line, line_width, grid = visualizationData.values()
                print("Total Frames", total_frames)
                reference_df = readCategory(downSampled, frame_rate, total_frames, ref_file, category, ["Frame", movement], duration, starting_time)
                student_df = readCategory(downSampled, frame_rate, total_frames, student_file,category, ["Frame", movement], duration, starting_time)
                min_value = reference_df.min().min()
                max_value = reference_df.max().max() 
                status_df = calculateThreshold(student_df, movement, min_value, max_value)

                # Add a new page if visualCount exceeds 3
                if visualCount > 2:
                    c.showPage()
                    GRAPH_WIDTH = (WIDTH*2/3) - 20
                    GRAPH_HEIGHT = (HEIGHT/3)-50
                    PIE_HEIGHT = GRAPH_HEIGHT-100
                    PIE_WIDTH = (WIDTH - GRAPH_WIDTH)-50
                    GRAPH_X_POSITION = 10
                    GRAPH_Y_POSITION = HEIGHT - GRAPH_HEIGHT - 40
                    PIE_X_POSITION = (WIDTH*2/3)+10
                    PIE_Y_POSITION = HEIGHT - PIE_HEIGHT -40
                    TEXT_X_POSITION = PIE_X_POSITION
                    TEXT_Y_POSITION = PIE_Y_POSITION - 70


                    visualCount = 0

                filename = f'{category}-{movement}{Graph_type}'
                graphFilePath = makeFilePath(filename)
                title = filename
                ComparisionGraph(Graph_type, graphFilePath, title, [reference_df, student_df], [ref_name, student_name], movement, min_value, max_value, line_width, horizontal_line, grid)
                c.drawImage(f"{graphFilePath}.png", GRAPH_X_POSITION, GRAPH_Y_POSITION, GRAPH_WIDTH, GRAPH_HEIGHT)


                filename = f'{category}-{movement}Pie Chart'
                pieChartFilePath = makeFilePath(filename)
                title = filename
                pieChart(status_df, pieChartFilePath, title)

                
                Optimal_in_second, TooHigh_in_second, TooLow_in_second, minimum_time_inSecond, maximum_time_inSecond = outputCriticalValues(status_df, movement, frame_rate)
                TooHighText, OptimalText, TooLowText, MinTimeText, MaxTimeText = GenerateInfoText(Optimal_in_second, TooHigh_in_second, TooLow_in_second, minimum_time_inSecond, maximum_time_inSecond)
                c.drawImage(f"{pieChartFilePath}.png", PIE_X_POSITION, PIE_Y_POSITION, PIE_WIDTH, PIE_HEIGHT)
                c.setFont(FONT, 7)
                c.drawString(TEXT_X_POSITION, TEXT_Y_POSITION, TooHighText)
                c.drawString(TEXT_X_POSITION, TEXT_Y_POSITION + 10, OptimalText)
                c.drawString(TEXT_X_POSITION, TEXT_Y_POSITION + 20, TooLowText)
                c.drawString(TEXT_X_POSITION, TEXT_Y_POSITION + 30, MinTimeText)
                c.drawString(TEXT_X_POSITION, TEXT_Y_POSITION + 40, MaxTimeText)

                GRAPH_Y_POSITION -= GRAPH_HEIGHT + 30
                PIE_Y_POSITION -= PIE_HEIGHT*2
                TEXT_Y_POSITION -=PIE_HEIGHT*2
                visualCount += 1

                SUMMARY_DATA.append([category, movement, minimum_time_inSecond, maximum_time_inSecond, TooLow_in_second, Optimal_in_second, TooHigh_in_second])

        # Last PDF Page
        c.showPage()        
        heading = ["Category", "Movement", "Lowest Time(sec)", "Highest Time(sec)", "TooLow", "Optimal", "TooHigh"]
        SUMMARY_DATA.insert(0, heading)
        table = SummaryTable(SUMMARY_DATA, TABLE_ROW_COLOR)
        table.wrapOn(c, inch * 8, inch * 8)  
        table.drawOn(c, inch/4+10, HEIGHT-350) 
        
        # End time
        end_time = time.time()
        # Calculate and print the elapsed time
        elapsed_time = (end_time - start_time) / 60
        print("Time taken:", elapsed_time, "seconds")
        
        # Generate PDF
        c.save()

        # Open the PDF file using the default PDF viewer
        DeleteTempFiles()
        open_pdf(file_path)
        SuccessMessage = "PDF is Generated!\nTime taken: {:.2f} minutes".format(elapsed_time)
        messagebox.showinfo("Completed", SuccessMessage)
        button.config(state=tk.NORMAL, text="Analyze")

    except Exception as e:
        # Handling any other exceptions
        show_error_message(e)
        print(e)


def open_pdf(file_path):
    if platform.system() == "Darwin":       # macOS
        subprocess.call(('open', file_path))
    elif platform.system() == "Windows":    # Windows
        os.startfile(file_path)
    else:                                   # Linux variants
        subprocess.call(('xdg-open', file_path))

def GenerateInfoText(Optimal, TooHigh, TooLow, minimum_time, maximum_time):

    if TooHigh != None:
        TooHighText = f"TooHigh Total duration' - {TooHigh} seconds"
    else:
        TooHighText = "There is no high Duration!"


    if Optimal != None:
        OptimalText = f"Optimal Total duration' - {Optimal} seconds"
    else:
        OptimalText = "There is no Optimal Duration"

    if TooLow != None:
        TooLowText = f"TooLow Total duration' - {TooLow} seconds"
    else:
        TooLowText = "There is no low Duration!"
    MinTimeText = "Minimum Time at {} second".format(str(minimum_time))
    MaxTimeText = "Minimum Time at {} second".format(str(maximum_time))
    return TooHighText, OptimalText, TooLowText, MinTimeText, MaxTimeText
