import plot_utils as ps

ps.plot_scatter('results_x100.csv', 'img/fig_x100.svg', "Average photons per sec (25 samples, 32768000 photons, 16 lanes)")
ps.plot_efficiency('results_x100.csv', 'img/fig_efficiency_x100.svg', "Efficiency of previous results (25 samples, 32768000 photons, 16 lanes)")

