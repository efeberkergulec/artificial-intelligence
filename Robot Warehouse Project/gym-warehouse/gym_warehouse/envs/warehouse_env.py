import numpy as np
import sys
from six import StringIO, b

import gym
#from gym import utils
from gym import spaces


MAPS = {
    "8x8": [
        "....A...",
        "........",
        "........",
        "..****..",
        ".....*..",
        "....a*..",
        "........",
        "........"
    ],
    "20x20": [
        ".................C..",
        "....................",
        "...............*****",
        "....................",
        "......A.............",
        "....................",
        "....****............",
        "....*..*......d.....",
        "*****...............",
        ".........*******...B",
        ".........c.....*....",
        "............D..*....",
        "...............*****",
        "....................",
        "....................",
        ".............b......",
        "....................",
        "....a...............",
        "....................",
        "...................."
    ],
}

class SingleRobotWarehouseEnv(gym.Env):
    """
    Warehouse environment to test some MAPF problems
    """

    metadata = {'render.modes': ['human']}

    def __init__(self, desc=None, map='8x8'):
        self.action_space = spaces.Discrete(5)

        if desc is None and map is None:
            raise ValueError('Must provide either desc or map_name')
        elif desc is None:
            desc = MAPS[map]
        self.desc = desc = np.asarray(desc,dtype='c')
        self.nrow, self.ncol = nrow, ncol = desc.shape
        self.observation_space = spaces.Discrete(self.nrow * self.ncol)

        # for agents performance
        self.tot_turns = 0
        self.turn_limit = 1000
        self.tot_reward = 0.0

        self.ACTION_LEFT = 0
        self.ACTION_DOWN = 1
        self.ACTION_RIGHT = 2
        self.ACTION_UP = 3
        self.ACTION_WAIT= 4

        self.robots = []
        self.destinations = []
        for x in np.nditer(self.desc):
            i = x.item().decode('utf-8')
            if i.isalpha() and i.islower():
                self.robots.append(i)
            if i.isalpha() and i.isupper():
                self.destinations.append(i)
        self.robots.sort()
        self.destinations.sort()

        self.states = []
        self.destination_coords = []
        for r in self.robots:
            coord = np.where(self.desc ==b(r))
            self.states.append(coord[0].item()*self.ncol + coord[1].item())
        for r in self.destinations:
            coord = np.where(self.desc ==b(r))
            self.destination_coords.append((coord[0].item(),coord[1].item()))
        
    def step(self, action):

        def to_s(row, col):
            return row*self.ncol + col
        
        def inc(row, col, a):
            if a==0: # left
                col = max(col-1,0)
            elif a==1: # down
                row = min(row+1,self.nrow-1)
            elif a==2: # right
                col = min(col+1,self.ncol-1)
            elif a==3: # up
                row = max(row-1,0)
            return (row, col)

        def print_done():
            print('Turns:',self.tot_turns)
            print('Reward:',self.tot_reward)
            return

        a = [action]
        self.tot_turns += 1
        if self.tot_turns > self.turn_limit:
            self.tot_reward = -1.0
            print_done()
            return (None, -1.0, True)

        if len(a) != len(self.robots):
            print('Wrong actions')
            self.tot_reward = -1.0
            print_done()
            return (None, -1.0, True)
        for i in range(len(self.robots)):
            oldrow, oldcol = self.states[i] // self.ncol, self.states[i] % self.ncol
            if a[i] == self.ACTION_WAIT: continue
            newrow, newcol = inc(oldrow,oldcol,a[i])
            if (newrow,newcol) == (oldrow,oldcol):
                # bumped into the wall
                print('There has been a collision.')
                self.tot_reward = -1.0
                print_done()
                return (None, -1.0, True)
            if self.desc[newrow][newcol] == b'*':
                # obstacle
                print('There has been a collision.')
                self.tot_reward = -1.0
                print_done()
                return (None, -1.0, True)
            n = self.desc[newrow][newcol].item().decode('utf-8')
            if n.isalpha() and n.islower():
                idxn = self.robots.index(n)
                if a[idxn] == self.ACTION_WAIT:
                    # collision between robots
                    print('There has been a collision.')
                    self.tot_reward = -1.0
                    print_done()
                    return (None, -1.0, True)
                if abs(a[i] - a[idxn]) == 2:
                    # edge collision
                    print('There has been a collision.')
                    self.tot_reward = -1.0
                    print_done()
                    return (None, -1.0, True)
            self.desc[newrow][newcol] = b(self.robots[i])
            if self.desc[oldrow][oldcol] ==  b(self.robots[i]):
                self.desc[oldrow][oldcol] = b'.'
            self.states[i] = to_s(newrow,newcol)
        
        for i in range(len(self.destinations)):
            if self.desc[self.destination_coords[i][0]][self.destination_coords[i][1]] == b'.':
                self.desc[self.destination_coords[i][0]][self.destination_coords[i][1]]= b(self.destinations[i])

        # check whether all robots reached their destinations
        for i in range(len(self.robots)):
            rrow, rcol = self.states[i] // self.ncol, self.states[i] % self.ncol
            if (rrow,rcol) != self.destination_coords[i]:
                # not finished yet
                return (None, 0.0, False)

        # finised
        self.tot_reward = 1.0
        print('Well done, the robot has finised its task')
        print_done()
        return (None, 1.0, True)

    def look(self):
        desc = self.desc.tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        return desc

    def render(self, mode='human'):
        outfile = sys.stdout

        desc = self.desc.tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        outfile.write("\n")
        outfile.write("\n".join(''.join(line) for line in desc)+"\n")


