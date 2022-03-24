from typing import Callable

from sklearn import preprocessing

from __typings import Market_moment, Decisions
from genome import Genome
# from neuron import Neuron_type
from sensor import Sensor
from internal import Internal
from action import Action
from world import World

Neuron_type = {
    'SENSOR': 0,
    'INTERNAL_TRANSMITTER': 1,
    'INTERNAL_RECEIVER': 0,
    'ACTION': 1,
}

class Brain:

    def __init__(
        self,
        *,
        sensor_factory: Callable[..., Sensor],
        internal_factory: Callable[..., Internal],
        action_factory: Callable[..., Action],
        genome_factory: Callable[..., Genome],
        world: World,
        genome_as_hex_string: str = '',
        max_internal_neuron: int,
    ) -> None:
        self.sensors_type = world.sensors_type
        self.sensors: dict[Sensor] = {}
        self.internals: dict[Internal] = {}
        self.actions: dict[Action] = {}
        self.balance_diffs = []
        self.max_internal_neuron = max_internal_neuron

        self.genome = genome_factory(hex_string=genome_as_hex_string)

        for gene in self.genome.genes:
            weight = gene.weight / 65536 * 8 - 4

            if gene.transmitter_type == Neuron_type['SENSOR']:
                transmitter_id = gene.transmitter_id % len(self.sensors_type)
                self.sensors[transmitter_id] = self.sensors.get(transmitter_id, False) or sensor_factory(id=transmitter_id)

                if gene.receiver_type == Neuron_type['INTERNAL_RECEIVER']:
                    receiver_id = gene.receiver_id % self.max_internal_neuron
                    self.internals[receiver_id] = self.internals.get(receiver_id, False) or internal_factory(id=receiver_id)
                    self.sensors[transmitter_id].connect_forward(self.internals[receiver_id], weight)
                elif gene.receiver_type == Neuron_type['ACTION']:
                    receiver_id = gene.receiver_id % len(Action.types)
                    self.actions[receiver_id] = self.actions.get(receiver_id, False) or action_factory(id=receiver_id)
                    self.sensors[transmitter_id].connect_forward(self.actions[receiver_id], weight)
                else:
                    raise Exception
            elif gene.transmitter_type == Neuron_type['INTERNAL_TRANSMITTER']:
                transmitter_id = gene.transmitter_id % self.max_internal_neuron
                self.internals[transmitter_id] = self.internals.get(transmitter_id, False) or internal_factory(id=transmitter_id)

                if gene.receiver_type == Neuron_type['INTERNAL_RECEIVER']:
                    receiver_id = gene.receiver_id % self.max_internal_neuron
                    self.internals[receiver_id] = self.internals.get(receiver_id, False) or internal_factory(id=receiver_id)
                    self.internals[transmitter_id].connect_forward(self.internals[receiver_id], weight)
                elif gene.receiver_type == Neuron_type['ACTION']:
                    receiver_id = gene.receiver_id % len(Action.types)
                    self.actions[receiver_id] = self.actions.get(receiver_id, False) or action_factory(id=receiver_id)
                    self.internals[transmitter_id].connect_forward(self.actions[receiver_id], weight)
                else:
                    raise Exception
            else:
                raise Exception

        # if self.id == 0:
        #     for sensor in self.sensors.values():
        #         for [next, _] in sensor.connected_forward_to.values():
        #             if next.type == 'Internal':
        #                 print(f'Internal {next.id}')

        self.clean_up()

    def run(self, moment: Market_moment) -> Decisions:
        # previous_balance = self.balance

        for id, sensor in self.sensors.items():
            sensor.sense(moment[self.sensors_type[id]])

        for _, internal in self.internals.items():
            internal.compute()

        # for _, action in self.actions.items():
        #     action.run(self, moment)

        return {action.name: action.run() for action in self.actions.values()}

        self.balance_diffs.append(self.balance - previous_balance)

    def clean_up(self) -> None:
        neuron_has_been_removed = False
        internals_to_remove = []
        sensors_to_remove = []

        for internal in self.internals.values():
            has_relevant_outputs = False

            for [next, _] in internal.connected_forward_to.values():
                if next.type != 'Internal' or next.id != internal.id:
                    has_relevant_outputs = True

            if not has_relevant_outputs:
                neuron_has_been_removed = True
                internals_to_remove.append(internal.id)

        for id in internals_to_remove:
            self.remove_internal(id)

        for sensor in self.sensors.values():
            if len(sensor.connected_forward_to) == 0:
                neuron_has_been_removed = True
                sensors_to_remove.append(sensor.id)

        for id in sensors_to_remove:
            self.remove_sensor(id)

        if neuron_has_been_removed:
            self.clean_up()

    def remove_internal(self, id: int) -> None:
        for internal in self.internals.values():
            if id in internal.connected_forward_to:
                del internal.connected_forward_to[id]

        for sensor in self.sensors.values():
            if id in sensor.connected_forward_to:
                del sensor.connected_forward_to[id]

        # if self.id == 0:
        #     print(f'Removed internal {id}')
        #     print(self.internals[id].connected_forward_to)

        del self.internals[id]

    def remove_sensor(self, id: int) -> None:
        del self.sensors[id]



'''
+1   -------

+0.5 -------





-0.5 -------

-1   -------
'''
