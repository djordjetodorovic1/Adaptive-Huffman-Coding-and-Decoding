import heapq
from bitarray import bitarray
from node import Node


class AdaptiveHuffmanTree:
    def __init__(self):
        self.nyt = Node("NYT", 0)
        self.root = self.nyt

    @staticmethod
    def get_code(node):
        code = bitarray()
        while node.parent is not None:
            if node.parent.left is node:
                code.insert(0, 0)
            else:
                code.insert(0, 1)
            node = node.parent

        return code

    def update_tree(self, min_heap):
        # Reconstructing tree form heap
        while len(min_heap) > 1:
            n1 = heapq.heappop(min_heap)
            n2 = heapq.heappop(min_heap)
            new_node = Node(None, n1.freq + n2.freq)
            new_node.left = n1
            new_node.right = n2
            n1.parent = new_node
            n2.parent = new_node
            heapq.heappush(min_heap, new_node)

        self.root = min_heap[0]

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
