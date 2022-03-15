import pandas
from pandas.tseries.offsets import DateOffset
from market import Market


class World:
    def __init__(self, sources):
        self.markets = [Market(source) for source in sources]
        self.sensors_type = [column for column in self.markets[0].dataframe.columns if '_normalized' in column]

        start = min([market.dataframe.index[0] for market in self.markets])
        end = max([market.dataframe.index[-1] for market in self.markets])
        freq_in_ns = min([market.dataframe.index.to_series().diff().min() for market in self.markets]).delta
        index = pandas.date_range(start=start, end=end, freq=pandas.offsets.Nano(freq_in_ns))

        for market in self.markets:
            market.reindex(index)

    def __iter__(self):
        return WorldIterator(self)

        # column_names = [
        #     'timestamp', 'date', 'symbol', 'open', 'high', 'low', 'close', 'volume'
        # ]
        # columns_to_use = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        # original_dataframe = pandas.read_csv(source,
        #                                      header=0,
        #                                      names=column_names,
        #                                      index_col='timestamp',
        #                                      usecols=columns_to_use)

        # original_dataframe.index = pandas.to_datetime(original_dataframe.index, unit='ms')
        # dataframe = original_dataframe.sort_values(by='timestamp')

        # dataframe.ta.sma(append=True)
        # dataframe.ta.sma(append=True, length=40)
        # dataframe.ta.rsi(append=True)
        # dataframe.ta.macd(append=True)
        # dataframe.ta.stoch(append=True)
        # dataframe.ta.ebsw(append=True)
        # dataframe.ta.cdl_pattern(name="all", append=True)

        # print(dataframe)
        # # print(dataframe["open"].min())
        # # print(dataframe["open"].max())

        # min_max_scaler = preprocessing.MinMaxScaler()
        # x_scaled = min_max_scaler.fit_transform(dataframe.values)
        # normalized_dataframe = pandas.DataFrame(x_scaled, columns=dataframe.columns)
        # normalized_dataframe.index = original_dataframe.index[::-1]
        # normalized_dataframe = normalized_dataframe.add_suffix("_normalized")
        # # print(normalized_dataframe)
        # dataframe = pandas.concat([dataframe, normalized_dataframe], axis=1)

        # self.dataframe = dataframe
        # self.dataframe.info(memory_usage="deep")
        # # print(sys.getsizeof(self.dataframe))
        # # time.sleep(10)
        # self.sensors_type = [column for column in self.dataframe.columns if "_normalized" in column]

        # print(self.sensors_type)



class WorldIterator:
    def __init__(self, world: World):
        self._world = world
        self._index = 0
        self._length = min([len(market) for market in world.markets])

    def __next__(self):
        if self._index < self._length:
            moment = [market.dataframe.iloc[self._index] for market in self._world.markets]

            self._index += 1

            return moment

        raise StopIteration

    def __iter__(self):
        return self
