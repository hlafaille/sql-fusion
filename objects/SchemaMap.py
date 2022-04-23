"""
This object is used for storing a database schema (aka structure). Will allow for mapping to JSON and dataclass.
It is effectively your lowest level of data abstraction, where the raw data format is before any organization by JSON or
dataclasses. Note the nesting features of the SchemaMap, this is how you will also define your API structure.
SchemaMap takes one required argument, 'columns'. It is also able to take an optional 'name' column.


Example of SQL Schema to SchemaMap translation in a Sales Order:

SQL: id, address_line1, address_line2, customer_name, zip

SchemaMap:
    schema = SchemaMap(
        [
            Column("isn", int),
            SchemaMap(columns=[
                SchemaAlias("customer_name", "name", str),
                SchemaAlias("customer_address_line1", "line1", str),
                SchemaAlias("customer_address_line2", "line2", str),
                SchemaAlias("customer_address_zip", "zip", int)],
                group_name="customer"),
            SchemaMap(columns=[
                Column("id", int),
                SchemaAlias("first_name", "firstName", str),
                SchemaAlias("last_name", "lastName", str),
                Column("status", str)
            ],
                group_name="employee")
        ])
"""

from exceptions import ColumnExistsException


class SchemaMap:
    def __init__(self, columns, group_name):
        self.group_name = group_name

        # where we actually store the SchemaMaps
        self.columns = []

        # if there was no group name passed
        for col in columns:
            self.add_column(col)

    def __iter__(self):
        return iter(self.columns)

    # adds a column to the schema map
    def add_column(self, column_name):
        # test if a group_name was passed
        self.columns.append(column_name)

        # test if the column is already in the map
        if column_name not in self.columns:
            self.columns.append(column_name)
        else:
            pass
            #print(self.columns)
            #raise ColumnExistsException("Column '{0}' already exists in the schema map. ".format(column_name))

    def add_schema_group(self, columns, group_name):
        temp_group = {"schema_group_name": group_name,
                      "columns": columns}
        self.columns.append(temp_group)


class RootSchemaMap:
    def __init__(self, columns, root_name):
        self.root_name = root_name

        # where we actually store the SchemaMaps
        self.columns = []

        # if there was no group name passed
        for col in columns:
            self.add_column(col)

    def __iter__(self):
        return iter(self.columns)

    # adds a column to the schema map
    def add_column(self, column_name):
        # test if a group_name was passed
        self.columns.append(column_name)

        # test if the column is already in the map
        if column_name not in self.columns:
            self.columns.append(column_name)
        else:
            pass
            #print(self.columns)
            #raise ColumnExistsException("Column '{0}' already exists in the schema map. ".format(column_name))

    def add_schema_group(self, columns, group_name):
        temp_group = {"schema_group_name": group_name,
                      "columns": columns}
        self.columns.append(temp_group)