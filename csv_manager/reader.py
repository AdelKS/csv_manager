import csv
import tkinter as tk
from tkinter import filedialog
from py_expression_eval import Parser


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
        self.column_vals = []
        self.column_names = dict()

class Reader:
    def __init__(self):
        self.parsed_files = dict()
        self.file_aliases = dict()

    def load(self, csv_file, alias=None, csv_separator=' '):       

        if alias != None:
            self.file_aliases[alias] = csv_file
       
        self.file_aliases[csv_file] = csv_file     
        
        parsing = ParsedFile()
        last_column_empty = True
        with open(csv_file) as openFile:
            reader = csv.reader(openFile, delimiter=csv_separator)
            columns = 1
            for row_number, row_content in enumerate(reader):                
                if row_content[-1]:
                    last_column_empty = False
                if row_number == 0:
                    columns = len(row_content)
                    parsing.column_vals = [ [] for i in range(columns)]
                    for col, val in enumerate(row_content):
                        if is_number(val):
                            parsing.column_vals[col].append(float(val))                           
                        else:
                            parsing.column_names[val] = col
                else:                    
                    if row_content[-1]:
                        last_column_empty = False
                    for col, val in enumerate(row_content):
                        if is_number(val):
                            parsing.column_vals[col].append(float(val))
        
        if last_column_empty:
            # last column empty, removing it 
            del parsing.column_vals[-1]
            del parsing.column_names['']

        self.parsed_files[csv_file] = parsing

    def get(self, file_alias, expr):
        # col can be either a string or an integer index
        if not self.file_aliases[file_alias] in self.parsed_files:
            raise EnvironmentError("CSV File not loaded beforehand" )  

        col_names = self.parsed_files[self.file_aliases[file_alias]].column_names
        col_vals = self.parsed_files[self.file_aliases[file_alias]].column_vals
        
        if is_number(expr):
            # the column's index is given
            index = expr
            return col_vals[index]
        
        elif expr in col_names:
            # a column name has been given
            return col_vals[col_names[expr]]
        
        else:
            # Assume that col general mathematical expression, involving column names as variables
            parser = Parser()
            expr = parser.parse(expr)
            vals = []
            var_values_dict = dict()
                      
            for i in range(len(col_vals[0])):
                for var_name in col_names.keys():
                    var_values_dict[var_name] = col_vals[col_names[var_name]][i]
                vals.append(expr.evaluate(var_values_dict))

            return vals       

    def free(self, csv_file):
        del self.parsed_files[csv_file]
        for key in self.file_aliases:
            if self.file_aliases[key] == csv_file:
                del self.file_aliases[key]
