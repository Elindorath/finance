#! /usr/bin/env python

# from src.genome import Genome
# from src.gene import Gene
from src.population import Population


sensors_type = [
    'open_normalized', 'high_normalized', 'low_normalized', 'close_normalized',
    'volume_normalized', 'SMA_10_normalized', 'SMA_40_normalized',
    'RSI_14_normalized', 'MACD_12_26_9_normalized', 'MACDh_12_26_9_normalized',
    'MACDs_12_26_9_normalized', 'STOCHk_14_3_3_normalized',
    'STOCHd_14_3_3_normalized'
]
population = Population("", sensors_type)

bin_strings_before = [gene.bin_string for gene in population.actors[0].genome.genes]
survivors = population.select()
population.reproduce(survivors)
bin_strings_after = [gene.bin_string for gene in population.actors[0].genome.genes]

# genome = Genome()
# bin_strings_before = [gene.bin_string for gene in genome.genes]
# genome.mutate()
# bin_strings_after = [gene.bin_string for gene in genome.genes]
# print("\n".join(["\n".join([before, after, "\n"]) for before, after in zip(bin_strings_before, bin_strings_after)]))


# gene = Gene()
# print(gene.hex_string)
# print(gene.bin_string)
# gene.random_bit_flip()
# print(gene.hex_string)
# print(gene.bin_string)


# gene2 = Gene(gene.hex_string)
# # gene2 = Gene("2be7f26b")
# print(gene2.hex_string)
# print(gene2.bin_string)
# print(
#     gene.transmitter_type == gene2.transmitter_type
#     and gene.transmitter_id == gene2.transmitter_id
#     and gene.receiver_type == gene2.receiver_type
#     and gene.receiver_id == gene2.receiver_id
#     and gene.weight == gene2.weight
# )
# print(genome.get_string())
