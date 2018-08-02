import numpy as np
from attribute import CARD_ATTRIBUTES, NUMBER_OF_PLAYABLE_CARDS, NUMBER_OF_OPTIONS_PER_PROPERTY

from card import Card
from set import Set


class Board:
    def __init__(self, self.rows=3, self.columns=3):
        ''' Board class
        Manages the cards on the board, the unplayed cards, and can retrieve properties such
        as the number of sets on the board. 
        '''
        # set init variables
        self.rows = rows
        self.columns = columns

        # matrix of card numbers (e.g. 0-80) reshaped (e.g. 3x3x3x3) for conversion between card number and index
        self.card_matrix = np.arange(NUMBER_OF_PLAYABLE_CARDS).reshape(
            NUMBER_OF_OPTIONS_PER_PROPERTY)

        # list of card numbers (e.g. 0-80) that have not yet been played; values will get removed from this
        self.unplayed_cards = list(range(NUMBER_OF_PLAYABLE_CARDS))

        # cards drawn for the rows x columns sized board
        self.cards_on_board = [self.get_unplayed_card()
                               for _ in range(self.rows * self.columns)]

        # define current sets on board
        self.sets_on_board = self.__find_sets()

    def get_unplayed_card(self):
        ''' Retrieve a single unplayed card 
        Randomly choose card number from unplayed cards, remove, and return corresponding card. 

        Returns: 
            card: instance of Card class
        '''
        # Choose a card and remove from unplayed cards
        card_number = np.random.choice(self.unplayed_cards)
        self.unplayed_cards.remove(card_number)

        # Convert card number to actual card
        card = Card().card_number(card_number)
        return card

    def get_cards(self, indices, flattened=False):
        ''' Retrieve cards based on (flattened or unflattened) indices
        Args: 
            indices: list of tuples (e.g. [(2, 1), (1, 0)]) or integers (e.g. [3, 7])
            flattened: bool indicating whether indices are tuples or integers
        Returns: 
            list of cards (Card class)
        '''
        flattened_indices = [self.__get_flattened_index(
            x, y) for x, y in indices] if not flattened else indices
        return [self.cards_on_board[index] for index in flattened_indices]

    def update_board(self, indices):
        ''' Updates board
        Removes given indices from board and replaces with a new unplayed card. 

        Args: 
            indices: list of tuples (e.g. [(2, 1), (1, 0)]) 
        '''
        for x, y in indices:
            index = self.__get_flattened_index(x, y)

            if len(self.unplayed_cards) > 0:
                self.cards_on_board[index] = self.get_unplayed_card()
            else:
                del self.cards_on_board[index]

        self.sets_on_board = self.__find_sets()

    def set_on_board(self, cards):
        ''' Returns whether a set of cards is on the board. '''
        for card in cards:
            if not card in self.cards_on_board:
                return False
        return True

    def redraw(self):
        ''' Redraws all cards on the board - note that the current cards are lost. '''
        self.cards_on_board = [self.get_unplayed_card()
                               for _ in range(self.rows * self.columns)]

    def __get_flattened_index(self, x, y):
        ''' Convert coordinate (e.g. x = 2, y = 1) to flattened index (e.g. 7). '''
        return (x * self.rows) + y

    def done(self):
        ''' Board is satisfied -- no unplayed cards and no sets left on board. '''
        return len(self.unplayed_cards) == 0 and len(self.sets_on_board) == 0

    def __find_sets(self):
        ''' Find sets on board. '''
        found_sets = []
        for i, card1 in enumerate(self.cards_on_board):
            for j, card2 in enumerate(self.cards_on_board[i+1:]):
                for _, card3 in enumerate(self.cards_on_board[j+1:]):
                    set = Set([card1, card2, card3])
                    if set.is_valid(verbose=False):
                        found_sets.append((set))
        return found_sets

    def __repr__(self):
        ''' Representation of the board for printing: self.rows x self.columns grid with card representation. '''
        card_representation = ''
        for i, card in enumerate(self.cards_on_board):
            card_representation += card.get_card() + '\t'
            if (i+1) % self.columns == 0:
                card_representation += '\n'
        return card_representation
