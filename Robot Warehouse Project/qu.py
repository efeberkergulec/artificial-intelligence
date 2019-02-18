class Queue:
    def __init__(self, enval=0, deval=0):
        self.items = []
        self.enval = enval
        self.deval = deval

    def enqueue(self, vertex):
        self.items.insert(self.enval, vertex)
        self.enval += 1

    def dequeue(self):
        rt = self.items[self.deval]
        self.items[self.deval] = None
        self.deval += 1
        return rt

    def is_empty(self):
        return (self.enval - self.deval) == 0