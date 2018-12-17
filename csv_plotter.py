import matplotlib as mpl
from csv_reader import *

import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (11.69,8.27)
plt.rcParams['text.usetex'] = True
plt.rcParams['axes.formatter.useoffset'] = True
plt.rcParams['axes.formatter.limits'] = (-3, 3)

#plt.rcParams['axes.grid'] = True
plt.rcParams['font.size'] = 20

class CSV_Plotter:
    def __init__(self, num_rows = 1, num_columns = 1, share_x = False, share_y = False):
        self.fig, self.graphs = plt.subplots(num_rows, num_columns, sharex=share_x, sharey=share_y)
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.csv_reader = CSV_Reader()

        self.file_aliases = dict()

        if num_rows == 1:
            if num_columns == 1:
                self.graphs = [[self.graphs]]
            else:
                self.graphs = [self.graphs]
        elif num_columns == 1:
            self.graphs = [[graph] for graph in self.graphs]

    def load(self, csv_file, alias=None, csv_separator = ' '):
        self.csv_reader.parse(csv_file, csv_separator)
        if alias != None:
            self.file_aliases[alias] = csv_file
       
        self.file_aliases[csv_file] = csv_file        

    def plot(self, alias, x_column, y_column, graph_row, graph_column, **kwargs):        
        x_vals = self.csv_reader.get_column(self.file_aliases[alias], x_column)
        y_vals = self.csv_reader.get_column(self.file_aliases[alias], y_column)            
        self.graphs[graph_row][graph_column].plot(x_vals, y_vals, **kwargs)
        self.graphs[graph_row][graph_column].grid()
        if 'label' in kwargs and kwargs['label']:
            self.graphs[graph_row][graph_column].legend()        

    def set(self, row, col, **kwargs):
        self.graphs[row][col].set(**kwargs)

    def show(self):         
        plt.show()


      
