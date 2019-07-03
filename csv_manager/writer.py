def write(data_list, file_name, list_type = 'rows', separator=' '):
    r"""
    Writes `data_list` into the file `file_name` in a csv format with `separator`
    as separator. `data_list` can contain variable names to indicate the column names
    in the resulting csv file.d

    Parameters
    ----------
    data_list : a container of 1D containers
        Has to be able to be called data_list[i][j]
    file_name : str
        File name to write to, with eventually the full path
    list_type: 'rows' or 'columns'
        Indicates if `data_list` is a list of 'rows' or a list of 'columns' for
        the script to write the file correctly.
    separator: str
        Separator to use to separate between columns, at the same row. 
    """
    data = open(file_name, 'w')
    if list_type == 'rows':            
        for row in data_list:
            for value in row:
                data.write(str(value) + separator)
            data.write('\n')        
    else:       
        column_count = len(data_list)
        row_count = max([len(col) for col in data_list])
        for i in range(row_count):
            for j in range(column_count):
                if i < len(data_list[j]):
                    data.write(str(data_list[j][i]) + separator)
                else:
                    data.write(separator)
            data.write('\n') 
    data.close()

