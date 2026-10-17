class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self._values = {}
        self._order = []  # least recent first

    def get(self, key):
        if key not in self._values:
            return -1
        self._order.remove(key)
        self._order.append(key)
        return self._values[key]

    def put(self, key, value):
        if key in self._values:
            self._order.remove(key)
        self._values[key] = value
        self._order.append(key)
        if len(self._order) > self.capacity:
            oldest = self._order.pop(0)
            del self._values[oldest]
