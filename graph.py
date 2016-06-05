import pandas as pd
import requests as req
import numpy as np
from bokeh.plotting import figure
from bokeh.palettes import Spectral11


def get_data(stock='ADI', checkbox_list='Open'):
    r = req.get('https://www.quandl.com/api/v3/datasets/WIKI/' +
                stock + '.json')
    raw_data = r.json()
    final_data = pd.DataFrame(raw_data['dataset']['data'], columns=raw_data[
                              'dataset']['column_names'])
    final_data = final_data.set_index('Date')
    final_data = final_data.ix[:, checkbox_list]
    return final_data


# final_data = get_data()

# checkbox_list = ['Open', 'Close']

def datetime(x):
    return np.array(x, dtype=np.datetime64)


def create_graph(final_data, checkbox_list):
    p1 = figure(x_axis_type="datetime")
    p1.title = "Stock Prices"
    p1.grid.grid_line_alpha = 0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'
    numlines = len(checkbox_list)
    mypalette = Spectral11[0:numlines]

    p1.multi_line(xs=[datetime(final_data.index.values)] * numlines,
                  ys=[final_data[name].values for name in final_data], line_color=mypalette, line_width=1)
    # output_file("templates/stocks.html", title="Stock Analysis")
    return p1
