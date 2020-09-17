import csv
from py_expression_eval import Parser

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


class DataSet:
    def __init__(self):
        self.column_vals = []
        self.column_names = dict()
        self.source_files = []

class Reader:
    r"""
    CSV reader class, can load CSV files with arbitrary separators. It can 
    return separately any column of any file in a list and can also return the 
    of the mathematical combinations of the file's columns.
    """

    def __init__(self):
        self.datasets = dict()      

    def load(self, csv_file: str, alias : str, csv_separator : str = ' ') -> None:       
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

        if not isinstance(alias, str):
            raise ValueError("A string alias must be given for the csv file to load.")        
       
        with open(csv_file) as openFile:
            reader = csv.reader(openFile, delimiter=csv_separator)
            
            dataset = None
            if alias in self.datasets.keys():
                dataset = self.datasets[alias]
            else:
                self.datasets[alias] = DataSet()
                dataset = self.datasets[alias]

            dataset.source_files.append(csv_file)
        
            last_column_empty = True

            columns = 1
            start_col = 0
            for row_number, row_content in enumerate(reader):                
                if row_content[-1]:
                    last_column_empty = False
                if row_number == 0:
                    columns = len(row_content)
                    start_col = len(dataset.column_vals)
                    dataset.column_vals.extend([ [] for i in range(columns)])
                    for col, val in enumerate(row_content):
                        col_ind = col + start_col                        
                        col_name = val                               
                        while col_name in dataset.column_names:
                            col_name += "_b"
                        dataset.column_names[col_name] = col_ind
                else:                    
                    if row_content[-1]:
                        last_column_empty = False
                    for col, val in enumerate(row_content):
                        col_ind = col + start_col
                        dataset.column_vals[col_ind].append(val)
        
            if last_column_empty:
                # last column empty, removing it 
                del dataset.column_vals[-1]
                del dataset.column_names['']


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
        
        return list(self.datasets[alias].column_names.keys())      


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
            for alias, dataset in self.datasets.items():
                print("----------------------------------------")
                print("Dataset alias: ", alias)
                print("Source files:")
                for source_file in dataset.source_files:
                    print("\t", source_file)               
                print("Column names: ")
                for name in dataset.column_names.keys():
                    print("\t", name)

        else:
            print("----------------------------------------")
            dataset = self.datasets[alias]
            print("Dataset alias: ", alias)
            print("Source files:")
            for source_file in dataset.source_files:
                print("\t", source_file)               
            print("Column names: ")
            for name in dataset.column_names.keys():
                print("\t", name)



    def get(self, alias: str, expr: str, data_type: str = "float") -> typing.List[typing.Union[float, str, int, complex]]:
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

        # col can be either a string or an integer index
        if alias not in self.datasets.keys():
            raise ValueError("Alias doesn't exist.")

        col_names = self.datasets[alias].column_names
        col_vals = self.datasets[alias].column_vals
        
        if is_integer(expr):
            # the column's index is given
            index = expr
            return [data_caster_dict[data_type](val) for val in col_vals[index]]
        
        elif expr in col_names:
            # a column name has been given
            return [data_caster_dict[data_type](val) for val in col_vals[col_names[expr]]]
        
        else:
            if data_type == "string":
                raise ValueError(" `data_type' can't be `string' if a mathematical expression is asked ")
            # Assume that col general mathematical expression, involving column names as variables
            parser = Parser()
            expr = parser.parse(expr)
            vals = []
            var_values_dict = dict()
                      
            for i in range(len(col_vals[0])):
                for var_name in col_names.keys():
                    var_values_dict[var_name] = data_caster_dict[data_type](col_vals[col_names[var_name]][i])
                vals.append(expr.evaluate(var_values_dict))

            return vals       

    def delete(self, alias : str) -> None:
        r"""
        Unload a dataset from memory

        Parameters:
        -----------

        alias : str
            Alias of the dataset to be unloaded from memory

        """
        if alias in self.datasets.keys():
            del self.datasets[alias]
       
