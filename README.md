## csv_manager

This is a python module that features three simple classes for reading (class `Reader`), plotting (class `Plotter`, using Matplotlib with Latex rendering enabled) for the plots) and managing (class `Database`) CSV files and also a method for writing CSVs.

By using this module, the user avoids the cumbersome repetition of coding a csv reader using the `csv` python library then making the data in a readable structure for `plt.plot(...)`.

#### Simple single graph example

```python
from csv_manager import Plotter, DataFile
# Plotter inherits the class Reader

plotter = Plotter()
# Number of rows and columns for plt.sublots

datafile = DataFile('data_file_1.csv')

datafile.get_column_names('dataset1')
# returns the list of column names of the file `data_file_1.csv`

######################################################

plotter.plot(datafile, 'time', 'position', label='position $x(t)$', color='red', linestyle=':')
# Starting from " label='save' [...]" the arguments are the **kwargs in https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
plotter.plot(datafile, 'time', 'speed', label='speed $v(t)$', color='blue', linestyle='--')

plotter.plot(datafile, 'time', 'position + sqrt(2/10 * speed)', 0, 1, label='dummy curve from expression')
# Mathematical expressions involving column names can be used

plotter.plot_data([0, 1, 2], [0, 1, 2], label='dummy data')

plotter.set(xlabel='Time ', ylabel='Position')
# the options that can be set are the **kwargs in https://matplotlib.org/api/axes_api.html

plotter.show()
```

The file `data_file_1.csv` can be the followin (Note that the default column separator is a single space):

```csv
time position speed
0 0 0
1 5 3
2 20 3.6
3 45 2
4 80 5
5 125 8
6 180 9
7 245 10
8 320 9.2
9 405 8
10 500 7
```

#### Using `Database`

If you have a folder with lots of CSV files and find it too cumbersome to find the correct ones to plot or read. The class `Databse` is made for you!

Requirements:
- Have all your CSV files in a folder (still works if they are in a subfolder of that folder)
- One of the following (or both):
    - Follow a specific naming scheme on your CSV files: `filename|var1=val1|var2=val2|...|varN=valN.csv` where `|` is a separator that can be different (any string of characters).
    - Have `sim_setting_name` and `sim_setting_value` columns in your datafile (names can be changed), that contains the variables that define the simulation settings, _e.g._:
        ```
        time speed sim_setting_name sim_setting_value
        0 1 wind_speed 2.4
        1 2 temp 25
        2 4
        3 5
        ...
        ```

##### Filtering

Then, what you can do is to create a `Database` instance with the folder path, and then you can use its method `filter_datafiles`:

```python
def filter_datafiles(self, file_name_base: str, filter_dict : dict) -> List[DataFile]:
```
where:
- `file_name_base` is a string that the file should contain in its filename (the text before the start of the variable definitions)
- `filter_dict` is a dictionary that contains `(key, val)` pairs, both strings, that correspond to `varN=valN` in the csv files you are looking for.

And this method will return all the files that match your filters. The retrieve a single datafile interactively, you can use the `file_selection_prompt` method from `Database`.

## Dependencies:

- Python Matplotlib
- Python [py_expression_eval](https://github.com/Axiacore/py-expression-eval), can be installed with `pip install py_expression_eval`
- Latex distribution installed in your computer, can be deactivated in csv_plotter.py by changing the following line `plt.rcParams['text.usetex'] = True` to `plt.rcParams['text.usetex'] = False`
