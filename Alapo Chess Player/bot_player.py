import time
player_id = ""

"""
Initialization of the game.
p_id = player_id
"""


def game_started(env, p_id):
    global player_id
    player_id = p_id
    return True


"""
Write your move returning code to this method.
"""


def move(env):
    print(env.board_output)
    letter_format = input("Type your move:")
    return letter_format


"""
    moves = env.get_possible_moves(env.state, you)
    m = random.choice(moves)
    return m
"""


"""
Get the response of your move here.
"""


def move_response(env, resultCode):
    print(env.board_output)

"""
Opponent Moved - get updated env
"""


def opponent_moved(env):
    print(env.board_output)

"""
Game end
"""


def game_ended(env, result, resultCode):
    print(env.board_output)
    print("Result Code:" +str(resultCode))
    if result == "won":
        print("You won the game")
    elif result == "lost":
        print("You lost the game")
    elif result == "draw":
        print("The game is drew")

"""
Disconnected From Server
"""


def disconnected_from_server():
    pass

"""
Connected to Server
"""


def connected_to_server():
    pass