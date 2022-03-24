from typing import TypedDict


class World_Config(TypedDict):
    markets: list[str]


class Simulation_Config(TypedDict):
    generation_count: int

class Population_Config(TypedDict):
    actor_count: int
    genomes: str
    save_genomes: str
    max_internal_neuron: int
    initial_balance: int
    initial_goods_count: int
    buy_or_sell_threshold: float

class Config_Config(TypedDict):
    config_file: str
    write_config: str

class Config(World_Config, Simulation_Config, Population_Config, Config_Config):
    pass

# arguments_definition = {
#     'markets': {
#         'flags': '--markets',
#         # 'type': existing_file_path,
#         'tt': list[str],
#         'nargs': '+',
#         'required': True,
#         # 'default': configargparse.SUPPRESS,
#         'metavar': 'MARKET_OHLCV_FILE_PATH',
#         'help': '\n'.join([
#             'List of file paths containing OHLCV market data',
#         ]),
#     }
# }
# t = {name: arg['tt'] for name, arg in arguments_definition.items()}

# Config = TypedDict('Config', t)
