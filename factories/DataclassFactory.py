"""
This object converts an interpreted RootSchemaMap into a Python Dataclass file.
"""

from objects.SchemaInterpreter import SchemaInterpreter
from objects.SchemaMap import RootSchemaMap


class DataclassFactory:
    def __init__(self, root_schema_map: RootSchemaMap):
        # variables
        self.dataclasses = []

        # get interpreted schema map
        self.interpreted_schema = SchemaInterpreter(root_schema_map)

        # iterate over the interpreted root schema map, establish what we're working with
        for x in self.interpreted_schema.get_interpreted():
            print("root_schema_map is {0}".format(x))
            print("---------------------")

            # iterate over the named_schema_maps, those're going to be our data classes.
            for col in self.interpreted_schema.get_interpreted()[x]:
                if col["sql_fusion_type"] == "named_schema_map":
                    # establish some per-dataclass variables (ex: name)
                    dataclass_name = col["name"].title()

                    print("found nested named_schema_map, beginning compilation of {0}".format(dataclass_name))
                    print("---------------------")

                    # append dataclass name so we can keep track for when we compile the root_schema_map
                    self.dataclasses.append(col["name"])

                    # begin with class header
                    beginning_string = "@dataclass \n" \
                                       "class {0}:\n".format(dataclass_name)

                    compiled_text = self.dataclass_compile(col["data"])
                    compiled_text = beginning_string + compiled_text
                    print("---------------------")
                    print(compiled_text)
                    input()

    # Handle dataclass compilation
    def dataclass_compile(self, schema_map):
        section = []
        text = ""

        # just like in SchemaInterpreter, iterate over all the objects in this schema map.
        for obj in schema_map:

            # iterate over all the attributes for this object

            try:
                for attribute in obj:
                        object_type = obj[attribute]["sql_fusion_type"]
                        if object_type == "schema_alias":
                            print("found schema_alias - pretty: {0}, ugly: {1}".format(obj[attribute]["pretty_name"], attribute))
                            text += self.add_indent(1, "{0}: {1}    #Database: {2}".format(obj[attribute]["pretty_name"],
                                                                            obj[attribute]["datatype"],
                                                                              attribute))
            except TypeError:
                if obj["sql_fusion_type"] == "column":
                    print("found column - {0}".format(obj["name"]))
                    text += self.add_indent(1, "{0}: {1}".format(obj["name"],
                                                                 obj["datatype"]))

        return text

    # quick function to handle indents
    def add_indent(self, tabs, text):
        indent = ""
        for x in range(tabs * 4):
            indent += " "
        return indent + text + "\n"