import csv
from py_expression_eval import Parser
from pathlib import Path

import typing

def identity(val):
    return val

def get_complex(val):
    if is_complex(val):
        return complex(val)
    else:
        return complex("nan")

def is_integer(s):
    try:
        complex(s)
        return True
    except ValueError:
        return False

def get_integer(val):
    if is_integer(val):
        return int(val)
    else:
         raise ValueError("Casting a non integer value: ", val)

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_float(val):
    if is_float(val):
        return float(val)
    else:
        return float("nan")

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class DataFile:
    r"""
        A class that represents a single CSV file, can load CSV files with arbitrary separators. It can 
        return separately any column of the file and any mathematical combinations of its columns.
    """

    def __init__(self, filepath="", filename_var_separator="|", csv_separator=" "):
        self.file_base = ""
        self.csv_separator = csv_separator
        self.filepath = Path(filepath)
        self.filename_var_separator = filename_var_separator
        self.sim_settings = dict()
        self.unique_pars = dict()
        self.base_name = ""

        self.columns = []
        self.column_name_to_index = dict()

        self.is_data_loaded = False

        self._populate_pars()
        self._read_column_names()

    def _populate_pars(self):
        self.filename = self.filepath.name
        if self.filename.endswith(".csv"):
            self.filename = self.filename[:-4]

        split = self.filename.split(self.filename_var_separator)
    
        first = True
        for string in split:
            if first and "=" not in string:
                self.base_name += string
                self.file_base += string.replace("_", " ")
            else:
                first = False
                key, value = string.split("=")
                self.sim_settings[key] = value

        self.unique_pars = self.sim_settings.copy()

    def _read_column_names(self):  
       
        with open(self.filepath) as openFile:
            reader = csv.reader(openFile, delimiter=self.csv_separator)
            
            row_content = reader.__next__()
            self.columns = [ [] for i in range(len(row_content))]

            for col, val in enumerate(row_content):                                   
                col_name = val      
                first = True                         
                while col_name in self.column_name_to_index:
                    if first:
                        col_name += "_"
                        first = False
                    col_name += "b"
                self.column_name_to_index[col_name] = col

    def compute_unique_pars(self, datafiles):
        self.unique_pars.clear()
        for key, val in self.sim_settings.items():
            if not all([key in datafile.sim_settings.keys() and val == datafile.sim_settings[key] for datafile in datafiles]):
                self.unique_pars[key] = val

    def _load_data(self):   
        r"""
        Loads the CSV file pointed by `csv_file` into memory. This step
        should be done first before requesting any data from the file through
        `get([...])`

        Parameters
        ----------

        csv_file : str
            The absolute or relative path to the file to load.

        alias : str
            The alias to give to the file, the data in the file can be accessed with it. If
            the user loads two files and give the same alias for both, their data will be put
            together: if two columns share the same name the last one loaded will have "_b" 
            appended to its name.

        csv_separator : str
            The separator string used to separate between columns at any given line in the 
            CSV file. The default is a blank space ' ' (even though the name CSV says otherwise)

        """         
       
        with open(self.filepath) as openFile:
            reader = csv.reader(openFile, delimiter=self.csv_separator)
        
            for row_number, row_content in enumerate(reader):                
                if row_number > 0:             
                    for col, val in enumerate(row_content):
                        self.columns[col].append(val)


    def get_column_names(self, alias: str) -> typing.List[str]:
        r"""
        Returns the list of columns names of the loaded file given referenced by alias.

        Parameters
        ----------

        alias : str
            The alias of the dataset for which to return the column names. 

        Returns
        -------

        A list of strings, each being a column name
        """
        
        return list(self.column_name_to_index.keys())


    def get(self, expr: str, data_type: str = "float") -> typing.List[typing.Union[float, str, int, complex]]:
        r"""
        Returns the column whose name is given by `expr`, from the file given in `file_alias`.
        Note that `expr` can be a mathematical expression, like :math:` 2 * time + offset`
        where `time` and `offset` are two column names.

        Parameters
        ----------

        alias : str
            The alias of the dataset to get data from

        expr : str
            The desired column name to retrieve, or mathematical expression involving the dataset's column
            names to calculate and return

        data_type : str
            "string", "integer", "float" or "complex", the type in which method tries to cast the data to before returning it.
            If `expr' is a mathematical expression, `type' can't be "string"

        Returns
        -------

        A list of `type` containing the result of `expr`

        """

        data_caster_dict = {"string": identity, "float": get_float, "integer": get_integer, "complex": get_complex}

        if data_type not in data_caster_dict.keys():
            raise ValueError("the given `data_type' doesn't match any known types. Which are `string', `integer', `float' or `complex'")

        if is_integer(expr):
            # the column's index is given
            index = expr
            return [data_caster_dict[data_type](val) for val in self.columns[index]]
        
        elif expr in self.column_name_to_index:
            # a column name has been given
            return [data_caster_dict[data_type](val) for val in self.columns[self.column_name_to_index[expr]]]
        
        else:
            if data_type == "string":
                raise ValueError(" `data_type' can't be `string' if a mathematical expression is asked ")
            # Assume that col general mathematical expression, involving column names as variables
            parser = Parser()
            expr = parser.parse(expr)
            vals = []
            var_values_dict = dict()
                      
            for i in range(len(self.columns[0])):
                for var_name in self.column_name_to_index.keys():
                    var_values_dict[var_name] = data_caster_dict[data_type](self.columns[self.column_name_to_index[var_name]][i])
                vals.append(expr.evaluate(var_values_dict))

            return vals       