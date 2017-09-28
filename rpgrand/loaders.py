
class Loader(object):

    def __init__(self, load_func):
        self.load_func = load_func

    def load(self, path):
        return self.load_func(path)


    @classmethod
    def get_loader(cls, source_type=None, source_loader=None):

        def yaml_file_load(path):
            from yaml import load
            with open(path) as fobj:
                return load(fobj)

        def json_file_load(path):
            from json import load
            with open(path) as fobj:
                return load(fobj)

        def url_load(path):
            import requests
            r = requests.get(path)
            return r.json()

        if source_loader == "file" and (source_type == "yaml" or source_type == "yml"):
            return cls(yaml_file_load)
        if source_loader == "file" and source_type == "json":
            return cls(json_file_load)
        if source_loader == "url" and source_type == "json":
            return cls(url_load)
