import csv
from py_expression_eval import Parser
from pathlib import Path
from .writer import write
import numpy as np

import typing

def identity(val):
    return val

def get_complex(val):
    if is_complex(val):
        return complex(val)
    else:
        return complex("nan")

def is_complex(s):
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
        self.csv_separator = csv_separator
        self.filepath = Path(filepath)
        self.filename = self.filepath.name
        self.filename_var_separator = filename_var_separator
        self.sim_settings = dict()
        self.vars = dict()
        self.num_vars = dict()
        self.unique_pars = dict()
        self.base_name = ""
        self.file_exists = False

        self.columns = []
        self.column_name_to_index = dict()

        self._is_data_loaded = False
        self._update_base_name()

        self.results_possible_col_names = [("result_name", "result_value")]
        self.settings_possible_col_names = [("sim_setting_name", "sim_setting_value"), 
                                            ("setting_name", "setting_value")]

        if self.filepath.is_file():
            self.file_exists = True
            self._read_column_names()        
        
            self._populate_sim_settings()
            self._populate_vars()

    def _update_base_name(self):
        extless_filename = self.filename
        if extless_filename.endswith(".csv"):
            extless_filename = extless_filename[:-4]

        split = extless_filename.split(self.filename_var_separator)    

        self.base_name += split[0]

    def _populate_sim_settings(self):

        self.sim_settings = dict()
        for name_col, val_col in self.settings_possible_col_names:
            self.sim_settings.update(self._load_scalar_results(result_names_col=name_col, result_values_col=val_col))            
        
        if not self.sim_settings:
            # Couldn't find sim settings in the file itself
            # We try to load them from the filename

            extless_filename = self.filepath.name
            if extless_filename.endswith(".csv"):
                extless_filename = extless_filename[:-4]

            split = extless_filename.split(self.filename_var_separator)
        
            first = True
            for string in split:
                if first:
                    first = False
                else:
                    first = False
                    key, value = string.split("=")
                    self.sim_settings[key] = value

        self.unique_pars = self.sim_settings.copy()

    def _read_column_names(self):
       
        with open(self.filepath) as openFile:
            reader = csv.reader(openFile, delimiter=self.csv_separator)
            
            row_content = reader.__next__()

            for col, val in enumerate(row_content):                                   
                col_name = val
                if col_name:  
                    first = True                         
                    while col_name in self.column_name_to_index:
                        if first:
                            col_name += "_"
                            first = False
                        col_name += "b"
                    self.column_name_to_index[col_name] = col

    def move_to_folder(self, folder_path):
        r"""
            move file to new folder, the original file isn't moved nor deleted. a call to `save_to_disk()` is needed
            for the file to be saved in the new folder
        """
        self.filepath = Path(str(folder_path) + "/" + self.filename)

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

        def extend_columns(new_column_num):
            current_row_num = 0
            if self.columns:
                current_row_num = len(self.columns[0])
                assert(all([len(column) == current_row_num for column in self.columns]))
            
            current_column_num = len(self.columns)
            if new_column_num >= current_column_num:
                self.columns += [ ["" for j in range(current_row_num)] for i in range(new_column_num - current_column_num)]

       
        with open(self.filepath) as openFile:
            reader = csv.reader(openFile, delimiter=self.csv_separator)
            self._is_data_loaded = True
        
            for row_number, row_content in enumerate(reader):                
                if row_number > 0:             
                    extend_columns(len(row_content))
                    for col, val in enumerate(row_content):
                        self.columns[col].append(val)
        
        # Delete any eventual empty column
        if all([val == "" for val in self.columns[-1]]):
            del self.columns[-1]
    
    def get_num_var_names(self) -> typing.List[str]:
        r"""
        Returns the list of all numerically valued variables in the datafile
        """
        return self.vars.keys()

    def get_column_names(self) -> typing.List[str]:
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

    def _populate_vars(self):
        self.vars = dict()
        for name_col, val_col in self.results_possible_col_names + self.settings_possible_col_names:
            self.vars.update(self._load_scalar_results(result_names_col=name_col, result_values_col=val_col))
        
        self.num_vars = dict()
        for key, val in self.vars.items():
            try:
                num_val = float(val)
                self.num_vars[key] = num_val
            except:
                pass


    def _load_scalar_results(self, result_names_col, result_values_col):
        scalar_results = dict()

        column_names = self.get_column_names()
        if result_names_col not in column_names or result_values_col not in column_names:
            return scalar_results

        if not self._is_data_loaded:
            with open(self.filepath) as openFile:
                reader = csv.reader(openFile, delimiter=self.csv_separator)
                name_index = column_names.index(result_names_col)
                val_index = column_names.index(result_values_col)
            
                for row_number, row_content in enumerate(reader):                
                    if row_number > 0:             
                        scalar_name = ""
                        scalar_val = ""
                        for col, val in enumerate(row_content):
                            if col == name_index:
                                scalar_name = val
                            elif col == val_index:
                                scalar_val = val
                        if scalar_name and scalar_val:
                            scalar_results[scalar_name] = scalar_val
        
        else:
            names_column = self.get(result_names_col, data_type="string")
            values_column = self.get(result_values_col, data_type="string")

            for name, value in zip(names_column, values_column):
                scalar_results[name] = value
        
        return scalar_results

    def set(self, column_name: str, values: typing.Union[typing.List[float], typing.List[int], typing.List[str], typing.List[complex]]):
        self.column_name_to_index[column_name] = len(self.columns)
        self.columns.append(values.copy())

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

        if self.file_exists and not self._is_data_loaded:
            self._load_data()

        if len(self.columns) == 0:
            raise ValueError("Datafile empty, can't return any data")

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
            var_values_dict = self.num_vars.copy()
                      
            for i in range(len(self.columns[0])):
                for var_name in self.column_name_to_index.keys():
                    var_values_dict[var_name] = data_caster_dict[data_type](self.columns[self.column_name_to_index[var_name]][i])
                vals.append(expr.evaluate(var_values_dict))

            return vals
    
    def append_to_columns(self, new_vals: dict) -> None:
        r"""
        Append each value pointed by new_vals at the end of each corresponding column in the datafile. 
        If the columns that get appended don't have the same size, they get appended empty values so
        they are all the same size first.

        Parameters
        ----------

        new_vals : dict[str, str] or dict[str, float] or dict[str, complex]
            A dictionnary containing the (column_name, new_value) pairs, where `new_value` is to be appended
            to `column_name`

        """
        # First: check that the user provided correct input
        for col_name, new_val in new_vals.items():
            if not (isinstance(col_name, str) and \
                isinstance(new_val, (str, bool, int, float, complex, np.int, np.complex, np.float))):
                raise ValueError("Provided `new_vals` doesn't have the correct types, aka a dict[str, number or str]")
        
        # Load data if not already done
        if self.file_exists and not self._is_data_loaded:
            self._load_data()
        
        # Second: create empty columns if they don't exist
        for col_name in new_vals.keys():
            if col_name not in self.column_name_to_index.keys():
                self.set(col_name, [])

        # Third: get size of biggest column in-file from new_vals keys
        biggest_col_size = 0        
        for col_name in new_vals.keys():
            size = len(self.columns[self.column_name_to_index[col_name]])
            if size > biggest_col_size:
                biggest_col_size = size
        
        # Fourth: append empty string to smaller columns if needed
        for col_name in new_vals.keys():
            diff = biggest_col_size - len(self.columns[self.column_name_to_index[col_name]])
            if diff > 0:
                for i in range(diff):
                    self.columns[self.column_name_to_index[col_name]].append("")
        
        # Fifth: append the new values
        for col_name, new_val in new_vals.items():
            self.columns[self.column_name_to_index[col_name]].append(str(new_val))

    def save_to_disk(self, column_name_order=None):
        r"""
            Saves the file's data to disk.
            Warning: if the Datafile has been loaded from a file, it will overwrite it with any changes that has been made 
            to the class instance.
        """
        remaining_column_names = [name for (name, index) in sorted(self.column_name_to_index.items(), key=lambda item: item[1])]
        data_array = []
        if column_name_order:
            for column_name in column_name_order:
                if column_name in remaining_column_names:
                    remaining_column_names.remove(column_name)
                    data_array += [[column_name, *self.columns[self.column_name_to_index[column_name]]]]

        data_array += [[key, *self.columns[self.column_name_to_index[key]]] for key in remaining_column_names]
        write(data_array, self.filepath, list_type = 'columns', separator=' ')