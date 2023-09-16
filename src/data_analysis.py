import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import openpyxl
import math

def readCategory(file_path:str, category:str, movement: list, duration: str, startingTime: int = 0):
    df = pd.read_excel(file_path, header=0, index_col= 0 ,sheet_name = category, usecols = movement)
    starting_rows = startingTime
    if duration == "":
        return df.iloc[starting_rows::]
    duration = int(duration)
    ending_rows = starting_rows + duration
    return df.iloc[starting_rows:ending_rows]
        

def ComparisionGraph(dataframes: list, dataframe_names: list[str], y_label: str, min_critical_value: float, max_critical_value: float, grid_line: bool, line_width: float , horizontal_line: bool = False):
    fig, ax = plt.subplots(figsize=(11, 4)) 
    for (dataframe, dataframe_name) in zip(dataframes, dataframe_names):
        ax.plot(dataframe, label= dataframe_name, linewidth=1)
    ax.set_xlabel("Frames")
    ax.set_ylabel(y_label)
    if horizontal_line == True:
        ax.axhline(y = max_critical_value, color = 'r', linestyle = '-', label = "maximum threshold")
        ax.axhline(y = min_critical_value, color = 'g', linestyle = '-', label = "minimum threshold")
    ax.legend()
    ax.grid(grid_line)
    plt.tight_layout()
    return plt.gcf()

def ComparisionGraph2(dataframes: list, dataframe_names: list[str], movement: str,min_critical_value, max_critical_value,grid_line: bool, line_width: float, horizontal_line: bool = False ):    
    fig, axes = plt.subplots(1, len(dataframes), sharey=True, figsize=(11, 4))
    for count, (dataframe,dataframe_names)  in enumerate(zip(dataframes,dataframe_names)):
        sns.lineplot(ax=axes[count], x= dataframe.index, y=movement, data=dataframe, linewidth=1)
        sns.set(style="whitegrid")
        axes[count].set_title(dataframe_names)
    if horizontal_line == True:
        plt.axhline(y = max_critical_value, color = 'r', linestyle = '-', label = "maximum threshold")
        plt.axhline(y = min_critical_value, color = 'g', linestyle = '-', label = "minimum threshold")
    plt.tight_layout()
    plt.grid(grid_line)
    return plt.gcf()

def calculateThreshold(df, category, min_critical_value, max_critical_value):
    statusDataframe = pd.DataFrame(df)
    if min_critical_value is None or max_critical_value is None:
        min_critical_value = df[category].describe().min()
        max_critical_value = df[category].describe().max()
    statusDataframe["Status"] = statusDataframe[category].apply(lambda x: "too low" if x < min_critical_value else ("too high" if x > max_critical_value else "optimal"))
    return statusDataframe

def pieChart(statusDataframe, title: str = ""):    
    data = statusDataframe["Status"].value_counts()
    fig = plt.figure(figsize= (4,4))
    explode = (0.05)
    # for i in range(1, data.shape[0]):
    #     explode += 0.05
    data = statusDataframe["Status"].value_counts()
    colors = {'too high': '#ff6666', 'optimal': '#ffcc99', 'too low': '#99ff99'}
    plt.pie(data, labels = data.index,colors=[colors[c] for c in data.index], autopct='%1.1f%%', startangle=90)

    #draw circle
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    plt.axis('equal') 
    plt.legend()
    plt.tight_layout()
    plt.title(title)
    return plt.gcf()  

def outputCriticalValues(StatusDataframe, movement):
    (row, col) = StatusDataframe.shape
    if (StatusDataframe['Status']== "optimal").any():
        Optimal_in_second = StatusDataframe["Status"].value_counts()["optimal"]
        Optimal = round(Optimal_in_second / 60, 1)
    else:
        Optimal = None

    if (StatusDataframe['Status']== "too high").any():
        TooHigh_in_second = StatusDataframe["Status"].value_counts()["too high"]
        TooHigh = round(TooHigh_in_second / 60, 1)
    else:
        TooHigh = None

    if (StatusDataframe['Status']== "too low").any():
        TooLow_in_second = StatusDataframe["Status"].value_counts()["too low"]
        TooLow = round(TooLow_in_second / 60, 1)
    else:
        TooLow = None
    
    minimum = StatusDataframe[movement].min()
    minimum_time_inSecond = StatusDataframe[StatusDataframe[movement] == minimum].index.tolist()[0]
    minimum_time_inMinute = round(float(minimum_time_inSecond) / 60, 1)
    
    maximum = StatusDataframe[movement].max()
    maximum_time_inSecond = StatusDataframe[StatusDataframe[movement] == maximum].index.tolist()[0]
    maximum_time_inMinute =round(float(maximum_time_inSecond) / 60, 1)

    return Optimal, TooHigh, TooLow, minimum_time_inMinute, maximum_time_inMinute