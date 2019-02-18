import time
import numpy as np
import random, math
from copy import deepcopy
player_id = ""
player = None


class AlapoChessPlayer:
    # Pieces to shapes
    p_to_s = {
        'LS': "▢", 'SS': "▫", 'LT': "△", 'ST': "▵", 'LC': "◯", 'SC': "◦",
        'ls': "▣", 'ss': "▪", 'lt': "▲", 'st': "▴", 'lc': "●", 'sc': "•",
        '-': '-'
    }
    # Pieces to ID's
    p_to_i = {
        'LS1': 1, 'LT1': 2, 'LC1': 3, 'LC2': 4, 'LT2': 5, 'LS2': 6,
        'SS1': 7, 'ST1': 8, 'SC1': 9, 'SC2': 10, 'ST2': 11, 'SS2': 12,
        'ls1': -1, 'lt1': -2, 'lc1': -3, 'lc2': -4, 'lt2': -5, 'ls2': -6,
        'ss1': -7, 'st1': -8, 'sc1': -9, 'sc2': -10, 'st2': -11, 'ss2': -12,
        '-': 0
    }
    # ID's to pieces
    i_to_p = {vals:keys for keys, vals in p_to_i.items()}
    # Piece values
    p_values = {'LS': 3, 'LT': 5, 'LC': 10, 'SS': 1, 'ST': 2, 'SC': 3, '-': 0,
                'ls': -3, 'lt': -5, 'lc': -10,'ss': -1, 'st': -2, 'sc': -3}

    def sign(self, x):
        if x > 0:
            return 1
        if x == 0:
            return 0
        return -1

    def __init__(self, player_id, env):
        self.player = self.define_player(player_id)
        self.board = self.initialize_board(env)
        self.values = self.p_values
        self.eat = {1: [], -1: []}
        self.d = 5    # Depth

    ''' Defines player id. Returns true if our player is white. '''
    # DONE
    def define_player(self, p_id):
        if int(p_id) is 1:
            return 1
        else:
            return -1

    ''' Initializes board. Returns an array which has indexes inside it.'''
    # DONE
    def initialize_board(self,env):
        board = [[int(env.state['board'][i][j]) for j in range(len(env.state['board']))]for i in range(len(env.state['board']))]
        return board

    '''Define values for our pieces. Returns a dictionary that holds values'''
    # DONE
    def define_values(self):
        return self.p_values

    ''' Gets possible moves. '''
    def get_moves(self, board, attack=True):
        total_moves = []
        tmeo = 0
        for position, piece_id in np.ndenumerate(board):
            if piece_id != 0 and self.sign(piece_id) == self.sign(self.player):
                piece_name = self.i_to_p[piece_id]
                piece_type = piece_name[0].lower() + piece_name[1].lower()
                if piece_type == 'sc':
                    moves = self.smallcircle_actions(board, position, attack=attack)
                elif piece_type == 'ls':
                    moves = self.largesquare_actions(board,position, attack=attack)
                elif piece_type == 'lc':
                    moves = self.largecircle_actions(board, position, attack=attack)
                elif piece_type == 'ss':
                    moves = self.smallsquare_actions(board, position, attack=attack)
                elif piece_type == 'st':
                    moves = self.smalltriange_actions(board, position, attack=attack)
                elif piece_type == 'lt':
                    moves = self.largetriange_actions(board, position, attack=attack)
                elif piece_type == '-':
                    moves = []
                    continue
                else:
                    raise Exception("ERROR - inexistent piece type ")
                for m in moves:
                    tmeo += 1
                    if self.is_playable(board, m) or self.is_empty(board, m) and not(board[position[0]][position[1]] == 0 and board[m[0]][m[1]] == 0):
                        x0, x1 = position[0], 5 - position[1]
                        total_moves.append({
                            'piece_id': piece_id,
                            'pos': (x0, x1),
                            'new_pos': (m[0], (5 - m[1])),
                            'is_eat': 1 if ((self.sign(board[x0][x1]) != self.sign(board[m[0]][5 - m[1]])) and (self.sign(board[m[0]][5 - m[1]]) != 0)) else 0,
                            'type': 'move'
                        })
                        # print(position, "\t\t", m[0], m[1])
            else:
                continue
        return total_moves

    def smallsquare_actions(self,board, position, attack=True):
        """
        Small Square  ACTIONS
        ------------
        """
        go_to = []

        pos = np.array(position)
        steps = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for step in steps:
            move = pos + np.array(step)
            if attack:
                if self.smallsquare_attack(board, move):
                    go_to.append(move)
            else:
                if self.sah_move(board, move):
                    go_to.append(move)
        return go_to

    def smalltriange_actions(self, board, position, attack=True):
        """
        Small Triange  ACTIONS
        ------------
        """
        go_to = []
        pos = np.array(position)
        steps = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

        for step in steps:
            move = pos + np.array(step)
            if attack:
                if self.smalltriange_attack(board, move):
                    go_to.append(move)
            else:
                if self.sah_move(board, move):
                    go_to.append(move)
        return go_to

    def smallcircle_actions(self,board, position, attack=True):
        """
        SAH / sc  ACTIONS
        ------------
        """
        go_to = []

        pos = np.array(position)
        steps = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

        for step in steps:
            move = pos + np.array(step)
            if attack:
                if self.sah_attack(board, move):
                    go_to.append(move)
            else:
                if self.sah_move(board,move):
                    go_to.append(move)
        return go_to

    def largecircle_actions(self, board, position, attack=True):
        """
        Vezir ACTIONS
        -------------
        """
        go_to = self.largesquare_actions(board,position, attack=attack)
        go_to += self.largetriange_actions(board, position, attack=attack)
        return go_to

    def largesquare_actions(self, board, position, attack=True):
        pos = np.array(position)
        go_to = []
        for i in [-1, +1]:
            step = np.array([i, 0])
            go_to += self.iterative_steps(board, pos, step, attack=attack)

        for j in [-1, +1]:
            step = np.array([0, j])
            go_to += self.iterative_steps(board, pos, step, attack=attack)

        return go_to

    def largetriange_actions(self, board, position, attack=True):
        pos = np.array(position)
        go_to = []

        for i in [-1, +1]:
            for j in [-1, +1]:
                step = np.array([i, j])
                go_to += self.iterative_steps(board, pos, step, attack=attack)
        return go_to

    def iterative_steps(self, board, position, step, attack=True):
        go_to = []
        pos = np.array(position)
        step = np.array(step)
        k = 1
        while True:
            move = pos + k * step
            if attack:
                add_bool, stop_bool = self.control_attackable(board, move)
                if add_bool:
                    go_to.append(move)
                if stop_bool:
                    break
                else:
                    k += 1
            else:
                add_bool, stop_bool = self.control_playable(board, move) # Common boolean for playable_move
                if add_bool:
                    go_to.append(move)
                if stop_bool:
                    break
                else:
                    k += 1
        return go_to

    def sah_move(self,board,move):
        if not self.inside_boundary(move):
            return False
        elif self.is_playable(board, move) or self.is_empty(board, move):
            return True
        return False

    def smalltriange_attack(self,board,move):
        if not self.inside_boundary(move):
            return False
        elif self.is_playable(board, move) or self.is_empty(board, move):
            return True
        return False

    def smallsquare_attack(self,board,move):
        if not self.inside_boundary(move):
            return False
        elif self.is_playable(board, move) or self.is_empty(board, move):
            return True
        return False

    def sah_attack(self,board,move):
        if not self.inside_boundary(move):
            return False
        elif self.is_playable(board, move) or self.is_empty(board, move):
            return True
        return False

    ''' Unites these control statements and make moves. '''
    def control_playable(self, board, move):
        if not self.inside_boundary(move):
            return False, True
        elif not self.is_playable(board, move):
            return False, True
        elif self.is_playable(board, move):
            return False, False
        elif self.is_empty(board, move):
            return True, False
        return False, False

    def control_attackable(self, board, move):
        if not self.inside_boundary(move):
            return False, True
        elif not self.is_playable(board, move):
            return False, True
        elif self.is_playable(board, move):
            return True, True
        elif self.is_empty(board, move):
            return True, False
        return False, False

    ''' Controls whether boundary of tuple is inside the board or not.'''
    def inside_boundary(self,tuple):
        """
        :param tuple: location of the possible move
        :return: returns True if it's inside board. Else it returns False.
        """
        return 0 <= tuple[0] <= 5 and 0 <= tuple[1] <= 5

    ''' Controls whether tuple's location is empty or not, '''
    def is_empty(self,board, tuple):
        """
        :param tuple: location of the possible move
        :return: returns True if location of possible move is empty.
        Else it returns False.
        """
        x, y = tuple[0], tuple[1]
        if board[x][y] == 0:
            return True
        return False

    ''' Controls whether there is another piece or not in tuple's location. '''
    def is_playable(self,board, tuple):
        """
        :param tuple: location of the possible move
        :return: returns True if opponent's piece is at there.
        Else it returns False.
        """
        x, y = tuple[0], tuple[1]
        if self.sign(self.player) != self.sign(board[x][y]):
            return True
        return False

    ''' Our evaluation function. Returns evaluated values of pieces. '''
    def evaluate(self, board, attack=True):
        positive, negative = 0, 0
        for x in range(len(board)):
            for y in range(len(board[0])):

                temp = self.i_to_p[board[x][y]] # Keeps LS1 etc.
                str = temp[:2]  # LS
                board_val = self.p_values[str]  # Values of pieces
                large = temp[:1]
                row = 0
                if self.sign(board[x][y]) == 1:
                    row = (6-x)
                    positive += (row * board_val)

                elif self.sign(board[x][y]) == -1:
                    row = (-(x + 1))
                    negative += (row * board_val)
        if self.player == 1:
            # print("WHITE EVAL VAL",positive - negative)
            return positive - negative
        else:
            # print('BLACK EVAL VAL',negative - positive)
            return negative - positive

    ''' Updates board. Returns an updated location array.'''
    def update_board(self,board,move):
        temp_board = board
        #print('*' * 30)
        #print("UPDATE ==> Current position", (move['pos'][0], move['pos'][1]), " is ", board[move['pos'][0]][move['pos'][1]])
        #print("UPDATE ==> New position", (move['new_pos'][0], move['new_pos'][1]), " is ",board[move['new_pos'][0]][move['new_pos'][1]])
        if move['is_eat']:
            self.eat[self.player].append(board[move['new_pos'][0]][move['new_pos'][1]])
            # del self.p_to_i[self.board[move['new_pos'][0]][move['new_pos'][1]]]
            temp_board[move['pos'][0]][move['pos'][1]], temp_board[move['new_pos'][0]][move['new_pos'][1]] = 0, board[move['pos'][0]][move['pos'][1]]
            # print("eatten sonra", board)
        else:
            temp_board[move['pos'][0]][move['pos'][1]], board[move['new_pos'][0]][move['new_pos'][1]] = board[move['new_pos'][0]][move['new_pos'][1]], board[move['pos'][0]][move['pos'][1]]
            # print("elseden sonra", board)
        return temp_board

    ''' Defines next state of the board by picking move.'''
    def next_state(self,board,move):
        next_board = self.update_board(board,move)
        return next_board

    def max_value(self, state, alpha, beta, depth):
        temp_state = deepcopy(state)
        if depth == self.d:
            return self.evaluate(temp_state)
        v = -math.inf
        for a in self.get_moves(state, True):
            temp_val = self.next_state(temp_state, a)
            temp_state = deepcopy(state)
            v = max(v, self.min_value(temp_val, alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, depth):
        temp_state = deepcopy(state)
        if depth == self.d:
            return self.evaluate(temp_state)
        v = math.inf
        for a in self.get_moves(state, True):
            temp_val = self.next_state(temp_state,a)
            temp_state = deepcopy(state)
            v = min(v, self.max_value(temp_val,alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    ''' Alpha-Beta search algorithm that we used. We picked this
    data from AIMA website and integrate it. '''
    def alphabeta_cutoff_search(self,board):
        # Body of alphabeta_cutoff_search starts here:
        # The default test cuts off at depth d or at a terminal state
        # cutoff_test = (cutoff_test or
        #                (lambda state, depth: depth > d))
        temp_board = deepcopy(board)
        best_score = -math.inf
        beta = math.inf
        best_action = None
        tree = []
        for a in self.get_moves(board, True):
            temp_val = self.next_state(temp_board,a)
            temp_board = deepcopy(board)
            v = self.max_value(temp_val, best_score, beta, 1)
            #print(self.next_state(board,a))
            if a['is_eat'] == 1:
                return a
            elif v > best_score:
                best_score = v
                best_action = a

        return best_action

    ''' Generates an output for terminal input. Returns a string has length 4.'''
    def generate_output(self,move):
        action = str(chr((move['pos'][1])+97))
        action += str(int((move['pos'][0]))+1)
        action += str(chr((move['new_pos'][1])+97))
        action += str(int((move['new_pos'][0]))+1)
        return action

    def get_board_opponent(self, env):
        board = self.initialize_board(env)
        return board

    def move_process(self, env):
        self.board = self.get_board_opponent(env)
        board = deepcopy(self.board)
        m = self.alphabeta_cutoff_search(board)
        letter_format = self.generate_output(m)
        print(m)
        print(letter_format)
        print('##############################\nSON HALI ==> ', self.board)
        print(env.state['board'])
        return letter_format


"""
Initialization of the game.
p_id = player_id
"""


def game_started(env, p_id):
    print(env.board_output)
    global player_id
    player_id = p_id
    global player
    player = AlapoChessPlayer(player_id=player_id, env=env)
    return True


"""
Write your move returning code to this method.
"""


def move(env):
    print("Type your move:")
    letter_format = player.move_process(env)
    return letter_format


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


def game_ended(env, result, resultcode):
    print(env.board_output)
    print(result)
    print("Result code:" + str(resultcode))
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
