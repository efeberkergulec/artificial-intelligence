import gym
import gym_warehouse
from qu import Queue

''' 1) Create nodes and keep them under an array. In next steps, 
I will assign edges to them and after that I will put them into graph.'''
# WORKING
def create_nodes(arr, mark):
    node_arr = [[None for x in range(len(arr[0]))] for y in range(len(arr))]
    init_node, fin_node = (0,0), (0,0)
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == '.':
                node_arr[i][j] = {'value': 0, 'left': None, 'right': None, 'up': None, 'down': None, 'neighbours': {}, 'cost': 0, 'parent': None}
            elif 'A' <= arr[i][j] <= 'Z':
                node_arr[i][j] = {'value': 0, 'left': None, 'right': None, 'up': None, 'down': None, 'neighbours': {}, 'cost': 0, 'parent': None}
                fin_node = (i,j)
            elif 'a' <= arr[i][j] <= 'z':
                node_arr[i][j] = {'value': 0, 'left': None, 'right': None, 'up': None, 'down': None, 'neighbours': {}, 'cost': 0, 'parent': None}
                init_node = (i,j)
            else:
                node_arr[i][j] = None
                mark[i][j] = True
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if node_arr[i][j] == None:
                continue
            else:
                node_arr[i][j]['value'] = manhattan(i,fin_node[0],j,fin_node[1])

    return init_node, fin_node, node_arr

''' 1.1) Manhattan Method. I am using this method to calculate heuristic 
values of nodes. I am using it just after I create my nodes.'''
# WORKING
def manhattan(x,a,y,b):
    return abs(x - a) + abs(y - b)

''' 2) Create edges by using nodes. All path values of edges are equal
right now but I can change them if I can't get enough speed. Result of
this function will be the graph that I will use at my search.'''
# WORKING
def create_edges(node_arr,fin):
    for i in range(len(node_arr)):
        for j in range(len(node_arr[0])):
            if node_arr[i][j] is None:
                continue
            else:
                node_arr[i][j] = add_edge(node_arr,i,j,fin[0],fin[1])
    return node_arr

''' 2.1) Support function which adds edges to nodes. It is adding to
node['neighbour'] with path value 1. These values can change'''
# WORKING
def add_edge(node_array, xsize, ysize,finx,finy):
    n0 = node_array[xsize][ysize]
    nx1 = (int(xsize + 1), int(ysize))  # down
    nxm1 = (int(xsize - 1),int(ysize))  # up
    ny1 = (int(xsize),int(ysize + 1))  # right
    nym1 = (int(xsize),int(ysize - 1))  # left
    if xsize == 0:
        if ysize == 0:
            n0['right'] = ny1
            n0['down'] = nx1
            n0['neighbours'].update({ny1: (abs(finx - xsize) + abs(finy - ysize))})
            n0['neighbours'].update({nx1: (abs(finx - xsize) + abs(finy - ysize))})
        elif ysize == len(node_array[0]) - 1:
            n0['left'] = nym1
            n0['down'] = nx1
            n0['neighbours'].update({nym1: (abs(finx - xsize) + abs(finy - ysize))})
            n0['neighbours'].update({nx1: (abs(finx - xsize) + abs(finy - ysize))})
        else:
            n0['left'] = nym1
            n0['right'] = ny1
            n0['down'] = nx1
            n0['neighbours'].update({nym1: (abs(finx - xsize) + abs(finy - ysize))})
            n0['neighbours'].update({ny1: (abs(finx - xsize) + abs(finy - ysize))})
            n0['neighbours'].update({nx1: (abs(finx - xsize) + abs(finy - ysize))})
    elif xsize == len(node_array) - 1:
        if ysize == 0:
            n0['right'] = ny1
            n0['up'] = nxm1
            n0['neighbours'].update({ny1: (abs(finx - xsize) + abs(finy - ysize))})
            n0['neighbours'].update({nxm1: (abs(finx - xsize) + abs(finy - ysize))})
        elif ysize == len(node_array[0]) -1:
            n0['left'] = nym1
            n0['up'] = nxm1
            n0['neighbours'].update({nym1: (abs(finx - xsize) + abs(finy - ysize))})
            n0['neighbours'].update({nxm1: (abs(finx - xsize) + abs(finy - ysize))})
        else:
            n0['left'] = nym1
            n0['up'] = nxm1
            n0['right'] = ny1
            n0['neighbours'].update({nym1: (abs(finx - xsize) + abs(finy - ysize))})
            n0['neighbours'].update({nxm1: (abs(finx - xsize) + abs(finy - ysize))})
            n0['neighbours'].update({ny1: (abs(finx - xsize) + abs(finy - ysize))})
    elif ysize == 0:
        if 0 < xsize < len(node_array) - 1:
            n0['up'] = nxm1
            n0['right'] = ny1
            n0['down'] = nx1
            n0['neighbours'].update({nxm1: (abs(finx - xsize) + abs(finy - ysize))})
            n0['neighbours'].update({ny1: (abs(finx - xsize) + abs(finy - ysize))})
            n0['neighbours'].update({nx1: (abs(finx - xsize) + abs(finy - ysize))})
    elif ysize == len(node_array[0]) - 1:
        if 0 < xsize < len(node_array) - 1:
            n0['left'] = nym1
            n0['up'] = nxm1
            n0['down'] = nx1
            n0['neighbours'].update({nym1: (abs(finx - xsize) + abs(finy - ysize))})
            n0['neighbours'].update({nxm1: (abs(finx - xsize) + abs(finy - ysize))})
            n0['neighbours'].update({nx1: (abs(finx - xsize) + abs(finy - ysize))})
    else:
        n0['left'] = nym1
        n0['up'] = nxm1
        n0['right'] = ny1
        n0['down'] = nx1
        n0['neighbours'].update({nym1: (abs(finx - xsize) + abs(finy - ysize))})
        n0['neighbours'].update({nxm1: (abs(finx - xsize) + abs(finy - ysize))})
        n0['neighbours'].update({ny1: (abs(finx - xsize) + abs(finy - ysize))})
        n0['neighbours'].update({nx1: (abs(finx - xsize) + abs(finy - ysize))})

    if 0 <= nym1[0] < len(node_array) and 0 <= nym1[1] < len(node_array):
        if node_array[nym1[0]][nym1[1]] is None:
            del n0['neighbours'][nym1]
            n0['left'] = None
    if 0 <= nxm1[0] < len(node_array) and 0 <= nxm1[1] < len(node_array):
        if node_array[nxm1[0]][nxm1[1]] is None:
            del n0['neighbours'][nxm1]
            n0['up'] = None
    if 0 <= ny1[0] < len(node_array) and 0 <= ny1[1] < len(node_array):
        if node_array[ny1[0]][ny1[1]] is None:
            del n0['neighbours'][ny1]
            n0['right'] = None
    if 0 <= nx1[0] < len(node_array) and 0 <= nx1[1] < len(node_array):
        if node_array[nx1[0]][nx1[1]] is None:
            del n0['neighbours'][nx1]
            n0['down'] = None
    return n0

