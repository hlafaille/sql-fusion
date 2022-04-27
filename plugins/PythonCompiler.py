"""
This plugin ships with sql-fusion and provides Python dataclass functionality.
If you wish to write your own plugin, the pre-provided plugins are excessively commented for your convenience.
"""
from plugin_api.SQLFusionPlugin import SQLFusionPlugin


# Subclass of SQLFusionPlugin, this makes the sql-fusion CLI recognize our plugin
class PythonCompiler(SQLFusionPlugin):

    # Overwrite init special function (we must take plugin_registry as an arg!)
    def __init__(self, plugin_registry):
        super(PythonCompiler, self).__init__(plugin_registry)
        print("ass" + self.get_subclass_name())