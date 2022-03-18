import math
import numpy
# from brain import Brain


threshold = 0.25

class Action:
    type = "Action"
    types = [
        "buy_or_sell",
    ]

    def __init__(self, id) -> None:
        self.id = id
        self.name = Action.types[id]
        self.inputs = []
        # self.inputs = numpy.array([])
        self.connected_backward_to = {}

    def receive(self, input):
        # self.inputs = numpy.append(self.inputs, input)
        self.inputs.append(input)

    def run(self):
        output = math.tanh(sum(self.inputs))
        # output = math.tanh(numpy.sum(self.inputs))
        # output = math.tanh(numpy.sum(numpy.array(self.inputs)))
        # percent = (abs(output) - threshold) / (1 - threshold)

        self.inputs = []

        return output
        # self.inputs = numpy.array([])

        # if output > 0.25 or output < -0.25:
        #     print("Action")

        # if output > threshold:
        #     budget = brain.balance * percent
        #     brain.goods_count += budget / time_slice.close
        #     brain.balance -= budget
        # elif output < -threshold:
        #     quantity = brain.goods_count * percent
        #     brain.balance += quantity * time_slice.close
        #     brain.goods_count -= quantity

        # print(brain.balance, brain.goods_count)

    def connect_backward(self, neuron, weight):
        self.connected_backward_to[neuron.id] = [neuron, weight]
