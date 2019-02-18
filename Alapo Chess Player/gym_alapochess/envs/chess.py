import io
import sys
import tokenize

from copy import copy
from six import StringIO

import gym
from gym import spaces, error
from gym.utils import seeding
import numpy as np

uniDict = {
    'LS': "▢", 'SS': "▫", 'LT': "△", 'ST': "▵", 'LC': "◯", 'SC': "◦",
    'ls': "▣", 'ss': "▪", 'lt': "▲", 'st': "▴", 'lc': "●", 'sc': "•",
    '-': '-'
}
pieces_to_ids = {
    'LS1': 1, 'LT1': 2, 'LC1': 3, 'LC2': 4, 'LT2': 5, 'LS2': 6,
    'SS1': 7, 'ST1': 8, 'SC1': 9, 'SC2': 10, 'ST2': 11, 'SS2': 12,
    'ls1': -1, 'lt1': -2, 'lc1': -3, 'lc2': -4, 'lt2': -5, 'ls2': -6,
    'ss1': -7, 'st1': -8, 'sc1': -9, 'sc2': -10, 'st2': -11, 'ss2': -12,
    '-': 0
}
# return sign of number

sign = lambda x: (1, -1)[x < 0]

""" 
    AGENT POLICY !!!
    ------------ 
"""

def make_random_policy(np_random):

    def random_policy(state):
        opp_player = -1
        moves = AlapoEnv.get_possible_moves(state, opp_player)
        # No moves left
        if len(moves) == 0:
            return 'resign'
        else:
            return np.random.choice(moves)
    return random_policy

    """ 
    CHESS GYM ENVIRONMENT CLASS
    --------------------------- 
    """

