from bokeh.io import output_notebook, show
from bokeh.plotting import figure

width = input("What's the width?")
height = input("What's the height?")

# create a new plot using figure
p = figure(plot_width=int(width), plot_height=int(height))

# add a square renderer with a size, color, alpha, and sizes
p.square([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=[10, 15, 20, 25, 30], color="firebrick", alpha=0.6)

show(p) # show the results