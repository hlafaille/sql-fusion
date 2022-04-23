"""
This is a small tool class that simply holds a key value pair, one pretty name for the API and one database name
for referencing the table.

SchemaAlias use case:
------
Instead of having this be our JSON response:
{
    "customer_name": "Tim the Enchanter",
    "customer_address_line1": "123 Monty Python Way",
    "customer_address_line2": "Apartment 45",
    "customer_address_zip": 6789
}

We can utilize SchemaAliases and SchemaMaps to nest this for the sql-fusion dataclass compiler and JSON serializer to understand.

SchemaMap/SchemaAlias example:
------
    schema = SchemaMap(
        ["isn",
         SchemaMap(columns=[
             SchemaAlias("customer_name", "name"),
             SchemaAlias("customer_address_line1", "line1"),
             SchemaAlias("customer_address_line2", "line2"),
             SchemaAlias("customer_address_zip", "zip"),
         ],
         group_name="customer")]
    )

Using a SchemaMap in combination with SchemaAliases will bind our linear database columns into a tree like structure,
absolutely perfect... even though not many people will see it. It's the thought that counts, right?

"""


class SchemaAlias:
    def __init__(self, database_name, pretty_name):
        self.pretty_name = pretty_name
        self.database_name = database_name
