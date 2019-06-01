from bokeh.io import output_notebook, show
from bokeh.plotting import figure

# Get the total size of the plot you want to make
def plot(width, height):
    the_plot = figure(plot_width=width, plot_height-height)
    return the_plot

