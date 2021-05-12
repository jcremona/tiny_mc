import plots

title="Average photons per sec (50 samples, 8 lanes)"
plots.open_and_plot("ispc/ispc_photons.txt", "img/ispc_photons.svg", title, width=0.1, xlimmin=-0.7,xlimmax=0.7)
