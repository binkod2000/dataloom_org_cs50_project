from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
import numpy as np

#configure plot size
width = 800
height = 600
plot = figure(plot_width=width, plot_height=height)

# x = []
# y = []

# for i in range(10):
#         num1 = np.random.randint(1, 100)
#         num2 = np.random.randint(1, 100)
#         x.append(num1)
#         y.append(num2)
x = [2, 4, 5, 13, 25, 13, 4]
y = [3, 15, 24, 20, 3, 3, 1]

print(x)
#variable to controll the glyphs size, color and transparency
glyph_size = 20
glyph_color = "navy"
glyph_transparency = 0.5
glyph_shape = 'circle'


plot.circle(x, y, size=glyph_size, color=glyph_color, alpha=glyph_transparency)

# html = file_html(plot, CDN, "text_plot.html")
script, div = components(plot)

# file = open("test_plot.html", "w")
# file.write(html)
# file.close()
# #
# file = open("/Users/Liam/Desktop/js/div.html", "w")
# file.write(div)
# file.close()
#
# file = open("/Users/Liam/Desktop/js/script.html", "w")
# file.write(script)
# file.close()
dataset_dropdown = '{% block dataset %}\n' + '{% for data in dataset %}\n' + '<option value = "{{ data }}">{{ data }}</option>\n' +'{% endfor %}\n' + '{% endblock %}'
dataset2_dropdown = '{% block dataset2 %}\n' + '{% for data in dataset2 %}\n' + '<option value = "{{ data }}">{{ data }}</option>\n' + '{% endfor %}\n' + '{% endblock %}'



file = open("plot.html", "w")
total = '{% extends "layout.html" %} \n' + dataset_dropdown + dataset2_dropdown + '{% block main %}' + script + div + '\n{% endblock %}'
file.write(total)



file.close()