class AlapoEnv(gym.Env):

    # Taş değerleri
    # pieces_values = {'ls': 3, 'lt': 3, 'lc': 10, 'ss': 1, 'sc': 1, 'st': 6, '-': 0}
    ids_to_pieces = {v: k for k, v in pieces_to_ids.items()}
    WHITE = 1
    BLACK = -1
    # metadata = {'render.modes': ['human']}

    def __init__(self, player_color=1, opponent="random", log=True):
    # self.moves_max = 500
        self.log = log

        # One action (for each board position) x (no. of pieces), 2xcastles, offer/accept draw and resign
        self.observation_space = spaces.Box(-12, 12, (6, 6)) # board 8x8
        self.action_space = spaces.Discrete(36*12 + 4)

        #self.player = player_color # define player # TODO: implement
        self.opponent = opponent # define opponent

        # reset and build state
        self.seed()
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)

        # Update the random policy if needed
        if isinstance(self.opponent, str):
            if self.opponent == 'random':
                self.opponent_policy = make_random_policy(self.np_random)
            elif self.opponent == 'none':
                self.opponent_policy = None
            else:
                raise error.Error('Unrecognized opponent policy {}'.format(self.opponent))
        else:
            self.opponent_policy = self.opponent

        return [seed]

    def reset(self):
        """
        Resets the state of the environment, returning an initial observation.
        Outputs -> observation : the initial observation of the space. (Initial reward is assumed to be 0.)
        """
        # reset pieces (pawns that became queen become pawns again)
        AlapoEnv.ids_to_pieces = {v: k for k, v in pieces_to_ids.items()}
        # vars
        self.player_threated = 0
        self.player_threated_piece_id = 0
        self.state = {}
        self.done = False
        self.current_player = 1
        self.move_output = ""
        # material captured
        self.state['captured'] = {1: [], -1: []}
        # current move
        self.state['on_move'] = 1
        # Board
        board = [['LS1', 'LT1', 'LC1', 'LC2', 'LT2', 'LS2']]
        board += [['SS1', 'ST1', 'SC1', 'SC2', 'ST2', 'SS2']]
        board += [['-']*6] * 2
        board += [['ss1', 'st1', 'sc1', 'sc2', 'st2', 'ss2']]
        board += [['ls1', 'lt1', 'lc1', 'lc2', 'lt2', 'ls2']]
        self.state['board'] = np.array([[pieces_to_ids[x] for x in row] for row in board])
        self.state['prev_board'] = copy(self.state['board'])
        self.board_output = AlapoEnv.render_board(self.state, mode='ansi')
        return self.state

        # TODO
        #
        # Let the opponent play if it's not the agent's turn
        # if self.player_color != self.to_play:
        #     a = self.opponent_policy(self.state)
        #     HexEnv.make_move(self.state, a, HexEnv.BLACK)
        #     self.to_play = HexEnv.WHITE

    # Global Variable

    def step(self, action, move):
        """
        Run one timestep of the environment's dynamics. When end of episode
        is reached, reset() should be called to reset the environment's internal state.

        Input
        -----
        action : an action provided by the environment
        move : a move provided by the environment

        Outputs
        -------
        (observation, reward, done, info)
        observation : agent's observation of the current environment
        reward [Float] : amount of reward due to the previous action
        done : a boolean, indicating whether the episode has ended
        info : a dictionary containing other diagnostic information from the previous action
        """
        # validate action
        if not (self.action_space.contains(action)):
            return self.state, 502, True, {'state': self.state}

        if len(AlapoEnv.get_possible_moves(self.state, self.current_player)) == 0:
            print("No moves left")
            return self.state, 202, True,  {'state': self.state}

        move_is_legal = False
        possible_moves = AlapoEnv.get_possible_moves(self.state, self.current_player)
        for m in possible_moves:
            if (m['piece_id'] == move['piece_id']) and (m['pos'] == move['pos']) and (m['new_pos'][0] == move['new_pos'][0]) and (m['new_pos'][1] == move['new_pos'][1]):
                move_is_legal = True

        if not move_is_legal:
            return self.state, 501, True, {'state': self.state}

        # render previous board
        print('Before Move Board State')
        AlapoEnv.render_board(self.state, mode='human')

        # make move
        self.state, result, self.done = self.player_move(
            self.current_player, self.state, action,
            render=self.log, render_msg='Player '+str(self.current_player))
        # render current board
        print('After Move Board State')
        AlapoEnv.render_board(self.state, mode='human')
        self.board_output = AlapoEnv.render_board(self.state, mode='ansi')

        if result == 503:
            print(str(self.current_player) + " resigned the game")

        if self.player_threated == self.current_player:
            if self.player_threated_piece_id in self.state['captured'][-1*self.current_player]:
                if self.current_player == -1:
                    self.state['on_move'] += 1
                self.current_player *= -1
                print("Tehdit eden taş yenildi.")

                self.player_threated = 0
                self.player_threated_piece_id = 0

                return self.state, 200, False, {'state': self.state}
            else:
                print("Tehdit eden taş yenilmedi. Oyunu current player kazandı.")
                return self.state, 400, True,  {'state': self.state}
        elif self.player_threated == -1*self.current_player:
            if self.player_threated_piece_id in self.state['captured'][self.current_player]:
                if self.current_player == -1:
                    self.state['on_move'] += 1
                self.current_player *= -1
                print("Tehdit eden taş yenildi.")

                self.player_threated = 0
                self.player_threated_piece_id = 0

                return self.state, 200, False, {'state': self.state}
            else:
                print("Tehdit eden taş yenilmedi. Oyunu opponent kazandı.")
                return self.state, 399, True,  {'state': self.state}
        # Game is over? if over return rewards etc.

        if self.at_the_end_of_the_board(self.state, self.current_player):
            opponent_attackable = False
            for m in AlapoEnv.get_possible_moves(self.state, -1*self.current_player, True):
                if m['new_pos'][0] == move['new_pos'][0] and m['new_pos'][1] == move['new_pos'][1]:
                    opponent_attackable = True
                    print("Player " + str(self.current_player) + "   " + str(self.player_threated_piece_id) + " idli taş ile tehdit etti.")
                    self.player_threated = self.current_player
                    self.player_threated_piece_id = move['piece_id']
            if not opponent_attackable:
                print("Current player kazandı")
                return self.state, 400, True,  {'state': self.state}
            else:
                if self.current_player == -1:
                    self.state['on_move'] += 1
                self.current_player *= -1
                return self.state, 200, False,  {'state': self.state}
        else:
            # +1 step
            if self.current_player == -1:
                self.state['on_move'] += 1
            self.current_player *= -1
            return self.state, 200, False, {'state': self.state}


    """# player vs. player game
        if not self.opponent_policy:
            # +1 step
            if self.current_player == -1:
                self.state['on_move'] += 1
            self.current_player *= -1
            return self.state, 200, False, {'state': self.state}
    """
    def player_move(self, player, state, action, render=True, render_msg='Player'):
        """
        Returns (state, done)
        """
        # Resign
        if AlapoEnv.has_resigned(action):
            return state, 503, True

        # Play
        move = AlapoEnv.action_to_move(action, player)
        new_state, prev_piece = AlapoEnv.next_state(
            copy(state), move, player)
        # Keep track of movements
        piece_id = move['piece_id']
        #new_state['kr_moves'][piece_id] += 1
        # Save material captured
        if prev_piece != 0:
            new_state['captured'][player].append(prev_piece)
        # Save current state and keep track of repetitions
        #self.saved_states = AlapoEnv.encode_current_state(state, self.saved_states)

        if render:
            if self.current_player == 1:
                render_msg = "Human Player"
            elif self.current_player == -1:
                render_msg = "Bot Player"
            print(render_msg + ' moved \n X : new position \n <> : moved piece \n ++ : captured piece')
            AlapoEnv.render_moves(state, move['piece_id'], [move], mode='human')
            self.move_output = self.render_moves(state, move['piece_id'], [move], mode='ansi')
        return new_state, 0, False

    def _render(self, mode='human', close=False):
        return AlapoEnv.render_board(self.state, mode=mode, close=close)

    @staticmethod
    def render_board(state, mode='human', close=False):
        """
        Render the playing board
        """
        board = state['board']
        outfile = StringIO() if mode == 'ansi' else sys.stdout

        outfile.write('    ')
        outfile.write('-' * 25)
        outfile.write('\n')

        for i in range(5, -1, -1):
            outfile.write(' {} | '.format(i+1))
            for j in range(5, -1, -1):
                piece = AlapoEnv.ids_to_pieces[board[i, j]]
                figure = ""
                if len(piece) == 3:
                    figure = uniDict[piece[0] + piece[1]]
                elif len(piece) == 1:
                    figure = uniDict[piece[0]]
                outfile.write(' {} '.format(figure))
            outfile.write('|\n')
        outfile.write('    ')
        outfile.write('-' * 25)
        outfile.write('\n      a  b  c  d  e  f ')
        outfile.write('\n')
        outfile.write('\n')

        if mode != 'human':
            contents = outfile.getvalue()
            outfile.close()
            return contents


    @staticmethod
    def render_moves(state, piece_id, moves, mode='human'):
        """
        Render the possible moves that a piece can take
        """
        board = state['board']
        moves_pos = [m['new_pos'] for m in moves if m['piece_id'] == piece_id]

        outfile = StringIO() if mode == 'ansi' else sys.stdout
        outfile.write('    ')
        outfile.write('-' * 25)
        outfile.write('\n')

        for i in range(5,-1,-1):
            outfile.write(' {} | '.format(i+1))
            for j in range(5,-1,-1):
                piece = AlapoEnv.ids_to_pieces[board[i,j]]
                piece_second = ""
                if not(len(piece) < 2):
                    piece_second = piece[1]
                piece_new = piece[0] + piece_second
                figure = uniDict[piece_new]

                # check moves + piece
                if board[i,j] == piece_id:
                    outfile.write('<{}>'.format(figure))
                elif moves_pos and any(np.equal(moves_pos, [i, j]).all(1)):
                    if piece == '-':
                        outfile.write(' X ')
                    else:
                        outfile.write('+{}+'.format(figure))
                else:
                    outfile.write(' {} '.format(figure))
            outfile.write('|\n')

        outfile.write('    ')
        outfile.write('-' * 25)
        outfile.write('\n      a  b  c  d  e  f ')
        outfile.write('\n')
        outfile.write('\n')

        if mode != 'human':
            contents = outfile.getvalue()
            outfile.close()
            return contents

    @staticmethod
    def encode_current_state(state, saved_states):
        board = state['board']
        new_saved_states = copy(saved_states)
        # 'LS': "▢", 'SS': "▫", 'LT': "△", 'ST': "▵", 'LC': "◯", 'SC': "◦",
        pieces_encoding = {'-': 0, 'ls': 1, 'lt': 2, 'lc': 3, 'ss': 4, 'st': 5, 'sc': 6}
        encoding = ""
        for i in range(6):
            for j in range(6):
                piece_id = board[i][j]
                player = sign(piece_id)

                piece_str_2 = ""
                if not(len(AlapoEnv.ids_to_pieces[piece_id]) < 2):
                    piece_str_2 = AlapoEnv.ids_to_pieces[piece_id][1]

                piece_str_1 = AlapoEnv.ids_to_pieces[piece_id][0]

                piece_type = piece_str_1.lower() + piece_str_2.lower()
                piece_encode = pieces_encoding[piece_type]
                if piece_encode != 0:
                    piece_encode += 3*(1-player)
                # hex encoding
                encoding += hex(piece_encode)[2:]
        if encoding in new_saved_states:
            new_saved_states[encoding] += 1
        else:
            new_saved_states[encoding] = 1
        return new_saved_states

    @staticmethod
    def resign_action():
        return 6**2 * 12 + 3

    @staticmethod
    def has_resigned(action):
        return action == AlapoEnv.resign_action()

    @staticmethod
    def move_to_actions(move):
        """
        Encode move into action
        """
        if move == 'resign':
            return AlapoEnv.resign_action()

        else:
            piece_id = move['piece_id']
            new_pos = move['new_pos']
            return 36*(abs(piece_id) - 1) + (new_pos[0]*6 + new_pos[1]).item()

    @staticmethod
    def action_to_move(action, player):
        """
        Decode move from action
        """
        square = action % 36
        column = square % 6
        row = (square - column) // 6
        piece_id = (action - square) // 36 + 1
        return {
            'piece_id': piece_id * player,
            'new_pos': np.array([int(row), int(column)]),
        }

    @staticmethod
    def next_state(state, move, player):
        """
        Return the next state given a move
        -------
        (next_state, previous_piece, reward)
        """
        new_state = copy(state)
        new_state['prev_board'] = copy(state['board'])

        board = copy(new_state['board'])
        new_pos = move['new_pos']
        piece_id = move['piece_id']

        # find old position
        try:
            old_pos = np.array([x[0] for x in np.where(board == piece_id)])
        except:
            print('piece_id', piece_id)
            print(board)
            raise Exception()
        r, c = old_pos[0], old_pos[1]
        board[r, c] = 0

        # replace new position
        new_pos = np.array(new_pos)
        r, c = new_pos
        prev_piece = board[r, c]
        board[r, c] = piece_id

        # Reward for capturing a piece
        """piece_type = ""
        if prev_piece == 0:
            piece_type = AlapoEnv.ids_to_pieces[prev_piece][0].lower()
        else:
            piece_type = AlapoEnv.ids_to_pieces[prev_piece][0].lower() + AlapoEnv.ids_to_pieces[prev_piece][1].lower()
        reward += AlapoEnv.pieces_values[piece_type]
        """

        new_state['board'] = board
        return new_state, prev_piece

    @staticmethod
    def get_possible_actions(state, player):
        moves = AlapoEnv.get_possible_moves(state, player)
        return [AlapoEnv.move_to_actions(m) for m in moves]

    @staticmethod
    def get_possible_moves(state, player, attack=False):
        """
        Returns a list of numpy tuples
        -----
        piece_id - id
        position - (row, ccolumn)
        new_position - (row, column)
        """
        board = state['board']
        total_moves = []
        player = int(player)
        for position, piece_id in np.ndenumerate(board):
            if piece_id != 0 and sign(piece_id) == sign(player):

                piece_name = AlapoEnv.ids_to_pieces[piece_id]
                piece_type = piece_name[0].lower() + piece_name[1].lower()
                if piece_type == 'sc':
                    moves = AlapoEnv.smallcircle_actions(state, position, player, attack=attack)
                elif piece_type == 'ls':
                    moves = AlapoEnv.largesquare_actions(state, position, player, attack=attack)
                elif piece_type == 'lc':
                    moves = AlapoEnv.largecircle_actions(state, position, player, attack=attack)
                elif piece_type == 'ss':
                    moves = AlapoEnv.smallsquare_actions(state, position, player, attack=attack)
                elif piece_type == 'st':
                    moves = AlapoEnv.smalltriange_actions(state, position, player, attack=attack)
                elif piece_type == 'lt':
                    moves = AlapoEnv.largetriange_actions(state, position, player, attack=attack)
                elif piece_type == '-':
                    moves = []
                    continue

                else:
                    raise Exception("ERROR - inexistent piece type ")

                for m in moves:
                    total_moves.append({
                            'piece_id': piece_id,
                            'pos': position,
                            'new_pos': m,
                            'type': 'move'
                    })
            else:
                continue

        return total_moves

    def smallsquare_actions(state, position, player, attack=False):
        """
        Small Square  ACTIONS
        ------------
        """
        go_to = []
        board = state['board']
        pos = np.array(position)
        steps = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for step in steps:
            move = pos + np.array(step)
            if attack:
                if AlapoEnv.smallsquare_attack(state, move, player):
                    go_to.append(move)
            else:
                if AlapoEnv.sah_move(state, move, player):
                  go_to.append(move)
        return go_to

    @staticmethod
    def smalltriange_actions(state, position, player, attack=False):
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
                if AlapoEnv.smalltriange_attack(state, move, player):
                    go_to.append(move)
            else:
                if AlapoEnv.sah_move(state, move, player):
                  go_to.append(move)
        return go_to

    @staticmethod
    def smallcircle_actions(state, position, player, attack=False):
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
                if AlapoEnv.sah_attack(state, move, player):
                    go_to.append(move)
            else:
                if AlapoEnv.sah_move(state, move, player):
                    go_to.append(move)
        return go_to

    @staticmethod
    def largecircle_actions(state, position, player, attack=False):
        """
        Vezir ACTIONS
        -------------
        """
        go_to = AlapoEnv.largesquare_actions(state, position, player, attack=attack)
        go_to += AlapoEnv.largetriange_actions(state, position, player, attack=attack)
        return go_to

    @staticmethod
    def largesquare_actions(state, position, player, attack=False):
        """
        Large Square ACTIONS
        ------------
        """
        pos = np.array(position)
        go_to = []

        for i in [-1, +1]:
            step = np.array([i, 0])
            go_to += AlapoEnv.iterative_steps(state, player, pos, step, attack=attack)

        for j in [-1, +1]:
            step = np.array([0, j])
            go_to += AlapoEnv.iterative_steps(state, player, pos, step, attack=attack)

        return go_to

    @staticmethod
    def largetriange_actions(state, position, player, attack=False):
        """
        BISHOP ACTIONS
        --------------
        """
        pos = np.array(position)
        go_to = []

        for i in [-1, +1]:
            for j in [-1, +1]:
                step = np.array([i, j])
                go_to += AlapoEnv.iterative_steps(state, player, pos, step, attack=attack)
        return go_to

    @staticmethod
    def iterative_steps(state, player, position, step, attack=False):
        """
        Used to calculate large Square, large triange and Large circle moves
        """
        go_to = []
        pos = np.array(position)
        step = np.array(step)
        k = 1
        while True:
            move = pos + k*step
            if attack:
                add_bool, stop_bool = AlapoEnv.attacking_move(state, move, player)
                if add_bool:
                    go_to.append(move)
                if stop_bool:
                    break
                else:
                    k += 1
            else:
                add_bool, stop_bool = AlapoEnv.playable_move(state, move, player)
                if add_bool:
                    go_to.append(move)
                if stop_bool:
                    break
                else:
                    k += 1
        return go_to

    @staticmethod
    def sah_move(state, move, player):
        """
        return squares to which the king can move,
        i.e. unattacked squares that can be:
        - empty squares
        - opponent pieces (excluding king)
        If opponent king is encountered, then there's a problem...
        => return [<bool> add_move]
        """
        board = state['board']
        """checked_squares = AlapoEnv.squares_attacked(state, player)
        """
        if not AlapoEnv.pos_is_in_board(move):
            return False
        elif AlapoEnv.is_own_piece(board, move, player):
            return False
        elif AlapoEnv.is_opponent_piece(board, move, player):
            return True
        elif board[move[0], move[1]] == 0: # empty square move'ın x ve y si boşsa değeri 0.
            return True
        else:
            raise Exception('KING MOVEMENT ERROR \n{} \n{} \n{}'.format(
                board, move, player))

    @staticmethod
    def smalltriange_attack(state, move, player):
        """
        return all the squares that the king can attack, except:
        - squares outside the board
        If opponent triange is encountered, then there's a problem...
        => return [<bool> add_move]
        """
        board = state['board']
        if not AlapoEnv.pos_is_in_board(move):
            return False
        elif AlapoEnv.is_own_piece(board, move, player):
            return True
        elif AlapoEnv.is_opponent_piece(board, move, player):
            return True
        elif board[move[0], move[1]] == 0: # empty square
            return True
        else:
            raise Exception('Small Triange ATTACK ERROR \n{} \n{} \n{}'.format(
                board, move, player))

    @staticmethod
    def smallsquare_attack(state, move, player):
        """
        return all the squares that the king can attack, except:
        - squares outside the board
        If opponent sah is encountered, then there's a problem...
        => return [<bool> add_move]
        """
        board = state['board']
        if not AlapoEnv.pos_is_in_board(move):
            return False
        elif AlapoEnv.is_own_piece(board, move, player):
            return True
        elif AlapoEnv.is_opponent_piece(board, move, player):
            return True
        elif board[move[0], move[1]] == 0: # empty square
            return True
        else:
            raise Exception('Small Square ATTACK ERROR \n{} \n{} \n{}'.format(
                board, move, player))

    @staticmethod
    def sah_attack(state, move, player):
        """
        return all the squares that the king can attack, except:
        - squares outside the board
        If opponent sah is encountered, then there's a problem...
        => return [<bool> add_move]
        """
        board = state['board']
        if not AlapoEnv.pos_is_in_board(move):
            return False
        elif AlapoEnv.is_own_piece(board, move, player):
            return True
        elif AlapoEnv.is_opponent_piece(board, move, player):
            return True
        elif board[move[0], move[1]] == 0: # empty square
            return True
        else:
            raise Exception('KING ATTACK ERROR \n{} \n{} \n{}'.format(
                board, move, player))

    @staticmethod
    def playable_move(state, move, player):
        """
        return squares to which a piece can move
        - empty squares
        - opponent pieces (excluding king)
        => return [<bool> add_move, <bool> break]
        """
        board = state['board']
        if not AlapoEnv.pos_is_in_board(move):
            return False, True
        elif AlapoEnv.is_own_piece(board, move, player):
            return False, True
        elif AlapoEnv.is_opponent_piece(board, move, player):
            return True, True
        elif board[move[0], move[1]] == 0: # empty square
            return True, False
        else:
            raise Exception('MOVEMENT ERROR \n{} \n{} \n{}'.format(board, move, player))

    @staticmethod
    def attacking_move(state, move, player):
        """
        return squares that are attacked or defended
        - empty squares
        - opponent pieces (opponent king is ignored)
        - own pieces
        => return [<bool> add_move, <bool> break]
        """
        board = state['board']
        if not AlapoEnv.pos_is_in_board(move):
            return False, True
        elif AlapoEnv.is_own_piece(board, move, player):
            return True, True
        elif AlapoEnv.is_opponent_piece(board, move, player):
            return True, True
        elif board[move[0], move[1]] == 0: # empty square
            return True, False
        else:
            raise Exception('ATTACKING ERROR \n{} \n{} \n{}'.format(board, move, player))

    """
    - flatten board
    - find move in move list
    """
    @staticmethod
    def move_in_list(move, move_list):
        move_list_flat = [AlapoEnv.flatten_position(m) for m in move_list]
        move_flat = AlapoEnv.flatten_position(move)
        return move_flat in move_list_flat

    @staticmethod
    def flatten_position(position):
        x, y = position[0], position[1]
        return x + y*6

    @staticmethod
    def boardise_position(position):
        x = position % 6
        y = (position - x)//6
        return x, y

    @staticmethod
    def pos_is_in_board(pos):
        return not (pos[0] < 0 or pos[0] > 5 or pos[1] < 0 or pos[1] > 5)

    @staticmethod
    def squares_attacked(state, player):
        opponent_moves = AlapoEnv.get_possible_moves(state, -player, attack=True)
        attacked_pos = [m['new_pos'] for m in opponent_moves]
        return attacked_pos

    # TODO: CHECK IF GAME IS OVER

    @staticmethod
    def at_the_end_of_the_board(state, currplayer):
        board = state['board']
        if currplayer == -1:
            for i in range(0, 6):
                position = 0, i
                if AlapoEnv.is_own_piece(board, position, currplayer):
                    print("Player -1 board'un sonunda")
                    return True
        elif currplayer == 1:
            for i in range(0, 6):
                position = 5, i
                if AlapoEnv.is_own_piece(board, position, currplayer):
                    print("Player 1 board'un sonunda")
                    return True
        return False

    """
    Player Pieces
    """
    @staticmethod
    def is_own_piece(board, position, plyr):
        return AlapoEnv.is_player_piece(board, position, plyr)

    @staticmethod
    def is_opponent_piece(board, position, plyr):
        return AlapoEnv.is_player_piece(board, position, -plyr)

    @staticmethod
    def is_player_piece(board, position, plyr):
        x, y = position
        return board[x, y] != 0 and sign(board[x, y]) == plyr