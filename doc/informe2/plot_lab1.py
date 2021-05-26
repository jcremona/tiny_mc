import plots

title = "Average photons per sec (50 samples, 327680 simulated photons)"
plots.open_and_plot("lab1corregido/lab1corregido_photons.txt", "img/lab1.svg", title, width=0.5, xlimmin=-2, xlimmax=4)
