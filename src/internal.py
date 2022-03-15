import math
import numpy


class Internal:
    type = "Internal"

    def __init__(self, id) -> None:
        self.id = id
        self.inputs = []
        # self.inputs = numpy.array([])
        self.connected_forward_to = {}
        self.connected_backward_to = {}

    def compute(self):
        output = math.tanh(sum(self.inputs))
        # output = math.tanh(numpy.sum(self.inputs))
        # output = math.tanh(numpy.sum(numpy.array(self.inputs)))

        self.inputs = []
        # self.inputs = numpy.array([])

        for [next, weight] in self.connected_forward_to.values():
            next.receive(output * weight)

    def receive(self, input):
        # self.inputs = numpy.append(self.inputs, input)
        self.inputs.append(input)

    def connect_forward(self, neuron, weight):
        self.connected_forward_to[neuron.id] = [neuron, weight]

    def connect_backward(self, neuron, weight):
        self.connected_backward_to[neuron.id] = [neuron, weight]
