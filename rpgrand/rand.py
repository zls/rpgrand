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
        nl = []
        for item in l:
            for times in range(item[0]):
                nl.append(item[1])
        return choice(nl)
