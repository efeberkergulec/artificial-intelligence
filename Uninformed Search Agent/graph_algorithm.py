
MAP = [
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"]]


class Vertex:
    def __init__(self, sign=None, xindex=None, yindex=None, neighbours=None, cost=None, left=None,
                 right=None, up=None, down=None, name=None, path=None):
        self.sign = sign  # letter
        self.xindex = xindex  # x location in map
        self.yindex = yindex  # y location in map
        self.neighbours = neighbours  # it keeps neighbours of vertex
        self.path = []  # it keeps path
        self.cost = cost  # distance between source
        self.left = left  # (x,y--)
        self.right = right  # (x,y++)
        self.up = up  # (x--,y)
        self.down = down  # (x++,y)

    def printit(self):
        print("Self sign = {}\nxIndex = {}\nyIndex = {}\nleft node = {}"
              "\nright node = {}\nup node = {}\ndown node = {}\nneighbours = {}\npath = {}\ncost = {}"
              .format((0 if self.sign is None else self.sign),
                      (0 if self.xindex is None else self.xindex),
                      (0 if self.yindex is None else self.yindex),
                      (0 if self.left is None else self.left),
                      (0 if self.right is None else self.right),
                      (0 if self.up is None else self.up),
                      (0 if self.down is None else self.down),
                      (0 if self.neighbours is None else self.neighbours),
                      (0 if self.path is None else self.path),
                      (0 if self.cost is None else self.cost)))
        print("****************************************")

    def print_them(self):
        for s in self.path:
            MAP[s.xindex][s.yindex] = "1"
            strn = ""
            for i in range(len(MAP)):
                for j in range(len(MAP)):
                    strn = strn + str(MAP[i][j])
                strn = strn + "\n"
        MAP[self.path[0].xindex][self.path[0].yindex] = "2"

    def control_path(self, cc):
        count = 0
        for i in self.path:
            if i.sign is 'T':
                count += 1
        if count >= cc:
            return 1
        else:
            return 0

    @staticmethod
    def breadth_first_search(vertex, count):
        vertex.cost = 0
        qu = Queue()
        qu.enqueue(vertex=vertex)
        while qu.is_empty():
            uq = qu.dequeue()
            for sub in uq.neighbours:
                sub.path = uq.path.copy()
                sub.path.append(uq)
                sub.cost = uq.cost + 1
                qu.enqueue(sub)
                # print(sub.cost)
                for found in sub.path:
                    if found is sub:
                        sub.path.remove(found)
                        break
                if sub.sign == 'E':
                    bool = sub.control_path(count)
                    if bool:
                        sub.print_them()
                        MAP[sub.xindex][sub.yindex] = "3"
                        # Graph.print_graph()
                        MAP[sub.xindex][sub.yindex] = "1"
                        print("COST = {}".format(sub.cost + count))
                        return MAP
        return 1

    @staticmethod
    def breadth_first_search_gentle(vertex, count, maxturn):
        vertex.cost = 0
        collect = 0
        qu = Queue()
        qu.enqueue(vertex=vertex)
        while qu.is_empty():
            uq = qu.dequeue()
            for sub in uq.neighbours:
                if sub.cost >= maxturn:
                    print("Maximum number!!!!")
                    return 0
                if sub.sign == 'T':
                    collect += 1
                sub.path = uq.path.copy()
                sub.path.append(uq)
                sub.cost = uq.cost + 1 + collect
                qu.enqueue(sub)
                # print(sub.cost)
                for found in sub.path:
                    if found is sub:
                        sub.path.remove(found)
                        break
                if sub.sign == 'E':
                    bool = sub.control_path(count)
                    if bool:
                        sub.print_them()
                        MAP[sub.xindex][sub.yindex] = "3"
                        # Graph.print_graph()
                        MAP[sub.xindex][sub.yindex] = "1"
                        return MAP
        return 1


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
        return (self.enval - self.deval) > 0


class Graph:
    def __init__(self, arr, xsize, ysize, vertex):
        self.arr = arr
        self.vertex = vertex
        self.xsize = xsize
        self.ysize = ysize
        self.adj = [[vertex for y in range(ysize + 1)] for x in range(xsize + 1)]

    def add_edge(self, n0, xsize, ysize):
        if xsize > self.xsize or ysize > self.ysize or xsize < 0 or ysize < 0:
            print("Invalid edge")
        nx1 = self.adj[xsize + 1][ysize]  # down
        nxm1 = self.adj[xsize - 1][ysize]  # up
        ny1 = self.adj[xsize][ysize + 1]  # right
        nym1 = self.adj[xsize][ysize - 1]  # left
        if xsize == 0:
            if ysize == 0:
                n0.right = ny1
                n0.down = nx1
                n0.neighbours = [n0.right, n0.down]
            elif ysize == self.ysize - 1:
                n0.left = nym1
                n0.down = nx1
                n0.neighbours = [n0.left, n0.down]
            else:
                n0.right = ny1
                n0.down = nx1
                n0.left = nym1
                n0.neighbours = [n0.left, n0.down, n0.right]
        elif xsize == self.xsize - 1:
            if ysize == 0:
                n0.right = ny1
                n0.up = nxm1
                n0.neighbours = [n0.up, n0.right]
            elif ysize == self.ysize - 1:
                n0.left = nym1
                n0.up = nxm1
                n0.neighbours = [n0.left, n0.up]
            else:
                n0.right = ny1
                n0.up = nxm1
                n0.left = nym1
                n0.neighbours = [n0.left, n0.up, n0.right]
        elif ysize == 0:
            if 0 < xsize and xsize < self.xsize - 1:
                n0.down = nx1
                n0.right = ny1
                n0.up = nxm1
                n0.neighbours = [n0.up, n0.right, n0.down]
        elif ysize == self.ysize - 1:
            if 0 < xsize and xsize < self.xsize - 1:
                n0.down = nx1
                n0.left = nym1
                n0.up = nxm1
                n0.neighbours = [n0.left, n0.up, n0.down]
        else:
            n0.down = nx1
            n0.left = nym1
            n0.up = nxm1
            n0.right = ny1
            n0.neighbours = [n0.left, n0.up, n0.right, n0.down]
        return n0

    @staticmethod
    def print_graph():
        strn = ""
        for i in range(len(MAP)):
            for j in range(len(MAP)):
                strn = strn + str(MAP[i][j])
            strn = strn + "\n"
        print(strn)
