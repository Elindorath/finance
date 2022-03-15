from pathlib import Path
import pandas
import pandas_ta as pta
from sklearn import preprocessing
from memory_size_format import memory_size_format


class Market:
    def __init__(self, source):
        self.name = Path(source).stem

        columns_to_use = ['open', 'high', 'low', 'close', 'volume']
        column_mapper = {
            'Unix Timestamp': 'timestamp',
            'Date': 'date',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Adj Close': 'adjusted_close',
            'Volume': 'volume',
        }
        dataframe = pandas.read_csv(source)

        dataframe.rename(columns=column_mapper, inplace=True)

        dataframe.index = pandas.to_datetime(dataframe.date)
        dataframe = dataframe[columns_to_use]

        dataframe.sort_values(by='date', inplace=True)

        dataframe.ta.sma(append=True)
        dataframe.ta.sma(append=True, length=40)
        dataframe.ta.rsi(append=True)
        dataframe.ta.macd(append=True)
        dataframe.ta.stoch(append=True)
        dataframe.ta.ebsw(append=True)
        dataframe.ta.cdl_pattern(name="all", append=True)

        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(dataframe.values)
        normalized_dataframe = pandas.DataFrame(x_scaled, columns=dataframe.columns, index=dataframe.index)
        normalized_dataframe = normalized_dataframe.add_suffix("_normalized")

        self.dataframe = normalized_dataframe
        # self.dataframe = pandas.concat([dataframe, normalized_dataframe], axis=1)
        # self.dataframe.info(memory_usage="deep")
        print(memory_size_format(self.dataframe.memory_usage(index=True, deep=True).sum()))
        # # print(sys.getsizeof(self.dataframe))
        # # time.sleep(10)
        # self.sensors_type = [column for column in self.dataframe.columns if "_normalized" in column]

        # print(self.sensors_type)

    def reindex(self, index):
        self.dataframe = self.dataframe.reindex(index)

    def __len__(self):
        return len(self.dataframe)