class MultiRobotWarehouseEnv(gym.Env):
    """
    Warehouse environment to test some MAPF problems
    """

    metadata = {'render.modes': ['human']}

    def __init__(self, desc=None, map='20x20'):
        self.action_space = spaces.Discrete(5)

        if desc is None and map is None:
            raise ValueError('Must provide either desc or map_name')
        elif desc is None:
            desc = MAPS[map]
        self.desc = desc = np.asarray(desc,dtype='c')
        self.nrow, self.ncol = nrow, ncol = desc.shape
        self.observation_space = spaces.Discrete(self.nrow * self.ncol)

        # for agents performance
        self.tot_turns = 0
        self.turn_limit = 1000
        self.tot_reward = 0.0

        self.ACTION_LEFT = 0
        self.ACTION_DOWN = 1
        self.ACTION_RIGHT = 2
        self.ACTION_UP = 3
        self.ACTION_WAIT= 4

        self.robots = []
        self.destinations = []
        for x in np.nditer(self.desc):
            i = x.item().decode('utf-8')
            if i.isalpha() and i.islower():
                self.robots.append(i)
            if i.isalpha() and i.isupper():
                self.destinations.append(i)
        self.robots.sort()
        self.destinations.sort()

        self.states = []
        self.destination_coords = []
        for r in self.robots:
            coord = np.where(self.desc ==b(r))
            self.states.append(coord[0].item()*self.ncol + coord[1].item())
        for r in self.destinations:
            coord = np.where(self.desc ==b(r))
            self.destination_coords.append((coord[0].item(),coord[1].item()))
        
    def step(self, a):

        def to_s(row, col):
            return row*self.ncol + col
        
        def inc(row, col, a):
            if a==0: # left
                col = max(col-1,0)
            elif a==1: # down
                row = min(row+1,self.nrow-1)
            elif a==2: # right
                col = min(col+1,self.ncol-1)
            elif a==3: # up
                row = max(row-1,0)
            return (row, col)

        def print_done():
            print('Turns:',self.tot_turns)
            print('Reward:',self.tot_reward)
            return

        self.tot_turns += 1
        if self.tot_turns > self.turn_limit:
            self.tot_reward = -1.0
            print_done()
            return (None, -1.0, True)

        if len(a) != len(self.robots):
            print('Wrong actions')
            self.tot_reward = -1.0
            print_done()
            return (None, -1.0, True)
        for i in range(len(self.robots)):
            oldrow, oldcol = self.states[i] // self.ncol, self.states[i] % self.ncol
            if a[i] == self.ACTION_WAIT: continue
            newrow, newcol = inc(oldrow,oldcol,a[i])
            if (newrow,newcol) == (oldrow,oldcol):
                # bumped into the wall
                print('There has been a collision.')
                self.tot_reward = -1.0
                print_done()
                return (None, -1.0, True)
            if self.desc[newrow][newcol] == b'*':
                # obstacle
                print('There has been a collision.')
                self.tot_reward = -1.0
                print_done()
                return (None, -1.0, True)
            n = self.desc[newrow][newcol].item().decode('utf-8')
            if n.isalpha() and n.islower():
                idxn = self.robots.index(n)
                if a[idxn] == self.ACTION_WAIT:
                    # collision between robots
                    print('There has been a collision.')
                    self.tot_reward = -1.0
                    print_done()
                    return (None, -1.0, True)
                if abs(a[i] - a[idxn]) == 2:
                    # edge collision
                    print('There has been a collision.')
                    self.tot_reward = -1.0
                    print_done()
                    return (None, -1.0, True)
            self.desc[newrow][newcol] = b(self.robots[i])
            if self.desc[oldrow][oldcol] ==  b(self.robots[i]):
                self.desc[oldrow][oldcol] = b'.'
            self.states[i] = to_s(newrow,newcol)
        
        for i in range(len(self.destinations)):
            if self.desc[self.destination_coords[i][0]][self.destination_coords[i][1]] == b'.':
                self.desc[self.destination_coords[i][0]][self.destination_coords[i][1]]= b(self.destinations[i])

        # check whether all robots reached their destinations
        for i in range(len(self.robots)):
            rrow, rcol = self.states[i] // self.ncol, self.states[i] % self.ncol
            if (rrow,rcol) != self.destination_coords[i]:
                # not finished yet
                return (None, 0.0, False)

        # finised
        self.tot_reward = 1.0
        print('Well done, the robots have finised their tasks')
        print_done()
        return (None, 1.0, True)

    def look(self):
        desc = self.desc.tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        return desc

    def render(self, mode='human'):
        outfile = sys.stdout

        desc = self.desc.tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        outfile.write("\n")
        outfile.write("\n".join(''.join(line) for line in desc)+"\n")

