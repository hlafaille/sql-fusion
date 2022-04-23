"""
This object converts an interpreted RootSchemaMap into a Python Dataclass file.
"""
import json
import os
import shutil
import string
import traceback

from exceptions import DuplicateDataclassException
from objects.SchemaInterpreter import SchemaInterpreter
from objects.SchemaMap import RootSchemaMap


class DataclassFactory:
    def __init__(self, root_schema_map: RootSchemaMap, project_name):
        # variables
        self.dataclasses = {}
        self.root_schema_map = ""

        # get interpreted schema map
        self.interpreted_schema = SchemaInterpreter(root_schema_map)

        # iterate over the interpreted root schema map, establish what we're working with
        for x in self.interpreted_schema.get_interpreted():
            print("[.] root schema map is {0}.".format(x))
            self.root_schema_map = x

            # iterate over the named_schema_maps, those're going to be our data classes.
            for col in self.interpreted_schema.get_interpreted()[x]:
                try:
                    if col["sql_fusion_type"] == "named_schema_map":
                        # establish some per-dataclass variables (ex: name)
                        dataclass_name = col["name"]

                        print("---------------------")
                        print("[.] found nested named schema map in root, beginning compilation of {0}".format(
                            dataclass_name))

                        # append the dataclasses to the dictionary
                        compiled_text = self.dataclass_compile(col["data"], col["name"])

                        # check if the compiled text is in the dictionary already
                        try:
                            for dataclass in self.dataclasses:
                                if compiled_text in self.dataclasses[dataclass]:
                                    print("[!] came across duplicate {0}, ignoring dataclass compilation (we can still use this for JSON or SQL later.".format(col["name"]))
                                    raise DuplicateDataclassException
                        except DuplicateDataclassException:
                            pass
                        else:
                            self.dataclasses[col["name"]] = compiled_text

                except KeyError:
                    pass
        print("---------------------")
        print("[*] compilation of sub schema maps, complete.")
        print("[.] cleaning build directory...")

        # try to clean the build folder,
        try:
            shutil.rmtree("build/{0}".format(project_name))
            os.mkdir("build/{0}".format(project_name))
        except FileNotFoundError:
            os.mkdir("build/{0}".format(project_name))

        # iterate over the compiled dataclasses, export them
        for compiled_source in self.dataclasses:
            print("[.] building {0}...".format(compiled_source))

            with open(os.path.join("build", project_name, "{0}.py".format(compiled_source)), "w") as file:
                file.write(self.dataclasses[compiled_source])

        print("[.] sub dataclasses built, now compiling root schema map.")
        print("---------------------")
        with open(os.path.join("build", project_name, "{0}.py".format(x)), "w") as file:
            temp = self.root_dataclass_compile(self.interpreted_schema.get_interpreted(), x)
            file.write(temp)
        print("---------------------")
        print("[*] compilation complete with {0} nested dataclasses. ".format(len(self.dataclasses)))

    # Handle root dataclass compilation (this wil reference nested dataclasses we've created).
    def root_dataclass_compile(self, root_schema_map, dataclass_name):
        imports = ""
        text = "from dataclasses import dataclass\n" \
               "\n" \
               "\n" \
               "@dataclass\n" \
               "class {0}:\n".format(dataclass_name)

        # just like in SchemaInterpreter, iterate over all the objects in this schema map.
        for obj in root_schema_map[dataclass_name]:
            try:
                # if we're dealing with a column
                if obj["sql_fusion_type"] == "column":
                    temp = self.add_indent(1, "{0}: {1}".format(obj["name"], obj["datatype"]))

                    if temp not in text:
                        print("[.] found root schema map column - {0}".format(obj["name"]))
                        text += temp
                    else:
                        print("[!] duplicate root schema map column, ignoring - {0}".format(obj["name"]))

                # what about a schema map?
                elif obj["sql_fusion_type"] == "named_schema_map":
                    temp = self.add_indent(1, "{0}: {0}".format(obj["name"]))

                    if temp not in text:
                        print("[.] found named schema map - {0}".format(obj["name"]))
                        text += self.add_indent(1, "{0}: {0}".format(obj["name"]))
                        imports += "from {0} import {0}\n".format(obj["name"])
                    else:
                        print("[!] duplicate named schema map, ignoring - {0}".format(obj["name"]))

            # if it's not a schema map, it's gotta be something else...
            except KeyError:
                for database_name in obj:
                    if obj[database_name]["sql_fusion_type"] == "schema_alias":
                        temp = self.add_indent(1, "{0}: {1}".format(obj[database_name]["pretty_name"],
                                                                     obj[database_name]["datatype"]))

                        if temp not in text:
                            print("[.] found root level schema alias - pretty: {0}, ugly: {1}".format(
                                obj[database_name]["pretty_name"],
                                database_name))
                            text += self.add_indent(1, "{0}: {1}".format(obj[database_name]["pretty_name"],
                                                                         obj[database_name]["datatype"]))
                        else:
                            print("[!] duplicate root level schema alias, ignoring - pretty: {0}, ugly: {1}".format(
                                obj[database_name]["pretty_name"],
                                database_name))

        return imports + text

    # Handle dataclass compilation
    def dataclass_compile(self, schema_map, dataclass_name):
        imports = '"""\nsql-fusion compiled nested dataclass {0}\nThis class is a child class of {1}\n"""\n'.format(
            dataclass_name, self.root_schema_map)
        text = "from dataclasses import dataclass\n" \
               "\n" \
               "\n" \
               "@dataclass\n" \
               "class {0}:\n".format(str(dataclass_name))

        from_database_function = self.add_indent(1, "def from_database(self):\n")

        # just like in SchemaInterpreter, iterate over all the objects in this schema map.
        for obj in schema_map:
            # iterate over all the attributes for this object
            try:
                # if this object is a schema alias
                for attribute in obj:
                    object_type = obj[attribute]["sql_fusion_type"]
                    if object_type == "schema_alias":
                        if obj[attribute]["pretty_name"] == attribute:
                            print("[!] warning: schema alias not needed - pretty: {0}, ugly: {1}".format(
                                obj[attribute]["pretty_name"],
                                attribute))
                        print(
                            "[.]     found schema alias - pretty: {0}, ugly: {1}".format(obj[attribute]["pretty_name"],
                                                                                         attribute))
                        text += self.add_indent(1, "# Database Column: {0}".format(attribute))
                        text += self.add_indent(1, "{0}: {1}".format(obj[attribute]["pretty_name"],
                                                                     obj[attribute]["datatype"]))

            # if it's not a schema alias, it's gotta be something else...
            except TypeError:
                # maybe it's a column?
                if obj["sql_fusion_type"] == "column":
                    print("[.]     found column - {0}".format(obj["name"]))
                    text += self.add_indent(1, "{0}: {1}".format(obj["name"],
                                                                 obj["datatype"]))

                # no... it's gotta be a named_schema_map...
                else:
                    if obj["sql_fusion_type"] == "named_schema_map":
                        print(
                            "[!] found nested named schema map during another schema map compilation, pausing and compiling first. - {0}".format(
                                obj["name"]))

                        imports += "from {0} import {0}\n".format(obj["name"])
                        text += self.add_indent(1, "{0}: {0}".format(obj["name"]))
                        self.dataclasses[obj["name"]] = self.dataclass_compile(obj["data"], obj["name"])
        return imports + text

    # quick function to handle indents
    def add_indent(self, tabs, text):
        indent = ""
        for x in range(tabs * 4):
            indent += " "
        return indent + text + "\n"
