from collections import OrderedDict
import numpy as np


class Attribute:
    ''' Attribute class for card attributes. '''

    def __init__(self, name, options):
        ''' Set name (e.g. 'color') and options (e.g. ['red', 'blue', 'green']). '''
        # set initial values
        self.name = name
        self.options = sorted(options)

        # set number of options for this attribute
        self.num_options = len(self.options)

    def value2index(self, value):
        ''' Convert value to index, e.g. 'blue' to 1. '''
        return self.options.index(value)

    def index2value(self, index):
        ''' Convert index to value, e.g. 2 to 'green'. '''
        return self.options[index]


colors = Attribute('color', ['red', 'blue', 'green'])
fills = Attribute('fill', ['empty', 'dots', 'filled'])
shapes = Attribute('shape', ['square', 'triangle', 'circle'])
counts = Attribute('count', ['1', '2', '3'])

attributes_listed = [colors, fills, shapes, counts]
attributes_dict = dict(
    zip([attr.name for attr in attributes_listed], attributes_listed))

# Set importable constants
CARD_ATTRIBUTES = OrderedDict(sorted(attributes_dict.items()))
NUMBER_OF_OPTIONS_PER_PROPERTY = [
    attribute.num_options for attribute in CARD_ATTRIBUTES.values()]
NUMBER_OF_PLAYABLE_CARDS = np.prod(NUMBER_OF_OPTIONS_PER_PROPERTY)
