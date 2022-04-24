import importlib
import os
import shutil
import sys

from factories.DataclassFactory import DataclassFactory
from factories.SQLFactory import SQLFactory


class CommandInterpreter:
    def __init__(self):
        self.user_input = None
        self.current_project = None
        self.current_project_name = ""

        self.header()
        self.get_input()

    def header(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("███████  ██████  ██            ███████ ██    ██ ███████ ██  ██████  ███    ██      ██████ ██      ██ ")
        print("██      ██    ██ ██            ██      ██    ██ ██      ██ ██    ██ ████   ██     ██      ██      ██ ")
        print("███████ ██    ██ ██      █████ █████   ██    ██ ███████ ██ ██    ██ ██ ██  ██     ██      ██      ██ ")
        print("     ██ ██ ▄▄ ██ ██            ██      ██    ██      ██ ██ ██    ██ ██  ██ ██     ██      ██      ██ ")
        print("███████  ██████  ███████       ██       ██████  ███████ ██  ██████  ██   ████      ██████ ███████ ██ ")

        if self.current_project:
            print("current project: {0}".format(self.current_project_name))

        print("-----------------------------------------------------------------------------------------------------")
        print("type 'help' for commands, exit to exit.")

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
            print("(n)ew     - copies 'src/template/' to 'src', creating a new sql-fusion project.")
            print("(c)ompile - compiles the project in 'src', outputting it in 'build'.")
            print("(o)pen    - lists the projects in 'src', if there's only one it will be automatically opened.")
            print("(e)xit    - exits the cli.")

        # exit procedure
        elif self.user_input == "exit" or self.user_input == "e":
            sys.exit(0)

        # compilation procedure
        elif self.user_input == "compile" or self.user_input == "c":
            if self.current_project:
                print("are you sure you wish to compile? this will erase everything in the projects build directory!")
                if self.get_confirmation():
                    dataclass = DataclassFactory(self.current_project.schema, self.current_project_name)
                    sql_factory = SQLFactory(self.current_project.schema, self.current_project_name)
            else:
                print("no project selected")

        # new procedure
        elif self.user_input == "new" or self.user_input == "n":
            print("are you sure you wish to create a new project? this will erase anything in the projects 'build' and 'src' directories!")
            if self.get_confirmation():
                print("what is this projects name?")
                project_name = input("> ").replace("-", "_").replace(" ", "_")

                if not project_name == "":
                    dir_list = ["src", "build"]

                    # create build and src directories
                    for directory in dir_list:
                        try:
                            os.mkdir(directory)
                        except FileExistsError:
                            pass

                    # create build/project and src/project directories
                    for directory in dir_list:
                        try:
                            os.mkdir(os.path.join(directory, project_name))
                        except FileExistsError:
                            pass

                    # copy the template schema map to src
                    shutil.copy(os.path.join("template", "schema_map_template.py"),
                                os.path.join("src", project_name, "schema_map.py"))

                    print("schema map created in 'src/{0}', check it out!".format(project_name))

                    # import the module, use it for project management
                    self.current_project = importlib.import_module(".schema_map", package="src.{0}".format(project_name))
                    self.current_project_name = project_name

                    self.header()

        elif self.user_input == "open" or self.user_input == "o":
            directories = next(os.walk('src/'))[1]
            directories.remove("__pycache__")

            # if there's only one project, auto open it.
            if not len(directories) == 1:
                print("select project to open")
                for x in range(len(directories)):
                    print("{0}) {1}".format(x, directories[x]))

                project = int(input("{0}-{1}> ".format(0, len(directories) - 1)))

                self.current_project = importlib.import_module(".schema_map", package="src.{0}".format(directories[project]))
                self.current_project_name = directories[project]
            else:
                for x in range(len(directories)):
                    self.current_project = importlib.import_module(".schema_map", package="src.{0}".format(directories[x]))
                    self.current_project_name = directories[x]

            self.header()

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



