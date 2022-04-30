"""
This plugin ships with sql-fusion and provides Python dataclass functionality.
If you wish to write your own plugin, the pre-provided plugins are excessively commented for your convenience.
"""
import importlib
import os
import shutil

from prettytable import PrettyTable

from plugin_api.PluginConfiguration import PluginConfiguration
from plugin_api.SQLFusionPlugin import SQLFusionPlugin, plugin_registry


# Subclass of SQLFusionPlugin, this makes the sql-fusion CLI recognize our plugin
class Plugin(SQLFusionPlugin):

    # Overwrite init dunder function (we must take plugin_registry as an arg!)
    def __init__(self):
        # set our plugin configuration
        self.set_plugin_configuration(PluginConfiguration(plugin_name="Projects",
                                                          plugin_version="0.1.0",
                                                          plugin_short_description="Project management",
                                                          author="hlafaille"))

        # we can now call super to register ourselves with the plugin registry
        super(Plugin, self).__init__()

        # register some commands
        self.register_command("projects", self.projects, "Simply displays a help table")

        # notify PluginRegistry of all current projects
        self.discover_projects()

    def projects(self, args):
        # if no args were passed,
        if len(args) == 0:
            # show a table (thanks prettytable) of all commands
            command_table = PrettyTable()
            command_table.field_names = ["Command", "Description"]
            command_table.add_row(["projects list", "Lists all projects"])
            command_table.add_row(["projects create", "Creates a project"])
            command_table.add_row(["projects open", "Opens a project"])

            self.log_no_prefix(command_table)
        else:
            # begin parsing args
            if args[0] == "list":
                self.projects_list()

            elif args[0] == "create":
                self.project_create()

            elif args[0] == "open":
                self.project_open()

    def discover_projects(self):
        # reset projects
        plugin_registry.clear_projects()

        # discover projects in src folder
        try:
            projects = next(os.walk('src/'))[1]
        except StopIteration:
            # warn the user that the src folder is missing (shouldn't be unless purposefully deleted)
            self.log_warning("'src/' doesn't exist, creating it! Please restart sql-fusion.")
            os.mkdir("src")
            f = open("src/__init__.py", "w")
            f.write("")
            f.close()

        # attempt to remove __pycache__ from src1 folder (if it doesn't exist, ignore it)
        try:
            projects.remove("__pycache__")
        except ValueError:
            pass

        # if there's no projects found, warn user
        if len(projects) == 0:
            self.log_warning("No sql-fusion projects were found in 'src/', run 'projects create' to create one!")
        else:
            for project in projects:
                plugin_registry.load_project(project)

    def projects_list(self):
        self.discover_projects()
        projects_table = PrettyTable()
        projects_table.field_names = ["#", "Name"]
        for number, project in enumerate(plugin_registry.get_projects()):
            projects_table.add_row([number, project])

        self.log_no_prefix(projects_table)
        return len(plugin_registry.get_projects())

    def project_create(self):
        self.log_question("What is this projects name?")
        project_name = self.get_user_input("project name")

        # do some post-processing
        project_name = project_name.replace(" ", "-")

        # create the project directory and copy the template schema map
        try:
            os.mkdir(os.path.join("src", project_name))

            shutil.copy(os.path.join("template", "schema_map_template.py"),
                        os.path.join("src", project_name, "schema_map.py"))
        except FileExistsError:
            # if the project exists, offer to overwrite it
            self.log_question("'{0}' already exists, should I overwrite it?".format(project_name))
            confirmation = self.get_user_input("y/n")

            if confirmation == "y":
                shutil.rmtree(os.path.join("src", project_name))
                os.mkdir(os.path.join("src", project_name))

                shutil.copy(os.path.join("template", "schema_map_template.py"),
                            os.path.join("src", project_name, "schema_map.py"))
            else:
                pass

        self.log_success("Project '{0}' created!".format(project_name))

    def project_open(self):
        # get the total count of all projects in src
        project_count = self.projects_list()

        # variable used in while loop below, will force the user to select an actual project in range (0-project_count - 1)
        project_go_ahead = False

        # if we've got more than one project, ask the user which one
        if project_count > 1:
            while not project_go_ahead:
                self.log_question("What project do you wish to open?")
                open_project = self.get_user_input("0-{0}".format(project_count - 1))

                try:
                    if int(open_project) not in range(project_count):
                        self.log_warning("Project selection out of range (0-{0}".format(project_count))
                    else:
                        plugin_registry.set_current_project(importlib.import_module(".schema_map",
                                                                                    package="src.{0}".format(
                                                                                        plugin_registry.get_projects()[
                                                                                            open_project])).schema,
                                                            plugin_registry.get_projects()[open_project])

                        plugin_registry.set_current_project(plugin_registry.get_projects()[int(open_project)])
                        project_go_ahead = True
                        self.log_success(
                            "Project '{0}' is opened.".format(plugin_registry.get_projects()[int(open_project)]))
                except ValueError:
                    self.log_warning("Project selection must be an integer.")
        else:
            self.log(
                "'{0}' is the only project, so by default it will be opened.".format(plugin_registry.get_projects()[0]))
            plugin_registry.set_current_project(importlib.import_module(".schema_map",
                                                                        package="src.{0}".format(
                                                                            plugin_registry.get_projects()[
                                                                                0])).schema, plugin_registry.get_projects()[0])
