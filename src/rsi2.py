#! /usr/bin/env python

import pandas
import pandas_ta as pta
import matplotlib.pyplot as plt


column_names = ['timestamp', 'date', 'symbol', 'open', 'high', 'low', 'close', 'volume']
columns_to_use = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
dfo = pandas.read_csv('./bitcoin-2021.csv',
                      header=0,
                      names=column_names,
                      index_col='timestamp',
                      usecols=columns_to_use)

# df = dfo[::-1]
dfo.index = pandas.to_datetime(dfo.index, unit='ms')
df = dfo.sort_values(by='timestamp')

df.ta.sma(append=True)
df.ta.rsi(append=True)
df.ta.macd(append=True)

print(df)
# df.reset_index()

# rsi = pta.rsi(df['close'], length = 14)
# # help(pta.macd)
# macd = pta.macd(df['close'])

# print(macd)

# df['rsi'] = rsi

# df.reset_index()

# # df.plot(x='timestamp', y='rsi')

# # plt.show()

for index, row in df.head(28).iterrows():
    print(index, row['RSI_14'])
