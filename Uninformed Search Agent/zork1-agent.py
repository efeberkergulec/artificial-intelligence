import gym
import gym_hw1
from graph_algorithm import *

def action(MAP,env):
    start_pos = [0,0]
    finish_pos = [0,0]
    count = 0
    temp = 0
    for i in range(len(MAP)):
        for j in range(len(MAP)):
            if MAP[i][j] == "2":
                start_pos = [i,j]
                MAP[i][j] == "1"
                count += 1
            elif MAP[i][j] == "3":
                finish_pos = [i,j]
                MAP[i][j] == "1"
                count += 1
            elif MAP[i][j] == "1":
                count += 1
    temp_pos = start_pos

    marked = [[0 for y in range(len(MAP))] for x in range(len(MAP))]
    s = env.look()

    while temp < count - 1:
        if(s[temp_pos[0]][temp_pos[1]] == 'T'):
            ob, rew, done = env.step(env.ACTION_COLLECT)
        if 0 <= temp_pos[0] <= len(MAP) and 0 <= temp_pos[1] < len(MAP):
            if MAP[temp_pos[0]][temp_pos[1] + 1] == "1" and marked[temp_pos[0]][temp_pos[1] + 1] != 1:
                ob, rew, done = env.step(env.ACTION_RIGHT)
                marked[temp_pos[0]][temp_pos[1] + 1] = 1
                temp_pos[1] += 1
            elif MAP[temp_pos[0]][temp_pos[1] - 1] == "1" and marked[temp_pos[0]][temp_pos[1] - 1] != 1:
                ob, rew, done = env.step(env.ACTION_LEFT)
                marked[temp_pos[0]][temp_pos[1] - 1] = 1
                temp_pos[1] -= 1
            else:
                if 0 <= temp_pos[0] < len(MAP) and 0 <= temp_pos[1] <= len(MAP):
                    if MAP[temp_pos[0] - 1][temp_pos[1]] == "1" and marked[temp_pos[0] - 1][temp_pos[1]] != 1:
                        ob, rew, done = env.step(env.ACTION_UP)
                        marked[temp_pos[0] - 1][temp_pos[1]] = 1
                        temp_pos[0] -= 1
                    elif MAP[temp_pos[0] + 1][temp_pos[1]] == "1" and marked[temp_pos[0] + 1][temp_pos[1]] != 1:
                        ob, rew, done = env.step(env.ACTION_DOWN)
                        marked[temp_pos[0] + 1][temp_pos[1]] = 1
                        temp_pos[0] += 1
        env.render()
        env.loc()
        print("**********************************************")
        temp += 1

    print("Labrynth has solved!")

def run_agent():
    # create the Gym environment
    env = gym.make('zork1-v0')
    env.reset()

    s = env.look()
    zz = env.min_treasure()

    init_node = Vertex(s[0][0],0,0)
    source_node = Vertex(s[0][0],0,0)
    my_graph = Graph(env.look(),len(s),len(s),vertex=init_node)

    for i in range(len(s)):
        for j in range(len(s)):
            rr = Vertex(s[i][j], i, j)
            rr.sign = s[i][j]
            rr.xindex = i
            rr.yindex = j
            if s[i][j] is 'S':
                source_node = rr
            my_graph.adj[i][j] = rr

    t = init_node
    for i in range(len(s)):
        r = t
        for j in range(len(s)):
            my_graph.adj[i][j] = my_graph.add_edge(r, r.xindex, r.yindex)
            # r.printit()
            r = r.right
        t = t.down

    print('I need minimum', zz, 'treasures to go home')

    MAP = Vertex.breadth_first_search(vertex=source_node, count=zz)
    action(MAP,env)

    env.close()

if __name__ == "__main__":
    run_agent()
