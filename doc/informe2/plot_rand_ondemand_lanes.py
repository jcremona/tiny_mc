import plots

title="Average photons per sec (50 samples, 327680 photons)"
plots.open_and_plot("rand-ondemand/rand_ondemand_lanes.txt", "img/rand_ondemand_lanes.svg", title, width=0.2, xlimmin=-1,xlimmax=3)
