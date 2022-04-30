"""
This class handles calling all commands
"""
import traceback

from exceptions import CommandNotFoundException
from plugin_api.SQLFusionPlugin import plugin_registry


class CommandInterpreter:
    def __init__(self):
        self.user_input = None
        print("sql-fusion cli, type help for help - {0} plugins loaded".format(len(plugin_registry.get_plugins())))

        while True:
            self.user_input = input("> ").split(" ")
            self.check_command()

    def check_command(self):
        # iterate over commands in plugin registry, check if any match the provided input
        try:
            for command in range(len(plugin_registry.get_commands())):
                if plugin_registry.get_commands()[command].command == self.user_input[0]:
                    command_arguments = self.user_input.pop(0)
                    try:
                        plugin_registry.get_commands()[command].function(command_arguments)
                    except TypeError:
                        print("error: plugin '{0}' command function '{1}' does not take arguments as an input!".format(
                            plugin_registry.get_commands()[command].plugin.plugin_configuration.plugin_name,
                            plugin_registry.get_commands()[command].function.__name__
                        ))
                    break
                else:
                    # if we've iterated over all the commands and still haven't found match
                    if command == len(plugin_registry.get_commands()) - 1:
                        raise CommandNotFoundException
                    else:
                        continue

        except (CommandNotFoundException, AttributeError):
            print("command {0} was not found".format(self.user_input[0]))

