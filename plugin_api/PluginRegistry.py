"""
This class is instantiated once the sql-fusion CLI is run, and is required to be an argument on all plugins.
APIRegistry will facilitate your main communication path between the sql-fusion CLI/compiler and your plugin.
It will provide you with many functions to communicate to the CLI.
"""


class PluginRegistry:
    def __int__(self):
        self.registered_plugins = []

    # called on plugin instantiation, this registry maintains a list of all active plugins and provides the main api
    def register_plugin(self, plugin):
        self.registered_plugins.append(plugin)


class MessageStatuses:
    COMMON = "."
    SUCCESS = "*"
    ERROR = "!"
    QUESTION = "?"
