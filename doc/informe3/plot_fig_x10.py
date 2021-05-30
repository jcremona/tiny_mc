import plot_utils as ps

ps.plot_scatter('results_x10.csv', 'img/fig_x10.svg', "Average photons per sec (25 samples, 3276800 photons, 16 lanes)")
ps.plot_efficiency('results_x10.csv', 'img/fig_efficiency_x10.svg', "Efficiency of previous results (25 samples, 3276800 photons, 16 lanes)")

