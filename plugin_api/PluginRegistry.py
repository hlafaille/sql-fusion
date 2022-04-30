"""
This class can be instantiated by a plugin to create a command for the sql-fusion CLI
"""
import importlib
import os

from exceptions import ProjectNotFoundException

"""
A simple data object, represent an sql-fusion command.
"""

class SQLFusionCommand:
    def __init__(self, command, plugin, function, description):
        self.command = command
        self.plugin = plugin
        self.function = function
        self.description = description


"""
This class is instantiated once the sql-fusion CLI is run, and is required to be an argument on all plugins.
APIRegistry will facilitate your main communication path between the sql-fusion CLI/compiler and your plugin.
It will provide you with many functions to communicate to the CLI.
"""


class PluginRegistry:
    total_plugins = []
    commands = []
    projects = []

    # called on plugin instantiation, this registry maintains a list of all active plugins and provides the main api
    def __init__(self):
        self.current_project = None
        self.project_name = ""

    def register_plugin(self, plugin):
        self.total_plugins.append(plugin)

    def load_plugins(self):
        # get a list of plugins from the plugin directory
        plugin_directory = next(os.walk('plugins/'))[2]

        # try and remove __pycache__
        try:
            plugin_directory.remove("__pycache__")
        except ValueError:
            pass

        # iterate over the plugins and load them into the PluginRegistry
        for plugin in plugin_directory:
            if not plugin == "__init__.py":
                plugin_module = importlib.import_module("plugins.{0}".format(plugin.replace(".py", "")), ".")
                temp_plugin = plugin_module.Plugin()

    def load_project(self, project):
        self.projects.append(project)

    def clear_projects(self):
        self.projects = []
        try:
            self.set_current_project(None, "")
        except ProjectNotFoundException:
            pass

    # iterates over all plugins, calls their compile function
    def begin_compilation(self):
        for plugin in self.total_plugins:
            # ignore if this plugin isn't a compiler
            try:
                plugin.compile()
            except AttributeError:
                pass

    # registers a command
    def register_command(self, command: SQLFusionCommand):
        self.commands.append(command)

    # returns the total plugins registered
    def get_plugins(self):
        return self.total_plugins

    # sets the current project
    def set_current_project(self, project, project_name):
        self.current_project = project
        self.project_name = project_name

    # returns all projects
    def get_projects(self):
        return self.projects

    # returns all commands
    def get_commands(self):
        return self.commands

