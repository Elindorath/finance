from typing import Any


type_bit_count = 1
id_bit_count = 7
weight_bit_count = 16
total_bit_count = type_bit_count * 2 + id_bit_count * 2 + weight_bit_count
point_mutation_rate = 0.001

class Gene:
    def __init__(self, *, random: Any, hex_string: str = '') -> None:
        self.random = random
        self.transmitter_type = 0
        self.transmitter_id = 0
        self.receiver_type = 0
        self.receiver_id = 0
        self.weight = 0
        self.hex_string = ''
        self.bin_string = ''

        if len(hex_string) > 0:
            self.initialize_from_hex_string(hex_string)
        else:
            self.generate_random()

        # self.hex_string = hex(int(self.hex_string, base=2))[2:].zfill(int(total_bit_count / 4))

    # def transmitter_type(self):
    #     return self.string

    # def transmitter_id(self):
    #     return self.string

    # def receiver_type(self):
    #     return self.string

    # def receiver_id(self):
    #     return self.string

    # def weight(self):
    #     return int(self.string[type_bit_count * 2 + id_bit_count * 2:], base=2)

    def generate_random(self) -> None:
        self.transmitter_type = self.random.getrandbits(type_bit_count)
        self.transmitter_id = self.random.getrandbits(id_bit_count)
        self.receiver_type = self.random.getrandbits(type_bit_count)
        self.receiver_id = self.random.getrandbits(id_bit_count)
        self.weight = self.random.getrandbits(weight_bit_count)

        self.bin_string = bin(self.transmitter_type)[2:].zfill(type_bit_count) \
            + bin(self.transmitter_id)[2:].zfill(id_bit_count) \
            + bin(self.receiver_type)[2:].zfill(type_bit_count) \
            + bin(self.receiver_id)[2:].zfill(id_bit_count) \
            + bin(self.weight)[2:].zfill(weight_bit_count)

        self.hex_string = hex(int(self.bin_string, base=2))[2:].zfill(int(total_bit_count / 4))

    def initialize_from_hex_string(self, hex_string: str) -> None:
        self.hex_string = hex_string
        self.bin_string = bin(int(self.hex_string, base=16))[2:].zfill(total_bit_count)

        index = 0
        self.transmitter_type = int(self.bin_string[index:index + type_bit_count], base=2)
        index += type_bit_count
        self.transmitter_id = int(self.bin_string[index:index + id_bit_count], base=2)
        index += id_bit_count
        self.receiver_type = int(self.bin_string[index:index + type_bit_count], base=2)
        index += type_bit_count
        self.receiver_id = int(self.bin_string[index:index + id_bit_count], base=2)
        index += id_bit_count
        self.weight = int(self.bin_string[index:], base=2)

    def random_bit_flip(self, force: bool = False) -> None:
        if force or self.random.random() < point_mutation_rate:
            # print("MUTATE")
            bit_position = self.random.randint(0, total_bit_count - 1)
            mask = 1 << bit_position
            self.initialize_from_hex_string(hex(int(self.bin_string, base=2) ^ mask)[2:].zfill(int(total_bit_count / 4)))



#
#   [1][0110101] [0][0111001] [0001111111100011]
#    ^     ^      ^     ^             ^
# source   |    sink    |           weight
#  type    |    type    |
#      source id     sink id
#
# 4046790627
# f1351fe3
# 11110001 00110101 00011111 11100011
#
