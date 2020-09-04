## csv_manager

This is a python module that features three simple classes for reading (class `Reader`), plotting (class `Plotter`, using Matplotlib with Latex rendering enabled) for the plots) and filtering (class `Database`) CSV files. And also a method for writing CSVs.

By using this module, the user avoids the cumbersome repetition of coding a csv reader using the `csv` python library then making the data in a readable structure for `plt.plot(...)`.

#### Using `Reader` and `Plotter`

An example is written in `example/csv_plot_example.py`, that showcases what can be done with this module:

```python
from csv_manager.plotter import Plotter
# Plotter inherits the class Reader

plotter = Plotter(num_rows=1, num_columns=2)
# Number of rows and columns for plt.sublots

file1 = 'data_file_1.csv'
file2 = 'data_file_2.csv'

plotter.load(file1, alias='dataset1')
plotter.load(file2, alias='dataset1')
#Both files are loaded in the same `dataset`, if column names collide, the latest ones get "_b" appended to their name

plotter.show_loaded_data()
# prints the loaded datasets. For each dataset, is printed:
# - the source files the data has been loaded from
# - the column names

plotter.get_column_names('dataset1')
# returns the list of column names of the dataset `dataset1`

######################################################

plotter.plot('dataset1', 'time', 'position', 0, 0, label='position $x(t)$', color='red', linestyle=':')
# Starting from " label='save' [...]" the arguments are the **kwargs in https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
plotter.plot('dataset1', 'time', 'speed', 0, 0, label='speed $v(t)$', color='blue', linestyle='--')

plotter.plot('dataset1', 'time', 'position + sqrt(2/10 * speed)', 0, 1, label='dummy curve from expression')

plotter.plot_data(0, 0, [0, 1, 2], [0, 1, 2], label='dummy data')

plotter.set(0, 0, xlabel='Time ', ylabel='Position')
# Starting from " xlabel='time' [...]" the options that can be set are the **kwargs in https://matplotlib.org/api/axes_api.html

plotter.set(0, 1, xlabel='Time ', ylabel='Dummy data')

plotter.show()
```

The file `example/data_file_1.csv` looks like the following:

```csv
time position
0 0
1 5
2 20
3 45
4 80
5 125
6 180
7 245
8 320
9 405
10 500
```

The file `example/data_file_2.csv` looks like the following:

```csv
time speed
0 0
1 3
2 3.6
3 2
4 5
5 8
6 9
7 10
8 9.1
9 8
10 7
```

#### Using `Database`

If you have a folder with lots of CSV files and find it too cumbersome to find the correct ones to plot or read. The class `Databse` is made for you!

Requirements:
- Follow a specific naming scheme on your CSV files: `filename|var1=val1|var2=val2|...|varN=valN.csv` where `|` is a separator that can be different (any string of characters).
- Have all your CSV files in a folder (work if they are in a subfolder of that folder)

Then, what you can do is to create a `Database` instance with the folder path, and then you can use its method `filter_datafiles`:

```python
def filter_datafiles(self, file_name_base: str, filter_dict : dict) -> List[DataFile]:
```
where:
- `file_name_base` is a string that the file should contain in its filename (the text before the var definitions start)
- `filter_dict` is a dictionnary that contains `(key, val)` pairs, both strings, that correspond to `varN=valN` in the csv files you are looking for.

And this method will return all the files that match your filters.

## Dependencies:

- Python Matplotlib
- Python [py_expression_eval](https://github.com/Axiacore/py-expression-eval), can be installed with `pip install py_expression_eval`
- Latex distribution installed in your computer, can be deactivated in csv_plotter.py by changing the following line `plt.rcParams['text.usetex'] = True` to `plt.rcParams['text.usetex'] = False`
