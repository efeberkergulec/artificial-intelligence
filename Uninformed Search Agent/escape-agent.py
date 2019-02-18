import gym
import gym_hw1

MAP = [['9', '9', '9', '9', '9', '9', '9', '9'],
       ['0', '0', '0', '0', '0', '0', '0', '0'],
       ['0', '0', '0', '0', '0', '0', '0', '0'],
       ['0', '0', '0', '0', '0', '0', '0', '0'],
       ['0', '0', '0', '0', '0', '0', '0', '0'],
       ['0', '0', '0', '0', '0', '0', '0', '0'],
       ['0', '0', '0', '0', '0', '0', '0', '0'],
       ['0', '0', '0', '0', '0', '0', '0', '0']]

def loc_light(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if (arr[i][j] == 'L'):
                MAP[i][j] = 2
                light = (i, j)
    return light

def find_path(env,arr,x,y):
    loc1x = x[0]
    loc2x = y[0]
    loc1y = x[1]
    loc2y = y[1]

    s = env.look()

    i = loc1x - loc2x
    j = loc1y - loc2y

    for w in range(abs(j)):
        if (j > 0):
            ob, rew, done = env.step(env.ACTION_LEFT)
            loc1y = loc1y - 1
            MAP[loc1x][loc1y] = 1
        elif (j < 0):
            ob, rew, done = env.step(env.ACTION_RIGHT)
            loc1y = loc1y + 1
            MAP[loc1x][loc1y] = 1
        env.render()

    for w in range(abs(i)):
        if(i > 0):
            ob, rew, done = env.step(env.ACTION_UP)
            loc1x = loc1x - 1
            MAP[loc1x][loc1y] = 1
        elif(i < 0):
            ob, rew, done = env.step(env.ACTION_DOWN)
            loc1x = loc1x + 1
            MAP[loc1x][loc1y] = 1
        env.render()

    return 1

def loc_exit(arr):
    for z in range(len(arr[0])):
        if(arr[0][z] == 'F'):
            MAP[0][z] = 3
            return (0,z)
    return 1

def print_map(arr):
    strn = ""
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            strn = strn + str(arr[i][j])
        strn = strn + "\n"
    print(strn)
    return 1

def run_agent():
    # create the Gym environment
    env = gym.make('escape-v0')
    env.reset()

    mp = env.look()
    start_point = env.loc()
    light_point = loc_light(mp)

    MAP[start_point[0]][start_point[1]] = 1

    print("Our starting cell is " + str(start_point) + " and we will first go through our light cell.\n")

    env.render()

    find_path(env,MAP,start_point,light_point)

    print("\nNow let's find our exit cell\n")

    env.render()

    exit_point = loc_exit(env.look())

    find_path(env,MAP,light_point,exit_point)

    print("\nEnd of the cells! I have listed my way from starting cell to finish cell."
          " This is the path.\n")
    print_map(MAP)

    print("0: UNVISITED CELLS\n"
          "1: VISITED CELLS\n"
          "9: DEADS")

    env.close()

if __name__ == "__main__":
    run_agent()

