import heapq
from tree import AdaptiveHuffmanTree
from node import Node, r, e
from bitarray import bitarray
from functools import partial
from bitarray.util import ba2int


def read_from_file(input_file, block_size=32768):
    for block in iter(partial(input_file.read, block_size), ''):
        yield block


def read_chunk(input_file, padding, chunk_size=65536):
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
        self.symbols_map = {}
        self.min_heap = []
        heapq.heappush(self.min_heap, self.tree.nyt)

    def encode(self, input_file_name, output_file_name):
        bits_buffer = bitarray()
        bits_buffer_size = 32768
        try:
            with open(input_file_name, "r") as input_file, \
                    open(output_file_name, "wb") as output_file:

                output_file.write(b'\x00')  # reserved for padding length
                for block in read_from_file(input_file):
                    for character in block:
                        if character in self.symbols_map:
                            node = self.symbols_map[character]
                            node_code = self.tree.get_code(node)
                            node.update_node()
                            #heapq.heapify(self.min_heap)
                        else:
                            node = Node(character)
                            node_code = node.calculate_code(self.tree)
                            self.symbols_map[character] = node
                            heapq.heappush(self.min_heap, node)

                        bits_buffer.extend(node_code)
                        self.tree.update_tree(list(self.min_heap))
                        #self.tree.print_tree()
                        #print('\n'*3)

                        if len(bits_buffer) >= bits_buffer_size:
                            output_file.write(bits_buffer[:bits_buffer_size].tobytes())
                            bits_buffer = bits_buffer[bits_buffer_size:]

                padding = (8 - len(bits_buffer) % 8) % 8
                bits_buffer.fill()
                output_file.write(bits_buffer.tobytes())

                output_file.seek(0)
                output_file.write(padding.to_bytes())
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

                header = input_file.read(1)
                padding = int.from_bytes(header)

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

                        node = node.right if bit else node.left

                    if node.is_nyt():
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

                        ch = chr(value)

                        new_node = Node(ch)
                        heapq.heappush(self.min_heap, new_node)
                    else:
                        ch = node.symbol
                        node.update_node()
                        #heapq.heapify(self.min_heap)

                    write_buffer.append(ch)
                    if len(write_buffer) >= write_buffer_size:
                        output_file.write(''.join(write_buffer))
                        write_buffer = []

                    self.tree.update_tree(list(self.min_heap))

                if write_buffer:
                    output_file.write(''.join(write_buffer))
        except FileNotFoundError:
            print(f"File \"{input_file_name}\" not found!")
        except PermissionError:
            print(f"File \"{input_file_name}\" access denied!")
