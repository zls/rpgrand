from .rand import RandomItem
from random import randrange

class Property(object):
    def __init__(self, name, values, randomizer, quantity="1"):
        self.name = name
        self.values = values
        self.randomizer = self._get_randomizer(randomizer)
        if '..' in quantity:
            self.random_quantity = True
            self.quantity = quantity
        else:
            self.random_quantity = False
            self.quantity = int(quantity)


    def __str__(self):
        return self.value


    def __repr__(self):
        return "{}".format(self.value)


    def __iter__(self):
        v = []
        if self.random_quantity:
            _s, _e = self.quantity.split('..')
            q = randrange(int(_s),int( _e))
        else:
            q = self.quantity

        for c in range(q):
            yield self.value


    @property
    def value(self):
        return self.randomizer(self.values)


    def _get_randomizer(self, randomizer):
        r = RandomItem()
        return getattr(r, randomizer, lambda: None)
