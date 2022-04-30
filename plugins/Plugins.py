"""
This plugin ships with sql-fusion and provides Python dataclass functionality.
If you wish to write your own plugin, the pre-provided plugins are excessively commented for your convenience.
"""
from prettytable import PrettyTable

from plugin_api.PluginConfiguration import PluginConfiguration
from plugin_api.SQLFusionPlugin import SQLFusionPlugin, plugin_registry


# Subclass of SQLFusionPlugin, this makes the sql-fusion CLI recognize our plugin
class Plugin(SQLFusionPlugin):

    # Overwrite init dunder function (we must take plugin_registry as an arg!)
    def __init__(self):
        # set our plugin configuration
        self.set_plugin_configuration(PluginConfiguration(plugin_name="Plugins",
                                                          plugin_version="0.1.0",
                                                          plugin_short_description="Displays all loaded plugins",
                                                          author="hlafaille"))

        # we can now call super to register ourselves with the plugin registry
        super(Plugin, self).__init__()

        # register some commands
        self.register_command("plugins", self.show_plugins, "Displays all loaded plugins")

    def show_plugins(self, args):
        # show a table (thanks prettytable) of all plugins
        plugin_table = PrettyTable()
        plugin_table.field_names = ["Name", "Version", "Author", "Description"]

        for plugin in plugin_registry.get_plugins():
            plugin_table.add_row([plugin.plugin_configuration.plugin_name,
                                  plugin.plugin_configuration.plugin_version,
                                  plugin.plugin_configuration.author,
                                  plugin.plugin_configuration.plugin_short_description])
        self.log_no_prefix(plugin_table)