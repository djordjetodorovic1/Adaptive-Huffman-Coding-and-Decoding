import heapq


class MaxHeap:
    def __init__(self):
        self.heap = []
        self.entry_finder = {}

    def push(self, node):
        if node in self.entry_finder:
            self.remove(node)
        self.entry_finder[node] = node
        heapq.heappush(self.heap, node)

    def top(self):
        while self.heap:
            node = self.heap[0]
            if node in self.entry_finder:
                return node
            heapq.heappop(self.heap)
        return None

    def remove(self, node):
        self.entry_finder.pop(node, None)
