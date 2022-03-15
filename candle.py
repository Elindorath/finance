#! /usr/bin/env python

import pandas
import matplotlib.pyplot as plt, mpld3
import mplfinance as mpf


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

figure = mpf.figure(style="yahoo", figsize=(19.5, 11))
figure.set_tight_layout(True)
ax = figure.add_subplot(1, 1, 1)
ax.grid(False)
mpf.plot(dataframe, type='candle', ax=ax, volume=False, returnfig=True)
# figure = mpf.plot(dataframe, type="candle", volume=True, returnfig=True)

# print(figure)
# mpld3.
mpld3.show(fig=figure)
