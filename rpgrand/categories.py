from loaders import Loader
from properties import Property

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
    def create(cls, config_path, source_type="yml", source_loader="file"):
        '''Create object from json config.

        {
            "Type": "config_map",
            "Metadata": {
                "Version": "1"
                "CategoryType": "npc"
            },
            "Config": {
                "Defaults": {
                    "Randomizer": "from_list",
                    "Source": "./foo/bar.yml",
                    "SourceLoader": "file",
                    "SourceType": "yml"
                },
                "Properties": [
                    {
                        "Name": "Name",
                        "Randomizer": "weighted",
                        "Source": "./foo/bar/yml",
                        "SourceLoader": "file",
                        "SourceType": "yml",
                        "SourceKeyPath": ".Names.Unisex",
                        "Sources": [
                            {
                                "Source": ./foo/bar.yml",
                                "SourceLoader": "file",
                                "SourceType": "yml",
                                "SourceKeyPath": ".Names.Unisex"
                            }
                        ]
                    }
                ]
            }
        }
        '''
        _loader = Loader.get_loader(source_type=source_type, source_loader=source_loader)
        config = _loader.load(config_path)
        if config.get("Type") == "config_map":
            properties = cls.create_properties_map(config)
        elif config.get("Type"):
            raise CategoryInvalidConfig("Unknown `Type` {}".format(config["Type"]))
        else:
            raise CategoryInvalidConfig("No `Type` section")
        return cls(**properties)


    @classmethod
    def create_properties_map(cls, config, defaults=None):
        properties = {}
        if not config.get("Config"):
            raise CategoryInvalidConfig("No `Config` section")
        if not config["Config"].get("Properties"):
            raise CategoryInvalidConfig("No `Config.Properties` section")

        config_defaults = config["Config"].get("Defaults", {})
        defaults = {}
        defaults["source"] = config_defaults.get("Source", None)
        defaults["source_loader"] = config_defaults.get("SourceLoader", None)
        defaults["source_type"] = config_defaults.get("SourceType", None)
        defaults["randomizer"] = config_defaults.get("Randomizer", None)
        return _load_properties_from_sources(config["Config"]["Properties"], defaults)


def _load_properties_from_sources(props, defaults):
    properties = {}
    for prop in props:
        if prop.get("Source") and prop.get("Sources"):
            raise CategoryInvalidConfig("`Source` and `Sources` are mutually exclusive")

        if not prop.get("Name"):
            raise CategoryInvalidConfigProperty("No `Name` key in `Config.Properties` item")
        name = prop["Name"]

        if not defaults["source"] and ( not prop.get("Source") and not prop.get("Sources") ):
            raise CategoryInvalidConfigProperty("No `Source` or `Sources` key in `Config.Properties` item and default not set")
        if prop.get("Source"):
            sources = [ prop["Source"] ]
        elif prop.get("Sources"):
            sources = prop["Sources"]
        else:
            sources = [ defaults["source"] ]

        values = []
        for source in sources:
            if type(source) == dict:
                _s = source.get("Source")
                _sl = source.get("SourceLoader")
                _st = source.get("SourceType")
                _rnd = source.get("Randomizer")
            else:
                _s = source
                _sl = prop.get("SourceLoader")
                _st = prop.get("SourceType")
                _rnd = prop.get("Randomizer")

            if not _sl and not defaults["source_loader"]:
                raise CategoryInvalidConfigProperty("No `SourceLoader` key in `Config.Properties` item and default not set")
            source_loader = _sl if _sl else defaults["source_loader"]

            if not _st and not defaults["source_type"]:
                raise CategoryInvalidConfigProperty("No `SourceType` key in `Config.Properties` item and default not set")
            source_type = _st if _st else defaults["source_type"]

            if not _rnd and not defaults["randomizer"]:
                raise CategoryInvalidConfigProperty("No `Randomizer` key in `Config.Properties` item and default not set")
            randomizer = _rnd if _rnd else defaults["randomizer"]

            _loader = Loader.get_loader(source_type=source_type, source_loader=source_loader)
            property_values = _loader.load(_s)
            if prop.get("SourceKeyPath"):
                values += property_values.get(prop["SourceKeyPath"])
            else:
                values += property_values

            properties[name] = Property(name, values, randomizer)
    return properties
