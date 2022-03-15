from enum import unique
from actor import Actor
from brain import Brain
from world import World

class Population:
    def __init__(self, source = '', world: World = []):
        self.actor_count = 1  # TODO: config
        self.actors: list(Actor) = []
        self.world = world

        if len(source) > 0:
            with open(source) as file:
                lines = file.readlines()
                self.actor_count = len(lines)

                for i in range(self.actor_count):
                    self.actors.append(Actor(self.world, i, lines[i]))
        else:
            for i in range(self.actor_count):
                self.actors.append(Actor(self.world, i))

    def select(self):
        sorted_list = sorted(self.actors, key=lambda x: x.balance)[int(len(self.actors) / 2):]
        seen = {actor.genome.hex_string: actor for actor in sorted_list}

        return list(seen.values())

    def reproduce(self, actors):
        unique_count = len(actors)
        self.actors = []

        for i in range(self.actor_count):
            actor = Brain(self.world, i, actors[i % unique_count].genome.hex_string)
            if (i >= unique_count):
                actor.genome.mutate(i >= unique_count)
            self.actors.append(actor)

    def __iter__(self):
        return self.actors.__iter__()


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
