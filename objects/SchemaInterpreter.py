"""
This object interprets a SchemaMap, compiles it into a JSON format which can be used to create dataclasses.
"""
from objects.SQLColumn import Column
from objects.SchemaMap import SchemaMap
from objects.SchemaAlias import SchemaAlias


class SchemaInterpreter:
    def __init__(self, schema_map: SchemaMap):
        self.master_json = []
        self.count = 0
        self.schema_map_interpreter(schema_map)

    def column_interpreter(self, column: Column):
        #print("column {0} with datatype {1}".format(column.name, column.python_datatype))
        return {column.name: column.python_datatype}

    def schema_map_interpreter(self, schema_map: SchemaMap, name=""):
        section = []

        # begin interpretation
        for column in schema_map:
            # if this entry in the schema map is a lone column (ex: primary key)
            if type(column) == Column:
                section.append(self.column_interpreter(column))

            # if this entry is a nested schema map (call schema map interpreter) (ex: customer data)
            elif type(column) == SchemaMap:
                self.schema_map_interpreter(column)

            # if this entry is a nested schema alias (call schema alias interpreter)
            elif type(column) == SchemaAlias:
                 section.append(self.schema_alias_interpreter(column))

            # if this entry is a dictionary (used in a named SchemaMap)
            elif type(column) == dict:
                # iterate over the objects in the schema map
                section.append(self.named_schema_map_interpreter(column))

        if len(section) == 1:
            self.master_json.append(section[0])
        else:
            self.master_json.append(section)

    # handles a named schema map (dict)
    def named_schema_map_interpreter(self, named_schema_map: dict):
        #self.schema_map_interpreter(named_schema_map["columns"], name=named_schema_map["schema_group_name"])

        section = []

        # begin interpretation
        for column in named_schema_map["columns"]:

            # if this entry in the schema map is a lone column (ex: primary key)
            if type(column) == Column:
                section.append(self.column_interpreter(column))

            # if this entry is a nested schema map (call schema map interpreter) (ex: customer data)
            elif type(column) == SchemaMap:
                self.schema_map_interpreter(column)

            # if this entry is a nested schema alias (call schema alias interpreter)
            elif type(column) == SchemaAlias:
                 section.append(self.schema_alias_interpreter(column))

            # if this entry is a dictionary (used in a named SchemaMap)
            elif type(column) == dict:
                # iterate over the objects in the schema map
                self.named_schema_map_interpreter(column)

        testy = {named_schema_map["schema_group_name"]: section}
        return testy

    def schema_alias_interpreter(self, schema_alias: SchemaAlias):
        # returns dict
        return {schema_alias.database_name: {"pretty_name": schema_alias.pretty_name, "datatype": schema_alias.datatype}}
