from pathlib import Path
from typing import List

def concatenate(string_list, inter_prepend="", return_prepend="", return_every=None):
    res = return_prepend
    for i, string in enumerate(string_list):
        res += string + "," + inter_prepend
        if return_every and i % return_every == 0 and i != 0:
            res += "\n" + return_prepend
    return res


def dict_to_string(dic, separator = "|"):
    extension = str()
    if dic:
        extension += separator
    for i, (key, val) in enumerate(sorted(dic.items())):
        if isinstance(val, float):
            extension += key + "=" + "{0:.5g}".format(val)
        else:
            extension += key + "=" + str(val)
        if i < len(dic) - 1:
            extension += separator
    return extension

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

        self.unique_pars = self.pars.copy()

    def compute_unique_pars(self, datafiles):
        self.unique_pars.clear()
        for key, val in self.pars.items():
            if not all([key in datafile.pars.keys() and val == datafile.pars[key] for datafile in datafiles]):
                self.unique_pars[key] = val

class Database:
    def __init__(self, data_folder_path: str = "", file_var_separator: str = "|"):   

        self.datafiles = []
        self.data_folder = data_folder_path
        self.filepaths = []
        self.datafilesnum = 0
        self.file_var_separator = file_var_separator

        if self.data_folder:
            self._populate_database()

    def file_selection_prompt(self, already_selected_files : List[DataFile] = list()) -> DataFile :

        def parse_filter_command(command_str):
            keywords = []
            filter_dict = {}
            for equality in command_str.split(" "):
                split = equality.split("=")
                if len(split) != 2:
                    raise ValueError("Error parsing this: ", equality)
                else:
                    if split[0] == "contains":
                        keywords.append(split[1])
                    else:
                        filter_dict[split[0]] = split[1]
            return keywords, filter_dict
        
        keywords = []
        filter_dict = {}
        available_files = []

        while True:    
            print("#################################")

            available_files = self.datafiles

            if already_selected_files:
                self.compute_unique_pars(already_selected_files)
                self.sort_vs_unique_pars()

            if filter_dict or keywords:
                available_files = self.filter_datafiles(keywords, filter_dict)    
            
            print("Available files: ")        
            for i, datafile in reversed(list(enumerate(available_files))):
                shortened_filename = datafile.base_name + dict_to_string(datafile.unique_pars, separator=self.file_var_separator)               
                print("    {0})  {1}".format(i+1, shortened_filename))
            
            if filter_dict or keywords:
                print("Used filters:")
                if keywords:                
                    print("    Contains: " + concatenate(keywords, inter_prepend=" "))

                if filter_dict:
                    filter_string = ""
                    for key, val in filter_dict.items():
                        filter_string += "{0}={1}  ".format(key, val)
                    print("    Variable definitions: " + filter_string) 

            if already_selected_files:            
                print("Already selected files: ")
                for plotted_datafile in already_selected_files:
                    print("    - " + plotted_datafile.filename)

            chosen_index = input("File wanted [1,{0}]: ".format(len(available_files)))
            if not chosen_index:
                return None
            elif chosen_index == "filter clear":
                keywords.clear()
                filter_dict.clear()
            elif chosen_index.startswith("filter"):
                print("Parsing: " + chosen_index[7:])
                extra_keywords, extra_filters = parse_filter_command(chosen_index[7:])
                keywords += extra_keywords
                filter_dict.update(extra_filters)
            else:
                return available_files[int(chosen_index)-1]

    def set_data_folder(self, data_folder : str):
        self.data_folder = data_folder

    def _populate_database(self):
        self.filepaths = list(Path(self.data_folder).rglob("*.csv"))
        self.datafiles = [DataFile(str(filepath)) for filepath in self.filepaths]
        self.datafilesnum = len(self.datafiles)
    
    def filter_datafiles(self, keywords: list, filter_dict : dict) -> List[DataFile]:
        filtered_datafiles = []
        for datafile in self.datafiles:
            if all([keyword in datafile.base_name for keyword in keywords]) and all([item in datafile.pars.items() for item in filter_dict.items()]):
                filtered_datafiles.append(datafile)
        
        for filtered_datafile in filtered_datafiles:
            filtered_datafile.compute_unique_pars(filtered_datafiles)

        return filtered_datafiles

    def compute_unique_pars(self, datafiles_subset : list):
        """ 
        Computes the unique parameters for each datafile in self.datafiles with respect
        to datafules_subset list.
        """
        for datafile in self.datafiles:
            datafile.compute_unique_pars(datafiles_subset)
    
    def sort_vs_unique_pars(self):
        self.datafiles.sort(key=lambda datafile: len(datafile.unique_pars))


    