''' 3) A* Search. I arrange everything. There is only one step left.
I will take a path as a result. After that, I will do actions to my
robot by the path that I took from this function'''
# WORKING
def a_star_search(graph, start, finish):
    openset = {}
    closedset = {}
    current = start
    openset.update({current: graph[int(current[0])][int(current[1])]['cost']})
    while openset:
        current = min(openset, key=lambda o:graph[int(current[0])][int(current[1])]['cost'] + graph[int(current[0])][int(current[1])]['value'])
        if current == finish:
            path = []
            while graph[int(current[0])][int(current[1])]['parent']:
                path.append(current)
                current = graph[int(current[0])][int(current[1])]['parent']
            path.append(current)
            return path[::-1]
        del openset[current]
        closedset.update({current: graph[int(current[0])][int(current[1])]['cost']})
        for node in graph[int(current[0])][int(current[1])]['neighbours']:
            if node in closedset:
                continue
            if node in openset:
                new_g = graph[int(current[0])][int(current[1])]['cost'] + graph[int(current[0])][int(current[1])]['neighbours'][(node[0],node[1])]
                if graph[int(node[0])][int(node[1])]['cost'] >= new_g:
                    graph[int(node[0])][int(node[1])]['cost'] = new_g
                    graph[int(node[0])][int(node[1])]['parent'] = current
            else:
                graph[int(node[0])][int(node[1])]['cost'] = graph[int(current[0])][int(current[1])]['cost'] + graph[int(current[0])][int(current[1])]['value']
                graph[int(node[0])][int(node[1])]['parent'] = current
                openset.update({node: graph[int(node[0])][int(node[1])]['cost']})

''' 4) Action phase. At this step, my agent does action by the help
of this method, my agent analyzes A* Search and does action.'''
# WORKING
def do_an_action(env, path, cur):
    val = path.pop(0)
    new_cur = val
    px1, py1 = int(cur[0]), int(cur[1])
    px2, py2 = int(new_cur[0]), int(new_cur[1])
    if px1 == px2 + 1 and py1 == py2:
        return new_cur, env.ACTION_UP
    elif px1 == px2 - 1 and py1 == py2:
        return new_cur, env.ACTION_DOWN
    elif px1 == px2 and py1 == py2 + 1:
        return new_cur, env.ACTION_LEFT
    elif px1 == px2 and py1 == py2 - 1:
        return new_cur, env.ACTION_RIGHT

def run_agent():
    # create the Gym environment
    env = gym.make('singlerobot-warehouse-v0')

    # sense
    s = env.look()

    # marked array that will be used in breadth first search and a* search
    marked = [[False for x in range(len(s))] for y in range(len(s[0]))]

    # creating nodes
    initial_point, final_point, node_array = create_nodes(arr=s,mark=marked)

    # adding nodes to edges
    graph = create_edges(node_arr=node_array,fin=final_point)

    # creating path
    path = a_star_search(graph=graph, start=initial_point, finish=final_point)
    path = path[1:]

    # point that will help agent to move
    current_point = initial_point

    while True:
        env.render()    # you can used this for printing the environment

        # think
        current_point, next_step = do_an_action(env,path,current_point)

        # act
        ob, rew, done = env.step(next_step)
        
        if done:
            break

    env.close()


if __name__ == "__main__":
    run_agent()


