import plots

title="Average photons per sec (50 samples, 327680 simulated photons)"
plots.open_and_plot("ispc/ispc_lanes.txt", "img/ispc_lanes.svg", title, width=0.1, xlimmin=-0.5,xlimmax=0.5)
