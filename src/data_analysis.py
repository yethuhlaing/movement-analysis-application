import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import openpyxl
import math

def readCategory(file_path:str, category:str, movement: list, duration: int, startingTime: int = 0):
    df = pd.read_excel(file_path, header=0, index_col= 0 ,sheet_name = category, usecols = movement)
    starting_rows = startingTime
    ending_rows = starting_rows + duration
    return df.iloc[starting_rows:ending_rows]

def ComparisionGraph(dataframes: list, dataframe_names: list[str], y_label: str, min_critical_value: float, max_critical_value: float, figsize: tuple = (15, 5)):
    fig, ax = plt.subplots(figsize= figsize)
    for (dataframe, dataframe_name) in zip(dataframes, dataframe_names):
        ax.plot(dataframe, label= dataframe_name, linewidth=1)
    ax.set_xlabel("Frames")
    ax.set_ylabel(y_label)
    ax.axhline(y = max_critical_value, color = 'r', linestyle = '-', label = "maximum threshold")
    ax.axhline(y = min_critical_value, color = 'g', linestyle = '-', label = "minimum threshold")
    ax.legend()
    return fig

def ComparisionGraph2(dataframes: list, dataframe_names: list[str], movement: str,min_critical_value, max_critical_value, figsize: tuple = (15, 5), ):    
    fig, axes = plt.subplots(1, len(dataframes), figsize= figsize, sharey=True)
    for count, (dataframe,dataframe_names)  in enumerate(zip(dataframes,dataframe_names)):
        sns.lineplot(ax=axes[count], x= dataframe.index, y=movement, data=dataframe)
        sns.set(style="whitegrid")
        axes[count].set_title(dataframe_names)
    plt.axhline(y = max_critical_value, color = 'r', linestyle = '-', label = "maximum threshold")
    plt.axhline(y = min_critical_value, color = 'g', linestyle = '-', label = "minimum threshold")
    return fig

def calculateThreshold(df, category, min_critical_value, max_critical_value):
    statusDataframe = pd.DataFrame(df)
    if min_critical_value is None or max_critical_value is None:
        min_critical_value = df[category].describe().min()
        max_critical_value = df[category].describe().max()
    statusDataframe["Status"] = statusDataframe[category].apply(lambda x: "too low" if x < min_critical_value else ("too high" if x > max_critical_value else "optimal"))
    return statusDataframe

def pieChart(statusDataframe, title: str = ""):    
    data = statusDataframe["Status"].value_counts()
    fig = plt.figure()
    explode = (0.05)
    for i in range(1, data.shape[0]):
        explode += 0.05
    data = statusDataframe["Status"].value_counts()
    colors = ['#ff6666', '#ffcc99', '#99ff99', '#66b3ff']
    plt.pie(data, labels = data.index,colors = colors, autopct='%1.1f%%')

    #draw circle
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    plt.axis('equal')     # Equal aspect ratio ensures that pie is drawn as a circle
    plt.legend()
    plt.tight_layout()
    plt.title(title)
    return fig  