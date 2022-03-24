from typing import Any, Callable

from __typings import Moment, Account, Market_moment
from genome import Genome
from brain import Brain
from market import Market


class Actor:
    def __init__(
        self,
        *,
        brain_factory: Callable[..., Brain],
        markets: list[Market],
        genome_as_hex_string: str = '',
        initial_balance: int,
        initial_goods_count: int,
        buy_or_sell_threshold: float,
    ) -> None:
        self.initial_balance = initial_balance
        self.initial_goods_count = initial_goods_count
        self.buy_or_sell_threshold = buy_or_sell_threshold
        self.accounts = {}
        self.initialize_accounts(markets)
        self.brain = brain_factory(genome_as_hex_string=genome_as_hex_string)

    def run(self, moment: Moment) -> None:
        for market_name, market_moment in moment.items():
            # Notes: decisions = {action_id: percent}
            decisions = self.brain.run(market_moment)

            for action_id, decision in decisions.items():
                self[action_id](decision, self.accounts[market_name], market_moment)

            # print('=====================')
            # print(self.accounts)
            self.accounts[market_name]['history'].append(decisions)

    def buy_or_sell(self, decision: float, account: Account, market_moment: Market_moment) -> None:
        percent = (abs(decision) - self.buy_or_sell_threshold) / (1 - self.buy_or_sell_threshold)

        if market_moment.close != 0:
            if decision > self.buy_or_sell_threshold:
                budget = account['balance'] * percent
                account['goods_count'] += budget / market_moment.close
                account['balance'] -= budget
            elif decision < -self.buy_or_sell_threshold:
                quantity = account['goods_count'] * percent
                account['balance'] += quantity * market_moment.close
                account['goods_count'] -= quantity

    def initialize_accounts(self, markets: list[Market]):
        self.accounts = {
            market.name: {
                'balance': self.initial_balance,
                'goods_count': self.initial_goods_count,
                'history': []
            }
            for market in markets
        }

    @property
    def balance(self) -> float:
        return sum([account['balance'] for account in self.accounts.values()])

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)



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
