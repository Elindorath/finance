from genome import Genome
from brain import Brain
from world import World


initial_balance = 3000
initial_goods_count = 0
threshold = 0.25

class Actor:
    def __init__(self, world: World, id: int, genome_as_hex_string: str) -> None:
        self.accounts = {
            market.name: {
                'balance': initial_balance,
                'goods_count': initial_goods_count,
                'history': []
            }
            for market in world.markets
        }
        self.brain = Brain(world)

    def run(self, moment, market_id):
        for market_moment in moment:
            # Notes: decisions = {actionId: percent}
            decisions = self.brain.run(market_moment)

            self.accounts[market_id].history.append(decisions)


    def acts(self, time_slice):
        for sensor in self.brain.sensors:
            sensor.sense(time_slice[sensor.id])

        for action in self.brain.actions:
            action.output(self.state)



"""
Sensor -> Internal -> Internal -> Internal -> Action
       ^           v           ^           v
       ^<<<<<<<<<<<<           ^<<<<<<<<<<<<

Sensor -> Internal -> Internal -> Internal -> Action
       ^                                   v
       ^<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<



We first iterate over sensors
We then iterate over internal outputs

===============================================================
Sensor ->>>>>>>>>>>>>>V
                      V
Sensor -> Internal 1 -> Internal 2 -> Internal 3 -> Action
       ^                                         v
       ^<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

Step 1:
Internal 1 = [1]
Internal 2 = [1, 1]
Internal 3 = [2]

Step 2:
Internal 1 = [2, 1]
Internal 2 = [1, 3]
Internal 3 = [4]

Step 3:
Internal 1 = [4, 1]
Internal 2 = [1, 5]
Internal 3 = [6]

Internal 1: 1
Internal 2: 1 + 1
Internal 3: 1 + 2
===============================================================

===============================================================
Sensor ->>>>>>>>>>>>>>V
                      V
Sensor -> Internal 2 -> Internal 1 -> Internal 3 -> Action
       ^                                         v
       ^<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

Step 1:
Internal 1 = [1]
Internal 2 = [1]
Internal 3 = [1]

Step 2:
Internal 1 = [1, 1]
Internal 2 = [1, 1]
Internal 3 = [2]

Step 3:
Internal 1 = [2, 1]
Internal 2 = [2, 1]
Internal 3 = [3]

Internal 1: 1 +
Internal 2: 1 + 1
Internal 3: 1 + 2
===============================================================



Brain
    sensors = []
    internals = []
    actions = []

    def run(self, time_slice):
        for sensor in self.sensors:
            sensor.sense(time_slice[sensor.id])

        for internal in self.internals:
            internal.compute()

        for action in self.actions:
            internal.output(self.state)

Sensor
    connected_forward_to = [Internal]

    def sense(self, input):
        for next in self.connected_forward_to:
            next.send(input)

Internal
    connected_forward_to = [Action]
    inputs = []

    def send(self, input):
        self.inputs.append(input)

    def compute(self):
        output = sum(self.inputs)

        for next in self.connected_forward_to:
            next.send(output)

        self.inputs = []

Action
    def send(self, input):
        self.inputs.append(input)

    def get_output(self, actor_state):
        output = sum(self.inputs)

        actor_state
"""
