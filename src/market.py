from pathlib import Path
from typing import Sized

import pandas
import pandas_ta as pta
from sklearn import preprocessing

from memory_size_format import memory_size_format


class Market(Sized):
    def __init__(self, *, source: Path) -> None:
        self.name = source.stem

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
        dataframe = pandas.read_csv(str(source))

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
        normalized_dataframe = normalized_dataframe.add_suffix('_normalized')

        normalized_dataframe = normalized_dataframe.join(dataframe['close'])

        self.dataframe = normalized_dataframe.head(20).fillna(0)

        # self.dataframe = pandas.concat([dataframe, normalized_dataframe], axis=1)
        # self.dataframe.info(memory_usage="deep")
        print(f'{self.name}: {memory_size_format(num=self.dataframe.memory_usage(index=True, deep=True).sum())}')
        # # print(sys.getsizeof(self.dataframe))
        # # time.sleep(10)
        # self.sensors_type = [column for column in self.dataframe.columns if "_normalized" in column]

        # print(self.sensors_type)

    def reindex(self, index: pandas.Index) -> None:
        self.dataframe = self.dataframe.reindex(index, fill_value=0)

    def __len__(self) -> int:
        return len(self.dataframe)
