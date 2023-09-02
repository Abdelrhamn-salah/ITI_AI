import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split

# Global variables

data = None


# GUI function to open and load CSV file
def open_file():
    global data
    file_path = filedialog.askopenfilename()
    if not os.path.exists(file_path):
        return
    data = pd.read_csv(file_path)
    print(data)


# Data cleaning functions
def check_file_exists(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist")


def handle_invalid_file_format(file_path):
    raise ValueError("File is not in the correct format")


def fill_missing_values(data, method="mean"):
    if method == "mean":
        data.fillna(data.mean(), inplace=True)
    elif method == "mode":
        data.fillna(data.mode(), inplace=True)
    else:
        raise ValueError("Invalid method for filling missing values")


def detect_outliers(data, threshold=3):
    numerical_columns = data.select_dtypes(include=[np.number]).columns
    for column in numerical_columns:
        z_scores = (data[column] - data[column].mean()) / data[column].std()
        outliers = data[abs(z_scores) > threshold]
        data.drop(outliers.index, inplace=True)


def scale_normalize(data):
    numerical_columns = data.select_dtypes(include=[np.number]).columns
    for column in numerical_columns:
        # Min-Max scaling
        data[column] = (data[column] - data[column].min()) / (data[column].max() - data[column].min())
        # Standard normalization (z-score normalization)
        # data[column] = (data[column] - data[column].mean()) / data[column].std()


def encode_categorical_data(data):
    categorical_columns = data.select_dtypes(include=[np.object]).columns
    data = pd.get_dummies(data, columns=categorical_columns)


def show_new_data():
    print(data)


# GUI function to load, prepare, and show data
def main():
    root = tk.Tk()

    # Create buttons
    load_button = tk.Button(root, text="Load CSV File", command=open_file)
    load_button.pack()

    remove_duplicates_button = tk.Button(root, text="Remove Duplicates", command=check_file_exists)
    remove_duplicates_button.pack()

    remove_corrupted_images_button = tk.Button(root, text="Remove Corrupted Images", command=handle_invalid_file_format)
    remove_corrupted_images_button.pack()

    handle_missing_values_button = tk.Button(
        root, text="Handle Missing Values", command=lambda: fill_missing_values(data, method="mean")
    )
    handle_missing_values_button.pack()

    detect_outliers_button = tk.Button(root, text="Detect Outliers", command=detect_outliers)
    detect_outliers_button.pack()

    scale_normalize_button = tk.Button(root, text="Scale and Normalize", command=lambda: scale_normalize(data))
    scale_normalize_button.pack()

    encode_categorical_data_button = tk.Button(
        root, text="Encode Categorical Data", command=encode_categorical_data
    )
    encode_categorical_data_button.pack()

    show_new_data_button = tk.Button(root, text="Show New Data", command=show_new_data)
    show_new_data_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
