import numpy as np
import sys
from six import StringIO, b

from gym import utils
from gym.envs.toy_text import discrete

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

MAPS = {
    "8x8": [
        "XXFXXXXX",
        "........",
        "........",
        "........",
        ".L......",
        "........",
        "........",
        "...S...."
    ],
}


class EscapeEnv(discrete.DiscreteEnv):
    """

    Based on Toy_text FrozenLake environment
    """

    metadata = {'render.modes': ['human']}

    def __init__(self, desc=None, map_name="8x8",is_slippery=False):
        if desc is None and map_name is None:
            raise ValueError('Must provide either desc or map_name')
        elif desc is None:
            desc = MAPS[map_name]
        self.desc = desc = np.asarray(desc,dtype='c')
        self.nrow, self.ncol = nrow, ncol = desc.shape
        self.reward_range = (0, 1)
        self.lights = False

        nA = 4
        self.ACTION_LEFT = 0
        self.ACTION_DOWN = 1
        self.ACTION_RIGHT = 2
        self.ACTION_UP = 3

        nS = nrow * ncol

        isd = np.array(desc == b'S').astype('float64').ravel()
        isd /= isd.sum()

        P = {s : {a : [] for a in range(nA)} for s in range(nS)}

        # for agents performance
        self.tot_turns = 0
        self.turn_limit = 1000
        self.tot_reward = 0.0

        def to_s(row, col):
            return row*ncol + col
        
        def inc(row, col, a):
            if a==0: # left
                col = max(col-1,0)
            elif a==1: # down
                row = min(row+1,nrow-1)
            elif a==2: # right
                col = min(col+1,ncol-1)
            elif a==3: # up
                row = max(row-1,0)
            return (row, col)

        for row in range(nrow):
            for col in range(ncol):
                s = to_s(row, col)
                for a in range(4):
                    li = P[s][a]
                    letter = desc[row, col]
                    if letter in b'FX':
                        li.append((1.0, s, 0, True))
                    else:
                        if is_slippery:
                            for b in [(a-1)%4, a, (a+1)%4]:
                                newrow, newcol = inc(row, col, b)
                                newstate = to_s(newrow, newcol)
                                newletter = desc[newrow, newcol]
                                done = bytes(newletter) in b'GH'
                                rew = float(newletter == b'G')
                                li.append((1.0/3.0, newstate, rew, done))
                        else:
                            newrow, newcol = inc(row, col, a)
                            newstate = to_s(newrow, newcol)
                            newletter = desc[newrow, newcol]
                            done = bytes(newletter) in b'FX'
                            #rew = float(newletter == b'E')
                            if newletter == b'F': rew = 1.0
                            elif newletter== b'X': rew = -1.0
                            else: rew = 0.0
                            li.append((1.0, newstate, rew, done))

        super(EscapeEnv, self).__init__(nS, nA, P, isd)

    def step(self, a):
        self.tot_turns += 1
        ob, rew, done, prb = super(EscapeEnv, self).step(a)
        if self.tot_turns > self.turn_limit:
            done = True
        row, col = self.s // self.ncol, self.s % self.ncol
        if self.desc[row,col] == b'L': self.lights = self.lights != True
        self.tot_reward += rew
        if done:
            if self.desc[row,col] == b'X': print('You died miserably!!!')
            print('Turns:',self.tot_turns)
            print('Reward:',self.tot_reward)
        return (ob,rew,done)

    def look(self):
        desc = self.desc.tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        if not self.lights:
            for c in range(0,self.ncol):
                desc[0][c] = '?'
        return desc

    def loc(self):
        row, col = self.s // self.ncol, self.s % self.ncol
        return (row,col)

    def render(self, mode='human'):
        outfile = StringIO() if mode == 'ansi' else sys.stdout

        row, col = self.s // self.ncol, self.s % self.ncol
        desc = self.desc.tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        if not self.lights:
            for c in range(0,self.ncol):
                desc[0][c] = '?'
        desc[row][col] = utils.colorize(desc[row][col], "red", highlight=True)
        if self.lastaction is not None:
            outfile.write("  ({})\n".format(["Left","Down","Right","Up"][self.lastaction]))
        else:
            outfile.write("\n")
        outfile.write("\n".join(''.join(line) for line in desc)+"\n")

        if mode != 'human':
            return outfile

