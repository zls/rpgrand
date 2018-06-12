class CategoryInvalidConfig(Exception): pass

class CategoryInvalidConfigProperty(Exception): pass

class Category(object):
    def __init__(self, *args, **kwargs):
        self.items = {}
        self.items.update(**kwargs)


    def get(self):
        ret = {}
        for k, v in self.items.items():
            ret[k] = v.value
        return ret


    def __repr__(self):
        return "{}".format(self.get())


    @classmethod
    def create(cls, config_map):
        return cls(**config_map.properties)
