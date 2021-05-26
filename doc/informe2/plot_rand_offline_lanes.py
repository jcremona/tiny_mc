import plots

title="Average photons per sec (50 samples, 327680 simulated photons)"
plots.open_and_plot("rand-offline/rand_offline_lanes.txt", "img/rand_offline_lanes.svg", title, width=0.2, xlimmin=-1,xlimmax=3)
