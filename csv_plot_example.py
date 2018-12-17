from csv_plotter import *

plotter = CSV_Plotter(num_rows=2, num_columns=2, share_x='col')

csv_elec_01 =  '/home/akarasl/Documents/Recherches/Code/tQdot/Data/Heat_current_partial_derivatives_t0=0.1_tmax=1_dt=0.02_ɣ=4_ɣc=1_μ=0_T=0.1_εμ=0.1_εT=0.1_λ=1_ε0=0.5_s=0.5_err=1e-06_lead=L.csv'
csv_elec_001 = '/home/akarasl/Documents/Recherches/Code/tQdot/Data/Heat_current_partial_derivatives_t0=0.1_tmax=1_dt=0.02_ɣ=4_ɣc=1_μ=0_T=0.1_εμ=0.01_εT=0.01_λ=1_ε0=0.5_s=0.5_err=1e-06_lead=L.csv'
csv_elec_0001 = '/home/akarasl/Documents/Recherches/Code/tQdot/Data/Heat_current_partial_derivatives_t0=0.1_tmax=1_dt=0.02_ɣ=4_ɣc=1_μ=0_T=0.1_εμ=0.001_εT=0.001_λ=1_ε0=0.5_s=0.5_err=1e-06_lead=L.csv'


plotter.load(csv_elec_01, alias='Heat01')
plotter.load(csv_elec_001, alias='Heat001')
plotter.load(csv_elec_0001, alias='Heat0001')

plotter.plot('Heat01', 'time', 'μL', 1, 0, '$\\varepsilon_\\mu=0.1$')
plotter.plot('Heat001', 'time', 'μL', 1, 0, '$\\varepsilon_\\mu=0.01$')
plotter.plot('Heat0001', 'time', 'μL', 1, 0, '$\\varepsilon_\\mu=0.001$')

plotter.graph(1, 0).set(xlabel='$t ~~ {\\scriptstyle [\\hbar / \\Gamma]}$', ylabel='$\\partial_{\\mu_L} I_h ~~ {\\scriptstyle [\\Gamma / \\hbar]}$')

plotter.plot('Heat01', 'time', 'TL', 1, 1, '$\\varepsilon_T=0.1$')
plotter.plot('Heat001', 'time', 'TL', 1, 1, '$\\varepsilon_T=0.01$')
plotter.plot('Heat0001', 'time', 'TL', 1, 1, '$\\varepsilon_T=0.001$')

plotter.graph(1, 1).set(xlabel='$t ~~ {\\scriptstyle [\\hbar / \\Gamma]}$', ylabel='$\\partial_{T_L} I_h ~~ {\\scriptstyle [\\Gamma / \\hbar]}$')

#####################################################################


csv_elec_01 =  '/home/akarasl/Documents/Recherches/Code/tQdot/Data/Electric_current_partial_derivatives_t0=0.1_tmax=1_dt=0.02_ɣ=4_ɣc=1_μ=0_T=0.1_εμ=0.1_εT=0.1_λ=1_ε0=0.5_s=0.5_err=1e-06_lead=L.csv'
csv_elec_001 = '/home/akarasl/Documents/Recherches/Code/tQdot/Data/Electric_current_partial_derivatives_t0=0.1_tmax=1_dt=0.02_ɣ=4_ɣc=1_μ=0_T=0.1_εμ=0.01_εT=0.01_λ=1_ε0=0.5_s=0.5_err=1e-06_lead=L.csv'
csv_elec_0001 = '/home/akarasl/Documents/Recherches/Code/tQdot/Data/Electric_current_partial_derivatives_t0=0.1_tmax=1_dt=0.02_ɣ=4_ɣc=1_μ=0_T=0.1_εμ=0.001_εT=0.001_λ=1_ε0=0.5_s=0.5_err=1e-06_lead=L.csv'


plotter.load(csv_elec_01, alias='Elec01')
plotter.load(csv_elec_001, alias='Elec001')
plotter.load(csv_elec_0001, alias='Elec0001')

plotter.plot('Elec01', 'time', 'μL', 0, 0, '$\\varepsilon_\\mu=0.1$')
plotter.plot('Elec001', 'time', 'μL', 0, 0, '$\\varepsilon_\\mu=0.01$')
plotter.plot('Elec0001', 'time', 'μL', 0, 0, '$\\varepsilon_\\mu=0.001$')

plotter.graph(0, 0).set(ylabel='$\\partial_{\\mu_L} I_e ~~ {\\scriptstyle [\\Gamma / \\hbar]}$')

plotter.plot('Elec01', 'time', 'TL', 0, 1, '$\\varepsilon_T=0.1$')
plotter.plot('Elec001', 'time', 'TL', 0, 1, '$\\varepsilon_T=0.01$')
plotter.plot('Elec0001', 'time', 'TL', 0, 1, '$\\varepsilon_T=0.001$')

plotter.graph(0, 1).set(ylabel='$\\partial_{T_L} I_e ~~ {\\scriptstyle [\\Gamma / \\hbar]}$')

plotter.show()