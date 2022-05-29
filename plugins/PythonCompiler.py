"""
This plugin ships with sql-fusion and provides Python dataclass functionality.
If you wish to write your own plugin, the pre-provided plugins are excessively commented for your convenience.
"""
import sys

from exceptions import CompiledFileNotFoundException
from objects.SQLColumn import Column
from objects.SchemaAlias import SchemaAlias
from objects.SchemaMap import SchemaMap
from plugin_api.CompilerAPI import FileManagement
from plugin_api.PluginConfiguration import PluginConfiguration
from plugin_api.SQLFusionPlugin import SQLFusionPlugin, plugin_registry

"""
Stores a list of symbols, used for duplicate detection. For example, if you specify multiple addresses
that share the same structure the compiler will overwrite the 'Address' dataclass repeatedly until the
last time it's referenced.
"""
class SymbolDefinition:
    def __init__(self, name, symbols=None):
        self.name = name

        if symbols:
            self.symbols = symbols
        else:
            self.symbols = []

    def add_symbol(self, symbol_name, symbol_datatype: type):
        self.symbols.append({symbol_name: symbol_datatype})

"""
Subclass of SQLFusionPlugin, this makes the sql-fusion CLI recognize our plugin
"""

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

        # Register variables
        self.symbols = []

    # define a symbol for duplicate file detection
    def define_symbol(self, symbol_definition: SymbolDefinition):
        # check if this symbol already exists
        for symbol in self.symbols:
            if not symbol.name == symbol_definition.name:
                self.symbols.append(symbol_definition)
                self.log("Defined symbol '{0}'".format(symbol_definition.name))
            else:
                self.log_warning("Symbol '{0}' defined previously, skipping new definition".format(symbol_definition.name))
                break
        else:
            self.log("Defining first symbol '{0}'".format(symbol_definition.name))
            self.symbols.append(symbol_definition)

    # since this is a compiler only plugin, we just define compile() and sql-fusion takes care of the rest
    def compile(self, object=None, master=None):
        # if an object was passed to this function
        if object:
            # gets the object file from the master
            try:
                object_file = self.get_compiled_file(master)
            except CompiledFileNotFoundException as e:
                self.log_warning("Compile file '{0}' not found! Creating...".format(e))
                self.add_compiled_file(FileManagement(plugin_registry, master, extension="py"))
                object_file = self.get_compiled_file(master)
                object_file.add_line("from dataclasses import dataclass")
                object_file.add_new_line(count=2)
                object_file.add_line("@dataclass")
                object_file.add_line("class {0}:".format(master))

            # if passed object was a Column
            if type(object) == Column:
                if master:
                    self.log("Found Column '{0}' from {1}.".format(object.name, master))
                    object_file.add_line("{0}: {1}".format(object.name, object.datatype.__name__), indent=1)

            # if passed object was a SchemaAlias
            elif type(object) == SchemaAlias:
                if master:
                    self.log("Found SchemaAlias '{0}:{1}' from {2}.".format(object.database_name, object.pretty_name, master))
                    object_file.add_line("{0}: {1}".format(object.pretty_name, object.datatype.__name__), indent=1)

            # if passed object was a SchemaMap
            elif type(object) == SchemaMap:
                symbol_definition = SymbolDefinition(object.group_name.lower())
                symbol_definition.add_symbol(object.group_name.lower(), SchemaMap)
                self.define_symbol(symbol_definition)

                # add class import
                object_file.add_top_line("from {0} import {0}".format(object.group_name))

                # add class parameter
                object_file.add_line("{0}: {1}".format(object.group_name.lower(), object.group_name), indent=1)

                # recursively call compile()
                self.log("Found SchemaMap '{0}' from '{1}', entering recursively.".format(object.group_name, master))
                for child in object.columns:
                    self.compile(child, master=object.group_name)

            # if object type is unknown, warn user (possibly run a git pull?)
            else:
                self.log_critical("Type '{0}' appears to be valid Python type, but I don't have a compiler method for it!".format(type(object)))

            object_file.save_file()

        # if an object wasn't passed (assuming the Compiler plugin is calling this function)
        else:
            self.log("Compiling '{0}'".format(plugin_registry.project_name))

            # if there was a table specified in the RootSchemaMap
            if self.get_root_schema_map().table:
                self.log("RootSchemaMap specified '{0}' as it's '..FROM..' table".format(self.get_root_schema_map().table))

            # create the top most level dataclass
            self.add_compiled_file(FileManagement(plugin_registry, self.get_root_schema_map().root_name, extension="py"))

            # import dataclasses.dataclass
            root_file = self.get_compiled_file(self.get_root_schema_map().root_name)
            root_file.add_line("from dataclasses import dataclass")
            root_file.add_new_line(count=2)
            root_file.add_line("@dataclass")
            root_file.add_line("class {0}:".format(self.get_root_schema_map().root_name))

            # iterate over the RootSchemaMap, call compile but pass the object as well (so we can reference the file)
            for object in self.get_root_schema_map().columns:
                self.compile(object, self.get_root_schema_map().root_name)