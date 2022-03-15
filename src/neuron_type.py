from enum import Enum


class Neuron_type(Enum):
    # Transmitter types
    SENSOR = 0
    INTERNAL_TRANSMITTER = 1
    # Receiver types
    INTERNAL_RECEIVER = 0
    ACTION = 1
