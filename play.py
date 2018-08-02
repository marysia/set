import numpy as np
import random
import ast
import time
from collections import defaultdict, namedtuple

from set import Set
from board import Board


class Game:
    def __init__(self, board_shape=(3, 3)):
        ''' Game class
        Specify the allowed input options and their corresponding methods and descriptions, 
        the game variables (board and exit), and player variables that record the player entries
        and time passed.
        '''
        # input options
        Option = namedtuple('Option', 'function help')
        self.options = {
            'set': Option(self.enter_sets, 'to enter a set.'),
            'redraw': Option(self.redraw_board, 'redraw the current board.'),
            'info': Option(self.report_sets, 'report number of available sets.'),
            'hint': Option(self.report_hint, 'get a hint.'),
            'status': Option(self.report_status, 'report current game status.'),
            'quit': Option(self.quit, 'exit the game.')
        }

        # manage game variables
        self.board = Board(rows=board_shape[0], columns=board_shape[1])
        self.exit = False

        # player variables
        self.player_variables = defaultdict(int)
        self.hints = {'set': [], 'hinted': []}
        self.start_time = time.time()

    def start_game(self):
        ''' Introduction to game - print board and play options. '''
        print('Welcome to set! Let\'s start with the current board:')
        print(self.board)
        self.play_options()

    def report_status(self):
        ''' Report status - player variables (hints, valid sets, etc.), time and unplayed cards. '''
        # print all variables in player variables with their corresponding value
        for variable, value in self.player_variables.items():
            variable = variable.replace('_', ' ')
            print(f'{variable}: {value}')

        # print time passed
        time_passed = int((time.time() - self.start_time) / 60)
        print(f'Player played for {time_passed} minute(s).')

        # print remaining cards
        if not self.exit:
            print(f'There are {len(self.board.unplayed_cards)} unplayed cards left.')

    def report_sets(self):
        ''' Report number of available sets on the current board. '''
        print(f'There are {len(self.board.sets_on_board)} sets on this board.')

    def report_hint(self):
        ''' Provide the player with a hint. 

        A new hint request should be a continuation the previously given hints. E.g. if hint g●●● 
        was sampled from set [b◉◉◉, g●●●, r◯◯◯], the next hint should be b◉◉◉ or r◯◯◯. 
        '''
        # add hint request to player variables
        self.player_variables['hints_asked'] += 1

        # New hint set logic: 1) no set yet determined 2) whole set has been hinted 3) set no longer on the board
        refresh_hints = True if len(self.hints['hinted']) == 3 or len(
            self.hints['set']) == 0 else False
        set_on_board = self.board.set_on_board(self.hints['set'])
        refresh_hint_set = not set_on_board if not refresh_hints else True

        if refresh_hint_set:
            # randomly choose a set and a hint.
            hint_options = np.random.choice(self.board.sets_on_board).cards
            hint_chosen = np.random.choice(hint_options)

            # save choices for future reference
            self.hints['set'] = hint_options
            self.hints['hinted'] = [hint_chosen]
        else:
            # choose hint from options (set - already given hints)
            hint_options = [elem for elem in self.hints['set']
                            if elem not in self.hints['hinted']]
            hint_chosen = np.random.choice(hint_options)

            # save chosen hint
            self.hints['hinted'].append(hint_chosen)

        print(
            f"There is a set on this board that contains {self.hints['hinted']}")

    def play_options(self):
        ''' Print play options based on self.options. '''
        play_options_string = 'Play options: \n'
        for action, properties in self.options.items():
            play_options_string += f'\t - {action}: {properties.help}\n'
        print(play_options_string)

    def quit(self):
        ''' Option to quit the program. Report status before exiting. '''
        self.exit = True
        self.report_status()

    def redraw_board(self):
        ''' Redraw the cards on the board. '''
        self.player_variables['board_redrawn'] += 1
        self.board.redraw()
        print(self.board)

    def enter_sets(self):
        ''' Player enters sets. 
        Allow the player to enter a tuple of board coordinates and validate the corresponding cards. 
        Retrieve player input, check validity of the input (e.g. 3 cards, tuples.), check validity of
        the set and update the board and score accordingly. 

        '''
        # Retrieve input
        print('Enter the set in comma-separated tuples, row-column order.')
        given_set_string = input('> ').strip()
        given_set_list = list(ast.literal_eval(given_set_string))

        # Check input validity.
        if len(given_set_list) != 3 or not all([len(elem) == 2 for elem in given_set_list]):
            print('Invalid input.')
            return

        self.player_variables['proposed_sets'] += 1

        # Check set validity
        cards = self.board.get_cards(given_set_list, flattened=False)
        proposed_set = Set(cards)
        valid_set = proposed_set.is_valid(verbose=True)
        valid_verbose = 'valid' if valid_set else 'invalid'
        print(
            f'Proposed set {cards[0], cards[1], cards[2]} is {valid_verbose}.')

        # Update board and score
        if valid_set:
            self.player_variables['valid_sets'] += 1
            self.board.update_board(given_set_list)
            print('\n', self.board)

    def play(self):
        ''' Play game
        Continue playing rounds until stop condition has been satisfied. The stop condition
        is that either the player choses to stop the game, or all cards have been played and 
        there are no remaining sets on the board.
        '''
        # print introduction
        self.start_game()

        # play rounds
        while not self.exit and not self.board.done():
            self.play_round()

    def play_round(self):
        ''' Play round -  a round consists of a single userinput entry that gets executed. '''
        # Retrieve user input
        userinput = input('> ')
        # Parse user input based on the options.
        move = self.options.get(userinput)
        # Execute corresponding method
        move.function() if move is not None else print('Unknown input.')


if __name__ == "__main__":
    game = Game()
    game.play()
