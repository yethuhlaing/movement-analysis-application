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

def makeFilePath(filename):
    temp_dir = FindTempFolder()
    # Ensure that the temporary folder exists, if not, create it
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    filepath = os.path.join(temp_dir, filename)
    return filepath

def FindTempFolder():
    current_dir = os.path.abspath(__file__)
    parent_dir = os.path.dirname(current_dir)
    temp_dir = os.path.join(os.path.dirname(parent_dir), "temp")
    return temp_dir

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