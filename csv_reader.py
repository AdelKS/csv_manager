import csv
import tkinter as tk
from tkinter import filedialog


def get_file_name_with_dialog():
    root = tk.Tk()
    root.withdraw()

    return filedialog.askopenfilename()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class ParsedFile:
    def __init__(self):
        self.val_columns = []
        self.column_names = dict()

class CSV_Reader:
    def __init__(self):
        self.parsed_files = dict()

    def parse(self, csv_file, csv_separator=' '):
        if csv_file in self.parsed_files:
            return
        
        parsing = ParsedFile()
        with open(csv_file) as openFile:
            reader = csv.reader(openFile, delimiter=csv_separator)
            columns = 1
            for row_number, row_content in enumerate(reader):
                if row_number == 0:
                    columns = len(row_content)
                    parsing.val_columns = [ [] for i in range(columns)]
                    for col, val in enumerate(row_content):
                        if is_number(val):
                            parsing.val_columns[col].append(float(val))                           
                        else:
                            parsing.column_names[val] = col
                else:
                    for col, val in enumerate(row_content):
                        if is_number(val):
                            parsing.val_columns[col].append(float(val))
        
        self.parsed_files[csv_file] = parsing

    def get_column(self, csv_file, col):
        # col can be either a string or an integer index
        if not csv_file in self.parsed_files:
            raise "File not loaded beforehand"
        
        
        if is_number(col):
            index = col
        else:
            index = self.parsed_files[csv_file].column_names[col]
        
        return self.parsed_files[csv_file].val_columns[index]

    def free(self, csv_file):
        del self.parsed_files[csv_file]

