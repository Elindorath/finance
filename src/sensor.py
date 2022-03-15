class Sensor:
    type = "Sensor"
    # types = [
    #     "open_normalized",
    #     "high_normalized",
    #     "low_normalized",
    #     "close_normalized",
    #     "volume_normalized",
    #     "SMA_10_normalized",
    #     "RSI_14_normalized",
    #     "MACD_12_26_9_normalized",
    #     "MACDh_12_26_9_normalized",
    #     "MACDs_12_26_9_normalized",
    # ]

    def __init__(self, id) -> None:
        self.id = id
        self.connected_forward_to = {}

    def sense(self, input):
        for [next, weight] in self.connected_forward_to.values():
            next.receive(input * weight)

    def connect_forward(self, neuron, weight):
        self.connected_forward_to[neuron.id] = [neuron, weight]
