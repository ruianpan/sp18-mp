'''
A priority queue class optimized for searching frontier management
'''
from heapq import heappush, heappop

import itertools

__author__ = 'Zhengdai Hu'


class Frontier:

    def __init__(self) -> None:
        super().__init__()
        self.priority_queue = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of node to entries
        self.REMOVED = '<removed-task>'  # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def __contains__(self, node):
        return node in self.entry_finder

    def __bool__(self):
        return bool(self.entry_finder)

    def __remove(self, node):
        """Mark an existing node as REMOVED.  Raise KeyError if not found."""
        entry = self.entry_finder.pop(node)
        entry[-1] = self.REMOVED

    def add(self, node, priority):
        """Add a new node or update the priority of an existing node"""
        if node in self.entry_finder:
            self.__remove(node)
        count = next(self.counter)
        entry = [priority, count, node]
        self.entry_finder[node] = entry
        heappush(self.priority_queue, entry)

    @property
    def nearest(self):
        """Remove and return the lowest priority node and its priority. Raise KeyError if empty."""
        while self.priority_queue:
            priority, count, node = self.priority_queue[0]
            if node is not self.REMOVED:
                return node, priority
            else:
                heappop(self.priority_queue)
        raise KeyError('frontier is empty')

    def pop_nearest(self):
        """Remove and return the lowest priority node and its priority. Raise KeyError if empty."""
        while self.priority_queue:
            priority, count, node = heappop(self.priority_queue)
            if node is not self.REMOVED:
                del self.entry_finder[node]
                return node, priority
        raise KeyError('frontier is empty')
