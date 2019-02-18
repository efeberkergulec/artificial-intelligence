import time

import numpy as np
import rpyc
import gym
from six import StringIO
import gym_alapochess.envs.chess

player1 = "1"  # white pieces
player2 = "-1"  # black pieces
port1 = ""
port2 = ""
game_is_done = False
player1_result = ""
player2_result = ""
player1_moves = []
player2_moves = []
conn_player1 = False
conn_player2 = True
timeout = False
no_captured_count = 0
last_captured_state_1 = 0
last_captured_state_2 = 0
result_code = 500
repeat_limit = 30
time_out_limit = 45
env = gym.make('Alapochess-v1')

# First Player id should be 1.\nSecond Player id should be -1.

if player1 == "1":
    port1 = 8000
elif player1 == "-1":
    port1 = 8001
else:
    raise print("player id is not valid.")
if player2 == "-1":
    port2 = 8001
elif player2 == "1":
    port2 = 8000
else:
    raise print("player id is not valid.")

try:
    proxy1 = rpyc.connect('localhost', port1, config={'allow_public_attrs': True, 'sync_request_timeout': time_out_limit})
    start_result1 = proxy1.root.startgame(env, player1)
    if start_result1:
        print("Player1 is ready")
    else:
        print('Player1 is not ready')
    conn_player1 = True
except:
    conn_player1 = False

try:
    proxy2 = rpyc.connect('localhost', port2, config={'allow_public_attrs': True, 'sync_request_timeout': time_out_limit})
    start_result2 = proxy2.root.startgame(env, player2)
    if start_result2:
        print("Player2 is ready")
    else:
        print('Player2 is not ready')
    conn_player2 = True
except:
    conn_player2 = False

"""
Player 1 Move
"""

def player_1():
    # Get the move from Player1
    move_letter_format = proxy1.root.move(player1, env)
    #Play the move
    move_env_format = convert_envmove_format(move_letter_format)

    piece_id = move_env_format['piece_id']
    new_pos = move_env_format['new_pos']
    action1 = 36*(abs(piece_id) - 1) + (new_pos[0]*6 + new_pos[1]).item()
    state, result, done, __ = env.step(action1, move_env_format)
    player1_moves.append(move_env_format)
    if result == 200:
        proxy1.root.move_response(env, result)
    return state, result, done

"""
Player 2 Move
"""
def player_2():
    # Get the move from Player2
    move_letter_format = proxy2.root.move(player2, env)

    move_env_format = convert_envmove_format(move_letter_format)

    #Play the move
    piece_id = move_env_format['piece_id']
    new_pos = move_env_format['new_pos']
    action2 = 36*(abs(piece_id) - 1) + (new_pos[0]*6 + new_pos[1]).item()
    state, result, done, __ = env.step(action2, move_env_format)
    player2_moves.append(move_env_format)
    if result == 200:
        proxy1.root.opponent_moved(env)
        proxy2.root.move_response(env, result)
    return state, result, done

"""
Converts move from the letter format (a1a4)
to Environment move format.
"""
def convert_envmove_format(letter_format):
    if len(letter_format) == 4:
        try:
            posx = letter_format[0]
            posy = int(letter_format[1]) - 1
            newposx = letter_format[2]
            newposy = int(letter_format[3]) - 1
            convpos = ()
            if posx == "a":
                convpos = (posy, 5)
            elif posx == "b":
                convpos = (posy, 4)
            elif posx == "c":
                convpos = (posy, 3)
            elif posx == "d":
                convpos = (posy, 2)
            elif posx == "e":
                convpos = (posy, 1)
            elif posx == "f":
                convpos = (posy, 0)
            else:
                raise print("Current Position type error")
            convnewpos = 0
            if newposx == "a":
                convnewpos = np.array([newposy, 5], np.int64)
            elif newposx == "b":
                convnewpos = np.array([newposy, 4], np.int64)
            elif newposx == "c":
                convnewpos = np.array([newposy, 3], np.int64)
            elif newposx == "d":
                convnewpos = np.array([newposy, 2], np.int64)
            elif newposx == "e":
                convnewpos = np.array([newposy, 1], np.int64)
            elif newposx == "f":
                convnewpos = np.array([newposy, 0], np.int64)
            else:
                raise print("New Position type error")
            piece_id = env.state['board'][convpos[0]][convpos[1]]
            print(piece_id)
            move = {'piece_id': piece_id, 'pos': convpos, 'new_pos': convnewpos, 'type': 'move'}

            return move
        except BaseException:
            raise print("Error while converting to Env Move format")
        except Exception:
            raise print("Error while converting to Env Move format")
    else:
        raise print("Your move format should be a1a4 etc.")


