## csv_manager

This is a python module that features two simple classes for reading (class `Reader`) and plotting (class `Plotter`) CSVs using Python and Matplotlib (Latex rendering enabled), which avoids the cumbersome repetition of coding a csv reader using the `csv` python library then making the data in a readable structure for `plt.plot(...)`. An example is written in `example/csv_plot_example.py` :

```python
from csv_manager.plotter import Plotter

plotter = Plotter(num_rows=1, num_columns=2)

file1 = 'test_file.csv'

plotter.load(file1, alias='test file')

######################################################

plotter.plot('test file', 'time', 'position', 0, 0, label='position $x(t)$', color='red', linestyle=':')
# Starting from " label='save' [...]" the arguments are the **kwargs in https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html

plotter.plot('test file', 'time', '10 * sqrt(2/10 * position)', 0, 1, label='speed $v(t)$')

plotter.plot_data(0, 0, [0, 1, 2], [0, 1, 2], label='dummy data')

plotter.set(0, 0, xlabel='Time ', ylabel='Position')
# Starting from " xlabel='time' [...]" the options that can be set are the **kwargs in https://matplotlib.org/api/axes_api.html

plotter.set(0, 1, xlabel='Time ', ylabel='Speed')

plotter.show()
```

where the file `example/test_file.csv` looks like the following:

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

## Dependencies:

- Python Matplotlib
- Python [py_expression_eval](https://github.com/Axiacore/py-expression-eval), can be installed with `pip install py_expression_eval`
- Latex distribution installed in your computer, can be deactivated in csv_plotter.py by changing the following line `plt.rcParams['text.usetex'] = True` to `plt.rcParams['text.usetex'] = False`
