"""
A class designed solely to be subclassed. Will contain the basic layout for your plugin.
---
An SQLFusionPlugin can be many things, it could be a Factory for a file format not included,
it could be a CLI extension, it could be a lot of things. The plugin API is always growing!
"""


import json
import os.path
from json import JSONDecodeError

from colorama import Fore

from plugin_api.CompilerAPI import FileManagement
from plugin_api.PluginConfiguration import PluginConfiguration
from plugin_api.PluginRegistry import PluginRegistry, SQLFusionCommand

plugin_registry = PluginRegistry()


class SQLFusionPlugin:
    plugin_configuration = PluginConfiguration()

    def __init__(self):
        plugin_registry.register_plugin(plugin=self)
        self.config_file = {}
        self.compiled_file = None

        # execution
        self.open_configuration()

    # setup plugin compiled file
    def setup_compiled_file(self, shebang=None, extension=None):
        self.compiled_file = FileManagement(shebang=shebang, extension=extension)

    # returns the current root schema map
    def get_root_schema_map(self):
        return plugin_registry.current_project

    # opens the configuration file, reads it
    def open_configuration(self):
        # if the file exists, read it. if not create it.
        try:
            with open(os.path.join("plugins", "config", "{0}.json").format(self.plugin_configuration.plugin_name),
                      "r") as f:
                self.config_file = json.loads(f.read())
        except (FileNotFoundError, JSONDecodeError):
            # try to make the config folder
            try:
                os.mkdir(os.path.join("plugins", "config"))
            except FileExistsError:
                pass

            # write the blank config file
            with open(os.path.join("plugins", "config", "{0}.json").format(self.plugin_configuration.plugin_name),
                      "w") as f:
                f.write(json.dumps(self.config_file, indent=4))
            self.log_critical("config file not found")

    # sets this plugins configuration
    def set_plugin_configuration(self, configuration: PluginConfiguration):
        self.plugin_configuration = configuration

    # registers a command with plugin registry
    def register_command(self, command, function, description):
        plugin_registry.register_command(SQLFusionCommand(command=command,
                                                          plugin=self,
                                                          function=function,
                                                          description=description))

    # calls plugin registry to begin all plugin compilation
    def call_compilation(self):
        plugin_registry.begin_compilation()

    def log_no_prefix(self, message):
        print(Fore.LIGHTWHITE_EX + str(message) + Fore.RESET)

    def log(self, message):
        print_string = Fore.LIGHTMAGENTA_EX + "[{0}]".format(
            self.plugin_configuration.plugin_name) + Fore.LIGHTWHITE_EX + "[.] {0}".format(message) + Fore.RESET
        print(print_string)

    def log_success(self, message):
        print_string = Fore.LIGHTMAGENTA_EX + "[{0}]".format(
            self.plugin_configuration.plugin_name) + Fore.LIGHTGREEN_EX + "[*] " + Fore.LIGHTWHITE_EX + "{0}".format(
            message) + Fore.RESET
        print(print_string)

    def log_warning(self, message):
        print_string = Fore.LIGHTMAGENTA_EX + "[{0}]".format(
            self.plugin_configuration.plugin_name) + Fore.LIGHTYELLOW_EX + "[-] " + Fore.LIGHTWHITE_EX + "{0}".format(
            message) + Fore.RESET
        print(print_string)

    def log_question(self, message):
        print_string = Fore.LIGHTMAGENTA_EX + "[{0}]".format(
            self.plugin_configuration.plugin_name) + Fore.LIGHTCYAN_EX + "[?] " + Fore.LIGHTWHITE_EX + "{0}".format(
            message) + Fore.RESET
        print(print_string)

    def log_critical(self, message):
        print_string = Fore.LIGHTMAGENTA_EX + "[{0}]".format(
            self.plugin_configuration.plugin_name) + Fore.LIGHTRED_EX + "[!] " + Fore.LIGHTWHITE_EX + "{0}".format(
            message) + Fore.RESET
        print(print_string)

    def get_user_input(self, prefix=None):
        if prefix:
            return input(Fore.LIGHTWHITE_EX + "{0}".format(prefix) + Fore.RESET + "> ")
        else:
            return input("> ")
