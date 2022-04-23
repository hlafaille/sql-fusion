import pprint

from factories.DataclassFactory import DataclassFactory
from objects.SQLColumn import Column
from objects.SchemaAlias import SchemaAlias
from objects.SchemaInterpreter import SchemaInterpreter
from objects.SchemaMap import SchemaMap, RootSchemaMap

if __name__ == "__main__":
    schema = RootSchemaMap(
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
                Column("status", str),
                Column("email", str),
                SchemaMap(columns=[
                    Column("sales", float),
                    Column("purchasing", float)
                ],
                    group_name="commission"),
            ],
                group_name="employee")
        ],
        root_name="sales_order"
    )

    dataclass_factory = DataclassFactory(schema)
