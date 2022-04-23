from objects.SchemaAlias import SchemaAlias
from objects.SchemaMap import SchemaMap

if __name__ == "__main__":
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
