from random import choice

class RandomItem():


    @staticmethod
    def from_list(l):
        '''Return a random value from a list.'''
        return choice(l)


    @staticmethod
    def from_dict(d):
        '''Return a random tuple of key, value from items in dictionary.'''
        return choice(list(d.items()))

    @staticmethod
    def weighted(l):
        '''Return a random value from a weighted list.

        [
            [ 1, 'value'],
            [ 2, 'value'],
            [ 1, 'value']
        ]


        '''
        total = sum([x[0] for x in l])
        nl = []
        for item in l:
            for times in range([0]):
                nl.append(x[1])
        return choice(nl)
