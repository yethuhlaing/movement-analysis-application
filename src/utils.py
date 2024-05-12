import datetime
import pandas as pd
import matplotlib.pyplot as plt
import json
import pickle
import tkinter as tk
import os
COLOR = '#%02x%02x%02x' % (174, 239, 206)
STYLE_SHEETS = plt.style.available

# button_font = font.Font(family="Bookman Old Style", size=10)
# text_font = font.Font(family="Bookman Old Style", size=10)
# heading_font = font.Font(family="Bookman Old Style", size=20, weight="bold")

def current_date():
    return datetime.date.today()

def current_time():
    return datetime.datetime.now().time().strftime("%H:%M:%S")

def serializeDataframeList(dataframe_list):
    serializedDataframeList = []
    for dataframe in dataframe_list:
        dataframe_bytes = pickle.dumps(dataframe)
        serializedDataframeList.append(dataframe_bytes)
    return serializedDataframeList

def deserializeDataframe(df_bytes):
    return pickle.loads(df_bytes)

def serialize(dict):
    return json.dumps(dict)

def deserialize(json_str):
    return json.loads(json_str)

# def clear_entry_text(entry):
#     entry.delete(0, tk.END)  # Delete current text
#     entry.insert(0, "")  

def makeFilePath(filename):
    current_dir = os.path.abspath(__file__)
    parent_dir = os.path.dirname(current_dir)
    temp_dir = os.path.join(os.path.dirname(parent_dir), "temp")
    # Ensure that the temporary folder exists, if not, create it
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    filepath = os.path.join(temp_dir, filename)
    return filepath

def DeleteTempFiles():

    current_dir = os.path.abspath(__file__)
    parent_dir = os.path.dirname(current_dir)
    temp_dir = os.path.join(os.path.dirname(parent_dir), "temp")
    # List all files in the directory
    files = os.listdir(temp_dir)
    # Iterate over each file and delete it
    for file in files:
        file_path = os.path.join(temp_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"Skipping non-file: {file_path}")