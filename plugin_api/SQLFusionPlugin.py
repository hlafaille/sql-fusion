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
        self.plugin_registry = plugin_registry
