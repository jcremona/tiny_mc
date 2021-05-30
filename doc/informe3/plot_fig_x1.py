import plot_utils as ps

ps.plot_scatter('results_x1.csv', 'img/fig_x1.svg', "Average photons per sec (25 samples, 327680 photons, 16 lanes)")
ps.plot_efficiency('results_x1.csv', 'img/fig_efficiency_x1.svg', "Efficiency of previous results (25 samples, 327680 photons, 16 lanes)")

