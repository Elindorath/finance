from pathlib import Path
import logging
import yaml


class Config:
    def __init__(self, config_path: str='config.yaml'):
        config_path = Path.cwd().joinpath(config_path).resolve(strict=True)

        with open(config_path) as config_file:
            config = yaml.load(config_file, Loader=yaml.Loader)

        self.max_internal_neuron_count = 4
        self.initial_balance = 3000
        self.initial_goods_count = 0
        self.buy_or_sell_threshold = 0.25
        self.actor_count = 1
        self.max_generation = 2

        for key, value in config.items():
            if not hasattr(self, key):
                logging.warning(f'{key} is not a valid config parameter, ignoring it')
            else:
                setattr(self, key, value)
