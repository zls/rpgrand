from rand import RandomItem

class Property(object):
    def __init__(self, name, values, randomizer):
        self.name = name
        self.values = values
        self.randomizer = self._get_randomizer(randomizer)


    def __str__(self):
        return self.value


    @property
    def value(self):
        return self.randomizer(self.values)


    def _get_randomizer(self, randomizer):
        r = RandomItem()
        if randomizer == "from_list":
            return r.from_list

