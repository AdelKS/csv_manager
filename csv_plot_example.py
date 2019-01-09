# Author: Adel KARA SLIMANE <adel.kara-slimane@cea.fr>

from csv_plotter import *

plotter = CSV_Plotter(num_rows=1, num_columns=1)


file1 = '/home/akarasl/Documents/Recherches/Code/tQdot/Data/Onsager_direct_t0=0.1_tmax=12_dt=0.04_γ=4_γc=1_μ=0_T=0.1_α=0.5_λ=2_ε0=0.5_s=0.5_err=1e-06_lead=L_α=0.5.csv'


plotter.load(file1, alias='file1')

######################################################

plotter.plot('file1', 'time', '-L21/L12', 0, 0, label='example of legend', color='red', linestyle=':')
# Starting from " label='save' [...]" the arguments are the **kwargs in https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html

plotter.set(0, 0, xlabel='time', ylabel='$-L_{21}/L_{12}$')
# Starting from " xlabel='time' [...]" the options that can be set are the **kwargs in https://matplotlib.org/api/axes_api.html

plotter.show()