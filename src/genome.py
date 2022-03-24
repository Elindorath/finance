from typing import Callable

from gene import Gene


class Genome:
    gene_count = 32
    gene_length = 8

    def __init__(self, *, hex_string: str, gene_factory: Callable[..., Gene]) -> None:
        self.genes: list[Gene] = []
        self.hex_string = ''

        for i in range(self.gene_count):
            # if i == 31:
            #     print(hex_string[i * self.gene_length:(i + 1) * self.gene_length])
            gene = gene_factory(hex_string=hex_string[i * self.gene_length:(i + 1) * self.gene_length]) if len(hex_string) > 0 else gene_factory()
            self.genes.append(gene)
            # print(gene.bin_string)
            self.hex_string += gene.hex_string

    def mutate(self, force: bool = False) -> None:
        # print(f"OLD: {self.hex_string}")
        self.hex_string = ''

        for gene in self.genes:
            gene.random_bit_flip(force)
            self.hex_string += gene.hex_string

        # print(f"NEW: {self.hex_string}")
