from enum import unique
from actor import Actor
from brain import Brain
from world import World

class Population:
    def __init__(self, source = '', world: World = []):
        self.actor_count = 1  # TODO: config
        self.actors: dict[str, Actor] = {}
        # self.actors: list[Actor] = []
        self.world = world

        if len(source) > 0:
            with open(source) as file:
                lines = file.readlines()
                self.actor_count = len(lines)

                for i in range(self.actor_count):
                    self.add_actor(genome_hex=lines[i])
                    # self.actors.append(Actor(self.world, lines[i]))
        else:
            while len(self.actors) < self.actor_count:
                # for i in range(self.actor_count):
                self.add_actor()
                # self.actors.append(Actor(self.world))

    def add_actor(self, *, genome_hex: str='', should_mutate: bool=False):
        actor = Actor(self.world, genome_hex)

        if should_mutate:
            actor.brain.genome.mutate(force=True)

        self.actors[actor.brain.genome.hex_string] = actor

    def select(self):
        survivors = sorted(self.actors.values(), key=lambda actor: actor.balance)[len(self.actors) // 2:]
        # sorted_list = sorted(self.actors, key=lambda x: x.balance)[len(self.actors) // 2:]
        # seen = {actor.brain.genome.hex_string: actor for actor in sorted_list}

        self.actors = {actor.brain.genome.hex_string: actor for actor in survivors}
        # self.actors = list(seen.values())

        return self

    def reproduce(self):
        actors = sorted(self.actors.values(), key=lambda actor: actor.balance, reverse=True)

        for actor in self.actors.values():
            actor.initialize_accounts(self.world)

        for i in range(self.actor_count - len(self)):
            self.add_actor(genome_hex=actors[i].brain.genome.hex_string, should_mutate=True)

    def __iter__(self):
        return self.actors.values().__iter__()

    def __getitem__(self, key) -> Actor:
        return sorted(self.actors.values(), key=lambda actor: actor.balance, reverse=True)[key]

    def __len__(self):
        return self.actors.__len__()

    def __bool__(self):
        return self.actors.__bool__()


        # actors = [*actors, *actors]
        # self.actors = []

        # for i, actor in enumerate(actors):
        #     actor.genome.mutate()
        #     # print(f'N: {actor.genome.genes[0].hex_string}')
        #     # print(f'N: {actor.genome.genes[0].bin_string}')
        #     self.actors.append(Brain(self.sensors_type, i, actor.genome.hex_string))
        #     # print(f'O: {self.actors[len(self.actors) - 1].genome.genes[0].bin_string}')
        #     # print(f'O: {self.actors[len(self.actors) - 1].genome.genes[0].hex_string}')
        #     # print('')
