#! /usr/bin/env python

import os
from math import pi
import pandas
from bokeh.io import curdoc
from bokeh import plotting as plt
from bokeh.layouts import column
from bokeh.models.tools import PanTool, WheelZoomTool, BoxZoomTool, CrosshairTool, HoverTool, ResetTool, SaveTool


column_names = [
    'timestamp', 'date', 'symbol', 'open', 'high', 'low', 'close', 'volume'
]
columns_to_use = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
original_dataframe = pandas.read_csv("./bitcoin-daily.csv",
                                     header=0,
                                     names=column_names,
                                     index_col='timestamp',
                                     usecols=columns_to_use)

original_dataframe.index = pandas.to_datetime(original_dataframe.index, unit='ms')
dataframe = original_dataframe.sort_values(by='timestamp')

inc = dataframe.close > dataframe.open
dec = dataframe.open > dataframe.close
w = 12 * 60 * 60 * 1000  # half day in ms

output_file_path = "./bokeh.html"

curdoc().theme = "dark_minimal"

wheel_zoom_tool = WheelZoomTool()

candlesticks = plt.figure(
    x_axis_type="datetime",
    tools=[
        PanTool(),
        wheel_zoom_tool,
        BoxZoomTool(),
        CrosshairTool(line_alpha=0.2, line_color="#FFFFFF"),
        HoverTool(),
        ResetTool(),
        SaveTool(),
    ],
    title="Bitcoin Candlestick",
    sizing_mode="stretch_both",
    # x_axis_label="Date",
    y_axis_label="Price",
    output_backend="webgl",
)

candlesticks.min_border = 0

candlesticks.xaxis.visible = False
# candlesticks.xaxis.major_label_orientation = pi / 4
candlesticks.grid.grid_line_alpha = 0.3

candlesticks.toolbar.active_scroll = wheel_zoom_tool
candlesticks.toolbar.logo = None

candlesticks.segment(dataframe.index[inc], dataframe.high[inc], dataframe.index[inc], dataframe.low[inc], color="#42AF51")
candlesticks.segment(dataframe.index[dec], dataframe.high[dec], dataframe.index[dec], dataframe.low[dec], color="#E21E2A")
candlesticks.vbar(dataframe.index[inc], w, dataframe.open[inc], dataframe.close[inc], fill_color="#42AF51", line_color="#42AF51")
candlesticks.vbar(dataframe.index[dec], w, dataframe.open[dec], dataframe.close[dec], fill_color="#E21E2A", line_color="#E21E2A")

volume = plt.figure(
    x_axis_type="datetime",
    sizing_mode="stretch_both",
    x_axis_label="Date",
    y_axis_label="Price",
    output_backend="webgl",
    x_range=candlesticks.x_range,
)

volume.xaxis.major_label_orientation = pi / 4
volume.grid.grid_line_alpha = 0.3

volume.vbar(dataframe.index[inc], w, 0, dataframe.volume[inc], fill_color="#42AF51", line_color="#42AF51")
volume.vbar(dataframe.index[dec], w, 0, dataframe.volume[dec], fill_color="#E21E2A", line_color="#E21E2A")

volume.min_border = 0

layout = column(children=[candlesticks, volume], sizing_mode="stretch_both")
layout.margin = 0

plt.save(obj=layout, filename=output_file_path)

os.system(f"wslview {output_file_path}")
