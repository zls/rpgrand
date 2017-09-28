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
                        "Source": "./foo/bar.yml",
                        "SourceLoader": "file",
                        "SourceType": "yml",
                        "SourceKeyPath": ".Names.Unisex"
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
        default_source = config_defaults.get("Source", None)
        default_source_loader = config_defaults.get("SourceLoader", None)
        default_source_type = config_defaults.get("SourceType", None)
        default_randomizer = config_defaults.get("Randomizer", None)

        for prop in config["Config"]["Properties"]:
            if not prop.get("Name"):
                raise CategoryInvalidConfigProperty("No `Name` key in `Config.Properties` item")
            name = prop["Name"]

            if not prop.get("Source") and not default_source:
                raise CategoryInvalidConfigProperty("No `Source` key in `Config.Properties` item and default not set")
            source = prop.get("Source") if prop.get("Source") else default_source

            if not prop.get("SourceLoader") and  not default_source_loader:
                raise CategoryInvalidConfigProperty("No `SourceLoader` key in `Config.Properties` item and default not set")
            source_loader = prop.get("SourceLoader") if prop.get("SourceLoader") else default_source_loader

            if not prop.get("SourceType") and not default_source_type:
                raise CategoryInvalidConfigProperty("No `SourceType` key in `Config.Properties` item and default not set")
            source_type = prop.get("SourceType") if prop.get("SourceType") else default_source_type

            if not prop.get("Randomizer") and not default_randomizer:
                raise CategoryInvalidConfigProperty("No `Randomizer` key in `Config.Properties` item and default not set")
            randomizer = prop.get("Randomizer") if prop.get("Randomizer") else default_randomizer

            _loader = Loader.get_loader(source_type=source_type, source_loader=source_loader)
            property_values = _loader.load(source)
            if prop.get("SourceKeyPath"):
                values = property_values.get(prop["SourceKeyPath"])
            else:
                values = property_values

            properties[name] = Property(name, values, randomizer)

        return properties
