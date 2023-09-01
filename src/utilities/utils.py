import datetime
import pandas as pd
import matplotlib.pyplot as plt
import json
import pickle
import tkinter as tk

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

def clear_entry_text(entry):
    entry.delete(0, tk.END)  # Delete current text
    entry.insert(0, "")  

