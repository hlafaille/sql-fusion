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
        self.set_plugin_configuration(PluginConfiguration(plugin_name="Compiler",
                                                          plugin_version="0.1.0",
                                                          plugin_short_description="Compiles Schema Maps to various output files.",
                                                          author="hlafaille"))

        # we can now call super to register ourselves with the plugin registry
        super(Plugin, self).__init__()

        # register command (we can't just call SQLFusionPlugin's call_compile() function because it doesn't take any args)
        self.register_command("compile", self.bootstrap_compilation, "Compiles a given Root Schema Map to build files.")

    # begin bootstrapping the compilation process
    def bootstrap_compilation(self, args):
        if self.get_root_schema_map():
            self.call_compilation()
        else:
            self.log_critical("No project is selected!")