if conn_player1 and conn_player2:

    while True:
        state = env.state
        board = state['board']
        captured = state['captured']
        timeout = False
        t0 = 0
        try:
            # measure time
            t0 = time.time()
            gen_state, gen_result, done = player_1()
            game_is_done = done
        except TimeoutError:
            print(time.time() - t0, "seconds passed for Player1 to move.")
            player1_result = "lost"
            player2_result = "won"
            print("Time out")
            gen_result = 303
            timeout = True
        except ValueError:
            player1_result = "lost"
            player2_result = "won"
            print("Value error")
            timeout = True
        if timeout:
            break
        if game_is_done:
            if gen_result == 399:
                player1_result = "lost"
                player2_result = "won"
            elif gen_result == 400:
                player1_result = "won"
                player2_result = "lost"
            elif gen_result == 202:
                player1_result = "draw"
                player2_result = "draw"
        # İllegal Move
            elif gen_result == 501:
                player1_result = "lost"
                player2_result = "won"
                print("Player 1 İllegally Moved.")
            # İllegal Action
            elif gen_result == 502:
                player1_result = "lost"
                player2_result = "won"
                print("Player 1 İllegally Moved.")
            result_code = gen_result
            env.reset()
            break
        else:
            result_code = gen_result
            captured_1_state = len(captured[1])
            if last_captured_state_1 == captured_1_state:
                no_captured_count += 1
            elif not(last_captured_state_1 == captured_1_state):
                no_captured_count = 0
            if no_captured_count == repeat_limit:
                print("Draw State")
                game_is_done = True
                player1_result = "draw"
                player2_result = "draw"
                result_code = 201
                break

            last_captured_state_1 = captured_1_state
            timeout = False
            t1 = 0
            try:
                t1 = time.time()
                gen_state, gen_result, done = player_2()
                game_is_done = done
            except TimeoutError:
                # measure time
                print(time.time() - t1, "seconds passed for Player2 to move.")
                player1_result = "won"
                player2_result = "lost"
                gen_result = 303
                timeout = True
            except ValueError:
                player1_result = "won"
                player2_result = "lost"
                print("Value error")
                timeout = True
            if timeout:
                break
            if game_is_done:
              if gen_result == 399:
                  player1_result = "won"
                  player2_result = "lost"
              elif gen_result == 202:
                  player1_result = "draw"
                  player2_result = "draw"
              elif gen_result == 400:
                  player1_result = "lost"
                  player2_result = "won"
              # İllegal Move
              elif gen_result == 501:
                player1_result = "won"
                player2_result = "lost"
                print("Player 2 İllegally Moved.")
              elif gen_result == 502:
                player1_result = "won"
                player2_result = "lost"
                print("Player 2 İllegal Action.")
              gen_result = result_code
              env.reset()
              break
            else:
                if not game_is_done:
                    captured_2_state = len(captured[-1])
                    if last_captured_state_2 == captured_2_state:
                        no_captured_count += 1
                    elif not(last_captured_state_2 == captured_2_state):
                        no_captured_count = 0
                    if no_captured_count == repeat_limit:
                        print("Draw State")
                        game_is_done = True
                        player1_result = "draw"
                        player2_result = "draw"
                        result_code = 201
                        break
                    else:
                        print("No captured for " + str(no_captured_count) + " moves")
                    last_captured_state_2 = captured_2_state
    # Game is over
    try:
        proxy1.root.game_ended(env, player1_result, gen_result)
        proxy2.root.game_ended(env, player2_result, gen_result)
    except:
        pass

    print('\n')
    print('#' * 40)
    print('\n')
    print('GAME IS OVER ')

    print('\n')
    print('#' * 40)
    print('\n')
    print('PLAYER 1 ALL MOVES')
    print('\n')
    print('\n')
    print(player1_moves)
    print('\n')
    print('#' * 40)
    print('\n')
    print('PLAYER 2 ALL MOVES')
    print('\n')
    print('\n')
    print(player2_moves)


    print('\n')
    print('#'*40)
    print('#'*40)
    print('#'*40)
    print("\n PLAYER 1 " + player1_result + " the game.")
    print(" PLAYER 2 " + player2_result + " the game.")
    print('\n')
    env.reset()
else:
    if not conn_player1:
        print("Couldn't connect to 8000")
    if not conn_player2:
        print("Couldn't connect to 8001")