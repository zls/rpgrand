from .loaders import Loader
from .properties import Property


class ConfigMap(object):
    '''Create object from config.

    {
        "Type": "config_map",
        "Metadata": {
            "Version": "1"
            "CategoryType": "npc"
        },
        "Config": {
            "Defaults": {
                "Randomizer": "from_list",
                "Type": "list"
                "Source": "./foo/bar.yml",
                "SourceLoader": "file",
                "SourceType": "yml",
                "UseNameForSourceKeyPath": true
            },
            "Properties": [
                {
                    "Name": "Name",
                    "Type": "dict",
                    "Randomizer": "weighted",
                    "Quantity": "1..4",
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
    def __init__(self, config_path, source_type="yml", source_loader="file"):
        loader = Loader.get_loader(source_type=source_type, source_loader=source_loader)
        self.config = loader.load(config_path)
        _validate_config(self.config)

        self.properties = _create_properties_map(self.config)


    def __repr__(self):
        return "{}".format(self.config)

    def __str__(self):
        return self.config


def _create_properties_map(config):
    properties = {}
    return _load_properties_from_sources(
        config["Config"]["Properties"],
        _load_defaults(config))


def _validate_config(config):
    if config.get('Type') != 'config_map':
        raise CategoryInvalidConfig("Unknown `Type` {}".format(config["Type"]))
    elif not config.get('Type'):
        raise CategoryInvalidConfig("No `Type` section")

    if not config.get("Config"):
        raise CategoryInvalidConfig("No `Config` section")

    if not config["Config"].get("Properties"):
        raise CategoryInvalidConfig("No `Config.Properties` section")

    defaults = _load_defaults(config)

    for prop in config['Config']['Properties']:
        _validate_property(prop, defaults)
        for source in _get_sources(prop, defaults):
            _validate_sources(source, prop, defaults)


def _validate_property(prop, defaults):
    if prop.get("Source") and prop.get("Sources"):
        raise CategoryInvalidConfig("`Source` and `Sources` are mutually exclusive")

    if not prop.get("Name"):
        raise CategoryInvalidConfigProperty("No `Name` key in `Config.Properties` item")

    if not defaults["source"] and ( not prop.get("Source") and not prop.get("Sources") ):
        raise CategoryInvalidConfigProperty("No `Source` or `Sources` key in `Config.Properties` item and default not set")


def _validate_sources(source, prop, defaults):
    _s, _sl, _st, _rnd = _get_source_properties(source, prop)

    if not _sl and not defaults["source_loader"]:
        raise CategoryInvalidConfigProperty("No `SourceLoader` key in `Config.Properties` item and default not set")

    if not _st and not defaults["source_type"]:
        raise CategoryInvalidConfigProperty("No `SourceType` key in `Config.Properties` item and default not set")

    if not _rnd and not defaults["randomizer"]:
        raise CategoryInvalidConfigProperty("No `Randomizer` key in `Config.Properties` item and default not set")


def _load_defaults(config):
    '''Set config defaults.'''
    config_defaults = config["Config"].get("Defaults", {})
    defaults = {}
    defaults["type"] = config_defaults.get("Type", "list")
    defaults["source"] = config_defaults.get("Source", None)
    defaults["source_loader"] = config_defaults.get("SourceLoader", None)
    defaults["source_type"] = config_defaults.get("SourceType", None)
    defaults["randomizer"] = config_defaults.get("Randomizer", None)
    defaults["use_name_skp"] = config_defaults.get("UseNameForSourceKeyPath", None)
    return defaults


def _get_ptype(t):
    if t == "list":
        return list
    elif t == "dict":
        return dict
    return None


def _update_values(v, data, ptype=None):
    if ptype == dict:
        v.update(data)
    elif ptype == list:
        v += data


def _get_sources(prop, defaults):
    if prop.get("Source"):
        sources = [ prop["Source"] ]
    elif prop.get("Sources"):
        sources = prop["Sources"]
    else:
        sources = [ defaults["source"] ]
    return sources


def _get_source_properties(source, prop):
    if type(source) == dict:
        s = source.get("Source")
        sl = source.get("SourceLoader")
        st = source.get("SourceType")
        rnd = source.get("Randomizer")
    else:
        s = source
        sl = prop.get("SourceLoader")
        st = prop.get("SourceType")
        rnd = prop.get("Randomizer")
    return s, sl, st, rnd


def _load_properties_from_sources(props, defaults):
    properties = {}
    for prop in props:
        name = prop["Name"]
        sources = _get_sources(prop, defaults)
        quantity = prop.get("Quantity", "1")
        ptype = _get_ptype(prop["Type"]) if prop.get("Type") else _get_ptype(defaults["type"])
        values = ptype()
        for source in sources:
            _s, _sl, _st, _rnd = _get_source_properties(source, prop)

            source_loader = _sl if _sl else defaults["source_loader"]
            source_type = _st if _st else defaults["source_type"]
            randomizer = _rnd if _rnd else defaults["randomizer"]
            _loader = Loader.get_loader(source_type=source_type, source_loader=source_loader)
            property_values = _loader.load(_s)
            if prop.get("SourceKeyPath") or defaults["use_name_skp"]:
                data = property_values.get(prop["SourceKeyPath"]) if property_values.get(prop.get("SourceKeyPath")) else property_values.get(name)
            else:
                data = property_values
            _update_values(values, data, ptype=ptype)

        properties[name] = Property(name, values, randomizer, quantity=quantity)
    return properties
