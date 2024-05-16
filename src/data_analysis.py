import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.table import Table
import seaborn as sns
matplotlib.use('TkAgg')
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def readCategory(frameRate: int, totalFrames: int, file_path:str, category:str, movement: list, duration: str, startingTime: int = 0):
    df = pd.read_excel(file_path, header=0, index_col= 0 ,sheet_name = category, usecols = movement)
    starting_frame = int(startingTime*frameRate)
    if duration == "":
        return df.iloc[starting_frame::]
    required_rows = int(duration)*frameRate
    ending_frame = int(starting_frame + required_rows)
    if totalFrames < ending_frame:
        return df.iloc[starting_frame::]
    else:
        return df.iloc[starting_frame:ending_frame]
     



def ComparisionGraph(Graph_type: str, graphFilePath: str,title: str, dataframes: list, dataframe_names: list[str], movement: str, min_critical_value: float, max_critical_value: float, grid_line: bool= False, line_width: float= 1.0 , horizontal_line: bool = False):
    if Graph_type == "Single Graph":
        for (dataframe, dataframe_name) in zip(dataframes, dataframe_names):
            plt.plot(dataframe.index, dataframe,label='Demo', linewidth=1)
        plt.title(title)
        plt.xlabel("Frames")
        plt.ylabel(movement)
        if horizontal_line == True:
            plt.axhline(y = max_critical_value, color = 'r', linestyle = '-', label = "maximum threshold")
            plt.axhline(y = min_critical_value, color = 'g', linestyle = '-', label = "minimum threshold")
        plt.grid(grid_line)
        plt.tight_layout()      
        plt.savefig(graphFilePath)
        plt.close()
    else:
        fig, axes = plt.subplots(1, len(dataframes), sharey=True, figsize=(11, 4))
        for count, (dataframe,dataframe_names)  in enumerate(zip(dataframes,dataframe_names)):
            sns.lineplot(ax=axes[count], x= dataframe.index, y=movement, data=dataframe, linewidth=1)
            sns.set_theme(style="whitegrid")
            axes[count].set_title(dataframe_names)
        if horizontal_line == True:
            plt.axhline(y = max_critical_value, color = 'r', linestyle = '-', label = "maximum threshold")
            plt.axhline(y = min_critical_value, color = 'g', linestyle = '-', label = "minimum threshold")
        plt.title(title)
        plt.xlabel("Frames")
        plt.ylabel(movement)
        plt.tight_layout()
        plt.legend()
        plt.grid(grid_line)
        plt.savefig(graphFilePath)
        plt.close()


def calculateThreshold(df, category, min_critical_value, max_critical_value):
    statusDataframe = pd.DataFrame(df)
    if min_critical_value is None or max_critical_value is None:
        min_critical_value = df[category].describe().min()
        max_critical_value = df[category].describe().max()
    statusDataframe["Status"] = statusDataframe[category].apply(lambda x: "too low" if x < min_critical_value else ("too high" if x > max_critical_value else "optimal"))
    return statusDataframe

def pieChart(statusDataframe, pieChartFilePath, title: str):  

    data = statusDataframe["Status"].value_counts()


    explode = [0] * data.shape[0]  # Initialize explode list with zeros
    for i in range(1, data.shape[0]):
        explode[i] = 0.05 * i  # Incrementally increase the explode value for each slice
    data = statusDataframe["Status"].value_counts()
    colors = {'too high': '#ff6666', 'optimal': '#ffcc99', 'too low': '#99ff99'}
    plt.pie(data, labels = data.index,colors=[colors[c] for c in data.index], autopct='%1.1f%%', startangle=90, explode=explode)
    plt.axis('equal') 
    plt.title(title)
    plt.tight_layout()
    plt.legend()
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    plt.legend()
    fig.gca().add_artist(centre_circle)
    plt.savefig(f'{pieChartFilePath}')
    plt.close()

def SummaryTable(SummaryData: list, rowColor):

    table = Table(SummaryData)

    # Add style to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), "#00c2e5"),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), rowColor),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    # Set background color for alternating rows
    for i, row in enumerate(SummaryData[1:], start=1):  # Skip heading row
        if i % 2 == 0:
            style.add('BACKGROUND', (0, i), (-1, i), rowColor)
        else:
            style.add('BACKGROUND', (0, i), (-1, i), colors.white)
        table.setStyle(style)
    return table


def outputCriticalValues(StatusDataframe, movement, frameRate):
    (row, col) = StatusDataframe.shape
    if (StatusDataframe['Status']== "optimal").any():
        Optimal_frame_count = StatusDataframe["Status"].value_counts()["optimal"]
        Optimal_in_second = round(Optimal_frame_count / frameRate, 1)
    else:
        Optimal_in_second = None

    if (StatusDataframe['Status']== "too high").any():
        TooHigh_frame_count = StatusDataframe["Status"].value_counts()["too high"]
        TooHigh_in_second = round(TooHigh_frame_count / frameRate, 1)
    else:
        TooHigh_in_second = None

    if (StatusDataframe['Status']== "too low").any():
        TooLow_frame_count = StatusDataframe["Status"].value_counts()["too low"]
        TooLow_in_second = round(TooLow_frame_count / frameRate, 1)
    else:
        TooLow_in_second = None
    
    minimum = StatusDataframe[movement].min()
    minimum_time_frame = StatusDataframe[StatusDataframe[movement] == minimum].index.tolist()[0]
    minimum_time_inSecond = round(float(minimum_time_frame) / frameRate, 1)
    
    maximum = StatusDataframe[movement].max()
    maximum_time_frame = StatusDataframe[StatusDataframe[movement] == maximum].index.tolist()[0]
    maximum_time_inSecond =round(float(maximum_time_frame) / frameRate, 1)

    return Optimal_in_second, TooHigh_in_second, TooLow_in_second, minimum_time_inSecond, maximum_time_inSecond