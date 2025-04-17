from bitarray import bitarray
from node import Node


class AdaptiveHuffmanTree:
    def __init__(self):
        self.nyt = Node()
        self.nodes = [self.nyt] # list of nodes sorted by order
        self.symbol_map = {} # map: symbol -> node

    def root(self):
        return self.nodes[0] if self.nodes else self.nyt

    @staticmethod
    def get_code(node):
        code = bitarray()
        current = node
        while current.parent is not None:
            code.insert(0, 0 if current.parent.left is current else 1)
            current = current.parent

        return code

    def add_node(self, symbol):
        new_internal = Node()
        new_leaf = Node(symbol, 1)

        if self.nyt.parent:
            new_internal.parent = self.nyt.parent
            if new_internal.parent.left == self.nyt:
                new_internal.parent.left = new_internal
            else:
                new_internal.parent.right = new_internal

        new_internal.left = self.nyt
        new_internal.right = new_leaf
        self.nyt.parent = new_internal
        new_leaf.parent = new_internal

        self.nodes.remove(self.nyt)
        self.nodes.extend([new_internal, new_leaf, self.nyt])
        self.symbol_map[symbol] = new_leaf

        return new_internal

    def update_tree(self, node):
        while node is not None:
            leader = self.find_leader(node)
            if leader != node and leader != node.parent:
                self.swap_nodes(node, leader)

            node.freq += 1
            node = node.parent
        # self.print_tree()
        # print("\n"*3)

    def find_leader(self, node):
        # leader - node with the highest order and same frequency as current node
        index = self.nodes.index(node)
        while index > 0 and self.nodes[index - 1].freq == node.freq:
            index -= 1
        return self.nodes[index]

    def swap_nodes(self, node1, node2):
        self.nodes[self.nodes.index(node1)] = node2
        self.nodes[self.nodes.index(node2)] = node1

        node1.parent, node2.parent = node2.parent, node1.parent

        if node1.parent:
            if node1.parent.left == node2:
                node1.parent.left = node1
            else:
                node1.parent.right = node1

        if node2.parent:
            if node2.parent.left == node1:
                node2.parent.left = node2
            else:
                node2.parent.right = node2

    def print_tree(self, node=None, prefix="", is_left=True):
        if node is None:
            node = self.root()
        if node.right:
            new_prefix = prefix + ("│   " if is_left else "    ")
            self.print_tree(node.right, new_prefix, False)

        print(prefix + ("└── " if is_left else "┌── ") + str(node))

        if node.left:
            new_prefix = prefix + ("    " if is_left else "│   ")
            self.print_tree(node.left, new_prefix, True)
