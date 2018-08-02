import numpy as np

from collections import OrderedDict

from attribute import CARD_ATTRIBUTES, NUMBER_OF_PLAYABLE_CARDS, NUMBER_OF_OPTIONS_PER_PROPERTY

CARD_MATRIX = np.arange(NUMBER_OF_PLAYABLE_CARDS).reshape(
    NUMBER_OF_OPTIONS_PER_PROPERTY)


class Card:
    ''' Class CARD represents a single card in the game Set. '''

    def keywords(self, **kwargs):
        ''' Initialise class using keyworded arguments, e.g. color='red', shape='square', etc.
        Methods asserts the provided keyworded arguments correspond to a valid card
        by ensuring each provided keyworded argument is a card attribute and its value
        is an option for that card attribute, and additionally checking that all card 
        attributes are specified by the arguments. 

        If the card is valid, a representation of the card is made in three forms: 
            * values: a sorted dictionary mapping the card attribute (e.g. 'color') 
                        to a value (e.g. 'red')
            * indices: a tuple indicating the values (e.g. (1, 0, 2, 2) for three 
                        blue empty circles)
            * matrix: an 4x4 matrix zeros matrix with one at the index of the card.
        '''
        # assert valid card
        for key, value in kwargs.items():
            assert key in CARD_ATTRIBUTES.keys()
            assert value in CARD_ATTRIBUTES[key].options
        for name in CARD_ATTRIBUTES.keys():
            assert name in kwargs.keys()

        # set card representations
        self.values = OrderedDict(sorted(kwargs.items()))
        self.indices = self.__get_index_representation()
        self.matrix = self.__get_matrix_representation()
        return self

    def card_tuple(self, card_tuple):
        ''' Initialise class using tuple, e.g. (2, 1, 0, 1)
        Retrieve the matrix and find the values corresponding to the tuple. 
        '''
        # Check for card validity
        assert all([card_tuple[i] < NUMBER_OF_OPTIONS_PER_PROPERTY[i]
                    for i in range(len(card_tuple))])

        # Set all representations
        self.indices = card_tuple
        self.matrix = self.__get_matrix_representation()
        self.values = self.__tuple2values(card_tuple)

        return self

    def card_number(self, card_number):
        ''' Initialise class using card number, e.g. 74 
        Find the indices by looking up the number in the CARD_MATRIX and use the set_card_tuple classmethod.
        '''
        # Check for card validity
        assert np.isin(card_number, CARD_MATRIX)

        # Initialise the class using the corresponding tuple.
        card_array = np.where(CARD_MATRIX == card_number)
        card_tuple = tuple([value[0] for value in card_array])
        self.card_tuple(card_tuple)

        return self

    def __get_index_representation(self):
        ''' Convert every value to its corresponding index and return as tuple. '''
        return tuple([CARD_ATTRIBUTES[name].value2index(value) for name, value in self.values.items()])

    def __get_matrix_representation(self):
        ''' Create an empty matrix of the correct size and fill the appropriate spot with a 1. '''
        # initialise matrix
        shape = [attribute.num_options for attribute in CARD_ATTRIBUTES.values()]
        representation = np.zeros(shape)

        # fill in card representation based on indices
        representation[self.indices] = 1
        return representation

    @staticmethod
    def __tuple2values(card_tuple):
        ''' Convert a tuple to values 
        E.g. (2, 0, 1, 1) to {'color': 'red', 'shape': 'triangle', 'fill': 'dots', 'count': '1}
        '''
        attribute_options = [(name, attribute.options)
                             for name, attribute in CARD_ATTRIBUTES.items()]
        values = [(attribute_options[i][0], attribute_options[i][1][index])
                  for i, index in enumerate(card_tuple)]
        values = dict(values)
        return values

    def get_card(self):
        ''' Return card representation, e.g. g▣▣▣ for three green squares with dots. '''
        # define properties color, count, and symbol (shape + fill combination)
        color = self.values['color'][0]
        count = int(self.values['count'])
        shapes = {
            'square': ['▢', '▣', '■'], 
            'triangle': ['△', '◬', '▲'], 
            'circle': ['◯', '◉', '●']}
        fills = ['empty', 'dots', 'filled']
        symbol = shapes[self.values['shape']][fills.index(self.values['fill'])]

        # combine symbol and properties into representation
        shape_count_fill = symbol * count + ' ' * (3 - count)
        representation = color + shape_count_fill
        return representation

    def __repr__(self):
        return self.get_card()
