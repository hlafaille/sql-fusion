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
        self.set_plugin_configuration(PluginConfiguration(plugin_name="CLI-Help",
                                                          plugin_version="0.1.0",
                                                          plugin_short_description="Simply displays a help table",
                                                          author="hlafaille"))

        # we can now call super to register ourselves with the plugin registry
        super(Plugin, self).__init__()

        # register some commands
        self.register_command("help", self.show_help, "Gives the user some help... cause lord knows they're gonna need it.")

    def show_help(self):
        # show a table (thanks prettytable) of all commands
        command_table = PrettyTable()
        command_table.field_names = ["Command", "Plugin", "Description"]

        for command in plugin_registry.get_commands():
            command_table.add_row(
                [command.command, command.plugin.plugin_configuration.plugin_name, command.description])

        print(command_table)