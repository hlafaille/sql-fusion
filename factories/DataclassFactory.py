"""
This object converts an interpreted RootSchemaMap into a Python Dataclass file.
"""
import json

from objects.SchemaInterpreter import SchemaInterpreter
from objects.SchemaMap import RootSchemaMap


class DataclassFactory:
    def __init__(self, root_schema_map: RootSchemaMap):
        # variables
        self.dataclasses = {}

        # get interpreted schema map
        self.interpreted_schema = SchemaInterpreter(root_schema_map)

        # iterate over the interpreted root schema map, establish what we're working with
        for x in self.interpreted_schema.get_interpreted():
            print("[-] root_schema_map is {0}".format(x))
            print("---------------------")

            # iterate over the named_schema_maps, those're going to be our data classes.
            for col in self.interpreted_schema.get_interpreted()[x]:
                if col["sql_fusion_type"] == "named_schema_map":
                    # establish some per-dataclass variables (ex: name)
                    dataclass_name = col["name"].title()

                    print("[.] found nested named_schema_map, beginning compilation of {0}".format(dataclass_name))
                    print("---------------------")

                    # append the dataclasses to the dictionary
                    compiled_text = self.dataclass_compile(col["data"], col["name"])
                    self.dataclasses[col["name"]] = compiled_text
        print("---------------------")
        print("[*] Compilation complete.")
        for compiled_source in self.dataclasses:
            print("[-] {0}]=-----------".format(compiled_source))
            print(self.dataclasses[compiled_source])
        print("---------------------")
        print("Would you like to save these files to 'build/' ?")
        save_files = input("y/n> ")


    # Handle dataclass compilation
    def dataclass_compile(self, schema_map, dataclass_name):
        section = []

        text = "@dataclass \n" \
               "class {0}:\n".format(dataclass_name)

        # just like in SchemaInterpreter, iterate over all the objects in this schema map.
        for obj in schema_map:
            # iterate over all the attributes for this object
            try:
                # if this object is a schema alias
                for attribute in obj:
                    object_type = obj[attribute]["sql_fusion_type"]
                    if object_type == "schema_alias":
                        print("[.] found schema_alias - pretty: {0}, ugly: {1}".format(obj[attribute]["pretty_name"],
                                                                                   attribute))
                        text += self.add_indent(1, "# Database Column: {0}".format(attribute))
                        text += self.add_indent(1, "{0}: {1}".format(obj[attribute]["pretty_name"],
                                                                                       obj[attribute]["datatype"]))
            # if it's not a schema alias, it's gotta be something else...
            except TypeError:
                # maybe it's a column?
                if obj["sql_fusion_type"] == "column":
                    print("[.] found column - {0}".format(obj["name"]))
                    text += self.add_indent(1, "{0}: {1}".format(obj["name"],
                                                                 obj["datatype"]))

                # no... it's gotta be a named_schema_map...
                else:
                    if obj["sql_fusion_type"] == "named_schema_map":
                        print("[!] found nested named_schema_map during another schema_map compilation, appending - {0}".format(obj["name"]))

                        self.dataclasses[obj["name"].title()] = self.dataclass_compile(obj["data"], obj["name"])
        return text

    # quick function to handle indents
    def add_indent(self, tabs, text):
        indent = ""
        for x in range(tabs * 4):
            indent += " "
        return indent + text + "\n"
