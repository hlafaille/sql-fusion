"""
This file provides a handy API for exporting your RootSchemaMap to a corresponding file
"""


import os.path
from plugin_api.SQLFusionPlugin import plugin_registry


class FileManagement:
    def __init__(self, shebang=None, extension=""):
        self.shebang = shebang
        self.extension = extension

    def save_file(self):
        # try to make build directory
        try:
            os.mkdir("build")
        except FileExistsError:
            pass

        # try to make project directory
        try:
            os.mkdir(os.path.join("build", plugin_registry.project_name))
        except FileExistsError:
            pass

        with open(os.path.join("build", plugin_registry.project_name, "{0}.{1}".format(plugin_registry.project_name, self.extension)), "w") as file:
            file.write(" ")
