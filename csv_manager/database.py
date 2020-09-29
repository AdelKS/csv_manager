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


    def load_from_folder(self, data_folder_path, csv_separator=" ", filename_var_separator="|"):
        """
            Load all CSV files form the given folder
        """

        filepaths = list(Path(data_folder_path).rglob("*.csv"))
        self.datafiles += [DataFile(str(filepath), csv_separator=csv_separator, filename_var_separator=filename_var_separator) for filepath in filepaths]

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
            while sim_setting_name not in file1.sim_settings.keys():
                file1 = remaining_datafiles.pop()
            
            data_slice = []
            for file2 in remaining_datafiles:
                if (not match_basename or file1.base_name == file2.base_name) and \
                    set(file1.sim_settings.keys()) == set(file2.sim_settings.keys()) and \
                    all([file1.sim_settings[key] == file2.sim_settings[key] for key in file1.sim_settings.keys() if key != sim_setting_name]):
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
                datafile.assign(key, vals)
            
            new_datafiles.append(datafile)
        
        return new_datafiles




    