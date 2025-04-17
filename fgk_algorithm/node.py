import math
from bitarray import bitarray

number_of_elements = 128  # ASCII
e = int(math.floor(math.log2(number_of_elements)))
r = int(number_of_elements - math.pow(2, e))


class Node:
    def __init__(self, symbol=None, freq=0):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None
        self.parent = None

    def __repr__(self):
        if self.is_leaf():
            return f"Leaf-{self.symbol}({self.freq})"
        else:
            return f"Internal-({self.freq})"

    def is_leaf(self):
        return self.left is None and self.right is None

    def is_nyt(self):
        return self.symbol is None and self.freq == 0

    @staticmethod
    def calculate_code(symbol, tree):
        nyt_node_code = tree.get_code(tree.nyt)
        k = ord(symbol)  # ASCII value
        if 0 <= k <= 2 * r:
            fixed_code = bitarray(format(k, f'0{e + 1}b'))
        else:
            fixed_code = bitarray(format(k - r, f'0{e}b'))

        return nyt_node_code + fixed_code
