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