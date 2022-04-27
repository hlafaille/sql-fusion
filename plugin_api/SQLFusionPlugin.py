"""
A class designed solely to be subclassed. Will contain the basic layout for your plugin.
---
An SQLFusionPlugin can be many things, it could be a Factory for a file format not included,
it could be a CLI extension, it could be a lot of things. The plugin API is always growing!
---
The API works as follows:
- on CLI initialization, all plugins are loaded, tested, etc.
- plugins are event driven
"""
from plugin_api.PluginConfiguration import PluginConfiguration
from plugin_api.PluginRegistry import PluginRegistry


class SQLFusionPlugin:
    plugin_configuration = PluginConfiguration()

    def __init__(self, plugin_registry: PluginRegistry):
        # register ourselves with the plugin registry. will be used as primary communication between CLI and plugins
        plugin_registry.register_plugin(self)

    # used for loading into the plugin registry, finding out which classes are plugins and which arent
    @classmethod
    def get_subclass_name(cls):
        return cls.__name__
