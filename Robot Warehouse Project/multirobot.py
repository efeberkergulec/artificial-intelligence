import gym
import gym_warehouse
from qu import Queue
from copy import deepcopy

''' 1) Create nodes and keep them under an array. In next steps, 
I will assign edges to them and after that I will put them into graph.'''
# WORKING
def create_nodes(arr, mark):
    node_arr = [[None for x in range(len(arr[0]))] for y in range(len(arr))]
    init_node, fin_node = {}, {}
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == '.':
                node_arr[i][j] = {'value': 0, 'left': None, 'right': None, 'up': None, 'down': None, 'neighbours': {}, 'cost': 0, 'parent': None}
            elif 'A' <= arr[i][j] <= 'Z':
                node_arr[i][j] = {'value': 0, 'left': None, 'right': None, 'up': None, 'down': None, 'neighbours': {}, 'cost': 0, 'parent': None}
                fin_node.update({arr[i][j]:(i,j)})
            elif 'a' <= arr[i][j] <= 'z':
                node_arr[i][j] = {'value': 0, 'left': None, 'right': None, 'up': None, 'down': None, 'neighbours': {}, 'cost': 0, 'parent': None}
                init_node.update({arr[i][j]:(i,j)})
            else:
                node_arr[i][j] = None
                mark[i][j] = True
    return init_node, fin_node, node_arr

''' 2) Create edges by using nodes. All path values of edges are equal
right now but I can change them if I can't get enough speed. Result of
this function will be the graph that I will use at my search.'''
# WORKING
def create_edges(node_arr,fin,fin_vals):
    for a in fin_vals:
        x,y = int(fin_vals[a][0]), int(fin_vals[a][1])
        node_arr[x][y] = None

    for i in range(len(node_arr)):
        for j in range(len(node_arr[0])):
            if node_arr[i][j] is None:
                continue
            else:
                node_arr[i][j] = add_edge(node_arr,i,j,fin[0],fin[1])

    for i in range(len(node_arr)):
        for j in range(len(node_arr[0])):
            if node_arr[i][j] == None:
                continue
            else:
                node_arr[i][j]['value'] = manhattan(i,fin[0],j,fin[1])
    return node_arr

''' 2.1) Support function which adds edges to nodes. It is adding to
node['neighbour'] with path value 1. These values can change'''
# WORKING
def add_edge(node_array, xsize, ysize,finx,finy):
    if xsize > len(node_array) or ysize > len(node_array) or xsize < 0 or ysize < 0:
        print("Invalid edge")
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

''' 2.2) Manhattan Method. I am using this method to calculate heuristic 
values of nodes. I am using it just after I create my nodes.'''
# WORKING
def manhattan(x,a,y,b):
    return abs(x - a) + abs(y - b)

''' 3) A* Search. I arrange everything. There is only one step left.
I will take a path as a result. After that, I will do actions to my
robot by the path that I took from this function'''
# WORKING
def a_star_search(graph, start, finish):
    pqueue = set()
    eliminated = set()
    current = start
    pqueue.add(current)
    while pqueue:
        current = min(pqueue, key=lambda o:graph[int(current[0])][int(current[1])]['cost'] + graph[int(current[0])][int(current[1])]['value'])
        if current == finish:
            path = []
            while graph[int(current[0])][int(current[1])]['parent']:
                path.append(current)
                current = graph[int(current[0])][int(current[1])]['parent']
            path.append(current)
            return path[::-1]
        pqueue.remove(current)
        eliminated.add(current)
        for node in graph[int(current[0])][int(current[1])]['neighbours']:
            if node in eliminated:
                continue
            if node in pqueue:
                new_g = graph[int(current[0])][int(current[1])]['cost'] + graph[int(current[0])][int(current[1])]['neighbours'][(node[0],node[1])]
                if graph[int(node[0])][int(node[1])]['cost'] > new_g:
                    graph[int(node[0])][int(node[1])]['cost'] = new_g
                    graph[int(node[0])][int(node[1])]['parent'] = current
            else:
                graph[int(node[0])][int(node[1])]['cost'] = graph[int(current[0])][int(current[1])]['cost'] + graph[int(current[0])][int(current[1])]['neighbours'][(node[0],node[1])]
                graph[int(node[0])][int(node[1])]['parent'] = current
                pqueue.add(node)

