#! /usr/bin/env python

from perf_context import timed_performance
from world import World
from population import Population
from simulation import Simulation
from sensor import Sensor
from config import Config


def main(config: Config):
    # def main(world_source, population_source='', save_to='', config={}):
    with timed_performance('World created'):
        world = World(config)

    with timed_performance('Population created'):
        population = Population(world, config)

    with timed_performance('Simulation ran'):
        simulation = Simulation(world, population, config)

        simulation.run()



if __name__ == '__main__':
    import logging
    import configargparse


    logging.basicConfig(format='%(levelname)s: %(message)s')

    def existing_file_path(file_path):
        from pathlib import Path


        error_message = ''
        absolute_path = Path.cwd().joinpath(file_path).resolve()
        absolute_path_str = str(absolute_path)

        if not absolute_path.exists():
            error_message = f'{file_path} doesn\'t exist (resolved to {absolute_path_str})'
        elif not absolute_path.is_file():
            error_message = f'{file_path} is not a valid file (resolved to {absolute_path_str})'

        if len(error_message):
            raise configargparse.ArgumentTypeError(error_message)

        return absolute_path_str

    def warn_existing_file_path(file_path):
        from pathlib import Path


        error_message = ''
        absolute_path = Path.cwd().joinpath(file_path).resolve()
        absolute_path_str = str(absolute_path)

        if absolute_path.exists() and not absolute_path.is_file():
            error_message = f'{file_path} already exists and is not a file (resolved to {absolute_path_str})'
        else:
            logging.warning(f'{file_path} already exists, it will be overriden (resolved to {absolute_path_str})')

        if len(error_message):
            raise configargparse.ArgumentTypeError(error_message)

        return absolute_path_str

    parser = configargparse.ArgumentParser(
        # configargparse specific options
        # default_config_files=['./config.yaml'],
        config_file_parser_class=configargparse.YAMLConfigFileParser,
        # config_arg_help_message='\n'.join([
        #     'File path from which to read config values',
        # ]),
        # args_for_setting_config_path=False,
        ignore_unknown_config_file_keys=True,
        # args_for_writing_out_config_file=['-w', '--write-config'],
        # write_out_config_file_arg_help_message='\n'.join([
        #     'File path where to write a configuration file with the current command line args',
        #     'When provided, exits command immediately after writing out the configuration file',
        # ]),
        # argparse options
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
    )

    argument_group_world = parser.add_argument_group('world')
    argument_group_simulation = parser.add_argument_group('simulation')
    argument_group_population = parser.add_argument_group('population')
    argument_group_configuration = parser.add_argument_group('configuration')

    argument_group_world.add_argument(
        '--markets',
        type=existing_file_path,
        nargs='+',
        required=True,
        default=configargparse.SUPPRESS,
        metavar='MARKET_OHLCV_FILE_PATH',
        help='\n'.join([
            'List of file paths containing OHLCV market data',
        ]),
    )
    argument_group_simulation.add_argument(
        *['-g', '--generation-count'],
        type=int,
        default=2,
        metavar='GENERATION_COUNT',
        help='\n'.join([
            'The number of generations',
        ]),
    )
    argument_group_population.add_argument(
        *['-n', '--actor-count'],
        type=int,
        default=2,
        metavar='ACTOR_COUNT',
        help='\n'.join([
            'The number of actors per generation',
        ]),
    )
    argument_group_population.add_argument(
        '--genomes',
        type=existing_file_path,
        default=configargparse.SUPPRESS,
        metavar='IN_GENOMES_FILE_PATH',
        help='\n'.join([
            'File path from which to read the genomes of the first generation',
        ]),
    )
    argument_group_population.add_argument(
        '--save-genomes',
        type=warn_existing_file_path,
        default=configargparse.SUPPRESS,
        metavar='OUT_GENOMES_FILE_PATH',
        help='\n'.join([
            'File path where to write the genomes of the last generation',
            'Overwrite the file if it exists',
        ]),
    )
    argument_group_population.add_argument(
        '--max_neuron',
        type=int,
        dest='max_internal_neuron',
        default=4,
        metavar='MAX_INTERNAL_NEURON_COUNT',
        help='\n'.join([
            'Max internal neuron count per brain',
        ]),
    )
    argument_group_population.add_argument(
        '--balance',
        type=int,
        dest='initial_balance',
        default=3000,
        metavar='INITIAL_BALANCE',
        help='\n'.join([
            'Initial balance for each market account of each actor',
        ]),
    )
    argument_group_population.add_argument(
        '--goods',
        type=int,
        dest='initial_goods_count',
        default=0,
        metavar='INITIAL_GOODS_COUNT',
        help='\n'.join([
            'Initial goods count for each market account of each actor',
        ]),
    )
    argument_group_population.add_argument(
        '--trade-threshold',
        type=float,
        dest='buy_or_sell_threshold',
        default=0.25,
        metavar='BUY_OR_SELL_THRESHOLD',
        help='\n'.join([
            'Threshold beyond which actors decide to buy or sell',
            'Must be between 0 and 1'
        ]),
    )
    argument_group_configuration.add_argument(
        *['-c', '--config-file'],
        type=existing_file_path,
        dest='config_file',
        default=configargparse.SUPPRESS,
        metavar='IN_CONFIG_FILE_PATH',
        help='\n'.join([
            'File path from which to read config values',
        ]),
        is_config_file_arg=True,
    )
    argument_group_configuration.add_argument(
        *['-w', '--write-config'],
        type=warn_existing_file_path,
        dest='write_out_config_file_to_this_path',
        default=configargparse.SUPPRESS,
        metavar='OUT_CONFIG_FILE_PATH',
        help='\n'.join([
            'File path where to write a configuration file with the current command line args',
            'When provided, exits command immediately after writing out the configuration file',
        ]),
        is_write_out_config_file_arg=True,
    )

    # max_internal_neuron_count: 4
    # initial_balance: 3000
    # initial_goods_count: 0
    # buy_or_sell_threshold: 0.25
    # actor_count: 1
    # max_generation: 2

    # import argparse
    # import logging
    # from config import Config

    # logging.basicConfig(format='%(levelname)s: %(message)s')
    # config = Config()

    # parser = argparse.ArgumentParser(description='Generate random neural network and select the best through natural selection.')
    # # parser.add_argument('world_source')
    # parser.add_argument('--market', dest='market_sources', metavar='market_source', action='extend', nargs='+', required=True)
    # parser.add_argument('--population', dest='population_source' ,metavar='population_source', default='')
    # parser.add_argument('-s', '--save', default='')

    args = parser.parse_args()

    print(args)
    # print(argument_group_world)
    # main(args.market_sources, args.population_source, args.save, config)
