import os
import shutil

from factories.DataclassFactory import DataclassFactory

try:
    from src.schema_map import schema
except ModuleNotFoundError:
    print("[!] src not found, creating.")
    os.mkdir("src")
    shutil.copy(os.path.join("template", "schema_map_template.py"), os.path.join("src", "schema_map.py"))


class CommandInterpreter:
    def __init__(self):
        self.user_input = None

        print("███████  ██████  ██            ███████ ██    ██ ███████ ██  ██████  ███    ██      ██████ ██      ██ ")
        print("██      ██    ██ ██            ██      ██    ██ ██      ██ ██    ██ ████   ██     ██      ██      ██ ")
        print("███████ ██    ██ ██      █████ █████   ██    ██ ███████ ██ ██    ██ ██ ██  ██     ██      ██      ██ ")
        print("     ██ ██ ▄▄ ██ ██            ██      ██    ██      ██ ██ ██    ██ ██  ██ ██     ██      ██      ██ ")
        print("███████  ██████  ███████       ██       ██████  ███████ ██  ██████  ██   ████      ██████ ███████ ██ ")
        print("-----------------------------------------------------------------------------------------------------")
        print("type 'help' for commands, exit to exit.")
        self.get_input()

    # get the user input
    def get_input(self, prompt=None):
        if prompt:
            self.user_input = input("{0}> ".format(prompt))
        else:
            self.user_input = input("> ")

        self.interpret_input()

    # interprets the user input
    def interpret_input(self):
        #  help screen
        if self.user_input == "help":
            print("new     - copies 'src/template/' to 'src', creating a new sql-fusion project.")
            print("compile - compiles the project in 'src', outputting it in 'build'.")

        # compilation procedure
        elif self.user_input == "compile":
            print("are you sure you wish to compile? this will erase anything in the 'build' directory!")
            if self.get_confirmation():
                dataclass = DataclassFactory(schema)

        # new procedure
        elif self.user_input == "new":
            print("are you sure you wish to create a new project? this will erase anything in the 'build' and 'src' directories!")
            if self.get_confirmation():
                # remove build and src directories
                try:
                    shutil.rmtree("build/")
                    shutil.rmtree("src/")
                except FileNotFoundError:
                    pass

                # create build and src directories
                try:
                    os.mkdir("src")
                    os.mkdir("build/")
                except FileExistsError:
                    os.mkdir("build/")

                # copy the template schema map to src
                shutil.copy(os.path.join("template", "schema_map_template.py"),
                            os.path.join("src", "schema_map.py"))

                print("schema map created in 'src', check it out!")
        else:
            print("unknown command, type help for a list of commands.")
        self.get_input()

    # quick function to get the user confirmation
    def get_confirmation(self):
        confirmation = input("y/n> ")

        if "y" in confirmation.lower():
            return True
        else:
            return False



