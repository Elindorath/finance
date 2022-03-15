#! /usr/bin/env python

from perf_context import timed_performance
from world import World
from population import Population
from simulation import Simulation
from sensor import Sensor


def main(world_source, population_source='', save_to=''):
    with timed_performance('World created'):
        world = World(world_source)

    with timed_performance('Population created'):
        population = Population(population_source, world)

    with timed_performance('Simulation ran'):
        simulation = Simulation(world, population, save_to)

        simulation.run()



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate random neural network and select the best through natural selection.')
    # parser.add_argument('world_source')
    parser.add_argument('--market', dest='market_sources', metavar='market_source', action='extend', nargs='+', required=True)
    parser.add_argument('--population', dest='population_source' ,metavar='population_source', default='')
    parser.add_argument('-s', '--save', default='')

    args = parser.parse_args()

    print(args)
    main(args.market_sources, args.population_source, args.save)
