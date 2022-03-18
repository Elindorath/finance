import os
from multiprocessing import Pool
from statistics import mean
import pandas
import matplotlib.pyplot as plt
from pyvis.network import Network
import networkx as nx
from perf_context import timed_performance
from world import World
from population import Population
from sensor import Sensor
from action import Action


class Simulation:
    def __init__(self, world: World, population: Population, save_to=""):
        self.world = world
        self.population = population
        self.save_to = save_to

    def run(self):
        max_generation = 2 # TODO: config
        counter = 0
        # rows = min(len(self.world.dataframe.index), 5000)
        rows = 5000

        results = []

        with timed_performance("Actors trained"):
            for g in range(max_generation):
                print(f"Starting generation {g}")
                # results.append([])

                for actor in self.population:
                    for moment in self.world:
                        actor.run(moment)

                if g < max_generation - 1:
                    self.population.select()
                    # print(f"Survivors balance's: {[survivor.balance for survivor in survivors]}")
                    # print(f"Survivors genome's: {[survivor.genome.hex_string for survivor in survivors]}")
                    self.population.reproduce()

        print(self.population[0].balance)

        #         for timestamp, t in self.world.dataframe.head(rows).iterrows():
        #             # results.append([timestamp, t["close"]])
        #             # results[g].append([timestamp])
        #             counter += 1
        #             # print(t)
        #             # print("===========================")
        #             for actor in self.population.actors:
        #                 actor.run(t)

        #                 # if counter == rows:
        #                 #     results[len(results) - 1].append(actor.balance + actor.goods_count * t["close"])
        #                 # else:
        #                 #     results[len(results) - 1].append(actor.balance)

        #                 # if counter == rows:
        #                 #     results[g][len(results[g]) - 1].append(actor.balance + actor.goods_count * t["close"])
        #                 # else:
        #                 #     results[g][len(results[g]) - 1].append(actor.balance)

        #                 # results[g][len(results[g]) - 1].append(actor.balance_diffs[len(actor.balance_diffs) - 1])


        #     generation_winner = sorted(self.population.actors, key=lambda x: x.balance, reverse=True)[0]
        #     results.append(generation_winner.balance)
        #     print(f"Results: {results}")

        #     if g < max_generation - 1:
        #         survivors = self.population.select()
        #         print(f"Survivors balance's: {[survivor.balance for survivor in survivors]}")
        #         # print(f"Survivors genome's: {[survivor.genome.hex_string for survivor in survivors]}")
        #         self.population.reproduce(survivors)


        # winner = sorted(self.population.actors, key=lambda x: x.balance, reverse=True)[0]

        # graph = nx.DiGraph()

        # for sensor in winner.sensors.values():
        #     graph.add_node(sensor.id)


        # net = Network(width="1920px", height="1080px", directed=True)

        # for sensor in winner.sensors.values():
        #     net.add_node(f"S{sensor.id}", label=self.world.sensors_type[sensor.id], color="blue", group="sensors")

        # for internal in winner.internals.values():
        #     net.add_node(f"I{internal.id}", label=f"N{internal.id}", color="gray", group="internals")

        # for action in winner.actions.values():
        #     net.add_node(f"A{action.id}", label=Action.types[action.id], color="red", group="actions")



        # for sensor in winner.sensors.values():
        #     for [next, weight] in sensor.connected_forward_to.values():
        #         net.add_edge(f"S{sensor.id}", f"{'I' if next.type == 'Internal' else 'A'}{next.id}", value=abs(weight) / 4, color="red" if weight < 0 else "green", title=weight, arrowStrikethrough=False)

        # for internal in winner.internals.values():
        #     for [next, weight] in internal.connected_forward_to.values():
        #         net.add_edge(f"I{internal.id}", f"{'I' if next.type == 'Internal' else 'A'}{next.id}", value=abs(weight) / 4, color="red" if weight < 0 else "green", title=weight, arrowStrikethrough=False)

        # net.show_buttons()

        # net.set_edge_smooth("discrete")
        # net.toggle_physics(False)

        # net.write_html("network.html")


        # columns_to_use = [
        #     # 'timestamp', 'close', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
        #     'timestamp', *list(range(1, self.population.actor_count + 1))
        # ]

        # dataframes = []

        # # for result in results:
        # #     dataframes.append(pandas.DataFrame(result, columns=columns_to_use))
        # # dataframe = pandas.DataFrame(results[len(results) - 1], columns=columns_to_use)
        # dataframe = pandas.DataFrame(results)
        # # print(dataframes[len(dataframes) - 1])

        # print([mean(actor.balance_diffs) for actor in self.population.actors])
        # print([actor.balance for actor in self.population.actors])

        # os.system("wslview network.html")

        # dataframe.plot()

        # # figure = plt.figure()
        # # axes = figure.gca(projection="3d")
        # # z_axis = list(range(1, max_generation + 1))

        # # for z in z_axis:
        # #     # axes.plot(dataframe["timestamp"], dataframe.drop(columns=["timestamp"]).values, zs=z, zdir='y')
        # #     axes.plot(dataframes[z - 1].index, dataframes[z - 1].drop(columns=["timestamp"]).values, zs=z, zdir='y', zorder=max_generation + 2 - z)

        # # axes.set_yticks(z_axis)

        # # figure.legend()
        # # figure.set(dpi=72)

        # # print(f"DPI   : {figure.get_dpi()}")
        # # print(f"Width : {figure.get_figwidth()}")
        # # print(f"Height: {figure.get_figheight()}")
        # # print(f"Bbox  : {axes.get_box_aspect()}")

        # plt.show()

        # # ax = figure.add_subplot(projection="3d")
        # # y_axis = list(range(max_generation))

        # # for i in y_axis:
        # #     ax.plot(dataframe.index, dataframe.values)

        # # plt.show()


        # if len(self.save_to) > 0:
        #     with open(self.save_to, "w") as file:
        #         for actor in self.population.actors:
        #             file.write(f"{actor.genome.hex_string}\n")

        #         print(f"Genomes saved to {self.save_to}")

    def process_actor(self, world, actor):
        rows = min(len(self.world.dataframe.index), 5000)

        for timestamp, t in self.world.dataframe.head(rows).iterrows():
            actor.run(t)

        pass

    def process_time_slice(self, actors, time_slice):
        for actor in actors:
            actor.run(time_slice)

        pass



# create new generation
# iterate over time
# iterate over population
