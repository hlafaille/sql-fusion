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
from plugin_api.PluginRegistry import PluginRegistry, SQLFusionCommand

plugin_registry = PluginRegistry()


class SQLFusionPlugin:
    plugin_configuration = PluginConfiguration()

    def __init__(self):
        plugin_registry.register_plugin(plugin=self)

    def set_plugin_configuration(self, configuration: PluginConfiguration):
        self.plugin_configuration = configuration

    def register_command(self, command, function, description):
        plugin_registry.register_command(SQLFusionCommand(command=command,
                                                          plugin=self,
                                                          function=function,
                                                          description=description))

    def log_common(self, message):
        print(f"[.] {message}")

    def log_success(self, message):
        print(f"[*] {message}")

    def log_question(self, message):
        print(f"[?] {message}")

    def log_critical(self, message):
        print(f"[!] {message}")