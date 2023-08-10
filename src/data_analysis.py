import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import timeit
import openpyxl
from pywaffle import Waffle
import math
from tabulate import tabulate

def readCategory(file_path:str, sheet_name:str, category: list, frameRate: int, Duration: float, startingTime: float = 0):
    df = pd.read_excel(file_path, header=0, index_col= 0 ,sheet_name = sheet_name, usecols = category)
    num_rows = df.shape[0]
    desired_num_rows = math.floor(frameRate*Duration) 
    starting_rows =  math.floor(startingTime*frameRate) 
    ending_rows = starting_rows + desired_num_rows
    if desired_num_rows > num_rows:     
        return df.iloc[starting_rows:-1]
    else:
        return df.iloc[starting_rows:ending_rows]

def ComparisionGraph(dataframes: list, dataframe_names: list[str], x_label: str, y_label: str, min_critical_value: float, max_critical_value: float, figsize: tuple = (15, 5)):
    fig, ax = plt.subplots(figsize= figsize)
    for (dataframe, dataframe_name) in zip(dataframes, dataframe_names):
        ax.plot(dataframe, label= dataframe_name, linewidth=1)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.axhline(y = max_critical_value, color = 'r', linestyle = '-', label = "maximum threshold")
    ax.axhline(y = min_critical_value, color = 'g', linestyle = '-', label = "minimum threshold")
    ax.legend()
    return fig

def ComparisionGraph2(dataframes: list, dataframe_names: list[str], title: str, x_labels: list, y_labels: list,min_critical_value, max_critical_value, figsize: tuple = (15, 5), ):    
    fig, axes = plt.subplots(1, len(dataframes), figsize= figsize, sharey=True)
    fig.suptitle(title)  
    for count, (dataframe,dataframe_names)  in enumerate(zip(dataframes,dataframe_names)):
        sns.lineplot(ax=axes[count], x= dataframe.index, y=dataframe["L5S1 Lateral Bending"], data=dataframe)
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
    statusDataframe["Status"] = statusDataframe[category].apply(lambda x: "low" if x < min_critical_value else ("high" if x > max_critical_value else "medium"))
    return statusDataframe