''' 4) Action phase. At this step, my agent does action by the help
of this method, my agent analyzes A* Search and does action.'''
# WORKING
def do_an_action(env, path, cur, curarr):
    val = path.pop(0)
    new_cur = val
    px1, py1 = int(cur[0]), int(cur[1])
    px2, py2 = int(new_cur[0]), int(new_cur[1])

    if px1 == px2 and py1 == py2 + 1:
        if new_cur in curarr:
            path.insert(0, new_cur)
            return cur, env.ACTION_WAIT
        else:
            return new_cur, env.ACTION_LEFT
    elif px1 == px2 - 1 and py1 == py2:
        if new_cur in curarr:
            path.insert(0, new_cur)
            return cur, env.ACTION_WAIT
        else:
            return new_cur, env.ACTION_DOWN
    elif px1 == px2 and py1 == py2 - 1:
        if new_cur in curarr:
            path.insert(0, new_cur)
            return cur, env.ACTION_WAIT
        else:
            return new_cur, env.ACTION_RIGHT
    elif px1 == px2 + 1 and py1 == py2:
        if new_cur in curarr:
            path.insert(0, new_cur)
            return cur,env.ACTION_WAIT
        else:
            return new_cur, env.ACTION_UP

def run_agent():
    # create the Gym environment
    env = gym.make('multirobot-warehouse-v0')

    # sense
    s = env.look()

    # marked array that will be used in breadth first search and a* search
    marked = [[False for x in range(len(s))] for y in range(len(s[0]))]

    # creating nodes
    initial_points, final_points, node_array = create_nodes(s,marked)

    # sorts initial and final values, only letter remains (for alphabetical order)
    initial_values, final_values = list(sorted(initial_points)), list(sorted(final_points))

    # I am copying graph and marked to initial points because I have several different roads.
    graphs = [None for x in range(len(initial_points))]

    # create edges
    for i in range(len(graphs)):
        nn = deepcopy(node_array)
        aa = final_points[final_values[0]]
        bb = final_values[0]
        del final_points[final_values[0]]
        final_values.pop(0)
        graphs[i] = create_edges(node_arr=nn,fin=aa,fin_vals=final_points)
        final_points.update({bb: aa})
        final_values.insert(len(final_points) - 1,bb)

    # I am creating paths to let them determine path
    paths = [None for x in range(len(initial_points))]
    current_points, current_values = initial_points, initial_values
    next_steps = [None for x in range(len(initial_points))]

    # for loop for a* search.
    for i in range(len(paths)):
        paths[i] = a_star_search(graph=graphs[i],start=initial_points[initial_values[i]],finish=final_points[final_values[i]])
        paths[i] = paths[i][1:]

    # I will use these variables during my action phase
    dd = False
    mmm = [False for x in range(len(initial_points))]

    while True:
        env.render()    # you can used this for printing the environment

        # think
        for i in range(len(paths)):
            if mmm[i] is True:
                next_steps[i] = env.ACTION_WAIT
            elif len(paths[i]) is not 1:
                current_points[current_values[i]], next_steps[i] = do_an_action(env, paths[i],
                                                                                current_points[current_values[i]],
                                                                                current_points.values())
            elif len(paths[i]) is 1 and mmm[i] is False:
                current_points[current_values[i]], next_steps[i] = do_an_action(env, paths[i],
                                                                                current_points[current_values[i]],
                                                                                current_points.values())
                mmm[i] = True

        # control statement. I am using cont to control status of my agents.
        cont = 0
        for i in range(len(next_steps)):
            if next_steps[i] is env.ACTION_WAIT:
                cont += 1

        # I tried to provide an alternative solution if all agents start to wait
        if cont == len(next_steps):
            for i in range(len(next_steps)):
                if current_points[current_values[i]] is final_points[final_values[i]]:
                    continue
                elif not current_points[current_values[i]] is final_points[final_values[i]] and dd is False:
                    dd = True
                    final_points.update({current_values[i]:current_points[current_values[i]]})
                else:
                    if not current_values[i] in final_points:
                        paths[i] = a_star_search(graph=graphs[i], start=initial_points[initial_values[i]],
                                         finish=final_points[final_values[i]])
                    break

        # act
        ob, rew, done = env.step(next_steps)
        
        if done:
            break
             
    env.close()


if __name__ == "__main__":
    run_agent()


