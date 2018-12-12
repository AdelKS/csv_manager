import matplotlib as mpl
mpl.use('Agg')

from csv_reader import *

import matplotlib.pyplot as plt

class CSV_Plotter:
    def __init__(self, rows, columns, share_x, share_y):
        self.fig, self.graphs = plt.subplots(2, 2, sharex=share_x, sharey=share_y)
        self.csv_reader = CSV_Reader()

    def plot(csv_file, csv_separator, csv_x_column, csv_y_column, graph_row, graph_column, legend, style):
        self.csv_reader.parse

      
