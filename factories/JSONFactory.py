import json
import os.path

from objects.SQLColumn import Column
from objects.SchemaAlias import SchemaAlias
from objects.SchemaMap import RootSchemaMap, SchemaMap


class JSONFactory:
    def __init__(self, schema_map: RootSchemaMap, project_name):
        self.schema_map = schema_map
        self.project_name = project_name
        self.columns = {project_name: []}

        # entrypoint
        self.iterate_root_schema_map(schema_map)

        with open(os.path.join("build", project_name, "{0}.json".format(project_name)), "w") as file:
            file.write(json.dumps(self.columns, indent=4))

        print("[*] json compilation complete, returning to prompt")

    # iterate over the schema map
    def iterate_root_schema_map(self, schema_map):
        temp = {}
        print("---------------------")
        print("[.] beginning json compilation")
        for obj in schema_map:
            if type(obj) == Column:
                print("[.] found column - {0}".format(obj.name))
                temp[obj.name] = str(obj.python_datatype.__name__)

            elif type(obj) == SchemaMap:
                print("[.] found schema map, entering tree - {0}".format(obj.group_name))
                self.columns[self.project_name].append(self.iterate_schema_map(obj))

            elif type(obj) == SchemaAlias:
                print("[.] found schema alias - {0}".format(obj.database_name))
                temp[obj.pretty_name] = str(obj.datatype.__name__)

        self.columns[self.project_name].append(temp)

    # iterate over the schema map
    def iterate_schema_map(self, schema_map):
        temp = {schema_map.group_name: {}}

        print("---------------------")
        print("[.] beginning json compilation")
        for obj in schema_map:
            if type(obj) == Column:
                print("[.] found column - {0}".format(obj.name))
                temp[schema_map.group_name][obj.name] = str(obj.python_datatype.__name__)

            elif type(obj) == SchemaMap:
                print("[.] found schema map, entering tree - {0}".format(obj.group_name))
                temp[schema_map.group_name][obj.group_name] = self.iterate_schema_map(obj)

            elif type(obj) == SchemaAlias:
                print("[.] found schema alias - {0}".format(obj.database_name))
                temp[schema_map.group_name][obj.pretty_name] = str(obj.datatype.__name__)

        return temp
