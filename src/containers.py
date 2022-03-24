import random
from math import tanh

from dependency_injector import containers, providers

from config import Config
from world import World
from market import Market
from population import Population
from actor import Actor
from brain import Brain
from genome import Genome
from gene import Gene
from sensor import Sensor
from internal import Internal
from action import Action
from simulation import Simulation


def activate_neuron(inputs: list[float]) -> float:
    return tanh(sum(inputs))

class Container(containers.DeclarativeContainer):

    random_lib = providers.Object(random)

    neuron_activation_function = providers.Callable(
        activate_neuron,
    )

    config: Config = providers.Configuration()

    market_factory = providers.Factory(
        Market,
    )

    world_singleton = providers.Singleton(
        World,
        market_factory=market_factory.provider,
        # markets=[market_factory(source) for source in config.markets],
        markets=config.markets,
    )

    sensor_factory = providers.Factory(
        Sensor,
    )

    internal_factory = providers.Factory(
        Internal,
        activation_function=neuron_activation_function.provider,
    )

    action_factory = providers.Factory(
        Action,
        activation_function=neuron_activation_function.provider,
    )

    gene_factory = providers.Factory(
        Gene,
        random=random_lib,
    )

    genome_factory = providers.Factory(
        Genome,
        gene_factory=gene_factory.provider,
    )

    brain_factory = providers.Factory(
        Brain,
        sensor_factory=sensor_factory.provider,
        internal_factory=internal_factory.provider,
        action_factory=action_factory.provider,
        genome_factory=genome_factory.provider,
        world=world_singleton,
        max_internal_neuron=config.max_internal_neuron,
    )

    actor_factory = providers.Factory(
        Actor,
        brain_factory=brain_factory.provider,
        markets=world_singleton.provided.markets,
        initial_balance=config.initial_balance,
        initial_goods_count=config.initial_goods_count,
        buy_or_sell_threshold=config.buy_or_sell_threshold,
    )

    population_singleton = providers.Singleton(
        Population,
        actor_factory=actor_factory.provider,
        world=world_singleton,
        actor_count=config.actor_count,
        genomes=config.genomes,
    )

    simulation_factory = providers.Singleton(
        Simulation,
        world=world_singleton,
        population=population_singleton,
        generation_count=config.generation_count,
        save_to=config.save_genomes,
    )
