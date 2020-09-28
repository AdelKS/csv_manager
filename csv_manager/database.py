from pathlib import Path
from typing import List

from .datafile import DataFile

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

class Database:
    def __init__(self):
        self.datafiles = []

    def load_from_folder(self, data_folder_path, csv_separator=" ", file_var_separator="|"):
        """
            Load all CSV files form the given folder
        """

        filepaths = list(Path(data_folder_path).rglob("*.csv"))
        self.datafiles += [DataFile(str(filepath), csv_separator=csv_separator, var_separator=file_var_separator) for filepath in filepaths]

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
                shortened_filename = datafile.base_name + dict_to_string(datafile.unique_pars, separator=datafile.filename_var_separator)               
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

    def filter_datafiles(self, keywords: list, filter_dict : dict) -> List[DataFile]:
        filtered_datafiles = []
        for datafile in self.datafiles:
            if all([keyword in datafile.base_name for keyword in keywords]) and all([item in datafile.sim_settings.items() for item in filter_dict.items()]):
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

    def slice(self, sim_setting_name, filtered_datafiles=None):
        """
            Returns a list of lists of DataFile, each list contains Datafiles that share 
            the same values of all their sim_pars except the one given in `sim_setting_name`
            Datafiles that don't share all their sim_par values (except `sim_setting_name`) with any other Datafile
            are omitted.
        """
        if filtered_datafiles == None:
            filtered_datafiles = self.datafiles

        slicing = []
        n = len(filtered_datafiles)
        for i in range(n):
            file1 = filtered_datafiles[i]
            slice = [file1]
            for j in range(i+1, n):
                file2 = filtered_datafiles[2]
                if set(file1.sim_settings.keys()) == set(file2.sim_settings.keys()) and \
                    all([file1.sim_settings[key] == file2.sim_settings[key] for key in file1.sim_settings.keys() if key != sim_setting_name]):
                    slice.append(file2)
            if len(slice) >= 2:
                slicing.append(slice)        
        return slicing
                



    