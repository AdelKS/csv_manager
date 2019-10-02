import csv
import tkinter as tk
from tkinter import filedialog
from py_expression_eval import Parser

import typing


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
    r"""
    CSV reader class, can load CSV files with arbitrary separators. It can 
    return separately any column of any file in a list and can also return the 
    of the mathematical combinations of the file's columns.
    """

    def __init__(self):
        self.parsed_files = dict()
        self.file_aliases = dict()

    def load(self, csv_file: str, alias : str = None, csv_separator : str = ' ') -> None:       
        r"""
        Loads the CSV file pointed by `csv_file` into memory. This step
        should be done first before requesting any data from the file through
        `get([...])`

        Parameters
        ----------

        csv_file : str
            The absolute or relative path to the file to load.

        alias : str
            The alias to give to the file, the file can be referred to with its alias 
            when querying data from it.

        csv_separator : str
            The separator string used to separate between columns at any given line in the 
            CSV file. The default is a blank space ' ' (even though the name CSV says otherwise)

        """
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
                            parsing.column_names[col+1] = col # the column's name is its index (starting from 1)
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


    def get_column_names(self, alias: str) -> typing.List[str]:
        r"""
        Returns the list of columns names of the loaded file given referenced by alias.

        Parameters
        ----------

        alias : str
            The file name or alias of loaded file for which to return the column names. 

        Returns
        -------

        A list of strings, each being a column name
        """

        parsing = self.parsed_files[self.file_aliases[alias]]
        return list(parsing.column_names.keys())      


    def show_loaded_data(self, alias : str = None) -> None:
        r"""
        Prints to stdout the file names whose data have been loaded, their alias (if set) 
        and the their column names.
        
        Parameters
        -----------
        alias : str
            The file name or alias of the specific file for which the column names will shown. 
            If not specified, all loaded files will be shown.	
        """

        if not alias:
            for (file_name, parsing) in self.parsed_files.items():
                print("----------------------------------------")
                print("File: ", file_name)
                aliases = [nick for (nick, file) in self.file_aliases.items() if (file_name == file and nick != file_name)]
                if aliases:
                    print("Alias: ", aliases[0])
                print("Column names: ")
                for name in parsing.column_names.keys():
                    print("   ", name)

        else:
            print("----------------------------------------")
            print("File: ", [file_name for (nick, file_name) in self.file_aliases.items() if nick == alias][0])
            print("Alias: ", alias)

            parsing = self.parsed_files[self.file_aliases[alias]]
            print("Column names: ")
            for name in parsing.column_names.keys():
                print("   ", name)



    def get(self, file_alias: str, expr: str) -> typing.List[float]:
        r"""
        Returns the column whose name is given by `expr`, from the file given in `file_alias`.
        Note that `expr` can be a mathematical expression, like :math:` 2 * time + offset`
        where `time` and `offset` are two column names.

        Parameters
        ----------

        file_alias : str
            The desired file path of alias from which to retrieve/calculate `expr`

        expr : str
            The desired column name to retrieve, or mathematical expression involving the file's column
            names to calculate and retrieve

        Returns
        -------

        A list of floats containing the result of `expr`

        """

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

    def delete(self, file_alias : str) -> None:
        r"""
        Unload the perviously loaded `csv_file` from memory

        Parameters:
        -----------

        file_alias : str
            Alias of file path (as given when the file has been loaded) to be unloaded from memory

        """
        del self.parsed_files[self.file_aliases[file_alias]]
        for key in self.file_aliases:
            if self.file_aliases[key] == csv_file:
                del self.file_aliases[key]
