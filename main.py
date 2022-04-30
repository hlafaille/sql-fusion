from colorama import init

from cli.NewCommandInterpreter import CommandInterpreter
from plugin_api.SQLFusionPlugin import plugin_registry

if __name__ == "__main__":
    init()
    # load all plugins
    plugin_registry.load_plugins()

    # call command interpreter and bootstrap ourselves up
    command_interpreter = CommandInterpreter()
