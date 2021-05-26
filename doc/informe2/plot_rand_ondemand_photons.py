import plots

title="Average photons per sec (50 samples, 8 lanes)"
plots.open_and_plot("rand-ondemand/rand_ondemand_photons.txt", "img/rand_ondemand_photons.svg", title, width=0.15, xlimmin=-1,xlimmax=3)
