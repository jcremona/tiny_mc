import plots

title="Average photons per sec (50 samples, 8 lanes)"
plots.open_and_plot("rand-offline/rand_offline_photons.txt", "img/rand_offline_photons.svg", title, width=0.15, xlimmin=-1,xlimmax=3)
