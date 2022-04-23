"""
This object interprets a SchemaMap, compiles it into a JSON format which can be used to create dataclasses.
"""
from objects.SQLColumn import Column
from objects.SchemaMap import SchemaMap, RootSchemaMap
from objects.SchemaAlias import SchemaAlias


class SchemaInterpreter:
    def __init__(self, schema_map: RootSchemaMap):
        self.master_json = {}

        # how many kinds of dataclasses do we need to establish?
        self.dataclass_types = []

        # entrypoint
        self.root_schema_map_interpreter(schema_map)

    # interprets exact name columns (ex: database name is the same as this objects)
    def column_interpreter(self, column: Column):
        return {"name": column.name, "datatype": column.python_datatype}

    def root_schema_map_interpreter(self, root_schema_map):
        self.master_json[root_schema_map.root_name] = []

        # begin interpretation
        for column in root_schema_map:
            # if this entry in the schema map is a lone column (ex: primary key)
            if type(column) == Column:
                self.master_json[root_schema_map.root_name].append(self.column_interpreter(column))

            # if this entry is a nested schema map (call schema map interpreter) (ex: customer data)
            elif type(column) == SchemaMap:
                self.master_json[root_schema_map.root_name].append(self.schema_map_interpreter(column))

            # if this entry is a nested schema alias (call schema alias interpreter)
            elif type(column) == SchemaAlias:
                self.master_json[root_schema_map.root_name].append(self.schema_alias_interpreter(column))

            # if this is an unknown type to the interpreter
            else:
                raise TypeError("Unsupported sql-fusion type {0} in RootSchemaMap. Possibly have RootSchemaMap and SchemaMap confused? Check out the documentation!".format(type(column)))

    # interprets schema maps, possible recursive function.
    def schema_map_interpreter(self, schema_map):
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

            # if this is an unknown type to the interpreter
            else:
                raise TypeError("Unsupported sql-fusion type {0} with value '{1}', please read the documentation.".format(type(column), column))

        if len(section) == 1:
            return section[0]
        else:
            return section

    # handles a named schema map (dict)
    def named_schema_map_interpreter(self, named_schema_map: dict):
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

    # handles interpretation of schema aliases (ex: translates linear database columns to pretty key-value nested pairs)
    def schema_alias_interpreter(self, schema_alias: SchemaAlias):
        # returns dict
        return {schema_alias.database_name: {"pretty_name": schema_alias.pretty_name, "datatype": schema_alias.datatype}}
