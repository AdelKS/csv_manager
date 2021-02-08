import os
from pathlib import Path
from .datafile import DataFile

import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True

plt.rcParams['figure.figsize'] = (11.69,8.27)
plt.rcParams['axes.formatter.useoffset'] = True
plt.rcParams['axes.formatter.limits'] = (-2, 2)

plt.rcParams['axes.grid'] = True
plt.rcParams['font.size'] = 20

class Plotter():
    def __init__(self, num_rows: int = 1, num_columns: int = 1, share_x: bool = False, share_y: bool = False, fig_num=None):
        r"""
        Creates a Plotter class instance, used to plot 2D data using matplotlib

        Parameters
        ----------

        num_rows : int
            The number of rows of subplots

        num_columns : int
            The number of columns of subplots

        share_x : bool
            Whether or not subplots of the same column share their x axis min, max and ticks

        share_y : bool
            Whether or not subplots of the same row share their y axis min, max and ticks

        """       
        super().__init__()
        self.share_x = share_x
        self.share_y = share_y        
        self.num_rows = num_rows
        self.num_columns = num_columns

        self.fig_num = fig_num
        self.fig = None
        self.plt = plt

        self._instance_new_subplots()

    def _instance_new_subplots(self):       

        self.fig, self.graphs = plt.subplots(self.num_rows, self.num_columns, sharex=self.share_x, sharey=self.share_y, num=self.fig_num)

        if self.num_rows == 1:
            if self.num_columns == 1:
                self.graphs = [[self.graphs]]
            else:
                self.graphs = [self.graphs]
        elif self.num_columns == 1:
            self.graphs = [[graph] for graph in self.graphs] 

    def plot(self, datafile: DataFile, x_expr, y_expr, graph_row=0, graph_column=0, **kwargs):    
        '''
            x_expr and y_expr can either be:
            - an integer: it corresponds to the column index in the csv
            - string: 
                - a column's name
                - an expression involving as variables the column names of the csv file
        '''

        x_vals = datafile.get(x_expr)
        y_vals = datafile.get(y_expr)            
        lines = self.graphs[graph_row][graph_column].plot(x_vals, y_vals, **kwargs)
        if 'label' in kwargs and kwargs['label']:
            self.graphs[graph_row][graph_column].legend()
        
        return lines 

    def plot_data(self, *args, graph_row=0, graph_column=0, **kwargs):
        '''
            Use the regular plt.plot() with its args
        '''
        fig = self.graphs[graph_row][graph_column].plot(*args, **kwargs)
        if 'label' in kwargs and kwargs['label']:
            self.graphs[graph_row][graph_column].legend()
        return fig

    def imshow(self, *args, graph_row=0, graph_column=0, **kwargs):
        '''
            Use the regular plt.imshow() with its args
        '''
        fig = self.graphs[graph_row][graph_column].imshow(*args, **kwargs)
        if 'label' in kwargs and kwargs['label']:
            self.graphs[graph_row][graph_column].legend()
        return fig        

    def set(self, graph_row=0, graph_column=0, **kwargs):
        self.graphs[graph_row][graph_column].set(**kwargs)

    def show(self):         
        plt.show()
        self._instance_new_subplots()

    def savefig(self, *args, **kwargs):
        file_path = args[0]
        file_folder = Path(file_path).parent
        os.makedirs(file_folder, exist_ok=True)

        plt.savefig(*args, **kwargs)
        plt.close()
        self._instance_new_subplots()

    def legend(self, *args, **kwargs):
        plt.legend(*args, **kwargs)


      
