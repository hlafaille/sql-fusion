"""
This template is used for defining your schema map. It is a simple Python object.
"""

from objects.SQLColumn import Column
from objects.SchemaAlias import SchemaAlias
from objects.SchemaMap import SchemaMap, RootSchemaMap

schema = RootSchemaMap(columns=[
    Column("id", int),
    SchemaMap(columns=[
        SchemaAlias(database_name="incremental", pretty_name="id", datatype=int),
        SchemaMap(columns=[
            SchemaAlias(database_name="address_line1", pretty_name="line1", datatype=str),
            SchemaAlias(database_name="address_line2", pretty_name="line2", datatype=str),
            SchemaAlias(database_name="address_zip", pretty_name="zip", datatype=str),
            SchemaAlias(database_name="address_city", pretty_name="city", datatype=str),
            SchemaAlias(database_name="address_state", pretty_name="state", datatype=str),
            SchemaAlias(database_name="address_country", pretty_name="country", datatype=str)
        ], group_name="Address")
    ], group_name="Customer")
],
    root_name="MySchemaMap")
