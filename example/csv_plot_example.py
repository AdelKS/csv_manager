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
