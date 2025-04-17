from tree import AdaptiveHuffmanTree
from node import Node, r, e
from bitarray import bitarray
from functools import partial
from bitarray.util import ba2int


def read_from_file(input_file, block_size=32768):
    for block in iter(partial(input_file.read, block_size), ''):
        yield block


def read_chunk(input_file, padding, chunk_size=32768):
    chunk = input_file.read(chunk_size)
    if not chunk:
        return None
    temp = bitarray()
    temp.frombytes(chunk)
    if len(chunk) < chunk_size and padding > 0:
        return temp[:-padding]
    return temp


class AdaptiveHuffmanCoding:
    def __init__(self):
        self.tree = AdaptiveHuffmanTree()

    def encode(self, input_file_name, output_file_name):
        bits_buffer = bitarray()
        bits_buffer_size = 32768
        try:
            with open(input_file_name, "r") as input_file, \
                    open(output_file_name, "wb") as output_file:

                output_file.write(b'\x00')  # reserved for padding length
                for block in read_from_file(input_file):
                    for character in block:
                        # print("--- CHARACTER: ", character, " ---")
                        if character in self.tree.symbol_map:
                            node = self.tree.symbol_map[character]
                            code = self.tree.get_code(node)
                        else:
                            code = Node.calculate_code(character, self.tree)
                            node = self.tree.add_node(character)
                        bits_buffer.extend(code)
                        self.tree.update_tree(node)

                        if len(bits_buffer) >= bits_buffer_size:
                            output_file.write(bits_buffer[:bits_buffer_size].tobytes())
                            bits_buffer = bits_buffer[bits_buffer_size:]

                padding = (8 - len(bits_buffer) % 8) % 8
                bits_buffer.fill()
                output_file.write(bits_buffer.tobytes())

                output_file.seek(0)
                output_file.write(padding.to_bytes(1))
        except FileNotFoundError:
            print(f"File \"{input_file_name}\" not found!")
        except PermissionError:
            print(f"File \"{input_file_name}\" access denied!")

    def decode(self, input_file_name, output_file_name):
        write_buffer = []
        write_buffer_size = 32768
        try:
            with open(input_file_name, "rb") as input_file, \
                    open(output_file_name, "w") as output_file:

                padding = int.from_bytes(input_file.read(1))
                buffer = read_chunk(input_file, padding)
                bit_index = 0

                while True:
                    if bit_index >= len(buffer):
                        buffer = read_chunk(input_file, padding)
                        if buffer is None:
                            break
                        bit_index = 0

                    node = self.tree.root
                    while not node.is_leaf():
                        if bit_index >= len(buffer):
                            buffer = read_chunk(input_file, padding)
                            if buffer is None:
                                break
                            bit_index = 0
                        bit = buffer[bit_index]
                        bit_index += 1

                        if bit == 0:
                            node = node.left
                        else:
                            node = node.right

                    if node == self.tree.nyt:
                        while len(buffer) - bit_index < e:
                            temp = read_chunk(input_file, padding)
                            if temp is None:
                                break
                            buffer.extend(temp)

                        fixed_bits = buffer[bit_index:bit_index + e]
                        value = ba2int(fixed_bits)
                        bit_index += e

                        if value < r:
                            if len(buffer) - bit_index < 1:
                                temp = read_chunk(input_file, padding)
                                if temp is None:
                                    break
                                buffer.extend(temp)

                            extra_bit = buffer[bit_index]
                            bit_index += 1
                            value = (value << 1) | extra_bit
                        else:
                            value += r

                        character = chr(value)
                        node = self.tree.add_node(character)
                    else:
                        character = node.symbol

                    self.tree.update_tree(node)
                    write_buffer.append(character)
                    if len(write_buffer) >= write_buffer_size:
                        output_file.write(''.join(write_buffer))
                        write_buffer = []

                if write_buffer:
                    output_file.write(''.join(write_buffer))
        except FileNotFoundError:
            print(f"File \"{input_file_name}\" not found!")
        except PermissionError:
            print(f"File \"{input_file_name}\" access denied!")
