from bitarray import bitarray
from node import Node, number_of_elements
import heapq


class AdaptiveHuffmanTree:
    def __init__(self):
        self.max_order = 2 * number_of_elements - 1
        self.nyt = Node(self.max_order)
        self.root = self.nyt
        self.symbol_map = {} # map: symbol -> node
        self.inner_nodes = [] # heap - internal nodes
        self.leaf_nodes = [self.nyt] # heap - leaf nodes

    @staticmethod
    def get_code(node):
        code = bitarray()
        current = node
        while current.parent:
            code.insert(0, 0 if current.parent.left is current else 1)
            current = current.parent

        return code

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

        self.symbol_map[symbol] = new_leaf

        self.leaf_nodes.remove(self.nyt)
        self.nyt = new_nyt

        heapq.heappush(self.inner_nodes, new_internal)
        heapq.heappush(self.leaf_nodes, new_leaf)
        heapq.heappush(self.leaf_nodes, new_nyt)

        # print("LEAF:")
        # print(self.leaf_nodes)
        # print("INNER:")
        # print(self.inner_nodes)
        # print()

        return new_internal

    @staticmethod
    def find_leader(node, nodes_heap):
        # leader - node with the highest order and same weight as updated node
        while nodes_heap:
            current = heapq.heappop(nodes_heap)
            if current.order > node.order and node.parent != current:
                if current.weight == node.weight:
                    return current
                continue
            else:
                return None


    def update_tree(self, node):
        while node:
            # if node is leaf search for a leader among internal nodes
            if node.is_leaf():
                nodes_heap = list(self.inner_nodes)
            # if node is internal search for a leader among leaf nodes
            else:
                nodes_heap = list(self.leaf_nodes)
            leader = self.find_leader(node, nodes_heap)
            if leader:
                self.swap_nodes(node, leader)

            node.weight += 1
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

        if node1.is_leaf() or node2.is_leaf():
            heapq.heapify(self.leaf_nodes)
        if not node1.is_leaf() or not node2.is_leaf():
            heapq.heapify(self.inner_nodes)

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
