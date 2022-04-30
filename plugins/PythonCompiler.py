"""
This plugin ships with sql-fusion and provides Python dataclass functionality.
If you wish to write your own plugin, the pre-provided plugins are excessively commented for your convenience.
"""
from objects.SQLColumn import Column
from objects.SchemaAlias import SchemaAlias
from objects.SchemaMap import SchemaMap
from plugin_api.PluginConfiguration import PluginConfiguration
from plugin_api.SQLFusionPlugin import SQLFusionPlugin, plugin_registry


# Subclass of SQLFusionPlugin, this makes the sql-fusion CLI recognize our plugin
class Plugin(SQLFusionPlugin):

    # Overwrite init dunder function (we must take plugin_registry as an arg!)
    def __init__(self):
        # set our plugin configuration
        self.set_plugin_configuration(PluginConfiguration(plugin_name="Compiler-Python",
                                                          plugin_version="0.1.0",
                                                          plugin_short_description="Compiles Root Schema Maps to Python dataclasses",
                                                          author="hlafaille"))

        # we can now call super to register ourselves with the plugin registry
        super(Plugin, self).__init__()

        # setup our compiled file configuration
        self.setup_compiled_file(extension="py")

    # since this is a compiler only plugin, we just define compile() and sql-fusion takes care of the rest
    def compile(self, object=None, master=None):
        # if an object was passed to this function
        if object:

            # if passed object was a Column
            if type(object) == Column:
                if master:
                    self.log("Found Column '{0}' from {1}.".format(object.name, master))
                else:
                    self.log("Found Column '{0}'.".format(object.name))

            # if passed object was a SchemaAlias
            elif type(object) == SchemaAlias:
                if master:
                    self.log("Found SchemaAlias '{0}:{1}' from {2}.".format(object.database_name, object.pretty_name, master))
                else:
                    self.log("Found Column '{0}'.".format(object.name))

            # if passed object was a SchemaMap
            elif type(object) == SchemaMap:
                self.log("Found SchemaMap '{0}' from '{1}', entering recursively.".format(object.group_name, master))
                for child in object.columns:
                    self.compile(child, object.group_name)

            # if object type is unknown, warn user (possibly run a git pull?)
            else:
                self.log_warning("Unknown type {0}".format(type(object)))

        # if an object wasn't passed (assuming the Compiler plugin is calling this function)
        else:
            self.log("Compiling '{0}'".format(plugin_registry.project_name))
            for object in self.get_root_schema_map().columns:
                self.compile(object, self.get_root_schema_map().root_name)