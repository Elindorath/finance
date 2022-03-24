from typing import TypedDict

import pandas

from sensor import Sensor
from internal import Internal
from action import Action


Moment = dict[str, pandas.Series]
Decisions = dict[str, float]
# Account = TypedDict('Account', {'balance': int, 'goods_count': int, 'history': list[Decisions]})

class Account(TypedDict):
    balance: int
    goods_count: int
    history: list[Decisions]

class Market_moment(TypedDict):
    close: float

Transmitter_neuron = Sensor | Internal
Receiver_neuron = Internal | Action
Neuron = Transmitter_neuron | Receiver_neuron
