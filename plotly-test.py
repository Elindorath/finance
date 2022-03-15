#! /usr/bin/env python

# import plotly
# import plotly.graph_objects as go
from plotly import graph_objects as go

import pandas
# from datetime import datetime


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

fig = go.Figure(data=[go.Candlestick(x=dataframe.index,
                open=dataframe['open'],
                high=dataframe['high'],
                low=dataframe['low'],
                close=dataframe['close'])])

fig.show()
