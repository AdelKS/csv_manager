import matplotlib as mpl
from .reader import *

import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True

plt.rcParams['figure.figsize'] = (11.69,8.27)
plt.rcParams['axes.formatter.useoffset'] = True
plt.rcParams['axes.formatter.limits'] = (-2, 2)

plt.rcParams['axes.grid'] = True
plt.rcParams['font.size'] = 20

class Plotter(Reader):
    def __init__(self, num_rows = 1, num_columns = 1, share_x = False, share_y = False):
        super().__init__()
        self.share_x = share_x
        self.share_y = share_y        
        self.num_rows = num_rows
        self.num_columns = num_columns

        self._instance_new_subplots()

    def _instance_new_subplots(self):
        self.fig, self.graphs = plt.subplots(self.num_rows, self.num_columns, sharex=self.share_x, sharey=self.share_y)

        if self.num_rows == 1:
            if self.num_columns == 1:
                self.graphs = [[self.graphs]]
            else:
                self.graphs = [self.graphs]
        elif num_columns == 1:
            self.graphs = [[graph] for graph in self.graphs] 

    def plot(self, alias, x_expr, y_expr, graph_row=0, graph_column=0, **kwargs):    
        '''
            x_expr and y_expr can either be:
            - an integer: it corresponds to the column index in the csv
            - string: 
                - a column's name
                - an expression involving as variables the column names of the csv file
        '''

        x_vals = self.get(alias, x_expr)
        y_vals = self.get(alias, y_expr)            
        lines = self.graphs[graph_row][graph_column].plot(x_vals, y_vals, **kwargs)
        if 'label' in kwargs and kwargs['label']:
            self.graphs[graph_row][graph_column].legend()
        
        return lines 

    def plot_data(self, graph_row, graph_column, *args, **kwargs):
        '''
            Use the regular plt.plot() with its args
        '''
        fig = self.graphs[graph_row][graph_column].plot(*args, **kwargs)
        if 'label' in kwargs and kwargs['label']:
            self.graphs[graph_row][graph_column].legend()
        return fig
        

    def set(self, row, col, **kwargs):
        self.graphs[row][col].set(**kwargs)

    def show(self):         
        plt.show()
        self._instance_new_subplots()


      
