import numpy as np

from attribute import CARD_ATTRIBUTES
from card import Card


class Set:
    def __init__(self, cards):
        ''' Set class
        Has the individual cards and a condensed representation of the cards in matrix
        and indices format, main accessible method is is_valid that determines if the 
        provided set of cards is a valid set. 
        '''
        self.cards = cards
        self.set_matrix = self.__get_condensed_matrix(cards)
        self.set_indices = self.__get_condensed_indices(cards)

    @staticmethod
    def __get_condensed_matrix(cards):
        ''' Condensed matrix representation - sum of individual card matrices. '''
        cards_all_matrices = np.array([card.matrix for card in cards])
        cards_single_matrix = np.sum(cards_all_matrices, axis=0)
        return cards_single_matrix

    @staticmethod
    def __get_condensed_indices(cards):
        ''' Condensed transposed indices representation 
        
        Returns: 
            cards_indices_transposed: list of lists, where each list represents the 
            different attribute values. E.g. three cards with colors red, red and blue
            will be [0, 0, 2].
        '''
        cards_indices = [card.indices for card in cards]
        cards_indices_transposed = list(map(list, zip(*cards_indices)))
        return cards_indices_transposed

    @staticmethod
    def is_valid_attribute(attribute_values):
        ''' Checks individual attribute for validity
        Valid if one unique value, or number of unique values equal to the length.
        E.g. 
            * [0, 0, 2] -> invalid. (red, red, blue)
            * [0, 0, 0] -> valid. (red, red, red)
            * [1, 0, 2] -> valid, (green, red, blue)
        '''
        unique_attribute_values = len(set(attribute_values))
        return unique_attribute_values == 1 or unique_attribute_values == len(attribute_values)

    def is_valid(self, verbose=False):
        ''' Checks set for validity - set is valid if all individual attributes are valid. '''
        # determine validity of attributes and set
        valid_attributes = [self.is_valid_attribute(values) for values in self.set_indices]
        valid_set = all(valid_attributes)
        
        # report invalid attributes if verbose 
        if verbose and not valid_set: 
            invalid_attributes_indices = [i for i, attribute in enumerate(valid_attributes) if not attribute]
            invalid_attributes_names = [list(CARD_ATTRIBUTES.keys())[i] for i in invalid_attributes_indices]
            print(f'The following attribute(s) are not compatible: {", ".join(invalid_attributes_names)}')
            
        return valid_set
        
    def __repr__(self):
        return ' '.join([card.get_card() for card in self.cards])
