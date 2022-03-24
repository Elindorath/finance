from typing import Callable

from __typings import Transmitter_neuron, Receiver_neuron


class Internal:
    type = 'Internal'

    def __init__(self, *, id: int, activation_function: Callable[[list[float]], float]) -> None:
        self.id = id
        self.activation_function = activation_function
        self.inputs = []
        # self.inputs = numpy.array([])
        self.connected_forward_to = {}
        self.connected_backward_to = {}

    def compute(self) -> None:
        output = self.activation_function(self.inputs)
        # output = math.tanh(sum(self.inputs))
        # output = math.tanh(numpy.sum(self.inputs))
        # output = math.tanh(numpy.sum(numpy.array(self.inputs)))

        self.inputs = []
        # self.inputs = numpy.array([])

        for [next, weight] in self.connected_forward_to.values():
            next.receive(output * weight)

    def receive(self, input: float) -> None:
        # self.inputs = numpy.append(self.inputs, input)
        self.inputs.append(input)

    def connect_forward(self, neuron: Receiver_neuron, weight: float) -> None:
        self.connected_forward_to[neuron.id] = [neuron, weight]

    def connect_backward(self, neuron: Transmitter_neuron, weight: float) -> None:
        self.connected_backward_to[neuron.id] = [neuron, weight]
