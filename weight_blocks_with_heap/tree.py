from bitarray import bitarray
from node import Node, number_of_elements
from max_heap import MaxHeap


class AdaptiveHuffmanTree:
    def __init__(self):
        self.order_counter = 2 * number_of_elements - 1
        self.nyt = Node(self.order_counter)
        self.root = self.nyt
        self.symbol_map = {} # map: symbol -> node
        self.weight_blocks = {} # map: weight -> max heap (nodes with same weight)
        self.add_to_weight_block(self.nyt, 0)

    @staticmethod
    def get_code(node):
        code = bitarray()
        current = node
        while current.parent:
            code.insert(0, 0 if current.parent.left is current else 1)
            current = current.parent

        return code

    def add_to_weight_block(self, node, weight):
        if weight not in self.weight_blocks:
            self.weight_blocks[weight] = MaxHeap()
        self.weight_blocks[weight].push(node)

    def update_weight_block(self, node, old_weight, new_weight):
        if old_weight in self.weight_blocks:
            self.weight_blocks[old_weight].remove(node)
        self.add_to_weight_block(node, new_weight)

    def add_node(self, symbol):
        new_internal = Node(self.nyt.order)
        new_leaf = Node(self.nyt.order - 1, symbol, 1)
        new_nyt = Node(self.nyt.order - 2)

        if self.nyt.parent:
            new_internal.parent = self.nyt.parent
            if new_internal.parent.left == self.nyt:
                new_internal.parent.left = new_internal
            else:
                new_internal.parent.right = new_internal
        else:
            self.root = new_internal

        new_internal.left = new_nyt
        new_internal.right = new_leaf
        new_nyt.parent = new_internal
        new_leaf.parent = new_internal

        self.weight_blocks[0].remove(self.nyt)
        self.add_to_weight_block(new_nyt, 0)
        self.add_to_weight_block(new_internal, 0)
        self.add_to_weight_block(new_leaf, 1)

        self.symbol_map[symbol] = new_leaf
        self.nyt = new_nyt

        return new_internal

    def update_tree(self, node):
        while node is not None:
            leader = None
            if node.weight in self.weight_blocks:
                leader = self.weight_blocks[node.weight].top()
            if leader and leader != node and leader != node.parent and leader.order > node.order:
                self.swap_nodes(node, leader)
            old_weight = node.weight
            node.weight += 1
            self.update_weight_block(node, old_weight, node.weight)
            node = node.parent

        # self.print_tree()
        # print("\n"*3)

    def swap_nodes(self, node1, node2):
        # print(f"Nodes to swap:{node1} ---- {node2}")
        if node1.parent is None or node2.parent is None:
            return
        if node1.parent is not node2.parent:
            if node1.parent.left == node1:
                node1.parent.left = node2
            else:
                node1.parent.right = node2

            if node2.parent.left == node2:
                node2.parent.left = node1
            else:
                node2.parent.right = node1

            node1.parent, node2.parent = node2.parent, node1.parent
        else:
            parent = node1.parent
            parent.left = node2
            parent.right = node1

        node1.order, node2.order = node2.order, node1.order

        if node1.weight in self.weight_blocks:
            self.weight_blocks[node1.weight].push(node1)
        if node2.weight in self.weight_blocks:
            self.weight_blocks[node2.weight].push(node2)

        # self.print_tree()
        # print("SWAPPED")
        # print("\n" * 3)


    def print_tree(self, node=None, prefix="", is_left=True):
        if node is None:
            node = self.root
        if node.right:
            new_prefix = prefix + ("│   " if is_left else "    ")
            self.print_tree(node.right, new_prefix, False)

        print(prefix + ("└── " if is_left else "┌── ") + str(node))

        if node.left:
            new_prefix = prefix + ("    " if is_left else "│   ")
            self.print_tree(node.left, new_prefix, True)
