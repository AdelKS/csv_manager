from pathlib import Path
from typing import List

class DataFile:
    def __init__(self, filepath = "", var_separator = "|"):
        self.file_base = ""
        self.filepath = filepath
        self.var_separator = var_separator
        self.pars = dict()
        self.unique_pars = dict()
        self.base_name = ""

        self._populate_pars()

    def _populate_pars(self):
        self.filename = Path(self.filepath).name
        if self.filename.endswith(".csv"):
            self.filename = self.filename[:-4]

        split = self.filename.split(self.var_separator)
    
        first = True
        for string in split:
            if first and "=" not in string:
                self.base_name += string
                self.file_base += string.replace("_", " ")
            else:
                first = False
                key, value = string.split("=")
                self.pars[key] = value

    def compute_unique_pars(self, datafiles):
        self.unique_pars.clear()
        for i, datafile in enumerate(datafiles):
            if str(datafile.filepath) != str(self.filepath):
                for key, val in self.pars.items():
                    if key not in datafile.pars.keys() or val != datafile.pars[key]:
                        self.unique_pars[key] = val

class Database:
    def __init__(self, data_folder_path: str = "", file_var_separator: str = "|"):   

        self.datafiles = []
        self.data_folder = data_folder_path
        self.filepaths = []
        self.datafilesnum = 0

        if self.data_folder:
            self._populate_database()

    def set_data_folder(self, data_folder : str):
        self.data_folder = data_folder

    def _populate_database(self):
        self.filepaths = list(Path(self.data_folder).rglob("*.csv"))
        self.datafiles = [DataFile(str(filepath)) for filepath in self.filepaths]
        self.datafilesnum = len(self.datafiles)
    
    def filter_datafiles(self, file_name_base: str, filter_dict : dict) -> List[DataFile]:
        filtered_datafiles = []
        for datafile in self.datafiles:
            if file_name_base in datafile.base_name and all([item in datafile.pars.items() for item in filter_dict.items()]):
                filtered_datafiles.append(datafile)
        
        for filtered_datafile in filtered_datafiles:
            filtered_datafile.compute_unique_pars(filtered_datafiles)

        return filtered_datafiles


    