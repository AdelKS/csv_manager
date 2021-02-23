from pathlib import Path
from typing import List, Union

from .datafile import DataFile
from .misc import *

import time

class Database:
    def __init__(self, data_folder_path=None, csv_separator=" ", filename_var_separator="|"):
        self.datafiles = []
        self.result_names_col = None
        self.result_values_col = None
        self.sim_settings_names_col = None
        self.sim_settings_values_col = None

        if data_folder_path:
            self.load_from_folder(data_folder_path, csv_separator, filename_var_separator)

    def set_scalar_result_column_names(self, result_names_col: str, result_values_col: str):
        r"""
        Set the column names of the columns that contain respectively the sim_results variable names
        and the column containing their values

        Parameters
        ----------

        result_names_col : str
            Name of the column that contains the scalar result variable names

        result_values_col : str
            Name of the column that contains the scalar result variable values
        """

        self.result_names_col = result_names_col
        self.result_values_col = result_values_col
    
    def set_sim_settings_column_names(self, sim_settings_names_col: str, sim_settings_values_col: str):
        r"""
        Set the column names of the columns that contain respectively the sim_results variable names
        and the column containing their values

        Parameters
        ----------

        result_names_col : str
            Name of the column that contains the scalar result variable names

        result_values_col : str
            Name of the column that contains the scalar result variable values
        """

        self.sim_settings_names_col = sim_settings_names_col
        self.sim_settings_values_col = sim_settings_values_col

    def add(self, datafiles):
        if isinstance(datafiles, list):
            for datafile in datafiles:
                assert(isinstance(datafile, DataFile))
                self.datafiles.append(datafile)
        elif isinstance(datafiles, DataFile):
            self.datafiles.append(datafiles)

    def load_from_folder(self, data_folder_path, csv_separator=" ", filename_var_separator="|"):
        """
            Load all CSV files form the given folder
        """
        print("Querying available CSV files")
        filepaths = list(Path(data_folder_path).rglob("*.csv"))
        
        start = time.perf_counter()        
        current_elapsed_time = 0
        self.datafiles = []
        N = len(filepaths)

        print("Loading {} CSV files in database".format(N))
        for index, filepath in enumerate(filepaths):
            self.datafiles.append(DataFile(str(filepath), csv_separator=csv_separator, filename_var_separator=filename_var_separator))
            new_elapsed_time = int(time.perf_counter() - start)
            if new_elapsed_time != current_elapsed_time:
                current_elapsed_time = new_elapsed_time
                print("  Progress = {:.0f} %".format(100*(index+1)/N))

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
        available_files = self.datafiles

        while True:    
            print("#################################")

            if filter_dict or keywords:
                available_files = self.filter_datafiles(available_files, keywords, filter_dict)  

            if already_selected_files:
                self.compute_unique_pars(already_selected_files)
                self.sort_vs_unique_pars(already_selected_files)  
            elif len(available_files) <= 50:
                self.compute_unique_pars(available_files)
                self.sort_vs_unique_pars(available_files)            
            
            print("Available files: ")  
            max_len = min(100, len(available_files))      
            for i, datafile in reversed(list(enumerate(available_files[:max_len]))):
                shortened_filename = datafile.base_name + dict_to_string(datafile.unique_pars, separator=datafile.filename_var_separator)               
                print("    {0})  {1}".format(i+1, shortened_filename))
            
            if len(available_files) > 100:
                print("################################################################################")
                print("NOTE: Number of available files is too big and got truncated,")
                print("      please use filters to query the entire database")
                print("################################################################################")
            
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

            chosen_index = input("File wanted [1,{0}]: ".format(len(available_files[:max_len])))
            if not chosen_index:
                pass
            elif chosen_index=="done":
                return None
            elif chosen_index == "filter clear":
                keywords.clear()
                filter_dict.clear()
                available_files = self.datafiles
            elif chosen_index.startswith("filter"):
                print("Parsing: " + chosen_index[7:])
                extra_keywords, extra_filters = parse_filter_command(chosen_index[7:])
                keywords += extra_keywords
                filter_dict.update(extra_filters)
            elif chosen_index.startswith("file"):
                filename = chosen_index[5:]
                for datafile in self.datafiles:
                    if filename in datafile.filename:
                        return datafile
                print("File not found")
            else:
                try:
                    index = int(chosen_index)
                    return available_files[index-1]
                except:
                    print("Input not recognized, please try again")

    def filter_datafiles(self, datafiles, keywords: Union[list, str] = [], filter_dict : dict = dict()) -> List[DataFile]:
        filtered_datafiles = []

        if isinstance(keywords, str):
            keywords=[keywords]

        for datafile in datafiles:
            if all([keyword in datafile.base_name for keyword in keywords]) and \
                set(filter_dict.keys()) <= set(datafile.sim_settings.keys()) and \
                all([datafile.sim_settings[filter_key].startswith(filter_val) for filter_key, filter_val in filter_dict.items()]):

                filtered_datafiles.append(datafile)
        
        for filtered_datafile in filtered_datafiles:
            filtered_datafile.compute_unique_pars(filtered_datafiles)

        return filtered_datafiles

    def compute_unique_pars(self, datafiles_subset : list):
        """ 
        Computes the unique parameters for each datafile among the datafiles in datafiles_subset
        """
        for datafile in datafiles_subset:
            datafile.compute_unique_pars(datafiles_subset)
    
    def sort_vs_unique_pars(self, datafiles):
        datafiles.sort(key=lambda datafile: len(datafile.unique_pars))

    def slice(self, sim_setting_name: str, match_basename: bool=True, datafiles_subset: List[DataFile]=None):
        r"""
            Returns a list of DataFile objects that share the same `sim_settings` except the one given in `sim_setting_name`,
            each DataFile will compile the values of the `scalar_results` of the original files. The filename of the newly created
            files will take the basename of the files that got regroupped + "_vs_" + `sim_setting_name`, along with the sim_settings.
            Datafiles that don't share all their sim_par values (except `sim_setting_name`) with any other Datafile
            are omitted.

            Parameters
            ----------

            sim_setting_name : str
                The name of the sim_setting that is permitted to vary, all the others will be fixed (per newly created DataFile)

            match_basename : bool
                The desired column name to retrieve, or mathematical expression involving the dataset's column
                names to calculate and return

            datafiles_subset : list[DataFile] or None
                a subset of DataFile objects to look into, if set to None, all the DataFiles loaded in the Database instance
                will be used.

            Returns
            -------

            A list of `type` containing the result of `expr`
        """
        if datafiles_subset == None:
            datafiles_subset = self.datafiles

        # first: calcualte a List of List of Datafiles
        slicings = []
        n = len(datafiles_subset)
        remaining_datafiles = set(datafiles_subset)
        while len(remaining_datafiles) >= 2:
            file1 = remaining_datafiles.pop()            

            #pick a file that contains `sim_setting_name` in it sim_settings keys
            if sim_setting_name not in file1.sim_settings.keys():
                continue
            
            data_slice = []
            for file2 in remaining_datafiles:
                if (not match_basename or file1.base_name == file2.base_name) and \
                    set(file1.sim_settings.keys()) == set(file2.sim_settings.keys()) and \
                    all([key == sim_setting_name or file1.sim_settings[key] == file2.sim_settings[key] for key in file1.sim_settings.keys()]):
                    data_slice.append(file2)
            if data_slice:
                for file in data_slice:
                    remaining_datafiles.remove(file)
                data_slice.append(file1)
                slicings.append(data_slice)
        # Done
        # 
        # Second: create new datafiles from each DataFile list 
        
        new_datafiles = []
        for slicing in slicings:
            file = slicing[0]
            sim_settings = file.sim_settings.copy()
            del sim_settings[sim_setting_name]
            parent_folder = str(Path(file.filepath).parent)

            columns = dict()

            # Define all possible key values and load scalar values
            all_keys = set()
            for file in slicing:
                file.load_scalar_results(self.result_names_col, self.result_values_col)
                all_keys.update(set(file.sim_scalar_results.keys()))
            
            for key in all_keys:
                columns[key] = []
            
            #initialise columns[sim_setting_name] if not present in all_keys
            sim_setting_name_already_present = True
            if sim_setting_name not in all_keys:
                sim_setting_name_already_present = False
                columns[sim_setting_name] = []

            for file in slicing:
                #Append empty values for non exisiting keys
                sub_keys = file.sim_scalar_results.keys()
                diff = all_keys - sub_keys
                for key in diff:
                    columns[key].append("")
                
                # append existing values
                for key, val in file.sim_scalar_results.items():
                    columns[key].append(val)

                # append the value of `sim_setting_name`
                if not sim_setting_name_already_present:
                    columns[sim_setting_name].append(file.sim_settings[sim_setting_name])

            filepath = parent_folder + "/" + file.base_name + "_vs_" + sim_setting_name + dict_to_string(sim_settings) + ".csv"
            datafile = DataFile(filepath)

            for key, vals in columns.items():
                datafile.set(key, vals)
            
            new_datafiles.append(datafile)
        
        return new_datafiles




    